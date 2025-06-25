@echo off
chcp 65001 >nul
title AdsPower工具专业版 - 依赖安装

echo.
echo ========================================
echo    AdsPower工具专业版 - 依赖安装
echo ========================================
echo.

:: 检查Python是否安装
echo [检查] 正在检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python 3.7+
    echo 下载地址: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

:: 显示Python版本
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [信息] 检测到Python版本: %PYTHON_VERSION%

:: 运行Python安装脚本
echo [安装] 正在运行依赖安装脚本...
python install_dependencies.py

:: 检查安装结果
if errorlevel 1 (
    echo.
    echo [错误] 依赖安装失败，尝试备用方案...
    echo [备用] 使用pip直接安装...

    if exist "requirements.txt" (
        pip install -r requirements.txt
        if errorlevel 1 (
            echo [错误] 备用安装也失败，请手动安装依赖
        ) else (
            echo [成功] 备用安装完成
        )
    ) else (
        echo [错误] 找不到requirements.txt文件
    )
)

:: 运行环境检查
echo.
echo [验证] 正在验证安装结果...
if exist "environment_checker.py" (
    python environment_checker.py
) else (
    echo [跳过] 环境检查器不存在
)

echo.
echo [完成] 安装过程结束
echo 如果安装成功，现在可以运行"启动.bat"启动程序
echo.
pause
