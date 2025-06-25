#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AdsPower样式的调试日志对话框
根据用户提供的截图完全复制AdsPower的调试日志格式
"""

import sys
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QTextEdit, QWidget, QApplication, QScrollArea)
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtGui import QFont, QTextCursor

# 导入iOS 26样式管理器
try:
    from ios26_style_manager import iOS26StyleManager
except ImportError:
    # 如果导入失败，创建简化版本
    class iOS26StyleManager:
        @classmethod
        def get_complete_style(cls):
            return ""
        @classmethod
        def get_button_style(cls, variant='primary'):
            return ""
        @classmethod
        def get_input_style(cls):
            return ""

class DebugLogDialog(QDialog):
    """AdsPower样式的调试日志对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.log_entries = []
        self.init_ui()
        # 不再自动开始演示日志记录，保持初始状态为空白
        
    def init_ui(self):
        """初始化界面 - iOS 26 Liquid Glass风格"""
        self.setWindowTitle("📋 调试日志")
        self.setFixedSize(800, 600)  # 优化对话框尺寸

        # 应用统一的iOS 26风格样式
        self.setStyleSheet(iOS26StyleManager.get_complete_style())
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # 标题区域
        self.create_title_section(layout)
        
        # 日志显示区域
        self.create_log_section(layout)
        
        # 按钮区域
        self.create_buttons_section(layout)
        
    def create_title_section(self, parent_layout):
        """创建标题区域"""
        title_widget = QWidget()
        title_layout = QHBoxLayout(title_widget)
        title_layout.setContentsMargins(0, 0, 0, 0)
        
        # 执行统计 - 初始状态为空
        self.stats_label = QLabel("0 执行 0 日志")
        self.stats_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: 600;
                color: #333333;
            }
        """)
        title_layout.addWidget(self.stats_label)
        
        title_layout.addStretch()
        
        parent_layout.addWidget(title_widget)
        
    def create_log_section(self, parent_layout):
        """创建日志显示区域"""
        # 日志文本区域 - iOS 26风格
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.9),
                    stop:1 rgba(255, 255, 255, 0.7));
                border: 1px solid rgba(0, 122, 255, 0.1);
                border-radius: 16px;
                padding: 20px;
                font-family: "SF Mono", "Monaco", "Consolas", "Courier New", monospace;
                font-size: 13px;
                line-height: 1.5;
                color: rgba(28, 28, 30, 0.9);
                backdrop-filter: blur(20px);
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
            }
        """ + iOS26StyleManager.get_scrollbar_style())
        
        # 设置初始日志内容
        self.init_log_content()
        
        parent_layout.addWidget(self.log_text)
        
    def create_buttons_section(self, parent_layout):
        """创建按钮区域"""
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # 清空日志按钮
        clear_btn = QPushButton("清空日志")
        clear_btn.setFixedSize(120, 44)
        clear_btn.setStyleSheet(iOS26StyleManager.get_button_style('secondary'))
        clear_btn.clicked.connect(self.clear_logs)
        button_layout.addWidget(clear_btn)

        button_layout.addSpacing(12)

        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.setFixedSize(100, 44)
        close_btn.setStyleSheet(iOS26StyleManager.get_button_style('primary'))
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)
        
        parent_layout.addLayout(button_layout)
        
    def init_log_content(self):
        """初始化日志内容 - 保持空白状态"""
        # 初始状态为空白，不设置任何预设内容
        self.log_text.clear()
        
    def add_log_entry(self, message, log_type="info"):
        """添加日志条目"""
        timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        
        # 根据日志类型设置颜色
        color_map = {
            "info": "#333333",
            "success": "#52c41a", 
            "warning": "#faad14",
            "error": "#ff4d4f"
        }
        
        color = color_map.get(log_type, "#333333")
        
        # 格式化日志条目
        log_entry = f"[ {timestamp} ] {message}"
        
        # 添加到文本区域
        cursor = self.log_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(f"\n{log_entry}")
        
        # 滚动到底部
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
        # 更新统计
        self.update_stats()
        
    def update_stats(self):
        """更新执行统计"""
        lines = self.log_text.toPlainText().split('\n')
        log_count = len([line for line in lines if line.strip()])
        execution_count = len([line for line in lines if '执行' in line or '访问' in line or '点击' in line])
        
        self.stats_label.setText(f"{execution_count} 执行 {log_count} 日志")
        
    def clear_logs(self):
        """清空日志"""
        self.log_text.clear()
        self.stats_label.setText("0 执行 0 日志")

    def add_log(self, message, log_type="info"):
        """添加日志条目"""
        timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        log_entry = f"[ {timestamp} ] {message}"

        # 添加到日志文本框
        self.log_text.append(log_entry)

        # 更新统计
        self.update_stats()
        
    def start_demo_logging(self):
        """开始演示日志记录"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.add_demo_log)
        self.demo_logs = [
            ("检测页面加载状态", "info"),
            ("页面加载完成", "success"),
            ("开始执行点击操作", "info"),
            ("点击操作执行成功", "success"),
            ("等待页面响应", "info"),
            ("页面响应正常", "success"),
            ("任务执行完成", "success")
        ]
        self.demo_index = 0
        
        # 每3秒添加一条演示日志
        self.timer.start(3000)
        
    def add_demo_log(self):
        """添加演示日志"""
        if self.demo_index < len(self.demo_logs):
            message, log_type = self.demo_logs[self.demo_index]
            self.add_log_entry(message, log_type)
            self.demo_index += 1
        else:
            self.timer.stop()
            
    def closeEvent(self, event):
        """关闭事件 - 优化资源清理"""
        self.cleanup_resources()
        event.accept()

    def cleanup_resources(self):
        """清理资源"""
        try:
            if hasattr(self, 'timer') and self.timer:
                self.timer.stop()
                self.timer = None

            # 清理日志条目，释放内存
            if hasattr(self, 'log_entries'):
                self.log_entries.clear()

        except Exception as e:
            print(f"[调试日志对话框] 清理资源时出错: {e}")

    def __del__(self):
        """析构函数"""
        try:
            self.cleanup_resources()
        except:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    dialog = DebugLogDialog()
    dialog.show()
    
    sys.exit(app.exec_())
