#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
正确使用自定义下载地址的示例

演示如何正确使用新的下载地址功能
"""

import logging
from py_myt import MYTSDKManager

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """主函数"""
    logger.info("=== 正确使用自定义下载地址示例 ===")
    
    # 方法1: 在init()方法中传入download_url参数（推荐）
    logger.info("\n方法1: 使用init()方法的download_url参数")
    myt = MYTSDKManager()
    
    # 显示初始状态
    logger.info(f"初始版本: {myt.SDK_VERSION}")
    logger.info(f"初始下载地址: {myt.SDK_DOWNLOAD_URL}")
    
    # 使用自定义下载地址初始化（这会自动检测版本并更新配置）
    custom_url = "http://d.moyunteng.com/sdk/myt_sdk_1.0.14.30.31.zip"
    
    try:
        # 正确的方式：通过init方法传入download_url
        result = myt.init(download_url=custom_url, start_sdk=False)  # 不启动SDK，只下载
        logger.info(f"初始化结果: {result['status']}")
        
        # 显示更新后的状态
        status = myt.get_status()
        logger.info(f"更新后状态: {status}")
        
    except Exception as e:
        logger.error(f"初始化失败: {e}")
    
    logger.info("\n" + "="*60)
    
    # 方法2: 手动调用_update_sdk_config_from_url方法
    logger.info("\n方法2: 手动更新SDK配置")
    myt2 = MYTSDKManager()
    
    logger.info(f"更新前版本: {myt2.SDK_VERSION}")
    logger.info(f"更新前下载地址: {myt2.SDK_DOWNLOAD_URL}")
    
    # 手动更新配置
    myt2._update_sdk_config_from_url(custom_url)
    
    logger.info(f"更新后版本: {myt2.SDK_VERSION}")
    logger.info(f"更新后下载地址: {myt2.SDK_DOWNLOAD_URL}")
    logger.info(f"更新后SDK目录: {myt2.sdk_dir}")
    
    logger.info("\n" + "="*60)
    
    # 错误示例：直接设置属性（不推荐）
    logger.info("\n错误示例: 直接设置SDK_DOWNLOAD_URL属性")
    myt3 = MYTSDKManager()
    
    # 这种方式不会更新版本和路径！
    myt3.SDK_DOWNLOAD_URL = custom_url
    
    logger.info(f"直接设置后版本: {myt3.SDK_VERSION}")
    logger.info(f"直接设置后下载地址: {myt3.SDK_DOWNLOAD_URL}")
    logger.info(f"直接设置后SDK目录: {myt3.sdk_dir}")
    logger.warning("注意：直接设置属性不会更新版本和路径，这会导致问题！")
    
    # 显示状态对比
    status3 = myt3.get_status()
    logger.info(f"错误方式的状态: {status3}")
    
if __name__ == "__main__":
    main()