"""MYT SDK异常测试模块"""

import unittest

from py_myt.exceptions import (
    MYTSDKConfigError,
    MYTSDKDownloadError,
    MYTSDKError,
    MYTSDKFileError,
    MYTSDKProcessError,
)


class TestMYTSDKExceptions(unittest.TestCase):
    """MYT SDK异常测试类"""

    def test_base_exception(self):
        """测试基础异常"""
        error = MYTSDKError("测试错误")
        self.assertEqual(str(error), "测试错误")
        self.assertIsInstance(error, Exception)

    def test_download_error(self):
        """测试下载错误异常"""
        error = MYTSDKDownloadError("下载失败", url="http://example.com")

        self.assertEqual(
            str(error), "[DOWNLOAD_ERROR] 下载失败 (URL: http://example.com)"
        )
        self.assertEqual(error.url, "http://example.com")
        self.assertIsInstance(error, MYTSDKError)

    def test_process_error(self):
        """测试进程错误异常"""
        error = MYTSDKProcessError("进程启动失败", process_name="test_process")

        self.assertEqual(
            str(error), "[PROCESS_ERROR] 进程启动失败 (Process: test_process)"
        )
        self.assertEqual(error.process_name, "test_process")
        self.assertIsInstance(error, MYTSDKError)

    def test_config_error(self):
        """测试配置错误异常"""
        error = MYTSDKConfigError("配置错误")

        self.assertEqual(str(error), "[CONFIG_ERROR] 配置错误")
        self.assertIsInstance(error, MYTSDKError)

    def test_file_error(self):
        """测试文件错误异常"""
        error = MYTSDKFileError("文件不存在", file_path="/path/to/file")

        self.assertEqual(str(error), "[FILE_ERROR] 文件不存在 (File: /path/to/file)")
        self.assertEqual(error.file_path, "/path/to/file")
        self.assertIsInstance(error, MYTSDKError)

    def test_exception_inheritance(self):
        """测试异常继承关系"""
        # 所有自定义异常都应该继承自MYTSDKError
        exceptions = [
            MYTSDKDownloadError,
            MYTSDKProcessError,
            MYTSDKConfigError,
            MYTSDKFileError,
        ]

        for exc_class in exceptions:
            self.assertTrue(issubclass(exc_class, MYTSDKError))
            self.assertTrue(issubclass(exc_class, Exception))

    def test_exception_with_details(self):
        """测试带详细信息的异常"""
        error = MYTSDKDownloadError(
            "下载失败", url="http://example.com", status_code=404
        )

        self.assertIn("下载失败", str(error))
        self.assertEqual(error.url, "http://example.com")
        self.assertEqual(error.status_code, 404)

    def test_exception_without_details(self):
        """测试不带详细信息的异常"""
        error = MYTSDKError("基础错误")

        self.assertEqual(str(error), "基础错误")
        self.assertIsInstance(error, Exception)


if __name__ == "__main__":
    unittest.main()
