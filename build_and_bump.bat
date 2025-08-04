@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo ========================================
echo MYT SDK 一键打包脚本
echo ========================================
echo.

REM 检查是否在项目根目录
if not exist "setup.py" (
    echo 错误: 请在项目根目录运行此脚本
    pause
    exit /b 1
)

REM 检查并激活虚拟环境
if not exist ".venv" (
    echo 错误: 虚拟环境不存在，请先创建虚拟环境:
    echo python -m venv .venv
    echo .venv\Scripts\activate
    echo pip install -e ".[dev]"
    pause
    exit /b 1
)

echo 激活虚拟环境...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo 错误: 激活虚拟环境失败
    pause
    exit /b 1
)

REM 运行打包脚本
echo.
echo 运行打包脚本...
python build_and_bump.py
if errorlevel 1 (
    echo 错误: 打包脚本执行失败
    pause
    exit /b 1
)

echo.
echo 打包完成!
pause