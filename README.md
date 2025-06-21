# MYT SDK

魔云腾SDK通用包 - 用于自动下载、管理和启动MYT SDK

## 描述

MYT SDK是一个Python包，用于简化MYT SDK的下载、安装和启动过程。它会自动检测系统中是否已安装SDK，如果没有则从指定URL下载并解压到用户缓存目录，然后启动SDK进程。

## 特性

- 🚀 自动下载和安装MYT SDK
- 📁 智能缓存管理（使用系统缓存目录）
- 🔍 进程检测（避免重复启动）
- 🛡️ 完善的错误处理和日志记录
- 💻 Windows
- 🎯 简单的命令行接口
- 🌐 完整的API客户端支持
- 📱 容器管理和设备控制
- 🎥 摄像头和传感器配置
- 📍 位置服务和代理管理
- 📊 GitHub仓库实时监控和统计

## 安装

### 从PyPI安装（推荐）

```bash
pip install myt-sdk
```

### 从源码安装

```bash
git clone https://github.com/moyunteng/myt-sdk.git
cd myt-sdk
pip install -e .
```

## 使用方法

### 命令行使用

#### 初始化SDK（下载并启动）

```bash
# 基本初始化
myt-sdk init

# 强制重新下载
myt-sdk init --force

# 只下载不启动
myt-sdk init --no-start

# 使用自定义缓存目录
myt-sdk init --cache-dir /path/to/cache

# 启用详细日志
myt-sdk init --verbose
```

#### 查看SDK状态

```bash
myt-sdk status
```

### Python代码使用

#### SDK管理器

```python
from py_myt import MYTSDKManager

# 创建SDK管理器
sdk_manager = MYTSDKManager()

# 检查SDK状态
status = sdk_manager.get_status()
print(f"SDK已安装: {status['installed']}")
print(f"SDK正在运行: {status['running']}")

# 初始化SDK
result = sdk_manager.init()
print(f"初始化结果: {result}")
```

#### API客户端

```python
from py_myt import create_client
from py_myt.exceptions import MYTSDKError

# 创建API客户端
client = create_client(base_url="http://192.168.1.100:5000")

try:
    # 容器管理
    containers = client.get_containers(ip="192.168.1.100")
    print(f"容器列表: {containers}")
    
    # 创建Android容器
    result = client.create_android_container(
        ip="192.168.1.100",
        index=1,
        name="my_container",
        image_addr="android_image"
    )
    print(f"容器创建结果: {result}")
    
    # 设置摄像头推流
    client.set_camera_stream(
        ip="192.168.1.100",
        name="my_container",
        v_type=1,  # RTMP流
        resolution=1,  # 1920x1080@30
        addr="rtmp://live.example.com/stream"
    )
    
    # 配置S5代理
    client.set_s5_connection(
        ip="192.168.1.100",
        name="my_container",
        s5ip="127.0.0.1",
        s5port="1080",
        s5user="username",
        s5pwd="password"
    )
    
except MYTSDKError as e:
    print(f"API调用失败: {e}")
```

## API功能

### 容器管理
- 创建/删除Android容器
- 容器状态查询和控制
- 批量容器操作
- 容器配置管理

### 设备控制
- 设备信息查询
- 主机版本管理
- 文件上传下载
- 随机设备信息生成

### 摄像头功能
- 获取摄像头推流信息
- 设置摄像头旋转和镜像
- 配置RTMP/WebRTC推流
- 图片显示设置

### 传感器配置
- 运动传感器灵敏度调节
- 摇一摇功能开关
- 传感器状态监控

### 位置服务
- IP智能定位
- 手动设置设备位置
- 多语言环境支持

### 代理管理
- S5代理连接设置
- 代理状态控制
- 域名解析配置

### 视频处理
- 视频文件预处理
- 播放优化

### GitHub监控
- 实时访问统计
- 仓库流量分析
- 下载量监控
- 用户行为追踪

## GitHub仓库

### 统计

[![GitHub stars](https://img.shields.io/github/stars/kuqitt/myt_sdk?style=social)](https://github.com/kuqitt/myt_sdk/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/kuqitt/myt_sdk?style=social)](https://github.com/kuqitt/myt_sdk/network/members)
[![GitHub watchers](https://img.shields.io/github/watchers/kuqitt/myt_sdk?style=social)](https://github.com/kuqitt/myt_sdk/watchers)
[![GitHub issues](https://img.shields.io/github/issues/kuqitt/myt_sdk)](https://github.com/kuqitt/myt_sdk/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/kuqitt/myt_sdk)](https://github.com/kuqitt/myt_sdk/pulls)

### 下载统计

[![GitHub all releases](https://img.shields.io/github/downloads/kuqitt/myt_sdk/total)](https://github.com/kuqitt/myt_sdk/releases)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/kuqitt/myt_sdk)](https://github.com/kuqitt/myt_sdk/releases/latest)
[![PyPI downloads](https://img.shields.io/pypi/dm/myt-sdk)](https://pypi.org/project/myt-sdk/)

### 代码质量

[![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/kuqitt/myt_sdk)](https://github.com/kuqitt/myt_sdk)
[![GitHub repo size](https://img.shields.io/github/repo-size/kuqitt/myt_sdk)](https://github.com/kuqitt/myt_sdk)
[![GitHub language count](https://img.shields.io/github/languages/count/kuqitt/myt_sdk)](https://github.com/kuqitt/myt_sdk)
[![GitHub top language](https://img.shields.io/github/languages/top/kuqitt/myt_sdk)](https://github.com/kuqitt/myt_sdk)

### 活跃度统计

[![GitHub commit activity](https://img.shields.io/github/commit-activity/m/kuqitt/myt_sdk)](https://github.com/kuqitt/myt_sdk/graphs/commit-activity)
[![GitHub last commit](https://img.shields.io/github/last-commit/kuqitt/myt_sdk)](https://github.com/kuqitt/myt_sdk/commits/main)
[![GitHub contributors](https://img.shields.io/github/contributors/kuqitt/myt_sdk)](https://github.com/kuqitt/myt_sdk/graphs/contributors)


## 文档

- [API客户端文档](docs/api_client.md)
- [高级API方法文档](docs/advanced_api_methods.md)
- [示例代码](examples/)

## 开发

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_api_client.py
pytest tests/test_new_api_methods.py

# 运行测试并显示覆盖率
pytest --cov=py_myt
```

### 代码格式化

```bash
black py_myt/
```

### 类型检查

```bash
mypy py_myt/
```

```bash
flake8 py_myt/
```

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 更新日志

### 0.2.0
- 新增完整的API客户端支持
- 添加容器管理功能
- 实现摄像头控制API
- 添加传感器配置功能
- 支持位置服务和代理管理
- 新增视频预处理功能
- 完善测试覆盖率
- 添加详细文档和示例

### 0.1.0
- 初始版本