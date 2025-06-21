# MYT SDK 高级API方法文档

本文档介绍了MYT SDK中新增的高级API方法，包括S5代理连接管理、摄像头控制、传感器配置、位置服务等功能。

## S5代理连接管理

### 设置S5连接

```python
from py_myt import create_client

client = create_client()

# 设置S5代理连接
result = client.set_s5_connection(
    ip="192.168.1.100",
    name="container_name",
    s5ip="127.0.0.1",
    s5port="1080",
    s5user="username",
    s5pwd="password",
    domain_mode=2  # 1=本地域名解析, 2=服务端域名解析(默认)
)
```

### 关闭S5连接

```python
# 关闭S5代理连接
result = client.stop_s5_connection(
    ip="192.168.1.100",
    name="container_name"
)
```

## 摄像头控制

### 获取摄像头推流信息

```python
# 获取当前摄像头推流地址和类型
stream_info = client.get_camera_stream(
    ip="192.168.1.100",
    name="container_name"
)
print(f"推流地址: {stream_info['msg']['stream_url']}")
print(f"推流类型: {stream_info['msg']['stream_type']}")
```

### 设置摄像头旋转

```python
# 设置摄像头旋转和镜像
result = client.set_camera_rotation(
    ip="192.168.1.100",
    name="container_name",
    rot=1,  # 0=不旋转, 1=90度, 2=180度, 3=270度
    face=0  # 0=不镜像, 1=镜像
)
```

### 设置摄像头推流

```python
# 设置RTMP推流
result = client.set_camera_stream(
    ip="192.168.1.100",
    name="container_name",
    v_type=1,  # 1=RTMP流, 2=WebRTC流, 3=图片
    resolution=1,  # 1=1920x1080@30, 2=1280x720@30
    addr="rtmp://live.example.com/stream/demo"
)

# 设置WebRTC推流
result = client.set_camera_stream(
    ip="192.168.1.100",
    name="container_name",
    v_type=2,
    resolution=2,
    addr="webrtc://call.example.com/room/123"
)

# 设置图片显示
result = client.set_camera_stream(
    ip="192.168.1.100",
    name="container_name",
    v_type=3,
    addr="https://example.com/image.jpg"
)
```

## 传感器配置

### 设置运动传感器灵敏度

```python
# 设置运动传感器灵敏度
result = client.set_motion_sensitivity(
    ip="192.168.1.100",
    name="container_name",
    factor=500  # 范围[0,1000]: 0=关闭, 10=静止, 1000=运动状态
)
```

### 设置摇一摇功能

```python
# 开启摇一摇功能
result = client.set_shake_status(
    ip="192.168.1.100",
    name="container_name",
    enable=1  # 0=关闭, 1=开启
)
```

## 位置服务

### IP智能定位

```python
# 根据IP自动设置环境信息
result = client.set_ip_location(
    ip="192.168.1.100",
    name="container_name",
    language="zh"  # zh=中文, en=英语, fr=法语, th=泰国, vi=越南, ja=日本, ko=韩国, lo=老挝, in=印尼
)
```

### 手动设置设备位置

```python
# 手动设置设备经纬度
result = client.set_device_location(
    ip="192.168.1.100",
    name="container_name",
    lat=39.9042,  # 纬度
    lng=116.4074  # 经度
)
```

## 视频预处理

### 预处理视频文件

```python
# 预处理视频文件以减少播放卡顿
result = client.preprocess_video(
    path="/path/to/video.mp4"  # 视频文件完整路径
)
```

## 完整使用示例

```python
from py_myt import create_client
from py_myt.exceptions import MYTSDKError

def setup_container_advanced_features():
    """配置容器的高级功能"""
    client = create_client(base_url="http://192.168.1.100:5000")
    
    ip = "192.168.1.100"
    container_name = "demo_container"
    
    try:
        # 1. 设置S5代理
        print("设置S5代理...")
        client.set_s5_connection(
            ip=ip, name=container_name,
            s5ip="127.0.0.1", s5port="1080",
            s5user="proxy_user", s5pwd="proxy_pass"
        )
        
        # 2. 配置摄像头
        print("配置摄像头...")
        client.set_camera_rotation(ip=ip, name=container_name, rot=0, face=0)
        client.set_camera_stream(
            ip=ip, name=container_name, v_type=1,
            resolution=1, addr="rtmp://live.example.com/stream"
        )
        
        # 3. 设置传感器
        print("配置传感器...")
        client.set_motion_sensitivity(ip=ip, name=container_name, factor=500)
        client.set_shake_status(ip=ip, name=container_name, enable=1)
        
        # 4. 设置位置
        print("配置位置信息...")
        client.set_ip_location(ip=ip, name=container_name, language="zh")
        client.set_device_location(ip=ip, name=container_name, lat=39.9042, lng=116.4074)
        
        print("高级功能配置完成!")
        
    except MYTSDKError as e:
        print(f"配置失败: {e}")

if __name__ == "__main__":
    setup_container_advanced_features()
```

## 错误处理

所有API方法都可能抛出 `MYTSDKError` 异常，建议使用try-catch进行错误处理：

```python
from py_myt.exceptions import MYTSDKError

try:
    result = client.set_camera_stream(
        ip="192.168.1.100",
        name="container_name",
        v_type=1,
        addr="rtmp://invalid.url"
    )
except MYTSDKError as e:
    print(f"API调用失败: {e}")
    # 处理错误逻辑
except Exception as e:
    print(f"未知错误: {e}")
```

## 返回值格式

所有API方法的返回值都遵循统一格式：

```json
{
    "code": 200,
    "msg": "操作成功" // 或包含具体数据的对象
}
```

- `code`: HTTP状态码，200表示成功
- `msg`: 响应消息或数据对象

## 注意事项

1. **参数验证**: 所有必需参数都会进行验证，确保传入正确的数据类型和值范围
2. **网络连接**: 确保客户端能够访问目标主机的API服务
3. **容器状态**: 某些操作需要容器处于运行状态
4. **权限要求**: 部分功能可能需要特定的系统权限
5. **资源限制**: 注意系统资源限制，避免设置过高的参数值

更多详细信息请参考 [API客户端文档](api_client.md) 和 [示例代码](../examples/advanced_features.py)。