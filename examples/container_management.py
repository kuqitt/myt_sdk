#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
容器管理示例

演示如何使用MYT API客户端创建和管理安卓容器，包括：
- 容器创建和运行
- 文件操作（上传、下载）
- 剪切板操作
- 应用管理（安装、卸载、运行）
- 系统控制（截图、音频、ADB命令）
- 网络配置（S5代理）
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from py_myt import MYTAPIClient, MYTSDKError


def basic_container_creation():
    """基础容器创建示例"""
    print("=== 基础容器创建示例 ===")
    
    with MYTAPIClient() as client:
        try:
            # 基础容器创建
            result = client.create_android_container(
                ip="192.168.100.235",
                index=1,
                name="test_container_1"
            )
            print(f"容器创建结果: {result}")
            
        except MYTSDKError as e:
            print(f"创建失败: {e}")


def advanced_container_creation():
    """高级容器创建示例"""
    print("\n=== 高级容器创建示例 ===")
    
    with MYTAPIClient() as client:
        try:
            # 高级配置容器创建
            result = client.create_android_container(
                ip="192.168.1.100",
                index=2,
                name="advanced_container",
                # 性能配置
                memory=2048,  # 2GB内存
                cpu="0,1,2,3",  # 绑定CPU核心
                # 显示配置
                resolution=1,  # 1080P
                width=1080,
                height=1920,
                dpi=480,
                fps=60,
                # 网络配置
                dns="8.8.8.8",
                # 沙盒模式
                sandbox=1,
                sandbox_size=32,
                # 设备配置
                random_dev=0,  # 不随机设备信息
                mac="aa:bb:cc:dd:ee:ff",
                # 端口映射
                tcp_map_port="{5555:55555, 8080:58080}",
                udp_map_port="{9999:59999}",
                # ADB配置
                adbport=5555
            )
            print(f"高级容器创建结果: {result}")
            
        except MYTSDKError as e:
            print(f"创建失败: {e}")


def bridge_mode_container():
    """桥接模式容器创建示例"""
    print("\n=== 桥接模式容器创建示例 ===")
    
    with MYTAPIClient() as client:
        try:
            # 桥接模式配置
            bridge_config = {
                "gw": "192.168.1.1",
                "ip": "192.168.1.150",
                "subnet": "255.255.255.0"
            }
            
            result = client.create_android_container(
                ip="192.168.1.100",
                index=3,
                name="bridge_container",
                bridge_config=bridge_config
            )
            print(f"桥接模式容器创建结果: {result}")
            
        except MYTSDKError as e:
            print(f"创建失败: {e}")


def proxy_container():
    """代理配置容器创建示例"""
    print("\n=== 代理配置容器创建示例 ===")
    
    with MYTAPIClient() as client:
        try:
            # 使用SOCKS5代理
            result = client.create_android_container(
                ip="192.168.1.100",
                index=4,
                name="proxy_container",
                s5ip="127.0.0.1",
                s5port=1080,
                s5user="proxy_user",
                s5pwd="proxy_password"
            )
            print(f"代理容器创建结果: {result}")
            
        except MYTSDKError as e:
            print(f"创建失败: {e}")


def batch_container_creation():
    """批量容器创建示例"""
    print("\n=== 批量容器创建示例 ===")
    
    with MYTAPIClient() as client:
        containers = [
            {"ip": "192.168.1.100", "index": 10, "name": "batch_container_1"},
            {"ip": "192.168.1.100", "index": 11, "name": "batch_container_2"},
            {"ip": "192.168.1.101", "index": 10, "name": "batch_container_3"},
        ]
        
        success_count = 0
        for container in containers:
            try:
                result = client.create_android_container(**container)
                print(f"容器 {container['name']} 创建成功: {result.get('code', 'unknown')}")
                success_count += 1
            except MYTSDKError as e:
                print(f"容器 {container['name']} 创建失败: {e}")
        
        print(f"\n批量创建完成，成功: {success_count}/{len(containers)}")


def error_handling_example():
    """错误处理示例"""
    print("\n=== 错误处理示例 ===")
    
    with MYTAPIClient() as client:
        try:
            # 测试无效的桥接配置
            invalid_bridge_config = {
                "gw": "192.168.1.1",
                # 缺少ip和subnet字段
            }
            
            result = client.create_android_container(
                ip="192.168.1.100",
                index=99,
                name="error_test",
                bridge_config=invalid_bridge_config
            )
            
        except MYTSDKError as e:
            print(f"预期的错误: {e}")
        
        try:
            # 测试无效的桥接配置类型
            result = client.create_android_container(
                ip="192.168.1.100",
                index=98,
                name="error_test_2",
                bridge_config="invalid_config"  # 应该是字典类型
            )
            
        except MYTSDKError as e:
            print(f"预期的错误: {e}")


def container_list_and_run_examples():
    """容器列表和运行示例"""
    print("\n=== 容器列表和运行示例 ===")
    
    with MYTAPIClient() as client:
        try:
            host_ip = "192.168.1.100"
            
            # 获取所有容器列表
            print("1. 获取所有容器列表:")
            containers = client.get_android_containers(host_ip)
            print(f"容器列表: {containers}")
            
            # 获取指定索引的容器
            print("\n2. 获取索引为1的容器:")
            container_by_index = client.get_android_containers(host_ip, index="1")
            print(f"索引1容器: {container_by_index}")
            
            # 运行容器
            if containers.get('code') == 200 and containers.get('msg'):
                container_list = containers['msg']
                if container_list:
                    container_name = container_list[0].get('Names', '')
                    print(f"\n3. 运行容器: {container_name}")
                    run_result = client.run_android_container(host_ip, container_name)
                    print(f"运行结果: {run_result}")
                    
                    # 检查启动状态
                    print(f"\n4. 检查容器启动状态:")
                    boot_status = client.get_android_boot_status(host_ip, container_name)
                    print(f"启动状态: {boot_status}")
                    
        except Exception as e:
            print(f"操作失败: {e}")


def file_operations_examples():
    """文件操作示例"""
    print("\n=== 文件操作示例 ===")
    
    with MYTAPIClient() as client:
        try:
            host_ip = "192.168.1.100"
            container_name = "test_container"
            
            # 从URL上传文件
            print("1. 从URL上传文件:")
            upload_result = client.upload_url_file_to_android(
                host_ip, 
                container_name,
                url="https://example.com/test.apk",
                remote_path="/sdcard/Download/test.apk",
                retry=3
            )
            print(f"上传结果: {upload_result}")
            
            # 下载文件
            print("\n2. 下载文件:")
            download_result = client.download_file_from_android(
                host_ip,
                container_name,
                path="/sdcard/Download/test.apk",
                local="/tmp/downloaded_test.apk"
            )
            print(f"下载结果: {download_result}")
            
        except Exception as e:
            print(f"文件操作失败: {e}")


def clipboard_operations_examples():
    """剪切板操作示例"""
    print("\n=== 剪切板操作示例 ===")
    
    with MYTAPIClient() as client:
        try:
            host_ip = "192.168.1.100"
            container_name = "test_container"
            
            # 设置剪切板内容
            print("1. 设置剪切板内容:")
            set_result = client.set_clipboard_content(
                host_ip, container_name, "Hello from MYT API!"
            )
            print(f"设置结果: {set_result}")
            
            # 获取剪切板内容
            print("\n2. 获取剪切板内容:")
            get_result = client.get_clipboard_content(host_ip, container_name)
            print(f"剪切板内容: {get_result}")
            
        except Exception as e:
            print(f"剪切板操作失败: {e}")


def app_management_examples():
    """应用管理示例"""
    print("\n=== 应用管理示例 ===")
    
    with MYTAPIClient() as client:
        try:
            host_ip = "192.168.1.100"
            container_name = "test_container"
            package_name = "com.example.app"
            
            # 安装本地APK
            print("1. 安装本地APK:")
            install_result = client.install_apk(
                host_ip, container_name, "/path/to/local/app.apk"
            )
            print(f"安装结果: {install_result}")
            
            # 从URL安装APK
            print("\n2. 从URL安装APK:")
            install_url_result = client.install_apk_from_url(
                host_ip, container_name,
                url="https://example.com/app.apk",
                retry=2
            )
            print(f"URL安装结果: {install_url_result}")
            
            # 设置应用Root权限
            print("\n3. 设置应用Root权限:")
            root_result = client.set_app_root_permission(
                host_ip, container_name, package_name
            )
            print(f"Root权限设置结果: {root_result}")
            
            # 设置应用所有权限
            print("\n4. 设置应用所有权限:")
            permissions_result = client.set_app_all_permissions(
                host_ip, container_name, package_name
            )
            print(f"权限设置结果: {permissions_result}")
            
            # 运行应用
            print("\n5. 运行应用:")
            run_app_result = client.run_app(host_ip, container_name, package_name)
            print(f"运行应用结果: {run_app_result}")
            
            # 卸载应用
            print("\n6. 卸载应用:")
            uninstall_result = client.uninstall_apk(
                host_ip, container_name, package_name
            )
            print(f"卸载结果: {uninstall_result}")
            
        except Exception as e:
            print(f"应用管理失败: {e}")


def system_control_examples():
    """系统控制示例"""
    print("\n=== 系统控制示例 ===")
    
    with MYTAPIClient() as client:
        try:
            host_ip = "192.168.1.100"
            container_name = "test_container"
            
            # 获取截图
            print("1. 获取高清截图:")
            screenshot_result = client.take_screenshot(host_ip, container_name, 3)
            print(f"截图结果: {screenshot_result}")
            
            # 播放音频
            print("\n2. 播放音频:")
            audio_result = client.set_audio_playback(
                host_ip, container_name, "play", "/sdcard/Music/test.mp3"
            )
            print(f"音频播放结果: {audio_result}")
            
            # 执行ADB命令
            print("\n3. 执行ADB命令:")
            adb_result = client.execute_adb_command(
                host_ip, container_name, "pm list packages"
            )
            print(f"ADB命令结果: {adb_result}")
            
            # 设置分辨率感知白名单
            print("\n4. 设置分辨率感知白名单:")
            resolution_result = client.set_app_resolution_filter(
                host_ip, container_name, "com.example.app", 1
            )
            print(f"分辨率白名单结果: {resolution_result}")
            
        except Exception as e:
            print(f"系统控制失败: {e}")


def network_config_examples():
    """网络配置示例"""
    print("\n=== 网络配置示例 ===")
    
    with MYTAPIClient() as client:
        try:
            host_ip = "192.168.1.100"
            container_name = "test_container"
            
            # 设置S5域名过滤
            print("1. 设置S5域名过滤:")
            s5_filter_result = client.set_s5_filter_url(
                host_ip, container_name, "['www.baidu.com','qq.com']"
            )
            print(f"S5过滤设置结果: {s5_filter_result}")
            
            # 查询S5连接信息
            print("\n2. 查询S5连接信息:")
            s5_query_result = client.query_s5_connection(host_ip, container_name)
            print(f"S5连接信息: {s5_query_result}")
            
            # 上传谷歌证书
            print("\n3. 上传谷歌证书:")
            cert_result = client.upload_google_cert(
                host_ip, container_name, "/path/to/google_cert.p12"
            )
            print(f"证书上传结果: {cert_result}")
            
        except Exception as e:
            print(f"网络配置失败: {e}")


if __name__ == "__main__":
    print("MYT 容器管理示例")
    print("注意: 这些示例需要MYT SDK服务器运行在默认地址 127.0.0.1:5000")
    print("请确保目标主机IP地址可访问\n")
    
    try:
        basic_container_creation()
        # advanced_container_creation()
        # bridge_mode_container()
        # proxy_container()
        # batch_container_creation()
        error_handling_example()
        
        # 新增功能示例
        container_list_and_run_examples()
        file_operations_examples()
        clipboard_operations_examples()
        app_management_examples()
        system_control_examples()
        network_config_examples()
        
    except KeyboardInterrupt:
        print("\n用户中断操作")
    except Exception as e:
        print(f"\n未预期的错误: {e}")
    
    print("\n示例运行完成")