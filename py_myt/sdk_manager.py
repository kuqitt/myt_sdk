"""MYT SDK 管理器模块"""

import logging
import os
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Any, Dict, Optional
from urllib.parse import urlparse

import psutil
import requests

from .exceptions import (
    MYTSDKDownloadError,
    MYTSDKError,
    MYTSDKFileError,
    MYTSDKProcessError,
)

logger = logging.getLogger(__name__)


class MYTSDKManager:
    """MYT SDK 管理器"""

    # SDK配置
    SDK_VERSION = "1.0.14.30.25"
    SDK_DOWNLOAD_URL = "http://d.moyunteng.com/sdk/myt_sdk_1.0.14.30.25.zip"
    SDK_EXECUTABLE = "myt_sdk/myt_sdk.exe"
    SDK_NAME = 'myt_sdk.exe'
    def __init__(self, cache_dir: Optional[str] = None):
        """
        初始化SDK管理器

        Args:
            cache_dir: 自定义缓存目录，如果为None则使用系统默认缓存目录
        """
        self.cache_dir = Path(cache_dir) if cache_dir else self._get_default_cache_dir()
        self.sdk_dir = self.cache_dir / "myt_sdk" / self.SDK_VERSION
        self.sdk_executable_path = self.sdk_dir / self.SDK_EXECUTABLE

        # 确保缓存目录存在
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"MYT SDK Manager 初始化完成，缓存目录: {self.cache_dir}")

    def _get_default_cache_dir(self) -> Path:
        """
        获取默认缓存目录

        Returns:
            默认缓存目录路径
        """
        if sys.platform == "win32":
            # Windows: %LOCALAPPDATA%\MYT_SDK
            cache_base = os.environ.get(
                "LOCALAPPDATA", os.path.expanduser("~\\AppData\\Local")
            )
        elif sys.platform == "darwin":
            # macOS: ~/Library/Caches/MYT_SDK
            cache_base = os.path.expanduser("~/Library/Caches")
        else:
            # Linux: ~/.cache/MYT_SDK
            cache_base = os.environ.get(
                "XDG_CACHE_HOME", os.path.expanduser("~/.cache")
            )

        return Path(cache_base) / "MYT_SDK"

    def is_sdk_installed(self) -> bool:
        """
        检查SDK是否已安装

        Returns:
            True如果SDK已安装，否则False
        """
        return self.sdk_executable_path.exists() and self.sdk_executable_path.is_file()

    def is_sdk_running(self) -> bool:
        """
        检查SDK进程是否正在运行

        Returns:
            True如果SDK进程正在运行，否则False
        """
        try:
            for proc in psutil.process_iter(["pid", "name", "exe"]):
                try:
                    if (
                        proc.info["name"]
                        and self.SDK_EXECUTABLE.lower() in proc.info["name"].lower()
                    ):
                        return True
                    if (
                        proc.info["exe"]
                        and str(self.sdk_executable_path).lower()
                        in proc.info["exe"].lower()
                    ):
                        return True
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            return False
        except Exception as e:
            logger.warning(f"检查SDK进程状态时出错: {e}")
            return False

    def download_sdk(self, force: bool = False) -> None:
        """
        下载SDK

        Args:
            force: 是否强制重新下载

        Raises:
            MYTSDKDownloadError: 下载失败时抛出
        """
        if self.is_sdk_installed() and not force:
            logger.info("SDK已存在，跳过下载")
            return

        logger.info(f"开始下载SDK: {self.SDK_DOWNLOAD_URL}")

        try:
            # 创建临时文件
            with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as temp_file:
                temp_path = Path(temp_file.name)

            # 下载文件
            response = requests.get(self.SDK_DOWNLOAD_URL, stream=True, timeout=30)
            response.raise_for_status()

            total_size = int(response.headers.get("content-length", 0))
            downloaded_size = 0

            with open(temp_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)

                        # 简单的进度显示
                        if total_size > 0:
                            progress = (downloaded_size / total_size) * 100
                            logger.debug(f"下载进度: {progress:.1f}%")

            logger.info(f"SDK下载完成: {temp_path}")

            # 解压文件
            self._extract_sdk(temp_path)

            # 清理临时文件
            temp_path.unlink()

        except requests.RequestException as e:
            raise MYTSDKDownloadError(
                f"下载SDK失败: {str(e)}",
                url=self.SDK_DOWNLOAD_URL,
                status_code=(
                    getattr(e.response, "status_code", None)
                    if hasattr(e, "response")
                    else None
                ),
            )
        except Exception as e:
            raise MYTSDKDownloadError(f"下载SDK时发生未知错误: {str(e)}")

    def _extract_sdk(self, zip_path: Path) -> None:
        """
        解压SDK文件

        Args:
            zip_path: ZIP文件路径

        Raises:
            MYTSDKFileError: 解压失败时抛出
        """
        try:
            logger.info(f"开始解压SDK: {zip_path} -> {self.sdk_dir}")

            # 确保目标目录存在
            self.sdk_dir.mkdir(parents=True, exist_ok=True)

            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                # 先列出ZIP文件内容
                file_list = zip_ref.namelist()
                logger.debug(f"ZIP文件内容: {file_list[:10]}...")  # 只显示前10个文件

                # 解压所有文件
                zip_ref.extractall(self.sdk_dir)

            logger.info("SDK解压完成")

            # 查找可执行文件（保持原始目录结构）
            exe_found = False
            actual_exe_path = None
            for root, dirs, files in os.walk(self.sdk_dir):
                for file in files:
                    if file.lower() == self.SDK_EXECUTABLE.lower():
                        actual_exe_path = Path(root) / file
                        logger.info(f"找到SDK可执行文件: {actual_exe_path}")

                        # 更新可执行文件路径为实际位置（不移动文件，保持目录结构）
                        self.sdk_executable_path = actual_exe_path

                        exe_found = True
                        break
                if exe_found:
                    break

            # 验证可执行文件是否存在
            if not exe_found or not self.sdk_executable_path.exists():
                # 列出解压后的所有文件用于调试
                all_files = []
                for root, dirs, files in os.walk(self.sdk_dir):
                    for file in files:
                        all_files.append(str(Path(root) / file))

                logger.error(
                    f"解压后的文件列表: {all_files[:20]}..."
                )  # 只显示前20个文件

                raise MYTSDKFileError(
                    f"解压后未找到SDK可执行文件: {self.sdk_executable_path}",
                    file_path=str(self.sdk_executable_path),
                )

        except zipfile.BadZipFile as e:
            raise MYTSDKFileError(f"无效的ZIP文件: {str(e)}", file_path=str(zip_path))
        except Exception as e:
            raise MYTSDKFileError(f"解压SDK失败: {str(e)}", file_path=str(zip_path))

    def _prepare_sdk_environment(self) -> None:
        """
        准备SDK运行环境

        创建必要的目录和文件
        """
        try:
            # 使用SDK可执行文件所在目录作为基础目录
            sdk_base_dir = self.sdk_executable_path.parent

            # 创建conf目录
            conf_dir = sdk_base_dir / "conf"
            conf_dir.mkdir(exist_ok=True)

            # 创建pid文件（如果不存在）
            pid_file = conf_dir / "myt.pid"
            if not pid_file.exists():
                pid_file.write_text("0", encoding="utf-8")

            logger.info(f"SDK运行环境准备完成: {conf_dir}")

        except Exception as e:
            logger.warning(f"准备SDK运行环境时出错: {e}")

    def start_sdk(self, wait: bool = False) -> subprocess.Popen:
        """
        启动SDK进程

        Args:
            wait: 是否等待进程结束

        Returns:
            启动的进程对象

        Raises:
            MYTSDKProcessError: 启动失败时抛出
        """
        if not self.is_sdk_installed():
            raise MYTSDKProcessError(
                "SDK未安装，请先运行初始化", process_name=self.SDK_EXECUTABLE
            )

        if self.is_sdk_running():
            logger.info("SDK进程已在运行")
            # 返回一个虚拟的进程对象
            return None

        try:
            # 准备SDK运行环境
            self._prepare_sdk_environment()

            logger.info(f"启动SDK进程: {self.sdk_executable_path}")

            # 启动进程（后台运行，不显示窗口）
            creation_flags = 0
            if sys.platform == "win32":
                # Windows下隐藏窗口并创建新进程组
                creation_flags = (
                    subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP
                )

            # 创建日志文件用于调试
            log_file = self.sdk_dir / "sdk_output.log"

            with open(log_file, "w", encoding="utf-8") as log_f:
                process = subprocess.Popen(
                    [str(self.sdk_executable_path)],
                    cwd=str(self.sdk_dir),
                    stdout=log_f,
                    stderr=subprocess.STDOUT,
                    stdin=subprocess.DEVNULL,
                    creationflags=creation_flags,
                )

            # 等待一小段时间确保进程启动
            import time

            time.sleep(1)

            # 检查进程是否还在运行
            if process.poll() is not None:
                # 进程已退出，读取日志
                try:
                    with open(log_file, "r", encoding="utf-8") as f:
                        output = f.read()
                    logger.error(f"SDK进程启动后立即退出，退出码: {process.returncode}")
                    logger.error(f"SDK输出: {output}")
                    raise MYTSDKProcessError(
                        f"SDK进程启动失败，退出码: {process.returncode}",
                        process_name=self.SDK_EXECUTABLE,
                        exit_code=process.returncode,
                    )
                except Exception as e:
                    logger.error(f"读取SDK日志失败: {e}")
                    raise MYTSDKProcessError(
                        f"SDK进程启动失败，退出码: {process.returncode}",
                        process_name=self.SDK_EXECUTABLE,
                        exit_code=process.returncode,
                    )

            if wait:
                process.wait()

            logger.info(f"SDK进程启动成功，PID: {process.pid}")
            return process

        except FileNotFoundError:
            raise MYTSDKProcessError(
                f"找不到SDK可执行文件: {self.sdk_executable_path}",
                process_name=self.SDK_EXECUTABLE,
            )
        except Exception as e:
            raise MYTSDKProcessError(
                f"启动SDK进程失败: {str(e)}", process_name=self.SDK_EXECUTABLE
            )

    def stop_sdk(self, force: bool = False, timeout: int = 10) -> Dict[str, Any]:
        """
        停止SDK进程

        Args:
            force: 是否强制终止进程
            timeout: 等待进程正常退出的超时时间（秒）

        Returns:
            停止操作的结果信息

        Raises:
            MYTSDKProcessError: 停止失败时抛出
        """
        if not self.is_sdk_running():
            logger.info("SDK进程未运行")
            return {
                "status": "not_running",
                "message": "SDK进程未运行",
                "stopped_processes": 0
            }

        stopped_processes = 0
        failed_processes = []

        try:
            logger.info("开始停止SDK进程")

            # 查找所有相关的SDK进程
            sdk_processes = []
            for proc in psutil.process_iter(["pid", "name", "exe"]):
                try:
                    if (
                        proc.info["name"]
                        and self.SDK_NAME.lower() in proc.info["name"].lower()
                    ):
                        sdk_processes.append(proc)
                    elif (
                        proc.info["exe"]
                        and str(self.sdk_executable_path).lower()
                        in proc.info["exe"].lower()
                    ):
                        sdk_processes.append(proc)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            if not sdk_processes:
                logger.info("未找到运行中的SDK进程")
                return {
                    "status": "not_found",
                    "message": "未找到运行中的SDK进程",
                    "stopped_processes": 0
                }

            # 尝试优雅地停止进程
            for proc in sdk_processes:
                try:
                    logger.info(f"尝试停止SDK进程 PID: {proc.pid}")
                    
                    if force:
                        # 强制终止
                        proc.kill()
                        logger.info(f"强制终止进程 PID: {proc.pid}")
                    else:
                        # 优雅停止
                        proc.terminate()
                        logger.info(f"发送终止信号到进程 PID: {proc.pid}")
                        
                        # 等待进程退出
                        try:
                            proc.wait(timeout=timeout)
                            logger.info(f"进程 PID: {proc.pid} 已正常退出")
                        except psutil.TimeoutExpired:
                            logger.warning(f"进程 PID: {proc.pid} 在{timeout}秒内未退出，强制终止")
                            proc.kill()
                            proc.wait(timeout=5)  # 等待强制终止完成
                            logger.info(f"强制终止进程 PID: {proc.pid} 完成")
                    
                    stopped_processes += 1
                    
                except psutil.NoSuchProcess:
                    logger.info(f"进程 PID: {proc.pid} 已不存在")
                    stopped_processes += 1
                except psutil.AccessDenied as e:
                    logger.error(f"无权限停止进程 PID: {proc.pid}: {e}")
                    failed_processes.append({"pid": proc.pid, "error": "权限不足"})
                except Exception as e:
                    logger.error(f"停止进程 PID: {proc.pid} 时出错: {e}")
                    failed_processes.append({"pid": proc.pid, "error": str(e)})

            # 验证是否还有进程在运行
            if self.is_sdk_running():
                remaining_msg = "部分SDK进程可能仍在运行"
                logger.warning(remaining_msg)
                if failed_processes:
                    return {
                        "status": "partial_success",
                        "message": remaining_msg,
                        "stopped_processes": stopped_processes,
                        "failed_processes": failed_processes
                    }
                else:
                    return {
                        "status": "partial_success",
                        "message": remaining_msg,
                        "stopped_processes": stopped_processes
                    }
            else:
                success_msg = f"成功停止 {stopped_processes} 个SDK进程"
                logger.info(success_msg)
                result = {
                    "status": "success",
                    "message": success_msg,
                    "stopped_processes": stopped_processes
                }
                if failed_processes:
                    result["failed_processes"] = failed_processes
                return result

        except Exception as e:
            error_msg = f"停止SDK进程时发生错误: {str(e)}"
            logger.error(error_msg)
            raise MYTSDKProcessError(
                error_msg,
                process_name=self.SDK_EXECUTABLE
            )

    def init(self, force: bool = False, start_sdk: bool = True) -> Dict[str, Any]:
        """
        初始化SDK（下载并启动）

        Args:
            force: 是否强制重新下载
            start_sdk: 是否启动SDK进程

        Returns:
            初始化结果信息

        Raises:
            MYTSDKError: 初始化失败时抛出
        """
        try:
            logger.info("开始初始化MYT SDK")

            # 检查是否已在运行
            if self.is_sdk_running() and not force:
                return {
                    "status": "already_running",
                    "message": "SDK已在运行",
                    "installed": True,
                    "running": True,
                    "sdk_path": str(self.sdk_executable_path),
                    "cache_dir": str(self.cache_dir),
                }

            # 检查是否需要下载
            if not self.is_sdk_installed() or force:
                logger.info("开始下载SDK")
                self.download_sdk(force=force)
                logger.info("SDK下载完成")

            # 是否启动SDK
            if start_sdk and not self.is_sdk_running():
                process = self.start_sdk()
                return {
                    "status": "started",
                    "message": "SDK已成功启动",
                    "installed": True,
                    "running": True,
                    "pid": process.pid if process else None,
                    "sdk_path": str(self.sdk_executable_path),
                    "cache_dir": str(self.cache_dir),
                }
            else:
                return {
                    "status": "ready",
                    "message": "SDK已准备就绪",
                    "installed": True,
                    "running": self.is_sdk_running(),
                    "sdk_path": str(self.sdk_executable_path),
                    "cache_dir": str(self.cache_dir),
                }

        except Exception as e:
            logger.error(f"MYT SDK初始化失败: {e}")
            raise

    def get_status(self) -> Dict[str, Any]:
        """
        获取SDK状态信息

        Returns:
            SDK状态信息
        """
        return {
            "version": self.SDK_VERSION,
            "installed": self.is_sdk_installed(),
            "running": self.is_sdk_running(),
            "sdk_path": str(self.sdk_executable_path),
            "cache_dir": str(self.cache_dir),
            "download_url": self.SDK_DOWNLOAD_URL,
        }
