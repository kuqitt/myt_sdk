"""MYT SDK 命令行接口模块"""

import argparse
import logging
import sys
from typing import List, Optional

from . import __version__
from .exceptions import MYTSDKError
from .sdk_manager import MYTSDKManager

logger = logging.getLogger(__name__)


def setup_logging(level: str = "INFO", log_file: Optional[str] = None) -> None:
    """
    设置日志配置

    Args:
        level: 日志级别
        log_file: 日志文件路径（可选）
    """
    log_level = getattr(logging, level.upper(), logging.INFO)

    # 基本配置
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 如果指定了日志文件，添加文件处理器
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(log_level)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)

        # 获取根日志器并添加文件处理器
        root_logger = logging.getLogger()
        root_logger.addHandler(file_handler)


def create_parser() -> argparse.ArgumentParser:
    """
    创建命令行参数解析器

    Returns:
        参数解析器
    """
    parser = argparse.ArgumentParser(
        prog="myt-sdk",
        description="MYT SDK - 魔云腾SDK通用包命令行工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("--version", action="version", version=f"MYT SDK {__version__}")

    parser.add_argument("--verbose", "-v", action="store_true", help="启用详细输出")

    parser.add_argument("--log-file", type=str, help="日志文件路径")

    parser.add_argument("--cache-dir", type=str, help="自定义缓存目录路径")

    # 子命令
    subparsers = parser.add_subparsers(
        dest="command", help="可用命令", metavar="COMMAND"
    )

    # init 命令
    init_parser = subparsers.add_parser("init", help="初始化MYT SDK（下载并启动）")
    init_parser.add_argument("--force", action="store_true", help="强制重新下载SDK")
    init_parser.add_argument("--no-start", action="store_true", help="只下载不启动SDK")
    init_parser.add_argument(
        "--daemon", action="store_true", help="以守护进程模式运行，保持CLI进程不退出"
    )

    # status 命令（隐藏命令，用于调试）
    status_parser = subparsers.add_parser("status", help="查看SDK状态信息")

    return parser


def cmd_init(args) -> int:
    """
    处理 init 命令

    Args:
        args: 命令行参数

    Returns:
        退出码
    """
    try:
        # 创建SDK管理器
        sdk_manager = MYTSDKManager(cache_dir=args.cache_dir)

        print("=== MYT SDK 初始化 ===")
        print(f"缓存目录: {sdk_manager.cache_dir}")
        print(f"SDK版本: {sdk_manager.SDK_VERSION}")
        print()

        # 检查当前状态
        status = sdk_manager.get_status()
        print(f"当前状态:")
        print(f"  已安装: {status['installed']}")
        print(f"  正在运行: {status['running']}")
        print()

        if args.no_start:
            # 只下载不启动
            if not status["installed"] or args.force:
                print("开始下载SDK...")
                sdk_manager.download_sdk(force=args.force)
                print("SDK下载完成")
            else:
                print("SDK已存在，跳过下载")
            return 0

        # 完整初始化
        print("开始初始化SDK...")
        result = sdk_manager.init(force=args.force)

        print("=== 初始化结果 ===")
        print(f"状态: {result['status']}")
        print(f"消息: {result['message']}")
        print(f"SDK已安装: {result['installed']}")
        print(f"SDK正在运行: {result['running']}")
        print(f"SDK路径: {result['sdk_path']}")

        # 守护进程模式
        if args.daemon and result["running"]:
            print("\n=== 守护进程模式 ===")
            print("CLI将保持运行以监控SDK进程状态")
            print("按 Ctrl+C 退出")
            print()

            try:
                import time

                while True:
                    # 每30秒检查一次SDK状态
                    time.sleep(30)
                    if not sdk_manager.is_sdk_running():
                        print("检测到SDK进程已停止，正在重新启动...")
                        try:
                            sdk_manager.start_sdk()
                            print("SDK进程重新启动成功")
                        except Exception as e:
                            print(f"重新启动SDK失败: {e}")
                            return 1
                    else:
                        print(f"SDK进程运行正常 [{time.strftime('%Y-%m-%d %H:%M:%S')}]")
            except KeyboardInterrupt:
                print("\n收到退出信号，停止守护进程")
                return 0

        return 0 if result["status"] in ["already_running", "started", "ready"] else 1

    except MYTSDKError as e:
        logger.error(f"SDK初始化失败: {e}")
        print(f"错误: {e}")
        return 1
    except Exception as e:
        logger.error(f"未知错误: {e}")
        print(f"未知错误: {e}")
        return 1


def cmd_status(args) -> int:
    """
    处理 status 命令

    Args:
        args: 命令行参数

    Returns:
        退出码
    """
    try:
        sdk_manager = MYTSDKManager(cache_dir=args.cache_dir)
        status = sdk_manager.get_status()

        print("=== MYT SDK 状态 ===")
        print(f"版本: {status['version']}")
        print(f"已安装: {status['installed']}")
        print(f"正在运行: {status['running']}")
        print(f"SDK路径: {status['sdk_path']}")
        print(f"缓存目录: {status['cache_dir']}")
        print(f"下载地址: {status['download_url']}")

        return 0

    except Exception as e:
        logger.error(f"获取状态失败: {e}")
        print(f"错误: {e}")
        return 1


def main(argv: Optional[List[str]] = None) -> int:
    """
    主入口函数

    Args:
        argv: 命令行参数列表

    Returns:
        退出码
    """
    parser = create_parser()
    args = parser.parse_args(argv)

    # 设置日志
    log_level = "DEBUG" if args.verbose else "INFO"
    setup_logging(log_level, args.log_file)

    logger.info(f"MYT SDK v{__version__} 启动")

    # 如果没有指定命令，显示帮助
    if not args.command:
        parser.print_help()
        return 0

    # 执行对应的命令
    command_handlers = {
        "init": cmd_init,
        "status": cmd_status,
    }

    handler = command_handlers.get(args.command)
    if handler:
        return handler(args)
    else:
        print(f"未知命令: {args.command}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
