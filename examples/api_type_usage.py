#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API类型使用示例

演示如何使用不同的API类型配置来适应不同的服务器端点结构。
"""

from py_myt import MYTAPIClient


def demonstrate_api_types():
    """演示不同API类型的使用"""
    base_url = "http://127.0.0.1:5000"
    
    print("=== API类型使用示例 ===")
    print()
    
    # 1. 默认模式（无前缀）
    print("1. 默认模式 (api_type=None)")
    client_default = MYTAPIClient(base_url=base_url)
    print(f"   客户端配置: base_url={client_default.base_url}, api_type={client_default.api_type}")
    print("   登录请求URL: http://127.0.0.1:5000/login/admin/password123")
    print()
    
    # 2. v1模式（添加/and_api/v1/前缀）
    print("2. v1模式 (api_type='v1')")
    client_v1 = MYTAPIClient(base_url=base_url, api_type="v1")
    print(f"   客户端配置: base_url={client_v1.base_url}, api_type={client_v1.api_type}")
    print("   登录请求URL: http://127.0.0.1:5000/and_api/v1/login/admin/password123")
    print()
    
    # 3. P1模式（无前缀，仅标识）
    print("3. P1模式 (api_type='P1')")
    client_p1 = MYTAPIClient(base_url=base_url, api_type="P1")
    print(f"   客户端配置: base_url={client_p1.base_url}, api_type={client_p1.api_type}")
    print("   登录请求URL: http://127.0.0.1:5000/login/admin/password123")
    print()
    
    # 4. CQ1模式（无前缀，仅标识）
    print("4. CQ1模式 (api_type='CQ1')")
    client_cq1 = MYTAPIClient(base_url=base_url, api_type="CQ1")
    print(f"   客户端配置: base_url={client_cq1.base_url}, api_type={client_cq1.api_type}")
    print("   登录请求URL: http://127.0.0.1:5000/login/admin/password123")
    print()
    
    # 清理资源
    client_default.close()
    client_v1.close()
    client_p1.close()
    client_cq1.close()
    
    print("=== 使用建议 ===")
    print("- 如果服务器要求在所有API路径前添加 /and_api/v1/ 前缀，请使用 api_type='v1'")
    print("- 如果服务器使用标准路径，请使用默认配置（api_type=None）")
    print("- 其他API类型（P1, CQ1等）主要用于客户端标识，不影响实际请求路径")


def demonstrate_real_usage():
    """演示实际使用场景"""
    print("\n=== 实际使用场景演示 ===")
    print()
    
    # 场景1: 连接到v1 API服务器
    print("场景1: 连接到v1 API服务器")
    try:
        with MYTAPIClient(base_url="http://127.0.0.1:5000", api_type="v1") as client:
            print("   已创建v1 API客户端")
            print("   所有API调用将自动添加 /and_api/v1/ 前缀")
            # 这里可以添加实际的API调用
            # version = client.get_version()
            # print(f"   SDK版本: {version}")
    except Exception as e:
        print(f"   连接失败: {e}")
    
    print()
    
    # 场景2: 连接到标准API服务器
    print("场景2: 连接到标准API服务器")
    try:
        with MYTAPIClient(base_url="http://127.0.0.1:5000") as client:
            print("   已创建标准API客户端")
            print("   API调用使用原始路径")
            # 这里可以添加实际的API调用
            # version = client.get_version()
            # print(f"   SDK版本: {version}")
    except Exception as e:
        print(f"   连接失败: {e}")


if __name__ == "__main__":
    demonstrate_api_types()
    demonstrate_real_usage()