#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AdsPower工具专业版 - RPA参数配置转换器
将当前配置界面的参数转换为AdsPower官方标准格式
"""

import json
from typing import Dict, Any, Optional

class AdsPowerConfigConverter:
    """AdsPower参数配置转换器"""
    
    def __init__(self):
        self.conversion_map = {}
        self._init_conversion_map()
    
    def _init_conversion_map(self):
        """初始化参数转换映射表"""
        self.conversion_map = {
            # 点击元素参数转换
            "点击元素": {
                "old_to_new": {
                    "click_selector_type": "selector_type",
                    "click_selector": "selector",
                    "click_action": "key_type",
                    "click_type": "click_type",
                    "click_element_index": "element_order",
                    "click_element_order": "element_order"
                },
                "value_mapping": {
                    "click_type": {
                        "left": "鼠标左键",
                        "right": "鼠标右键", 
                        "middle": "鼠标中键",
                        "double": "双击"
                    },
                    "key_type": {
                        "single": "单击",
                        "double": "双击"
                    }
                },
                "default_values": {
                    "stored_element": "无",
                    "element_order": 1,
                    "click_type": "鼠标左键",
                    "key_type": "单击"
                }
            },
            
            # 输入内容参数转换
            "输入内容": {
                "old_to_new": {
                    "input_selector_type": "selector_type",
                    "input_selector": "selector",
                    "input_content": "content",
                    "input_method": "clear_before",
                    "input_interval": "input_interval",
                    "input_element_order": "element_order"
                },
                "value_mapping": {
                    "clear_before": {
                        "覆盖": True,
                        "追加": False
                    }
                },
                "default_values": {
                    "stored_element": "无",
                    "element_order": 1,
                    "content_type": "顺序选取",
                    "input_interval": 300,
                    "clear_before": True
                }
            },
            
            # 等待元素出现参数转换
            "等待元素出现": {
                "old_to_new": {
                    "wait_element_selector": "selector",
                    "wait_element_timeout": "timeout",
                    "wait_element_order": "element_order"
                },
                "default_values": {
                    "element_order": 1,
                    "is_visible": True,
                    "timeout": 30000,
                    "save_to": ""
                }
            },
            
            # 页面截图参数转换
            "页面截图": {
                "old_to_new": {
                    "screenshot_name": "screenshot_name",
                    "image_format": "image_format"
                },
                "default_values": {
                    "full_page": False,
                    "jpeg_quality": 80
                }
            },
            
            # 等待时间参数转换
            "等待时间": {
                "old_to_new": {
                    "wait_type": "wait_type",
                    "wait_time": "wait_time",
                    "wait_min": "wait_min",
                    "wait_max": "wait_max"
                },
                "default_values": {
                    "wait_type": "固定值",
                    "wait_time": 3000,
                    "wait_min": 2000,
                    "wait_max": 5000
                }
            }
        }
    
    def convert_to_standard(self, operation: str, old_config: Dict[str, Any]) -> Dict[str, Any]:
        """将旧格式配置转换为AdsPower官方标准格式"""
        if operation not in self.conversion_map:
            # 如果没有转换规则，直接返回原配置
            return old_config.copy()
        
        conversion_rule = self.conversion_map[operation]
        new_config = {}
        
        # 应用参数名称转换
        old_to_new = conversion_rule.get("old_to_new", {})
        for old_key, new_key in old_to_new.items():
            if old_key in old_config:
                old_value = old_config[old_key]
                
                # 应用值映射转换
                value_mapping = conversion_rule.get("value_mapping", {})
                if new_key in value_mapping and old_value in value_mapping[new_key]:
                    new_config[new_key] = value_mapping[new_key][old_value]
                else:
                    new_config[new_key] = old_value
        
        # 添加默认值
        default_values = conversion_rule.get("default_values", {})
        for key, value in default_values.items():
            if key not in new_config:
                new_config[key] = value
        
        # 保留未转换的参数
        for key, value in old_config.items():
            if key not in old_to_new and key not in new_config:
                new_config[key] = value
        
        return new_config
    
    def convert_from_standard(self, operation: str, standard_config: Dict[str, Any]) -> Dict[str, Any]:
        """将AdsPower官方标准格式转换为当前界面格式"""
        if operation not in self.conversion_map:
            return standard_config.copy()
        
        conversion_rule = self.conversion_map[operation]
        old_config = {}
        
        # 反向转换参数名称
        old_to_new = conversion_rule.get("old_to_new", {})
        new_to_old = {v: k for k, v in old_to_new.items()}
        
        for new_key, old_key in new_to_old.items():
            if new_key in standard_config:
                new_value = standard_config[new_key]
                
                # 反向应用值映射转换
                value_mapping = conversion_rule.get("value_mapping", {})
                if new_key in value_mapping:
                    reverse_mapping = {v: k for k, v in value_mapping[new_key].items()}
                    if new_value in reverse_mapping:
                        old_config[old_key] = reverse_mapping[new_value]
                    else:
                        old_config[old_key] = new_value
                else:
                    old_config[old_key] = new_value
        
        # 保留未转换的参数
        for key, value in standard_config.items():
            if key not in new_to_old and key not in old_config:
                old_config[key] = value
        
        return old_config
    
    def convert_step_config(self, step_config: Dict[str, Any]) -> Dict[str, Any]:
        """转换单个步骤配置"""
        operation = step_config.get("operation", "")
        if not operation:
            return step_config
        
        # 提取配置参数
        config_params = {k: v for k, v in step_config.items() if k != "operation"}
        
        # 转换为标准格式
        standard_params = self.convert_to_standard(operation, config_params)
        
        # 返回包含操作名称的完整配置
        return {
            "operation": operation,
            **standard_params
        }
    
    def convert_flow_config(self, flow_config: Dict[str, Any]) -> Dict[str, Any]:
        """转换整个流程配置"""
        converted_flow = flow_config.copy()
        
        if "steps" in flow_config:
            converted_steps = []
            for step in flow_config["steps"]:
                converted_step = self.convert_step_config(step)
                converted_steps.append(converted_step)
            converted_flow["steps"] = converted_steps
        
        return converted_flow
    
    def validate_standard_config(self, operation: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """验证标准配置的完整性"""
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        # 基本验证规则
        validation_rules = {
            "点击元素": {
                "required": ["selector"],
                "optional": ["stored_element", "element_order", "click_type", "key_type"]
            },
            "输入内容": {
                "required": ["selector", "content"],
                "optional": ["stored_element", "element_order", "content_type", "input_interval", "clear_before"]
            },
            "等待元素出现": {
                "required": ["selector"],
                "optional": ["element_order", "is_visible", "timeout", "save_to"]
            },
            "页面截图": {
                "required": [],
                "optional": ["screenshot_name", "full_page", "image_format", "jpeg_quality"]
            },
            "等待时间": {
                "required": ["wait_type"],
                "optional": ["wait_time", "wait_min", "wait_max"]
            }
        }
        
        if operation in validation_rules:
            rule = validation_rules[operation]
            
            # 检查必需参数
            for required_param in rule["required"]:
                if required_param not in config or not config[required_param]:
                    validation_result["valid"] = False
                    validation_result["errors"].append(f"缺少必需参数: {required_param}")
            
            # 检查参数类型和值范围
            if operation == "等待时间":
                wait_type = config.get("wait_type")
                if wait_type == "固定值" and "wait_time" not in config:
                    validation_result["errors"].append("固定值等待类型需要wait_time参数")
                elif wait_type == "区间随机" and ("wait_min" not in config or "wait_max" not in config):
                    validation_result["errors"].append("区间随机等待类型需要wait_min和wait_max参数")
        
        return validation_result
    
    def get_standard_template(self, operation: str) -> Dict[str, Any]:
        """获取操作的标准配置模板"""
        if operation not in self.conversion_map:
            return {"operation": operation}
        
        template = {"operation": operation}
        default_values = self.conversion_map[operation].get("default_values", {})
        template.update(default_values)
        
        return template
    
    def get_supported_operations(self) -> list:
        """获取支持转换的操作列表"""
        return list(self.conversion_map.keys())

# 全局转换器实例
config_converter = AdsPowerConfigConverter()

# 便捷函数
def convert_to_adspower_standard(operation: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """转换为AdsPower官方标准格式"""
    return config_converter.convert_to_standard(operation, config)

def convert_from_adspower_standard(operation: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """从AdsPower官方标准格式转换"""
    return config_converter.convert_from_standard(operation, config)

def validate_config(operation: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """验证配置"""
    return config_converter.validate_standard_config(operation, config)

def get_template(operation: str) -> Dict[str, Any]:
    """获取标准模板"""
    return config_converter.get_standard_template(operation)
