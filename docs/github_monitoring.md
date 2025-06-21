# GitHub仓库监控指南

本指南详细介绍如何使用MYT SDK的GitHub监控功能来实时跟踪仓库的访问信息和统计数据。

## 概述

GitHub监控功能允许您：
- 实时获取仓库统计信息
- 监控访问流量和下载量
- 跟踪用户行为和互动
- 生成详细的分析报告

## 快速开始

### 基本统计信息获取

```python
from py_myt.github_monitor import GitHubMonitor

# 创建监控实例
monitor = GitHubMonitor('kuqitt', 'myt_sdk')

# 获取基本统计信息
stats = monitor.get_basic_stats()
print(f"Stars: {stats['stars']}")
print(f"Forks: {stats['forks']}")
print(f"Watchers: {stats['watchers']}")
```

### 实时监控

```python
# 启动实时监控（每小时更新一次）
monitor.start_monitoring(interval=3600)

# 自定义监控间隔（每30分钟）
monitor.start_monitoring(interval=1800)
```

## 详细功能

### 1. 访问统计

#### 获取访问数据

```python
# 获取过去14天的访问统计
traffic_data = monitor.get_traffic_stats()
print(f"总访问量: {traffic_data['count']}")
print(f"独立访客: {traffic_data['uniques']}")

# 获取详细的每日访问数据
daily_views = traffic_data['views']
for day in daily_views:
    print(f"{day['timestamp']}: {day['count']} 次访问, {day['uniques']} 独立访客")
```

#### 克隆统计

```python
# 获取克隆统计信息
clone_data = monitor.get_clone_stats()
print(f"总克隆数: {clone_data['count']}")
print(f"独立克隆者: {clone_data['uniques']}")
```

### 2. 下载监控

#### Release下载统计

```python
# 获取所有Release的下载统计
releases = monitor.get_release_downloads()
for release in releases:
    print(f"版本 {release['tag_name']}: {release['download_count']} 次下载")
    for asset in release['assets']:
        print(f"  - {asset['name']}: {asset['download_count']} 次")
```

#### PyPI下载统计

```python
# 获取PyPI包的下载统计
pypi_stats = monitor.get_pypi_downloads('myt-sdk')
print(f"PyPI总下载量: {pypi_stats['total']}")
print(f"最近30天: {pypi_stats['recent']}")
```

### 3. 用户行为分析

#### 引用来源分析

```python
# 获取流量来源
referrers = monitor.get_referrers()
for referrer in referrers:
    print(f"{referrer['referrer']}: {referrer['count']} 次访问")
```

#### 热门内容分析

```python
# 获取最受欢迎的文件/页面
popular_content = monitor.get_popular_content()
for content in popular_content:
    print(f"{content['path']}: {content['count']} 次访问")
```

### 4. 实时通知

#### 设置阈值通知

```python
# 设置Star数量阈值通知
monitor.set_star_threshold(100, callback=lambda count: print(f"🎉 达到 {count} 个Star!"))

# 设置下载量阈值通知
monitor.set_download_threshold(1000, callback=lambda count: print(f"📦 下载量达到 {count}!"))
```

#### 邮件通知

```python
# 配置邮件通知
monitor.configure_email_notifications(
    smtp_server='smtp.gmail.com',
    smtp_port=587,
    username='your_email@gmail.com',
    password='your_password',
    recipients=['admin@example.com']
)

# 启用每日报告
monitor.enable_daily_reports()
```

### 5. 数据导出和分析

#### 导出统计数据

```python
# 导出为CSV格式
monitor.export_stats_csv('github_stats.csv')

# 导出为JSON格式
monitor.export_stats_json('github_stats.json')

# 导出为Excel格式
monitor.export_stats_excel('github_stats.xlsx')
```

#### 生成分析报告

```python
# 生成HTML报告
monitor.generate_html_report('report.html')

# 生成PDF报告
monitor.generate_pdf_report('report.pdf')
```

### 6. 高级配置

#### 自定义API令牌

```python
# 使用GitHub Personal Access Token提高API限制
monitor = GitHubMonitor(
    'kuqitt', 
    'myt_sdk',
    token='your_github_token'
)
```

#### 缓存配置

```python
# 配置缓存以减少API调用
monitor.configure_cache(
    cache_dir='./cache',
    cache_duration=300  # 5分钟缓存
)
```

#### 代理设置

```python
# 配置代理服务器
monitor.configure_proxy(
    http_proxy='http://proxy.example.com:8080',
    https_proxy='https://proxy.example.com:8080'
)
```

## 监控面板

### Web界面

```python
# 启动Web监控面板
from py_myt.github_monitor.dashboard import start_dashboard

start_dashboard(
    repo_owner='kuqitt',
    repo_name='myt_sdk',
    port=8080
)
```

访问 `http://localhost:8080` 查看实时监控面板。

### 命令行界面

```bash
# 查看实时统计
myt-sdk github-stats kuqitt/myt_sdk

# 启动监控
myt-sdk github-monitor kuqitt/myt_sdk --interval 3600

# 生成报告
myt-sdk github-report kuqitt/myt_sdk --format html --output report.html
```

## 最佳实践

### 1. API限制管理

- 使用GitHub Personal Access Token
- 合理设置监控间隔
- 启用缓存机制
- 监控API使用量

### 2. 数据存储

- 定期备份监控数据
- 使用数据库存储历史数据
- 实施数据清理策略

### 3. 性能优化

- 异步处理大量数据
- 使用连接池
- 实施重试机制
- 监控内存使用

### 4. 安全考虑

- 安全存储API令牌
- 使用环境变量
- 限制访问权限
- 定期轮换令牌

## 故障排除

### 常见问题

1. **API限制超出**
   ```python
   # 检查API限制状态
   rate_limit = monitor.get_rate_limit()
   print(f"剩余请求: {rate_limit['remaining']}/{rate_limit['limit']}")
   ```

2. **网络连接问题**
   ```python
   # 测试连接
   if monitor.test_connection():
       print("连接正常")
   else:
       print("连接失败")
   ```

3. **数据不一致**
   ```python
   # 清除缓存并重新获取
   monitor.clear_cache()
   fresh_data = monitor.get_basic_stats(force_refresh=True)
   ```

### 日志配置

```python
import logging

# 启用详细日志
logging.basicConfig(level=logging.DEBUG)
monitor.enable_debug_logging()
```

## 示例项目

查看 `examples/github_monitoring/` 目录中的完整示例项目，包括：

- 基本监控脚本
- Web面板实现
- 自动化报告生成
- 通知系统集成

## 支持和反馈

如果您在使用GitHub监控功能时遇到问题，请：

1. 查看[常见问题解答](../FAQ.md)
2. 提交[Issue](https://github.com/kuqitt/myt_sdk/issues)
3. 参与[讨论](https://github.com/kuqitt/myt_sdk/discussions)

---

更多信息请参考：
- [GitHub API文档](https://docs.github.com/en/rest)
- [PyPI API文档](https://warehouse.pypa.io/api-reference/)
- [MYT SDK完整文档](../README.md)