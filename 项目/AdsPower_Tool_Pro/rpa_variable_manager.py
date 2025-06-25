#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RPA变量管理系统
完全按照AdsPower原版实现变量系统，支持所有类型的变量操作
"""

import json
import os
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

class RPAVariableManager:
    """RPA变量管理器 - 完全按照AdsPower原版实现"""
    
    def __init__(self):
        self.variables = {}  # 存储所有变量
        self.environment_variables = {}  # AdsPower环境变量
        self.custom_variables = {}  # 用户自定义变量
        self.loop_variables = {}  # 循环变量
        self.system_variables = {}  # 系统变量
        self.variable_history = []  # 变量变更历史

        # 内存管理配置
        self.max_history_size = 500  # 最大历史记录数量
        self.max_variable_size = 1024 * 1024  # 单个变量最大大小 (1MB)
        
        # 初始化系统变量
        self._init_system_variables()
        
    def _init_system_variables(self):
        """初始化系统变量 - 按照AdsPower原版"""
        self.system_variables = {
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "current_date": datetime.now().strftime("%Y-%m-%d"),
            "current_timestamp": int(time.time()),
            "random_number": str(int(time.time() * 1000) % 10000),
            "task_start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "execution_count": 0
        }
        
        # 更新主变量字典
        self.variables.update(self.system_variables)
    
    def set_environment_variables(self, env_data: Dict[str, Any]):
        """设置AdsPower环境变量 - 完全按照AdsPower原版"""
        adspower_env_vars = {
            "task_id": env_data.get("task_id", ""),
            "task_name": env_data.get("task_name", ""),
            "serial_number": env_data.get("serial_number", ""),
            "browser_name": env_data.get("name", ""),
            "acc_id": env_data.get("user_id", ""),
            "comment": env_data.get("remark", ""),
            "user_name": env_data.get("username", ""),
            "password": env_data.get("password", ""),
            "group_id": env_data.get("group_id", ""),
            "group_name": env_data.get("group_name", ""),
            "proxy_type": env_data.get("proxy_type", ""),
            "proxy_host": env_data.get("proxy_host", ""),
            "proxy_port": env_data.get("proxy_port", ""),
            "user_agent": env_data.get("user_agent", ""),
            "screen_resolution": env_data.get("resolution", ""),
            "language": env_data.get("language", ""),
            "timezone": env_data.get("timezone", "")
        }
        
        self.environment_variables.update(adspower_env_vars)
        self.variables.update(adspower_env_vars)
        
        # 记录变量变更
        self._log_variable_change("environment", "batch_update", adspower_env_vars)
    
    def set_variable(self, name: str, value: Any, var_type: str = "custom"):
        """设置变量 - 支持所有AdsPower变量类型"""
        old_value = self.variables.get(name)
        
        # 类型转换和验证
        processed_value = self._process_variable_value(value)
        
        # 根据变量类型存储
        if var_type == "environment":
            self.environment_variables[name] = processed_value
        elif var_type == "loop":
            self.loop_variables[name] = processed_value
        elif var_type == "system":
            self.system_variables[name] = processed_value
        else:  # custom
            self.custom_variables[name] = processed_value
        
        # 更新主变量字典
        self.variables[name] = processed_value
        
        # 记录变量变更 - 控制历史记录大小
        self._log_variable_change(var_type, "set", {name: processed_value}, old_value)

        # 限制历史记录数量，防止内存泄漏
        if len(self.variable_history) > self.max_history_size:
            self.variable_history = self.variable_history[-self.max_history_size//2:]

        return True
    
    def get_variable(self, name: str, default: Any = None) -> Any:
        """获取变量值 - 按照AdsPower原版优先级"""
        # AdsPower原版变量优先级：循环变量 > 环境变量 > 自定义变量 > 系统变量
        if name in self.loop_variables:
            return self.loop_variables[name]
        elif name in self.environment_variables:
            return self.environment_variables[name]
        elif name in self.custom_variables:
            return self.custom_variables[name]
        elif name in self.system_variables:
            return self.system_variables[name]
        else:
            return default
    
    def delete_variable(self, name: str) -> bool:
        """删除变量"""
        deleted = False
        old_value = self.variables.get(name)
        
        # 从各个变量字典中删除
        if name in self.custom_variables:
            del self.custom_variables[name]
            deleted = True
        if name in self.loop_variables:
            del self.loop_variables[name]
            deleted = True
        if name in self.environment_variables:
            del self.environment_variables[name]
            deleted = True
        if name in self.variables:
            del self.variables[name]
            deleted = True
        
        if deleted:
            self._log_variable_change("delete", "delete", {name: None}, old_value)
        
        return deleted
    
    def clear_variables(self, var_type: str = "all"):
        """清除变量 - 按类型清除"""
        if var_type == "all":
            self.variables.clear()
            self.custom_variables.clear()
            self.loop_variables.clear()
            self.environment_variables.clear()
            self._init_system_variables()  # 重新初始化系统变量
        elif var_type == "custom":
            for name in list(self.custom_variables.keys()):
                if name in self.variables:
                    del self.variables[name]
            self.custom_variables.clear()
        elif var_type == "loop":
            for name in list(self.loop_variables.keys()):
                if name in self.variables:
                    del self.variables[name]
            self.loop_variables.clear()
        elif var_type == "environment":
            for name in list(self.environment_variables.keys()):
                if name in self.variables:
                    del self.variables[name]
            self.environment_variables.clear()
        
        self._log_variable_change(var_type, "clear", {})
    
    def get_all_variables(self) -> Dict[str, Any]:
        """获取所有变量"""
        return self.variables.copy()
    
    def get_variables_by_type(self, var_type: str) -> Dict[str, Any]:
        """按类型获取变量"""
        if var_type == "environment":
            return self.environment_variables.copy()
        elif var_type == "custom":
            return self.custom_variables.copy()
        elif var_type == "loop":
            return self.loop_variables.copy()
        elif var_type == "system":
            return self.system_variables.copy()
        else:
            return {}
    
    def set_loop_variables(self, loop_type: str, **kwargs):
        """设置循环变量 - 按照AdsPower原版循环变量命名"""
        if loop_type == "for_elements":
            self.set_variable("for_elements_item", kwargs.get("item"), "loop")
            self.set_variable("for_elements_index", kwargs.get("index", 0), "loop")
        elif loop_type == "for_times":
            self.set_variable("for_times_index", kwargs.get("index", 0), "loop")
        elif loop_type == "for_data":
            self.set_variable("for_list_item", kwargs.get("item"), "loop")
            self.set_variable("for_list_index", kwargs.get("index", 0), "loop")
        elif loop_type == "while":
            self.set_variable("while_loop_count", kwargs.get("count", 0), "loop")
    
    def clear_loop_variables(self):
        """清除所有循环变量"""
        loop_var_names = [
            "for_elements_item", "for_elements_index",
            "for_times_index", "for_list_item", "for_list_index",
            "while_loop_count"
        ]
        
        for var_name in loop_var_names:
            if var_name in self.loop_variables:
                del self.loop_variables[var_name]
            if var_name in self.variables:
                del self.variables[var_name]
    
    def update_system_variables(self):
        """更新系统变量"""
        self.system_variables.update({
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "current_date": datetime.now().strftime("%Y-%m-%d"),
            "current_timestamp": int(time.time()),
            "execution_count": self.system_variables.get("execution_count", 0) + 1
        })
        
        self.variables.update(self.system_variables)
    
    def _process_variable_value(self, value: Any) -> Any:
        """处理变量值 - 类型转换和验证，优化内存使用"""
        # 检查变量大小
        try:
            import sys
            value_size = sys.getsizeof(value)
            if value_size > self.max_variable_size:
                print(f"[变量管理器] 警告: 变量值过大 ({value_size} bytes)，可能影响性能")
                # 对于大字符串进行截断
                if isinstance(value, str) and len(value) > 10000:
                    value = value[:10000] + "...[截断]"
        except Exception as e:
            print(f"[变量管理器] 检查变量大小时出错: {e}")

        if value is None:
            return ""
        elif isinstance(value, (str, int, float, bool)):
            return value
        elif isinstance(value, (list, dict)):
            try:
                return json.dumps(value, ensure_ascii=False)
            except (TypeError, ValueError) as e:
                print(f"[变量管理器] JSON序列化失败: {e}")
                return str(value)
        else:
            return str(value)
    
    def _log_variable_change(self, var_type: str, action: str, data: Dict[str, Any], old_value: Any = None):
        """记录变量变更历史"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": var_type,
            "action": action,
            "data": data,
            "old_value": old_value
        }
        
        self.variable_history.append(log_entry)
        
        # 保持历史记录在合理范围内
        if len(self.variable_history) > 1000:
            self.variable_history = self.variable_history[-500:]
    
    def export_variables(self, file_path: str = None) -> str:
        """导出变量到文件"""
        export_data = {
            "export_time": datetime.now().isoformat(),
            "variables": {
                "environment": self.environment_variables,
                "custom": self.custom_variables,
                "loop": self.loop_variables,
                "system": self.system_variables
            },
            "history": self.variable_history[-100:]  # 只导出最近100条历史
        }
        
        if not file_path:
            file_path = f"variables_export_{int(time.time())}.json"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        return file_path
    
    def import_variables(self, file_path: str) -> bool:
        """从文件导入变量"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            variables = import_data.get("variables", {})
            
            # 导入各类型变量
            if "environment" in variables:
                self.environment_variables.update(variables["environment"])
            if "custom" in variables:
                self.custom_variables.update(variables["custom"])
            if "loop" in variables:
                self.loop_variables.update(variables["loop"])
            
            # 更新主变量字典
            self.variables.update(self.environment_variables)
            self.variables.update(self.custom_variables)
            self.variables.update(self.loop_variables)
            self.variables.update(self.system_variables)
            
            self._log_variable_change("import", "import", {"file": file_path})
            return True
            
        except Exception as e:
            print(f"导入变量失败: {str(e)}")
            return False
    
    def get_variable_info(self) -> Dict[str, Any]:
        """获取变量系统信息"""
        return {
            "total_variables": len(self.variables),
            "environment_variables": len(self.environment_variables),
            "custom_variables": len(self.custom_variables),
            "loop_variables": len(self.loop_variables),
            "system_variables": len(self.system_variables),
            "history_count": len(self.variable_history),
            "last_update": datetime.now().isoformat()
        }
