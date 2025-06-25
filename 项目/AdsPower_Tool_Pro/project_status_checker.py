#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
项目状态检查器
全面检查项目的UI设计、核心功能、代码质量等
"""

import os
import sys
import json
import ast
import re
from typing import Dict, List, Tuple

class ProjectStatusChecker:
    """项目状态检查器"""
    
    def __init__(self):
        self.issues = {
            "ui_issues": [],
            "functionality_issues": [],
            "code_quality_issues": [],
            "configuration_issues": [],
            "dependency_issues": []
        }
        
        self.fixes_applied = []
        
    def check_ui_design(self) -> List[Dict]:
        """检查UI设计问题"""
        ui_issues = []
        
        # 检查样式管理器导入问题
        debug_dialog_path = "debug_dialog.py"
        if os.path.exists(debug_dialog_path):
            with open(debug_dialog_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if "from ios26_style_manager import" in content:
                    ui_issues.append({
                        "type": "样式导入错误",
                        "file": debug_dialog_path,
                        "description": "debug_dialog.py中错误导入ios26_style_manager",
                        "severity": "中等",
                        "fixed": "from adspower_style_manager import" in content
                    })
        
        # 检查表格列宽设置
        main_py_path = "main.py"
        if os.path.exists(main_py_path):
            with open(main_py_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if "setColumnWidth" in content:
                    # 检查是否有响应式设计
                    if "响应式设计" in content:
                        self.fixes_applied.append("表格列宽响应式设计已应用")
                    else:
                        ui_issues.append({
                            "type": "表格布局问题",
                            "file": main_py_path,
                            "description": "表格列宽设置不够响应式",
                            "severity": "低",
                            "fixed": False
                        })
        
        # 检查任务流程对话框尺寸
        task_flow_path = "task_flow_dialog.py"
        if os.path.exists(task_flow_path):
            with open(task_flow_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if "setFixedSize(1200, 800)" in content:
                    ui_issues.append({
                        "type": "对话框尺寸固定",
                        "file": task_flow_path,
                        "description": "任务流程对话框尺寸固定，不适应不同屏幕",
                        "severity": "中等",
                        "fixed": "响应式设计" in content
                    })
        
        self.issues["ui_issues"] = ui_issues
        return ui_issues
    
    def check_core_functionality(self) -> List[Dict]:
        """检查核心功能实现"""
        func_issues = []
        
        # 检查RPA模块可用性
        try:
            import adspower_api
            import rpa_engine
            self.fixes_applied.append("RPA模块可正常导入")
        except ImportError as e:
            func_issues.append({
                "type": "RPA模块缺失",
                "description": f"无法导入RPA相关模块: {e}",
                "severity": "高",
                "fixed": False
            })
        
        # 检查API客户端
        api_path = "adspower_api.py"
        if os.path.exists(api_path):
            with open(api_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if "class AdsPowerAPIClient" in content:
                    self.fixes_applied.append("API客户端类存在")
                else:
                    func_issues.append({
                        "type": "API客户端问题",
                        "file": api_path,
                        "description": "API客户端类定义不完整",
                        "severity": "高",
                        "fixed": False
                    })
        
        # 检查任务流程管理
        if os.path.exists("task_flow_dialog.py"):
            self.fixes_applied.append("任务流程对话框存在")
        else:
            func_issues.append({
                "type": "任务流程缺失",
                "description": "任务流程管理模块不存在",
                "severity": "高",
                "fixed": False
            })
        
        self.issues["functionality_issues"] = func_issues
        return func_issues
    
    def check_code_quality(self) -> List[Dict]:
        """检查代码质量"""
        quality_issues = []
        
        # 检查启动脚本
        startup_script = "启动.bat"
        if os.path.exists(startup_script):
            with open(startup_script, 'r', encoding='utf-8') as f:
                content = f.read()
                if len(content.strip().split('\n')) < 10:
                    quality_issues.append({
                        "type": "启动脚本简陋",
                        "file": startup_script,
                        "description": "启动脚本过于简单，缺少错误检查",
                        "severity": "中等",
                        "fixed": "检查Python环境" in content
                    })
        
        # 检查错误处理
        if os.path.exists("error_handler.py"):
            self.fixes_applied.append("错误处理模块已创建")
        else:
            quality_issues.append({
                "type": "错误处理缺失",
                "description": "缺少统一的错误处理机制",
                "severity": "中等",
                "fixed": False
            })
        
        # 检查日志记录
        main_py_path = "main.py"
        if os.path.exists(main_py_path):
            with open(main_py_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if "log_info" in content or "logging" in content:
                    self.fixes_applied.append("日志记录功能已集成")
                else:
                    quality_issues.append({
                        "type": "日志记录缺失",
                        "file": main_py_path,
                        "description": "缺少日志记录功能",
                        "severity": "低",
                        "fixed": False
                    })
        
        self.issues["code_quality_issues"] = quality_issues
        return quality_issues
    
    def check_configuration(self) -> List[Dict]:
        """检查配置问题"""
        config_issues = []
        
        # 检查配置文件
        config_path = "config.json"
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # 检查API密钥是否硬编码
                api_key = config.get("api_key", "")
                if api_key and len(api_key) > 10:
                    config_issues.append({
                        "type": "API密钥硬编码",
                        "file": config_path,
                        "description": "配置文件中硬编码了API密钥",
                        "severity": "高",
                        "fixed": api_key == ""
                    })
                
                # 检查UI设置
                if "ui_settings" in config:
                    self.fixes_applied.append("UI设置配置已添加")
                else:
                    config_issues.append({
                        "type": "UI配置缺失",
                        "file": config_path,
                        "description": "缺少UI相关配置",
                        "severity": "低",
                        "fixed": False
                    })
                    
            except json.JSONDecodeError:
                config_issues.append({
                    "type": "配置文件格式错误",
                    "file": config_path,
                    "description": "配置文件JSON格式错误",
                    "severity": "高",
                    "fixed": False
                })
        
        self.issues["configuration_issues"] = config_issues
        return config_issues
    
    def check_dependencies(self) -> List[Dict]:
        """检查依赖问题"""
        dep_issues = []
        
        # 检查requirements.txt
        req_path = "requirements.txt"
        if os.path.exists(req_path):
            with open(req_path, 'r', encoding='utf-8') as f:
                requirements = f.read()
                
            required_packages = ["PyQt5", "requests", "selenium", "beautifulsoup4", "lxml", "openpyxl"]
            missing_packages = []
            
            for package in required_packages:
                if package.lower() not in requirements.lower():
                    missing_packages.append(package)
            
            if missing_packages:
                dep_issues.append({
                    "type": "依赖包缺失",
                    "file": req_path,
                    "description": f"requirements.txt中缺少: {', '.join(missing_packages)}",
                    "severity": "高",
                    "fixed": False
                })
        else:
            dep_issues.append({
                "type": "依赖文件缺失",
                "description": "requirements.txt文件不存在",
                "severity": "高",
                "fixed": False
            })
        
        # 检查环境检查器
        if os.path.exists("environment_checker.py"):
            self.fixes_applied.append("环境检查器已创建")
        else:
            dep_issues.append({
                "type": "环境检查缺失",
                "description": "缺少环境检查工具",
                "severity": "中等",
                "fixed": False
            })
        
        self.issues["dependency_issues"] = dep_issues
        return dep_issues
    
    def generate_report(self) -> str:
        """生成检查报告"""
        report = []
        report.append("=" * 80)
        report.append("AdsPower工具专业版 - 项目状态检查报告")
        report.append("=" * 80)
        report.append("")
        
        # 统计信息
        total_issues = sum(len(issues) for issues in self.issues.values())
        fixed_issues = sum(1 for category in self.issues.values() 
                          for issue in category if issue.get("fixed", False))
        
        report.append(f"📊 检查统计:")
        report.append(f"   总问题数: {total_issues}")
        report.append(f"   已修复: {fixed_issues}")
        report.append(f"   待修复: {total_issues - fixed_issues}")
        report.append(f"   已应用修复: {len(self.fixes_applied)}")
        report.append("")
        
        # 各类问题详情
        categories = {
            "ui_issues": "🎨 UI设计问题",
            "functionality_issues": "⚙️ 核心功能问题", 
            "code_quality_issues": "📝 代码质量问题",
            "configuration_issues": "⚙️ 配置问题",
            "dependency_issues": "📦 依赖问题"
        }
        
        for category, title in categories.items():
            issues = self.issues[category]
            if issues:
                report.append(f"{title} ({len(issues)}个):")
                for i, issue in enumerate(issues, 1):
                    status = "✅ 已修复" if issue.get("fixed", False) else "❌ 待修复"
                    severity = issue.get("severity", "未知")
                    report.append(f"   {i}. [{severity}] {issue['description']} - {status}")
                    if "file" in issue:
                        report.append(f"      文件: {issue['file']}")
                report.append("")
        
        # 已应用的修复
        if self.fixes_applied:
            report.append("✅ 已应用的修复:")
            for i, fix in enumerate(self.fixes_applied, 1):
                report.append(f"   {i}. {fix}")
            report.append("")
        
        # 建议
        report.append("💡 修复建议:")
        if total_issues - fixed_issues > 0:
            report.append("   1. 运行 '安装依赖.bat' 确保所有依赖已安装")
            report.append("   2. 检查配置文件中的API密钥设置")
            report.append("   3. 测试UI界面的响应式设计")
            report.append("   4. 验证RPA功能的完整性")
        else:
            report.append("   🎉 所有已知问题都已修复！")
        
        report.append("")
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def run_full_check(self) -> Dict:
        """运行完整检查"""
        print("🔍 开始项目状态检查...")
        
        self.check_ui_design()
        self.check_core_functionality()
        self.check_code_quality()
        self.check_configuration()
        self.check_dependencies()
        
        report = self.generate_report()
        print(report)
        
        # 保存报告
        try:
            with open("project_status_report.txt", 'w', encoding='utf-8') as f:
                f.write(report)
            print("📄 检查报告已保存到: project_status_report.txt")
        except Exception as e:
            print(f"⚠️ 保存报告失败: {e}")
        
        return {
            "issues": self.issues,
            "fixes_applied": self.fixes_applied,
            "report": report
        }

def main():
    """主函数"""
    checker = ProjectStatusChecker()
    results = checker.run_full_check()
    
    total_issues = sum(len(issues) for issues in results["issues"].values())
    fixed_issues = sum(1 for category in results["issues"].values() 
                      for issue in category if issue.get("fixed", False))
    
    if total_issues == fixed_issues:
        print("\n🎉 项目状态良好，所有已知问题都已修复！")
        return True
    else:
        print(f"\n⚠️ 项目还有 {total_issues - fixed_issues} 个问题需要修复")
        return False

if __name__ == "__main__":
    main()
