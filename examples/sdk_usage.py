#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MYT SDK使用示例

本示例展示了如何使用MYT SDK Python包来管理和使用MYT SDK。
"""

import logging
import sys
from pathlib import Path

# 添加项目根目录到Python路径（仅用于开发环境）
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from py_myt import MYTSDKManager
from py_myt.exceptions import MYTSDKError


def setup_logging():
    """设置日志配置"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def example_basic_usage():
    """基础使用示例"""
    print("=== MYT SDK 基础使用示例 ===")
    
    try:
        # 创建SDK管理器
        sdk_manager = MYTSDKManager()
        
        # 检查SDK状态
        print("\n1. 检查SDK状态...")
        status = sdk_manager.get_status()
        print(f"   SDK已安装: {status['installed']}")
        print(f"   SDK正在运行: {status['running']}")
        print(f"   缓存目录: {status['cache_dir']}")
        print(f"   SDK路径: {status['sdk_path']}")
        
        # 初始化SDK
        print("\n2. 初始化SDK...")
        result = sdk_manager.init()
        print(f"   初始化结果: {result['status']}")
        print(f"   消息: {result['message']}")
        
        if result['status'] == 'started':
            print(f"   进程ID: {result.get('pid', 'N/A')}")
        
        # 再次检查状态
        print("\n3. 再次检查SDK状态...")
        status = sdk_manager.get_status()
        print(f"   SDK已安装: {status['installed']}")
        print(f"   SDK正在运行: {status['running']}")
        
    except MYTSDKError as e:
        print(f"SDK错误: {e}")
        if hasattr(e, 'details') and e.details:
            print(f"错误详情: {e.details}")
    except Exception as e:
        print(f"未知错误: {e}")


def example_custom_cache_dir():
    """自定义缓存目录示例"""
    print("\n=== 自定义缓存目录示例 ===")
    
    try:
        # 使用自定义缓存目录
        custom_cache = Path.home() / "my_myt_cache"
        sdk_manager = MYTSDKManager(cache_dir=str(custom_cache))
        
        print(f"使用自定义缓存目录: {custom_cache}")
        
        # 检查状态
        status = sdk_manager.get_status()
        print(f"SDK已安装: {status['installed']}")
        print(f"缓存目录: {status['cache_dir']}")
        
    except Exception as e:
        print(f"错误: {e}")


def example_force_reinstall():
    """强制重新安装示例"""
    print("\n=== 强制重新安装示例 ===")
    
    try:
        sdk_manager = MYTSDKManager()
        
        # 强制重新下载和安装
        print("强制重新下载SDK...")
        result = sdk_manager.init(force=True)
        print(f"结果: {result['status']}")
        print(f"消息: {result['message']}")
        
    except Exception as e:
        print(f"错误: {e}")


def example_download_only():
    """仅下载不启动示例"""
    print("\n=== 仅下载不启动示例 ===")
    
    try:
        sdk_manager = MYTSDKManager()
        
        # 仅下载，不启动SDK
        print("仅下载SDK，不启动...")
        result = sdk_manager.init(start_sdk=False)
        print(f"结果: {result['status']}")
        print(f"消息: {result['message']}")
        
        # 检查状态
        status = sdk_manager.get_status()
        print(f"SDK已安装: {status['installed']}")
        print(f"SDK正在运行: {status['running']}")
        
    except Exception as e:
        print(f"错误: {e}")


def example_error_handling():
    """错误处理示例"""
    print("\n=== 错误处理示例 ===")
    
    try:
        # 使用无效的缓存目录（只读目录）
        invalid_cache = "C:\\Windows\\System32\\invalid_cache"
        sdk_manager = MYTSDKManager(cache_dir=invalid_cache)
        
        # 尝试初始化（可能会失败）
        result = sdk_manager.init()
        print(f"意外成功: {result}")
        
    except MYTSDKError as e:
        print(f"捕获到SDK错误: {e}")
        print(f"错误类型: {type(e).__name__}")
        if hasattr(e, 'details') and e.details:
            print(f"错误详情: {e.details}")
    except Exception as e:
        print(f"捕获到其他错误: {e}")
        print(f"错误类型: {type(e).__name__}")


def main():
    """主函数"""
    setup_logging()
    
    print("MYT SDK Python包使用示例")
    print("=" * 50)
    
    # 运行各种示例
    example_basic_usage()
    example_custom_cache_dir()
    example_force_reinstall()
    example_download_only()
    example_error_handling()
    
    print("\n=== 示例运行完成 ===")
    print("\n提示:")
    print("- 可以通过命令行使用: myt-sdk init")
    print("- 查看帮助: myt-sdk --help")
    print("- 查看状态: myt-sdk status")


if __name__ == "__main__":
    main()