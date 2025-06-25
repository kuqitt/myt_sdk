# MYT API客户端使用指南

## 概述

MYT API客户端提供了与MYT SDK服务器通信的完整接口封装，支持所有主要的API操作。

## 安装

确保已安装py_myt包：

```bash
pip install -e .
```

## 快速开始

### 基本使用

```python
from py_myt import MYTAPIClient, create_client

# 创建客户端
client = MYTAPIClient(base_url="http://127.0.0.1:5000")

try:
    # 获取版本信息
    version = client.get_version()
    print(f"SDK版本: {version['data']}")
    
    # 用户登录
    login_result = client.login("admin", "password123")
    token = login_result['msg']
    
finally:
    client.close()
```

### 使用上下文管理器（推荐）

```python
from py_myt import create_client

with create_client() as client:
    # 获取在线设备列表
    devices = client.query_myt_devices()
    print(f"在线设备: {devices['data']}")
    
    # 获取镜像列表
    images = client.get_image_list_v2("p1")
    print(f"镜像数量: {len(images['msg'])}")
```

## API接口说明

### 1. 用户认证

#### 登录
```python
result = client.login(username, password)
# 返回: {"code": 200, "msg": "token_string"}
```

### 2. 系统信息

#### 获取版本信息
```python
version = client.get_version()
# 返回: {"code": 200, "data": "1.0.14.30.25", "message": ""}
```

### 3. 设备管理

#### 获取在线设备列表
```python
devices = client.query_myt_devices()
# 返回: {
#     "code": 200,
#     "message": "success",
#     "data": {"192.168.181.27": "device_id"}
# }
```

#### 获取机型信息
```python
device_info = client.get_device_info()
# 返回: {
#     "code": 200,
#     "msg": {
#         "HONOR": {
#             "AKA-AL10": 39
#         }
#     }
# }
```

#### 修改设备信息
```python
# 获取机型字典表
result = client.modify_device_info("192.168.1.100", "container1", "1")

# 海外机型随机
result = client.modify_device_info("192.168.1.100", "container1", "2", abroad=1)

# 设置指定机型
result = client.modify_device_info("192.168.1.100", "container1", "2", model_id=1)

# 完整参数示例
result = client.modify_device_info(
    ip="192.168.1.100",
    name="container1", 
    act="2",
    abroad=1,
    model_id=5,
    lang="en",  # zh中文/en英语/fr法语/th泰国/vi越南/ja日本/ko韩国/lo老挝/in印尼
    userip="192.168.1.200",
    is_async=1  # 推荐使用异步方式
)
# 返回: {"code": 200, "msg": "success"}
```

**参数说明：**
- `ip`: 3588主机IP地址（必选）
- `name`: 容器名称（必选）
- `act`: 操作类型（必选）
  - `"1"`: 获取机型字典表
  - `"2"`: 随机设备机型
- `abroad`: 1表示海外设备机型随机（可选）
- `model_id`: 指定机型ID（可选）
- `lang`: 指定语言（可选）
- `userip`: 指定环境对应IP所在区域（可选，仅支持IPv4）
- `is_async`: 1表示使用异步方式（可选，推荐使用）

**注意：** 此接口默认超时时间为60秒。

### 4. 镜像管理

#### 获取镜像列表V2（推荐）
```python
# 支持的镜像类型: p1, q1, a1, c1
images = client.get_image_list_v2("p1")
# 返回: {
#     "code": 200,
#     "msg": [
#         {
#             "id": "46",
#             "image": "registry.cn-hangzhou.aliyuncs.com/whsyf/dobox:rk3588-dm-base-20230807-01",
#             "name": "test_0807"
#         }
#     ]
# }
```

#### 获取镜像列表V1
```python
images = client.get_image_list_v1()
# 返回格式与V2相同
```

### 5. 容器管理

#### 创建安卓容器
```python
# 基础容器创建
result = client.create_android_container(
    ip="192.168.1.100",
    index=1,
    name="my_container"
)

# 高级配置
result = client.create_android_container(
    ip="192.168.1.100",
    index=2,
    name="advanced_container",
    memory=4096,  # 4GB内存
    cpu="0,1,2,3",  # 绑定4个CPU核心
    resolution=1,  # 1080P分辨率
    width=1080,
    height=1920,
    dpi=480,
    fps=60,
    dns="8.8.8.8"
)

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

# 代理配置
result = client.create_android_container(
    ip="192.168.1.100",
    index=4,
    name="proxy_container",
    s5ip="192.168.1.200",
    s5port=1080,
    s5user="proxy_user",
    s5pwd="proxy_pass"
)
```

#### 创建A1安卓容器

```python
# 基础A1容器创建
result = client.create_a1_android_container(
    ip="192.168.1.100",
    index=1,
    name="a1_container"
)

# 高级A1容器配置
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

# A1容器端口映射配置
result = client.create_a1_android_container(
    ip="192.168.1.100",
    index=3,
    name="port_mapping_a1",
    tcp_map_port="{20000:50001, 30000:50002}",  # TCP端口映射
    udp_map_port="{25000:50003, 35000:50004}",  # UDP端口映射
    adbport=55555,  # ADB端口
    rpaport=56666  # RPA端口映射
)
```

#### 创建P1安卓容器

```python
# 基础P1容器创建
result = client.create_p1_android_container(
    ip="192.168.1.100",
    index=1,
    name="p1_container"
)

# P1容器代理配置
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

# P1容器自定义分辨率
result = client.create_p1_android_container(
    ip="192.168.1.100",
    index=3,
    name="custom_resolution_p1",
    resolution=2,  # 自定义分辨率
    width=1440,
    height=2560,
    dpi=560,
    fps=90
)
```

#### 容器创建参数说明

**必需参数:**
- `ip`: 主机IP地址
- `index`: 容器索引
- `name`: 容器名称

**性能配置:**
- `memory`: 内存限制大小(MB)，默认0
- `cpu`: 绑定的CPU核心，如"0,4"，可选

**显示配置:**
- `resolution`: 分辨率参数，0=720P, 1=1080P, 2=自定义，默认0
- `width`: 宽度，默认720
- `height`: 高度，默认1280
- `dpi`: 分辨率，默认320
- `fps`: 刷新率，默认24

**网络配置:**
- `dns`: 域名地址，默认223.5.5.5
- `s5ip`: SOCKS5代理服务器地址
- `s5port`: SOCKS5代理端口
- `s5user`: SOCKS5代理用户名
- `s5pwd`: SOCKS5代理密码

**沙盒配置:**
- `sandbox`: 是否使用沙盒模式，0=不使用, 1=使用，默认0
- `sandbox_size`: 沙盒空间大小，默认16

**设备配置:**
- `random_dev`: 创建时是否自动随机设备信息，默认1
- `mac`: 主机的MAC地址，格式如"11:11:11:11:11:11"
- `initdev`: 初始时的设备信息ID

**端口配置:**
- `tcp_map_port`: TCP端口映射，格式"{20000:20001, 30000:30001}"
- `udp_map_port`: UDP端口映射，格式"{20000:20001, 30000:30001}"
- `adbport`: ADB端口，默认0
- `rpaport`: RPA端口映射，默认0

**其他配置:**
- `image_addr`: 镜像地址
- `img_url`: URL镜像地址
- `data_res`: 容器的资源目录
- `timeoffset`: 设置已开机的时间，默认0
- `enablemeid`: 是否启用MEID，默认0
- `phyinput`: 是否使用物理触屏输入，默认0
- `enforce`: 设置严格模式，默认1
- `dnstcp_mode`: 使用dnstcp模式，默认0

**桥接模式配置:**
- `bridge_config`: 桥接模式配置字典，包含以下字段：
  - `gw`: 网关地址
  - `ip`: IP地址
  - `subnet`: 子网掩码

## 配置选项

### 自定义服务器地址和超时时间

```python
client = MYTAPIClient(
    base_url="http://192.168.1.100:8080",
    timeout=60  # 60秒超时
)
```

### 默认配置

- **默认服务器地址**: `http://127.0.0.1:5000`
- **默认超时时间**: 30秒
- **User-Agent**: `MYT-SDK-Client/1.0.0`
- **Content-Type**: `application/json`

## 错误处理

所有API调用都可能抛出`MYTSDKError`异常：

```python
from py_myt import create_client, MYTSDKError

with create_client() as client:
    try:
        version = client.get_version()
    except MYTSDKError as e:
        print(f"API调用失败: {e}")
```

### 常见错误类型

- **连接错误**: 服务器无法访问
- **超时错误**: 请求超时
- **HTTP错误**: 服务器返回错误状态码
- **JSON解析错误**: 响应不是有效的JSON格式
- **参数错误**: 传入了无效的参数

## 设备管理功能

### 获取安卓实例详细信息

获取指定安卓容器的详细信息，包括状态、配置、网络等信息。

```python
# 获取安卓实例详细信息
result = client.get_android_detail(
    ip="192.168.1.100",
    name="test_container"
)

if result["code"] == 200:
    device_info = result["msg"]
    print(f"设备状态: {device_info['status']}")
    print(f"分辨率: {device_info['width']}x{device_info['height']}")
    print(f"内存限制: {device_info['memory']} MB")
    print(f"本地IP: {device_info['local_ip']}")
    print(f"RPA端口: {device_info['rpa']}")
```

### 获取主机版本信息

获取MYT主机的版本信息。

```python
# 获取主机版本
result = client.get_host_version(ip="192.168.1.100")
print(f"主机版本: {result['msg']}")
```

### 上传文件到安卓容器

将本地文件上传到指定的安卓容器中。注意：本地文件必须与SDK在同一台主机上。

```python
# 上传APK文件
result = client.upload_file_to_android(
    ip="192.168.1.100",
    name="test_container",
    local_file="/home/user/Downloads/test.apk"
)

# 上传配置文件
result = client.upload_file_to_android(
    ip="192.168.1.100",
    name="test_container",
    local_file="/home/user/config.json"
)
```

### 随机更换设备信息

#### 同步随机设备信息

```python
# 基础随机设备信息
result = client.random_device_info(
    ip="192.168.1.100",
    name="test_container"
)

# 指定IP和设备型号的随机设备信息
result = client.random_device_info(
    ip="192.168.1.100",
    name="test_container",
    userip="192.168.1.200",  # 指定IP信息随机
    modelid="samsung_s21"     # 指定设备型号ID
)
```

#### 异步随机设备信息

```python
# 异步随机设备信息
result = client.random_device_info_async(
    ip="192.168.1.100",
    name="test_container",
    userip="192.168.1.200",
    modelid="xiaomi_mi11"
)
```

#### 异步随机设备信息2（支持任务管理）

```python
# 提交异步请求
result = client.random_device_info_async2(
    ip="192.168.1.100",
    name="test_container",
    act="request",  # 请求结果
    userip="192.168.1.150"
)

# 查询任务状态
result = client.random_device_info_async2(
    ip="192.168.1.100",
    name="test_container",
    act="query"  # 获取结果
)

# 获取结果并清空任务进度
result = client.random_device_info_async2(
    ip="192.168.1.100",
    name="test_container",
    act="get"  # 获取并清空
)
```

## 容器管理功能

### 获取容器列表

```python
# 获取所有容器
result = client.get_android_containers("192.168.1.100")
print(f"所有容器: {result}")

# 获取指定索引的容器
result = client.get_android_containers("192.168.1.100", index="1")
print(f"索引1的容器: {result}")

# 获取指定名称的容器
result = client.get_android_containers("192.168.1.100", name="test_container")
print(f"指定容器: {result}")
```

### 运行容器

```python
# 普通运行容器
result = client.run_android_container("192.168.1.100", "container_name")
print(f"运行结果: {result}")

# 强制运行容器
result = client.run_android_container("192.168.1.100", "container_name", force="1")
print(f"强制运行结果: {result}")
```

### 文件操作

```python
# 从URL上传文件
result = client.upload_url_file_to_android(
    "192.168.1.100", 
    "container_name",
    "https://example.com/file.apk",
    "/sdcard/Download/file.apk",
    retry=3
)
print(f"URL上传结果: {result}")

# 下载文件
result = client.download_file_from_android(
    "192.168.1.100", 
    "container_name",
    "/sdcard/Download/file.apk",
    "/local/path/file.apk"
)
print(f"下载结果: {result}")
```

### 剪切板操作

```python
# 获取剪切板内容
result = client.get_clipboard_content("192.168.1.100", "container_name")
print(f"剪切板内容: {result}")

# 设置剪切板内容
result = client.set_clipboard_content("192.168.1.100", "container_name", "Hello World")
print(f"设置剪切板结果: {result}")
```

### 系统状态

```python
# 检查启动状态
result = client.get_android_boot_status(
    "192.168.1.100", 
    "container_name",
    isblock=1,
    timeout=60,
    init_devinfo=1
)
print(f"启动状态: {result}")

# 获取截图
result = client.take_screenshot("192.168.1.100", "container_name", level=3)
print(f"截图结果: {result}")
```

### 应用管理

```python
# 安装APK（本地文件）
result = client.install_apk("192.168.1.100", "container_name", "/path/to/app.apk")
print(f"安装结果: {result}")

# 从URL安装APK
result = client.install_apk_from_url(
    "192.168.1.100", 
    "container_name",
    "https://example.com/app.apk",
    retry=2
)
print(f"URL安装结果: {result}")

# 卸载APK
result = client.uninstall_apk("192.168.1.100", "container_name", "com.example.app")
print(f"卸载结果: {result}")

# 运行应用
result = client.run_app("192.168.1.100", "container_name", "com.example.app")
print(f"运行应用结果: {result}")
```

### 权限管理

```python
# 设置Root权限
result = client.set_app_root_permission("192.168.1.100", "container_name", "com.example.app")
print(f"Root权限设置结果: {result}")

# 设置所有权限
result = client.set_app_all_permissions("192.168.1.100", "container_name", "com.example.app")
print(f"所有权限设置结果: {result}")

# 设置分辨率感知白名单
result = client.set_app_resolution_filter(
    "192.168.1.100", 
    "container_name", 
    "com.example.app", 
    enable=1
)
print(f"分辨率过滤设置结果: {result}")
```

### 系统控制

```python
# 音频播放控制
result = client.set_audio_playback(
    "192.168.1.100", 
    "container_name", 
    "play", 
    "/sdcard/Music/test.mp3"
)
print(f"音频播放结果: {result}")

# 执行ADB命令
result = client.execute_adb_command(
    "192.168.1.100", 
    "container_name", 
    "pm list packages"
)
print(f"ADB命令结果: {result}")

# 执行ADB命令2
result = client.execute_adb_command2(
    "192.168.1.100", 
    "container_name", 
    "getprop ro.build.version.release"
)
print(f"ADB命令2结果: {result}")
```

### 网络配置

```python
# 上传谷歌证书
result = client.upload_google_cert(
    "192.168.1.100", 
    "container_name", 
    "/path/to/cert.p12"
)
print(f"证书上传结果: {result}")

# 设置S5域名过滤
result = client.set_s5_filter_url(
    "192.168.1.100", 
    "container_name", 
    "['www.baidu.com','qq.com']"
)
print(f"S5过滤设置结果: {result}")

# 查询S5连接信息
result = client.query_s5_connection("192.168.1.100", "container_name")
print(f"S5连接信息: {result}")
```

### 自定义设备机型信息（数字孪生）

**重要提示**: 该功能请谨慎使用，如果传入的数据异常，可能会导致系统无法开机。

#### 真机数据提取工具

- 工具版本2下载地址: https://gitee.com/zwj5151/myt_tools/raw/master/myt_dev_tools_v2.zip
- 百度网盘下载地址: https://pan.baidu.com/s/1TQLQOuJEXLiQRajEX4huyg?pwd=lqs8

#### 使用流程

1. 在要提取的真机上安装工具，获取数据下载地址
2. 将真机数据通过该接口传入指定的云机

```python
# 基础自定义设备信息
device_data = '''
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
'''

result = client.set_custom_device_info(
    ip="192.168.1.100",
    name="test_container",
    device_data=device_data
)

# 完整参数自定义设备信息
result = client.set_custom_device_info(
    ip="192.168.1.100",
    name="test_container",
    device_data=device_data,
    android_id="1234567890abcdef",      # Android ID
    iccid="89860000000000000000",       # SIM卡ICCID
    imei="123456789012345",             # IMEI号
    imsi="123456789012345",             # IMSI号
    series_num="R58N123ABCD",           # 序列号
    btaddr="AA:BB:CC:DD:EE:FF",         # 蓝牙地址
    btname="Samsung Galaxy S21",        # 蓝牙名称
    wifi_mac="11:22:33:44:55:66",       # WiFi MAC地址
    wifi_name="Galaxy-S21",             # WiFi名称
    oaid="12345678-1234-1234-1234-123456789012",  # OAID
    aaid="12345678-1234-1234-1234-123456789012",  # AAID
    vaid="12345678-1234-1234-1234-123456789012"   # VAID
)
```

#### 支持的自定义参数

| 参数名 | 类型 | 必选 | 说明 |
|--------|------|------|------|
| ip | str | 是 | 3588主机IP地址 |
| name | str | 是 | 容器实例名称 |
| device_data | str | 是 | 导出的真机信息数据 |
| android_id | str | 否 | Android ID |
| iccid | str | 否 | SIM卡ICCID |
| imei | str | 否 | IMEI号 |
| imsi | str | 否 | IMSI号 |
| series_num | str | 否 | 序列号 |
| btaddr | str | 否 | 蓝牙地址 |
| btname | str | 否 | 蓝牙名称 |
| wifi_mac | str | 否 | WiFi MAC地址 |
| wifi_name | str | 否 | WiFi名称 |
| oaid | str | 否 | OAID |
| aaid | str | 否 | AAID |
| vaid | str | 否 | VAID |

## 批量操作示例

```python
with create_client() as client:
    # 批量获取不同类型的镜像
    image_types = ['p1', 'q1', 'a1', 'c1']
    
    for img_type in image_types:
        try:
            images = client.get_image_list_v2(img_type)
            print(f"镜像类型 {img_type}: {len(images['msg'])} 个镜像")
        except MYTSDKError as e:
            print(f"获取镜像类型 {img_type} 失败: {e}")
```

## 完整示例

查看 `examples/api_client_usage.py` 文件获取更多使用示例。

## 注意事项

1. **服务器状态**: 确保MYT SDK服务器正在运行
2. **网络连接**: 确保客户端能够访问服务器地址
3. **资源管理**: 使用上下文管理器或手动调用`close()`方法释放连接
4. **错误处理**: 始终捕获和处理`MYTSDKError`异常
5. **参数验证**: 某些API有参数限制，如镜像类型只支持特定值

## 开发和测试

运行测试：

```bash
python -m pytest tests/test_api_client.py -v
```

运行示例：

```bash
python examples/api_client_usage.py
```