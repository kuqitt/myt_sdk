# -*- coding: utf-8 -*-
"""
测试CMD窗口显示功能

这个脚本专门用于测试 show_window=True 参数是否能正确显示CMD窗口。
"""

import logging
import time
from py_myt.sdk_manager import MYTSDKManager

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_show_window():
    """测试显示CMD窗口功能"""
    
    print("=== 测试CMD窗口显示功能 ===")
    print()
    
    # 创建SDK管理器
    sdk_manager = MYTSDKManager()
    
    print("正在启动SDK并显示CMD窗口...")
    print("如果功能正常，您应该能看到一个CMD窗口弹出")
    print()
    
    try:
        # 确保SDK已安装
        if not sdk_manager.is_sdk_installed():
            print("SDK未安装，正在下载...")
            sdk_manager.download_sdk()
            print("SDK下载完成")
        
        # 启动SDK并显示窗口
        print("启动参数: show_window=True")
        process = sdk_manager.start_sdk(show_window=True)
        
        if process:
            print(f"✓ SDK启动成功")
            print(f"✓ 进程ID: {process.pid}")
            print(f"✓ 窗口显示: 是")
            print()
            print("请检查是否有CMD窗口弹出...")
            print("等待10秒后自动停止SDK")
            
            # 等待10秒让用户观察
            for i in range(10, 0, -1):
                print(f"\r倒计时: {i} 秒", end="", flush=True)
                time.sleep(1)
            
            print("\n\n正在停止SDK...")
            sdk_manager.stop_sdk()
            print("✓ SDK已停止")
            
        else:
            print("✗ SDK启动失败")
            
    except Exception as e:
        print(f"✗ 启动过程中出现错误: {e}")
        logger.exception("详细错误信息:")
    
    print()
    print("=== 测试完成 ===")
    print()
    print("说明:")
    print("- 如果看到CMD窗口弹出，说明 show_window=True 功能正常")
    print("- 如果没有看到CMD窗口，可能的原因:")
    print("  1. SDK可执行文件不存在或路径错误")
    print("  2. Windows系统设置阻止了窗口显示")
    print("  3. SDK启动失败")
    print("  4. 功能实现有问题")

if __name__ == "__main__":
    test_show_window()