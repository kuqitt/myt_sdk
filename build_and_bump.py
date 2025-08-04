#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键打包脚本 - 自动增加版本号并构建包

功能:
1. 检查虚拟环境
2. 自动读取当前版本号
3. 版本号+0.0.1
4. 更新setup.py文件
5. 清理旧的构建文件
6. 构建新的包
7. 可选择上传到PyPI
"""

import re
import os
import sys
import subprocess
from pathlib import Path


def check_virtual_env():
    """检查是否在虚拟环境中"""
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("❌ 错误: 请在虚拟环境中运行此脚本")
        print("\n请先激活虚拟环境:")
        if os.name == 'nt':  # Windows
            print("  .venv\\Scripts\\activate")
        else:  # Unix/Linux
            print("  source .venv/bin/activate")
        print("\n然后重新运行脚本")
        sys.exit(1)
    else:
        venv_path = os.environ.get('VIRTUAL_ENV', sys.prefix)
        print(f"✅ 虚拟环境已激活: {venv_path}")


def get_current_version():
    """从setup.py中读取当前版本号"""
    setup_file = Path("setup.py")
    if not setup_file.exists():
        raise FileNotFoundError("setup.py文件不存在")
    
    with open(setup_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 匹配版本号
    version_pattern = r'version\s*=\s*["\']([0-9]+\.[0-9]+\.[0-9]+)["\']'
    match = re.search(version_pattern, content)
    
    if not match:
        raise ValueError("无法在setup.py中找到版本号")
    
    return match.group(1)


def bump_version(version):
    """增加版本号 (patch版本+1)"""
    parts = version.split('.')
    if len(parts) != 3:
        raise ValueError(f"版本号格式错误: {version}")
    
    major, minor, patch = map(int, parts)
    new_patch = patch + 1
    
    return f"{major}.{minor}.{new_patch}"


def update_setup_version(new_version):
    """更新setup.py中的版本号"""
    setup_file = Path("setup.py")
    
    with open(setup_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换版本号
    version_pattern = r'(version\s*=\s*["\'])([0-9]+\.[0-9]+\.[0-9]+)(["\'])'
    new_content = re.sub(version_pattern, f'\\g<1>{new_version}\\g<3>', content)
    
    with open(setup_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ 已更新setup.py中的版本号为: {new_version}")


def run_command(cmd, description):
    """执行命令并显示结果"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description}完成")
        if result.stdout.strip():
            print(f"输出: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description}失败")
        if e.stderr.strip():
            print(f"错误: {e.stderr.strip()}")
        return False


def clean_build_files():
    """清理构建文件"""
    print("\n🧹 清理构建文件...")
    
    # 要清理的目录和文件
    clean_targets = [
        "build",
        "dist", 
        "*.egg-info",
        ".pytest_cache",
        "htmlcov",
        ".coverage"
    ]
    
    for target in clean_targets:
        if os.name == 'nt':  # Windows
            if '*' in target:
                run_command(f'for /d %i in ({target}) do rmdir /s /q "%i" 2>nul', f"清理 {target}")
            else:
                run_command(f'if exist "{target}" rmdir /s /q "{target}"', f"清理 {target}")
        else:  # Unix/Linux
            run_command(f'rm -rf {target}', f"清理 {target}")
    
    print("✅ 构建文件清理完成")


def build_package():
    """构建包"""
    return run_command("python setup.py sdist bdist_wheel", "构建包")


def upload_to_pypi():
    """上传到PyPI"""
    response = input("\n是否要上传到PyPI? (y/N): ").strip().lower()
    if response in ['y', 'yes']:
        return run_command("twine upload dist/*", "上传到PyPI")
    else:
        print("⏭️ 跳过上传到PyPI")
        return True


def main():
    """主函数"""
    print("🚀 MYT SDK 一键打包脚本")
    print("=" * 50)
    
    try:
        # 0. 检查虚拟环境
        check_virtual_env()
        
        # 1. 获取当前版本号
        current_version = get_current_version()
        print(f"📋 当前版本: {current_version}")
        
        # 2. 计算新版本号
        new_version = bump_version(current_version)
        print(f"📈 新版本: {new_version}")
        
        # 3. 确认操作
        response = input(f"\n确认要将版本从 {current_version} 升级到 {new_version} 并构建包吗? (y/N): ").strip().lower()
        if response not in ['y', 'yes']:
            print("❌ 操作已取消")
            return
        
        # 4. 更新版本号
        update_setup_version(new_version)
        
        # 5. 清理构建文件
        clean_build_files()
        
        # 6. 构建包
        if not build_package():
            print("❌ 构建失败，请检查错误信息")
            return
        
        # 7. 可选上传
        upload_to_pypi()
        
        print("\n🎉 打包完成!")
        print(f"📦 新版本 {new_version} 已构建完成")
        print("📁 构建文件位于 dist/ 目录")
        print("\n💡 建议接下来执行:")
        print(f"   git add .")
        print(f"   git commit -m 'Bump version to {new_version}'")
        print(f"   git tag v{new_version}")
        print(f"   git push && git push origin v{new_version}")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()