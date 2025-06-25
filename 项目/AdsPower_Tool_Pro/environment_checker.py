#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
环境检查模块
检查系统环境、依赖包、配置文件等
"""

import sys
import os
import subprocess
import json
from typing import Dict, List, Tuple

class EnvironmentChecker:
    """环境检查器"""
    
    def __init__(self):
        self.required_packages = [
            "PyQt5", "requests", "selenium", "webdriver-manager",
            "beautifulsoup4", "lxml", "openpyxl", "pandas", "Pillow", "pyautogui"
        ]
        
        self.required_files = [
            "main.py", "adspower_api.py", "rpa_engine.py",
            "requirements.txt", "config.json"
        ]
        
        self.required_dirs = ["data", "logs", "exports", "backups"]
        
        self.check_results = {
            "python": {"status": False, "details": ""},
            "packages": {"status": False, "details": [], "missing": []},
            "files": {"status": False, "details": [], "missing": []},
            "directories": {"status": False, "details": [], "missing": []},
            "config": {"status": False, "details": ""},
            "overall": {"status": False, "score": 0}
        }
    
    def check_python_version(self) -> Tuple[bool, str]:
        """检查Python版本"""
        try:
            version = sys.version_info
            version_str = f"{version.major}.{version.minor}.{version.micro}"
            
            if version.major >= 3 and version.minor >= 7:
                self.check_results["python"]["status"] = True
                self.check_results["python"]["details"] = f"Python {version_str} (符合要求)"
                return True, f"Python {version_str}"
            else:
                self.check_results["python"]["details"] = f"Python {version_str} (需要3.7+)"
                return False, f"Python版本过低: {version_str}"
                
        except Exception as e:
            self.check_results["python"]["details"] = f"检查失败: {e}"
            return False, f"Python版本检查失败: {e}"
    
    def check_packages(self) -> Tuple[bool, List[str], List[str]]:
        """检查依赖包"""
        installed = []
        missing = []

        for package in self.required_packages:
            try:
                # 特殊处理需要GUI环境的包
                if package == "pyautogui":
                    # 设置临时DISPLAY环境变量
                    import os
                    original_display = os.environ.get('DISPLAY')
                    if not original_display:
                        os.environ['DISPLAY'] = ':0'

                    try:
                        __import__(package)
                        installed.append(package)
                    finally:
                        # 恢复原始DISPLAY设置
                        if not original_display:
                            os.environ.pop('DISPLAY', None)
                        elif original_display:
                            os.environ['DISPLAY'] = original_display
                else:
                    __import__(package)
                    installed.append(package)
            except ImportError:
                missing.append(package)
            except Exception as e:
                # 对于其他异常（如GUI相关），仍然认为包已安装
                if "DISPLAY" in str(e) or "GUI" in str(e):
                    installed.append(package)
                else:
                    missing.append(package)
        
        self.check_results["packages"]["details"] = installed
        self.check_results["packages"]["missing"] = missing
        self.check_results["packages"]["status"] = len(missing) == 0
        
        return len(missing) == 0, installed, missing
    
    def check_files(self) -> Tuple[bool, List[str], List[str]]:
        """检查必要文件"""
        existing = []
        missing = []
        
        for file_path in self.required_files:
            if os.path.exists(file_path):
                existing.append(file_path)
            else:
                missing.append(file_path)
        
        self.check_results["files"]["details"] = existing
        self.check_results["files"]["missing"] = missing
        self.check_results["files"]["status"] = len(missing) == 0
        
        return len(missing) == 0, existing, missing
    
    def check_directories(self) -> Tuple[bool, List[str], List[str]]:
        """检查必要目录"""
        existing = []
        missing = []
        
        for dir_path in self.required_dirs:
            if os.path.exists(dir_path) and os.path.isdir(dir_path):
                existing.append(dir_path)
            else:
                missing.append(dir_path)
        
        self.check_results["directories"]["details"] = existing
        self.check_results["directories"]["missing"] = missing
        self.check_results["directories"]["status"] = len(missing) == 0
        
        return len(missing) == 0, existing, missing
    
    def check_config(self) -> Tuple[bool, str]:
        """检查配置文件"""
        try:
            if not os.path.exists("config.json"):
                self.check_results["config"]["details"] = "配置文件不存在"
                return False, "配置文件不存在"
            
            with open("config.json", 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            required_keys = ["api_url", "api_key", "timeout"]
            missing_keys = [key for key in required_keys if key not in config]
            
            if missing_keys:
                details = f"缺少配置项: {', '.join(missing_keys)}"
                self.check_results["config"]["details"] = details
                return False, details
            
            # 检查API密钥是否为空
            if not config.get("api_key"):
                details = "API密钥未配置"
                self.check_results["config"]["details"] = details
                return False, details
            
            self.check_results["config"]["status"] = True
            self.check_results["config"]["details"] = "配置文件正常"
            return True, "配置文件正常"
            
        except json.JSONDecodeError as e:
            details = f"配置文件格式错误: {e}"
            self.check_results["config"]["details"] = details
            return False, details
        except Exception as e:
            details = f"配置文件检查失败: {e}"
            self.check_results["config"]["details"] = details
            return False, details
    
    def create_missing_directories(self) -> bool:
        """创建缺失的目录"""
        try:
            for dir_path in self.check_results["directories"]["missing"]:
                os.makedirs(dir_path, exist_ok=True)
                print(f"✅ 已创建目录: {dir_path}")
            return True
        except Exception as e:
            print(f"❌ 创建目录失败: {e}")
            return False
    
    def install_missing_packages(self) -> bool:
        """安装缺失的依赖包"""
        missing = self.check_results["packages"]["missing"]
        if not missing:
            return True
        
        try:
            print(f"正在安装缺失的依赖包: {', '.join(missing)}")
            
            # 使用pip安装
            cmd = [sys.executable, "-m", "pip", "install"] + missing
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print("✅ 依赖包安装成功")
                return True
            else:
                print(f"❌ 依赖包安装失败: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ 依赖包安装超时")
            return False
        except Exception as e:
            print(f"❌ 依赖包安装失败: {e}")
            return False
    
    def run_full_check(self) -> Dict:
        """运行完整检查"""
        print("🔍 开始环境检查...")
        print("=" * 60)
        
        # 检查Python版本
        python_ok, python_info = self.check_python_version()
        print(f"Python版本: {'✅' if python_ok else '❌'} {python_info}")
        
        # 检查依赖包
        packages_ok, installed, missing_packages = self.check_packages()
        print(f"依赖包: {'✅' if packages_ok else '❌'} {len(installed)}/{len(self.required_packages)} 已安装")
        if missing_packages:
            print(f"  缺失: {', '.join(missing_packages)}")
        
        # 检查文件
        files_ok, existing_files, missing_files = self.check_files()
        print(f"必要文件: {'✅' if files_ok else '❌'} {len(existing_files)}/{len(self.required_files)} 存在")
        if missing_files:
            print(f"  缺失: {', '.join(missing_files)}")
        
        # 检查目录
        dirs_ok, existing_dirs, missing_dirs = self.check_directories()
        print(f"必要目录: {'✅' if dirs_ok else '❌'} {len(existing_dirs)}/{len(self.required_dirs)} 存在")
        if missing_dirs:
            print(f"  缺失: {', '.join(missing_dirs)}")
        
        # 检查配置
        config_ok, config_info = self.check_config()
        print(f"配置文件: {'✅' if config_ok else '❌'} {config_info}")
        
        # 计算总体得分
        checks = [python_ok, packages_ok, files_ok, dirs_ok, config_ok]
        score = sum(checks) / len(checks) * 100
        
        self.check_results["overall"]["score"] = score
        self.check_results["overall"]["status"] = score >= 80
        
        print("=" * 60)
        print(f"总体状态: {'✅ 良好' if score >= 80 else '❌ 需要修复'} (得分: {score:.1f}/100)")
        
        return self.check_results
    
    def auto_fix(self) -> bool:
        """自动修复问题"""
        print("\n🔧 开始自动修复...")
        
        success = True
        
        # 创建缺失目录
        if self.check_results["directories"]["missing"]:
            if not self.create_missing_directories():
                success = False
        
        # 安装缺失依赖
        if self.check_results["packages"]["missing"]:
            if not self.install_missing_packages():
                success = False
        
        return success

def main():
    """主函数"""
    checker = EnvironmentChecker()
    results = checker.run_full_check()
    
    if not results["overall"]["status"]:
        print("\n❓ 是否尝试自动修复问题? (y/n): ", end="")
        try:
            choice = input().lower().strip()
            if choice in ['y', 'yes', '是']:
                if checker.auto_fix():
                    print("✅ 自动修复完成，请重新运行检查")
                else:
                    print("❌ 自动修复失败，请手动解决问题")
        except KeyboardInterrupt:
            print("\n用户取消操作")
    
    return results["overall"]["status"]

if __name__ == "__main__":
    main()
