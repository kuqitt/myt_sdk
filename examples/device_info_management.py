#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
设备信息管理示例

演示如何使用 modify_device_info 接口进行设备信息管理，
包括获取机型字典表、随机设备机型等功能。
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from py_myt import MYTAPIClient


def main():
    """设备信息管理示例"""
    # 创建客户端
    client = MYTAPIClient(base_url="http://127.0.0.1:5000")
    
    try:
        ip = "192.168.1.100"
        container_name = "test_container"
        
        print("=== 设备信息管理示例 ===")
        
        # 1. 获取机型字典表
        print("\n1. 获取机型字典表...")
        try:
            result = client.modify_device_info(ip, container_name, "1")
            print(f"获取机型字典表结果: {result}")
        except Exception as e:
            print(f"获取机型字典表失败: {e}")
        
        # 2. 海外机型随机
        print("\n2. 海外机型随机...")
        try:
            result = client.modify_device_info(
                ip, container_name, "2", abroad=1
            )
            print(f"海外机型随机结果: {result}")
        except Exception as e:
            print(f"海外机型随机失败: {e}")
        
        # 3. 设置指定机型
        print("\n3. 设置指定机型...")
        try:
            result = client.modify_device_info(
                ip, container_name, "2", model_id=1
            )
            print(f"设置指定机型结果: {result}")
        except Exception as e:
            print(f"设置指定机型失败: {e}")
        
        # 4. 完整参数示例
        print("\n4. 完整参数示例...")
        try:
            result = client.modify_device_info(
                ip=ip,
                name=container_name,
                act="2",
                abroad=1,
                model_id=5,
                lang="en",  # 英语
                userip="192.168.1.200",
                is_async=1  # 使用异步方式
            )
            print(f"完整参数设置结果: {result}")
        except Exception as e:
            print(f"完整参数设置失败: {e}")
        
        # 5. 不同语言设置示例
        print("\n5. 不同语言设置示例...")
        languages = {
            "zh": "中文",
            "en": "英语", 
            "fr": "法语",
            "th": "泰语",
            "vi": "越南语",
            "ja": "日语",
            "ko": "韩语",
            "lo": "老挝语",
            "in": "印尼语"
        }
        
        for lang_code, lang_name in languages.items():
            try:
                result = client.modify_device_info(
                    ip, container_name, "2", lang=lang_code
                )
                print(f"设置{lang_name}({lang_code})结果: {result}")
                break  # 只演示一个语言设置
            except Exception as e:
                print(f"设置{lang_name}失败: {e}")
        
        print("\n=== 设备信息管理示例完成 ===")
        
    finally:
        # 关闭客户端连接
        client.close()
        print("\n客户端连接已关闭")


if __name__ == "__main__":
    main()