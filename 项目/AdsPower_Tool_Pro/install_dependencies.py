#!/usr/bin/env python3
"""
AdsPower Tool Pro - Dependency Installer
第二步：安装所有Python依赖包
"""

import subprocess
import sys
import os
import json

def print_header():
    print("=" * 60)
    print("  AdsPower Tool Pro - 依赖包安装器")
    print("  第二步：安装所有Python依赖包")
    print("=" * 60)
    print()
    print("⚠ 注意：运行此脚本前请确保已完成第一步（软件安装）")
    print()

def check_prerequisites():
    print("[1/5] 检查前置条件...")

    # 检查Python版本
    version = sys.version_info
    print(f"Python版本: {version.major}.{version.minor}.{version.micro}")

    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ 错误: 需要Python 3.7+")
        print("请先运行 'install_software.py' 安装Python")
        return False

    print("✓ Python版本检查通过")

    # 检查pip
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"],
                      check=True, capture_output=True)
        print("✓ pip可用")
    except subprocess.CalledProcessError:
        print("❌ pip不可用")
        return False

    return True

def create_directories():
    print("\n[2/5] Creating project directories...")
    directories = ['data', 'logs', 'exports', 'backups', 'temp']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✓ Created {directory}/")
        else:
            print(f"✓ {directory}/ already exists")

def install_packages():
    print("\n[3/5] Installing Python packages...")
    print("This may take several minutes...")
    
    packages = [
        "PyQt5==5.15.9",
        "requests",
        "selenium", 
        "beautifulsoup4",
        "lxml",
        "openpyxl",
        "pandas",
        "Pillow",
        "pyautogui",
        "webdriver-manager"
    ]
    
    # Upgrade pip first
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip", "--user"], 
                      check=True, capture_output=True)
        print("✓ pip upgraded")
    except subprocess.CalledProcessError:
        print("⚠ pip upgrade failed, continuing...")
    
    # Install packages
    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.run([sys.executable, "-m", "pip", "install", package, "--user"], 
                          check=True, capture_output=True)
            print(f"✓ {package} installed")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install {package}")
            print(f"Error: {e}")

def verify_installation():
    print("\n[4/5] Verifying installation...")
    
    test_imports = [
        ("PyQt5", "PyQt5"),
        ("requests", "requests"),
        ("selenium", "selenium"),
        ("beautifulsoup4", "bs4"),
        ("lxml", "lxml"),
        ("openpyxl", "openpyxl"),
        ("pandas", "pandas"),
        ("Pillow", "PIL"),
        ("pyautogui", "pyautogui"),
        ("webdriver-manager", "webdriver_manager")
    ]
    
    for package_name, import_name in test_imports:
        try:
            __import__(import_name)
            print(f"✓ {package_name}: OK")
        except ImportError:
            print(f"✗ {package_name}: FAILED")

def create_config():
    print("\n[5/5] Creating configuration...")
    
    # Check project files
    required_files = ["main.py", "adspower_api.py"]
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file} found")
        else:
            print(f"⚠ {file} not found!")
    
    # Create config.json if not exists
    if not os.path.exists("config.json"):
        config = {
            "api_url": "http://local.adspower.com:50325",
            "api_key": "",
            "timeout": 30,
            "auto_start": False,
            "max_threads": 5,
            "log_level": "INFO"
        }
        
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print("✓ config.json created")
    else:
        print("✓ config.json already exists")

def main():
    print_header()

    if not check_prerequisites():
        input("Press Enter to exit...")
        return
    
    create_directories()
    install_packages()
    verify_installation()
    create_config()
    
    print("\n" + "=" * 50)
    print("  Installation Complete!")
    print("=" * 50)
    print()
    print("Your system is now ready to run AdsPower Tool Pro!")
    print()
    print("To start the program:")
    print("1. Make sure AdsPower client is running")
    print("2. Double-click 'AdsPower_Tool_Launcher.bat'")
    print("3. Or run: python main.py")
    print()
    print("Important:")
    print("- Ensure AdsPower client is installed and running")
    print("- Check that AdsPower API is enabled")
    print("- Default API: http://local.adspower.com:50325")
    print()
    
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
