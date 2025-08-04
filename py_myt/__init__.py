"""MYT SDK - 魔云腾SDK通用包"""

try:
    from ._version import __version__
except ImportError:
    # 如果 _version.py 不存在，使用默认版本
    __version__ = "1.1.8"

__author__ = "Cooskin"
__email__ = "kuqitt1@163.com"

from .api_client import MYTAPIClient, create_client
from .exceptions import (
    MYTSDKDownloadError,
    MYTSDKError,
    MYTSDKFileError,
    MYTSDKProcessError,
)
from .sdk_manager import MYTSDKManager

__all__ = [
    "MYTSDKManager",
    "MYTAPIClient",
    "create_client",
    "MYTSDKError",
    "MYTSDKDownloadError",
    "MYTSDKProcessError",
    "MYTSDKFileError",
]
