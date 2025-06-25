@echo off
chcp 65001 >nul
title AdsPower工具专业版

echo.
echo ========================================
echo    AdsPower工具专业版 启动中...
echo ========================================
echo.

:: 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python 3.7+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: 检查依赖是否安装
echo [检查] 正在检查依赖包...
python -c "import PyQt5" >nul 2>&1
if errorlevel 1 (
    echo [警告] PyQt5未安装，正在自动安装依赖...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [错误] 依赖安装失败，请手动运行: pip install -r requirements.txt
        pause
        exit /b 1
    )
)

echo [启动] 正在启动AdsPower工具专业版...
echo.

:: 启动主程序
python main.py

:: 如果程序异常退出，显示错误信息
if errorlevel 1 (
    echo.
    echo [错误] 程序异常退出，错误代码: %errorlevel%
    echo 请检查错误信息或联系技术支持
)

pause
