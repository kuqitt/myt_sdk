#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub仓库监控示例

本示例展示如何使用MYT SDK的GitHub监控功能来实时跟踪仓库统计信息。

功能包括：
- 获取基本仓库统计信息
- 监控访问流量和下载量
- 生成监控报告
- 设置通知阈值
"""

import time
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class GitHubMonitor:
    """GitHub仓库监控器"""
    
    def __init__(self, repo_owner: str, repo_name: str, token: Optional[str] = None):
        """
        初始化GitHub监控器
        
        Args:
            repo_owner: 仓库所有者
            repo_name: 仓库名称
            token: GitHub Personal Access Token（可选，用于提高API限制）
        """
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.token = token
        self.base_url = "https://api.github.com"
        self.repo_url = f"{self.base_url}/repos/{repo_owner}/{repo_name}"
        
        # 设置请求头
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "MYT-SDK-Monitor/1.0"
        }
        
        if token:
            self.headers["Authorization"] = f"token {token}"
    
    def get_basic_stats(self) -> Dict:
        """
        获取仓库基本统计信息
        
        Returns:
            包含基本统计信息的字典
        """
        try:
            response = requests.get(self.repo_url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            
            stats = {
                'name': data['name'],
                'full_name': data['full_name'],
                'description': data.get('description', ''),
                'stars': data['stargazers_count'],
                'forks': data['forks_count'],
                'watchers': data['watchers_count'],
                'open_issues': data['open_issues_count'],
                'size': data['size'],
                'language': data.get('language', 'Unknown'),
                'created_at': data['created_at'],
                'updated_at': data['updated_at'],
                'pushed_at': data['pushed_at'],
                'default_branch': data['default_branch'],
                'license': data.get('license', {}).get('name', 'No License') if data.get('license') else 'No License',
                'topics': data.get('topics', []),
                'archived': data['archived'],
                'disabled': data['disabled'],
                'private': data['private']
            }
            
            return stats
            
        except requests.RequestException as e:
            print(f"获取基本统计信息失败: {e}")
            return {}
    
    def get_traffic_stats(self) -> Dict:
        """
        获取访问流量统计（需要仓库管理员权限）
        
        Returns:
            包含流量统计的字典
        """
        try:
            # 获取页面访问统计
            views_url = f"{self.repo_url}/traffic/views"
            response = requests.get(views_url, headers=self.headers)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 403:
                print("获取流量统计需要仓库管理员权限")
                return {}
            else:
                response.raise_for_status()
                
        except requests.RequestException as e:
            print(f"获取流量统计失败: {e}")
            return {}
    
    def get_clone_stats(self) -> Dict:
        """
        获取克隆统计（需要仓库管理员权限）
        
        Returns:
            包含克隆统计的字典
        """
        try:
            clones_url = f"{self.repo_url}/traffic/clones"
            response = requests.get(clones_url, headers=self.headers)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 403:
                print("获取克隆统计需要仓库管理员权限")
                return {}
            else:
                response.raise_for_status()
                
        except requests.RequestException as e:
            print(f"获取克隆统计失败: {e}")
            return {}
    
    def get_release_downloads(self) -> List[Dict]:
        """
        获取Release下载统计
        
        Returns:
            包含Release下载信息的列表
        """
        try:
            releases_url = f"{self.repo_url}/releases"
            response = requests.get(releases_url, headers=self.headers)
            response.raise_for_status()
            releases = response.json()
            
            download_stats = []
            for release in releases:
                total_downloads = sum(asset['download_count'] for asset in release['assets'])
                
                release_info = {
                    'tag_name': release['tag_name'],
                    'name': release['name'],
                    'published_at': release['published_at'],
                    'total_downloads': total_downloads,
                    'assets': [
                        {
                            'name': asset['name'],
                            'size': asset['size'],
                            'download_count': asset['download_count'],
                            'created_at': asset['created_at']
                        }
                        for asset in release['assets']
                    ]
                }
                download_stats.append(release_info)
            
            return download_stats
            
        except requests.RequestException as e:
            print(f"获取Release下载统计失败: {e}")
            return []
    
    def get_contributors(self) -> List[Dict]:
        """
        获取贡献者信息
        
        Returns:
            包含贡献者信息的列表
        """
        try:
            contributors_url = f"{self.repo_url}/contributors"
            response = requests.get(contributors_url, headers=self.headers)
            response.raise_for_status()
            
            return response.json()
            
        except requests.RequestException as e:
            print(f"获取贡献者信息失败: {e}")
            return []
    
    def get_rate_limit(self) -> Dict:
        """
        获取API限制信息
        
        Returns:
            包含API限制信息的字典
        """
        try:
            rate_limit_url = f"{self.base_url}/rate_limit"
            response = requests.get(rate_limit_url, headers=self.headers)
            response.raise_for_status()
            
            return response.json()
            
        except requests.RequestException as e:
            print(f"获取API限制信息失败: {e}")
            return {}
    
    def generate_report(self) -> Dict:
        """
        生成完整的监控报告
        
        Returns:
            包含完整监控信息的字典
        """
        print("正在生成监控报告...")
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'repository': f"{self.repo_owner}/{self.repo_name}",
            'basic_stats': self.get_basic_stats(),
            'traffic_stats': self.get_traffic_stats(),
            'clone_stats': self.get_clone_stats(),
            'release_downloads': self.get_release_downloads(),
            'contributors': self.get_contributors(),
            'rate_limit': self.get_rate_limit()
        }
        
        return report
    
    def save_report(self, report: Dict, filename: str = None) -> str:
        """
        保存监控报告到文件
        
        Args:
            report: 监控报告数据
            filename: 文件名（可选）
        
        Returns:
            保存的文件路径
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"github_report_{self.repo_owner}_{self.repo_name}_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"报告已保存到: {filename}")
        return filename
    
    def print_summary(self, stats: Dict):
        """
        打印统计信息摘要
        
        Args:
            stats: 统计信息字典
        """
        if not stats:
            print("无法获取统计信息")
            return
        
        print(f"\n📊 {stats['full_name']} 仓库统计")
        print("=" * 50)
        print(f"📝 描述: {stats['description']}")
        print(f"⭐ Stars: {stats['stars']:,}")
        print(f"🍴 Forks: {stats['forks']:,}")
        print(f"👀 Watchers: {stats['watchers']:,}")
        print(f"🐛 Open Issues: {stats['open_issues']:,}")
        print(f"📦 Size: {stats['size']:,} KB")
        print(f"💻 Language: {stats['language']}")
        print(f"📄 License: {stats['license']}")
        print(f"🏷️ Topics: {', '.join(stats['topics']) if stats['topics'] else 'None'}")
        print(f"📅 Created: {stats['created_at'][:10]}")
        print(f"🔄 Last Updated: {stats['updated_at'][:10]}")
        print(f"📤 Last Push: {stats['pushed_at'][:10]}")
        
        if stats['archived']:
            print("🗄️ Status: Archived")
        elif stats['disabled']:
            print("❌ Status: Disabled")
        else:
            print("✅ Status: Active")
    
    def monitor_continuously(self, interval: int = 3600, max_iterations: int = None):
        """
        持续监控仓库统计信息
        
        Args:
            interval: 监控间隔（秒）
            max_iterations: 最大迭代次数（None表示无限循环）
        """
        print(f"开始监控 {self.repo_owner}/{self.repo_name}")
        print(f"监控间隔: {interval} 秒")
        
        iteration = 0
        while max_iterations is None or iteration < max_iterations:
            try:
                print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 第 {iteration + 1} 次检查")
                
                # 获取统计信息
                stats = self.get_basic_stats()
                if stats:
                    self.print_summary(stats)
                    
                    # 保存到历史记录
                    history_entry = {
                        'timestamp': datetime.now().isoformat(),
                        'stats': stats
                    }
                    
                    # 追加到历史文件
                    history_file = f"monitor_history_{self.repo_owner}_{self.repo_name}.jsonl"
                    with open(history_file, 'a', encoding='utf-8') as f:
                        f.write(json.dumps(history_entry, ensure_ascii=False) + '\n')
                
                iteration += 1
                
                if max_iterations is None or iteration < max_iterations:
                    print(f"\n等待 {interval} 秒后进行下次检查...")
                    time.sleep(interval)
                    
            except KeyboardInterrupt:
                print("\n监控已停止")
                break
            except Exception as e:
                print(f"监控过程中发生错误: {e}")
                time.sleep(60)  # 错误后等待1分钟再重试


def main():
    """
    主函数 - 演示GitHub监控功能
    """
    # 配置监控参数
    REPO_OWNER = "kuqitt"
    REPO_NAME = "myt_sdk"
    GITHUB_TOKEN = None  # 可以设置您的GitHub Token
    
    print("🚀 GitHub仓库监控示例")
    print("=" * 50)
    
    # 创建监控器
    monitor = GitHubMonitor(REPO_OWNER, REPO_NAME, GITHUB_TOKEN)
    
    # 1. 获取基本统计信息
    print("\n1. 获取基本统计信息")
    stats = monitor.get_basic_stats()
    monitor.print_summary(stats)
    
    # 2. 检查API限制
    print("\n2. 检查API限制")
    rate_limit = monitor.get_rate_limit()
    if rate_limit:
        core_limit = rate_limit.get('rate', {})
        print(f"API限制: {core_limit.get('remaining', 0)}/{core_limit.get('limit', 0)}")
        reset_time = datetime.fromtimestamp(core_limit.get('reset', 0))
        print(f"重置时间: {reset_time}")
    
    # 3. 获取Release下载统计
    print("\n3. Release下载统计")
    releases = monitor.get_release_downloads()
    if releases:
        print(f"共有 {len(releases)} 个Release")
        for release in releases[:3]:  # 显示前3个
            print(f"  📦 {release['tag_name']}: {release['total_downloads']:,} 次下载")
    else:
        print("暂无Release或无法获取下载统计")
    
    # 4. 获取贡献者信息
    print("\n4. 贡献者信息")
    contributors = monitor.get_contributors()
    if contributors:
        print(f"共有 {len(contributors)} 位贡献者")
        for contributor in contributors[:5]:  # 显示前5位
            print(f"  👤 {contributor['login']}: {contributor['contributions']} 次贡献")
    
    # 5. 生成完整报告
    print("\n5. 生成完整报告")
    report = monitor.generate_report()
    report_file = monitor.save_report(report)
    
    # 6. 询问是否启动持续监控
    print("\n6. 持续监控选项")
    choice = input("是否启动持续监控？(y/N): ").lower().strip()
    
    if choice == 'y':
        try:
            interval = int(input("请输入监控间隔（秒，默认3600）: ") or "3600")
            max_iter = input("请输入最大监控次数（默认无限）: ").strip()
            max_iter = int(max_iter) if max_iter else None
            
            monitor.monitor_continuously(interval, max_iter)
        except ValueError:
            print("输入无效，使用默认设置")
            monitor.monitor_continuously()
    
    print("\n✅ 监控示例完成")


if __name__ == "__main__":
    main()