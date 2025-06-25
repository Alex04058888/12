#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RPA异常处理和错误恢复系统
完全按照AdsPower原版实现异常处理机制，包括网络异常、元素找不到、超时等各种异常情况的处理和恢复
"""

import time
import traceback
from datetime import datetime
from typing import Any, Dict, List, Optional, Callable
from enum import Enum

class ErrorType(Enum):
    """错误类型枚举"""
    NETWORK_ERROR = "network_error"
    ELEMENT_NOT_FOUND = "element_not_found"
    TIMEOUT_ERROR = "timeout_error"
    BROWSER_ERROR = "browser_error"
    SCRIPT_ERROR = "script_error"
    VALIDATION_ERROR = "validation_error"
    PERMISSION_ERROR = "permission_error"
    SYSTEM_ERROR = "system_error"
    UNKNOWN_ERROR = "unknown_error"

class RecoveryAction(Enum):
    """恢复动作枚举"""
    RETRY = "retry"
    SKIP = "skip"
    STOP = "stop"
    CONTINUE = "continue"
    RESTART_BROWSER = "restart_browser"
    WAIT_AND_RETRY = "wait_and_retry"
    FALLBACK = "fallback"

class RPAException(Exception):
    """RPA自定义异常基类"""
    
    def __init__(self, message: str, error_type: ErrorType = ErrorType.UNKNOWN_ERROR, 
                 step_id: str = None, data: Dict[str, Any] = None):
        super().__init__(message)
        self.message = message
        self.error_type = error_type
        self.step_id = step_id
        self.data = data or {}
        self.timestamp = datetime.now()

class NetworkException(RPAException):
    """网络异常"""
    def __init__(self, message: str, step_id: str = None, data: Dict[str, Any] = None):
        super().__init__(message, ErrorType.NETWORK_ERROR, step_id, data)

class ElementNotFoundException(RPAException):
    """元素未找到异常"""
    def __init__(self, message: str, step_id: str = None, data: Dict[str, Any] = None):
        super().__init__(message, ErrorType.ELEMENT_NOT_FOUND, step_id, data)

class TimeoutException(RPAException):
    """超时异常"""
    def __init__(self, message: str, step_id: str = None, data: Dict[str, Any] = None):
        super().__init__(message, ErrorType.TIMEOUT_ERROR, step_id, data)

class BrowserException(RPAException):
    """浏览器异常"""
    def __init__(self, message: str, step_id: str = None, data: Dict[str, Any] = None):
        super().__init__(message, ErrorType.BROWSER_ERROR, step_id, data)

class RPAExceptionHandler:
    """RPA异常处理器 - 完全按照AdsPower原版实现"""
    
    def __init__(self, logger=None):
        self.logger = logger
        self.error_history = []
        self.recovery_strategies = {}
        self.retry_counts = {}
        self.max_retries = 3
        self.retry_delay = 2.0
        
        # 初始化默认恢复策略
        self._init_default_strategies()
    
    def _init_default_strategies(self):
        """初始化默认恢复策略"""
        self.recovery_strategies = {
            ErrorType.NETWORK_ERROR: {
                "action": RecoveryAction.WAIT_AND_RETRY,
                "max_retries": 3,
                "delay": 5.0,
                "fallback": RecoveryAction.SKIP
            },
            ErrorType.ELEMENT_NOT_FOUND: {
                "action": RecoveryAction.WAIT_AND_RETRY,
                "max_retries": 2,
                "delay": 2.0,
                "fallback": RecoveryAction.SKIP
            },
            ErrorType.TIMEOUT_ERROR: {
                "action": RecoveryAction.RETRY,
                "max_retries": 2,
                "delay": 1.0,
                "fallback": RecoveryAction.SKIP
            },
            ErrorType.BROWSER_ERROR: {
                "action": RecoveryAction.RESTART_BROWSER,
                "max_retries": 1,
                "delay": 3.0,
                "fallback": RecoveryAction.STOP
            },
            ErrorType.SCRIPT_ERROR: {
                "action": RecoveryAction.SKIP,
                "max_retries": 0,
                "delay": 0.0,
                "fallback": RecoveryAction.CONTINUE
            },
            ErrorType.VALIDATION_ERROR: {
                "action": RecoveryAction.STOP,
                "max_retries": 0,
                "delay": 0.0,
                "fallback": RecoveryAction.STOP
            },
            ErrorType.PERMISSION_ERROR: {
                "action": RecoveryAction.STOP,
                "max_retries": 0,
                "delay": 0.0,
                "fallback": RecoveryAction.STOP
            },
            ErrorType.SYSTEM_ERROR: {
                "action": RecoveryAction.STOP,
                "max_retries": 0,
                "delay": 0.0,
                "fallback": RecoveryAction.STOP
            },
            ErrorType.UNKNOWN_ERROR: {
                "action": RecoveryAction.RETRY,
                "max_retries": 1,
                "delay": 1.0,
                "fallback": RecoveryAction.SKIP
            }
        }
    
    def handle_exception(self, exception: Exception, step_id: str = None,
                        operation: str = None) -> Dict[str, Any]:
        """处理异常并返回恢复策略 - 优化异常处理"""
        try:
            # 转换为RPA异常
            if isinstance(exception, RPAException):
                rpa_exception = exception
            else:
                rpa_exception = self._convert_to_rpa_exception(exception, step_id)

            # 记录异常
            self._log_exception(rpa_exception, operation)

            # 获取恢复策略
            recovery_plan = self._get_recovery_plan(rpa_exception, step_id)

            # 记录到历史 - 限制历史记录数量
            error_record = {
                "timestamp": rpa_exception.timestamp.isoformat(),
                "error_type": rpa_exception.error_type.value,
                "message": rpa_exception.message,
                "step_id": step_id,
                "operation": operation,
                "recovery_plan": recovery_plan,
                "traceback": traceback.format_exc()
            }

            self.error_history.append(error_record)

            # 限制历史记录数量，防止内存泄漏
            if len(self.error_history) > 1000:
                self.error_history = self.error_history[-500:]  # 保留最近500条

            return recovery_plan

        except Exception as e:
            # 异常处理器本身出错时的兜底处理
            print(f"[异常处理器] 处理异常时发生错误: {e}")
            return {
                "action": "stop",
                "message": "异常处理器故障，建议停止执行",
                "retry_count": 0,
                "wait_time": 0
            }
    
    def _convert_to_rpa_exception(self, exception: Exception, step_id: str = None) -> RPAException:
        """将普通异常转换为RPA异常"""
        exception_name = type(exception).__name__
        message = str(exception)
        
        # 根据异常类型判断错误类型
        if "timeout" in exception_name.lower() or "timeout" in message.lower():
            return TimeoutException(message, step_id)
        elif "network" in exception_name.lower() or "connection" in message.lower():
            return NetworkException(message, step_id)
        elif "element" in exception_name.lower() or "not found" in message.lower():
            return ElementNotFoundException(message, step_id)
        elif "browser" in exception_name.lower() or "webdriver" in exception_name.lower():
            return BrowserException(message, step_id)
        else:
            return RPAException(message, ErrorType.UNKNOWN_ERROR, step_id)
    
    def _log_exception(self, exception: RPAException, operation: str = None):
        """记录异常日志"""
        if self.logger:
            error_msg = f"异常发生: {exception.message}"
            if operation:
                error_msg += f" (操作: {operation})"
            if exception.step_id:
                error_msg += f" (步骤: {exception.step_id})"
            
            self.logger.error(error_msg, exception.step_id, {
                "error_type": exception.error_type.value,
                "exception_data": exception.data,
                "operation": operation
            })
    
    def _get_recovery_plan(self, exception: RPAException, step_id: str = None) -> Dict[str, Any]:
        """获取恢复计划"""
        error_type = exception.error_type
        strategy = self.recovery_strategies.get(error_type, self.recovery_strategies[ErrorType.UNKNOWN_ERROR])
        
        # 检查重试次数
        retry_key = f"{step_id}_{error_type.value}" if step_id else error_type.value
        current_retries = self.retry_counts.get(retry_key, 0)
        
        # 确定恢复动作
        if current_retries >= strategy["max_retries"]:
            action = strategy["fallback"]
            should_retry = False
        else:
            action = strategy["action"]
            should_retry = action in [RecoveryAction.RETRY, RecoveryAction.WAIT_AND_RETRY]
        
        # 更新重试计数
        if should_retry:
            self.retry_counts[retry_key] = current_retries + 1
        
        recovery_plan = {
            "action": action.value,
            "should_retry": should_retry,
            "retry_count": current_retries,
            "max_retries": strategy["max_retries"],
            "delay": strategy["delay"],
            "error_type": error_type.value,
            "message": exception.message,
            "recommendations": self._get_recommendations(exception)
        }
        
        return recovery_plan
    
    def _get_recommendations(self, exception: RPAException) -> List[str]:
        """获取错误处理建议"""
        recommendations = []
        
        if exception.error_type == ErrorType.NETWORK_ERROR:
            recommendations.extend([
                "检查网络连接是否正常",
                "确认目标网站是否可访问",
                "考虑增加网络超时时间",
                "检查代理设置是否正确"
            ])
        elif exception.error_type == ErrorType.ELEMENT_NOT_FOUND:
            recommendations.extend([
                "检查元素选择器是否正确",
                "确认页面是否完全加载",
                "考虑增加等待时间",
                "检查页面结构是否发生变化"
            ])
        elif exception.error_type == ErrorType.TIMEOUT_ERROR:
            recommendations.extend([
                "增加操作超时时间",
                "检查页面加载速度",
                "优化网络环境",
                "考虑分步骤执行"
            ])
        elif exception.error_type == ErrorType.BROWSER_ERROR:
            recommendations.extend([
                "重启浏览器实例",
                "检查浏览器版本兼容性",
                "清理浏览器缓存",
                "检查系统资源使用情况"
            ])
        
        return recommendations
    
    def execute_with_recovery(self, func: Callable, *args, **kwargs) -> Dict[str, Any]:
        """带异常恢复的函数执行"""
        step_id = kwargs.get('step_id')
        operation = kwargs.get('operation', func.__name__)
        
        while True:
            try:
                result = func(*args, **kwargs)
                # 成功执行，清除重试计数
                self._clear_retry_count(step_id, operation)
                return {"success": True, "result": result}
                
            except Exception as e:
                recovery_plan = self.handle_exception(e, step_id, operation)
                
                if recovery_plan["action"] == RecoveryAction.STOP.value:
                    return {
                        "success": False,
                        "error": str(e),
                        "recovery_plan": recovery_plan
                    }
                elif recovery_plan["action"] == RecoveryAction.SKIP.value:
                    return {
                        "success": False,
                        "skipped": True,
                        "error": str(e),
                        "recovery_plan": recovery_plan
                    }
                elif recovery_plan["action"] == RecoveryAction.CONTINUE.value:
                    return {
                        "success": False,
                        "continued": True,
                        "error": str(e),
                        "recovery_plan": recovery_plan
                    }
                elif recovery_plan["should_retry"]:
                    if recovery_plan["delay"] > 0:
                        time.sleep(recovery_plan["delay"])
                    continue  # 重试
                else:
                    return {
                        "success": False,
                        "error": str(e),
                        "recovery_plan": recovery_plan
                    }
    
    def _clear_retry_count(self, step_id: str = None, operation: str = None):
        """清除重试计数"""
        if step_id:
            keys_to_remove = [key for key in self.retry_counts.keys() if key.startswith(step_id)]
            for key in keys_to_remove:
                del self.retry_counts[key]
    
    def set_recovery_strategy(self, error_type: ErrorType, strategy: Dict[str, Any]):
        """设置恢复策略"""
        self.recovery_strategies[error_type] = strategy
    
    def get_error_statistics(self) -> Dict[str, Any]:
        """获取错误统计"""
        if not self.error_history:
            return {"total_errors": 0}
        
        error_counts = {}
        for error in self.error_history:
            error_type = error["error_type"]
            error_counts[error_type] = error_counts.get(error_type, 0) + 1
        
        return {
            "total_errors": len(self.error_history),
            "error_counts": error_counts,
            "recent_errors": self.error_history[-10:],
            "most_common_error": max(error_counts.items(), key=lambda x: x[1])[0] if error_counts else None
        }
    
    def clear_error_history(self):
        """清除错误历史"""
        self.error_history.clear()
        self.retry_counts.clear()
    
    def export_error_report(self, file_path: str = None) -> str:
        """导出错误报告"""
        import json
        
        if not file_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = f"error_report_{timestamp}.json"
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "statistics": self.get_error_statistics(),
            "error_history": self.error_history,
            "recovery_strategies": {
                error_type.value: strategy 
                for error_type, strategy in self.recovery_strategies.items()
            }
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        return file_path

# 全局异常处理装饰器
def handle_rpa_exceptions(logger=None):
    """RPA异常处理装饰器"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            handler = RPAExceptionHandler(logger)
            return handler.execute_with_recovery(func, *args, **kwargs)
        return wrapper
    return decorator

# 常用异常处理函数
def safe_execute(func: Callable, *args, logger=None, **kwargs) -> Dict[str, Any]:
    """安全执行函数"""
    handler = RPAExceptionHandler(logger)
    return handler.execute_with_recovery(func, *args, **kwargs)
