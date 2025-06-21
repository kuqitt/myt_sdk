#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MYT API客户端使用示例

演示如何使用MYTAPIClient进行各种API调用
"""

import sys
import logging
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from py_myt.api_client import MYTAPIClient, create_client
from py_myt.exceptions import MYTSDKError

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def demo_basic_usage():
    """基本使用示例"""
    print("=== MYT API客户端基本使用示例 ===")
    
    # 方式1: 直接创建客户端
    client = MYTAPIClient(base_url="http://127.0.0.1:5000")
    
    try:
        # 获取版本信息
        print("\n1. 获取版本信息:")
        version_info = client.get_version()
        print(f"版本: {version_info}")
        
        # 用户登录
        print("\n2. 用户登录:")
        login_result = client.login("admin", "password123")
        print(f"登录结果: {login_result}")
        
        # 获取在线设备列表
        print("\n3. 获取在线设备列表:")
        devices = client.query_myt_devices()
        print(f"设备列表: {devices}")
        
        # 获取镜像列表V2
        print("\n4. 获取镜像列表V2 (类型: p1):")
        images_v2 = client.get_image_list_v2("p1")
        print(f"镜像列表V2: {images_v2}")
        
        # 获取镜像列表V1
        print("\n5. 获取镜像列表V1:")
        images_v1 = client.get_image_list_v1()
        print(f"镜像列表V1: {images_v1}")
        
        # 获取机型信息
        print("\n6. 获取机型信息:")
        device_info = client.get_device_info()
        print(f"机型信息: {device_info}")
        
    except MYTSDKError as e:
        print(f"API调用失败: {e}")
    finally:
        client.close()


def demo_context_manager():
    """上下文管理器使用示例"""
    print("\n=== 使用上下文管理器 ===")
    
    # 方式2: 使用上下文管理器（推荐）
    with create_client() as client:
        try:
            # 获取版本信息
            version_info = client.get_version()
            print(f"SDK版本: {version_info.get('data', 'Unknown')}")
            
        except MYTSDKError as e:
            print(f"获取版本信息失败: {e}")


def demo_error_handling():
    """错误处理示例"""
    print("\n=== 错误处理示例 ===")
    
    # 使用错误的服务器地址
    with create_client(base_url="http://127.0.0.1:9999") as client:
        try:
            version_info = client.get_version()
            print(f"版本信息: {version_info}")
        except MYTSDKError as e:
            print(f"预期的连接错误: {e}")
    
    # 测试无效的镜像类型
    with create_client() as client:
        try:
            images = client.get_image_list_v2("invalid_type")
            print(f"镜像列表: {images}")
        except MYTSDKError as e:
            print(f"预期的参数错误: {e}")


def demo_custom_configuration():
    """自定义配置示例"""
    print("\n=== 自定义配置示例 ===")
    
    # 自定义服务器地址和超时时间
    custom_client = MYTAPIClient(
        base_url="http://192.168.1.100:8080",
        timeout=60  # 60秒超时
    )
    
    try:
        # 这里会因为服务器不存在而失败，仅作演示
        version_info = custom_client.get_version()
        print(f"版本信息: {version_info}")
    except MYTSDKError as e:
        print(f"自定义配置测试 - 预期的连接错误: {e}")
    finally:
        custom_client.close()


def demo_batch_operations():
    """批量操作示例"""
    print("\n=== 批量操作示例 ===")
    
    with create_client() as client:
        # 批量获取不同类型的镜像列表
        image_types = ['p1', 'q1', 'a1', 'c1']
        
        for img_type in image_types:
            try:
                images = client.get_image_list_v2(img_type)
                image_count = len(images.get('msg', []))
                print(f"镜像类型 {img_type}: {image_count} 个镜像")
            except MYTSDKError as e:
                print(f"获取镜像类型 {img_type} 失败: {e}")


if __name__ == "__main__":
    print("MYT API客户端使用示例")
    print("注意: 这些示例需要MYT SDK服务器在127.0.0.1:5000运行")
    print("如果服务器未运行，将会看到连接错误，这是正常的。")
    
    try:
        # 运行所有示例
        demo_basic_usage()
        demo_context_manager()
        demo_error_handling()
        demo_custom_configuration()
        demo_batch_operations()
        
        print("\n=== 示例运行完成 ===")
        
    except KeyboardInterrupt:
        print("\n用户中断了示例运行")
    except Exception as e:
        logger.error(f"示例运行出错: {e}")