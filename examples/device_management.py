#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安卓设备管理示例

本示例演示如何使用MYT API客户端进行安卓设备管理操作
包括获取设备详情、上传文件、随机更换设备信息、自定义设备信息等功能
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from py_myt.api_client import create_client
from py_myt.exceptions import MYTSDKError

def demo_get_android_detail():
    """演示获取安卓实例详细信息"""
    print("\n=== 获取安卓实例详细信息示例 ===")
    
    with create_client() as client:
        try:
            # 获取安卓实例详细信息
            print("\n1. 获取安卓实例详细信息:")
            result = client.get_android_detail(
                ip="192.168.100.235",
                name="test_container"
            )
            print(f"设备详情: {result}")
            
            # 解析设备信息
            if result.get("code") == 200 and "msg" in result:
                device_info = result["msg"]
                print(f"设备ID: {device_info.get('id', 'N/A')}")
                print(f"设备状态: {device_info.get('status', 'N/A')}")
                print(f"内存限制: {device_info.get('memory', 'N/A')} MB")
                print(f"分辨率: {device_info.get('width', 'N/A')}x{device_info.get('height', 'N/A')}")
                print(f"DPI: {device_info.get('dpi', 'N/A')}")
                print(f"FPS: {device_info.get('fps', 'N/A')}")
                print(f"本地IP: {device_info.get('local_ip', 'N/A')}")
                print(f"RPA端口: {device_info.get('rpa', 'N/A')}")
            
        except MYTSDKError as e:
            print(f"获取设备详情失败: {e}")
        except Exception as e:
            print(f"未知错误: {e}")

def demo_get_host_version():
    """演示获取主机版本信息"""
    print("\n=== 获取主机版本信息示例 ===")
    
    with create_client() as client:
        try:
            # 获取主机版本信息
            print("\n2. 获取主机版本信息:")
            result = client.get_host_version(ip="192.168.100.235")
            print(f"主机版本: {result}")
            
        except MYTSDKError as e:
            print(f"获取主机版本失败: {e}")
        except Exception as e:
            print(f"未知错误: {e}")

def demo_upload_file():
    """演示上传文件到安卓容器"""
    print("\n=== 上传文件到安卓容器示例 ===")
    
    with create_client() as client:
        try:
            # 上传APK文件
            print("\n3. 上传APK文件:")
            result = client.upload_file_to_android(
                ip="192.168.1.100",
                name="test_container",
                local_file="/home/user/Downloads/test.apk"
            )
            print(f"上传结果: {result}")
            
            # 上传其他文件
            print("\n4. 上传配置文件:")
            result = client.upload_file_to_android(
                ip="192.168.1.100",
                name="test_container",
                local_file="/home/user/config.json"
            )
            print(f"上传结果: {result}")
            
        except MYTSDKError as e:
            print(f"文件上传失败: {e}")
        except Exception as e:
            print(f"未知错误: {e}")

def demo_random_device_info():
    """演示随机更换设备信息"""
    print("\n=== 随机更换设备信息示例 ===")
    
    with create_client("http://192.168.1.100:8080") as client:
        try:
            # 基础随机设备信息（同步）
            print("\n5. 基础随机设备信息（同步）:")
            result = client.random_device_info(
                ip="192.168.1.100",
                name="test_container"
            )
            print(f"随机设备信息结果: {result}")
            
            # 指定IP和设备型号的随机设备信息
            print("\n6. 指定参数的随机设备信息:")
            result = client.random_device_info(
                ip="192.168.1.100",
                name="test_container",
                userip="192.168.1.200",
                modelid="samsung_s21"
            )
            print(f"指定参数随机结果: {result}")
            
        except MYTSDKError as e:
            print(f"随机设备信息失败: {e}")
        except Exception as e:
            print(f"未知错误: {e}")

def demo_random_device_info_async():
    """演示异步随机更换设备信息"""
    print("\n=== 异步随机更换设备信息示例 ===")
    
    with create_client("http://192.168.1.100:8080") as client:
        try:
            # 异步随机设备信息
            print("\n7. 异步随机设备信息:")
            result = client.random_device_info_async(
                ip="192.168.1.100",
                name="test_container",
                modelid="xiaomi_mi11"
            )
            print(f"异步随机设备信息结果: {result}")
            
            # 异步随机设备信息2 - 请求结果
            print("\n8. 异步随机设备信息2 - 请求:")
            result = client.random_device_info_async2(
                ip="192.168.1.100",
                name="test_container",
                act="request",
                userip="192.168.1.150"
            )
            print(f"异步请求结果: {result}")
            
            # 异步随机设备信息2 - 查询结果
            print("\n9. 异步随机设备信息2 - 查询:")
            result = client.random_device_info_async2(
                ip="192.168.1.100",
                name="test_container",
                act="query"
            )
            print(f"异步查询结果: {result}")
            
            # 异步随机设备信息2 - 获取并清空
            print("\n10. 异步随机设备信息2 - 获取并清空:")
            result = client.random_device_info_async2(
                ip="192.168.1.100",
                name="test_container",
                act="get"
            )
            print(f"异步获取并清空结果: {result}")
            
        except MYTSDKError as e:
            print(f"异步随机设备信息失败: {e}")
        except Exception as e:
            print(f"未知错误: {e}")

def demo_set_custom_device_info():
    """演示自定义设备机型信息"""
    print("\n=== 自定义设备机型信息示例 ===")
    
    with create_client("http://192.168.1.100:8080") as client:
        try:
            # 模拟真机设备数据（实际使用时应该是从真机提取的完整数据）
            device_data = """
            {
                "device_model": "SM-G991B",
                "manufacturer": "Samsung",
                "brand": "samsung",
                "hardware": "exynos2100",
                "fingerprint": "samsung/o1sxxx/o1s:12/SP1A.210812.016/G991BXXU5DVKB:user/release-keys",
                "build_id": "SP1A.210812.016",
                "version_release": "12",
                "version_sdk": "31"
            }
            """
            
            # 基础自定义设备信息
            print("\n11. 基础自定义设备信息:")
            result = client.set_custom_device_info(
                ip="192.168.1.100",
                name="test_container",
                device_data=device_data
            )
            print(f"自定义设备信息结果: {result}")
            
            # 带完整参数的自定义设备信息
            print("\n12. 完整参数自定义设备信息:")
            result = client.set_custom_device_info(
                ip="192.168.1.100",
                name="test_container",
                device_data=device_data,
                android_id="1234567890abcdef",
                imei="123456789012345",
                imsi="123456789012345",
                series_num="R58N123ABCD",
                btaddr="AA:BB:CC:DD:EE:FF",
                btname="Samsung Galaxy S21",
                wifi_mac="11:22:33:44:55:66",
                wifi_name="Galaxy-S21",
                oaid="12345678-1234-1234-1234-123456789012"
            )
            print(f"完整参数自定义结果: {result}")
            
        except MYTSDKError as e:
            print(f"自定义设备信息失败: {e}")
        except Exception as e:
            print(f"未知错误: {e}")

def demo_batch_device_operations():
    """演示批量设备操作"""
    print("\n=== 批量设备操作示例 ===")
    
    with create_client("http://192.168.1.100:8080") as client:
        # 批量获取设备详情
        containers = ["container_1", "container_2", "container_3"]
        
        print("\n13. 批量获取设备详情:")
        for i, container_name in enumerate(containers, 1):
            try:
                result = client.get_android_detail(
                    ip="192.168.1.100",
                    name=container_name
                )
                print(f"容器 {i} ({container_name}) 详情: {result.get('msg', {}).get('status', 'N/A')}")
            except Exception as e:
                print(f"容器 {i} ({container_name}) 获取失败: {e}")
        
        # 批量随机设备信息
        print("\n14. 批量随机设备信息:")
        for i, container_name in enumerate(containers, 1):
            try:
                result = client.random_device_info(
                    ip="192.168.1.100",
                    name=container_name
                )
                print(f"容器 {i} ({container_name}) 随机设备信息: {result}")
            except Exception as e:
                print(f"容器 {i} ({container_name}) 随机失败: {e}")

def demo_error_handling():
    """演示错误处理"""
    print("\n=== 错误处理示例 ===")
    
    with create_client("http://192.168.1.100:8080") as client:
        try:
            # 尝试获取不存在的容器详情
            print("\n15. 错误处理测试:")
            result = client.get_android_detail(
                ip="192.168.1.100",
                name="non_existent_container"
            )
            print(f"意外成功: {result}")
            
        except MYTSDKError as e:
            print(f"捕获到MYT SDK错误: {e}")
        except Exception as e:
            print(f"捕获到其他错误: {e}")
        
        try:
            # 尝试上传不存在的文件
            result = client.upload_file_to_android(
                ip="192.168.1.100",
                name="test_container",
                local_file="/non/existent/file.apk"
            )
            print(f"意外成功: {result}")
            
        except MYTSDKError as e:
            print(f"捕获到文件上传错误: {e}")
        except Exception as e:
            print(f"捕获到其他错误: {e}")

if __name__ == "__main__":
    print("MYT 安卓设备管理示例")
    print("注意: 请确保MYT服务器正在运行并且网络连接正常")
    print("警告: 自定义设备信息功能请谨慎使用，错误的数据可能导致系统无法开机")
    
    try:
        # 运行所有示例
        demo_get_android_detail()
        demo_get_host_version()
        demo_upload_file()
        demo_random_device_info()
        demo_random_device_info_async()
        demo_set_custom_device_info()
        demo_batch_device_operations()
        demo_error_handling()
        
        print("\n=== 所有示例执行完成 ===")
        
    except KeyboardInterrupt:
        print("\n用户中断执行")
    except Exception as e:
        print(f"\n程序执行出错: {e}")