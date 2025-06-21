# 更新日志

本项目的所有重要变更都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
并且本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [未发布]

### 新增
- 待添加的API功能
- 更多SDK管理选项

### 变更
- 待优化的下载和启动流程

### 修复
- 待修复的兼容性问题

## [1.0.0] - 2024-01-01

### 重大变更
- 完全重构为MYT SDK管理包
- 移除原有的通用Python包功能
- 专注于MYT SDK的下载、安装和管理

### 新增
- MYT SDK自动下载功能
- SDK进程管理和状态检测
- 智能缓存管理系统
- 完善的错误处理机制
- 命令行工具 (`myt-sdk`)
- SDK状态查询功能
- 强制重新下载选项
- 自定义缓存目录支持

### 技术特性
- Windows平台专门优化
- 基于requests的HTTP下载
- 使用psutil进行进程管理
- 完整的异常处理体系
- 详细的日志记录
- 单元测试覆盖

### 命令行接口
- `myt-sdk init` - 初始化并启动SDK
- `myt-sdk status` - 查看SDK状态
- 支持 `--force`, `--no-start`, `--cache-dir` 等选项

### 版本说明
- 这是MYT SDK管理包的首个正式版本
- 提供完整的SDK生命周期管理
- 适用于需要集成MYT SDK的Python项目