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
            mock_process.info = {"name": "myt_sdk.exe", "pid": 12345, "exe": str(self.sdk_manager.sdk_executable_path)}
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
                # 创建与ZIP文件内容匹配的目录结构
                sdk_dir = Path(path)
                myt_sdk_dir = sdk_dir / "myt_sdk"
                myt_sdk_dir.mkdir(parents=True, exist_ok=True)
                
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

    @patch.object(MYTSDKManager, "_update_sdk_config_from_url")
    @patch.object(MYTSDKManager, "download_sdk")
    @patch.object(MYTSDKManager, "start_sdk")
    @patch.object(MYTSDKManager, "is_sdk_running")
    def test_init_with_custom_url(self, mock_running, mock_start, mock_download, mock_update_config):
        """测试使用自定义下载地址初始化"""
        mock_running.return_value = False
        mock_process = MagicMock()
        mock_process.pid = 12345
        mock_start.return_value = mock_process
        
        custom_url = "http://example.com/myt_sdk_2.0.0.zip"
        result = self.sdk_manager.init(download_url=custom_url)
        
        mock_update_config.assert_called_once_with(custom_url)
        mock_download.assert_called_once_with(force=True)
        self.assertEqual(result["status"], "started")

    def test_update_sdk_config_from_url_with_version(self):
        """测试从URL更新SDK配置 - 包含版本号"""
        old_version = self.sdk_manager.SDK_VERSION
        old_url = self.sdk_manager.SDK_DOWNLOAD_URL
        
        new_url = "http://example.com/myt_sdk_2.0.15.zip"
        self.sdk_manager._update_sdk_config_from_url(new_url)
        
        self.assertEqual(self.sdk_manager.SDK_DOWNLOAD_URL, new_url)
        self.assertEqual(self.sdk_manager.SDK_VERSION, "2.0.15")
        self.assertNotEqual(self.sdk_manager.SDK_VERSION, old_version)

    def test_update_sdk_config_from_url_without_version(self):
        """测试从URL更新SDK配置 - 不包含版本号"""
        old_version = self.sdk_manager.SDK_VERSION
        
        new_url = "http://example.com/custom_sdk.zip"
        self.sdk_manager._update_sdk_config_from_url(new_url)
        
        self.assertEqual(self.sdk_manager.SDK_DOWNLOAD_URL, new_url)
        self.assertTrue(self.sdk_manager.SDK_VERSION.startswith("custom_"))
        self.assertNotEqual(self.sdk_manager.SDK_VERSION, old_version)

    def test_refresh_executable_path(self):
        """测试刷新可执行文件路径功能"""
        # 创建测试目录结构
        test_version = "test_1.0.0"
        self.sdk_manager.SDK_VERSION = test_version
        self.sdk_manager.sdk_dir = self.sdk_manager.cache_dir / "myt_sdk" / test_version
        
        # 创建SDK目录和可执行文件
        sdk_subdir = self.sdk_manager.sdk_dir / "myt_sdk"
        sdk_subdir.mkdir(parents=True, exist_ok=True)
        exe_file = sdk_subdir / "myt_sdk.exe"
        exe_file.write_text("fake executable")
        
        # 调用刷新方法
        self.sdk_manager._refresh_executable_path()
        
        # 验证路径已正确更新
        self.assertEqual(self.sdk_manager.sdk_executable_path, exe_file)
        self.assertTrue(self.sdk_manager.sdk_executable_path.exists())

    def test_init_with_download_url_updates_path(self):
        """测试使用自定义下载地址初始化时路径更新"""
        custom_url = "http://example.com/myt_sdk_2.0.0.zip"
        
        with patch('requests.get') as mock_get, \
             patch('zipfile.ZipFile') as mock_zipfile:
            
            # 模拟下载响应
            mock_response = Mock()
            mock_response.headers = {'content-length': '1000'}
            mock_response.iter_content.return_value = [b'fake zip content']
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            # 模拟ZIP文件解压
            mock_zip = Mock()
            mock_zip.namelist.return_value = ['myt_sdk/', 'myt_sdk/myt_sdk.exe']
            mock_zipfile.return_value.__enter__.return_value = mock_zip
            
            def create_sdk_file(*args, **kwargs):
                # 创建SDK可执行文件
                sdk_subdir = self.sdk_manager.sdk_dir / "myt_sdk"
                sdk_subdir.mkdir(parents=True, exist_ok=True)
                exe_file = sdk_subdir / "myt_sdk.exe"
                exe_file.write_text("fake executable")
            
            mock_zip.extractall.side_effect = create_sdk_file
            
            # 使用自定义URL初始化
            result = self.sdk_manager.init(download_url=custom_url, start_sdk=False)
            
            # 验证版本已更新
            self.assertEqual(self.sdk_manager.SDK_VERSION, "2.0.0")
            self.assertEqual(self.sdk_manager.SDK_DOWNLOAD_URL, custom_url)
            
            # 验证可执行文件路径已正确更新
            expected_path = self.sdk_manager.sdk_dir / "myt_sdk" / "myt_sdk.exe"
            self.assertEqual(self.sdk_manager.sdk_executable_path, expected_path)
            self.assertTrue(self.sdk_manager.sdk_executable_path.exists())

    @patch("py_myt.sdk_manager.psutil.process_iter")
    def test_stop_sdk_not_running(self, mock_process_iter):
        """测试停止SDK - 未运行"""
        mock_process_iter.return_value = []
        
        with patch.object(self.sdk_manager, "is_sdk_running", return_value=False):
            result = self.sdk_manager.stop_sdk()
            
            self.assertEqual(result["status"], "not_running")
            self.assertEqual(result["stopped_processes"], 0)

    @patch("py_myt.sdk_manager.psutil.process_iter")
    def test_stop_sdk_success(self, mock_process_iter):
        """测试停止SDK - 成功"""
        # 创建模拟进程
        mock_process = Mock()
        mock_process.pid = 12345
        mock_process.info = {"name": "myt_sdk.exe", "exe": str(self.sdk_manager.sdk_executable_path)}
        mock_process.terminate.return_value = None
        mock_process.wait.return_value = None
        mock_process_iter.return_value = [mock_process]
        
        with patch.object(self.sdk_manager, "is_sdk_running", side_effect=[True, False]):
            result = self.sdk_manager.stop_sdk()
            
            self.assertEqual(result["status"], "success")
            self.assertEqual(result["stopped_processes"], 1)
            mock_process.terminate.assert_called_once()

    @patch("py_myt.sdk_manager.psutil.process_iter")
    def test_stop_sdk_force(self, mock_process_iter):
        """测试强制停止SDK"""
        # 创建模拟进程
        mock_process = Mock()
        mock_process.pid = 12345
        mock_process.info = {"name": "myt_sdk.exe", "exe": str(self.sdk_manager.sdk_executable_path)}
        mock_process.kill.return_value = None
        mock_process_iter.return_value = [mock_process]
        
        with patch.object(self.sdk_manager, "is_sdk_running", side_effect=[True, False]):
            result = self.sdk_manager.stop_sdk(force=True)
            
            self.assertEqual(result["status"], "success")
            self.assertEqual(result["stopped_processes"], 1)
            mock_process.kill.assert_called_once()
            mock_process.terminate.assert_not_called()

    def test_redownload_updates_path(self):
        """测试重新下载后路径更新功能"""
        with patch('requests.get') as mock_get, \
             patch('zipfile.ZipFile') as mock_zipfile:
            
            # 模拟下载响应
            mock_response = Mock()
            mock_response.headers = {'content-length': '1000'}
            mock_response.iter_content.return_value = [b'fake zip content']
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            # 模拟ZIP文件解压
            mock_zip = Mock()
            mock_zip.namelist.return_value = ['myt_sdk/', 'myt_sdk/myt_sdk.exe']
            mock_zipfile.return_value.__enter__.return_value = mock_zip
            
            def create_sdk_file(*args, **kwargs):
                # 创建SDK可执行文件
                sdk_subdir = self.sdk_manager.sdk_dir / "myt_sdk"
                sdk_subdir.mkdir(parents=True, exist_ok=True)
                exe_file = sdk_subdir / "myt_sdk.exe"
                exe_file.write_text("fake executable")
            
            mock_zip.extractall.side_effect = create_sdk_file
            
            # 记录原始路径
            original_version = self.sdk_manager.SDK_VERSION
            original_path = self.sdk_manager.sdk_executable_path
            
            # 使用新版本URL重新下载
            new_url = "http://example.com/myt_sdk_3.0.0.zip"
            self.sdk_manager._update_sdk_config_from_url(new_url)
            self.sdk_manager.download_sdk(force=True)
            
            # 验证版本和路径已更新
            self.assertEqual(self.sdk_manager.SDK_VERSION, "3.0.0")
            self.assertNotEqual(self.sdk_manager.SDK_VERSION, original_version)
            self.assertNotEqual(self.sdk_manager.sdk_executable_path, original_path)
            
            # 验证新路径存在且正确
            expected_path = self.sdk_manager.sdk_dir / "myt_sdk" / "myt_sdk.exe"
            self.assertEqual(self.sdk_manager.sdk_executable_path, expected_path)
            self.assertTrue(self.sdk_manager.sdk_executable_path.exists())


if __name__ == "__main__":
    unittest.main()
