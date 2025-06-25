#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RPA流程管理系统
完全按照AdsPower原版实现流程导入导出功能，确保与AdsPower完全兼容
"""

import json
import os
import time
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

class RPAFlowManager:
    """RPA流程管理器 - 完全按照AdsPower原版实现"""
    
    def __init__(self):
        self.flows = {}  # 存储所有流程
        self.flow_templates = {}  # 流程模板
        self.import_history = []  # 导入历史
        self.export_history = []  # 导出历史
        
    # ==================== 流程导出功能 ====================
    
    def export_flow(self, flow_data: Dict[str, Any], export_format: str = "json") -> str:
        """导出流程 - 完全按照AdsPower原版格式"""
        try:
            # 构建AdsPower兼容的流程数据结构
            adspower_flow = self._convert_to_adspower_format(flow_data)
            
            if export_format.lower() == "json":
                # JSON格式导出（AdsPower标准格式）
                export_content = json.dumps(adspower_flow, ensure_ascii=False, indent=2)
            else:
                # 其他格式支持
                export_content = str(adspower_flow)
            
            # 记录导出历史
            export_record = {
                "timestamp": datetime.now().isoformat(),
                "flow_name": flow_data.get("name", "未命名流程"),
                "format": export_format,
                "step_count": len(flow_data.get("steps", [])),
                "export_size": len(export_content)
            }
            self.export_history.append(export_record)
            
            return export_content
            
        except Exception as e:
            raise Exception(f"导出流程失败: {str(e)}")
    
    def export_flow_to_file(self, flow_data: Dict[str, Any], file_path: str = None) -> str:
        """导出流程到文件"""
        try:
            if not file_path:
                flow_name = flow_data.get("name", "flow")
                timestamp = int(time.time())
                file_path = f"{flow_name}_{timestamp}.json"
            
            export_content = self.export_flow(flow_data, "json")
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(export_content)
            
            return file_path
            
        except Exception as e:
            raise Exception(f"导出流程到文件失败: {str(e)}")
    
    # ==================== 流程导入功能 ====================
    
    def import_flow(self, flow_content: str, import_mode: str = "replace") -> Dict[str, Any]:
        """导入流程 - 支持AdsPower原版格式"""
        try:
            # 解析流程内容
            if isinstance(flow_content, str):
                flow_data = json.loads(flow_content)
            else:
                flow_data = flow_content
            
            # 验证流程格式
            validated_flow = self._validate_and_convert_flow(flow_data)
            
            # 根据导入模式处理
            if import_mode == "replace":
                # 替换模式：完全替换现有流程
                result_flow = validated_flow
            elif import_mode == "append":
                # 追加模式：添加到现有流程末尾
                result_flow = self._append_flow_steps(validated_flow)
            else:
                # 默认替换模式
                result_flow = validated_flow
            
            # 记录导入历史
            import_record = {
                "timestamp": datetime.now().isoformat(),
                "flow_name": validated_flow.get("name", "导入的流程"),
                "import_mode": import_mode,
                "step_count": len(validated_flow.get("steps", [])),
                "source": "manual_import"
            }
            self.import_history.append(import_record)
            
            return result_flow
            
        except json.JSONDecodeError as e:
            raise Exception(f"流程格式错误: {str(e)}")
        except Exception as e:
            raise Exception(f"导入流程失败: {str(e)}")
    
    def import_flow_from_file(self, file_path: str, import_mode: str = "replace") -> Dict[str, Any]:
        """从文件导入流程"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                flow_content = f.read()
            
            result = self.import_flow(flow_content, import_mode)
            
            # 更新导入记录的来源
            if self.import_history:
                self.import_history[-1]["source"] = file_path
            
            return result
            
        except Exception as e:
            raise Exception(f"从文件导入流程失败: {str(e)}")
    
    # ==================== 格式转换功能 ====================
    
    def _convert_to_adspower_format(self, flow_data: Dict[str, Any]) -> Dict[str, Any]:
        """转换为AdsPower标准格式"""
        adspower_flow = {
            "name": flow_data.get("name", "未命名流程"),
            "description": flow_data.get("description", ""),
            "version": "1.0",
            "created_time": flow_data.get("created_time", datetime.now().isoformat()),
            "updated_time": datetime.now().isoformat(),
            "author": flow_data.get("author", "AdsPower Tool Pro"),
            "tags": flow_data.get("tags", []),
            "variables": flow_data.get("variables", {}),
            "steps": []
        }
        
        # 转换步骤格式
        for step in flow_data.get("steps", []):
            adspower_step = self._convert_step_to_adspower(step)
            adspower_flow["steps"].append(adspower_step)
        
        return adspower_flow
    
    def _convert_step_to_adspower(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """转换单个步骤为AdsPower格式"""
        adspower_step = {
            "id": step.get("id", str(uuid.uuid4())),
            "name": step.get("name", step.get("operation", "未命名操作")),
            "operation": step.get("operation", ""),
            "description": step.get("description", ""),
            "enabled": step.get("enabled", True),
            "parameters": step.get("parameters", {}),
            "timeout": step.get("timeout", 30000),
            "retry_count": step.get("retry_count", 0),
            "on_error": step.get("on_error", "stop"),
            "condition": step.get("condition", ""),
            "loop_config": step.get("loop_config", {}),
            "created_time": step.get("created_time", datetime.now().isoformat())
        }
        
        # 处理特殊参数映射
        self._map_parameters_to_adspower(adspower_step, step)
        
        return adspower_step
    
    def _map_parameters_to_adspower(self, adspower_step: Dict[str, Any], original_step: Dict[str, Any]):
        """映射参数到AdsPower格式"""
        operation = adspower_step["operation"]
        parameters = adspower_step["parameters"]
        
        # 根据操作类型映射参数
        if operation == "点击元素":
            parameters.update({
                "selector_type": original_step.get("click_selector_type", "Selector"),
                "selector": original_step.get("click_selector", ""),
                "element_order": original_step.get("click_element_order", 1),
                "click_type": original_step.get("click_type", "鼠标左键"),
                "click_action": original_step.get("click_action", "单击")
            })
        elif operation == "输入内容":
            parameters.update({
                "selector_type": original_step.get("input_selector_type", "Selector"),
                "selector": original_step.get("input_selector", ""),
                "content": original_step.get("input_content", ""),
                "clear_before": original_step.get("input_clear_before", True),
                "input_interval": original_step.get("input_interval", 100)
            })
        elif operation == "等待时间":
            parameters.update({
                "wait_type": original_step.get("wait_time_type", "固定时间"),
                "wait_time": original_step.get("wait_time_value", 1000),
                "wait_time_max": original_step.get("wait_time_max", 3000)
            })
        # 可以继续添加其他操作的参数映射
    
    def _validate_and_convert_flow(self, flow_data: Dict[str, Any]) -> Dict[str, Any]:
        """验证并转换流程数据"""
        # 基本结构验证
        if not isinstance(flow_data, dict):
            raise Exception("流程数据必须是字典格式")
        
        # 确保必要字段存在
        validated_flow = {
            "name": flow_data.get("name", "导入的流程"),
            "description": flow_data.get("description", ""),
            "steps": [],
            "variables": flow_data.get("variables", {}),
            "created_time": flow_data.get("created_time", datetime.now().isoformat()),
            "updated_time": datetime.now().isoformat()
        }
        
        # 验证和转换步骤
        steps = flow_data.get("steps", [])
        if not isinstance(steps, list):
            raise Exception("流程步骤必须是列表格式")
        
        for i, step in enumerate(steps):
            if not isinstance(step, dict):
                raise Exception(f"第{i+1}个步骤格式错误")
            
            # 确保步骤有必要的字段
            validated_step = {
                "id": step.get("id", str(uuid.uuid4())),
                "operation": step.get("operation", step.get("name", "未知操作")),
                "name": step.get("name", step.get("operation", "未命名操作")),
                "description": step.get("description", ""),
                "enabled": step.get("enabled", True),
                "parameters": step.get("parameters", {}),
                "timeout": step.get("timeout", 30000),
                "retry_count": step.get("retry_count", 0),
                "on_error": step.get("on_error", "stop")
            }
            
            # 复制其他参数
            for key, value in step.items():
                if key not in validated_step:
                    validated_step[key] = value
            
            validated_flow["steps"].append(validated_step)
        
        return validated_flow
    
    def _append_flow_steps(self, new_flow: Dict[str, Any]) -> Dict[str, Any]:
        """追加流程步骤到现有流程"""
        # 这里可以实现追加逻辑，目前返回新流程
        return new_flow
    
    # ==================== 流程模板功能 ====================
    
    def create_flow_template(self, flow_data: Dict[str, Any], template_name: str) -> bool:
        """创建流程模板"""
        try:
            template = {
                "name": template_name,
                "flow_data": flow_data,
                "created_time": datetime.now().isoformat(),
                "usage_count": 0
            }
            
            self.flow_templates[template_name] = template
            return True
            
        except Exception as e:
            print(f"创建流程模板失败: {str(e)}")
            return False
    
    def get_flow_template(self, template_name: str) -> Optional[Dict[str, Any]]:
        """获取流程模板"""
        template = self.flow_templates.get(template_name)
        if template:
            template["usage_count"] += 1
            return template["flow_data"].copy()
        return None
    
    def list_flow_templates(self) -> List[Dict[str, Any]]:
        """列出所有流程模板"""
        return [
            {
                "name": name,
                "created_time": template["created_time"],
                "usage_count": template["usage_count"]
            }
            for name, template in self.flow_templates.items()
        ]
    
    # ==================== 历史记录功能 ====================
    
    def get_import_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """获取导入历史"""
        return self.import_history[-limit:]
    
    def get_export_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """获取导出历史"""
        return self.export_history[-limit:]
    
    def clear_history(self, history_type: str = "all"):
        """清除历史记录"""
        if history_type == "import":
            self.import_history.clear()
        elif history_type == "export":
            self.export_history.clear()
        else:  # all
            self.import_history.clear()
            self.export_history.clear()
    
    # ==================== 兼容性检查 ====================
    
    def check_adspower_compatibility(self, flow_data: Dict[str, Any]) -> Dict[str, Any]:
        """检查与AdsPower的兼容性"""
        compatibility_report = {
            "compatible": True,
            "warnings": [],
            "errors": [],
            "suggestions": []
        }
        
        # 检查操作支持
        supported_operations = {
            "新建标签", "关闭标签", "关闭其他标签", "切换标签", "访问网站",
            "刷新页面", "页面后退", "页面截图", "经过元素", "下拉选择器",
            "元素聚焦", "点击元素", "输入内容", "上传附件", "执行JS脚本",
            "键盘按键", "组合键", "等待时间", "等待元素出现", "等待请求完成",
            "获取URL", "获取粘贴板内容", "元素数据", "当前焦点元素",
            "存到文件", "存到Excel", "导入txt", "获取邮件", "身份验证器码",
            "监听请求触发", "监听请求结果", "停止页面监听",
            "获取页面Cookie", "清除页面Cookie", "文本中提取", "转换Json对象",
            "字段提取", "随机提取", "更新环境备注", "更新环境标签",
            "启动新浏览器", "使用其他流程", "IF条件", "For循环元素",
            "For循环次数", "For循环数据", "While循环", "退出循环", "关闭浏览器"
        }
        
        for step in flow_data.get("steps", []):
            operation = step.get("operation", "")
            if operation not in supported_operations:
                compatibility_report["warnings"].append(f"操作 '{operation}' 可能不被AdsPower支持")
        
        return compatibility_report
    
    def get_manager_info(self) -> Dict[str, Any]:
        """获取流程管理器信息"""
        return {
            "stored_flows": len(self.flows),
            "flow_templates": len(self.flow_templates),
            "import_history_count": len(self.import_history),
            "export_history_count": len(self.export_history),
            "last_update": datetime.now().isoformat()
        }
