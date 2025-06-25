#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
错误处理和日志记录模块
提供统一的错误处理和用户友好的错误提示
"""

import os
import sys
import traceback
import logging
from datetime import datetime

# 尝试导入PyQt5，如果失败则使用占位符
try:
    from PyQt5.QtWidgets import QMessageBox, QApplication
    from PyQt5.QtCore import QObject, pyqtSignal
    PYQT5_AVAILABLE = True
except ImportError:
    PYQT5_AVAILABLE = False
    # 创建占位符类
    class QObject:
        def __init__(self):
            pass

    def pyqtSignal(*args):
        def dummy_signal(*args, **kwargs):
            pass
        return dummy_signal

class ErrorHandler(QObject):
    """统一错误处理器"""
    
    error_occurred = pyqtSignal(str, str)  # 错误类型, 错误消息
    
    def __init__(self):
        super().__init__()
        self.setup_logging()
        
    def setup_logging(self):
        """设置日志记录"""
        try:
            # 确保logs目录存在
            logs_dir = "logs"
            if not os.path.exists(logs_dir):
                os.makedirs(logs_dir)
            
            # 设置日志文件
            log_file = os.path.join(logs_dir, f"adspower_tool_{datetime.now().strftime('%Y%m%d')}.log")
            
            # 配置日志格式
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler(log_file, encoding='utf-8'),
                    logging.StreamHandler(sys.stdout)
                ]
            )
            
            self.logger = logging.getLogger(__name__)
            self.logger.info("错误处理器初始化完成")
            
        except Exception as e:
            print(f"日志系统初始化失败: {e}")
            self.logger = None
    
    def handle_exception(self, exc_type, exc_value, exc_traceback, context="未知"):
        """处理异常"""
        try:
            # 记录详细错误信息
            error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
            
            if self.logger:
                self.logger.error(f"[{context}] 发生异常: {error_msg}")
            else:
                print(f"[{context}] 发生异常: {error_msg}")
            
            # 生成用户友好的错误消息
            user_msg = self.get_user_friendly_message(exc_type, exc_value, context)
            
            # 发送错误信号
            self.error_occurred.emit(context, user_msg)
            
            # 显示错误对话框
            self.show_error_dialog(context, user_msg, str(exc_value))
            
        except Exception as e:
            print(f"错误处理器本身发生错误: {e}")
    
    def get_user_friendly_message(self, exc_type, exc_value, context):
        """生成用户友好的错误消息"""
        error_messages = {
            'ModuleNotFoundError': {
                'PyQt5': '界面库未安装，请运行"安装依赖.bat"或手动安装PyQt5',
                'requests': '网络库未安装，请运行"安装依赖.bat"或手动安装requests',
                'selenium': 'RPA库未安装，请运行"安装依赖.bat"或手动安装selenium',
                'default': '缺少必要的程序库，请检查依赖安装'
            },
            'ConnectionError': '网络连接失败，请检查网络设置或AdsPower是否正在运行',
            'TimeoutError': '操作超时，请检查网络连接或重试',
            'PermissionError': '权限不足，请以管理员身份运行程序',
            'FileNotFoundError': '找不到必要的文件，请检查程序完整性',
            'default': '程序运行出现问题，请查看详细错误信息'
        }
        
        exc_name = exc_type.__name__
        
        if exc_name == 'ModuleNotFoundError':
            module_name = str(exc_value).split("'")[1] if "'" in str(exc_value) else 'unknown'
            return error_messages['ModuleNotFoundError'].get(module_name, 
                   error_messages['ModuleNotFoundError']['default'])
        
        return error_messages.get(exc_name, error_messages['default'])
    
    def show_error_dialog(self, context, user_msg, technical_msg):
        """显示错误对话框"""
        try:
            if not PYQT5_AVAILABLE:
                print(f"[{context}] {user_msg}")
                print(f"技术详情: {technical_msg}")
                return

            app = QApplication.instance()
            if app is None:
                print(f"[{context}] {user_msg}")
                print(f"技术详情: {technical_msg}")
                return

            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setWindowTitle(f"错误 - {context}")
            msg_box.setText(user_msg)
            msg_box.setDetailedText(f"技术详情:\n{technical_msg}")
            msg_box.setStandardButtons(QMessageBox.Ok)
            
            # 设置样式
            msg_box.setStyleSheet("""
                QMessageBox {
                    background-color: #ffffff;
                    font-family: "Microsoft YaHei", Arial, sans-serif;
                    font-size: 14px;
                }
                QMessageBox QPushButton {
                    background-color: #1890ff;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    min-width: 80px;
                }
                QMessageBox QPushButton:hover {
                    background-color: #40a9ff;
                }
            """)
            
            msg_box.exec_()
            
        except Exception as e:
            print(f"显示错误对话框失败: {e}")
            print(f"原始错误: [{context}] {user_msg}")
    
    def log_info(self, message, context="信息"):
        """记录信息日志"""
        if self.logger:
            self.logger.info(f"[{context}] {message}")
        else:
            print(f"[{context}] {message}")
    
    def log_warning(self, message, context="警告"):
        """记录警告日志"""
        if self.logger:
            self.logger.warning(f"[{context}] {message}")
        else:
            print(f"[{context}] {message}")
    
    def log_error(self, message, context="错误"):
        """记录错误日志"""
        if self.logger:
            self.logger.error(f"[{context}] {message}")
        else:
            print(f"[{context}] {message}")

# 全局错误处理器实例
global_error_handler = ErrorHandler()

def setup_global_exception_handler():
    """设置全局异常处理器"""
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        
        global_error_handler.handle_exception(exc_type, exc_value, exc_traceback, "全局异常")
    
    sys.excepthook = handle_exception

def log_info(message, context="信息"):
    """便捷的信息日志记录函数"""
    global_error_handler.log_info(message, context)

def log_warning(message, context="警告"):
    """便捷的警告日志记录函数"""
    global_error_handler.log_warning(message, context)

def log_error(message, context="错误"):
    """便捷的错误日志记录函数"""
    global_error_handler.log_error(message, context)

def handle_api_error(result, operation="API操作"):
    """处理API错误响应"""
    if result.get("code") != 0:
        error_msg = result.get("msg", "未知错误")
        log_error(f"{operation}失败: {error_msg}", "API错误")
        return False, error_msg
    return True, "成功"

def safe_execute(func, *args, context="操作", **kwargs):
    """安全执行函数，自动处理异常"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        global_error_handler.handle_exception(type(e), e, e.__traceback__, context)
        return None
