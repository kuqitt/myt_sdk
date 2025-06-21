"""MYT SDK 异常定义模块"""


class MYTSDKError(Exception):
    """MYT SDK 基础异常类"""

    def __init__(self, message: str, error_code: str = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code

    def __str__(self):
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message


class MYTSDKDownloadError(MYTSDKError):
    """SDK下载相关异常"""

    def __init__(self, message: str, url: str = None, status_code: int = None):
        super().__init__(message, "DOWNLOAD_ERROR")
        self.url = url
        self.status_code = status_code

    def __str__(self):
        base_msg = super().__str__()
        if self.url:
            base_msg += f" (URL: {self.url})"
        if self.status_code:
            base_msg += f" (Status: {self.status_code})"
        return base_msg


class MYTSDKProcessError(MYTSDKError):
    """SDK进程相关异常"""

    def __init__(self, message: str, process_name: str = None, exit_code: int = None):
        super().__init__(message, "PROCESS_ERROR")
        self.process_name = process_name
        self.exit_code = exit_code

    def __str__(self):
        base_msg = super().__str__()
        if self.process_name:
            base_msg += f" (Process: {self.process_name})"
        if self.exit_code is not None:
            base_msg += f" (Exit Code: {self.exit_code})"
        return base_msg


class MYTSDKConfigError(MYTSDKError):
    """SDK配置相关异常"""

    def __init__(self, message: str, config_key: str = None):
        super().__init__(message, "CONFIG_ERROR")
        self.config_key = config_key

    def __str__(self):
        base_msg = super().__str__()
        if self.config_key:
            base_msg += f" (Config Key: {self.config_key})"
        return base_msg


class MYTSDKFileError(MYTSDKError):
    """SDK文件操作相关异常"""

    def __init__(self, message: str, file_path: str = None):
        super().__init__(message, "FILE_ERROR")
        self.file_path = file_path

    def __str__(self):
        base_msg = super().__str__()
        if self.file_path:
            base_msg += f" (File: {self.file_path})"
        return base_msg
