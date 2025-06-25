#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RPA流程管理界面 - 完全按照AdsPower原版设计
"""

import json
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QComboBox, QLineEdit, QCheckBox, QScrollArea,
                             QFrame, QGridLayout, QApplication, QMenu, QAction,
                             QSpinBox, QFormLayout, QWidget, QMessageBox)
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QFont, QIcon

# 导入AdsPower样式管理器
try:
    from adspower_style_manager import AdsPowerStyleManager as iOS26StyleManager
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
        @classmethod
        def get_table_style(cls):
            return ""


class RPATaskCard(QFrame):
    """RPA任务卡片 - 按照截图设计"""
    
    def __init__(self, task_id, task_name="暂无备注", parent=None):
        super().__init__(parent)
        self.task_id = task_id
        self.task_name = task_name
        self.init_ui()
        
    def init_ui(self):
        """初始化卡片界面 - iOS 26风格"""
        self.setFixedSize(200, 120)
        self.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.9),
                    stop:1 rgba(255, 255, 255, 0.7));
                border: 1px solid rgba(0, 122, 255, 0.1);
                border-radius: 16px;
                backdrop-filter: blur(30px);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
                margin: 8px;
            }
            QFrame:hover {
                border: 1px solid rgba(0, 122, 255, 0.3);
                box-shadow: 0 12px 40px rgba(0, 122, 255, 0.15);
                transform: translateY(-2px);
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        
        # 顶部：复选框和任务ID
        top_layout = QHBoxLayout()
        
        self.checkbox = QCheckBox()
        self.checkbox.setStyleSheet("""
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid rgba(0, 122, 255, 0.3);
                border-radius: 6px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.9),
                    stop:1 rgba(255, 255, 255, 0.7));
                backdrop-filter: blur(10px);
            }
            QCheckBox::indicator:checked {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(0, 122, 255, 0.9),
                    stop:1 rgba(0, 122, 255, 0.7));
                border-color: rgba(0, 122, 255, 0.8);
                box-shadow: 0 2px 8px rgba(0, 122, 255, 0.3);
            }
            QCheckBox::indicator:hover {
                border-color: rgba(0, 122, 255, 0.5);
                box-shadow: 0 0 0 2px rgba(0, 122, 255, 0.1);
            }
        """)
        
        task_id_label = QLabel(str(self.task_id))
        task_id_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333;")
        
        top_layout.addWidget(self.checkbox)
        top_layout.addWidget(task_id_label)
        top_layout.addStretch()
        
        # 中间：任务名称
        self.name_label = QLabel(self.task_name)
        self.name_label.setStyleSheet("font-size: 12px; color: #666; margin: 8px 0;")
        self.name_label.setWordWrap(True)
        
        # 底部：操作按钮
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        
        # 编辑按钮
        edit_btn = QPushButton("✏")
        edit_btn.setFixedSize(24, 24)
        edit_btn.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        
        # 更多按钮
        more_btn = QPushButton("⋯")
        more_btn.setFixedSize(24, 24)
        more_btn.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        
        bottom_layout.addWidget(edit_btn)
        bottom_layout.addWidget(more_btn)
        
        layout.addLayout(top_layout)
        layout.addWidget(self.name_label)
        layout.addStretch()
        layout.addLayout(bottom_layout)
        
        # 连接信号
        more_btn.clicked.connect(self.show_context_menu)
        
    def show_context_menu(self):
        """显示右键菜单"""
        menu = QMenu(self)
        
        copy_action = QAction("复制模板", self)
        export_action = QAction("导出", self)
        top_action = QAction("置顶", self)
        delete_action = QAction("删除", self)
        
        menu.addAction(copy_action)
        menu.addAction(export_action)
        menu.addAction(top_action)
        menu.addSeparator()
        menu.addAction(delete_action)
        
        # 显示菜单
        menu.exec_(self.mapToGlobal(self.rect().bottomRight()))


class RPAProcessDialog(QDialog):
    """RPA流程管理主界面 - 完全按照截图设计"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tasks = []
        self.thread_count = 3
        self.init_ui()
        
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("流程管理")
        self.setFixedSize(800, 600)  # 大型对话框标准尺寸

        # 应用统一的iOS 26 Liquid Glass风格
        self.setStyleSheet(iOS26StyleManager.get_complete_style())
        
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 顶部工具栏
        toolbar_layout = QHBoxLayout()
        
        # 创建任务流程按钮
        create_btn = QPushButton("+ 创建任务流程")
        create_btn.setStyleSheet(iOS26StyleManager.get_button_style('primary'))
        create_btn.clicked.connect(self.create_new_task)
        
        # 全选下拉框
        select_combo = QComboBox()
        select_combo.addItems(["全部", "已选择", "未选择"])
        select_combo.setStyleSheet(iOS26StyleManager.get_input_style())

        # 搜索框
        search_edit = QLineEdit()
        search_edit.setPlaceholderText("搜索我的任务流程")
        search_edit.setStyleSheet(iOS26StyleManager.get_input_style())
        
        # 右侧按钮组 - iOS 26风格
        refresh_btn = QPushButton("🔄")
        refresh_btn.setFixedSize(40, 40)
        refresh_btn.setStyleSheet(iOS26StyleManager.get_button_style('secondary'))

        export_btn = QPushButton("📤")
        export_btn.setFixedSize(40, 40)
        export_btn.setStyleSheet(iOS26StyleManager.get_button_style('secondary'))

        delete_btn = QPushButton("🗑")
        delete_btn.setFixedSize(40, 40)
        delete_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 59, 48, 0.9),
                    stop:1 rgba(255, 59, 48, 0.8));
                color: rgba(255, 255, 255, 0.95);
                border: none;
                border-radius: 12px;
                font-size: 16px;
                backdrop-filter: blur(20px);
                box-shadow: 0 4px 20px rgba(255, 59, 48, 0.2);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 59, 48, 1.0),
                    stop:1 rgba(255, 59, 48, 0.9));
                box-shadow: 0 6px 25px rgba(255, 59, 48, 0.3);
                transform: translateY(-1px);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 59, 48, 0.8),
                    stop:1 rgba(255, 59, 48, 0.7));
                transform: translateY(1px);
            }
        """)
        delete_btn.clicked.connect(self.delete_selected_tasks)

        settings_btn = QPushButton("⚙")
        settings_btn.setFixedSize(40, 40)
        settings_btn.setStyleSheet(iOS26StyleManager.get_button_style('secondary'))
        settings_btn.clicked.connect(self.show_settings)
        
        toolbar_layout.addWidget(create_btn)
        toolbar_layout.addWidget(QLabel(""))
        toolbar_layout.addWidget(select_combo)
        toolbar_layout.addWidget(search_edit)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(refresh_btn)
        toolbar_layout.addWidget(export_btn)
        toolbar_layout.addWidget(delete_btn)
        toolbar_layout.addWidget(settings_btn)
        
        main_layout.addLayout(toolbar_layout)
        
        # 全选区域
        select_all_layout = QHBoxLayout()
        self.select_all_checkbox = QCheckBox("全选")
        self.select_all_checkbox.setStyleSheet("""
            QCheckBox {
                font-size: 13px;
                color: #666;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 2px solid #ccc;
                border-radius: 3px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #0868f7;
                border-color: #0868f7;
            }
        """)
        
        # 创建流程数统计
        self.count_label = QLabel("创建流程数: 0 / 500")
        self.count_label.setStyleSheet("font-size: 13px; color: #666;")
        
        select_all_layout.addWidget(self.select_all_checkbox)
        select_all_layout.addStretch()
        select_all_layout.addWidget(self.count_label)
        
        main_layout.addLayout(select_all_layout)
        
        # 任务卡片区域
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #f8f9fa;
            }
        """)
        
        # 卡片容器
        self.cards_widget = QWidget()
        self.cards_layout = QGridLayout(self.cards_widget)
        self.cards_layout.setSpacing(10)
        
        # 空状态显示
        self.empty_widget = QWidget()
        empty_layout = QVBoxLayout(self.empty_widget)
        empty_layout.setAlignment(Qt.AlignCenter)
        
        empty_icon = QLabel("🤖")
        empty_icon.setAlignment(Qt.AlignCenter)
        empty_icon.setStyleSheet("font-size: 48px; margin: 20px;")
        
        empty_text = QLabel("暂无数据")
        empty_text.setAlignment(Qt.AlignCenter)
        empty_text.setStyleSheet("font-size: 16px; color: #999; margin: 10px;")
        
        create_empty_btn = QPushButton("+ 创建任务流程")
        create_empty_btn.setStyleSheet("""
            QPushButton {
                background-color: #0868f7;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0654d3;
            }
        """)
        create_empty_btn.clicked.connect(self.create_new_task)
        
        empty_layout.addWidget(empty_icon)
        empty_layout.addWidget(empty_text)
        empty_layout.addWidget(create_empty_btn)
        
        # 默认显示空状态
        self.scroll_area.setWidget(self.empty_widget)
        main_layout.addWidget(self.scroll_area)
        
        # 连接信号
        self.select_all_checkbox.stateChanged.connect(self.toggle_select_all)

    def create_new_task(self):
        """创建新任务"""
        # 创建简单的任务创建对话框
        dialog = QDialog(self)
        dialog.setWindowTitle("创建任务流程")
        dialog.setFixedSize(400, 300)  # 小对话框标准尺寸

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(20, 20, 20, 20)

        # 任务名称输入
        form_layout = QFormLayout()
        name_edit = QLineEdit()
        name_edit.setPlaceholderText("请输入任务名称")
        name_edit.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 13px;
            }
        """)
        form_layout.addRow("任务名称:", name_edit)
        layout.addLayout(form_layout)

        # 按钮
        button_layout = QHBoxLayout()

        confirm_btn = QPushButton("确定")
        confirm_btn.setStyleSheet("""
            QPushButton {
                background-color: #0868f7;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-size: 13px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #0654d3;
            }
        """)

        cancel_btn = QPushButton("取消")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #f8f9fa;
                color: #333;
                border: 1px solid #ddd;
                padding: 10px 20px;
                border-radius: 4px;
                font-size: 13px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #e9ecef;
            }
        """)

        button_layout.addStretch()
        button_layout.addWidget(confirm_btn)
        button_layout.addWidget(cancel_btn)

        layout.addStretch()
        layout.addLayout(button_layout)

        # 连接信号
        def create_task():
            task_name = name_edit.text().strip()
            if not task_name:
                task_name = "暂无备注"
            self.add_task_card(len(self.tasks) + 1, task_name)
            dialog.accept()

        confirm_btn.clicked.connect(create_task)
        cancel_btn.clicked.connect(dialog.reject)

        dialog.exec_()

    def add_task_card(self, task_id, task_name):
        """添加任务卡片"""
        card = RPATaskCard(task_id, task_name)
        self.tasks.append(card)

        # 如果是第一个任务，切换到卡片视图
        if len(self.tasks) == 1:
            self.scroll_area.setWidget(self.cards_widget)

        # 计算网格位置
        row = (len(self.tasks) - 1) // 4
        col = (len(self.tasks) - 1) % 4
        self.cards_layout.addWidget(card, row, col)

        # 更新计数
        self.update_count_label()

    def delete_selected_tasks(self):
        """删除选中的任务"""
        selected_tasks = []
        for task in self.tasks:
            if task.checkbox.isChecked():
                selected_tasks.append(task)

        if not selected_tasks:
            QMessageBox.information(self, "提示", "请先选择要删除的任务")
            return

        reply = QMessageBox.question(self, "确认删除",
                                   f"确定要删除选中的 {len(selected_tasks)} 个任务吗？",
                                   QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            for task in selected_tasks:
                self.cards_layout.removeWidget(task)
                task.deleteLater()
                self.tasks.remove(task)

            # 重新排列剩余卡片
            self.rearrange_cards()
            self.update_count_label()

            # 如果没有任务了，显示空状态
            if not self.tasks:
                self.scroll_area.setWidget(self.empty_widget)

    def rearrange_cards(self):
        """重新排列卡片"""
        for i, task in enumerate(self.tasks):
            row = i // 4
            col = i % 4
            self.cards_layout.addWidget(task, row, col)

    def toggle_select_all(self, state):
        """切换全选状态"""
        checked = state == Qt.Checked
        for task in self.tasks:
            task.checkbox.setChecked(checked)

    def update_count_label(self):
        """更新计数标签"""
        self.count_label.setText(f"创建流程数: {len(self.tasks)} / 500")

    def show_settings(self):
        """显示设置对话框"""
        dialog = QDialog(self)
        dialog.setWindowTitle("个人设置")
        dialog.setFixedSize(400, 200)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(30, 30, 30, 30)

        # 任务线程数设置
        form_layout = QFormLayout()

        thread_spin = QSpinBox()
        thread_spin.setRange(1, 500)
        thread_spin.setValue(self.thread_count)
        thread_spin.setStyleSheet("""
            QSpinBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 13px;
                min-width: 100px;
            }
        """)

        form_layout.addRow("任务线程数:", thread_spin)
        layout.addLayout(form_layout)

        # 按钮
        button_layout = QHBoxLayout()

        confirm_btn = QPushButton("确定")
        confirm_btn.setStyleSheet("""
            QPushButton {
                background-color: #0868f7;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-size: 13px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #0654d3;
            }
        """)

        cancel_btn = QPushButton("取消")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #f8f9fa;
                color: #333;
                border: 1px solid #ddd;
                padding: 10px 20px;
                border-radius: 4px;
                font-size: 13px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #e9ecef;
            }
        """)

        button_layout.addStretch()
        button_layout.addWidget(confirm_btn)
        button_layout.addWidget(cancel_btn)

        layout.addStretch()
        layout.addLayout(button_layout)

        # 连接信号
        def save_settings():
            self.thread_count = thread_spin.value()
            dialog.accept()

        confirm_btn.clicked.connect(save_settings)
        cancel_btn.clicked.connect(dialog.reject)

        dialog.exec_()


# 简化的脚本编辑对话框
class RPAScriptDialog(QDialog):
    """简化的RPA脚本编辑对话框"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("RPA脚本编辑器")
        self.setFixedSize(600, 400)

        layout = QVBoxLayout(self)

        # 简单的文本编辑器
        from PyQt5.QtWidgets import QTextEdit
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("请输入RPA脚本内容...")
        layout.addWidget(self.text_edit)

        # 按钮
        button_layout = QHBoxLayout()

        save_btn = QPushButton("保存")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #0868f7;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #0654d3;
            }
        """)

        cancel_btn = QPushButton("取消")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #f8f9fa;
                color: #333;
                border: 1px solid #ddd;
                padding: 10px 20px;
                border-radius: 4px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #e9ecef;
            }
        """)

        button_layout.addStretch()
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)

        layout.addLayout(button_layout)

        # 连接信号
        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
