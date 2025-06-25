#!/usr/bin/env python3
"""
AdsPower Tool Pro - Software Installer
第一步：安装所有必需的软件
"""

import subprocess
import sys
import os
import urllib.request
import platform

def print_header():
    print("=" * 60)
    print("  AdsPower Tool Pro - Python环境安装器")
    print("  第一步：安装Python环境")
    print("=" * 60)
    print()
    print("说明：此步骤只安装Python环境，AdsPower客户端请自行安装")
    print()

def check_system():
    print("[1/3] 检查系统环境...")
    system = platform.system()
    architecture = platform.architecture()[0]

    print(f"操作系统: {system}")
    print(f"架构: {architecture}")

    if system != "Windows":
        print("❌ 此工具仅支持Windows系统")
        return False

    print("✓ 系统环境检查通过")
    return True

def check_python():
    print("\n[2/3] 检查Python安装状态...")

    try:
        version = sys.version_info
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} 已安装")

        if version.major < 3 or (version.major == 3 and version.minor < 7):
            print("⚠ 警告: 建议使用Python 3.7+")
            return False

        # 检查pip
        try:
            import pip
            print("✓ pip 已安装")
        except ImportError:
            print("⚠ pip 未安装，尝试安装...")
            subprocess.run([sys.executable, "-m", "ensurepip", "--upgrade"])

        return True

    except Exception as e:
        print(f"❌ Python检查失败: {e}")
        return False

def install_python():
    print("\n正在准备安装Python...")
    print("由于权限和兼容性考虑，请手动安装Python：")
    print()
    print("📋 Python安装步骤：")
    print("1. 访问: https://www.python.org/downloads/")
    print("2. 下载Python 3.11或更高版本")
    print("3. 运行安装程序")
    print("4. ⚠ 重要：勾选 'Add Python to PATH'")
    print("5. 选择 'Install for all users'（推荐）")
    print("6. 完成安装后重启电脑")
    print("7. 重新运行此脚本验证安装")
    print()
    
    choice = input("是否已完成Python安装？(y/n): ").lower()
    if choice == 'y':
        print("请重启电脑后重新运行此脚本进行验证")
        return True
    return False

def download_python():
    print("\n正在尝试下载Python安装包...")

    try:
        # Python 3.11.9 下载链接
        python_url = "https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe"
        installer_path = "python-3.11.9-amd64.exe"

        print(f"下载地址: {python_url}")
        print("正在下载，请稍候...")

        urllib.request.urlretrieve(python_url, installer_path)

        if os.path.exists(installer_path):
            print("✓ Python安装包下载成功")
            return installer_path
        else:
            print("❌ 下载失败")
            return None

    except Exception as e:
        print(f"❌ 下载失败: {e}")
        return None

def install_python_auto():
    print("\n尝试自动安装Python...")

    installer_path = download_python()
    if not installer_path:
        return False

    try:
        print("正在安装Python...")
        print("安装参数: /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 Include_pip=1")

        # 静默安装Python
        result = subprocess.run([
            installer_path,
            "/quiet",
            "InstallAllUsers=1",
            "PrependPath=1",
            "Include_test=0",
            "Include_pip=1"
        ], timeout=300)

        # 清理安装包
        if os.path.exists(installer_path):
            os.remove(installer_path)

        if result.returncode == 0:
            print("✓ Python安装完成")
            print("⚠ 请重启电脑后重新运行此脚本验证安装")
            return True
        else:
            print("❌ Python安装失败")
            return False

    except Exception as e:
        print(f"❌ 安装过程出错: {e}")
        # 清理安装包
        if os.path.exists(installer_path):
            os.remove(installer_path)
        return False

def verify_installation():
    print("\n[3/3] 验证Python安装...")

    # 验证Python
    try:
        result = subprocess.run([sys.executable, "--version"],
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Python验证成功: {result.stdout.strip()}")
        else:
            print("❌ Python验证失败")
            return False
    except Exception as e:
        print(f"❌ Python验证失败: {e}")
        return False

    # 验证pip
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "--version"],
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ pip验证成功")
        else:
            print("❌ pip验证失败")
            return False
    except Exception as e:
        print(f"❌ pip验证失败: {e}")
        return False

    print("✓ Python环境验证通过")
    return True

def main():
    print_header()

    # 检查系统
    if not check_system():
        input("按Enter键退出...")
        return

    # 检查Python
    python_ok = check_python()
    if not python_ok:
        print("\nPython未安装或版本过低")
        print("选择安装方式：")
        print("1. 自动下载安装（推荐）")
        print("2. 手动安装")

        choice = input("请选择 (1/2): ").strip()

        if choice == "1":
            if install_python_auto():
                print("\n✅ Python安装完成！")
                print("⚠ 请重启电脑后重新运行此脚本验证安装")
                input("按Enter键退出...")
                return
            else:
                print("\n❌ 自动安装失败，请选择手动安装")
                choice = "2"

        if choice == "2":
            install_python()
            input("按Enter键退出...")
            return

    # 验证安装
    if not verify_installation():
        print("\nPython环境验证失败，请检查安装")
        input("按Enter键退出...")
        return

    print("\n" + "=" * 60)
    print("  第一步完成：Python环境已就绪！")
    print("=" * 60)
    print()
    print("✅ Python环境状态：")
    print("   - Python 3.7+ ✓")
    print("   - pip (包管理器) ✓")
    print()
    print("📋 下一步：")
    print("   1. 运行 '安装依赖项.bat' 安装Python依赖包")
    print("   2. 或者双击 'install_dependencies.py'")
    print()
    print("📝 关于AdsPower：")
    print("   - AdsPower客户端请自行下载安装")
    print("   - 启动AdsPower并启用API功能")
    print("   - API地址: http://local.adspower.com:50325")
    print()

    input("按Enter键退出...")

if __name__ == "__main__":
    main()
