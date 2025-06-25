#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AdsPower样式的调试对话框
根据用户提供的截图完全复制AdsPower的调试界面
"""

import sys
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QLineEdit, QWidget, QApplication, QComboBox,
                             QProgressBar, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

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

class DebugDialog(QDialog):
    """AdsPower样式的调试对话框 - 优化资源管理"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._resources_cleaned = False
        self.init_ui()
        
    def init_ui(self):
        """初始化界面 - iOS 26 Liquid Glass风格"""
        self.setWindowTitle("🐛 调试")
        self.setFixedSize(600, 400)  # 优化对话框尺寸

        # 应用统一的iOS 26风格样式
        self.setStyleSheet(iOS26StyleManager.get_complete_style())

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)  # 调整边距
        layout.setSpacing(15)  # 调整间距
        
        # 编号/ID输入区域
        self.create_id_input_section(layout)
        
        # 温馨提示区域
        self.create_tips_section(layout)
        
        # 按钮区域
        self.create_buttons_section(layout)
        
    def create_id_input_section(self, parent_layout):
        """创建编号/ID输入区域"""
        # 标签
        id_label = QLabel("编号/ID")
        id_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: 500;
                color: #333333;
                margin-bottom: 8px;
            }
        """)
        parent_layout.addWidget(id_label)

        # 输入框
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("请输入环境ID（如：knhoewu，非数字编号）")
        self.id_input.setText("")
        self.id_input.setFixedHeight(44)
        self.id_input.setStyleSheet(iOS26StyleManager.get_input_style())
        parent_layout.addWidget(self.id_input)
        
    def create_tips_section(self, parent_layout):
        """创建温馨提示区域"""
        # 提示容器 - iOS 26风格
        tips_container = QWidget()
        tips_container.setFixedHeight(140)
        tips_container.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(0, 122, 255, 0.08),
                    stop:1 rgba(0, 122, 255, 0.05));
                border: 1px solid rgba(0, 122, 255, 0.15);
                border-radius: 16px;
                padding: 16px;
                backdrop-filter: blur(20px);
                box-shadow: 0 4px 20px rgba(0, 122, 255, 0.1);
            }
        """)

        tips_layout = QVBoxLayout(tips_container)
        tips_layout.setContentsMargins(12, 12, 12, 12)  # 调整边距
        tips_layout.setSpacing(6)  # 调整间距
        
        # 温馨提示标题
        tips_title = QLabel("温馨提示:")
        tips_title.setStyleSheet("""
            QLabel {
                font-size: 13px;
                font-weight: 600;
                color: #333333;
                margin-bottom: 4px;
            }
        """)
        tips_layout.addWidget(tips_title)

        # 提示内容1 - 环境ID说明
        tip1 = QLabel("1. 请输入环境ID（如：knhoewu），不是环境编号。环境ID可在AdsPower环境管理页面查看")
        tip1.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #666666;
                line-height: 1.4;
                margin-left: 8px;
                padding: 2px 0px;
            }
        """)
        tip1.setWordWrap(True)
        tips_layout.addWidget(tip1)

        # 提示内容2
        tip2 = QLabel("2. 当前设备未执行任何RPA任务流程时，可以成功使用调试功能调试的任务流程")
        tip2.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #666666;
                line-height: 1.4;
                margin-left: 8px;
                padding: 2px 0px;
            }
        """)
        tip2.setWordWrap(True)
        tips_layout.addWidget(tip2)

        # 提示内容3
        tip3 = QLabel("3. 点击调试按钮当前设备RPA任务流程运行，并创建条件流程运行至全部条件执行完成")
        tip3.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #666666;
                line-height: 1.4;
                margin-left: 8px;
                padding: 2px 0px;
            }
        """)
        tip3.setWordWrap(True)
        tips_layout.addWidget(tip3)
        
        parent_layout.addWidget(tips_container)
        
    def create_buttons_section(self, parent_layout):
        """创建按钮区域"""
        # 添加弹性空间
        parent_layout.addStretch()
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # 取消按钮
        cancel_btn = QPushButton("取消")
        cancel_btn.setFixedSize(100, 44)
        cancel_btn.setStyleSheet(iOS26StyleManager.get_button_style('secondary'))
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)

        button_layout.addSpacing(12)

        # 确定按钮
        confirm_btn = QPushButton("确定")
        confirm_btn.setFixedSize(100, 44)
        confirm_btn.setStyleSheet(iOS26StyleManager.get_button_style('primary'))
        confirm_btn.clicked.connect(self.start_debug)
        button_layout.addWidget(confirm_btn)
        
        parent_layout.addLayout(button_layout)
        
    def start_debug(self):
        """开始调试"""
        env_id = self.id_input.text().strip()

        if not env_id:
            QMessageBox.warning(self, "警告", "请输入环境ID")
            return

        # 验证环境ID格式（AdsPower环境ID通常是字母数字组合，不是纯数字）
        if env_id.isdigit():
            reply = QMessageBox.question(self, "确认",
                f"您输入的是数字编号 '{env_id}'，但AdsPower API需要环境ID（字母数字组合）。\n\n"
                "如果您确定这是正确的环境ID，请点击'是'继续。\n"
                "如果这是环境编号，请点击'否'重新输入环境ID。",
                QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.No:
                return

        # 关闭对话框并返回成功
        self.accept()

    def get_env_id(self):
        """获取输入的环境ID"""
        return self.id_input.text().strip()

    def closeEvent(self, event):
        """关闭事件 - 清理资源"""
        self.cleanup_resources()
        event.accept()

    def cleanup_resources(self):
        """清理资源"""
        if self._resources_cleaned:
            return

        try:
            # 清理可能的定时器或其他资源
            if hasattr(self, 'timer') and self.timer:
                self.timer.stop()

            self._resources_cleaned = True

        except Exception as e:
            print(f"[调试对话框] 清理资源时出错: {e}")

    def __del__(self):
        """析构函数"""
        self.cleanup_resources()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    dialog = DebugDialog()
    if dialog.exec_() == QDialog.Accepted:
        print(f"调试环境ID: {dialog.get_env_id()}")
    
    sys.exit(app.exec_())
