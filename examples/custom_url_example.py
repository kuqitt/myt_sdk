#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自定义下载地址示例

演示如何使用自定义下载地址来初始化和管理MYT SDK
"""

import logging
from py_myt import MYTSDKManager

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """主函数"""
    # 创建SDK管理器
    sdk_manager = MYTSDKManager()
    
    logger.info("=== MYT SDK 自定义下载地址示例 ===")
    
    # 示例1: 使用自定义下载地址初始化SDK
    logger.info("\n1. 使用自定义下载地址初始化SDK")
    custom_url = "http://example.com/myt_sdk_2.0.15.zip"
    
    try:
        # 使用自定义下载地址初始化（这里只是演示，实际URL可能不存在）
        # result = sdk_manager.init(download_url=custom_url)
        # logger.info(f"初始化结果: {result}")
        
        # 由于示例URL不存在，我们只演示配置更新
        logger.info(f"原始版本: {sdk_manager.SDK_VERSION}")
        logger.info(f"原始下载地址: {sdk_manager.SDK_DOWNLOAD_URL}")
        
        # 更新SDK配置
        sdk_manager._update_sdk_config_from_url(custom_url)
        
        logger.info(f"更新后版本: {sdk_manager.SDK_VERSION}")
        logger.info(f"更新后下载地址: {sdk_manager.SDK_DOWNLOAD_URL}")
        
    except Exception as e:
        logger.error(f"初始化失败: {e}")
    
    # 示例2: 检查SDK状态
    logger.info("\n2. 检查SDK状态")
    status = sdk_manager.get_status()
    logger.info(f"SDK状态: {status}")
    
    # 示例3: 演示停止SDK功能
    logger.info("\n3. 演示停止SDK功能")
    try:
        # 尝试停止SDK（如果正在运行）
        stop_result = sdk_manager.stop_sdk()
        logger.info(f"停止结果: {stop_result}")
        
        # 演示强制停止
        force_stop_result = sdk_manager.stop_sdk(force=True)
        logger.info(f"强制停止结果: {force_stop_result}")
        
    except Exception as e:
        logger.error(f"停止SDK时出错: {e}")
    
    # 示例4: 演示版本检测功能
    logger.info("\n4. 演示版本检测功能")
    test_urls = [
        "http://example.com/myt_sdk_1.2.3.zip",
        "http://example.com/myt_sdk_v2.0.0.zip",
        "http://example.com/custom_sdk.zip"
    ]
    
    for url in test_urls:
        original_version = sdk_manager.SDK_VERSION
        sdk_manager._update_sdk_config_from_url(url)
        logger.info(f"URL: {url} -> 检测到版本: {sdk_manager.SDK_VERSION}")
        # 恢复原始版本用于下次测试
        sdk_manager.SDK_VERSION = original_version

if __name__ == "__main__":
    main()