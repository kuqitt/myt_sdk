# MYT SDK 使用示例

本目录包含了MYT SDK Python包的使用示例，帮助您快速了解如何在项目中集成和使用MYT SDK。

## 示例文件

### `sdk_usage.py`

完整的MYT SDK使用示例，包含以下功能演示：

- **基础使用**: 检查SDK状态、初始化SDK
- **自定义缓存目录**: 使用指定的缓存目录
- **强制重新安装**: 强制重新下载SDK
- **仅下载模式**: 下载SDK但不启动
- **错误处理**: 演示各种错误情况的处理

## 运行示例

### 方法1: 直接运行脚本

```bash
# 进入示例目录
cd examples

# 运行示例
python sdk_usage.py
```

### 方法2: 安装包后运行

```bash
# 安装MYT SDK包
pip install -e .

# 运行示例
python examples/sdk_usage.py
```

### 方法3: 使用命令行工具

```bash
# 安装包后，可以直接使用命令行工具
myt-sdk init
myt-sdk status
myt-sdk --help
```

## 示例输出

运行示例时，您将看到类似以下的输出：

```
MYT SDK Python包使用示例
==================================================

=== MYT SDK 基础使用示例 ===

1. 检查SDK状态...
   SDK已安装: False
   SDK正在运行: False
   缓存目录: C:\Users\YourName\AppData\Local\MYT\Cache
   SDK路径: C:\Users\YourName\AppData\Local\MYT\Cache\myt_sdk\myt_sdk.exe

2. 初始化SDK...
   正在下载MYT SDK...
   下载完成，正在解压...
   正在启动SDK...
   初始化结果: started
   消息: SDK已成功启动
   进程ID: 12345

3. 再次检查SDK状态...
   SDK已安装: True
   SDK正在运行: True
```

## 代码示例

### 基本用法

```python
from py_myt import MYTSDKManager

# 创建SDK管理器
sdk_manager = MYTSDKManager()

# 检查状态
status = sdk_manager.get_status()
print(f"SDK已安装: {status['installed']}")
print(f"SDK正在运行: {status['running']}")

# 初始化SDK
result = sdk_manager.init()
print(f"初始化结果: {result['status']}")
```

### 高级用法

```python
from py_myt import MYTSDKManager
from py_myt.exceptions import MYTSDKError

try:
    # 使用自定义缓存目录
    sdk_manager = MYTSDKManager(cache_dir="/path/to/cache")
    
    # 强制重新下载
    result = sdk_manager.init(force=True)
    
    # 仅下载不启动
    result = sdk_manager.init(start_sdk=False)
    
except MYTSDKError as e:
    print(f"SDK错误: {e}")
```

## 命令行使用

### 基本命令

```bash
# 初始化SDK（下载并启动）
myt-sdk init

# 查看SDK状态
myt-sdk status

# 查看帮助
myt-sdk --help
```

### 高级选项

```bash
# 强制重新下载
myt-sdk init --force

# 仅下载不启动
myt-sdk init --no-start

# 使用自定义缓存目录
myt-sdk init --cache-dir /path/to/cache

# 启用详细日志
myt-sdk init --verbose

# 保存日志到文件
myt-sdk init --log-file myt_sdk.log
```

## 故障排除

### 常见问题

1. **下载失败**
   - 检查网络连接
   - 确认防火墙设置
   - 尝试使用代理

2. **权限错误**
   - 确保对缓存目录有写权限
   - 在Windows上可能需要管理员权限

3. **进程启动失败**
   - 检查Windows版本兼容性
   - 确认没有杀毒软件阻止
   - 查看详细日志信息

### 调试技巧

```bash
# 启用详细日志
myt-sdk init --verbose --log-file debug.log

# 查看日志文件
type debug.log  # Windows
cat debug.log   # Linux/Mac
```

## 集成到项目

在您的Python项目中集成MYT SDK：

```python
# requirements.txt
myt-sdk>=1.0.0

# your_project.py
from py_myt import MYTSDKManager

def setup_myt_sdk():
    """在项目启动时初始化MYT SDK"""
    sdk_manager = MYTSDKManager()
    
    # 确保SDK已安装和运行
    if not sdk_manager.is_sdk_running():
        result = sdk_manager.init()
        if result['status'] not in ['started', 'already_running']:
            raise RuntimeError(f"SDK初始化失败: {result['message']}")
    
    return sdk_manager

# 在应用启动时调用
sdk_manager = setup_myt_sdk()
```

## 更多信息

- 查看项目README: `../README.md`
- 查看更新日志: `../CHANGELOG.md`
- 查看源代码: `../py_myt/`