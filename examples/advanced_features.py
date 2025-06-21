#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MYT SDK 高级功能使用示例

本示例展示了如何使用MYT SDK的高级功能，包括：
- S5代理连接管理
- 摄像头控制和推流设置
- 传感器配置
- 位置服务
- 视频预处理
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from py_myt import create_client
from py_myt.exceptions import MYTSDKError

def main():
    """主函数"""
    # 创建API客户端
    client = create_client(base_url="http://192.168.1.100:5000")
    
    # 容器信息
    ip = "192.168.1.100"
    container_name = "demo_container"
    
    try:
        print("=== MYT SDK 高级功能演示 ===")
        
        # 1. S5代理连接管理
        print("\n1. 设置S5代理连接...")
        s5_result = client.set_s5_connection(
            ip=ip,
            name=container_name,
            s5ip="127.0.0.1",
            s5port="1080",
            s5user="proxy_user",
            s5pwd="proxy_pass",
            domain_mode=2  # 服务端域名解析
        )
        print(f"S5连接设置结果: {s5_result}")
        
        # 2. 摄像头功能
        print("\n2. 摄像头功能演示...")
        
        # 获取当前摄像头推流信息
        stream_info = client.get_camera_stream(ip=ip, name=container_name)
        print(f"当前摄像头推流信息: {stream_info}")
        
        # 设置摄像头旋转（90度旋转，不镜像）
        rotation_result = client.set_camera_rotation(
            ip=ip,
            name=container_name,
            rot=1,  # 90度旋转
            face=0  # 不镜像
        )
        print(f"摄像头旋转设置结果: {rotation_result}")
        
        # 设置摄像头推流（RTMP流）
        stream_result = client.set_camera_stream(
            ip=ip,
            name=container_name,
            v_type=1,  # RTMP视频流
            resolution=1,  # 1920x1080@30
            addr="rtmp://live.example.com/stream/demo"
        )
        print(f"摄像头推流设置结果: {stream_result}")
        
        # 3. 传感器配置
        print("\n3. 传感器配置...")
        
        # 设置运动传感器灵敏度
        motion_result = client.set_motion_sensitivity(
            ip=ip,
            name=container_name,
            factor=500  # 中等灵敏度
        )
        print(f"运动传感器设置结果: {motion_result}")
        
        # 开启摇一摇功能
        shake_result = client.set_shake_status(
            ip=ip,
            name=container_name,
            enable=1  # 开启
        )
        print(f"摇一摇功能设置结果: {shake_result}")
        
        # 4. 位置服务
        print("\n4. 位置服务配置...")
        
        # IP智能定位（设置为中文环境）
        ip_location_result = client.set_ip_location(
            ip=ip,
            name=container_name,
            language="zh"  # 中文
        )
        print(f"IP智能定位设置结果: {ip_location_result}")
        
        # 手动设置设备位置（北京坐标）
        location_result = client.set_device_location(
            ip=ip,
            name=container_name,
            lat=39.9042,  # 北京纬度
            lng=116.4074  # 北京经度
        )
        print(f"设备位置设置结果: {location_result}")
        
        # 5. 视频预处理
        print("\n5. 视频预处理...")
        video_path = "/path/to/your/video.mp4"
        print(f"预处理视频文件: {video_path}")
        
        # 注意：这里使用示例路径，实际使用时请替换为真实的视频文件路径
        try:
            preprocess_result = client.preprocess_video(path=video_path)
            print(f"视频预处理结果: {preprocess_result}")
        except MYTSDKError as e:
            print(f"视频预处理失败（可能是文件路径不存在）: {e}")
        
        # 6. 关闭S5连接
        print("\n6. 关闭S5连接...")
        stop_s5_result = client.stop_s5_connection(ip=ip, name=container_name)
        print(f"S5连接关闭结果: {stop_s5_result}")
        
        print("\n=== 高级功能演示完成 ===")
        
    except MYTSDKError as e:
        print(f"操作失败: {e}")
        return 1
    except Exception as e:
        print(f"未知错误: {e}")
        return 1
    
    return 0

def demonstrate_camera_scenarios():
    """演示不同的摄像头使用场景"""
    client = create_client(base_url="http://192.168.1.100:5000")
    ip = "192.168.1.100"
    container_name = "camera_demo"
    
    print("\n=== 摄像头使用场景演示 ===")
    
    scenarios = [
        {
            "name": "RTMP直播流",
            "v_type": 1,
            "resolution": 1,
            "addr": "rtmp://live.example.com/stream/live"
        },
        {
            "name": "WebRTC视频通话",
            "v_type": 2,
            "resolution": 2,
            "addr": "webrtc://call.example.com/room/123"
        },
        {
            "name": "本地图片展示",
            "v_type": 3,
            "addr": "/sdcard/Pictures/demo.jpg"
        },
        {
            "name": "网络图片展示",
            "v_type": 3,
            "addr": "https://example.com/images/demo.png"
        }
    ]
    
    for scenario in scenarios:
        print(f"\n配置场景: {scenario['name']}")
        try:
            result = client.set_camera_stream(
                ip=ip,
                name=container_name,
                v_type=scenario['v_type'],
                resolution=scenario.get('resolution'),
                addr=scenario['addr']
            )
            print(f"配置结果: {result}")
        except MYTSDKError as e:
            print(f"配置失败: {e}")

def demonstrate_location_scenarios():
    """演示不同的位置设置场景"""
    client = create_client(base_url="http://192.168.1.100:5000")
    ip = "192.168.1.100"
    container_name = "location_demo"
    
    print("\n=== 位置服务场景演示 ===")
    
    # 不同城市的坐标
    cities = [
        {"name": "北京", "lat": 39.9042, "lng": 116.4074, "lang": "zh"},
        {"name": "上海", "lat": 31.2304, "lng": 121.4737, "lang": "zh"},
        {"name": "纽约", "lat": 40.7128, "lng": -74.0060, "lang": "en"},
        {"name": "东京", "lat": 35.6762, "lng": 139.6503, "lang": "ja"},
        {"name": "首尔", "lat": 37.5665, "lng": 126.9780, "lang": "ko"}
    ]
    
    for city in cities:
        print(f"\n设置位置为: {city['name']}")
        try:
            # 设置语言环境
            lang_result = client.set_ip_location(
                ip=ip,
                name=container_name,
                language=city['lang']
            )
            print(f"语言环境设置: {lang_result}")
            
            # 设置具体坐标
            location_result = client.set_device_location(
                ip=ip,
                name=container_name,
                lat=city['lat'],
                lng=city['lng']
            )
            print(f"位置坐标设置: {location_result}")
            
        except MYTSDKError as e:
            print(f"位置设置失败: {e}")

if __name__ == "__main__":
    # 运行主演示
    exit_code = main()
    
    # 运行场景演示
    if exit_code == 0:
        demonstrate_camera_scenarios()
        demonstrate_location_scenarios()
    
    sys.exit(exit_code)