"""MYT SDK Manager测试模块"""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

from py_myt.exceptions import MYTSDKDownloadError, MYTSDKProcessError
from py_myt.sdk_manager import MYTSDKManager


class TestMYTSDKManager(unittest.TestCase):
    """MYT SDK Manager测试类"""

    def setUp(self):
        """测试前准备"""
        self.temp_dir = tempfile.mkdtemp()
        self.sdk_manager = MYTSDKManager(cache_dir=self.temp_dir)

    def tearDown(self):
        """测试后清理"""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_init_default_cache_dir(self):
        """测试默认缓存目录初始化"""
        manager = MYTSDKManager()
        self.assertIsNotNone(manager.cache_dir)
        self.assertTrue(manager.cache_dir.exists())

    def test_init_custom_cache_dir(self):
        """测试自定义缓存目录初始化"""
        custom_dir = Path(self.temp_dir) / "custom_cache"
        manager = MYTSDKManager(cache_dir=str(custom_dir))
        self.assertEqual(manager.cache_dir, custom_dir)
        self.assertTrue(manager.cache_dir.exists())

    def test_is_sdk_installed_false(self):
        """测试SDK未安装的情况"""
        self.assertFalse(self.sdk_manager.is_sdk_installed())

    def test_is_sdk_installed_true(self):
        """测试SDK已安装的情况"""
        # 创建模拟的SDK可执行文件
        sdk_path = self.sdk_manager.sdk_executable_path
        sdk_path.parent.mkdir(parents=True, exist_ok=True)
        sdk_path.touch()

        self.assertTrue(self.sdk_manager.is_sdk_installed())

    @patch("py_myt.sdk_manager.psutil.process_iter")
    def test_is_sdk_running_false(self, mock_process_iter):
        """测试SDK未运行的情况"""
        mock_process_iter.return_value = []
        self.assertFalse(self.sdk_manager.is_sdk_running())

    @patch("py_myt.sdk_manager.psutil.process_iter")
    def test_is_sdk_running_true(self, mock_process_iter):
        """测试SDK正在运行的情况"""

        # 创建一个模拟进程，其中包含 myt_sdk.exe
        def mock_iter(attrs):
            mock_process = Mock()
            mock_process.info = {"name": "myt_sdk.exe", "pid": 12345, "exe": None}
            return [mock_process]

        mock_process_iter.side_effect = mock_iter

        self.assertTrue(self.sdk_manager.is_sdk_running())

    def test_get_status(self):
        """测试获取状态"""
        status = self.sdk_manager.get_status()

        self.assertIn("installed", status)
        self.assertIn("running", status)
        self.assertIn("cache_dir", status)
        self.assertIn("sdk_path", status)
        self.assertIsInstance(status["installed"], bool)
        self.assertIsInstance(status["running"], bool)

    @patch("py_myt.sdk_manager.zipfile.ZipFile")
    @patch("requests.get")
    def test_download_sdk_success(self, mock_get, mock_zipfile):
        """测试下载SDK成功"""
        # 模拟HTTP响应
        mock_response = Mock()
        mock_response.headers = {"content-length": "1000"}
        mock_response.iter_content.return_value = [b"fake_zip_content"]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # 模拟ZIP文件
        mock_zip = Mock()
        mock_zip.namelist.return_value = ["myt_sdk/myt_sdk.exe", "myt_sdk/config.json"]
        mock_zipfile.return_value.__enter__.return_value = mock_zip

        # 模拟SDK未安装，强制下载
        with patch.object(self.sdk_manager, "is_sdk_installed", return_value=False):
            # 创建模拟的SDK可执行文件（在解压后）
            def create_sdk_file(path):
                # 创建完整的目录结构
                sdk_dir = Path(path)
                sdk_dir.mkdir(parents=True, exist_ok=True)

                # 创建 myt_sdk 子目录
                myt_sdk_dir = sdk_dir / "myt_sdk"
                myt_sdk_dir.mkdir(exist_ok=True)

                # 创建可执行文件
                exe_path = myt_sdk_dir / "myt_sdk.exe"
                exe_path.touch()

            mock_zip.extractall.side_effect = create_sdk_file

            self.sdk_manager.download_sdk()

            mock_get.assert_called_once()
            mock_zip.extractall.assert_called_once()

    @patch("py_myt.sdk_manager.requests.get")
    def test_download_sdk_http_error(self, mock_get):
        """测试SDK下载HTTP错误"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = Exception("HTTP 404")
        mock_get.return_value = mock_response

        with self.assertRaises(MYTSDKDownloadError):
            self.sdk_manager.download_sdk()

    @patch("subprocess.Popen")
    def test_start_sdk_success(self, mock_popen):
        """测试启动SDK - 成功"""
        # 创建模拟的SDK可执行文件
        sdk_path = self.sdk_manager.sdk_executable_path
        sdk_path.parent.mkdir(parents=True, exist_ok=True)
        sdk_path.touch()

        # 模拟SDK已安装
        with patch.object(self.sdk_manager, "is_sdk_installed", return_value=True):
            mock_process = MagicMock()
            mock_process.pid = 12345
            mock_process.poll.return_value = None  # 进程仍在运行
            mock_process.returncode = None
            mock_popen.return_value = mock_process

            result = self.sdk_manager.start_sdk()

            self.assertEqual(result, mock_process)
            mock_popen.assert_called_once()

    def test_start_sdk_not_installed(self):
        """测试启动SDK - 未安装"""
        with self.assertRaises(MYTSDKProcessError):
            self.sdk_manager.start_sdk()

    @patch.object(MYTSDKManager, "start_sdk")
    @patch.object(MYTSDKManager, "download_sdk")
    @patch.object(MYTSDKManager, "is_sdk_running")
    @patch.object(MYTSDKManager, "is_sdk_installed")
    def test_init_already_running(
        self, mock_installed, mock_running, mock_download, mock_start
    ):
        """测试初始化时SDK已在运行"""
        mock_installed.return_value = True
        mock_running.return_value = True

        result = self.sdk_manager.init()

        self.assertEqual(result["status"], "already_running")
        mock_download.assert_not_called()
        mock_start.assert_not_called()

    @patch.object(MYTSDKManager, "start_sdk")
    @patch.object(MYTSDKManager, "download_sdk")
    @patch.object(MYTSDKManager, "is_sdk_running")
    @patch.object(MYTSDKManager, "is_sdk_installed")
    def test_init_download_and_start(
        self, mock_installed, mock_running, mock_download, mock_start
    ):
        """测试初始化时需要下载和启动"""
        mock_installed.return_value = False
        mock_running.return_value = False
        mock_download.return_value = None
        mock_process = MagicMock()
        mock_process.pid = 12345
        mock_start.return_value = mock_process

        result = self.sdk_manager.init()

        self.assertEqual(result["status"], "started")
        mock_download.assert_called_once()
        mock_start.assert_called_once()

    @patch.object(MYTSDKManager, "is_sdk_running")
    @patch.object(MYTSDKManager, "is_sdk_installed")
    @patch.object(MYTSDKManager, "start_sdk")
    def test_init_no_start(self, mock_start, mock_installed, mock_running):
        """测试初始化时不启动SDK"""
        mock_installed.return_value = True
        mock_running.return_value = False

        result = self.sdk_manager.init(start_sdk=False)

        self.assertEqual(result["status"], "ready")
        mock_start.assert_not_called()


if __name__ == "__main__":
    unittest.main()
