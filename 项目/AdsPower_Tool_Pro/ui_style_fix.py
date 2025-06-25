#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UI样式修复模块
修复界面显示问题，统一字体大小和按钮尺寸
"""

def apply_adspower_style_fixes():
    """应用AdsPower风格的UI修复"""
    return """
        /* AdsPower标准样式修复 */
        
        /* 统一字体系统 */
        * {
            font-family: "Microsoft YaHei", "PingFang SC", "Helvetica Neue", Arial, sans-serif;
        }
        
        /* 主窗口样式 */
        QMainWindow {
            background-color: #f5f5f5;
            font-size: 14px;
        }
        
        /* 统一按钮样式 */
        QPushButton {
            background-color: #1890ff;
            color: #ffffff;
            border: 1px solid #1890ff;
            border-radius: 4px;
            height: 32px;
            padding: 0 15px;
            font-size: 14px;
            font-weight: 400;
            min-width: 64px;
        }
        
        QPushButton:hover {
            background-color: #40a9ff;
            border-color: #40a9ff;
        }
        
        QPushButton:pressed {
            background-color: #096dd9;
            border-color: #096dd9;
        }
        
        /* 次要按钮样式 */
        QPushButton[class="secondary"] {
            background-color: #ffffff;
            color: #262626;
            border: 1px solid #d9d9d9;
        }
        
        QPushButton[class="secondary"]:hover {
            color: #1890ff;
            border-color: #1890ff;
        }
        
        /* 成功按钮样式 */
        QPushButton[class="success"] {
            background-color: #52c41a;
            border-color: #52c41a;
        }
        
        QPushButton[class="success"]:hover {
            background-color: #73d13d;
            border-color: #73d13d;
        }
        
        /* 危险按钮样式 */
        QPushButton[class="danger"] {
            background-color: #ff4d4f;
            border-color: #ff4d4f;
        }
        
        QPushButton[class="danger"]:hover {
            background-color: #ff7875;
            border-color: #ff7875;
        }
        
        /* 统一输入框样式 */
        QLineEdit, QComboBox, QSpinBox {
            background-color: #ffffff;
            border: 1px solid #d9d9d9;
            border-radius: 4px;
            height: 32px;
            padding: 6px 11px;
            font-size: 14px;
            color: #262626;
        }
        
        QLineEdit:hover, QComboBox:hover, QSpinBox:hover {
            border-color: #40a9ff;
        }
        
        QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
            border-color: #1890ff;
            outline: none;
        }
        
        /* 统一表格样式 */
        QTableWidget {
            background-color: #ffffff;
            border: 1px solid #d9d9d9;
            border-radius: 4px;
            gridline-color: #f0f0f0;
            font-size: 14px;
        }
        
        QTableWidget::item {
            padding: 8px;
            border-bottom: 1px solid #f0f0f0;
        }
        
        QTableWidget::item:selected {
            background-color: #e6f7ff;
            color: #1890ff;
        }
        
        QHeaderView::section {
            background-color: #fafafa;
            color: #262626;
            padding: 8px;
            border: none;
            border-bottom: 1px solid #d9d9d9;
            font-weight: 500;
            font-size: 14px;
        }
        
        /* 统一标签样式 */
        QLabel {
            color: #262626;
            font-size: 14px;
        }
        
        /* 分组框样式 */
        QGroupBox {
            font-size: 14px;
            font-weight: 500;
            color: #262626;
            border: 1px solid #d9d9d9;
            border-radius: 4px;
            margin-top: 8px;
            padding-top: 8px;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 8px;
            padding: 0 4px;
            background-color: #f5f5f5;
        }
        
        /* 菜单样式 */
        QMenuBar {
            background-color: #ffffff;
            border-bottom: 1px solid #d9d9d9;
            font-size: 14px;
            color: #262626;
        }
        
        QMenuBar::item {
            background-color: transparent;
            padding: 8px 16px;
        }
        
        QMenuBar::item:selected {
            background-color: #f0f0f0;
        }
        
        QMenu {
            background-color: #ffffff;
            border: 1px solid #d9d9d9;
            border-radius: 4px;
            font-size: 14px;
            color: #262626;
        }
        
        QMenu::item {
            padding: 8px 16px;
        }
        
        QMenu::item:selected {
            background-color: #e6f7ff;
            color: #1890ff;
        }
        
        /* 滚动条样式 */
        QScrollBar:vertical {
            background-color: #f0f0f0;
            width: 8px;
            border-radius: 4px;
        }
        
        QScrollBar::handle:vertical {
            background-color: #d9d9d9;
            border-radius: 4px;
            min-height: 20px;
        }
        
        QScrollBar::handle:vertical:hover {
            background-color: #bfbfbf;
        }
        
        QScrollBar:horizontal {
            background-color: #f0f0f0;
            height: 8px;
            border-radius: 4px;
        }
        
        QScrollBar::handle:horizontal {
            background-color: #d9d9d9;
            border-radius: 4px;
            min-width: 20px;
        }
        
        QScrollBar::handle:horizontal:hover {
            background-color: #bfbfbf;
        }
        
        /* 对话框样式 */
        QDialog {
            background-color: #ffffff;
            border: 1px solid #d9d9d9;
            border-radius: 4px;
        }
        
        /* 文本编辑器样式 */
        QTextEdit {
            background-color: #ffffff;
            border: 1px solid #d9d9d9;
            border-radius: 4px;
            padding: 8px;
            font-size: 14px;
            color: #262626;
            line-height: 1.5;
        }
        
        QTextEdit:focus {
            border-color: #1890ff;
        }
        
        /* 进度条样式 */
        QProgressBar {
            border: 1px solid #d9d9d9;
            border-radius: 4px;
            background-color: #f0f0f0;
            height: 20px;
            text-align: center;
            font-size: 12px;
        }
        
        QProgressBar::chunk {
            background-color: #1890ff;
            border-radius: 3px;
        }
        
        /* 复选框和单选框样式 */
        QCheckBox, QRadioButton {
            font-size: 14px;
            color: #262626;
            spacing: 8px;
        }
        
        QCheckBox::indicator, QRadioButton::indicator {
            width: 16px;
            height: 16px;
        }
        
        QCheckBox::indicator:unchecked {
            border: 1px solid #d9d9d9;
            background-color: #ffffff;
            border-radius: 2px;
        }
        
        QCheckBox::indicator:checked {
            border: 1px solid #1890ff;
            background-color: #1890ff;
            border-radius: 2px;
        }
        
        QRadioButton::indicator:unchecked {
            border: 1px solid #d9d9d9;
            background-color: #ffffff;
            border-radius: 8px;
        }
        
        QRadioButton::indicator:checked {
            border: 1px solid #1890ff;
            background-color: #1890ff;
            border-radius: 8px;
        }
    """

def get_button_class_style(variant):
    """获取特定类型按钮的样式类名"""
    class_map = {
        'primary': '',
        'secondary': 'secondary',
        'success': 'success',
        'danger': 'danger'
    }
    return class_map.get(variant, '')

def apply_button_style(button, variant='primary'):
    """为按钮应用特定样式"""
    class_name = get_button_class_style(variant)
    if class_name:
        button.setProperty('class', class_name)
    # 强制刷新样式
    button.style().unpolish(button)
    button.style().polish(button)
