#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RPA执行日志系统
完全按照AdsPower原版实现详细的执行过程记录和调试信息
"""

import os
import json
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from enum import Enum

class LogLevel(Enum):
    """日志级别"""
    DEBUG = "debug"
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class RPALogger:
    """RPA执行日志记录器 - 完全按照AdsPower原版实现"""
    
    def __init__(self, task_name: str = "RPA_Task", log_dir: str = "logs"):
        self.task_name = task_name
        self.log_dir = log_dir
        self.session_id = f"{task_name}_{int(time.time())}"
        self.start_time = datetime.now()

        # 创建日志目录
        os.makedirs(log_dir, exist_ok=True)

        # 日志存储 - 优化内存使用
        self.logs = []
        self.step_logs = {}  # 按步骤分组的日志
        self.performance_data = {}  # 性能数据
        self.error_count = 0
        self.warning_count = 0
        self.success_count = 0

        # 日志缓存控制
        self.max_logs_in_memory = 1000  # 最大内存中保存的日志数量
        self.log_buffer = []  # 日志缓冲区
        self.buffer_size = 50  # 缓冲区大小

        # 文件路径
        self.log_file = os.path.join(log_dir, f"{self.session_id}.log")
        self.json_file = os.path.join(log_dir, f"{self.session_id}.json")

        # 文件句柄
        self._log_file_handle = None

        # 初始化日志文件
        self._init_log_files()
    
    def _init_log_files(self):
        """初始化日志文件"""
        # 创建文本日志文件
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write(f"=== RPA执行日志 - {self.task_name} ===\n")
            f.write(f"开始时间: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"会话ID: {self.session_id}\n")
            f.write("=" * 50 + "\n\n")
    
    def log(self, message: str, level: LogLevel = LogLevel.INFO, 
            step_id: str = None, data: Dict[str, Any] = None):
        """记录日志"""
        timestamp = datetime.now()
        
        log_entry = {
            "timestamp": timestamp.isoformat(),
            "level": level.value,
            "message": message,
            "step_id": step_id,
            "data": data or {},
            "session_id": self.session_id
        }
        
        # 添加到内存日志 - 控制内存使用
        self.logs.append(log_entry)
        if len(self.logs) > self.max_logs_in_memory:
            # 移除最旧的日志，保持内存使用在合理范围内
            self.logs.pop(0)

        # 按步骤分组
        if step_id:
            if step_id not in self.step_logs:
                self.step_logs[step_id] = []
            self.step_logs[step_id].append(log_entry)

        # 更新计数器
        if level == LogLevel.ERROR or level == LogLevel.CRITICAL:
            self.error_count += 1
        elif level == LogLevel.WARNING:
            self.warning_count += 1
        elif level == LogLevel.SUCCESS:
            self.success_count += 1

        # 添加到缓冲区
        self.log_buffer.append(log_entry)

        # 当缓冲区满时，批量写入文件
        if len(self.log_buffer) >= self.buffer_size:
            self._flush_buffer()

        # 输出到控制台（可选）
        self._print_log(log_entry)

    def _flush_buffer(self):
        """刷新日志缓冲区到文件"""
        if not self.log_buffer:
            return

        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                for log_entry in self.log_buffer:
                    timestamp_str = datetime.fromisoformat(log_entry["timestamp"]).strftime("%H:%M:%S")
                    level_str = log_entry["level"].upper().ljust(8)
                    message = log_entry["message"]
                    step_info = f" [步骤:{log_entry['step_id']}]" if log_entry["step_id"] else ""
                    log_line = f"[{timestamp_str}] {level_str} {message}{step_info}\n"
                    f.write(log_line)

            # 清空缓冲区
            self.log_buffer.clear()

        except Exception as e:
            print(f"刷新日志缓冲区失败: {e}")

    def _write_to_file(self, log_entry: Dict[str, Any]):
        """写入日志文件"""
        timestamp_str = datetime.fromisoformat(log_entry["timestamp"]).strftime("%H:%M:%S")
        level_str = log_entry["level"].upper().ljust(8)
        message = log_entry["message"]
        step_info = f" [步骤:{log_entry['step_id']}]" if log_entry["step_id"] else ""
        
        log_line = f"[{timestamp_str}] {level_str} {message}{step_info}\n"
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_line)
    
    def _print_log(self, log_entry: Dict[str, Any]):
        """打印日志到控制台"""
        timestamp_str = datetime.fromisoformat(log_entry["timestamp"]).strftime("%H:%M:%S")
        level_str = log_entry["level"].upper()
        message = log_entry["message"]
        
        # 根据级别设置颜色（如果支持）
        color_codes = {
            "debug": "\033[36m",    # 青色
            "info": "\033[37m",     # 白色
            "success": "\033[32m",  # 绿色
            "warning": "\033[33m",  # 黄色
            "error": "\033[31m",    # 红色
            "critical": "\033[35m"  # 紫色
        }
        reset_code = "\033[0m"
        
        color = color_codes.get(log_entry["level"], "")
        print(f"{color}[{timestamp_str}] {level_str}: {message}{reset_code}")
    
    # 便捷方法
    def debug(self, message: str, step_id: str = None, data: Dict[str, Any] = None):
        """记录调试日志"""
        self.log(message, LogLevel.DEBUG, step_id, data)
    
    def info(self, message: str, step_id: str = None, data: Dict[str, Any] = None):
        """记录信息日志"""
        self.log(message, LogLevel.INFO, step_id, data)
    
    def success(self, message: str, step_id: str = None, data: Dict[str, Any] = None):
        """记录成功日志"""
        self.log(message, LogLevel.SUCCESS, step_id, data)
    
    def warning(self, message: str, step_id: str = None, data: Dict[str, Any] = None):
        """记录警告日志"""
        self.log(message, LogLevel.WARNING, step_id, data)
    
    def error(self, message: str, step_id: str = None, data: Dict[str, Any] = None):
        """记录错误日志"""
        self.log(message, LogLevel.ERROR, step_id, data)
    
    def critical(self, message: str, step_id: str = None, data: Dict[str, Any] = None):
        """记录严重错误日志"""
        self.log(message, LogLevel.CRITICAL, step_id, data)
    
    # 步骤相关方法
    def start_step(self, step_id: str, step_name: str, config: Dict[str, Any] = None):
        """开始执行步骤"""
        self.info(f"开始执行步骤: {step_name}", step_id, {
            "step_name": step_name,
            "config": config,
            "action": "step_start"
        })
    
    def end_step(self, step_id: str, step_name: str, success: bool = True, 
                result: Dict[str, Any] = None):
        """结束执行步骤"""
        level = LogLevel.SUCCESS if success else LogLevel.ERROR
        status = "成功" if success else "失败"
        self.log(f"步骤执行{status}: {step_name}", level, step_id, {
            "step_name": step_name,
            "success": success,
            "result": result,
            "action": "step_end"
        })
    
    def log_operation(self, operation: str, target: str = None, 
                     result: str = None, step_id: str = None):
        """记录操作日志"""
        message = f"执行操作: {operation}"
        if target:
            message += f" -> {target}"
        if result:
            message += f" | 结果: {result}"
        
        self.info(message, step_id, {
            "operation": operation,
            "target": target,
            "result": result,
            "action": "operation"
        })
    
    def log_element_action(self, action: str, selector: str, element_text: str = None,
                          success: bool = True, step_id: str = None):
        """记录元素操作日志"""
        status = "成功" if success else "失败"
        message = f"元素{action}{status}: {selector}"
        if element_text:
            message += f" (文本: {element_text[:50]})"
        
        level = LogLevel.SUCCESS if success else LogLevel.ERROR
        self.log(message, level, step_id, {
            "action": action,
            "selector": selector,
            "element_text": element_text,
            "success": success,
            "action_type": "element_action"
        })
    
    def log_navigation(self, url: str, success: bool = True, step_id: str = None):
        """记录页面导航日志"""
        status = "成功" if success else "失败"
        message = f"页面导航{status}: {url}"
        
        level = LogLevel.SUCCESS if success else LogLevel.ERROR
        self.log(message, level, step_id, {
            "url": url,
            "success": success,
            "action_type": "navigation"
        })
    
    def log_wait(self, wait_type: str, duration: float = None, 
                condition: str = None, step_id: str = None):
        """记录等待操作日志"""
        message = f"等待操作: {wait_type}"
        if duration:
            message += f" ({duration}秒)"
        if condition:
            message += f" - {condition}"
        
        self.info(message, step_id, {
            "wait_type": wait_type,
            "duration": duration,
            "condition": condition,
            "action_type": "wait"
        })
    
    def log_data_operation(self, operation: str, source: str = None, 
                          target: str = None, data_size: int = None, step_id: str = None):
        """记录数据操作日志"""
        message = f"数据操作: {operation}"
        if source:
            message += f" 来源: {source}"
        if target:
            message += f" 目标: {target}"
        if data_size:
            message += f" 大小: {data_size}"
        
        self.info(message, step_id, {
            "operation": operation,
            "source": source,
            "target": target,
            "data_size": data_size,
            "action_type": "data_operation"
        })
    
    # 性能监控
    def start_performance_timer(self, timer_name: str):
        """开始性能计时"""
        self.performance_data[timer_name] = {
            "start_time": time.time(),
            "end_time": None,
            "duration": None
        }
    
    def end_performance_timer(self, timer_name: str):
        """结束性能计时"""
        if timer_name in self.performance_data:
            end_time = time.time()
            self.performance_data[timer_name]["end_time"] = end_time
            duration = end_time - self.performance_data[timer_name]["start_time"]
            self.performance_data[timer_name]["duration"] = duration
            
            self.debug(f"性能计时 {timer_name}: {duration:.2f}秒", data={
                "timer_name": timer_name,
                "duration": duration,
                "action_type": "performance"
            })
    
    # 导出和统计
    def get_summary(self) -> Dict[str, Any]:
        """获取执行摘要"""
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        return {
            "session_id": self.session_id,
            "task_name": self.task_name,
            "start_time": self.start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "duration": duration,
            "total_logs": len(self.logs),
            "success_count": self.success_count,
            "warning_count": self.warning_count,
            "error_count": self.error_count,
            "steps_executed": len(self.step_logs),
            "performance_data": self.performance_data
        }
    
    def export_to_json(self) -> str:
        """导出日志到JSON文件"""
        export_data = {
            "summary": self.get_summary(),
            "logs": self.logs,
            "step_logs": self.step_logs,
            "performance_data": self.performance_data
        }
        
        with open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        return self.json_file
    
    def get_logs_by_level(self, level: LogLevel) -> List[Dict[str, Any]]:
        """按级别获取日志"""
        return [log for log in self.logs if log["level"] == level.value]
    
    def get_logs_by_step(self, step_id: str) -> List[Dict[str, Any]]:
        """按步骤获取日志"""
        return self.step_logs.get(step_id, [])
    
    def get_recent_logs(self, count: int = 50) -> List[Dict[str, Any]]:
        """获取最近的日志"""
        return self.logs[-count:]
    
    def clear_logs(self):
        """清空日志"""
        self.logs.clear()
        self.step_logs.clear()
        self.performance_data.clear()
        self.error_count = 0
        self.warning_count = 0
        self.success_count = 0
        
        # 重新初始化日志文件
        self._init_log_files()
    
    def finalize(self):
        """完成日志记录"""
        summary = self.get_summary()
        
        # 写入摘要到文本日志
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write("\n" + "=" * 50 + "\n")
            f.write("=== 执行摘要 ===\n")
            f.write(f"总耗时: {summary['duration']:.2f}秒\n")
            f.write(f"总日志数: {summary['total_logs']}\n")
            f.write(f"成功: {summary['success_count']}\n")
            f.write(f"警告: {summary['warning_count']}\n")
            f.write(f"错误: {summary['error_count']}\n")
            f.write(f"执行步骤: {summary['steps_executed']}\n")
            f.write("=" * 50 + "\n")
        
        # 导出JSON
        self.export_to_json()
        
        self.info(f"日志记录完成，文件保存至: {self.log_file}")
        return summary

    def close(self):
        """关闭日志器，刷新缓冲区并释放资源"""
        try:
            # 刷新剩余的缓冲区
            self._flush_buffer()

            # 关闭文件句柄
            if hasattr(self, '_log_file_handle') and self._log_file_handle:
                self._log_file_handle.close()
                self._log_file_handle = None

        except Exception as e:
            print(f"关闭日志器时出错: {e}")

    def __enter__(self):
        """上下文管理器入口"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close()

    def __del__(self):
        """析构函数"""
        try:
            self.close()
        except:
            pass
