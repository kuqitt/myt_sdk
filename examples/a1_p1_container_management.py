#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A1和P1安卓容器管理示例

本示例演示如何使用MYT API客户端创建A1和P1安卓容器
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from py_myt.api_client import create_client
from py_myt.exceptions import MYTSDKError

def demo_a1_container_creation():
    """演示A1容器创建"""
    print("\n=== A1安卓容器创建示例 ===")
    
    # 使用上下文管理器创建客户端
    with create_client() as client:
        try:
            # 基础A1容器创建
            print("\n1. 基础A1容器创建:")
            result = client.create_a1_android_container(
                ip="192.168.1.100",
                index=1,
                name="test_a1_container"
            )
            print(f"创建结果: {result}")
            
        except MYTSDKError as e:
            print(f"创建失败: {e}")
        except Exception as e:
            print(f"未知错误: {e}")

def demo_a1_container_advanced():
    """演示A1容器高级配置创建"""
    print("\n=== A1安卓容器高级配置示例 ===")
    
    with create_client() as client:
        try:
            # 高级配置A1容器创建
            print("\n2. 高级配置A1容器创建:")
            result = client.create_a1_android_container(
                ip="192.168.1.100",
                index=2,
                name="advanced_a1_container",
                sandbox=1,  # 启用沙盒模式
                sandbox_size=32,  # 32GB沙盒空间
                memory=4096,  # 4GB内存
                cpu="0,1,2,3",  # 绑定4个CPU核心
                resolution=1,  # 1080P分辨率
                width=1080,
                height=1920,
                dpi=480,
                fps=60,  # 60fps刷新率
                dns="8.8.8.8",  # 使用Google DNS
                random_dev=1,  # 随机设备信息
                enforce=1  # 严格模式
            )
            print(f"创建结果: {result}")
            
        except MYTSDKError as e:
            print(f"创建失败: {e}")
        except Exception as e:
            print(f"未知错误: {e}")

def demo_p1_container_creation():
    """演示P1容器创建"""
    print("\n=== P1安卓容器创建示例 ===")
    
    with create_client() as client:
        try:
            # 基础P1容器创建
            print("\n3. 基础P1容器创建:")
            result = client.create_p1_android_container(
                ip="192.168.1.100",
                index=1,
                name="test_p1_container"
            )
            print(f"创建结果: {result}")
            
        except MYTSDKError as e:
            print(f"创建失败: {e}")
        except Exception as e:
            print(f"未知错误: {e}")

def demo_p1_container_with_proxy():
    """演示P1容器代理配置创建"""
    print("\n=== P1安卓容器代理配置示例 ===")
    
    with create_client() as client:
        try:
            # 带代理配置的P1容器创建
            print("\n4. 带代理配置的P1容器创建:")
            result = client.create_p1_android_container(
                ip="192.168.1.100",
                index=2,
                name="proxy_p1_container",
                s5ip="192.168.1.200",  # SOCKS5代理IP
                s5port=1080,  # SOCKS5代理端口
                s5user="proxy_user",  # 代理用户名
                s5pwd="proxy_pass",  # 代理密码
                memory=2048,  # 2GB内存
                resolution=0,  # 720P分辨率
                dns="223.5.5.5"  # 阿里DNS
            )
            print(f"创建结果: {result}")
            
        except MYTSDKError as e:
            print(f"创建失败: {e}")
        except Exception as e:
            print(f"未知错误: {e}")

def demo_container_with_port_mapping():
    """演示容器端口映射配置"""
    print("\n=== 容器端口映射配置示例 ===")
    
    with create_client() as client:
        try:
            # 带端口映射的容器创建
            print("\n5. 带端口映射的A1容器创建:")
            result = client.create_a1_android_container(
                ip="192.168.1.100",
                index=3,
                name="port_mapping_container",
                tcp_map_port="{20000:50001, 30000:50002}",  # TCP端口映射
                udp_map_port="{25000:50003, 35000:50004}",  # UDP端口映射
                adbport=55555,  # ADB端口
                rpaport=56666,  # RPA端口映射
                memory=1024  # 1GB内存
            )
            print(f"创建结果: {result}")
            
        except MYTSDKError as e:
            print(f"创建失败: {e}")
        except Exception as e:
            print(f"未知错误: {e}")

def demo_batch_container_creation():
    """演示批量容器创建"""
    print("\n=== 批量容器创建示例 ===")
    
    with create_client() as client:
        # 批量创建A1容器
        containers = [
            {"ip": "192.168.1.100", "index": 10, "name": "batch_a1_1", "memory": 1024},
            {"ip": "192.168.1.100", "index": 11, "name": "batch_a1_2", "memory": 1024},
            {"ip": "192.168.1.100", "index": 12, "name": "batch_a1_3", "memory": 1024}
        ]
        
        print("\n6. 批量创建A1容器:")
        for i, container_config in enumerate(containers, 1):
            try:
                result = client.create_a1_android_container(**container_config)
                print(f"容器 {i} 创建结果: {result}")
            except Exception as e:
                print(f"容器 {i} 创建失败: {e}")
        
        # 批量创建P1容器
        p1_containers = [
            {"ip": "192.168.1.100", "index": 20, "name": "batch_p1_1", "resolution": 0},
            {"ip": "192.168.1.100", "index": 21, "name": "batch_p1_2", "resolution": 1}
        ]
        
        print("\n7. 批量创建P1容器:")
        for i, container_config in enumerate(p1_containers, 1):
            try:
                result = client.create_p1_android_container(**container_config)
                print(f"P1容器 {i} 创建结果: {result}")
            except Exception as e:
                print(f"P1容器 {i} 创建失败: {e}")

def demo_error_handling():
    """演示错误处理"""
    print("\n=== 错误处理示例 ===")
    
    with create_client() as client:
        try:
            # 尝试使用无效参数创建容器
            print("\n8. 错误处理测试:")
            result = client.create_a1_android_container(
                ip="",  # 空IP地址
                index=-1,  # 无效索引
                name=""  # 空名称
            )
            print(f"意外成功: {result}")
            
        except MYTSDKError as e:
            print(f"捕获到MYT SDK错误: {e}")
        except ValueError as e:
            print(f"捕获到参数错误: {e}")
        except Exception as e:
            print(f"捕获到其他错误: {e}")

if __name__ == "__main__":
    print("MYT A1/P1安卓容器管理示例")
    print("注意: 请确保MYT服务器正在运行并且网络连接正常")
    
    try:
        # 运行所有示例
        demo_a1_container_creation()
        demo_a1_container_advanced()
        demo_p1_container_creation()
        demo_p1_container_with_proxy()
        demo_container_with_port_mapping()
        demo_batch_container_creation()
        demo_error_handling()
        
        print("\n=== 所有示例执行完成 ===")
        
    except KeyboardInterrupt:
        print("\n用户中断执行")
    except Exception as e:
        print(f"\n程序执行出错: {e}")