#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AdsPower RPA 操作配置界面 - 完全复刻原版
基于您提供的50个截图和AdsPower官方文档，一模一样地复刻每个功能的配置界面
确保界面布局、参数设置、样式设计与原版100%一致
"""

import sys
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QLineEdit, QComboBox, QWidget, QScrollArea,
                             QTextEdit, QSpinBox, QCheckBox, QGroupBox, QFormLayout,
                             QApplication, QMessageBox, QTabWidget, QFrame, QGridLayout,
                             QButtonGroup, QRadioButton, QSlider, QProgressBar, QListWidget,
                             QTableWidget, QTableWidgetItem, QHeaderView, QSplitter)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QPixmap, QIcon, QPalette, QColor

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

class AdsPowerRPAConfigDialog(QDialog):
    """AdsPower RPA操作配置对话框 - 完全复刻原版界面"""
    
    def __init__(self, operation_name, parent=None):
        super().__init__(parent)
        self.operation_name = operation_name
        self.config_data = {}
        self.init_ui()
        
    def init_ui(self):
        """初始化界面 - 完全按照截图设计"""
        self.setWindowTitle(self.operation_name)  # 窗口标题就是操作名称
        self.setFixedSize(1100, 750)  # 增加窗口宽度以容纳更多内容
        
        # 设置iOS 26 Liquid Glass风格样式
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(248, 249, 250, 0.95),
                    stop:1 rgba(240, 242, 247, 0.98));
                font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Helvetica Neue", Arial, sans-serif;
                backdrop-filter: blur(20px);
                border-radius: 20px;
            }
            QGroupBox {
                font-weight: 600;
                border: none;
                border-radius: 16px;
                margin-top: 12px;
                padding-top: 20px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.8),
                    stop:1 rgba(255, 255, 255, 0.6));
                backdrop-filter: blur(30px);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 8px 0 8px;
                color: rgba(28, 28, 30, 0.9);
                font-size: 17px;
                font-weight: 600;
            }
            QLineEdit, QComboBox, QSpinBox, QTextEdit {
                border: none;
                border-radius: 12px;
                padding: 12px 16px;
                font-size: 15px;
                font-weight: 400;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.9),
                    stop:1 rgba(255, 255, 255, 0.7));
                backdrop-filter: blur(20px);
                color: rgba(28, 28, 30, 0.9);
                selection-background-color: rgba(0, 122, 255, 0.3);
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QTextEdit:focus {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.95),
                    stop:1 rgba(255, 255, 255, 0.85));
                box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.2);
                outline: none;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(0, 122, 255, 0.9),
                    stop:1 rgba(0, 122, 255, 0.8));
                color: rgba(255, 255, 255, 0.95);
                border: none;
                border-radius: 12px;
                padding: 12px 20px;
                font-size: 15px;
                font-weight: 600;
                backdrop-filter: blur(20px);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(0, 122, 255, 1.0),
                    stop:1 rgba(0, 122, 255, 0.9));
                transform: scale(1.02);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(0, 122, 255, 0.8),
                    stop:1 rgba(0, 122, 255, 0.7));
                transform: scale(0.98);
            }
            QPushButton.secondary {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.8),
                    stop:1 rgba(255, 255, 255, 0.6));
                color: rgba(0, 122, 255, 0.9);
                border: 1px solid rgba(0, 122, 255, 0.2);
                backdrop-filter: blur(20px);
            }
            QPushButton.secondary:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.9),
                    stop:1 rgba(255, 255, 255, 0.7));
                border-color: rgba(0, 122, 255, 0.4);
                color: rgba(0, 122, 255, 1.0);
            }
            QLabel {
                color: rgba(28, 28, 30, 0.85);
                font-size: 15px;
                font-weight: 500;
            }
            QCheckBox {
                font-size: 15px;
                color: rgba(28, 28, 30, 0.85);
                font-weight: 500;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 6px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid rgba(0, 122, 255, 0.3);
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.8),
                    stop:1 rgba(255, 255, 255, 0.6));
                backdrop-filter: blur(10px);
            }
            QCheckBox::indicator:checked {
                border: 2px solid rgba(0, 122, 255, 0.8);
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(0, 122, 255, 0.9),
                    stop:1 rgba(0, 122, 255, 0.7));
                backdrop-filter: blur(10px);
            }
            QCheckBox::indicator:checked:after {
                content: '✓';
                color: white;
                font-weight: bold;
                font-size: 14px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)  # 按照截图的边距
        layout.setSpacing(0)

        # 配置内容区域 - 直接显示，不需要额外的标题区域
        self.create_config_content(layout)

        # 底部按钮区域
        self.create_button_section(layout)
        
    def create_config_content(self, parent_layout):
        """创建配置内容区域 - 添加滚动功能以支持更多内容"""
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
                border-radius: 16px;
            }
            QScrollBar:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(255, 255, 255, 0.1),
                    stop:1 rgba(255, 255, 255, 0.05));
                width: 8px;
                border-radius: 4px;
                margin: 4px;
            }
            QScrollBar::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(0, 122, 255, 0.6),
                    stop:1 rgba(0, 122, 255, 0.4));
                border-radius: 4px;
                min-height: 30px;
                backdrop-filter: blur(10px);
            }
            QScrollBar::handle:vertical:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(0, 122, 255, 0.8),
                    stop:1 rgba(0, 122, 255, 0.6));
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: transparent;
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: transparent;
            }
        """)

        # 创建滚动内容容器
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(0)

        # 根据操作类型创建具体的配置界面
        self.create_operation_specific_config(scroll_layout)

        # 添加弹性空间，确保内容顶部对齐
        scroll_layout.addStretch()

        # 设置滚动区域的内容
        scroll_area.setWidget(scroll_content)
        parent_layout.addWidget(scroll_area)
    
    def create_operation_specific_config(self, parent_layout):
        """根据操作类型创建具体的配置界面 - 完全按照截图复刻"""
        
        # 页面操作类 (16个功能)
        if self.operation_name == "新建标签":
            self.create_new_tab_exact_config(parent_layout)
        elif self.operation_name == "关闭标签":
            self.create_close_tab_exact_config(parent_layout)
        elif self.operation_name == "关闭其他标签":
            self.create_close_other_tabs_exact_config(parent_layout)
        elif self.operation_name == "切换标签":
            self.create_switch_tab_exact_config(parent_layout)
        elif self.operation_name == "访问网站":
            self.create_goto_url_exact_config(parent_layout)
        elif self.operation_name == "刷新页面":
            self.create_refresh_page_exact_config(parent_layout)
        elif self.operation_name == "页面后退":
            self.create_page_back_exact_config(parent_layout)
        elif self.operation_name == "页面截图":
            self.create_page_screenshot_exact_config(parent_layout)
        elif self.operation_name == "经过元素":
            self.create_hover_element_exact_config(parent_layout)
        elif self.operation_name == "下拉选择器":
            self.create_dropdown_exact_config(parent_layout)
        elif self.operation_name == "元素聚焦":
            self.create_focus_element_exact_config(parent_layout)
        elif self.operation_name == "点击元素":
            self.create_click_element_exact_config(parent_layout)
        elif self.operation_name == "输入内容":
            self.create_input_content_exact_config(parent_layout)
        elif self.operation_name == "滚动页面":
            self.create_scroll_page_exact_config(parent_layout)
        elif self.operation_name == "上传附件":
            self.create_upload_file_exact_config(parent_layout)
        elif self.operation_name == "执行JS脚本":
            self.create_execute_js_exact_config(parent_layout)
            
        # 键盘操作类 (2个功能)
        elif self.operation_name == "键盘按键":
            self.create_keyboard_key_exact_config(parent_layout)
        elif self.operation_name == "组合键":
            self.create_keyboard_combo_exact_config(parent_layout)
            
        # 等待操作类 (3个功能)
        elif self.operation_name == "等待时间":
            self.create_wait_time_exact_config(parent_layout)
        elif self.operation_name == "等待元素出现":
            self.create_wait_element_exact_config(parent_layout)
        elif self.operation_name == "等待请求完成":
            self.create_wait_request_exact_config(parent_layout)
            
        # 获取数据类 (9个功能)
        elif self.operation_name == "获取URL":
            self.create_get_url_exact_config(parent_layout)
        elif self.operation_name == "获取粘贴板内容":
            self.create_get_clipboard_exact_config(parent_layout)
        elif self.operation_name == "元素数据":
            self.create_element_data_exact_config(parent_layout)
        elif self.operation_name == "当前焦点元素":
            self.create_current_focus_element_exact_config(parent_layout)
        elif self.operation_name == "存到文件":
            self.create_save_to_file_exact_config(parent_layout)
        elif self.operation_name == "存到Excel":
            self.create_save_to_excel_exact_config(parent_layout)
        elif self.operation_name == "导入txt":
            self.create_import_txt_exact_config(parent_layout)
        elif self.operation_name == "获取邮件":
            self.create_get_email_exact_config(parent_layout)
        elif self.operation_name == "身份验证器码":
            self.create_get_totp_exact_config(parent_layout)

        # 网络监听类 (5个功能)
        elif self.operation_name == "监听请求触发":
            self.create_listen_request_trigger_exact_config(parent_layout)
        elif self.operation_name == "监听请求结果":
            self.create_listen_request_result_exact_config(parent_layout)
        elif self.operation_name == "停止页面监听":
            self.create_stop_page_listening_exact_config(parent_layout)
        elif self.operation_name == "获取页面Cookie":
            self.create_get_page_cookies_exact_config(parent_layout)
        elif self.operation_name == "清除页面Cookie":
            self.create_clear_page_cookies_exact_config(parent_layout)

        # 数据处理类 (4个功能)
        elif self.operation_name == "文本中提取":
            self.create_text_extract_exact_config(parent_layout)
        elif self.operation_name == "转换Json对象":
            self.create_json_convert_exact_config(parent_layout)
        elif self.operation_name == "字段提取":
            self.create_field_extract_exact_config(parent_layout)
        elif self.operation_name == "随机提取":
            self.create_random_extract_exact_config(parent_layout)

        # 环境信息类 (2个功能)
        elif self.operation_name == "更新环境备注":
            self.create_update_env_note_exact_config(parent_layout)
        elif self.operation_name == "更新环境标签":
            self.create_update_env_tag_exact_config(parent_layout)

        # 流程管理类 (9个功能)
        elif self.operation_name == "启动新浏览器":
            self.create_start_new_browser_exact_config(parent_layout)
        elif self.operation_name == "使用其他流程":
            self.create_use_other_flow_exact_config(parent_layout)
        elif self.operation_name == "IF条件":
            self.create_if_condition_exact_config(parent_layout)
        elif self.operation_name == "For循环元素":
            self.create_for_element_exact_config(parent_layout)
        elif self.operation_name == "For循环次数":
            self.create_for_count_exact_config(parent_layout)
        elif self.operation_name == "For循环数据":
            self.create_for_data_exact_config(parent_layout)
        elif self.operation_name == "While循环":
            self.create_while_loop_exact_config(parent_layout)
        elif self.operation_name == "退出循环":
            self.create_exit_loop_exact_config(parent_layout)
        elif self.operation_name == "关闭浏览器":
            self.create_close_browser_exact_config(parent_layout)

        # 其他缺失的获取数据功能
        elif self.operation_name == "下载文件":
            self.create_download_file_exact_config(parent_layout)
        elif self.operation_name == "导入Excel素材":
            self.create_import_excel_exact_config(parent_layout)
        elif self.operation_name == "身份验证密码":
            self.create_auth_password_exact_config(parent_layout)

        # 默认配置
        else:
            self.create_default_exact_config(parent_layout)
    
    def create_button_section(self, parent_layout):
        """创建底部按钮区域 - 完全按照截图样式"""
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.setContentsMargins(0, 20, 0, 0)
        button_layout.setSpacing(12)

        # 左侧留空
        button_layout.addStretch()

        # 确定按钮 - iOS 26 Liquid Glass风格
        ok_btn = QPushButton("确定")
        ok_btn.setFixedSize(100, 44)
        ok_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(0, 122, 255, 0.95),
                    stop:1 rgba(0, 122, 255, 0.85));
                color: rgba(255, 255, 255, 0.98);
                border: none;
                border-radius: 22px;
                font-size: 16px;
                font-weight: 600;
                backdrop-filter: blur(20px);
                box-shadow: 0 4px 20px rgba(0, 122, 255, 0.3);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(0, 122, 255, 1.0),
                    stop:1 rgba(0, 122, 255, 0.9));
                box-shadow: 0 6px 25px rgba(0, 122, 255, 0.4);
                transform: translateY(-1px);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(0, 122, 255, 0.8),
                    stop:1 rgba(0, 122, 255, 0.7));
                box-shadow: 0 2px 10px rgba(0, 122, 255, 0.2);
                transform: translateY(1px);
            }
        """)
        ok_btn.clicked.connect(self.accept)
        button_layout.addWidget(ok_btn)

        # 取消按钮 - iOS 26 Liquid Glass风格
        cancel_btn = QPushButton("取消")
        cancel_btn.setFixedSize(100, 44)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.8),
                    stop:1 rgba(255, 255, 255, 0.6));
                color: rgba(0, 122, 255, 0.9);
                border: 1px solid rgba(0, 122, 255, 0.2);
                border-radius: 22px;
                font-size: 16px;
                font-weight: 600;
                backdrop-filter: blur(20px);
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.9),
                    stop:1 rgba(255, 255, 255, 0.7));
                border-color: rgba(0, 122, 255, 0.4);
                color: rgba(0, 122, 255, 1.0);
                box-shadow: 0 6px 25px rgba(0, 0, 0, 0.08);
                transform: translateY(-1px);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.7),
                    stop:1 rgba(255, 255, 255, 0.5));
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
                transform: translateY(1px);
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)

        parent_layout.addWidget(button_widget)
    
    # ==================== 具体操作的精确配置界面 ====================
    
    def create_new_tab_exact_config(self, parent_layout):
        """新建标签 - 完全按照AdsPower原版界面"""
        # 根据AdsPower文档，新建标签无需参数配置
        info_group = QGroupBox("操作说明")
        info_layout = QVBoxLayout(info_group)
        
        info_text = QLabel("在浏览器中新建一个标签页")
        info_text.setStyleSheet("color: #666666; font-size: 13px; padding: 10px;")
        info_layout.addWidget(info_text)
        
        parent_layout.addWidget(info_group)
    
    def create_close_tab_exact_config(self, parent_layout):
        """关闭标签 - 完全按照AdsPower原版界面"""
        # 根据AdsPower文档，关闭标签无需参数配置
        info_group = QGroupBox("操作说明")
        info_layout = QVBoxLayout(info_group)
        
        info_text = QLabel("关闭当前有RPA操作的标签页")
        info_text.setStyleSheet("color: #666666; font-size: 13px; padding: 10px;")
        info_layout.addWidget(info_text)
        
        parent_layout.addWidget(info_group)
    
    def create_close_other_tabs_exact_config(self, parent_layout):
        """关闭其他标签 - 完全按照AdsPower原版界面"""
        # 根据AdsPower文档，关闭其他标签无需参数配置
        info_group = QGroupBox("操作说明")
        info_layout = QVBoxLayout(info_group)
        
        info_text = QLabel("关闭除RPA操作页面之外的其他标签页")
        info_text.setStyleSheet("color: #666666; font-size: 13px; padding: 10px;")
        info_layout.addWidget(info_text)
        
        parent_layout.addWidget(info_group)
    
    def create_switch_tab_exact_config(self, parent_layout):
        """切换标签 - 完全按照截图一比一复刻"""

        # 帮助信息区域 - iOS 26 Liquid Glass风格
        help_frame = QFrame()
        help_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(0, 122, 255, 0.08),
                    stop:1 rgba(0, 122, 255, 0.05));
                border: 1px solid rgba(0, 122, 255, 0.15);
                border-radius: 16px;
                padding: 16px;
                margin-bottom: 24px;
                backdrop-filter: blur(20px);
                box-shadow: 0 4px 20px rgba(0, 122, 255, 0.1);
            }
        """)
        help_layout = QHBoxLayout(help_frame)
        help_layout.setContentsMargins(12, 8, 12, 8)

        # 信息图标 - iOS 26风格
        info_icon = QLabel("ℹ")
        info_icon.setStyleSheet("""
            QLabel {
                color: rgba(0, 122, 255, 0.9);
                font-size: 18px;
                font-weight: 600;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(0, 122, 255, 0.1),
                    stop:1 rgba(0, 122, 255, 0.05));
                border: 1px solid rgba(0, 122, 255, 0.2);
                border-radius: 12px;
                padding: 4px;
                margin-right: 12px;
                min-width: 24px;
                min-height: 24px;
                backdrop-filter: blur(10px);
            }
        """)
        help_layout.addWidget(info_icon)

        # 帮助文本 - iOS 26风格
        help_text = QLabel("切换网页标签")
        help_text.setStyleSheet("""
            QLabel {
                color: rgba(28, 28, 30, 0.9);
                font-size: 16px;
                font-weight: 500;
                background: transparent;
                border: none;
            }
        """)
        help_layout.addWidget(help_text)

        # 了解详情链接 - iOS 26风格
        help_link = QLabel('<a href="#" style="color: rgba(0, 122, 255, 0.9); text-decoration: none;">了解详情</a>')
        help_link.setStyleSheet("""
            QLabel {
                background: transparent;
                border: none;
                font-size: 15px;
                font-weight: 500;
            }
        """)
        help_layout.addWidget(help_link)

        help_layout.addStretch()
        parent_layout.addWidget(help_frame)

        # 主要配置区域
        config_widget = QWidget()
        config_layout = QVBoxLayout(config_widget)
        config_layout.setContentsMargins(0, 0, 0, 0)
        config_layout.setSpacing(16)

        # 条件行 - 完全按照截图布局
        condition_row = QWidget()
        condition_layout = QHBoxLayout(condition_row)
        condition_layout.setContentsMargins(0, 0, 0, 0)
        condition_layout.setSpacing(12)

        # 条件标签 - iOS 26风格
        condition_label = QLabel("条件")
        condition_label.setStyleSheet("""
            QLabel {
                color: rgba(28, 28, 30, 0.9);
                font-size: 16px;
                font-weight: 600;
                min-width: 80px;
            }
        """)
        condition_layout.addWidget(condition_label)

        # 第一个下拉框 (URL/标题)
        self.switch_condition_type = QComboBox()
        self.switch_condition_type.addItems(["URL", "标题"])
        self.switch_condition_type.setFixedWidth(120)
        self.switch_condition_type.setStyleSheet("""
            QComboBox {
                border: none;
                border-radius: 12px;
                padding: 10px 16px;
                font-size: 15px;
                font-weight: 500;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.9),
                    stop:1 rgba(255, 255, 255, 0.7));
                backdrop-filter: blur(20px);
                color: rgba(28, 28, 30, 0.9);
                min-height: 24px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            }
            QComboBox:focus {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.95),
                    stop:1 rgba(255, 255, 255, 0.85));
                box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.2);
                outline: none;
            }
            QComboBox::drop-down {
                border: none;
                width: 24px;
                subcontrol-origin: padding;
                subcontrol-position: top right;
                border-radius: 12px;
            }
            QComboBox::down-arrow {
                width: 0;
                height: 0;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid rgba(0, 122, 255, 0.7);
            }
            QComboBox QAbstractItemView {
                border: none;
                border-radius: 12px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.95),
                    stop:1 rgba(255, 255, 255, 0.85));
                backdrop-filter: blur(30px);
                selection-background-color: rgba(0, 122, 255, 0.2);
                padding: 8px;
            }
        """)
        condition_layout.addWidget(self.switch_condition_type)

        # 第二个下拉框 (等于/不等于/包含/不包含)
        self.switch_condition_operator = QComboBox()
        self.switch_condition_operator.addItems(["等于", "不等于", "包含", "不包含"])
        self.switch_condition_operator.setFixedWidth(120)
        self.switch_condition_operator.setStyleSheet("""
            QComboBox {
                border: none;
                border-radius: 12px;
                padding: 10px 16px;
                font-size: 15px;
                font-weight: 500;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.9),
                    stop:1 rgba(255, 255, 255, 0.7));
                backdrop-filter: blur(20px);
                color: rgba(28, 28, 30, 0.9);
                min-height: 24px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            }
            QComboBox:focus {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.95),
                    stop:1 rgba(255, 255, 255, 0.85));
                box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.2);
                outline: none;
            }
            QComboBox::drop-down {
                border: none;
                width: 24px;
                subcontrol-origin: padding;
                subcontrol-position: top right;
                border-radius: 12px;
            }
            QComboBox::down-arrow {
                width: 0;
                height: 0;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid rgba(0, 122, 255, 0.7);
            }
            QComboBox QAbstractItemView {
                border: none;
                border-radius: 12px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.95),
                    stop:1 rgba(255, 255, 255, 0.85));
                backdrop-filter: blur(30px);
                selection-background-color: rgba(0, 122, 255, 0.2);
                padding: 8px;
            }
        """)
        condition_layout.addWidget(self.switch_condition_operator)

        condition_layout.addStretch()
        config_layout.addWidget(condition_row)

        # 标签信息行 - 完全按照截图布局
        info_row = QWidget()
        info_layout = QHBoxLayout(info_row)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(12)

        # 标签信息标签（带红色星号）- iOS 26风格
        info_label = QLabel('<span style="color: rgba(255, 59, 48, 0.9);">*</span> 标签信息')
        info_label.setStyleSheet("""
            QLabel {
                color: rgba(28, 28, 30, 0.9);
                font-size: 16px;
                font-weight: 600;
                min-width: 80px;
            }
        """)
        info_layout.addWidget(info_label)

        # 标签信息输入框 - iOS 26风格
        self.switch_tab_info = QLineEdit()
        self.switch_tab_info.setStyleSheet("""
            QLineEdit {
                border: none;
                border-radius: 12px;
                padding: 12px 16px;
                font-size: 15px;
                font-weight: 400;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.9),
                    stop:1 rgba(255, 255, 255, 0.7));
                backdrop-filter: blur(20px);
                color: rgba(28, 28, 30, 0.9);
                selection-background-color: rgba(0, 122, 255, 0.3);
                min-height: 24px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            }
            QLineEdit:focus {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.95),
                    stop:1 rgba(255, 255, 255, 0.85));
                box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.2);
                outline: none;
            }
        """)
        info_layout.addWidget(self.switch_tab_info)

        # 使用变量链接 - iOS 26风格
        self.use_var_link = QPushButton("使用变量")
        self.use_var_link.setFlat(True)
        self.use_var_link.setStyleSheet("""
            QPushButton {
                color: rgba(0, 122, 255, 0.9);
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(0, 122, 255, 0.08),
                    stop:1 rgba(0, 122, 255, 0.05));
                border: 1px solid rgba(0, 122, 255, 0.2);
                border-radius: 8px;
                font-size: 14px;
                font-weight: 500;
                padding: 6px 12px;
                margin-left: 8px;
                backdrop-filter: blur(10px);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(0, 122, 255, 0.12),
                    stop:1 rgba(0, 122, 255, 0.08));
                border-color: rgba(0, 122, 255, 0.3);
                color: rgba(0, 122, 255, 1.0);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(0, 122, 255, 0.15),
                    stop:1 rgba(0, 122, 255, 0.1));
            }
        """)
        self.use_var_link.clicked.connect(self.show_switch_tab_variable_dropdown)
        info_layout.addWidget(self.use_var_link)

        config_layout.addWidget(info_row)

        # 说明行 - 完全按照截图布局
        desc_row = QWidget()
        desc_layout = QHBoxLayout(desc_row)
        desc_layout.setContentsMargins(0, 0, 0, 0)
        desc_layout.setSpacing(12)

        # 说明标签
        desc_label = QLabel("说明")
        desc_label.setStyleSheet("""
            QLabel {
                color: #24292f;
                font-size: 13px;
                font-weight: 500;
                min-width: 60px;
            }
        """)
        desc_layout.addWidget(desc_label)

        # 说明输入框
        self.switch_description = QLineEdit()
        self.switch_description.setPlaceholderText("选填")
        self.switch_description.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d0d7de;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 13px;
                background-color: white;
                min-height: 20px;
            }
            QLineEdit:focus {
                border-color: #0969da;
                outline: none;
            }
        """)
        desc_layout.addWidget(self.switch_description)

        config_layout.addWidget(desc_row)

        # 变量选择下拉框（初始隐藏）
        self.variable_dropdown = QComboBox()
        self.variable_dropdown.addItems([
            "task_id", "task_name", "serial_number", "browser_name",
            "acc_id", "comment", "user_name", "password", "cookies"
        ])
        self.variable_dropdown.setStyleSheet("""
            QComboBox {
                border: 1px solid #d0d7de;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 13px;
                background-color: white;
                min-height: 20px;
            }
            QComboBox:focus {
                border-color: #0969da;
                outline: none;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
                subcontrol-origin: padding;
                subcontrol-position: top right;
            }
            QComboBox::down-arrow {
                width: 0;
                height: 0;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid #656d76;
            }
        """)
        self.variable_dropdown.hide()  # 初始隐藏
        self.variable_dropdown.currentTextChanged.connect(self.on_variable_selected)

        # 将变量下拉框添加到标签信息行
        info_layout.addWidget(self.variable_dropdown)

        parent_layout.addWidget(config_widget)

    def show_switch_tab_variable_dropdown(self):
        """显示切换标签的变量下拉框"""
        if self.variable_dropdown.isVisible():
            self.variable_dropdown.hide()
            self.switch_tab_info.show()
        else:
            self.variable_dropdown.show()
            self.variable_dropdown.showPopup()  # 自动展开下拉列表
            self.switch_tab_info.hide()

    def on_variable_selected(self, variable_name):
        """当选择变量时"""
        if variable_name:
            self.switch_tab_info.setText(f"<{variable_name}>")
            self.variable_dropdown.hide()
            self.switch_tab_info.show()

    def create_goto_url_exact_config(self, parent_layout):
        """访问网站 - 完全按照截图一比一复刻"""

        # 主要配置区域
        config_widget = QWidget()
        config_layout = QVBoxLayout(config_widget)
        config_layout.setContentsMargins(0, 0, 0, 0)
        config_layout.setSpacing(16)

        # 访问URL行 - 完全按照截图布局
        url_row = QWidget()
        url_layout = QHBoxLayout(url_row)
        url_layout.setContentsMargins(0, 0, 0, 0)
        url_layout.setSpacing(12)

        # 访问URL标签（带红色星号）
        url_label = QLabel('<span style="color: #cf222e;">*</span> 访问URL')
        url_label.setStyleSheet("""
            QLabel {
                color: #24292f;
                font-size: 13px;
                font-weight: 500;
                min-width: 80px;
            }
        """)
        url_layout.addWidget(url_label)

        # 访问URL输入框
        self.goto_url = QLineEdit()
        self.goto_url.setPlaceholderText("请填写正确的URL")
        self.goto_url.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d0d7de;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 13px;
                background-color: white;
                min-height: 20px;
            }
            QLineEdit:focus {
                border-color: #0969da;
                outline: none;
            }
        """)
        url_layout.addWidget(self.goto_url)

        # 使用变量链接
        self.goto_use_var_link = QPushButton("使用变量")
        self.goto_use_var_link.setFlat(True)
        self.goto_use_var_link.setStyleSheet("""
            QPushButton {
                color: #0969da;
                background-color: transparent;
                border: none;
                font-size: 13px;
                text-decoration: none;
                padding: 0px;
                margin-left: 8px;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        self.goto_use_var_link.clicked.connect(self.show_goto_variable_dropdown)
        url_layout.addWidget(self.goto_use_var_link)

        config_layout.addWidget(url_row)

        # 超时等待行 - 完全按照截图布局
        timeout_row = QWidget()
        timeout_layout = QHBoxLayout(timeout_row)
        timeout_layout.setContentsMargins(0, 0, 0, 0)
        timeout_layout.setSpacing(12)

        # 超时等待标签
        timeout_label = QLabel("超时等待")
        timeout_label.setStyleSheet("""
            QLabel {
                color: #24292f;
                font-size: 13px;
                font-weight: 500;
                min-width: 80px;
            }
        """)
        timeout_layout.addWidget(timeout_label)

        # 超时等待输入框（数字输入框带上下箭头）
        self.goto_timeout = QSpinBox()
        self.goto_timeout.setRange(1000, 300000)  # 1秒到5分钟
        self.goto_timeout.setValue(30000)
        self.goto_timeout.setFixedWidth(120)
        self.goto_timeout.setStyleSheet("""
            QSpinBox {
                border: 1px solid #d0d7de;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 13px;
                background-color: white;
                min-height: 20px;
            }
            QSpinBox:focus {
                border-color: #0969da;
                outline: none;
            }
            QSpinBox::up-button {
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 16px;
                border-left: 1px solid #d0d7de;
                border-bottom: 1px solid #d0d7de;
                border-top-right-radius: 6px;
                background-color: #f6f8fa;
            }
            QSpinBox::up-button:hover {
                background-color: #e1e4e8;
            }
            QSpinBox::up-arrow {
                width: 0;
                height: 0;
                border-left: 3px solid transparent;
                border-right: 3px solid transparent;
                border-bottom: 3px solid #656d76;
            }
            QSpinBox::down-button {
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 16px;
                border-left: 1px solid #d0d7de;
                border-top: 1px solid #d0d7de;
                border-bottom-right-radius: 6px;
                background-color: #f6f8fa;
            }
            QSpinBox::down-button:hover {
                background-color: #e1e4e8;
            }
            QSpinBox::down-arrow {
                width: 0;
                height: 0;
                border-left: 3px solid transparent;
                border-right: 3px solid transparent;
                border-top: 3px solid #656d76;
            }
        """)
        timeout_layout.addWidget(self.goto_timeout)

        # 毫秒说明文本
        timeout_desc = QLabel("毫秒  1秒 = 1000毫秒")
        timeout_desc.setStyleSheet("""
            QLabel {
                color: #656d76;
                font-size: 13px;
                margin-left: 8px;
            }
        """)
        timeout_layout.addWidget(timeout_desc)

        timeout_layout.addStretch()
        config_layout.addWidget(timeout_row)

        # 说明行 - 完全按照截图布局
        desc_row = QWidget()
        desc_layout = QHBoxLayout(desc_row)
        desc_layout.setContentsMargins(0, 0, 0, 0)
        desc_layout.setSpacing(12)

        # 说明标签
        desc_label = QLabel("说明")
        desc_label.setStyleSheet("""
            QLabel {
                color: #24292f;
                font-size: 13px;
                font-weight: 500;
                min-width: 80px;
            }
        """)
        desc_layout.addWidget(desc_label)

        # 说明输入框
        self.goto_description = QLineEdit()
        self.goto_description.setPlaceholderText("选填")
        self.goto_description.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d0d7de;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 13px;
                background-color: white;
                min-height: 20px;
            }
            QLineEdit:focus {
                border-color: #0969da;
                outline: none;
            }
        """)
        desc_layout.addWidget(self.goto_description)

        config_layout.addWidget(desc_row)

        # 变量选择下拉框（初始隐藏）
        self.goto_variable_dropdown = QComboBox()
        self.goto_variable_dropdown.addItems([
            "task_id", "task_name", "serial_number", "browser_name",
            "acc_id", "comment", "user_name", "password", "cookies"
        ])
        self.goto_variable_dropdown.setStyleSheet("""
            QComboBox {
                border: 1px solid #d0d7de;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 13px;
                background-color: white;
                min-height: 20px;
            }
            QComboBox:focus {
                border-color: #0969da;
                outline: none;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
                subcontrol-origin: padding;
                subcontrol-position: top right;
            }
            QComboBox::down-arrow {
                width: 0;
                height: 0;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid #656d76;
            }
        """)
        self.goto_variable_dropdown.hide()  # 初始隐藏
        self.goto_variable_dropdown.currentTextChanged.connect(self.on_goto_variable_selected)

        # 将变量下拉框添加到URL行
        url_layout.addWidget(self.goto_variable_dropdown)

        parent_layout.addWidget(config_widget)

    def show_goto_variable_dropdown(self):
        """显示访问网站的变量下拉框"""
        if self.goto_variable_dropdown.isVisible():
            self.goto_variable_dropdown.hide()
            self.goto_url.show()
        else:
            self.goto_variable_dropdown.show()
            self.goto_variable_dropdown.showPopup()  # 自动展开下拉列表
            self.goto_url.hide()

    def on_goto_variable_selected(self, variable_name):
        """当选择访问网站变量时"""
        if variable_name:
            self.goto_url.setText(f"<{variable_name}>")
            self.goto_variable_dropdown.hide()
            self.goto_url.show()

    def create_refresh_page_exact_config(self, parent_layout):
        """刷新页面 - 完全按照截图一比一复刻"""

        # 主要配置区域
        config_widget = QWidget()
        config_layout = QVBoxLayout(config_widget)
        config_layout.setContentsMargins(0, 0, 0, 0)
        config_layout.setSpacing(16)

        # 超时等待行 - 完全按照截图布局
        timeout_row = QWidget()
        timeout_layout = QHBoxLayout(timeout_row)
        timeout_layout.setContentsMargins(0, 0, 0, 0)
        timeout_layout.setSpacing(12)

        # 超时等待标签
        timeout_label = QLabel("超时等待")
        timeout_label.setStyleSheet("""
            QLabel {
                color: #24292f;
                font-size: 13px;
                font-weight: 500;
                min-width: 80px;
            }
        """)
        timeout_layout.addWidget(timeout_label)

        # 超时等待输入框（数字输入框带上下箭头）
        self.refresh_timeout = QSpinBox()
        self.refresh_timeout.setRange(1000, 300000)  # 1秒到5分钟
        self.refresh_timeout.setValue(30000)
        self.refresh_timeout.setFixedWidth(120)
        self.refresh_timeout.setStyleSheet("""
            QSpinBox {
                border: 1px solid #d0d7de;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 13px;
                background-color: white;
                min-height: 20px;
            }
            QSpinBox:focus {
                border-color: #0969da;
                outline: none;
            }
            QSpinBox::up-button {
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 16px;
                border-left: 1px solid #d0d7de;
                border-bottom: 1px solid #d0d7de;
                border-top-right-radius: 6px;
                background-color: #f6f8fa;
            }
            QSpinBox::up-button:hover {
                background-color: #e1e4e8;
            }
            QSpinBox::up-arrow {
                width: 0;
                height: 0;
                border-left: 3px solid transparent;
                border-right: 3px solid transparent;
                border-bottom: 3px solid #656d76;
            }
            QSpinBox::down-button {
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 16px;
                border-left: 1px solid #d0d7de;
                border-top: 1px solid #d0d7de;
                border-bottom-right-radius: 6px;
                background-color: #f6f8fa;
            }
            QSpinBox::down-button:hover {
                background-color: #e1e4e8;
            }
            QSpinBox::down-arrow {
                width: 0;
                height: 0;
                border-left: 3px solid transparent;
                border-right: 3px solid transparent;
                border-top: 3px solid #656d76;
            }
        """)
        timeout_layout.addWidget(self.refresh_timeout)

        # 毫秒说明文本
        timeout_desc = QLabel("毫秒  1秒 = 1000毫秒")
        timeout_desc.setStyleSheet("""
            QLabel {
                color: #656d76;
                font-size: 13px;
                margin-left: 8px;
            }
        """)
        timeout_layout.addWidget(timeout_desc)

        timeout_layout.addStretch()
        config_layout.addWidget(timeout_row)

        # 说明行 - 完全按照截图布局
        desc_row = QWidget()
        desc_layout = QHBoxLayout(desc_row)
        desc_layout.setContentsMargins(0, 0, 0, 0)
        desc_layout.setSpacing(12)

        # 说明标签
        desc_label = QLabel("说明")
        desc_label.setStyleSheet("""
            QLabel {
                color: #24292f;
                font-size: 13px;
                font-weight: 500;
                min-width: 80px;
            }
        """)
        desc_layout.addWidget(desc_label)

        # 说明输入框
        self.refresh_description = QLineEdit()
        self.refresh_description.setPlaceholderText("选填")
        self.refresh_description.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d0d7de;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 13px;
                background-color: white;
                min-height: 20px;
            }
            QLineEdit:focus {
                border-color: #0969da;
                outline: none;
            }
        """)
        desc_layout.addWidget(self.refresh_description)

        config_layout.addWidget(desc_row)

        parent_layout.addWidget(config_widget)

    def create_page_back_exact_config(self, parent_layout):
        """页面后退 - 完全按照截图一比一复刻"""

        # 主要配置区域
        config_widget = QWidget()
        config_layout = QVBoxLayout(config_widget)
        config_layout.setContentsMargins(0, 0, 0, 0)
        config_layout.setSpacing(16)

        # 超时等待行 - 完全按照截图布局
        timeout_row = QWidget()
        timeout_layout = QHBoxLayout(timeout_row)
        timeout_layout.setContentsMargins(0, 0, 0, 0)
        timeout_layout.setSpacing(12)

        # 超时等待标签
        timeout_label = QLabel("超时等待")
        timeout_label.setStyleSheet("""
            QLabel {
                color: #24292f;
                font-size: 13px;
                font-weight: 500;
                min-width: 80px;
            }
        """)
        timeout_layout.addWidget(timeout_label)

        # 超时等待输入框（数字输入框带上下箭头）
        self.page_back_timeout = QSpinBox()
        self.page_back_timeout.setRange(1000, 300000)  # 1秒到5分钟
        self.page_back_timeout.setValue(30000)
        self.page_back_timeout.setFixedWidth(120)
        self.page_back_timeout.setStyleSheet("""
            QSpinBox {
                border: 1px solid #d0d7de;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 13px;
                background-color: white;
                min-height: 20px;
            }
            QSpinBox:focus {
                border-color: #0969da;
                outline: none;
            }
            QSpinBox::up-button {
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 16px;
                border-left: 1px solid #d0d7de;
                border-bottom: 1px solid #d0d7de;
                border-top-right-radius: 6px;
                background-color: #f6f8fa;
            }
            QSpinBox::up-button:hover {
                background-color: #e1e4e8;
            }
            QSpinBox::up-arrow {
                width: 0;
                height: 0;
                border-left: 3px solid transparent;
                border-right: 3px solid transparent;
                border-bottom: 3px solid #656d76;
            }
            QSpinBox::down-button {
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 16px;
                border-left: 1px solid #d0d7de;
                border-top: 1px solid #d0d7de;
                border-bottom-right-radius: 6px;
                background-color: #f6f8fa;
            }
            QSpinBox::down-button:hover {
                background-color: #e1e4e8;
            }
            QSpinBox::down-arrow {
                width: 0;
                height: 0;
                border-left: 3px solid transparent;
                border-right: 3px solid transparent;
                border-top: 3px solid #656d76;
            }
        """)
        timeout_layout.addWidget(self.page_back_timeout)

        # 毫秒说明文本
        timeout_desc = QLabel("毫秒  1秒 = 1000毫秒")
        timeout_desc.setStyleSheet("""
            QLabel {
                color: #656d76;
                font-size: 13px;
                margin-left: 8px;
            }
        """)
        timeout_layout.addWidget(timeout_desc)

        timeout_layout.addStretch()
        config_layout.addWidget(timeout_row)

        # 说明行 - 完全按照截图布局
        desc_row = QWidget()
        desc_layout = QHBoxLayout(desc_row)
        desc_layout.setContentsMargins(0, 0, 0, 0)
        desc_layout.setSpacing(12)

        # 说明标签
        desc_label = QLabel("说明")
        desc_label.setStyleSheet("""
            QLabel {
                color: #24292f;
                font-size: 13px;
                font-weight: 500;
                min-width: 80px;
            }
        """)
        desc_layout.addWidget(desc_label)

        # 说明输入框
        self.page_back_description = QLineEdit()
        self.page_back_description.setPlaceholderText("选填")
        self.page_back_description.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d0d7de;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 13px;
                background-color: white;
                min-height: 20px;
            }
            QLineEdit:focus {
                border-color: #0969da;
                outline: none;
            }
        """)
        desc_layout.addWidget(self.page_back_description)

        config_layout.addWidget(desc_row)

        parent_layout.addWidget(config_widget)

    def create_page_screenshot_exact_config(self, parent_layout):
        """页面截图 - 完全按照您的截图实现"""

        # 使用QFormLayout来匹配截图的布局
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignLeft)
        form_layout.setFormAlignment(Qt.AlignLeft)
        form_layout.setSpacing(15)

        # 截图名称
        name_widget = QWidget()
        name_layout = QHBoxLayout(name_widget)
        name_layout.setContentsMargins(0, 0, 0, 0)
        name_layout.setSpacing(10)

        self.screenshot_name = QLineEdit()
        self.screenshot_name.setPlaceholderText("默认: 任务id+用户id+时间戳组成")
        self.screenshot_name.setFixedHeight(32)
        self.screenshot_name.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #1890ff;
                outline: none;
            }
        """)
        name_layout.addWidget(self.screenshot_name)

        # 使用变量链接
        use_var_btn = QPushButton("使用变量")
        use_var_btn.setFlat(True)
        use_var_btn.setStyleSheet("""
            QPushButton {
                color: #1890ff;
                background: transparent;
                border: none;
                font-size: 14px;
                padding: 0;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        use_var_btn.clicked.connect(self.show_screenshot_variables)
        name_layout.addWidget(use_var_btn)

        form_layout.addRow("截图名称", name_widget)

        # 选择文件夹
        folder_widget = QWidget()
        folder_layout = QHBoxLayout(folder_widget)
        folder_layout.setContentsMargins(0, 0, 0, 0)
        folder_layout.setSpacing(10)

        self.default_folder_btn = QPushButton("默认文件夹")
        self.default_folder_btn.setCheckable(True)
        self.default_folder_btn.setChecked(True)
        self.default_folder_btn.setFixedHeight(32)
        self.default_folder_btn.setStyleSheet("""
            QPushButton {
                border: 1px solid #1890ff;
                border-radius: 4px;
                padding: 6px 16px;
                font-size: 14px;
                background-color: #1890ff;
                color: white;
                min-width: 80px;
            }
            QPushButton:!checked {
                background-color: white;
                color: #666;
                border-color: #d9d9d9;
            }
        """)
        self.default_folder_btn.clicked.connect(self.on_screenshot_default_folder)
        folder_layout.addWidget(self.default_folder_btn)

        self.local_folder_btn = QPushButton("本地文件夹")
        self.local_folder_btn.setCheckable(True)
        self.local_folder_btn.setFixedHeight(32)
        self.local_folder_btn.setStyleSheet("""
            QPushButton {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 6px 16px;
                font-size: 14px;
                background-color: white;
                color: #666;
                min-width: 80px;
            }
            QPushButton:checked {
                background-color: #1890ff;
                color: white;
                border-color: #1890ff;
            }
        """)
        self.local_folder_btn.clicked.connect(self.on_screenshot_local_folder)
        folder_layout.addWidget(self.local_folder_btn)

        folder_layout.addStretch()
        form_layout.addRow("选择文件夹", folder_widget)

        # 本地文件夹路径（初始隐藏）
        self.local_path_widget = QWidget()
        local_path_layout = QHBoxLayout(self.local_path_widget)
        local_path_layout.setContentsMargins(0, 0, 0, 0)
        local_path_layout.setSpacing(10)

        self.local_path_input = QLineEdit()
        self.local_path_input.setPlaceholderText("请输入本地文件夹路径")
        self.local_path_input.setFixedHeight(32)
        self.local_path_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #1890ff;
                outline: none;
            }
        """)
        local_path_layout.addWidget(self.local_path_input)

        browse_btn = QPushButton("浏览文件")
        browse_btn.setFixedHeight(32)
        browse_btn.setStyleSheet("""
            QPushButton {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 6px 16px;
                font-size: 14px;
                background-color: white;
                color: #666;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
            }
        """)
        local_path_layout.addWidget(browse_btn)

        self.local_path_widget.setVisible(False)
        form_layout.addRow("", self.local_path_widget)

        # 截全屏
        self.screenshot_fullscreen = QCheckBox()
        self.screenshot_fullscreen.setChecked(True)
        self.screenshot_fullscreen.setStyleSheet("""
            QCheckBox::indicator {
                width: 50px;
                height: 24px;
                border-radius: 12px;
                background-color: #1890ff;
                border: 1px solid #1890ff;
            }
            QCheckBox::indicator:unchecked {
                background-color: #ccc;
                border-color: #ccc;
            }
            QCheckBox::indicator:checked::before {
                content: "";
                width: 20px;
                height: 20px;
                border-radius: 10px;
                background-color: white;
                position: absolute;
                left: 28px;
                top: 2px;
            }
            QCheckBox::indicator:unchecked::before {
                content: "";
                width: 20px;
                height: 20px;
                border-radius: 10px;
                background-color: white;
                position: absolute;
                left: 2px;
                top: 2px;
            }
        """)
        form_layout.addRow("截全屏", self.screenshot_fullscreen)

        # 图片格式
        self.screenshot_format = QComboBox()
        self.screenshot_format.addItems(["png", "jpeg"])
        self.screenshot_format.setCurrentText("png")
        self.screenshot_format.setFixedHeight(32)
        self.screenshot_format.setStyleSheet("""
            QComboBox {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 14px;
                background-color: white;
                min-width: 100px;
            }
            QComboBox:focus {
                border-color: #1890ff;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666;
                margin-right: 5px;
            }
        """)
        form_layout.addRow("图片格式", self.screenshot_format)

        # 说明
        self.screenshot_description = QLineEdit()
        self.screenshot_description.setPlaceholderText("选填")
        self.screenshot_description.setFixedHeight(32)
        self.screenshot_description.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #1890ff;
                outline: none;
            }
        """)
        form_layout.addRow("说明", self.screenshot_description)

        parent_layout.addLayout(form_layout)

    def on_screenshot_default_folder(self):
        """选择默认文件夹"""
        self.default_folder_btn.setChecked(True)
        self.local_folder_btn.setChecked(False)
        self.local_path_widget.setVisible(False)

    def on_screenshot_local_folder(self):
        """选择本地文件夹"""
        self.default_folder_btn.setChecked(False)
        self.local_folder_btn.setChecked(True)
        self.local_path_widget.setVisible(True)

    def show_screenshot_variables(self):
        """显示变量选择下拉框"""
        # 创建变量下拉框
        dropdown = QWidget()
        dropdown.setWindowFlags(Qt.Popup)
        dropdown.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid #d9d9d9;
                border-radius: 4px;
            }
        """)

        layout = QVBoxLayout(dropdown)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(2)

        # 使用标准变量列表
        variables = self.get_standard_variables()

        for var_name, var_desc, var_type in variables:
            var_text = f"{var_name} - {var_desc} - {var_type}"
            var_btn = QPushButton(var_text)
            var_btn.setFlat(True)
            var_btn.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding: 6px 12px;
                    border: none;
                    background-color: transparent;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background-color: #f5f5f5;
                }
            """)
            var_btn.clicked.connect(lambda checked=False, name=var_name: self.insert_screenshot_variable(name))
            layout.addWidget(var_btn)

        # 计算位置并显示
        button_pos = self.screenshot_name.mapToGlobal(self.screenshot_name.rect().bottomLeft())
        dropdown.move(button_pos.x(), button_pos.y() + 5)
        dropdown.resize(400, 250)
        dropdown.show()

        # 保存引用
        self.screenshot_variable_dropdown = dropdown

    def insert_screenshot_variable(self, variable):
        """插入变量到截图名称输入框"""
        current_text = self.screenshot_name.text()
        cursor_pos = self.screenshot_name.cursorPosition()
        new_text = current_text[:cursor_pos] + f"{{{variable}}}" + current_text[cursor_pos:]
        self.screenshot_name.setText(new_text)
        self.screenshot_name.setFocus()

        # 关闭下拉框
        if hasattr(self, 'screenshot_variable_dropdown'):
            self.screenshot_variable_dropdown.close()



    def create_hover_element_exact_config(self, parent_layout):
        """经过元素 - 完全按照您的截图实现"""

        # 主容器
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(15)

        # 选项卡区域
        tab_widget = QWidget()
        tab_layout = QHBoxLayout(tab_widget)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.setSpacing(0)

        # 元素选择器选项卡
        self.hover_selector_tab = QPushButton("元素选择器")
        self.hover_selector_tab.setCheckable(True)
        self.hover_selector_tab.setChecked(True)
        self.hover_selector_tab.setFixedHeight(32)
        self.hover_selector_tab.setStyleSheet("""
            QPushButton {
                border: 1px solid #d9d9d9;
                border-bottom: none;
                border-radius: 4px 4px 0 0;
                padding: 6px 16px;
                font-size: 14px;
                background-color: #1890ff;
                color: white;
            }
            QPushButton:!checked {
                background-color: #f5f5f5;
                color: #666;
            }
        """)
        self.hover_selector_tab.clicked.connect(self.on_hover_selector_tab)
        tab_layout.addWidget(self.hover_selector_tab)

        # 储存的元素对象选项卡
        self.hover_stored_tab = QPushButton("储存的元素对象")
        self.hover_stored_tab.setCheckable(True)
        self.hover_stored_tab.setFixedHeight(32)
        self.hover_stored_tab.setStyleSheet("""
            QPushButton {
                border: 1px solid #d9d9d9;
                border-bottom: none;
                border-left: none;
                border-radius: 4px 4px 0 0;
                padding: 6px 16px;
                font-size: 14px;
                background-color: #f5f5f5;
                color: #666;
            }
            QPushButton:checked {
                background-color: #1890ff;
                color: white;
            }
        """)
        self.hover_stored_tab.clicked.connect(self.on_hover_stored_tab)
        tab_layout.addWidget(self.hover_stored_tab)

        tab_layout.addStretch()
        main_layout.addWidget(tab_widget)

        # 内容区域
        self.hover_content_widget = QWidget()
        self.hover_content_widget.setStyleSheet("""
            QWidget {
                border: 1px solid #d9d9d9;
                border-radius: 0 4px 4px 4px;
                background-color: white;
                padding: 15px;
            }
        """)
        content_layout = QVBoxLayout(self.hover_content_widget)
        content_layout.setContentsMargins(15, 15, 15, 15)
        content_layout.setSpacing(15)

        # 元素选择器内容
        self.hover_selector_content = QWidget()
        selector_layout = QVBoxLayout(self.hover_selector_content)
        selector_layout.setContentsMargins(0, 0, 0, 0)
        selector_layout.setSpacing(15)

        # 选择器类型
        selector_type_widget = QWidget()
        selector_type_layout = QHBoxLayout(selector_type_widget)
        selector_type_layout.setContentsMargins(0, 0, 0, 0)
        selector_type_layout.setSpacing(15)

        # 选择器标签
        selector_label = QLabel("选择器")
        selector_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 500;")
        selector_type_layout.addWidget(selector_label)

        # 单选按钮组
        from PyQt5.QtWidgets import QRadioButton, QButtonGroup
        self.hover_selector_group = QButtonGroup()

        self.hover_selector_radio = QRadioButton("Selector")
        self.hover_selector_radio.setChecked(True)
        self.hover_selector_radio.setStyleSheet("font-size: 14px; color: #333;")
        self.hover_selector_group.addButton(self.hover_selector_radio)
        selector_type_layout.addWidget(self.hover_selector_radio)

        self.hover_xpath_radio = QRadioButton("XPath")
        self.hover_xpath_radio.setStyleSheet("font-size: 14px; color: #333;")
        self.hover_selector_group.addButton(self.hover_xpath_radio)
        selector_type_layout.addWidget(self.hover_xpath_radio)

        self.hover_text_radio = QRadioButton("文本")
        self.hover_text_radio.setStyleSheet("font-size: 14px; color: #333;")
        self.hover_selector_group.addButton(self.hover_text_radio)
        selector_type_layout.addWidget(self.hover_text_radio)

        selector_type_layout.addStretch()
        selector_layout.addWidget(selector_type_widget)

        # 选择器输入框
        selector_input_widget = QWidget()
        selector_input_layout = QHBoxLayout(selector_input_widget)
        selector_input_layout.setContentsMargins(0, 0, 0, 0)
        selector_input_layout.setSpacing(10)

        self.hover_selector_input = QLineEdit()
        self.hover_selector_input.setPlaceholderText("请输入元素选择器，比如 #email input")
        self.hover_selector_input.setFixedHeight(32)
        self.hover_selector_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #1890ff;
                outline: none;
            }
        """)
        selector_input_layout.addWidget(self.hover_selector_input)

        # 使用变量链接
        hover_use_var_btn = QPushButton("使用变量")
        hover_use_var_btn.setFlat(True)
        hover_use_var_btn.setStyleSheet("""
            QPushButton {
                color: #1890ff;
                background: transparent;
                border: none;
                font-size: 14px;
                padding: 0;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        hover_use_var_btn.clicked.connect(self.show_hover_selector_variables)
        selector_input_layout.addWidget(hover_use_var_btn)

        selector_layout.addWidget(selector_input_widget)

        content_layout.addWidget(self.hover_selector_content)

        # 储存的元素对象内容
        self.hover_stored_content = QWidget()
        stored_layout = QVBoxLayout(self.hover_stored_content)
        stored_layout.setContentsMargins(0, 0, 0, 0)
        stored_layout.setSpacing(15)

        # 元素对象下拉框
        stored_object_widget = QWidget()
        stored_object_layout = QHBoxLayout(stored_object_widget)
        stored_object_layout.setContentsMargins(0, 0, 0, 0)
        stored_object_layout.setSpacing(10)

        # 元素对象标签
        stored_label = QLabel("元素对象")
        stored_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 500; min-width: 80px;")
        stored_object_layout.addWidget(stored_label)

        self.hover_stored_object = QComboBox()
        self.hover_stored_object.addItem("请选择")
        self.hover_stored_object.setFixedHeight(32)
        self.hover_stored_object.setStyleSheet("""
            QComboBox {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 14px;
                background-color: white;
                min-width: 400px;
            }
            QComboBox:focus {
                border-color: #1890ff;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666;
                margin-right: 5px;
            }
        """)
        stored_object_layout.addWidget(self.hover_stored_object)
        stored_object_layout.addStretch()

        stored_layout.addWidget(stored_object_widget)

        # 储存的元素对象选项卡的说明字段
        stored_desc_widget = QWidget()
        stored_desc_layout = QHBoxLayout(stored_desc_widget)
        stored_desc_layout.setContentsMargins(0, 0, 0, 0)
        stored_desc_layout.setSpacing(10)

        stored_desc_label = QLabel("说明")
        stored_desc_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 500; min-width: 80px;")
        stored_desc_layout.addWidget(stored_desc_label)

        self.hover_stored_description = QLineEdit()
        self.hover_stored_description.setPlaceholderText("选填")
        self.hover_stored_description.setFixedHeight(32)
        self.hover_stored_description.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #1890ff;
                outline: none;
            }
        """)
        stored_desc_layout.addWidget(self.hover_stored_description)

        stored_layout.addWidget(stored_desc_widget)

        # 默认隐藏储存的元素对象内容
        self.hover_stored_content.setVisible(False)
        content_layout.addWidget(self.hover_stored_content)

        # 元素顺序（添加到元素选择器内容中）
        order_widget = QWidget()
        order_layout = QHBoxLayout(order_widget)
        order_layout.setContentsMargins(0, 0, 0, 0)
        order_layout.setSpacing(10)

        # 元素顺序标签
        order_label = QLabel("元素顺序")
        order_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 500; min-width: 80px;")
        order_layout.addWidget(order_label)

        # 顺序类型下拉框
        self.hover_order_type = QComboBox()
        self.hover_order_type.addItems(["固定值", "区间随机"])
        self.hover_order_type.setFixedHeight(32)
        self.hover_order_type.setStyleSheet("""
            QComboBox {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 14px;
                background-color: white;
                min-width: 100px;
            }
            QComboBox:focus {
                border-color: #1890ff;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666;
                margin-right: 5px;
            }
        """)
        order_layout.addWidget(self.hover_order_type)

        # 顺序值输入框
        self.hover_order_value = QSpinBox()
        self.hover_order_value.setMinimum(1)
        self.hover_order_value.setValue(1)
        self.hover_order_value.setFixedHeight(32)
        self.hover_order_value.setStyleSheet("""
            QSpinBox {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 14px;
                background-color: white;
                min-width: 80px;
            }
            QSpinBox:focus {
                border-color: #1890ff;
            }
        """)
        order_layout.addWidget(self.hover_order_value)

        # 使用变量链接
        hover_order_var_btn = QPushButton("使用变量")
        hover_order_var_btn.setFlat(True)
        hover_order_var_btn.setStyleSheet("""
            QPushButton {
                color: #1890ff;
                background: transparent;
                border: none;
                font-size: 14px;
                padding: 0;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        hover_order_var_btn.clicked.connect(self.show_hover_order_variables)
        order_layout.addWidget(hover_order_var_btn)

        order_layout.addStretch()
        selector_layout.addWidget(order_widget)

        # 元素选择器选项卡的说明字段
        selector_desc_widget = QWidget()
        selector_desc_layout = QHBoxLayout(selector_desc_widget)
        selector_desc_layout.setContentsMargins(0, 0, 0, 0)
        selector_desc_layout.setSpacing(10)

        selector_desc_label = QLabel("说明")
        selector_desc_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 500; min-width: 80px;")
        selector_desc_layout.addWidget(selector_desc_label)

        self.hover_selector_description = QLineEdit()
        self.hover_selector_description.setPlaceholderText("选填")
        self.hover_selector_description.setFixedHeight(32)
        self.hover_selector_description.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #1890ff;
                outline: none;
            }
        """)
        selector_desc_layout.addWidget(self.hover_selector_description)

        selector_layout.addWidget(selector_desc_widget)

        main_layout.addWidget(self.hover_content_widget)
        parent_layout.addWidget(main_widget)

    def on_hover_selector_tab(self):
        """切换到元素选择器选项卡"""
        self.hover_selector_tab.setChecked(True)
        self.hover_stored_tab.setChecked(False)
        self.hover_selector_content.setVisible(True)
        self.hover_stored_content.setVisible(False)

    def on_hover_stored_tab(self):
        """切换到储存的元素对象选项卡"""
        self.hover_selector_tab.setChecked(False)
        self.hover_stored_tab.setChecked(True)
        self.hover_selector_content.setVisible(False)
        self.hover_stored_content.setVisible(True)

    def show_hover_selector_variables(self):
        """显示选择器变量下拉框"""
        self.show_simple_variable_menu(self.hover_selector_input)

    def show_hover_order_variables(self):
        """显示元素顺序变量下拉框"""
        self.show_simple_variable_menu(self.hover_order_value)

    def get_standard_variables(self):
        """获取标准变量列表 - 所有RPA功能统一使用"""
        return [
            ("task_id", "<任务ID>", "字符串"),
            ("task_name", "<任务名称>", "字符串"),
            ("serial_number", "<环境编号>", "字符串"),
            ("browser_name", "<环境名称>", "字符串"),
            ("acc_id", "<环境ID>", "字符串"),
            ("comment", "<环境备注>", "字符串"),
            ("user_name", "<平台账户>", "字符串"),
            ("password", "<平台密码>", "字符串"),
            ("cookies", "<环境cookies>", "字符串")
        ]

    def show_simple_variable_menu(self, target_widget):
        """显示简单的变量菜单"""
        from PyQt5.QtWidgets import QMenu

        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 4px;
            }
            QMenu::item {
                padding: 6px 12px;
                font-size: 13px;
                color: #333;
            }
            QMenu::item:hover {
                background-color: #f0f0f0;
            }
        """)

        # 使用标准变量列表
        variables = self.get_standard_variables()

        for var_name, var_desc, var_type in variables:
            action = menu.addAction(f"{var_name} - {var_desc} - {var_type}")
            action.triggered.connect(lambda checked, name=var_name: self.insert_simple_variable(target_widget, name))

        # 在按钮下方显示菜单
        try:
            if hasattr(target_widget, 'mapToGlobal'):
                button_pos = target_widget.mapToGlobal(target_widget.rect().bottomLeft())
                menu.exec_(button_pos)
            else:
                menu.exec_(target_widget.parent().mapToGlobal(target_widget.parent().rect().bottomLeft()))
        except:
            menu.exec_()

    def insert_simple_variable(self, target_widget, variable):
        """插入变量到目标控件 - 简化版本"""
        if isinstance(target_widget, QLineEdit):
            current_text = target_widget.text()
            cursor_pos = target_widget.cursorPosition()
            new_text = current_text[:cursor_pos] + f"{{{variable}}}" + current_text[cursor_pos:]
            target_widget.setText(new_text)
            target_widget.setFocus()
        elif isinstance(target_widget, QSpinBox):
            # 对于数字输入框，设置为变量引用
            target_widget.setValue(0)
            target_widget.setSpecialValueText(f"{{{variable}}}")

    def show_variable_dropdown(self, target_widget, dropdown_type):
        """通用变量下拉框显示方法"""
        # 关闭已存在的下拉框
        existing_dropdown = getattr(self, f'{dropdown_type}_variable_dropdown', None)
        if existing_dropdown:
            existing_dropdown.close()

        # 创建变量下拉框 - 使用QComboBox的弹出样式
        dropdown = QWidget(self)
        dropdown.setWindowFlags(Qt.Popup)
        dropdown.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            }
        """)

        layout = QVBoxLayout(dropdown)
        layout.setContentsMargins(1, 1, 1, 1)
        layout.setSpacing(0)

        # 使用标准变量列表
        variables = self.get_standard_variables()

        for var_name, var_desc, var_type in variables:
            var_btn = QPushButton(f"{var_name} - {var_desc} - {var_type}")
            var_btn.setFlat(True)
            var_btn.setFixedHeight(28)
            var_btn.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding: 4px 8px;
                    border: none;
                    background-color: transparent;
                    font-size: 12px;
                    color: #333;
                }
                QPushButton:hover {
                    background-color: #f0f0f0;
                }
            """)
            var_btn.clicked.connect(lambda checked, name=var_name: self.insert_variable(target_widget, name, dropdown_type))
            layout.addWidget(var_btn)

        # 计算位置并显示 - 在目标控件下方
        try:
            if hasattr(target_widget, 'mapToGlobal'):
                widget_pos = target_widget.mapToGlobal(target_widget.rect().bottomLeft())
                dropdown.move(widget_pos.x(), widget_pos.y() + 2)
            else:
                # 如果是SpinBox，使用父控件位置
                parent_widget = target_widget.parent()
                if parent_widget:
                    widget_pos = parent_widget.mapToGlobal(parent_widget.rect().bottomLeft())
                    dropdown.move(widget_pos.x(), widget_pos.y() + 35)
        except:
            # 如果位置计算失败，使用默认位置
            dropdown.move(100, 100)

        # 设置合适的大小
        dropdown.resize(300, min(len(variables) * 28 + 2, 200))
        dropdown.show()
        dropdown.raise_()

        # 保存引用
        setattr(self, f'{dropdown_type}_variable_dropdown', dropdown)

    def insert_variable(self, target_widget, variable, dropdown_type):
        """插入变量到目标控件"""
        if isinstance(target_widget, QLineEdit):
            current_text = target_widget.text()
            cursor_pos = target_widget.cursorPosition()
            new_text = current_text[:cursor_pos] + f"{{{variable}}}" + current_text[cursor_pos:]
            target_widget.setText(new_text)
            target_widget.setFocus()
        elif isinstance(target_widget, QSpinBox):
            # 对于数字输入框，设置为变量引用
            target_widget.setValue(0)
            target_widget.setSpecialValueText(f"{{{variable}}}")

        # 关闭下拉框
        dropdown = getattr(self, f'{dropdown_type}_variable_dropdown', None)
        if dropdown:
            dropdown.close()
            delattr(self, f'{dropdown_type}_variable_dropdown')

    def create_wait_time_exact_config(self, parent_layout):
        """等待时间 - 完全按照AdsPower原版界面"""
        config_group = QGroupBox("等待时间设置")
        config_layout = QFormLayout(config_group)

        # 等待时间
        self.wait_time = QSpinBox()
        self.wait_time.setRange(100, 300000)  # 100毫秒到5分钟
        self.wait_time.setValue(1000)
        self.wait_time.setSuffix(" 毫秒")
        self.wait_time.setStyleSheet(self.get_input_style())
        config_layout.addRow("等待时间:", self.wait_time)

        # 说明文本
        info_label = QLabel("让流程暂停指定时间，然后再执行下面的流程")
        info_label.setStyleSheet("color: #666666; font-size: 12px; margin-top: 10px;")
        config_layout.addRow("", info_label)

        parent_layout.addWidget(config_group)

    def get_input_style(self):
        """获取输入框样式"""
        return """
            QLineEdit, QComboBox, QSpinBox, QTextEdit {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 8px;
                font-size: 13px;
                background-color: white;
                min-height: 20px;
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QTextEdit:focus {
                border-color: #1890ff;
                outline: none;
            }
        """

    def create_click_element_exact_config(self, parent_layout):
        """点击元素 - 完全按照您的截图实现"""

        # 主容器
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(15)

        # 选项卡区域
        tab_widget = QWidget()
        tab_layout = QHBoxLayout(tab_widget)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.setSpacing(0)

        # 元素选择器选项卡
        self.click_selector_tab = QPushButton("元素选择器")
        self.click_selector_tab.setCheckable(True)
        self.click_selector_tab.setChecked(True)
        self.click_selector_tab.setFixedHeight(32)
        self.click_selector_tab.setStyleSheet("""
            QPushButton {
                border: 1px solid #d9d9d9;
                border-bottom: none;
                border-radius: 4px 4px 0 0;
                padding: 6px 16px;
                font-size: 14px;
                background-color: #1890ff;
                color: white;
            }
            QPushButton:!checked {
                background-color: #f5f5f5;
                color: #666;
            }
        """)
        self.click_selector_tab.clicked.connect(self.on_click_selector_tab)
        tab_layout.addWidget(self.click_selector_tab)

        # 储存的元素对象选项卡
        self.click_stored_tab = QPushButton("储存的元素对象")
        self.click_stored_tab.setCheckable(True)
        self.click_stored_tab.setFixedHeight(32)
        self.click_stored_tab.setStyleSheet("""
            QPushButton {
                border: 1px solid #d9d9d9;
                border-bottom: none;
                border-left: none;
                border-radius: 4px 4px 0 0;
                padding: 6px 16px;
                font-size: 14px;
                background-color: #f5f5f5;
                color: #666;
            }
            QPushButton:checked {
                background-color: #1890ff;
                color: white;
            }
        """)
        self.click_stored_tab.clicked.connect(self.on_click_stored_tab)
        tab_layout.addWidget(self.click_stored_tab)

        tab_layout.addStretch()
        main_layout.addWidget(tab_widget)

        # 内容区域
        self.click_content_widget = QWidget()
        self.click_content_widget.setStyleSheet("""
            QWidget {
                border: 1px solid #d9d9d9;
                border-radius: 0 4px 4px 4px;
                background-color: white;
                padding: 15px;
            }
        """)
        content_layout = QVBoxLayout(self.click_content_widget)
        content_layout.setContentsMargins(15, 15, 15, 15)
        content_layout.setSpacing(15)

        # 元素选择器内容
        self.click_selector_content = QWidget()
        selector_layout = QVBoxLayout(self.click_selector_content)
        selector_layout.setContentsMargins(0, 0, 0, 0)
        selector_layout.setSpacing(15)

        # 选择器类型
        selector_type_widget = QWidget()
        selector_type_layout = QHBoxLayout(selector_type_widget)
        selector_type_layout.setContentsMargins(0, 0, 0, 0)
        selector_type_layout.setSpacing(15)

        # 选择器标签
        selector_label = QLabel("选择器")
        selector_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 500;")
        selector_type_layout.addWidget(selector_label)

        # 单选按钮组
        from PyQt5.QtWidgets import QRadioButton, QButtonGroup
        self.click_selector_group = QButtonGroup()

        self.click_selector_radio = QRadioButton("Selector")
        self.click_selector_radio.setChecked(True)
        self.click_selector_radio.setStyleSheet("font-size: 14px; color: #333;")
        self.click_selector_group.addButton(self.click_selector_radio)
        selector_type_layout.addWidget(self.click_selector_radio)

        self.click_xpath_radio = QRadioButton("XPath")
        self.click_xpath_radio.setStyleSheet("font-size: 14px; color: #333;")
        self.click_selector_group.addButton(self.click_xpath_radio)
        selector_type_layout.addWidget(self.click_xpath_radio)

        self.click_text_radio = QRadioButton("文本")
        self.click_text_radio.setStyleSheet("font-size: 14px; color: #333;")
        self.click_selector_group.addButton(self.click_text_radio)
        selector_type_layout.addWidget(self.click_text_radio)

        selector_type_layout.addStretch()
        selector_layout.addWidget(selector_type_widget)

        # 选择器输入框
        selector_input_widget = QWidget()
        selector_input_layout = QHBoxLayout(selector_input_widget)
        selector_input_layout.setContentsMargins(0, 0, 0, 0)
        selector_input_layout.setSpacing(10)

        self.click_selector_input = QLineEdit()
        self.click_selector_input.setPlaceholderText("请输入元素选择器，比如 #email input")
        self.click_selector_input.setFixedHeight(32)
        self.click_selector_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #1890ff;
                outline: none;
            }
        """)
        selector_input_layout.addWidget(self.click_selector_input)

        # 使用变量链接
        click_use_var_btn = QPushButton("使用变量")
        click_use_var_btn.setFlat(True)
        click_use_var_btn.setStyleSheet("""
            QPushButton {
                color: #1890ff;
                background: transparent;
                border: none;
                font-size: 14px;
                padding: 0;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        click_use_var_btn.clicked.connect(self.show_click_selector_variables)
        selector_input_layout.addWidget(click_use_var_btn)

        selector_layout.addWidget(selector_input_widget)

        # 元素顺序（添加到元素选择器内容中）
        order_widget = QWidget()
        order_layout = QHBoxLayout(order_widget)
        order_layout.setContentsMargins(0, 0, 0, 0)
        order_layout.setSpacing(10)

        # 元素顺序标签
        order_label = QLabel("元素顺序")
        order_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 500; min-width: 80px;")
        order_layout.addWidget(order_label)

        # 顺序类型下拉框
        self.click_order_type = QComboBox()
        self.click_order_type.addItems(["固定值", "区间随机"])
        self.click_order_type.setFixedHeight(32)
        self.click_order_type.setStyleSheet("""
            QComboBox {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 14px;
                background-color: white;
                min-width: 100px;
            }
            QComboBox:focus {
                border-color: #1890ff;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666;
                margin-right: 5px;
            }
        """)
        order_layout.addWidget(self.click_order_type)

        # 顺序值输入框
        self.click_order_value = QSpinBox()
        self.click_order_value.setMinimum(1)
        self.click_order_value.setValue(1)
        self.click_order_value.setFixedHeight(32)
        self.click_order_value.setStyleSheet("""
            QSpinBox {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 14px;
                background-color: white;
                min-width: 80px;
            }
            QSpinBox:focus {
                border-color: #1890ff;
            }
        """)
        order_layout.addWidget(self.click_order_value)

        # 使用变量链接
        click_order_var_btn = QPushButton("使用变量")
        click_order_var_btn.setFlat(True)
        click_order_var_btn.setStyleSheet("""
            QPushButton {
                color: #1890ff;
                background: transparent;
                border: none;
                font-size: 14px;
                padding: 0;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        click_order_var_btn.clicked.connect(self.show_click_order_variables)
        order_layout.addWidget(click_order_var_btn)

        order_layout.addStretch()
        selector_layout.addWidget(order_widget)

        # 点击类型（添加到元素选择器内容中）
        click_type_widget = QWidget()
        click_type_layout = QHBoxLayout(click_type_widget)
        click_type_layout.setContentsMargins(0, 0, 0, 0)
        click_type_layout.setSpacing(10)

        # 点击类型标签
        click_type_label = QLabel("点击类型")
        click_type_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 500; min-width: 80px;")
        click_type_layout.addWidget(click_type_label)

        # 点击类型下拉框
        self.click_type = QComboBox()
        self.click_type.addItems(["左键", "中键", "右键"])
        self.click_type.setFixedHeight(32)
        self.click_type.setStyleSheet("""
            QComboBox {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 14px;
                background-color: white;
                min-width: 100px;
            }
            QComboBox:focus {
                border-color: #1890ff;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666;
                margin-right: 5px;
            }
        """)
        click_type_layout.addWidget(self.click_type)

        click_type_layout.addStretch()
        selector_layout.addWidget(click_type_widget)

        # 按键类型（添加到元素选择器内容中）
        key_type_widget = QWidget()
        key_type_layout = QHBoxLayout(key_type_widget)
        key_type_layout.setContentsMargins(0, 0, 0, 0)
        key_type_layout.setSpacing(10)

        # 按键类型标签
        key_type_label = QLabel("按键类型")
        key_type_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 500; min-width: 80px;")
        key_type_layout.addWidget(key_type_label)

        # 按键类型下拉框
        self.click_action = QComboBox()
        self.click_action.addItems(["单击", "双击"])
        self.click_action.setFixedHeight(32)
        self.click_action.setStyleSheet("""
            QComboBox {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 14px;
                background-color: white;
                min-width: 100px;
            }
            QComboBox:focus {
                border-color: #1890ff;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666;
                margin-right: 5px;
            }
        """)
        key_type_layout.addWidget(self.click_action)

        key_type_layout.addStretch()
        selector_layout.addWidget(key_type_widget)

        # 将元素选择器内容添加到主内容区域
        content_layout.addWidget(self.click_selector_content)

        # 储存的元素对象内容
        self.click_stored_content = QWidget()
        stored_layout = QVBoxLayout(self.click_stored_content)
        stored_layout.setContentsMargins(0, 0, 0, 0)
        stored_layout.setSpacing(15)

        # 元素对象下拉框
        stored_object_widget = QWidget()
        stored_object_layout = QHBoxLayout(stored_object_widget)
        stored_object_layout.setContentsMargins(0, 0, 0, 0)
        stored_object_layout.setSpacing(10)

        # 元素对象标签
        stored_label = QLabel("元素对象")
        stored_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 500; min-width: 80px;")
        stored_object_layout.addWidget(stored_label)

        self.click_stored_object = QComboBox()
        self.click_stored_object.addItem("请选择")
        self.click_stored_object.setFixedHeight(32)
        self.click_stored_object.setStyleSheet("""
            QComboBox {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 14px;
                background-color: white;
                min-width: 400px;
            }
            QComboBox:focus {
                border-color: #1890ff;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666;
                margin-right: 5px;
            }
        """)
        stored_object_layout.addWidget(self.click_stored_object)
        stored_object_layout.addStretch()

        stored_layout.addWidget(stored_object_widget)

        # 储存的元素对象选项卡中的点击类型
        stored_click_type_widget = QWidget()
        stored_click_type_layout = QHBoxLayout(stored_click_type_widget)
        stored_click_type_layout.setContentsMargins(0, 0, 0, 0)
        stored_click_type_layout.setSpacing(10)

        # 点击类型标签
        stored_click_type_label = QLabel("点击类型")
        stored_click_type_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 500; min-width: 80px;")
        stored_click_type_layout.addWidget(stored_click_type_label)

        # 点击类型下拉框（储存的元素对象选项卡）
        self.click_stored_type = QComboBox()
        self.click_stored_type.addItems(["左键", "中键", "右键"])
        self.click_stored_type.setFixedHeight(32)
        self.click_stored_type.setStyleSheet("""
            QComboBox {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 14px;
                background-color: white;
                min-width: 100px;
            }
            QComboBox:focus {
                border-color: #1890ff;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666;
                margin-right: 5px;
            }
        """)
        stored_click_type_layout.addWidget(self.click_stored_type)

        stored_click_type_layout.addStretch()
        stored_layout.addWidget(stored_click_type_widget)

        # 储存的元素对象选项卡中的按键类型
        stored_key_type_widget = QWidget()
        stored_key_type_layout = QHBoxLayout(stored_key_type_widget)
        stored_key_type_layout.setContentsMargins(0, 0, 0, 0)
        stored_key_type_layout.setSpacing(10)

        # 按键类型标签
        stored_key_type_label = QLabel("按键类型")
        stored_key_type_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 500; min-width: 80px;")
        stored_key_type_layout.addWidget(stored_key_type_label)

        # 按键类型下拉框（储存的元素对象选项卡）
        self.click_stored_action = QComboBox()
        self.click_stored_action.addItems(["单击", "双击"])
        self.click_stored_action.setFixedHeight(32)
        self.click_stored_action.setStyleSheet("""
            QComboBox {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 14px;
                background-color: white;
                min-width: 100px;
            }
            QComboBox:focus {
                border-color: #1890ff;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666;
                margin-right: 5px;
            }
        """)
        stored_key_type_layout.addWidget(self.click_stored_action)

        stored_key_type_layout.addStretch()
        stored_layout.addWidget(stored_key_type_widget)

        # 默认隐藏储存的元素对象内容
        self.click_stored_content.setVisible(False)
        content_layout.addWidget(self.click_stored_content)

        # 说明字段（共享）
        desc_widget = QWidget()
        desc_layout = QHBoxLayout(desc_widget)
        desc_layout.setContentsMargins(0, 0, 0, 0)
        desc_layout.setSpacing(10)

        desc_label = QLabel("说明")
        desc_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 500; min-width: 80px;")
        desc_layout.addWidget(desc_label)

        self.click_description = QLineEdit()
        self.click_description.setPlaceholderText("选填")
        self.click_description.setFixedHeight(32)
        self.click_description.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #1890ff;
                outline: none;
            }
        """)
        desc_layout.addWidget(self.click_description)

        content_layout.addWidget(desc_widget)

        main_layout.addWidget(self.click_content_widget)
        parent_layout.addWidget(main_widget)

    def on_click_selector_tab(self):
        """切换到元素选择器选项卡"""
        self.click_selector_tab.setChecked(True)
        self.click_stored_tab.setChecked(False)
        self.click_selector_content.setVisible(True)
        self.click_stored_content.setVisible(False)

    def on_click_stored_tab(self):
        """切换到储存的元素对象选项卡"""
        self.click_selector_tab.setChecked(False)
        self.click_stored_tab.setChecked(True)
        self.click_selector_content.setVisible(False)
        self.click_stored_content.setVisible(True)

    def show_click_selector_variables(self):
        """显示选择器变量下拉框"""
        self.show_simple_variable_menu(self.click_selector_input)

    def show_click_order_variables(self):
        """显示元素顺序变量下拉框"""
        self.show_simple_variable_menu(self.click_order_value)

    def create_input_content_exact_config(self, parent_layout):
        """输入内容 - 完全按照您的截图实现"""

        # 顶部提示信息
        info_widget = QWidget()
        info_widget.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 8px 12px;
                margin-bottom: 15px;
            }
        """)
        info_layout = QHBoxLayout(info_widget)
        info_layout.setContentsMargins(8, 8, 8, 8)
        info_layout.setSpacing(8)

        # 信息图标
        info_icon = QLabel("ⓘ")
        info_icon.setStyleSheet("color: #1890ff; font-size: 14px; font-weight: bold;")
        info_layout.addWidget(info_icon)

        # 信息文本
        info_text = QLabel("在指定元素内输入内容")
        info_text.setStyleSheet("color: #666; font-size: 13px;")
        info_layout.addWidget(info_text)

        # 了解详情链接
        detail_link = QPushButton("了解详情")
        detail_link.setFlat(True)
        detail_link.setStyleSheet("""
            QPushButton {
                color: #1890ff;
                background: transparent;
                border: none;
                font-size: 13px;
                padding: 0;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        info_layout.addWidget(detail_link)
        info_layout.addStretch()

        parent_layout.addWidget(info_widget)

        # 选项卡区域
        tab_widget = QWidget()
        tab_layout = QHBoxLayout(tab_widget)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.setSpacing(2)

        # 元素选择器选项卡
        self.input_selector_tab = QPushButton("元素选择器")
        self.input_selector_tab.setCheckable(True)
        self.input_selector_tab.setChecked(True)
        self.input_selector_tab.setFixedHeight(35)
        self.input_selector_tab.setStyleSheet("""
            QPushButton {
                border: 1px solid #d9d9d9;
                border-bottom: none;
                border-radius: 6px 6px 0 0;
                padding: 8px 20px;
                font-size: 13px;
                background-color: #1890ff;
                color: white;
                font-weight: 500;
            }
            QPushButton:!checked {
                background-color: #f8f9fa;
                color: #666;
            }
        """)
        self.input_selector_tab.clicked.connect(self.on_input_selector_tab)
        tab_layout.addWidget(self.input_selector_tab)

        # 储存的元素对象选项卡
        self.input_stored_tab = QPushButton("储存的元素对象")
        self.input_stored_tab.setCheckable(True)
        self.input_stored_tab.setFixedHeight(35)
        self.input_stored_tab.setStyleSheet("""
            QPushButton {
                border: 1px solid #d9d9d9;
                border-bottom: none;
                border-left: none;
                border-radius: 6px 6px 0 0;
                padding: 8px 20px;
                font-size: 13px;
                background-color: #f8f9fa;
                color: #666;
                font-weight: 500;
            }
            QPushButton:checked {
                background-color: #1890ff;
                color: white;
            }
        """)
        self.input_stored_tab.clicked.connect(self.on_input_stored_tab)
        tab_layout.addWidget(self.input_stored_tab)

        tab_layout.addStretch()
        parent_layout.addWidget(tab_widget)

        # 内容区域
        self.input_content_widget = QWidget()
        self.input_content_widget.setStyleSheet("""
            QWidget {
                border: 1px solid #d9d9d9;
                border-radius: 0 6px 6px 6px;
                background-color: white;
            }
        """)
        content_layout = QVBoxLayout(self.input_content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)

        # 元素选择器内容
        self.input_selector_content = QWidget()
        selector_layout = QVBoxLayout(self.input_selector_content)
        selector_layout.setContentsMargins(0, 0, 0, 0)
        selector_layout.setSpacing(18)

        # 选择器类型行
        selector_type_widget = QWidget()
        selector_type_layout = QHBoxLayout(selector_type_widget)
        selector_type_layout.setContentsMargins(0, 0, 0, 0)
        selector_type_layout.setSpacing(20)

        # 选择器标签
        selector_label = QLabel("选择器")
        selector_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 500; min-width: 60px;")
        selector_type_layout.addWidget(selector_label)

        # 单选按钮组
        from PyQt5.QtWidgets import QRadioButton, QButtonGroup
        self.input_selector_group = QButtonGroup()

        self.input_selector_radio = QRadioButton("Selector")
        self.input_selector_radio.setChecked(True)
        self.input_selector_radio.setStyleSheet("""
            QRadioButton {
                font-size: 14px;
                color: #333;
                spacing: 8px;
            }
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
            }
        """)
        self.input_selector_group.addButton(self.input_selector_radio)
        selector_type_layout.addWidget(self.input_selector_radio)

        self.input_xpath_radio = QRadioButton("XPath")
        self.input_xpath_radio.setStyleSheet("""
            QRadioButton {
                font-size: 14px;
                color: #333;
                spacing: 8px;
            }
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
            }
        """)
        self.input_selector_group.addButton(self.input_xpath_radio)
        selector_type_layout.addWidget(self.input_xpath_radio)

        self.input_text_radio = QRadioButton("文本")
        self.input_text_radio.setStyleSheet("""
            QRadioButton {
                font-size: 14px;
                color: #333;
                spacing: 8px;
            }
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
            }
        """)
        self.input_selector_group.addButton(self.input_text_radio)
        selector_type_layout.addWidget(self.input_text_radio)

        selector_type_layout.addStretch()
        selector_layout.addWidget(selector_type_widget)

        # 选择器输入框行
        selector_input_widget = QWidget()
        selector_input_layout = QHBoxLayout(selector_input_widget)
        selector_input_layout.setContentsMargins(0, 0, 0, 0)
        selector_input_layout.setSpacing(12)

        self.input_selector_input = QLineEdit()
        self.input_selector_input.setPlaceholderText("请输入元素选择器，比如 #email input")
        self.input_selector_input.setFixedHeight(36)
        self.input_selector_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #1890ff;
                outline: none;
            }
        """)
        selector_input_layout.addWidget(self.input_selector_input)

        # 使用变量链接
        input_use_var_btn = QPushButton("使用变量")
        input_use_var_btn.setFlat(True)
        input_use_var_btn.setStyleSheet("""
            QPushButton {
                color: #1890ff;
                background: transparent;
                border: none;
                font-size: 14px;
                padding: 4px 8px;
                text-decoration: none;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        input_use_var_btn.clicked.connect(self.show_input_selector_variables)
        selector_input_layout.addWidget(input_use_var_btn)

        selector_layout.addWidget(selector_input_widget)

        # 元素顺序行
        order_widget = QWidget()
        order_layout = QHBoxLayout(order_widget)
        order_layout.setContentsMargins(0, 0, 0, 0)
        order_layout.setSpacing(12)

        # 元素顺序标签
        order_label = QLabel("元素顺序")
        order_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 500; min-width: 80px;")
        order_layout.addWidget(order_label)

        # 顺序值输入框
        self.input_order_value = QSpinBox()
        self.input_order_value.setMinimum(1)
        self.input_order_value.setValue(1)
        self.input_order_value.setFixedHeight(36)
        self.input_order_value.setFixedWidth(100)
        self.input_order_value.setStyleSheet("""
            QSpinBox {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 14px;
                background-color: white;
            }
            QSpinBox:focus {
                border-color: #1890ff;
            }
        """)
        order_layout.addWidget(self.input_order_value)

        # 使用变量链接
        input_order_var_btn = QPushButton("使用变量")
        input_order_var_btn.setFlat(True)
        input_order_var_btn.setStyleSheet("""
            QPushButton {
                color: #1890ff;
                background: transparent;
                border: none;
                font-size: 14px;
                padding: 4px 8px;
                text-decoration: none;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        input_order_var_btn.clicked.connect(self.show_input_order_variables)
        order_layout.addWidget(input_order_var_btn)

        order_layout.addStretch()
        selector_layout.addWidget(order_widget)

        # 内容类型按钮组行
        content_type_widget = QWidget()
        content_type_layout = QHBoxLayout(content_type_widget)
        content_type_layout.setContentsMargins(0, 0, 0, 0)
        content_type_layout.setSpacing(12)

        # 内容类型按钮组
        self.input_content_type_group = QButtonGroup()

        # 顺序选取按钮
        self.input_sequential_btn = QPushButton("顺序选取")
        self.input_sequential_btn.setCheckable(True)
        self.input_sequential_btn.setChecked(True)
        self.input_sequential_btn.setFixedHeight(36)
        self.input_sequential_btn.setFixedWidth(90)
        self.input_sequential_btn.setStyleSheet("""
            QPushButton {
                border: 1px solid #1890ff;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 14px;
                background-color: #1890ff;
                color: white;
                font-weight: 500;
            }
            QPushButton:!checked {
                background-color: white;
                color: #1890ff;
            }
            QPushButton:hover {
                background-color: #40a9ff;
            }
        """)
        self.input_sequential_btn.clicked.connect(self.on_input_sequential_mode)
        self.input_content_type_group.addButton(self.input_sequential_btn)
        content_type_layout.addWidget(self.input_sequential_btn)

        # 随机选取按钮
        self.input_random_btn = QPushButton("随机选取")
        self.input_random_btn.setCheckable(True)
        self.input_random_btn.setFixedHeight(36)
        self.input_random_btn.setFixedWidth(90)
        self.input_random_btn.setStyleSheet("""
            QPushButton {
                border: 1px solid #1890ff;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 14px;
                background-color: white;
                color: #1890ff;
                font-weight: 500;
            }
            QPushButton:checked {
                background-color: #1890ff;
                color: white;
            }
            QPushButton:hover {
                background-color: #40a9ff;
                color: white;
            }
        """)
        self.input_random_btn.clicked.connect(self.on_input_random_mode)
        self.input_content_type_group.addButton(self.input_random_btn)
        content_type_layout.addWidget(self.input_random_btn)

        # 随机取数按钮
        self.input_random_num_btn = QPushButton("随机取数")
        self.input_random_num_btn.setCheckable(True)
        self.input_random_num_btn.setFixedHeight(36)
        self.input_random_num_btn.setFixedWidth(90)
        self.input_random_num_btn.setStyleSheet("""
            QPushButton {
                border: 1px solid #1890ff;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 14px;
                background-color: white;
                color: #1890ff;
                font-weight: 500;
            }
            QPushButton:checked {
                background-color: #1890ff;
                color: white;
            }
            QPushButton:hover {
                background-color: #40a9ff;
                color: white;
            }
        """)
        self.input_random_num_btn.clicked.connect(self.on_input_random_num_mode)
        self.input_content_type_group.addButton(self.input_random_num_btn)
        content_type_layout.addWidget(self.input_random_num_btn)

        # 清除内容后输入复选框
        self.input_clear_first = QCheckBox("清除内容后输入")
        self.input_clear_first.setChecked(True)
        self.input_clear_first.setStyleSheet("""
            QCheckBox {
                font-size: 14px;
                color: #333;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 1px solid #d9d9d9;
                border-radius: 3px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #1890ff;
                border-color: #1890ff;
            }
        """)
        content_type_layout.addWidget(self.input_clear_first)

        content_type_layout.addStretch()
        selector_layout.addWidget(content_type_widget)

        # 内容标签
        content_label_widget = QWidget()
        content_label_layout = QHBoxLayout(content_label_widget)
        content_label_layout.setContentsMargins(0, 0, 0, 0)
        content_label_layout.setSpacing(0)

        content_label = QLabel("* 内容")
        content_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 500;")
        content_label_layout.addWidget(content_label)
        content_label_layout.addStretch()

        selector_layout.addWidget(content_label_widget)

        # 内容输入区域（根据模式切换）
        # 顺序选取/随机选取模式的内容输入框
        self.input_content_text = QTextEdit()
        self.input_content_text.setFixedHeight(120)
        self.input_content_text.setPlaceholderText("单个内容请在一行输入；\n多个内容请换行输入，会依取其中一个内容，示例：\n内容一\n内容二\n内容最多 50 行，每行最多 500 个字符")
        self.input_content_text.setStyleSheet("""
            QTextEdit {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 12px;
                font-size: 14px;
                background-color: white;
                font-family: 'Microsoft YaHei', sans-serif;
                line-height: 1.4;
            }
            QTextEdit:focus {
                border-color: #1890ff;
                outline: none;
            }
        """)
        selector_layout.addWidget(self.input_content_text)

        # 随机取数模式的内容输入框（默认隐藏）
        self.input_content_range = QWidget()
        range_layout = QHBoxLayout(self.input_content_range)
        range_layout.setContentsMargins(0, 0, 0, 0)
        range_layout.setSpacing(12)

        self.input_range_min = QLineEdit()
        self.input_range_min.setPlaceholderText("0.1")
        self.input_range_min.setFixedHeight(36)
        self.input_range_min.setFixedWidth(100)
        self.input_range_min.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #1890ff;
                outline: none;
            }
        """)
        range_layout.addWidget(self.input_range_min)

        range_separator = QLabel("-")
        range_separator.setStyleSheet("font-size: 16px; color: #333; font-weight: bold;")
        range_layout.addWidget(range_separator)

        self.input_range_max = QLineEdit()
        self.input_range_max.setPlaceholderText("10")
        self.input_range_max.setFixedHeight(36)
        self.input_range_max.setFixedWidth(100)
        self.input_range_max.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #1890ff;
                outline: none;
            }
        """)
        range_layout.addWidget(self.input_range_max)

        range_layout.addStretch()
        self.input_content_range.setVisible(False)
        selector_layout.addWidget(self.input_content_range)

        # 使用变量按钮（内容区域）
        content_var_widget = QWidget()
        content_var_layout = QHBoxLayout(content_var_widget)
        content_var_layout.setContentsMargins(0, 0, 0, 0)
        content_var_layout.setSpacing(0)

        content_var_layout.addStretch()
        input_content_var_btn = QPushButton("使用变量")
        input_content_var_btn.setFlat(True)
        input_content_var_btn.setStyleSheet("""
            QPushButton {
                color: #1890ff;
                background: transparent;
                border: none;
                font-size: 14px;
                padding: 4px 8px;
                text-decoration: none;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        input_content_var_btn.clicked.connect(self.show_input_content_variables)
        content_var_layout.addWidget(input_content_var_btn)

        selector_layout.addWidget(content_var_widget)

        # 输入间隔时间行
        interval_widget = QWidget()
        interval_layout = QHBoxLayout(interval_widget)
        interval_layout.setContentsMargins(0, 0, 0, 0)
        interval_layout.setSpacing(12)

        # 输入间隔时间标签
        interval_label = QLabel("输入间隔时间")
        interval_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 500; min-width: 100px;")
        interval_layout.addWidget(interval_label)

        # 输入间隔时间输入框
        self.input_interval = QSpinBox()
        self.input_interval.setRange(0, 10000)
        self.input_interval.setValue(300)
        self.input_interval.setSuffix(" 毫秒")
        self.input_interval.setFixedHeight(36)
        self.input_interval.setFixedWidth(150)
        self.input_interval.setStyleSheet("""
            QSpinBox {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 14px;
                background-color: white;
            }
            QSpinBox:focus {
                border-color: #1890ff;
            }
        """)
        interval_layout.addWidget(self.input_interval)

        # 毫秒说明
        interval_note = QLabel("1 秒 = 1000 毫秒")
        interval_note.setStyleSheet("font-size: 13px; color: #999;")
        interval_layout.addWidget(interval_note)

        interval_layout.addStretch()
        selector_layout.addWidget(interval_widget)

        # 将元素选择器内容添加到主内容区域
        content_layout.addWidget(self.input_selector_content)

        # 储存的元素对象内容
        self.input_stored_content = QWidget()
        stored_layout = QVBoxLayout(self.input_stored_content)
        stored_layout.setContentsMargins(0, 0, 0, 0)
        stored_layout.setSpacing(15)

        # 元素对象下拉框
        stored_object_widget = QWidget()
        stored_object_layout = QHBoxLayout(stored_object_widget)
        stored_object_layout.setContentsMargins(0, 0, 0, 0)
        stored_object_layout.setSpacing(10)

        # 元素对象标签
        stored_label = QLabel("元素对象")
        stored_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 500; min-width: 80px;")
        stored_object_layout.addWidget(stored_label)

        self.input_stored_object = QComboBox()
        self.input_stored_object.addItem("请选择")
        self.input_stored_object.setFixedHeight(32)
        self.input_stored_object.setStyleSheet("""
            QComboBox {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 14px;
                background-color: white;
                min-width: 400px;
            }
            QComboBox:focus {
                border-color: #1890ff;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666;
                margin-right: 5px;
            }
        """)
        stored_object_layout.addWidget(self.input_stored_object)
        stored_object_layout.addStretch()

        stored_layout.addWidget(stored_object_widget)

        # 储存的元素对象选项卡中的内容类型按钮组（复制）
        stored_content_type_widget = QWidget()
        stored_content_type_layout = QHBoxLayout(stored_content_type_widget)
        stored_content_type_layout.setContentsMargins(0, 0, 0, 0)
        stored_content_type_layout.setSpacing(10)

        # 内容类型按钮组（储存的元素对象）
        self.input_stored_content_type_group = QButtonGroup()

        # 顺序选取按钮（储存的元素对象）
        self.input_stored_sequential_btn = QPushButton("顺序选取")
        self.input_stored_sequential_btn.setCheckable(True)
        self.input_stored_sequential_btn.setChecked(True)
        self.input_stored_sequential_btn.setFixedHeight(32)
        self.input_stored_sequential_btn.setStyleSheet("""
            QPushButton {
                border: 1px solid #1890ff;
                border-radius: 4px;
                padding: 6px 16px;
                font-size: 14px;
                background-color: #1890ff;
                color: white;
                min-width: 80px;
            }
            QPushButton:!checked {
                background-color: white;
                color: #1890ff;
            }
            QPushButton:hover {
                background-color: #40a9ff;
            }
        """)
        self.input_stored_sequential_btn.clicked.connect(self.on_input_stored_sequential_mode)
        self.input_stored_content_type_group.addButton(self.input_stored_sequential_btn)
        stored_content_type_layout.addWidget(self.input_stored_sequential_btn)

        # 随机选取按钮（储存的元素对象）
        self.input_stored_random_btn = QPushButton("随机选取")
        self.input_stored_random_btn.setCheckable(True)
        self.input_stored_random_btn.setFixedHeight(32)
        self.input_stored_random_btn.setStyleSheet("""
            QPushButton {
                border: 1px solid #1890ff;
                border-radius: 4px;
                padding: 6px 16px;
                font-size: 14px;
                background-color: white;
                color: #1890ff;
                min-width: 80px;
            }
            QPushButton:checked {
                background-color: #1890ff;
                color: white;
            }
            QPushButton:hover {
                background-color: #40a9ff;
                color: white;
            }
        """)
        self.input_stored_random_btn.clicked.connect(self.on_input_stored_random_mode)
        self.input_stored_content_type_group.addButton(self.input_stored_random_btn)
        stored_content_type_layout.addWidget(self.input_stored_random_btn)

        # 随机取数按钮（储存的元素对象）
        self.input_stored_random_num_btn = QPushButton("随机取数")
        self.input_stored_random_num_btn.setCheckable(True)
        self.input_stored_random_num_btn.setFixedHeight(32)
        self.input_stored_random_num_btn.setStyleSheet("""
            QPushButton {
                border: 1px solid #1890ff;
                border-radius: 4px;
                padding: 6px 16px;
                font-size: 14px;
                background-color: white;
                color: #1890ff;
                min-width: 80px;
            }
            QPushButton:checked {
                background-color: #1890ff;
                color: white;
            }
            QPushButton:hover {
                background-color: #40a9ff;
                color: white;
            }
        """)
        self.input_stored_random_num_btn.clicked.connect(self.on_input_stored_random_num_mode)
        self.input_stored_content_type_group.addButton(self.input_stored_random_num_btn)
        stored_content_type_layout.addWidget(self.input_stored_random_num_btn)

        # 清除内容后输入复选框（储存的元素对象）
        self.input_stored_clear_first = QCheckBox("清除内容后输入")
        self.input_stored_clear_first.setChecked(True)
        self.input_stored_clear_first.setStyleSheet("""
            QCheckBox {
                font-size: 14px;
                color: #333;
                spacing: 5px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 1px solid #d9d9d9;
                border-radius: 2px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #1890ff;
                border-color: #1890ff;
            }
        """)
        stored_content_type_layout.addWidget(self.input_stored_clear_first)

        stored_content_type_layout.addStretch()
        stored_layout.addWidget(stored_content_type_widget)

        # 储存的元素对象选项卡的内容输入区域
        # 顺序选取/随机选取模式的内容输入框（储存的元素对象）
        self.input_stored_content_text = QTextEdit()
        self.input_stored_content_text.setFixedHeight(100)
        self.input_stored_content_text.setPlaceholderText("单个内容请在一行输入；\n多个内容请换行输入，会依取其中一个内容，示例：\n内容一\n内容二\n内容最多 50 行，每行最多 500 个字符")
        self.input_stored_content_text.setStyleSheet("""
            QTextEdit {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 14px;
                background-color: white;
                font-family: 'Microsoft YaHei', sans-serif;
            }
            QTextEdit:focus {
                border-color: #1890ff;
                outline: none;
            }
        """)
        stored_layout.addWidget(self.input_stored_content_text)

        # 随机取数模式的内容输入框（储存的元素对象，默认隐藏）
        self.input_stored_content_range = QWidget()
        stored_range_layout = QHBoxLayout(self.input_stored_content_range)
        stored_range_layout.setContentsMargins(0, 0, 0, 0)
        stored_range_layout.setSpacing(10)

        self.input_stored_range_min = QLineEdit()
        self.input_stored_range_min.setPlaceholderText("0.1")
        self.input_stored_range_min.setFixedHeight(32)
        self.input_stored_range_min.setFixedWidth(80)
        self.input_stored_range_min.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #1890ff;
                outline: none;
            }
        """)
        stored_range_layout.addWidget(self.input_stored_range_min)

        stored_range_separator = QLabel("-")
        stored_range_separator.setStyleSheet("font-size: 14px; color: #333;")
        stored_range_layout.addWidget(stored_range_separator)

        self.input_stored_range_max = QLineEdit()
        self.input_stored_range_max.setPlaceholderText("10")
        self.input_stored_range_max.setFixedHeight(32)
        self.input_stored_range_max.setFixedWidth(80)
        self.input_stored_range_max.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #1890ff;
                outline: none;
            }
        """)
        stored_range_layout.addWidget(self.input_stored_range_max)

        stored_range_layout.addStretch()
        self.input_stored_content_range.setVisible(False)
        stored_layout.addWidget(self.input_stored_content_range)

        # 使用变量按钮（储存的元素对象内容区域）
        stored_content_var_widget = QWidget()
        stored_content_var_layout = QHBoxLayout(stored_content_var_widget)
        stored_content_var_layout.setContentsMargins(0, 0, 0, 0)
        stored_content_var_layout.setSpacing(10)

        stored_content_var_layout.addStretch()
        input_stored_content_var_btn = QPushButton("使用变量")
        input_stored_content_var_btn.setFlat(True)
        input_stored_content_var_btn.setStyleSheet("""
            QPushButton {
                color: #1890ff;
                background: transparent;
                border: none;
                font-size: 14px;
                padding: 0;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        input_stored_content_var_btn.clicked.connect(self.show_input_stored_content_variables)
        stored_content_var_layout.addWidget(input_stored_content_var_btn)

        stored_layout.addWidget(stored_content_var_widget)

        # 储存的元素对象选项卡的输入间隔时间
        stored_interval_widget = QWidget()
        stored_interval_layout = QHBoxLayout(stored_interval_widget)
        stored_interval_layout.setContentsMargins(0, 0, 0, 0)
        stored_interval_layout.setSpacing(10)

        # 输入间隔时间标签
        stored_interval_label = QLabel("输入间隔时间")
        stored_interval_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 500; min-width: 100px;")
        stored_interval_layout.addWidget(stored_interval_label)

        # 输入间隔时间输入框（储存的元素对象）
        self.input_stored_interval = QSpinBox()
        self.input_stored_interval.setRange(0, 10000)
        self.input_stored_interval.setValue(300)
        self.input_stored_interval.setSuffix(" 毫秒")
        self.input_stored_interval.setFixedHeight(32)
        self.input_stored_interval.setStyleSheet("""
            QSpinBox {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 14px;
                background-color: white;
                min-width: 120px;
            }
            QSpinBox:focus {
                border-color: #1890ff;
            }
        """)
        stored_interval_layout.addWidget(self.input_stored_interval)

        # 毫秒说明
        stored_interval_note = QLabel("1 秒 = 1000 毫秒")
        stored_interval_note.setStyleSheet("font-size: 12px; color: #999;")
        stored_interval_layout.addWidget(stored_interval_note)

        stored_interval_layout.addStretch()
        stored_layout.addWidget(stored_interval_widget)

        # 默认隐藏储存的元素对象内容
        self.input_stored_content.setVisible(False)
        content_layout.addWidget(self.input_stored_content)

        # 说明字段行
        desc_widget = QWidget()
        desc_layout = QHBoxLayout(desc_widget)
        desc_layout.setContentsMargins(0, 0, 0, 0)
        desc_layout.setSpacing(12)

        desc_label = QLabel("说明")
        desc_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 500; min-width: 80px;")
        desc_layout.addWidget(desc_label)

        self.input_description = QLineEdit()
        self.input_description.setPlaceholderText("选填")
        self.input_description.setFixedHeight(36)
        self.input_description.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #1890ff;
                outline: none;
            }
        """)
        desc_layout.addWidget(self.input_description)

        content_layout.addWidget(desc_widget)

        parent_layout.addWidget(self.input_content_widget)

    def on_input_selector_tab(self):
        """切换到元素选择器选项卡"""
        self.input_selector_tab.setChecked(True)
        self.input_stored_tab.setChecked(False)
        self.input_selector_content.setVisible(True)
        self.input_stored_content.setVisible(False)

    def on_input_stored_tab(self):
        """切换到储存的元素对象选项卡"""
        self.input_selector_tab.setChecked(False)
        self.input_stored_tab.setChecked(True)
        self.input_selector_content.setVisible(False)
        self.input_stored_content.setVisible(True)

    def on_input_sequential_mode(self):
        """切换到顺序选取模式（元素选择器）"""
        self.input_sequential_btn.setChecked(True)
        self.input_random_btn.setChecked(False)
        self.input_random_num_btn.setChecked(False)
        self.input_content_text.setVisible(True)
        self.input_content_range.setVisible(False)

    def on_input_random_mode(self):
        """切换到随机选取模式（元素选择器）"""
        self.input_sequential_btn.setChecked(False)
        self.input_random_btn.setChecked(True)
        self.input_random_num_btn.setChecked(False)
        self.input_content_text.setVisible(True)
        self.input_content_range.setVisible(False)

    def on_input_random_num_mode(self):
        """切换到随机取数模式（元素选择器）"""
        self.input_sequential_btn.setChecked(False)
        self.input_random_btn.setChecked(False)
        self.input_random_num_btn.setChecked(True)
        self.input_content_text.setVisible(False)
        self.input_content_range.setVisible(True)

    def on_input_stored_sequential_mode(self):
        """切换到顺序选取模式（储存的元素对象）"""
        self.input_stored_sequential_btn.setChecked(True)
        self.input_stored_random_btn.setChecked(False)
        self.input_stored_random_num_btn.setChecked(False)
        self.input_stored_content_text.setVisible(True)
        self.input_stored_content_range.setVisible(False)

    def on_input_stored_random_mode(self):
        """切换到随机选取模式（储存的元素对象）"""
        self.input_stored_sequential_btn.setChecked(False)
        self.input_stored_random_btn.setChecked(True)
        self.input_stored_random_num_btn.setChecked(False)
        self.input_stored_content_text.setVisible(True)
        self.input_stored_content_range.setVisible(False)

    def on_input_stored_random_num_mode(self):
        """切换到随机取数模式（储存的元素对象）"""
        self.input_stored_sequential_btn.setChecked(False)
        self.input_stored_random_btn.setChecked(False)
        self.input_stored_random_num_btn.setChecked(True)
        self.input_stored_content_text.setVisible(False)
        self.input_stored_content_range.setVisible(True)

    def show_input_selector_variables(self):
        """显示选择器变量下拉框"""
        self.show_simple_variable_menu(self.input_selector_input)

    def show_input_order_variables(self):
        """显示元素顺序变量下拉框"""
        self.show_simple_variable_menu(self.input_order_value)

    def show_input_content_variables(self):
        """显示内容变量下拉框"""
        self.show_simple_variable_menu(self.input_content_text)

    def show_input_stored_content_variables(self):
        """显示储存的元素对象内容变量下拉框"""
        self.show_simple_variable_menu(self.input_stored_content_text)

    def create_focus_element_exact_config(self, parent_layout):
        """元素聚焦 - 完全按照您的截图实现"""

        # 主容器
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(15)

        # 选项卡区域
        tab_widget = QWidget()
        tab_layout = QHBoxLayout(tab_widget)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.setSpacing(0)

        # 元素选择器选项卡
        self.focus_selector_tab = QPushButton("元素选择器")
        self.focus_selector_tab.setCheckable(True)
        self.focus_selector_tab.setChecked(True)
        self.focus_selector_tab.setFixedHeight(32)
        self.focus_selector_tab.setStyleSheet("""
            QPushButton {
                border: 1px solid #d9d9d9;
                border-bottom: none;
                border-radius: 4px 4px 0 0;
                padding: 6px 16px;
                font-size: 14px;
                background-color: #1890ff;
                color: white;
            }
            QPushButton:!checked {
                background-color: #f5f5f5;
                color: #666;
            }
        """)
        self.focus_selector_tab.clicked.connect(self.on_focus_selector_tab)
        tab_layout.addWidget(self.focus_selector_tab)

        # 储存的元素对象选项卡
        self.focus_stored_tab = QPushButton("储存的元素对象")
        self.focus_stored_tab.setCheckable(True)
        self.focus_stored_tab.setFixedHeight(32)
        self.focus_stored_tab.setStyleSheet("""
            QPushButton {
                border: 1px solid #d9d9d9;
                border-bottom: none;
                border-left: none;
                border-radius: 4px 4px 0 0;
                padding: 6px 16px;
                font-size: 14px;
                background-color: #f5f5f5;
                color: #666;
            }
            QPushButton:checked {
                background-color: #1890ff;
                color: white;
            }
        """)
        self.focus_stored_tab.clicked.connect(self.on_focus_stored_tab)
        tab_layout.addWidget(self.focus_stored_tab)

        tab_layout.addStretch()
        main_layout.addWidget(tab_widget)

        # 内容区域
        self.focus_content_widget = QWidget()
        self.focus_content_widget.setStyleSheet("""
            QWidget {
                border: 1px solid #d9d9d9;
                border-radius: 0 4px 4px 4px;
                background-color: white;
                padding: 15px;
            }
        """)
        content_layout = QVBoxLayout(self.focus_content_widget)
        content_layout.setContentsMargins(15, 15, 15, 15)
        content_layout.setSpacing(15)

        # 元素选择器内容
        self.focus_selector_content = QWidget()
        selector_layout = QVBoxLayout(self.focus_selector_content)
        selector_layout.setContentsMargins(0, 0, 0, 0)
        selector_layout.setSpacing(15)

        # 选择器类型
        selector_type_widget = QWidget()
        selector_type_layout = QHBoxLayout(selector_type_widget)
        selector_type_layout.setContentsMargins(0, 0, 0, 0)
        selector_type_layout.setSpacing(15)

        # 选择器标签
        selector_label = QLabel("选择器")
        selector_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 500;")
        selector_type_layout.addWidget(selector_label)

        # 单选按钮组
        from PyQt5.QtWidgets import QRadioButton, QButtonGroup
        self.focus_selector_group = QButtonGroup()

        self.focus_selector_radio = QRadioButton("Selector")
        self.focus_selector_radio.setChecked(True)
        self.focus_selector_radio.setStyleSheet("font-size: 14px; color: #333;")
        self.focus_selector_group.addButton(self.focus_selector_radio)
        selector_type_layout.addWidget(self.focus_selector_radio)

        self.focus_xpath_radio = QRadioButton("XPath")
        self.focus_xpath_radio.setStyleSheet("font-size: 14px; color: #333;")
        self.focus_selector_group.addButton(self.focus_xpath_radio)
        selector_type_layout.addWidget(self.focus_xpath_radio)

        self.focus_text_radio = QRadioButton("文本")
        self.focus_text_radio.setStyleSheet("font-size: 14px; color: #333;")
        self.focus_selector_group.addButton(self.focus_text_radio)
        selector_type_layout.addWidget(self.focus_text_radio)

        selector_type_layout.addStretch()
        selector_layout.addWidget(selector_type_widget)

        # 选择器输入框
        selector_input_widget = QWidget()
        selector_input_layout = QHBoxLayout(selector_input_widget)
        selector_input_layout.setContentsMargins(0, 0, 0, 0)
        selector_input_layout.setSpacing(10)

        self.focus_selector_input = QLineEdit()
        self.focus_selector_input.setPlaceholderText("请输入元素选择器，比如 #email input")
        self.focus_selector_input.setFixedHeight(32)
        self.focus_selector_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #1890ff;
                outline: none;
            }
        """)
        selector_input_layout.addWidget(self.focus_selector_input)

        # 使用变量链接
        focus_use_var_btn = QPushButton("使用变量")
        focus_use_var_btn.setFlat(True)
        focus_use_var_btn.setStyleSheet("""
            QPushButton {
                color: #1890ff;
                background: transparent;
                border: none;
                font-size: 14px;
                padding: 0;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        focus_use_var_btn.clicked.connect(self.show_focus_selector_variables)
        selector_input_layout.addWidget(focus_use_var_btn)

        selector_layout.addWidget(selector_input_widget)

        # 元素顺序（添加到元素选择器内容中）
        order_widget = QWidget()
        order_layout = QHBoxLayout(order_widget)
        order_layout.setContentsMargins(0, 0, 0, 0)
        order_layout.setSpacing(10)

        # 元素顺序标签
        order_label = QLabel("元素顺序")
        order_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 500; min-width: 80px;")
        order_layout.addWidget(order_label)

        # 顺序类型下拉框
        self.focus_order_type = QComboBox()
        self.focus_order_type.addItems(["固定值", "区间随机"])
        self.focus_order_type.setFixedHeight(32)
        self.focus_order_type.setStyleSheet("""
            QComboBox {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 14px;
                background-color: white;
                min-width: 100px;
            }
            QComboBox:focus {
                border-color: #1890ff;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666;
                margin-right: 5px;
            }
        """)
        order_layout.addWidget(self.focus_order_type)

        # 顺序值输入框
        self.focus_order_value = QSpinBox()
        self.focus_order_value.setMinimum(1)
        self.focus_order_value.setValue(1)
        self.focus_order_value.setFixedHeight(32)
        self.focus_order_value.setStyleSheet("""
            QSpinBox {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 14px;
                background-color: white;
                min-width: 80px;
            }
            QSpinBox:focus {
                border-color: #1890ff;
            }
        """)
        order_layout.addWidget(self.focus_order_value)

        # 使用变量链接
        focus_order_var_btn = QPushButton("使用变量")
        focus_order_var_btn.setFlat(True)
        focus_order_var_btn.setStyleSheet("""
            QPushButton {
                color: #1890ff;
                background: transparent;
                border: none;
                font-size: 14px;
                padding: 0;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        focus_order_var_btn.clicked.connect(self.show_focus_order_variables)
        order_layout.addWidget(focus_order_var_btn)

        order_layout.addStretch()
        selector_layout.addWidget(order_widget)

        # 将元素选择器内容添加到主内容区域
        content_layout.addWidget(self.focus_selector_content)

        # 储存的元素对象内容
        self.focus_stored_content = QWidget()
        stored_layout = QVBoxLayout(self.focus_stored_content)
        stored_layout.setContentsMargins(0, 0, 0, 0)
        stored_layout.setSpacing(15)

        # 元素对象下拉框
        stored_object_widget = QWidget()
        stored_object_layout = QHBoxLayout(stored_object_widget)
        stored_object_layout.setContentsMargins(0, 0, 0, 0)
        stored_object_layout.setSpacing(10)

        # 元素对象标签
        stored_label = QLabel("元素对象")
        stored_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 500; min-width: 80px;")
        stored_object_layout.addWidget(stored_label)

        self.focus_stored_object = QComboBox()
        self.focus_stored_object.addItem("请选择")
        self.focus_stored_object.setFixedHeight(32)
        self.focus_stored_object.setStyleSheet("""
            QComboBox {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 14px;
                background-color: white;
                min-width: 400px;
            }
            QComboBox:focus {
                border-color: #1890ff;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666;
                margin-right: 5px;
            }
        """)
        stored_object_layout.addWidget(self.focus_stored_object)
        stored_object_layout.addStretch()

        stored_layout.addWidget(stored_object_widget)

        # 默认隐藏储存的元素对象内容
        self.focus_stored_content.setVisible(False)
        content_layout.addWidget(self.focus_stored_content)

        # 说明字段（共享）
        desc_widget = QWidget()
        desc_layout = QHBoxLayout(desc_widget)
        desc_layout.setContentsMargins(0, 0, 0, 0)
        desc_layout.setSpacing(10)

        desc_label = QLabel("说明")
        desc_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 500; min-width: 80px;")
        desc_layout.addWidget(desc_label)

        self.focus_description = QLineEdit()
        self.focus_description.setPlaceholderText("选填")
        self.focus_description.setFixedHeight(32)
        self.focus_description.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #1890ff;
                outline: none;
            }
        """)
        desc_layout.addWidget(self.focus_description)

        content_layout.addWidget(desc_widget)

        main_layout.addWidget(self.focus_content_widget)
        parent_layout.addWidget(main_widget)

    def on_focus_selector_tab(self):
        """切换到元素选择器选项卡"""
        self.focus_selector_tab.setChecked(True)
        self.focus_stored_tab.setChecked(False)
        self.focus_selector_content.setVisible(True)
        self.focus_stored_content.setVisible(False)

    def on_focus_stored_tab(self):
        """切换到储存的元素对象选项卡"""
        self.focus_selector_tab.setChecked(False)
        self.focus_stored_tab.setChecked(True)
        self.focus_selector_content.setVisible(False)
        self.focus_stored_content.setVisible(True)

    def show_focus_selector_variables(self):
        """显示选择器变量下拉框"""
        self.show_simple_variable_menu(self.focus_selector_input)

    def show_focus_order_variables(self):
        """显示元素顺序变量下拉框"""
        self.show_simple_variable_menu(self.focus_order_value)

    def create_dropdown_exact_config(self, parent_layout):
        """下拉选择器 - 完全按照您的截图实现"""

        # 主容器
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(15)

        # 选项卡区域
        tab_widget = QWidget()
        tab_layout = QHBoxLayout(tab_widget)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.setSpacing(0)

        # 元素选择器选项卡
        self.dropdown_selector_tab = QPushButton("元素选择器")
        self.dropdown_selector_tab.setCheckable(True)
        self.dropdown_selector_tab.setChecked(True)
        self.dropdown_selector_tab.setFixedHeight(32)
        self.dropdown_selector_tab.setStyleSheet("""
            QPushButton {
                border: 1px solid #d9d9d9;
                border-bottom: none;
                border-radius: 4px 4px 0 0;
                padding: 6px 16px;
                font-size: 14px;
                background-color: #1890ff;
                color: white;
            }
            QPushButton:!checked {
                background-color: #f5f5f5;
                color: #666;
            }
        """)
        self.dropdown_selector_tab.clicked.connect(self.on_dropdown_selector_tab)
        tab_layout.addWidget(self.dropdown_selector_tab)

        # 储存的元素对象选项卡
        self.dropdown_stored_tab = QPushButton("储存的元素对象")
        self.dropdown_stored_tab.setCheckable(True)
        self.dropdown_stored_tab.setFixedHeight(32)
        self.dropdown_stored_tab.setStyleSheet("""
            QPushButton {
                border: 1px solid #d9d9d9;
                border-bottom: none;
                border-left: none;
                border-radius: 4px 4px 0 0;
                padding: 6px 16px;
                font-size: 14px;
                background-color: #f5f5f5;
                color: #666;
            }
            QPushButton:checked {
                background-color: #1890ff;
                color: white;
            }
        """)
        self.dropdown_stored_tab.clicked.connect(self.on_dropdown_stored_tab)
        tab_layout.addWidget(self.dropdown_stored_tab)

        tab_layout.addStretch()
        main_layout.addWidget(tab_widget)

        # 内容区域
        self.dropdown_content_widget = QWidget()
        self.dropdown_content_widget.setStyleSheet("""
            QWidget {
                border: 1px solid #d9d9d9;
                border-radius: 0 4px 4px 4px;
                background-color: white;
                padding: 15px;
            }
        """)
        content_layout = QVBoxLayout(self.dropdown_content_widget)
        content_layout.setContentsMargins(15, 15, 15, 15)
        content_layout.setSpacing(15)

        # 元素选择器内容
        self.dropdown_selector_content = QWidget()
        selector_layout = QVBoxLayout(self.dropdown_selector_content)
        selector_layout.setContentsMargins(0, 0, 0, 0)
        selector_layout.setSpacing(15)

        # 选择器类型
        selector_type_widget = QWidget()
        selector_type_layout = QHBoxLayout(selector_type_widget)
        selector_type_layout.setContentsMargins(0, 0, 0, 0)
        selector_type_layout.setSpacing(15)

        # 选择器标签
        selector_label = QLabel("选择器")
        selector_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 500;")
        selector_type_layout.addWidget(selector_label)

        # 单选按钮组
        from PyQt5.QtWidgets import QRadioButton, QButtonGroup
        self.dropdown_selector_group = QButtonGroup()

        self.dropdown_selector_radio = QRadioButton("Selector")
        self.dropdown_selector_radio.setChecked(True)
        self.dropdown_selector_radio.setStyleSheet("font-size: 14px; color: #333;")
        self.dropdown_selector_group.addButton(self.dropdown_selector_radio)
        selector_type_layout.addWidget(self.dropdown_selector_radio)

        self.dropdown_xpath_radio = QRadioButton("XPath")
        self.dropdown_xpath_radio.setStyleSheet("font-size: 14px; color: #333;")
        self.dropdown_selector_group.addButton(self.dropdown_xpath_radio)
        selector_type_layout.addWidget(self.dropdown_xpath_radio)

        self.dropdown_text_radio = QRadioButton("文本")
        self.dropdown_text_radio.setStyleSheet("font-size: 14px; color: #333;")
        self.dropdown_selector_group.addButton(self.dropdown_text_radio)
        selector_type_layout.addWidget(self.dropdown_text_radio)

        selector_type_layout.addStretch()
        selector_layout.addWidget(selector_type_widget)

        # 选择器输入框
        selector_input_widget = QWidget()
        selector_input_layout = QHBoxLayout(selector_input_widget)
        selector_input_layout.setContentsMargins(0, 0, 0, 0)
        selector_input_layout.setSpacing(10)

        self.dropdown_selector_input = QLineEdit()
        self.dropdown_selector_input.setPlaceholderText("请输入元素选择器，比如 #email input")
        self.dropdown_selector_input.setFixedHeight(32)
        self.dropdown_selector_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #1890ff;
                outline: none;
            }
        """)
        selector_input_layout.addWidget(self.dropdown_selector_input)

        # 使用变量链接
        dropdown_use_var_btn = QPushButton("使用变量")
        dropdown_use_var_btn.setFlat(True)
        dropdown_use_var_btn.setStyleSheet("""
            QPushButton {
                color: #1890ff;
                background: transparent;
                border: none;
                font-size: 14px;
                padding: 0;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        dropdown_use_var_btn.clicked.connect(self.show_dropdown_selector_variables)
        selector_input_layout.addWidget(dropdown_use_var_btn)

        selector_layout.addWidget(selector_input_widget)

        # 储存的元素对象内容
        self.dropdown_stored_content = QWidget()
        stored_layout = QVBoxLayout(self.dropdown_stored_content)
        stored_layout.setContentsMargins(0, 0, 0, 0)
        stored_layout.setSpacing(15)

        # 元素对象下拉框
        stored_object_widget = QWidget()
        stored_object_layout = QHBoxLayout(stored_object_widget)
        stored_object_layout.setContentsMargins(0, 0, 0, 0)
        stored_object_layout.setSpacing(10)

        # 元素对象标签
        stored_label = QLabel("元素对象")
        stored_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 500; min-width: 80px;")
        stored_object_layout.addWidget(stored_label)

        self.dropdown_stored_object = QComboBox()
        self.dropdown_stored_object.addItem("请选择")
        self.dropdown_stored_object.setFixedHeight(32)
        self.dropdown_stored_object.setStyleSheet("""
            QComboBox {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 14px;
                background-color: white;
                min-width: 400px;
            }
            QComboBox:focus {
                border-color: #1890ff;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666;
                margin-right: 5px;
            }
        """)
        stored_object_layout.addWidget(self.dropdown_stored_object)
        stored_object_layout.addStretch()

        stored_layout.addWidget(stored_object_widget)

        # 元素顺序（添加到元素选择器内容中）
        order_widget = QWidget()
        order_layout = QHBoxLayout(order_widget)
        order_layout.setContentsMargins(0, 0, 0, 0)
        order_layout.setSpacing(10)

        # 元素顺序标签
        order_label = QLabel("元素顺序")
        order_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 500; min-width: 80px;")
        order_layout.addWidget(order_label)

        # 顺序类型下拉框
        self.dropdown_order_type = QComboBox()
        self.dropdown_order_type.addItems(["固定值", "区间随机"])
        self.dropdown_order_type.setFixedHeight(32)
        self.dropdown_order_type.setStyleSheet("""
            QComboBox {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 14px;
                background-color: white;
                min-width: 100px;
            }
            QComboBox:focus {
                border-color: #1890ff;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666;
                margin-right: 5px;
            }
        """)
        order_layout.addWidget(self.dropdown_order_type)

        # 顺序值输入框
        self.dropdown_order_value = QSpinBox()
        self.dropdown_order_value.setMinimum(1)
        self.dropdown_order_value.setValue(1)
        self.dropdown_order_value.setFixedHeight(32)
        self.dropdown_order_value.setStyleSheet("""
            QSpinBox {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 14px;
                background-color: white;
                min-width: 80px;
            }
            QSpinBox:focus {
                border-color: #1890ff;
            }
        """)
        order_layout.addWidget(self.dropdown_order_value)

        # 使用变量链接
        dropdown_order_var_btn = QPushButton("使用变量")
        dropdown_order_var_btn.setFlat(True)
        dropdown_order_var_btn.setStyleSheet("""
            QPushButton {
                color: #1890ff;
                background: transparent;
                border: none;
                font-size: 14px;
                padding: 0;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        dropdown_order_var_btn.clicked.connect(self.show_dropdown_order_variables)
        order_layout.addWidget(dropdown_order_var_btn)

        order_layout.addStretch()
        selector_layout.addWidget(order_widget)

        # 将元素选择器内容添加到主内容区域
        content_layout.addWidget(self.dropdown_selector_content)

        # 默认隐藏储存的元素对象内容
        self.dropdown_stored_content.setVisible(False)
        content_layout.addWidget(self.dropdown_stored_content)

        # 选择的值字段（共享，两个选项卡都显示）
        selected_value_widget = QWidget()
        selected_value_layout = QHBoxLayout(selected_value_widget)
        selected_value_layout.setContentsMargins(0, 0, 0, 0)
        selected_value_layout.setSpacing(10)

        # 选择的值标签（带红色星号）
        selected_value_label = QLabel("* 选择的值")
        selected_value_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 500; min-width: 80px;")
        selected_value_layout.addWidget(selected_value_label)

        self.dropdown_selected_value = QLineEdit()
        self.dropdown_selected_value.setPlaceholderText("请输入选择的值")
        self.dropdown_selected_value.setFixedHeight(32)
        self.dropdown_selected_value.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #1890ff;
                outline: none;
            }
        """)
        selected_value_layout.addWidget(self.dropdown_selected_value)

        # 使用变量链接
        dropdown_value_var_btn = QPushButton("使用变量")
        dropdown_value_var_btn.setFlat(True)
        dropdown_value_var_btn.setStyleSheet("""
            QPushButton {
                color: #1890ff;
                background: transparent;
                border: none;
                font-size: 14px;
                padding: 0;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        dropdown_value_var_btn.clicked.connect(self.show_dropdown_value_variables)
        selected_value_layout.addWidget(dropdown_value_var_btn)

        content_layout.addWidget(selected_value_widget)

        # 说明字段（共享）
        desc_widget = QWidget()
        desc_layout = QHBoxLayout(desc_widget)
        desc_layout.setContentsMargins(0, 0, 0, 0)
        desc_layout.setSpacing(10)

        desc_label = QLabel("说明")
        desc_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 500; min-width: 80px;")
        desc_layout.addWidget(desc_label)

        self.dropdown_description = QLineEdit()
        self.dropdown_description.setPlaceholderText("选填")
        self.dropdown_description.setFixedHeight(32)
        self.dropdown_description.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #1890ff;
                outline: none;
            }
        """)
        desc_layout.addWidget(self.dropdown_description)

        content_layout.addWidget(desc_widget)

        main_layout.addWidget(self.dropdown_content_widget)
        parent_layout.addWidget(main_widget)

    def on_dropdown_selector_tab(self):
        """切换到元素选择器选项卡"""
        self.dropdown_selector_tab.setChecked(True)
        self.dropdown_stored_tab.setChecked(False)
        self.dropdown_selector_content.setVisible(True)
        self.dropdown_stored_content.setVisible(False)

    def on_dropdown_stored_tab(self):
        """切换到储存的元素对象选项卡"""
        self.dropdown_selector_tab.setChecked(False)
        self.dropdown_stored_tab.setChecked(True)
        self.dropdown_selector_content.setVisible(False)
        self.dropdown_stored_content.setVisible(True)

    def show_dropdown_selector_variables(self):
        """显示选择器变量下拉框"""
        self.show_simple_variable_menu(self.dropdown_selector_input)

    def show_dropdown_order_variables(self):
        """显示元素顺序变量下拉框"""
        self.show_simple_variable_menu(self.dropdown_order_value)

    def show_dropdown_value_variables(self):
        """显示选择的值变量下拉框"""
        self.show_simple_variable_menu(self.dropdown_selected_value)

    def create_wait_element_exact_config(self, parent_layout):
        """等待元素出现 - 完全按照AdsPower原版界面"""
        config_group = QGroupBox("等待元素出现设置")
        config_layout = QFormLayout(config_group)

        # 选择器类型
        self.wait_element_selector_type = QComboBox()
        self.wait_element_selector_type.addItems(["Selector", "XPath", "文本"])
        self.wait_element_selector_type.setStyleSheet(self.get_input_style())
        config_layout.addRow("选择器类型:", self.wait_element_selector_type)

        # 元素选择器
        self.wait_element_selector = QLineEdit()
        self.wait_element_selector.setPlaceholderText("请输入元素选择器")
        self.wait_element_selector.setStyleSheet(self.get_input_style())
        config_layout.addRow("元素选择器:", self.wait_element_selector)

        # 储存的元素对象
        self.wait_element_stored = QComboBox()
        self.wait_element_stored.addItem("选择一个保存为对象的变量")
        self.wait_element_stored.setStyleSheet(self.get_input_style())
        config_layout.addRow("储存的元素对象:", self.wait_element_stored)

        # 元素顺序
        order_widget = QWidget()
        order_layout = QHBoxLayout(order_widget)
        order_layout.setContentsMargins(0, 0, 0, 0)

        self.wait_element_order_type = QComboBox()
        self.wait_element_order_type.addItems(["固定值", "区间随机"])
        self.wait_element_order_type.setStyleSheet(self.get_input_style())
        order_layout.addWidget(self.wait_element_order_type)

        self.wait_element_order_value = QSpinBox()
        self.wait_element_order_value.setMinimum(1)
        self.wait_element_order_value.setValue(1)
        self.wait_element_order_value.setStyleSheet(self.get_input_style())
        order_layout.addWidget(self.wait_element_order_value)

        config_layout.addRow("元素顺序:", order_widget)

        # 超时等待
        self.wait_element_timeout = QSpinBox()
        self.wait_element_timeout.setRange(1000, 300000)
        self.wait_element_timeout.setValue(30000)
        self.wait_element_timeout.setSuffix(" 毫秒")
        self.wait_element_timeout.setStyleSheet(self.get_input_style())
        config_layout.addRow("超时等待:", self.wait_element_timeout)

        parent_layout.addWidget(config_group)

    def create_wait_request_exact_config(self, parent_layout):
        """等待请求完成 - 完全按照AdsPower原版界面"""
        config_group = QGroupBox("等待请求完成设置")
        config_layout = QFormLayout(config_group)

        # 请求URL
        self.wait_request_url = QLineEdit()
        self.wait_request_url.setPlaceholderText("请输入要等待的请求URL")
        self.wait_request_url.setStyleSheet(self.get_input_style())
        config_layout.addRow("请求URL:", self.wait_request_url)

        # 超时等待
        self.wait_request_timeout = QSpinBox()
        self.wait_request_timeout.setRange(1000, 300000)
        self.wait_request_timeout.setValue(30000)
        self.wait_request_timeout.setSuffix(" 毫秒")
        self.wait_request_timeout.setStyleSheet(self.get_input_style())
        config_layout.addRow("超时等待:", self.wait_request_timeout)

        parent_layout.addWidget(config_group)

    def create_keyboard_key_exact_config(self, parent_layout):
        """键盘按键 - 完全按照AdsPower原版界面"""
        config_group = QGroupBox("键盘按键设置")
        config_layout = QFormLayout(config_group)

        # 按键类型
        self.keyboard_key_type = QComboBox()
        self.keyboard_key_type.addItems([
            "退格键", "Tab键", "回车键", "空格键", "Esc键", "删除键",
            "方向上键", "方向下键", "方向左键", "方向右键"
        ])
        self.keyboard_key_type.setStyleSheet(self.get_input_style())
        config_layout.addRow("按键类型:", self.keyboard_key_type)

        parent_layout.addWidget(config_group)

    def create_keyboard_combo_exact_config(self, parent_layout):
        """组合键 - 完全按照AdsPower原版界面"""
        config_group = QGroupBox("组合键设置")
        config_layout = QFormLayout(config_group)

        # 组合键类型（根据AdsPower文档，Windows仅支持特定组合键）
        self.keyboard_combo_type = QComboBox()
        self.keyboard_combo_type.addItems(["Ctrl+A", "Ctrl+C", "Ctrl+V", "Ctrl+R"])
        self.keyboard_combo_type.setStyleSheet(self.get_input_style())
        config_layout.addRow("组合键:", self.keyboard_combo_type)

        # 说明文本
        info_label = QLabel("注意：在Windows系统中，仅支持Ctrl+A、Ctrl+C、Ctrl+V、Ctrl+R")
        info_label.setStyleSheet("color: #666666; font-size: 12px; margin-top: 10px;")
        config_layout.addRow("", info_label)

        parent_layout.addWidget(config_group)

    def create_get_url_exact_config(self, parent_layout):
        """获取URL - 完全按照AdsPower原版界面"""
        config_group = QGroupBox("获取URL设置")
        config_layout = QFormLayout(config_group)

        # 提取类型
        self.get_url_extract_type = QComboBox()
        self.get_url_extract_type.addItems(["完整地址", "根地址", "参数值"])
        self.get_url_extract_type.setStyleSheet(self.get_input_style())
        config_layout.addRow("提取类型:", self.get_url_extract_type)

        # 参数名（当选择参数值时显示）
        self.get_url_param_name = QLineEdit()
        self.get_url_param_name.setPlaceholderText("请输入参数名，如：k")
        self.get_url_param_name.setStyleSheet(self.get_input_style())
        self.get_url_param_name.setEnabled(False)
        config_layout.addRow("参数名:", self.get_url_param_name)

        # 保存至
        self.get_url_save_var = QLineEdit()
        self.get_url_save_var.setPlaceholderText("请输入保存URL的变量名")
        self.get_url_save_var.setStyleSheet(self.get_input_style())
        config_layout.addRow("保存至:", self.get_url_save_var)

        # 连接信号
        self.get_url_extract_type.currentTextChanged.connect(
            lambda text: self.get_url_param_name.setEnabled(text == "参数值")
        )

        parent_layout.addWidget(config_group)

    def create_get_clipboard_exact_config(self, parent_layout):
        """获取粘贴板内容 - 完全按照AdsPower原版界面"""
        config_group = QGroupBox("获取粘贴板内容设置")
        config_layout = QFormLayout(config_group)

        # 保存至
        self.get_clipboard_save_var = QLineEdit()
        self.get_clipboard_save_var.setPlaceholderText("请输入保存内容的变量名")
        self.get_clipboard_save_var.setStyleSheet(self.get_input_style())
        config_layout.addRow("保存至:", self.get_clipboard_save_var)

        # 说明文本
        info_label = QLabel("获取粘贴板中的文本内容，保存到变量中以便后续使用")
        info_label.setStyleSheet("color: #666666; font-size: 12px; margin-top: 10px;")
        config_layout.addRow("", info_label)

        parent_layout.addWidget(config_group)

    def create_element_data_exact_config(self, parent_layout):
        """元素数据 - 完全按照AdsPower原版界面"""
        config_group = QGroupBox("元素数据设置")
        config_layout = QFormLayout(config_group)

        # 选择器
        self.element_data_selector = QLineEdit()
        self.element_data_selector.setPlaceholderText("输入元素选择器，如#email_input、input[type=\"password\"]、.button_search等")
        self.element_data_selector.setStyleSheet(self.get_input_style())
        config_layout.addRow("选择器:", self.element_data_selector)

        # 储存的元素对象
        self.element_data_stored = QComboBox()
        self.element_data_stored.addItem("选择一个已保存为对象的变量")
        self.element_data_stored.setStyleSheet(self.get_input_style())
        config_layout.addRow("储存的元素对象:", self.element_data_stored)

        # 元素顺序
        order_widget = QWidget()
        order_layout = QHBoxLayout(order_widget)
        order_layout.setContentsMargins(0, 0, 0, 0)

        self.element_data_order_type = QComboBox()
        self.element_data_order_type.addItems(["固定值", "区间随机"])
        self.element_data_order_type.setStyleSheet(self.get_input_style())
        order_layout.addWidget(self.element_data_order_type)

        self.element_data_order_value = QSpinBox()
        self.element_data_order_value.setMinimum(1)
        self.element_data_order_value.setValue(1)
        self.element_data_order_value.setStyleSheet(self.get_input_style())
        order_layout.addWidget(self.element_data_order_value)

        config_layout.addRow("元素顺序:", order_widget)

        # 提取类型
        self.element_data_extract_type = QComboBox()
        self.element_data_extract_type.addItems(["文本", "对象", "iFrame框架", "源码", "属性", "子元素"])
        self.element_data_extract_type.setStyleSheet(self.get_input_style())
        config_layout.addRow("提取类型:", self.element_data_extract_type)

        # 属性名（当选择属性时显示）
        self.element_data_attr_name = QLineEdit()
        self.element_data_attr_name.setPlaceholderText("请输入属性名，如：data-src")
        self.element_data_attr_name.setStyleSheet(self.get_input_style())
        self.element_data_attr_name.setEnabled(False)
        config_layout.addRow("属性名:", self.element_data_attr_name)

        # 子元素名（当选择子元素时显示）
        self.element_data_child_name = QLineEdit()
        self.element_data_child_name.setPlaceholderText("请输入子元素名")
        self.element_data_child_name.setStyleSheet(self.get_input_style())
        self.element_data_child_name.setEnabled(False)
        config_layout.addRow("子元素名:", self.element_data_child_name)

        # 保存至
        self.element_data_save_var = QLineEdit()
        self.element_data_save_var.setPlaceholderText("请输入保存数据的变量名")
        self.element_data_save_var.setStyleSheet(self.get_input_style())
        config_layout.addRow("保存至:", self.element_data_save_var)

        # 连接信号
        def on_extract_type_changed(text):
            self.element_data_attr_name.setEnabled(text == "属性")
            self.element_data_child_name.setEnabled(text == "子元素")

        self.element_data_extract_type.currentTextChanged.connect(on_extract_type_changed)

        parent_layout.addWidget(config_group)

    def create_current_focus_element_exact_config(self, parent_layout):
        """当前焦点元素 - 完全按照AdsPower原版界面"""
        config_group = QGroupBox("当前焦点元素设置")
        config_layout = QFormLayout(config_group)

        # 保存至
        self.focus_element_save_var = QLineEdit()
        self.focus_element_save_var.setPlaceholderText("请输入保存焦点元素的变量名")
        self.focus_element_save_var.setStyleSheet(self.get_input_style())
        config_layout.addRow("保存至:", self.focus_element_save_var)

        # 说明文本
        info_label = QLabel("将当前聚焦状态下的元素保存为变量")
        info_label.setStyleSheet("color: #666666; font-size: 12px; margin-top: 10px;")
        config_layout.addRow("", info_label)

        parent_layout.addWidget(config_group)

    def create_save_to_file_exact_config(self, parent_layout):
        """存到文件 - 完全按照AdsPower原版界面"""
        config_group = QGroupBox("存到文件设置")
        config_layout = QFormLayout(config_group)

        # 文件名
        self.save_file_name = QLineEdit()
        self.save_file_name.setPlaceholderText("填写要输出的txt文件名，文件名可以使用已保存的变量")
        self.save_file_name.setStyleSheet(self.get_input_style())
        config_layout.addRow("文件名:", self.save_file_name)

        # 保存模板
        self.save_file_template = QTextEdit()
        self.save_file_template.setFixedHeight(100)
        self.save_file_template.setPlaceholderText("可输入文字，以及使用已保存的变量")
        self.save_file_template.setStyleSheet(self.get_input_style())
        config_layout.addRow("保存模板:", self.save_file_template)

        # 说明文本
        info_label = QLabel("txt文件保存位置在：【RPA】——【任务详情】——【日志详情】——【目录查看】")
        info_label.setStyleSheet("color: #666666; font-size: 12px; margin-top: 10px;")
        config_layout.addRow("", info_label)

        parent_layout.addWidget(config_group)

    def create_save_to_excel_exact_config(self, parent_layout):
        """存到Excel - 完全按照AdsPower原版界面"""
        config_group = QGroupBox("存到Excel设置")
        config_layout = QFormLayout(config_group)

        # 文件名
        self.save_excel_name = QLineEdit()
        self.save_excel_name.setPlaceholderText("填写要输出的Excel文件名，文件名可以使用已保存的变量")
        self.save_excel_name.setStyleSheet(self.get_input_style())
        config_layout.addRow("文件名:", self.save_excel_name)

        # 选择保存列
        self.save_excel_columns = QTextEdit()
        self.save_excel_columns.setFixedHeight(80)
        self.save_excel_columns.setPlaceholderText("选择变量作为Excel的列名称，变量数据会存到对应的列")
        self.save_excel_columns.setStyleSheet(self.get_input_style())
        config_layout.addRow("选择保存列:", self.save_excel_columns)

        parent_layout.addWidget(config_group)

    def create_import_txt_exact_config(self, parent_layout):
        """导入txt - 完全按照AdsPower原版界面"""
        config_group = QGroupBox("导入txt设置")
        config_layout = QFormLayout(config_group)

        # 文件路径
        file_widget = QWidget()
        file_layout = QHBoxLayout(file_widget)
        file_layout.setContentsMargins(0, 0, 0, 0)

        self.import_txt_path = QLineEdit()
        self.import_txt_path.setPlaceholderText("选择要导入的txt文件")
        self.import_txt_path.setStyleSheet(self.get_input_style())
        file_layout.addWidget(self.import_txt_path)

        browse_btn = QPushButton("浏览")
        browse_btn.setFixedWidth(60)
        browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                color: #333333;
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 6px;
            }
            QPushButton:hover {
                border-color: #1890ff;
                color: #1890ff;
            }
        """)
        file_layout.addWidget(browse_btn)

        config_layout.addRow("文件路径:", file_widget)

        # 提取方式
        self.import_txt_method = QComboBox()
        self.import_txt_method.addItems(["顺序提取", "随机提取"])
        self.import_txt_method.setStyleSheet(self.get_input_style())
        config_layout.addRow("提取方式:", self.import_txt_method)

        # 保存至
        self.import_txt_save_var = QLineEdit()
        self.import_txt_save_var.setPlaceholderText("请输入保存内容的变量名")
        self.import_txt_save_var.setStyleSheet(self.get_input_style())
        config_layout.addRow("保存至:", self.import_txt_save_var)

        parent_layout.addWidget(config_group)

    def create_get_email_exact_config(self, parent_layout):
        """获取邮件 - 完全按照AdsPower原版界面"""
        config_group = QGroupBox("获取邮件设置")
        config_layout = QFormLayout(config_group)

        # 使用变量选项
        self.email_use_variable = QCheckBox("使用变量")
        config_layout.addRow("", self.email_use_variable)

        # 邮箱
        self.email_address = QLineEdit()
        self.email_address.setPlaceholderText("输入邮箱账号")
        self.email_address.setStyleSheet(self.get_input_style())
        config_layout.addRow("邮箱:", self.email_address)

        # 密码/授权码
        self.email_password = QLineEdit()
        self.email_password.setPlaceholderText("输入邮箱密码或授权码")
        self.email_password.setEchoMode(QLineEdit.Password)
        self.email_password.setStyleSheet(self.get_input_style())
        config_layout.addRow("密码/授权码:", self.email_password)

        # 邮箱服务器
        self.email_server = QLineEdit()
        self.email_server.setPlaceholderText("请输入邮箱服务器，如：imap.gmail.com")
        self.email_server.setStyleSheet(self.get_input_style())
        config_layout.addRow("邮箱服务器:", self.email_server)

        # 端口
        self.email_port = QSpinBox()
        self.email_port.setRange(1, 65535)
        self.email_port.setValue(993)
        self.email_port.setStyleSheet(self.get_input_style())
        config_layout.addRow("端口:", self.email_port)

        # 状态选项
        status_widget = QWidget()
        status_layout = QVBoxLayout(status_widget)
        status_layout.setContentsMargins(0, 0, 0, 0)

        self.email_mark_read = QCheckBox("标为已读")
        self.email_from_spam = QCheckBox("从垃圾邮件获取")
        status_layout.addWidget(self.email_mark_read)
        status_layout.addWidget(self.email_from_spam)

        config_layout.addRow("状态:", status_widget)

        # 邮件时间
        time_widget = QWidget()
        time_layout = QHBoxLayout(time_widget)
        time_layout.setContentsMargins(0, 0, 0, 0)

        self.email_time_value = QSpinBox()
        self.email_time_value.setRange(1, 999)
        self.email_time_value.setValue(24)
        self.email_time_value.setStyleSheet(self.get_input_style())
        time_layout.addWidget(self.email_time_value)

        self.email_time_unit = QComboBox()
        self.email_time_unit.addItems(["小时", "天"])
        self.email_time_unit.setStyleSheet(self.get_input_style())
        time_layout.addWidget(self.email_time_unit)

        config_layout.addRow("邮件时间:", time_widget)

        # 发件人
        self.email_sender = QLineEdit()
        self.email_sender.setPlaceholderText("发件人关键字，留空即全部")
        self.email_sender.setStyleSheet(self.get_input_style())
        config_layout.addRow("发件人:", self.email_sender)

        # 邮件标题
        self.email_subject = QLineEdit()
        self.email_subject.setPlaceholderText("标题关键字，留空即全部")
        self.email_subject.setStyleSheet(self.get_input_style())
        config_layout.addRow("邮件标题:", self.email_subject)

        # 提取规则
        self.email_extract_rule = QLineEdit()
        self.email_extract_rule.setPlaceholderText("如：FB-(\\d*)，提取FB-后面的数字")
        self.email_extract_rule.setStyleSheet(self.get_input_style())
        config_layout.addRow("提取规则:", self.email_extract_rule)

        # 保存至
        self.email_save_var = QLineEdit()
        self.email_save_var.setPlaceholderText("请输入保存邮件内容的变量名")
        self.email_save_var.setStyleSheet(self.get_input_style())
        config_layout.addRow("保存至:", self.email_save_var)

        parent_layout.addWidget(config_group)

    def create_get_totp_exact_config(self, parent_layout):
        """身份验证器码 - 完全按照AdsPower原版界面"""
        config_group = QGroupBox("身份验证器码设置")
        config_layout = QFormLayout(config_group)

        # 密钥
        self.totp_secret = QLineEdit()
        self.totp_secret.setPlaceholderText("输入身份验证器密钥")
        self.totp_secret.setStyleSheet(self.get_input_style())
        config_layout.addRow("密钥:", self.totp_secret)

        # 保存至
        self.totp_save_var = QLineEdit()
        self.totp_save_var.setPlaceholderText("请输入保存验证码的变量名")
        self.totp_save_var.setStyleSheet(self.get_input_style())
        config_layout.addRow("保存至:", self.totp_save_var)

        # 说明文本
        info_label = QLabel("例如，开启Facebook的二次验证，会提供一串代码，将此代码复制到密钥")
        info_label.setStyleSheet("color: #666666; font-size: 12px; margin-top: 10px;")
        config_layout.addRow("", info_label)

        parent_layout.addWidget(config_group)

    def create_listen_request_trigger_exact_config(self, parent_layout):
        """监听请求触发 - 完全按照AdsPower原版界面"""
        config_group = QGroupBox("监听请求触发设置")
        config_layout = QFormLayout(config_group)

        # 请求URL
        self.listen_trigger_url = QLineEdit()
        self.listen_trigger_url.setPlaceholderText("例如：https://www.adspower.net/download?type=test")
        self.listen_trigger_url.setStyleSheet(self.get_input_style())
        config_layout.addRow("请求URL:", self.listen_trigger_url)

        # 提取类型
        self.listen_trigger_extract_type = QComboBox()
        self.listen_trigger_extract_type.addItems(["完整URL", "请求头", "Get参数", "Post数据"])
        self.listen_trigger_extract_type.setStyleSheet(self.get_input_style())
        config_layout.addRow("提取类型:", self.listen_trigger_extract_type)

        # 参数名（当选择Get参数时显示）
        self.listen_trigger_param_name = QLineEdit()
        self.listen_trigger_param_name.setPlaceholderText("请输入参数名，如：type")
        self.listen_trigger_param_name.setStyleSheet(self.get_input_style())
        self.listen_trigger_param_name.setEnabled(False)
        config_layout.addRow("参数名:", self.listen_trigger_param_name)

        # 保存至
        self.listen_trigger_save_var = QLineEdit()
        self.listen_trigger_save_var.setPlaceholderText("请输入保存内容的变量名")
        self.listen_trigger_save_var.setStyleSheet(self.get_input_style())
        config_layout.addRow("保存至:", self.listen_trigger_save_var)

        # 连接信号
        self.listen_trigger_extract_type.currentTextChanged.connect(
            lambda text: self.listen_trigger_param_name.setEnabled(text == "Get参数")
        )

        parent_layout.addWidget(config_group)

    def create_listen_request_result_exact_config(self, parent_layout):
        """监听请求结果 - 完全按照AdsPower原版界面"""
        config_group = QGroupBox("监听请求结果设置")
        config_layout = QFormLayout(config_group)

        # 请求URL
        self.listen_result_url = QLineEdit()
        self.listen_result_url.setPlaceholderText("例如：https://www.adspower.net/download")
        self.listen_result_url.setStyleSheet(self.get_input_style())
        config_layout.addRow("请求URL:", self.listen_result_url)

        # 保存至
        self.listen_result_save_var = QLineEdit()
        self.listen_result_save_var.setPlaceholderText("请输入保存请求结果的变量名")
        self.listen_result_save_var.setStyleSheet(self.get_input_style())
        config_layout.addRow("保存至:", self.listen_result_save_var)

        parent_layout.addWidget(config_group)

    def create_stop_page_listening_exact_config(self, parent_layout):
        """停止页面监听 - 完全按照AdsPower原版界面"""
        info_group = QGroupBox("操作说明")
        info_layout = QVBoxLayout(info_group)

        info_text = QLabel("可以在适当的时候，停止以上监听事件")
        info_text.setStyleSheet("color: #666666; font-size: 13px; padding: 10px;")
        info_layout.addWidget(info_text)

        parent_layout.addWidget(info_group)

    def create_get_page_cookies_exact_config(self, parent_layout):
        """获取页面Cookie - 完全按照AdsPower原版界面"""
        config_group = QGroupBox("获取页面Cookie设置")
        config_layout = QFormLayout(config_group)

        # 保存至
        self.get_cookies_save_var = QLineEdit()
        self.get_cookies_save_var.setPlaceholderText("请输入保存Cookie的变量名")
        self.get_cookies_save_var.setStyleSheet(self.get_input_style())
        config_layout.addRow("保存至:", self.get_cookies_save_var)

        # 说明文本
        info_label = QLabel("获取页面的cookies并保存为变量使用")
        info_label.setStyleSheet("color: #666666; font-size: 12px; margin-top: 10px;")
        config_layout.addRow("", info_label)

        parent_layout.addWidget(config_group)

    def create_clear_page_cookies_exact_config(self, parent_layout):
        """清除页面Cookie - 完全按照AdsPower原版界面"""
        info_group = QGroupBox("操作说明")
        info_layout = QVBoxLayout(info_group)

        info_text = QLabel("清除页面的cookies，清除后登录的账号将需要重新登录")
        info_text.setStyleSheet("color: #666666; font-size: 13px; padding: 10px;")
        info_layout.addWidget(info_text)

        parent_layout.addWidget(info_group)

    def create_upload_file_exact_config(self, parent_layout):
        """上传附件 - 完全按照AdsPower原版界面"""

        # 顶部标签页选择 (元素选择器/储存的元素对象)
        tab_group = QWidget()
        tab_layout = QHBoxLayout(tab_group)
        tab_layout.setContentsMargins(0, 0, 0, 16)
        tab_layout.setSpacing(0)

        # 元素选择器标签
        self.upload_selector_tab = QPushButton("元素选择器")
        self.upload_selector_tab.setFixedHeight(32)
        self.upload_selector_tab.setCheckable(True)
        self.upload_selector_tab.setChecked(True)  # 默认选中

        # 储存的元素对象标签
        self.upload_stored_tab = QPushButton("储存的元素对象")
        self.upload_stored_tab.setFixedHeight(32)
        self.upload_stored_tab.setCheckable(True)

        # 标签页样式
        tab_style = """
            QPushButton {
                border: 1px solid #d9d9d9;
                background-color: #f5f5f5;
                color: #666;
                font-size: 12px;
                padding: 0 16px;
            }
            QPushButton:checked {
                background-color: white;
                color: #1890ff;
                border-bottom: 2px solid #1890ff;
            }
            QPushButton:hover {
                background-color: #e6f7ff;
            }
        """

        self.upload_selector_tab.setStyleSheet(tab_style)
        self.upload_stored_tab.setStyleSheet(tab_style)

        # 标签页按钮组
        self.upload_tab_group = QButtonGroup()
        self.upload_tab_group.addButton(self.upload_selector_tab, 0)
        self.upload_tab_group.addButton(self.upload_stored_tab, 1)

        # 连接标签页切换事件
        self.upload_selector_tab.clicked.connect(lambda: self.switch_upload_tab(0))
        self.upload_stored_tab.clicked.connect(lambda: self.switch_upload_tab(1))

        tab_layout.addWidget(self.upload_selector_tab)
        tab_layout.addWidget(self.upload_stored_tab)
        tab_layout.addStretch()

        parent_layout.addWidget(tab_group)

        # 创建两个内容区域
        self.upload_selector_content = QWidget()
        self.upload_stored_content = QWidget()

        # 元素选择器内容
        self.create_upload_selector_content(self.upload_selector_content)
        parent_layout.addWidget(self.upload_selector_content)

        # 储存的元素对象内容
        self.create_upload_stored_content(self.upload_stored_content)
        parent_layout.addWidget(self.upload_stored_content)
        self.upload_stored_content.setVisible(False)  # 默认隐藏

        # 附件配置（两个标签页共用）
        self.create_upload_attachment_config(parent_layout)

    def create_upload_selector_content(self, parent_widget):
        """创建元素选择器内容区域"""
        layout = QVBoxLayout(parent_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 元素选择器选择 (Selector/XPath/文本)
        selector_type_group = QWidget()
        selector_type_layout = QHBoxLayout(selector_type_group)
        selector_type_layout.setContentsMargins(0, 0, 0, 16)
        selector_type_layout.setSpacing(16)

        selector_type_label = QLabel("选择器")
        selector_type_label.setFixedWidth(80)
        selector_type_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 500;")

        # 选择器类型单选按钮
        self.upload_selector_radio = QRadioButton("Selector")
        self.upload_xpath_radio = QRadioButton("XPath")
        self.upload_text_radio = QRadioButton("文本")

        self.upload_selector_radio.setChecked(True)  # 默认选中Selector

        for radio in [self.upload_selector_radio, self.upload_xpath_radio, self.upload_text_radio]:
            radio.setStyleSheet("""
                QRadioButton {
                    font-size: 12px;
                    color: #333;
                    spacing: 8px;
                }
                QRadioButton::indicator {
                    width: 16px;
                    height: 16px;
                }
                QRadioButton::indicator:unchecked {
                    border: 2px solid #d9d9d9;
                    border-radius: 8px;
                    background-color: white;
                }
                QRadioButton::indicator:checked {
                    border: 2px solid #1890ff;
                    border-radius: 8px;
                    background-color: #1890ff;
                }
                QRadioButton::indicator:checked:after {
                    content: '';
                    width: 6px;
                    height: 6px;
                    border-radius: 3px;
                    background-color: white;
                    margin: 3px;
                }
            """)

        selector_type_layout.addWidget(selector_type_label)
        selector_type_layout.addWidget(self.upload_selector_radio)
        selector_type_layout.addWidget(self.upload_xpath_radio)
        selector_type_layout.addWidget(self.upload_text_radio)
        selector_type_layout.addStretch()

        layout.addWidget(selector_type_group)

        # 选择器输入框
        selector_input_group = QWidget()
        selector_input_layout = QHBoxLayout(selector_input_group)
        selector_input_layout.setContentsMargins(80, 8, 0, 16)  # 左边距对齐标签

        self.upload_selector_input = QLineEdit()
        self.upload_selector_input.setPlaceholderText("请输入元素选择器，比如 #email input")
        self.upload_selector_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 12px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #40a9ff;
                outline: none;
            }
        """)

        upload_selector_var_btn = QPushButton("使用变量")
        upload_selector_var_btn.setFixedSize(80, 32)
        upload_selector_var_btn.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                color: #666;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #e6f7ff;
                border-color: #40a9ff;
                color: #1890ff;
            }
        """)
        upload_selector_var_btn.clicked.connect(self.show_upload_selector_variables)

        selector_input_layout.addWidget(self.upload_selector_input)
        selector_input_layout.addWidget(upload_selector_var_btn)

        layout.addWidget(selector_input_group)

        # 元素顺序
        order_group = QWidget()
        order_layout = QHBoxLayout(order_group)
        order_layout.setContentsMargins(0, 0, 0, 16)

        order_label = QLabel("元素顺序")
        order_label.setFixedWidth(80)
        order_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 500;")

        self.upload_order_value = QLineEdit("1")
        self.upload_order_value.setFixedWidth(120)
        self.upload_order_value.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 12px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #40a9ff;
                outline: none;
            }
        """)

        upload_order_var_btn = QPushButton("使用变量")
        upload_order_var_btn.setFixedSize(80, 32)
        upload_order_var_btn.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                color: #666;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #e6f7ff;
                border-color: #40a9ff;
                color: #1890ff;
            }
        """)
        upload_order_var_btn.clicked.connect(self.show_upload_order_variables)

        order_layout.addWidget(order_label)
        order_layout.addWidget(self.upload_order_value)
        order_layout.addWidget(upload_order_var_btn)
        order_layout.addStretch()

        layout.addWidget(order_group)

    def create_upload_stored_content(self, parent_widget):
        """创建储存的元素对象内容区域"""
        layout = QVBoxLayout(parent_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 元素对象选择
        stored_element_group = QWidget()
        stored_element_layout = QHBoxLayout(stored_element_group)
        stored_element_layout.setContentsMargins(0, 0, 0, 16)

        stored_element_label = QLabel("元素对象")
        stored_element_label.setFixedWidth(80)
        stored_element_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 500;")

        self.upload_stored_element = QComboBox()
        self.upload_stored_element.addItem("请选择")
        # 添加一些示例变量
        example_vars = ["element_obj_1", "saved_element", "target_element", "form_element"]
        for var in example_vars:
            self.upload_stored_element.addItem(var)
        self.upload_stored_element.setStyleSheet("""
            QComboBox {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 12px;
                background-color: white;
            }
            QComboBox:focus {
                border-color: #40a9ff;
                outline: none;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #999;
                margin-right: 5px;
            }
        """)

        stored_element_layout.addWidget(stored_element_label)
        stored_element_layout.addWidget(self.upload_stored_element)
        stored_element_layout.addStretch()

        layout.addWidget(stored_element_group)

    def create_upload_attachment_config(self, parent_layout):
        """创建附件配置区域（两个标签页共用）"""

        # 附件类型选择 (本地文件/文件夹文件随机/网络URL)
        attachment_type_group = QWidget()
        attachment_type_layout = QHBoxLayout(attachment_type_group)
        attachment_type_layout.setContentsMargins(0, 0, 0, 16)
        attachment_type_layout.setSpacing(16)

        attachment_type_label = QLabel("附件")
        attachment_type_label.setFixedWidth(80)
        attachment_type_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 500;")

        # 附件类型按钮
        self.upload_local_btn = QPushButton("本地文件")
        self.upload_folder_btn = QPushButton("文件夹文件随机")
        self.upload_url_btn = QPushButton("网络URL")

        for btn in [self.upload_local_btn, self.upload_folder_btn, self.upload_url_btn]:
            btn.setFixedHeight(32)
            btn.setStyleSheet("""
                QPushButton {
                    border: 1px solid #d9d9d9;
                    border-radius: 4px;
                    background-color: white;
                    color: #666;
                    font-size: 12px;
                    padding: 0 12px;
                }
                QPushButton:checked {
                    background-color: #1890ff;
                    color: white;
                    border-color: #1890ff;
                }
                QPushButton:hover {
                    border-color: #40a9ff;
                }
            """)
            btn.setCheckable(True)

        self.upload_local_btn.setChecked(True)  # 默认选中本地文件

        # 按钮组确保只能选择一个
        self.upload_type_group = QButtonGroup()
        self.upload_type_group.addButton(self.upload_local_btn, 0)
        self.upload_type_group.addButton(self.upload_folder_btn, 1)
        self.upload_type_group.addButton(self.upload_url_btn, 2)

        # 连接按钮点击事件
        self.upload_local_btn.clicked.connect(lambda: self.on_upload_type_changed(self.upload_local_btn))
        self.upload_folder_btn.clicked.connect(lambda: self.on_upload_type_changed(self.upload_folder_btn))
        self.upload_url_btn.clicked.connect(lambda: self.on_upload_type_changed(self.upload_url_btn))

        attachment_type_layout.addWidget(attachment_type_label)
        attachment_type_layout.addWidget(self.upload_local_btn)
        attachment_type_layout.addWidget(self.upload_folder_btn)
        attachment_type_layout.addWidget(self.upload_url_btn)
        attachment_type_layout.addStretch()

        parent_layout.addWidget(attachment_type_group)

        # 本地文件路径输入 (默认显示)
        self.upload_local_widget = QWidget()
        local_layout = QHBoxLayout(self.upload_local_widget)
        local_layout.setContentsMargins(80, 8, 0, 16)

        self.upload_local_path = QLineEdit()
        self.upload_local_path.setPlaceholderText("读取本地文件路径")
        self.upload_local_path.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 12px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #40a9ff;
                outline: none;
            }
        """)

        upload_browse_btn = QPushButton("浏览文件")
        upload_browse_btn.setFixedSize(80, 32)
        upload_browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #1890ff;
                border: 1px solid #1890ff;
                border-radius: 4px;
                color: white;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #40a9ff;
                border-color: #40a9ff;
            }
        """)
        upload_browse_btn.clicked.connect(self.browse_upload_file)

        upload_local_var_btn = QPushButton("使用变量")
        upload_local_var_btn.setFixedSize(80, 32)
        upload_local_var_btn.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                color: #666;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #e6f7ff;
                border-color: #40a9ff;
                color: #1890ff;
            }
        """)
        upload_local_var_btn.clicked.connect(self.show_upload_local_variables)

        local_layout.addWidget(self.upload_local_path)
        local_layout.addWidget(upload_browse_btn)
        local_layout.addWidget(upload_local_var_btn)

        parent_layout.addWidget(self.upload_local_widget)

        # 网络URL输入 (默认隐藏)
        self.upload_url_widget = QWidget()
        url_layout = QHBoxLayout(self.upload_url_widget)
        url_layout.setContentsMargins(80, 8, 0, 16)

        self.upload_url_path = QLineEdit()
        self.upload_url_path.setPlaceholderText("请输入正确的URL")
        self.upload_url_path.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 12px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #40a9ff;
                outline: none;
            }
        """)

        upload_url_var_btn = QPushButton("使用变量")
        upload_url_var_btn.setFixedSize(80, 32)
        upload_url_var_btn.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                color: #666;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #e6f7ff;
                border-color: #40a9ff;
                color: #1890ff;
            }
        """)
        upload_url_var_btn.clicked.connect(self.show_upload_url_variables)

        url_layout.addWidget(self.upload_url_path)
        url_layout.addWidget(upload_url_var_btn)

        parent_layout.addWidget(self.upload_url_widget)
        self.upload_url_widget.setVisible(False)  # 默认隐藏

        # 超时等待
        timeout_group = QWidget()
        timeout_layout = QHBoxLayout(timeout_group)
        timeout_layout.setContentsMargins(0, 0, 0, 16)

        timeout_label = QLabel("超时等待")
        timeout_label.setFixedWidth(80)
        timeout_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 500;")

        self.upload_timeout = QSpinBox()
        self.upload_timeout.setRange(1000, 300000)  # 1秒到5分钟
        self.upload_timeout.setValue(30000)  # 默认30秒
        self.upload_timeout.setSuffix(" 毫秒")
        self.upload_timeout.setFixedWidth(120)
        self.upload_timeout.setStyleSheet("""
            QSpinBox {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 12px;
                background-color: white;
            }
            QSpinBox:focus {
                border-color: #40a9ff;
                outline: none;
            }
            QSpinBox::up-button {
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 16px;
                border-left: 1px solid #d9d9d9;
                border-bottom: 1px solid #d9d9d9;
                border-top-right-radius: 4px;
                background-color: #f5f5f5;
            }
            QSpinBox::down-button {
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 16px;
                border-left: 1px solid #d9d9d9;
                border-top: 1px solid #d9d9d9;
                border-bottom-right-radius: 4px;
                background-color: #f5f5f5;
            }
            QSpinBox::up-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-bottom: 4px solid #666;
                width: 0px;
                height: 0px;
            }
            QSpinBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid #666;
                width: 0px;
                height: 0px;
            }
        """)

        timeout_desc_label = QLabel("1 秒 = 1000 毫秒")
        timeout_desc_label.setStyleSheet("font-size: 12px; color: #666; margin-left: 16px;")

        timeout_layout.addWidget(timeout_label)
        timeout_layout.addWidget(self.upload_timeout)
        timeout_layout.addWidget(timeout_desc_label)
        timeout_layout.addStretch()

        parent_layout.addWidget(timeout_group)

        # 说明
        desc_group = QWidget()
        desc_layout = QHBoxLayout(desc_group)
        desc_layout.setContentsMargins(0, 0, 0, 0)

        desc_label = QLabel("说明")
        desc_label.setFixedWidth(80)
        desc_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 500;")

        self.upload_description = QLineEdit()
        self.upload_description.setPlaceholderText("选填")
        self.upload_description.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 12px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #40a9ff;
                outline: none;
            }
        """)

        desc_layout.addWidget(desc_label)
        desc_layout.addWidget(self.upload_description)

        parent_layout.addWidget(desc_group)

    def create_execute_js_exact_config(self, parent_layout):
        """执行JS脚本 - 完全按照AdsPower原版界面"""
        config_group = QGroupBox("执行JS脚本设置")
        config_layout = QFormLayout(config_group)

        # JS代码
        self.js_code = QTextEdit()
        self.js_code.setFixedHeight(150)
        self.js_code.setPlaceholderText("请输入要执行的JavaScript代码")
        self.js_code.setStyleSheet(self.get_input_style())
        config_layout.addRow("JS代码:", self.js_code)

        # 保存返回值
        self.js_save_result = QCheckBox("保存返回值")
        config_layout.addRow("", self.js_save_result)

        # 保存至变量
        self.js_save_var = QLineEdit()
        self.js_save_var.setPlaceholderText("请输入保存返回值的变量名")
        self.js_save_var.setStyleSheet(self.get_input_style())
        self.js_save_var.setEnabled(False)
        config_layout.addRow("保存至:", self.js_save_var)

        # 连接信号
        self.js_save_result.toggled.connect(self.js_save_var.setEnabled)

        parent_layout.addWidget(config_group)

    def create_scroll_page_exact_config(self, parent_layout):
        """滚动页面 - 完全按照您的截图实现"""

        # 类型选择 (页面/选择器)
        type_group = QWidget()
        type_layout = QHBoxLayout(type_group)
        type_layout.setContentsMargins(0, 0, 0, 16)
        type_layout.setSpacing(16)

        type_label = QLabel("类型")
        type_label.setFixedWidth(80)
        type_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 500;")

        # 页面和选择器按钮
        self.scroll_page_btn = QPushButton("页面")
        self.scroll_selector_btn = QPushButton("选择器")

        for btn in [self.scroll_page_btn, self.scroll_selector_btn]:
            btn.setFixedSize(80, 32)
            btn.setStyleSheet("""
                QPushButton {
                    border: 1px solid #d9d9d9;
                    border-radius: 4px;
                    background-color: white;
                    color: #666;
                    font-size: 12px;
                }
                QPushButton:checked {
                    background-color: #1890ff;
                    color: white;
                    border-color: #1890ff;
                }
                QPushButton:hover {
                    border-color: #40a9ff;
                }
            """)
            btn.setCheckable(True)

        self.scroll_page_btn.setChecked(True)  # 默认选中页面

        # 按钮组确保只能选择一个
        self.scroll_type_group = QButtonGroup()
        self.scroll_type_group.addButton(self.scroll_page_btn, 0)
        self.scroll_type_group.addButton(self.scroll_selector_btn, 1)

        # 直接连接按钮的点击事件
        self.scroll_page_btn.clicked.connect(lambda: self.on_scroll_type_changed(self.scroll_page_btn))
        self.scroll_selector_btn.clicked.connect(lambda: self.on_scroll_type_changed(self.scroll_selector_btn))

        type_layout.addWidget(type_label)
        type_layout.addWidget(self.scroll_page_btn)
        type_layout.addWidget(self.scroll_selector_btn)
        type_layout.addStretch()

        parent_layout.addWidget(type_group)

        # 选择器配置区域 (默认隐藏)
        self.scroll_selector_widget = QWidget()
        selector_layout = QVBoxLayout(self.scroll_selector_widget)
        selector_layout.setContentsMargins(0, 0, 0, 16)

        # Selector/XPath/文本选择
        selector_type_widget = QWidget()
        selector_type_layout = QHBoxLayout(selector_type_widget)
        selector_type_layout.setContentsMargins(0, 0, 0, 0)
        selector_type_layout.setSpacing(16)

        selector_type_label = QLabel("选择器")
        selector_type_label.setFixedWidth(80)
        selector_type_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 500;")

        # 选择器类型单选按钮
        self.scroll_selector_radio = QRadioButton("Selector")
        self.scroll_xpath_radio = QRadioButton("XPath")
        self.scroll_text_radio = QRadioButton("文本")

        self.scroll_selector_radio.setChecked(True)  # 默认选中Selector

        for radio in [self.scroll_selector_radio, self.scroll_xpath_radio, self.scroll_text_radio]:
            radio.setStyleSheet("""
                QRadioButton {
                    font-size: 12px;
                    color: #333;
                    spacing: 8px;
                }
                QRadioButton::indicator {
                    width: 16px;
                    height: 16px;
                }
                QRadioButton::indicator:unchecked {
                    border: 2px solid #d9d9d9;
                    border-radius: 8px;
                    background-color: white;
                }
                QRadioButton::indicator:checked {
                    border: 2px solid #1890ff;
                    border-radius: 8px;
                    background-color: #1890ff;
                }
                QRadioButton::indicator:checked:after {
                    content: '';
                    width: 6px;
                    height: 6px;
                    border-radius: 3px;
                    background-color: white;
                    margin: 3px;
                }
            """)

        selector_type_layout.addWidget(selector_type_label)
        selector_type_layout.addWidget(self.scroll_selector_radio)
        selector_type_layout.addWidget(self.scroll_xpath_radio)
        selector_type_layout.addWidget(self.scroll_text_radio)
        selector_type_layout.addStretch()

        selector_layout.addWidget(selector_type_widget)

        # 选择器输入框
        selector_input_group = QWidget()
        selector_input_layout = QHBoxLayout(selector_input_group)
        selector_input_layout.setContentsMargins(80, 8, 0, 0)  # 左边距对齐标签

        self.scroll_selector_input = QLineEdit()
        self.scroll_selector_input.setPlaceholderText("请输入元素选择器，比如 #email input")
        self.scroll_selector_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 12px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #40a9ff;
                outline: none;
            }
        """)

        scroll_selector_var_btn = QPushButton("使用变量")
        scroll_selector_var_btn.setFixedSize(80, 32)
        scroll_selector_var_btn.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                color: #666;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #e6f7ff;
                border-color: #40a9ff;
                color: #1890ff;
            }
        """)
        scroll_selector_var_btn.clicked.connect(self.show_scroll_selector_variables)

        selector_input_layout.addWidget(self.scroll_selector_input)
        selector_input_layout.addWidget(scroll_selector_var_btn)

        selector_layout.addWidget(selector_input_group)

        # 元素顺序
        order_group = QWidget()
        order_layout = QHBoxLayout(order_group)
        order_layout.setContentsMargins(0, 8, 0, 0)

        order_label = QLabel("元素顺序")
        order_label.setFixedWidth(80)
        order_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 500;")

        self.scroll_order_value = QLineEdit("1")
        self.scroll_order_value.setFixedWidth(120)
        self.scroll_order_value.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 12px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #40a9ff;
                outline: none;
            }
        """)

        scroll_order_var_btn = QPushButton("使用变量")
        scroll_order_var_btn.setFixedSize(80, 32)
        scroll_order_var_btn.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                color: #666;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #e6f7ff;
                border-color: #40a9ff;
                color: #1890ff;
            }
        """)
        scroll_order_var_btn.clicked.connect(self.show_scroll_order_variables)

        order_layout.addWidget(order_label)
        order_layout.addWidget(self.scroll_order_value)
        order_layout.addWidget(scroll_order_var_btn)
        order_layout.addStretch()

        selector_layout.addWidget(order_group)

        parent_layout.addWidget(self.scroll_selector_widget)
        self.scroll_selector_widget.setVisible(False)  # 默认隐藏

        # 位置配置 - 两个下拉框
        position_group = QWidget()
        position_layout = QHBoxLayout(position_group)
        position_layout.setContentsMargins(0, 0, 0, 16)

        position_label = QLabel("位置")
        position_label.setFixedWidth(80)
        position_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 500;")

        # 第一个下拉框：位置类型
        self.scroll_position_type = QComboBox()
        self.scroll_position_type.addItems(["位置", "像素"])
        self.scroll_position_type.setFixedWidth(120)
        self.scroll_position_type.setStyleSheet("""
            QComboBox {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 12px;
                background-color: white;
            }
            QComboBox:focus {
                border-color: #40a9ff;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #999;
                margin-right: 5px;
            }
        """)

        # 第二个下拉框：具体位置
        self.scroll_position_value = QComboBox()
        self.scroll_position_value.addItems(["底部", "顶部", "中间"])
        self.scroll_position_value.setFixedWidth(120)
        self.scroll_position_value.setStyleSheet("""
            QComboBox {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 12px;
                background-color: white;
            }
            QComboBox:focus {
                border-color: #40a9ff;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #999;
                margin-right: 5px;
            }
        """)

        position_layout.addWidget(position_label)
        position_layout.addWidget(self.scroll_position_type)
        position_layout.addWidget(self.scroll_position_value)
        position_layout.addStretch()

        parent_layout.addWidget(position_group)

        # 滚动类型
        scroll_type_group = QWidget()
        scroll_type_layout = QHBoxLayout(scroll_type_group)
        scroll_type_layout.setContentsMargins(0, 0, 0, 16)

        scroll_type_label = QLabel("滚动类型")
        scroll_type_label.setFixedWidth(80)
        scroll_type_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 500;")

        self.scroll_type_combo = QComboBox()
        self.scroll_type_combo.addItems(["平滑", "瞬间"])
        self.scroll_type_combo.setFixedWidth(120)
        self.scroll_type_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 12px;
                background-color: white;
            }
            QComboBox:focus {
                border-color: #40a9ff;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #999;
                margin-right: 5px;
            }
        """)

        scroll_type_layout.addWidget(scroll_type_label)
        scroll_type_layout.addWidget(self.scroll_type_combo)
        scroll_type_layout.addStretch()

        parent_layout.addWidget(scroll_type_group)

        # 滚动速度
        speed_group = QWidget()
        speed_layout = QHBoxLayout(speed_group)
        speed_layout.setContentsMargins(0, 0, 0, 16)

        speed_label = QLabel("滚动速度")
        speed_label.setFixedWidth(80)
        speed_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 500;")

        speed_desc_label = QLabel("单次滚动范围在")
        speed_desc_label.setStyleSheet("font-size: 12px; color: #666;")

        self.scroll_speed_min = QSpinBox()
        self.scroll_speed_min.setRange(1, 9999)
        self.scroll_speed_min.setValue(100)
        self.scroll_speed_min.setFixedWidth(80)
        self.scroll_speed_min.setStyleSheet("""
            QSpinBox {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 12px;
                background-color: white;
            }
            QSpinBox:focus {
                border-color: #40a9ff;
                outline: none;
            }
            QSpinBox::up-button {
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 16px;
                border-left: 1px solid #d9d9d9;
                border-bottom: 1px solid #d9d9d9;
                border-top-right-radius: 4px;
                background-color: #f5f5f5;
            }
            QSpinBox::down-button {
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 16px;
                border-left: 1px solid #d9d9d9;
                border-top: 1px solid #d9d9d9;
                border-bottom-right-radius: 4px;
                background-color: #f5f5f5;
            }
            QSpinBox::up-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-bottom: 4px solid #666;
                width: 0px;
                height: 0px;
            }
            QSpinBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid #666;
                width: 0px;
                height: 0px;
            }
        """)

        dash_label = QLabel("-")
        dash_label.setStyleSheet("font-size: 12px; color: #666; margin: 0 8px;")

        self.scroll_speed_max = QSpinBox()
        self.scroll_speed_max.setRange(1, 9999)
        self.scroll_speed_max.setValue(150)
        self.scroll_speed_max.setFixedWidth(80)
        self.scroll_speed_max.setStyleSheet("""
            QSpinBox {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 12px;
                background-color: white;
            }
            QSpinBox:focus {
                border-color: #40a9ff;
                outline: none;
            }
            QSpinBox::up-button {
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 16px;
                border-left: 1px solid #d9d9d9;
                border-bottom: 1px solid #d9d9d9;
                border-top-right-radius: 4px;
                background-color: #f5f5f5;
            }
            QSpinBox::down-button {
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 16px;
                border-left: 1px solid #d9d9d9;
                border-top: 1px solid #d9d9d9;
                border-bottom-right-radius: 4px;
                background-color: #f5f5f5;
            }
            QSpinBox::up-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-bottom: 4px solid #666;
                width: 0px;
                height: 0px;
            }
            QSpinBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid #666;
                width: 0px;
                height: 0px;
            }
        """)

        speed_unit_label = QLabel("像素之间随机")
        speed_unit_label.setStyleSheet("font-size: 12px; color: #666;")

        speed_layout.addWidget(speed_label)
        speed_layout.addWidget(speed_desc_label)
        speed_layout.addWidget(self.scroll_speed_min)
        speed_layout.addWidget(dash_label)
        speed_layout.addWidget(self.scroll_speed_max)
        speed_layout.addWidget(speed_unit_label)
        speed_layout.addStretch()

        parent_layout.addWidget(speed_group)

        # 停留时长
        duration_group = QWidget()
        duration_layout = QHBoxLayout(duration_group)
        duration_layout.setContentsMargins(0, 0, 0, 16)

        duration_label = QLabel("停留时长在")
        duration_label.setFixedWidth(80)
        duration_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 500;")

        self.scroll_duration_min = QSpinBox()
        self.scroll_duration_min.setRange(1, 9999)
        self.scroll_duration_min.setValue(200)
        self.scroll_duration_min.setFixedWidth(80)
        self.scroll_duration_min.setStyleSheet("""
            QSpinBox {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 12px;
                background-color: white;
            }
            QSpinBox:focus {
                border-color: #40a9ff;
                outline: none;
            }
            QSpinBox::up-button {
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 16px;
                border-left: 1px solid #d9d9d9;
                border-bottom: 1px solid #d9d9d9;
                border-top-right-radius: 4px;
                background-color: #f5f5f5;
            }
            QSpinBox::down-button {
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 16px;
                border-left: 1px solid #d9d9d9;
                border-top: 1px solid #d9d9d9;
                border-bottom-right-radius: 4px;
                background-color: #f5f5f5;
            }
            QSpinBox::up-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-bottom: 4px solid #666;
                width: 0px;
                height: 0px;
            }
            QSpinBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid #666;
                width: 0px;
                height: 0px;
            }
        """)

        dash_label2 = QLabel("-")
        dash_label2.setStyleSheet("font-size: 12px; color: #666; margin: 0 8px;")

        self.scroll_duration_max = QSpinBox()
        self.scroll_duration_max.setRange(1, 9999)
        self.scroll_duration_max.setValue(300)
        self.scroll_duration_max.setFixedWidth(80)
        self.scroll_duration_max.setStyleSheet("""
            QSpinBox {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 12px;
                background-color: white;
            }
            QSpinBox:focus {
                border-color: #40a9ff;
                outline: none;
            }
            QSpinBox::up-button {
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 16px;
                border-left: 1px solid #d9d9d9;
                border-bottom: 1px solid #d9d9d9;
                border-top-right-radius: 4px;
                background-color: #f5f5f5;
            }
            QSpinBox::down-button {
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 16px;
                border-left: 1px solid #d9d9d9;
                border-top: 1px solid #d9d9d9;
                border-bottom-right-radius: 4px;
                background-color: #f5f5f5;
            }
            QSpinBox::up-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-bottom: 4px solid #666;
                width: 0px;
                height: 0px;
            }
            QSpinBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid #666;
                width: 0px;
                height: 0px;
            }
        """)

        duration_unit_label = QLabel("毫秒之间随机")
        duration_unit_label.setStyleSheet("font-size: 12px; color: #666;")

        duration_layout.addWidget(duration_label)
        duration_layout.addWidget(self.scroll_duration_min)
        duration_layout.addWidget(dash_label2)
        duration_layout.addWidget(self.scroll_duration_max)
        duration_layout.addWidget(duration_unit_label)
        duration_layout.addStretch()

        parent_layout.addWidget(duration_group)

        # 说明输入框
        desc_group = QWidget()
        desc_layout = QHBoxLayout(desc_group)
        desc_layout.setContentsMargins(0, 0, 0, 0)

        desc_label = QLabel("说明")
        desc_label.setFixedWidth(80)
        desc_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 500;")

        self.scroll_description = QLineEdit()
        self.scroll_description.setPlaceholderText("选填")
        self.scroll_description.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 12px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #40a9ff;
                outline: none;
            }
        """)

        desc_layout.addWidget(desc_label)
        desc_layout.addWidget(self.scroll_description)

        parent_layout.addWidget(desc_group)

    def on_scroll_type_changed(self, button):
        """滚动页面类型切换"""
        try:
            if button == self.scroll_page_btn:
                self.scroll_selector_widget.setVisible(False)
            else:  # 选择器
                self.scroll_selector_widget.setVisible(True)
        except Exception as e:
            print(f"滚动页面类型切换错误: {e}")
            import traceback
            traceback.print_exc()

    def show_scroll_selector_variables(self):
        """显示滚动选择器变量下拉框"""
        try:
            self.show_simple_variable_menu(self.scroll_selector_input)
        except Exception as e:
            print(f"显示滚动选择器变量错误: {e}")

    def show_scroll_order_variables(self):
        """显示滚动元素顺序变量下拉框"""
        try:
            self.show_simple_variable_menu(self.scroll_order_value)
        except Exception as e:
            print(f"显示滚动元素顺序变量错误: {e}")

    def on_upload_type_changed(self, button):
        """上传附件类型切换"""
        try:
            if button == self.upload_local_btn:
                self.upload_local_widget.setVisible(True)
                self.upload_url_widget.setVisible(False)
            elif button == self.upload_url_btn:
                self.upload_local_widget.setVisible(False)
                self.upload_url_widget.setVisible(True)
            else:  # 文件夹文件随机
                self.upload_local_widget.setVisible(True)
                self.upload_url_widget.setVisible(False)
        except Exception as e:
            print(f"上传附件类型切换错误: {e}")
            import traceback
            traceback.print_exc()

    def browse_upload_file(self):
        """浏览选择上传文件"""
        try:
            from PyQt5.QtWidgets import QFileDialog
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "选择要上传的文件",
                "",
                "所有文件 (*.*)"
            )
            if file_path:
                self.upload_local_path.setText(file_path)
        except Exception as e:
            print(f"浏览上传文件错误: {e}")

    def show_upload_selector_variables(self):
        """显示上传选择器变量下拉框"""
        try:
            self.show_simple_variable_menu(self.upload_selector_input)
        except Exception as e:
            print(f"显示上传选择器变量错误: {e}")

    def show_upload_order_variables(self):
        """显示上传元素顺序变量下拉框"""
        try:
            self.show_simple_variable_menu(self.upload_order_value)
        except Exception as e:
            print(f"显示上传元素顺序变量错误: {e}")

    def show_upload_local_variables(self):
        """显示上传本地路径变量下拉框"""
        try:
            self.show_simple_variable_menu(self.upload_local_path)
        except Exception as e:
            print(f"显示上传本地路径变量错误: {e}")

    def show_upload_url_variables(self):
        """显示上传URL变量下拉框"""
        try:
            self.show_simple_variable_menu(self.upload_url_path)
        except Exception as e:
            print(f"显示上传URL变量错误: {e}")

    def switch_upload_tab(self, tab_index):
        """切换上传附件的标签页"""
        try:
            if tab_index == 0:  # 元素选择器
                self.upload_selector_content.setVisible(True)
                self.upload_stored_content.setVisible(False)
            else:  # 储存的元素对象
                self.upload_selector_content.setVisible(False)
                self.upload_stored_content.setVisible(True)
        except Exception as e:
            print(f"切换上传标签页错误: {e}")
            import traceback
            traceback.print_exc()

    def show_simple_variable_menu(self, target_widget):
        """显示简单的变量选择菜单"""
        try:
            from PyQt5.QtWidgets import QMenu, QAction

            # 创建变量菜单
            menu = QMenu(self)

            # 添加常用变量
            variables = [
                "task_id", "task_name", "serial_number", "browser_name",
                "acc_id", "comment", "user_name", "password", "cookies",
                "current_url", "page_title", "clipboard_content"
            ]

            for var in variables:
                action = QAction(f"{{{var}}}", self)
                action.triggered.connect(lambda checked, v=var: self.insert_variable_to_widget(target_widget, v))
                menu.addAction(action)

            # 在按钮下方显示菜单
            menu.exec_(target_widget.mapToGlobal(target_widget.rect().bottomLeft()))

        except Exception as e:
            print(f"显示变量菜单错误: {e}")

    def insert_variable_to_widget(self, widget, variable):
        """将变量插入到指定控件"""
        try:
            if hasattr(widget, 'setText'):
                current_text = widget.text()
                widget.setText(current_text + f"{{{variable}}}")
            elif hasattr(widget, 'setPlainText'):
                current_text = widget.toPlainText()
                widget.setPlainText(current_text + f"{{{variable}}}")
        except Exception as e:
            print(f"插入变量错误: {e}")

    def create_default_exact_config(self, parent_layout):
        """默认配置界面"""
        info_group = QGroupBox("操作配置")
        info_layout = QVBoxLayout(info_group)

        info_text = QLabel(f"正在开发 {self.operation_name} 的配置界面...")
        info_text.setStyleSheet("color: #666666; font-size: 13px; padding: 10px;")
        info_layout.addWidget(info_text)

        parent_layout.addWidget(info_group)

    def accept(self):
        """收集配置数据并关闭对话框"""
        try:
            # 根据操作类型收集配置数据
            if self.operation_name == "上传附件":
                self.collect_upload_file_config()
            elif self.operation_name == "滚动页面":
                self.collect_scroll_page_config()
            elif self.operation_name == "切换标签":
                self.collect_switch_tab_config()
            elif self.operation_name == "访问网站":
                self.collect_goto_url_config()
            # 可以继续添加其他操作的配置收集...

            # 调用父类的accept方法
            super().accept()
        except Exception as e:
            print(f"收集配置数据错误: {e}")
            import traceback
            traceback.print_exc()
            super().accept()  # 即使出错也要关闭对话框

    def collect_upload_file_config(self):
        """收集上传附件配置数据"""
        try:
            # 选择器类型
            if hasattr(self, 'upload_selector_radio') and self.upload_selector_radio.isChecked():
                selector_type = "selector"
            elif hasattr(self, 'upload_xpath_radio') and self.upload_xpath_radio.isChecked():
                selector_type = "xpath"
            else:
                selector_type = "text"

            # 选择器内容
            selector = getattr(self, 'upload_selector_input', QLineEdit()).text()

            # 元素顺序
            element_order = getattr(self, 'upload_order_value', QLineEdit()).text()

            # 附件类型和路径
            if hasattr(self, 'upload_local_btn') and self.upload_local_btn.isChecked():
                attachment_type = "local_file"
                file_path = getattr(self, 'upload_local_path', QLineEdit()).text()
            elif hasattr(self, 'upload_url_btn') and self.upload_url_btn.isChecked():
                attachment_type = "network_url"
                file_path = getattr(self, 'upload_url_path', QLineEdit()).text()
            else:
                attachment_type = "folder_random"
                file_path = getattr(self, 'upload_local_path', QLineEdit()).text()

            # 超时等待
            timeout = getattr(self, 'upload_timeout', QSpinBox()).value()

            # 说明
            description = getattr(self, 'upload_description', QLineEdit()).text()

            self.config_data = {
                "operation": "上传附件",
                "selector_type": selector_type,
                "selector": selector,
                "element_order": element_order,
                "attachment_type": attachment_type,
                "file_path": file_path,
                "timeout": timeout,
                "description": description
            }
        except Exception as e:
            print(f"收集上传附件配置错误: {e}")
            self.config_data = {"operation": "上传附件"}

    def collect_scroll_page_config(self):
        """收集滚动页面配置数据"""
        try:
            # 类型 (页面/选择器)
            if hasattr(self, 'scroll_page_btn') and self.scroll_page_btn.isChecked():
                scroll_type = "page"
                selector = ""
                element_order = ""
            else:
                scroll_type = "selector"
                # 选择器类型
                if hasattr(self, 'scroll_selector_radio') and self.scroll_selector_radio.isChecked():
                    selector_type = "selector"
                elif hasattr(self, 'scroll_xpath_radio') and self.scroll_xpath_radio.isChecked():
                    selector_type = "xpath"
                else:
                    selector_type = "text"

                selector = getattr(self, 'scroll_selector_input', QLineEdit()).text()
                element_order = getattr(self, 'scroll_order_value', QLineEdit()).text()

            # 位置配置
            position_type = getattr(self, 'scroll_position_type', QComboBox()).currentText()
            position_value = getattr(self, 'scroll_position_value', QComboBox()).currentText()

            # 滚动类型
            scroll_behavior = getattr(self, 'scroll_type_combo', QComboBox()).currentText()

            # 滚动速度
            speed_min = getattr(self, 'scroll_speed_min', QSpinBox()).value()
            speed_max = getattr(self, 'scroll_speed_max', QSpinBox()).value()

            # 停留时长
            duration_min = getattr(self, 'scroll_duration_min', QSpinBox()).value()
            duration_max = getattr(self, 'scroll_duration_max', QSpinBox()).value()

            # 说明
            description = getattr(self, 'scroll_description', QLineEdit()).text()

            self.config_data = {
                "operation": "滚动页面",
                "scroll_type": scroll_type,
                "selector": selector,
                "element_order": element_order,
                "position_type": position_type,
                "position_value": position_value,
                "scroll_behavior": scroll_behavior,
                "speed_min": speed_min,
                "speed_max": speed_max,
                "duration_min": duration_min,
                "duration_max": duration_max,
                "description": description
            }
        except Exception as e:
            print(f"收集滚动页面配置错误: {e}")
            self.config_data = {"operation": "滚动页面"}

    def collect_switch_tab_config(self):
        """收集切换标签配置数据"""
        try:
            condition_type = getattr(self, 'switch_condition_type', QComboBox()).currentText()
            condition_operator = getattr(self, 'switch_condition_operator', QComboBox()).currentText()
            tab_info = getattr(self, 'switch_tab_info', QLineEdit()).text()
            description = getattr(self, 'switch_description', QLineEdit()).text()

            self.config_data = {
                "operation": "切换标签",
                "condition_type": condition_type,
                "condition_operator": condition_operator,
                "tab_info": tab_info,
                "description": description
            }
        except Exception as e:
            print(f"收集切换标签配置错误: {e}")
            self.config_data = {"operation": "切换标签"}

    def collect_goto_url_config(self):
        """收集访问网站配置数据"""
        try:
            url = getattr(self, 'goto_url', QLineEdit()).text()
            timeout = getattr(self, 'goto_timeout', QSpinBox()).value()

            self.config_data = {
                "operation": "访问网站",
                "url": url,
                "timeout": timeout
            }
        except Exception as e:
            print(f"收集访问网站配置错误: {e}")
            self.config_data = {"operation": "访问网站"}

    # ==================== 数据处理类配置方法 ====================

    def create_text_extract_exact_config(self, parent_layout):
        """文本中提取 - 完全按照AdsPower原版界面"""
        config_group = QGroupBox("文本中提取设置")
        config_layout = QFormLayout(config_group)

        # 源文本
        self.text_extract_source = QLineEdit()
        self.text_extract_source.setPlaceholderText("输入要提取的源文本或变量名")
        self.text_extract_source.setStyleSheet(self.get_input_style())
        config_layout.addRow("源文本:", self.text_extract_source)

        # 提取方式
        self.text_extract_method = QComboBox()
        self.text_extract_method.addItems(["正则表达式", "开始结束字符", "分割字符", "固定位置"])
        self.text_extract_method.setStyleSheet(self.get_input_style())
        config_layout.addRow("提取方式:", self.text_extract_method)

        # 提取规则
        self.text_extract_rule = QLineEdit()
        self.text_extract_rule.setPlaceholderText("输入提取规则")
        self.text_extract_rule.setStyleSheet(self.get_input_style())
        config_layout.addRow("提取规则:", self.text_extract_rule)

        # 保存至
        self.text_extract_save_var = QLineEdit()
        self.text_extract_save_var.setPlaceholderText("请输入保存结果的变量名")
        self.text_extract_save_var.setStyleSheet(self.get_input_style())
        config_layout.addRow("保存至:", self.text_extract_save_var)

        parent_layout.addWidget(config_group)

    def create_json_convert_exact_config(self, parent_layout):
        """转换Json对象 - 完全按照AdsPower原版界面"""
        config_group = QGroupBox("转换Json对象设置")
        config_layout = QFormLayout(config_group)

        # JSON字符串
        self.json_convert_source = QTextEdit()
        self.json_convert_source.setFixedHeight(100)
        self.json_convert_source.setPlaceholderText("输入JSON字符串或变量名")
        self.json_convert_source.setStyleSheet(self.get_input_style())
        config_layout.addRow("JSON字符串:", self.json_convert_source)

        # 转换类型
        self.json_convert_type = QComboBox()
        self.json_convert_type.addItems(["字符串转对象", "对象转字符串"])
        self.json_convert_type.setStyleSheet(self.get_input_style())
        config_layout.addRow("转换类型:", self.json_convert_type)

        # 保存至
        self.json_convert_save_var = QLineEdit()
        self.json_convert_save_var.setPlaceholderText("请输入保存结果的变量名")
        self.json_convert_save_var.setStyleSheet(self.get_input_style())
        config_layout.addRow("保存至:", self.json_convert_save_var)

        parent_layout.addWidget(config_group)

    def create_field_extract_exact_config(self, parent_layout):
        """字段提取 - 完全按照AdsPower原版界面"""
        config_group = QGroupBox("字段提取设置")
        config_layout = QFormLayout(config_group)

        # 源对象
        self.field_extract_source = QLineEdit()
        self.field_extract_source.setPlaceholderText("输入源对象变量名")
        self.field_extract_source.setStyleSheet(self.get_input_style())
        config_layout.addRow("源对象:", self.field_extract_source)

        # 字段路径
        self.field_extract_path = QLineEdit()
        self.field_extract_path.setPlaceholderText("输入字段路径，如：data.user.name")
        self.field_extract_path.setStyleSheet(self.get_input_style())
        config_layout.addRow("字段路径:", self.field_extract_path)

        # 保存至
        self.field_extract_save_var = QLineEdit()
        self.field_extract_save_var.setPlaceholderText("请输入保存结果的变量名")
        self.field_extract_save_var.setStyleSheet(self.get_input_style())
        config_layout.addRow("保存至:", self.field_extract_save_var)

        parent_layout.addWidget(config_group)

    def create_random_extract_exact_config(self, parent_layout):
        """随机提取 - 完全按照AdsPower原版界面"""
        config_group = QGroupBox("随机提取设置")
        config_layout = QFormLayout(config_group)

        # 数据源
        self.random_extract_source = QComboBox()
        self.random_extract_source.addItems(["数组变量", "文本行", "数字范围"])
        self.random_extract_source.setStyleSheet(self.get_input_style())
        config_layout.addRow("数据源:", self.random_extract_source)

        # 源数据
        self.random_extract_data = QLineEdit()
        self.random_extract_data.setPlaceholderText("输入源数据或变量名")
        self.random_extract_data.setStyleSheet(self.get_input_style())
        config_layout.addRow("源数据:", self.random_extract_data)

        # 提取数量
        self.random_extract_count = QSpinBox()
        self.random_extract_count.setRange(1, 100)
        self.random_extract_count.setValue(1)
        self.random_extract_count.setStyleSheet(self.get_input_style())
        config_layout.addRow("提取数量:", self.random_extract_count)

        # 保存至
        self.random_extract_save_var = QLineEdit()
        self.random_extract_save_var.setPlaceholderText("请输入保存结果的变量名")
        self.random_extract_save_var.setStyleSheet(self.get_input_style())
        config_layout.addRow("保存至:", self.random_extract_save_var)

        parent_layout.addWidget(config_group)

    # ==================== 环境信息类配置方法 ====================

    def create_update_env_note_exact_config(self, parent_layout):
        """更新环境备注 - 完全按照AdsPower原版界面"""
        config_group = QGroupBox("更新环境备注设置")
        config_layout = QFormLayout(config_group)

        # 备注内容
        self.env_note_content = QTextEdit()
        self.env_note_content.setFixedHeight(100)
        self.env_note_content.setPlaceholderText("输入要更新的备注内容")
        self.env_note_content.setStyleSheet(self.get_input_style())
        config_layout.addRow("备注内容:", self.env_note_content)

        # 更新方式
        self.env_note_mode = QComboBox()
        self.env_note_mode.addItems(["覆盖", "追加"])
        self.env_note_mode.setStyleSheet(self.get_input_style())
        config_layout.addRow("更新方式:", self.env_note_mode)

        # 环境ID（可选）
        self.env_note_env_id = QLineEdit()
        self.env_note_env_id.setPlaceholderText("留空则更新当前环境")
        self.env_note_env_id.setStyleSheet(self.get_input_style())
        config_layout.addRow("环境ID:", self.env_note_env_id)

        parent_layout.addWidget(config_group)

    def create_update_env_tag_exact_config(self, parent_layout):
        """更新环境标签 - 完全按照AdsPower原版界面"""
        config_group = QGroupBox("更新环境标签设置")
        config_layout = QFormLayout(config_group)

        # 标签内容
        self.env_tag_content = QLineEdit()
        self.env_tag_content.setPlaceholderText("输入要更新的标签，多个标签用逗号分隔")
        self.env_tag_content.setStyleSheet(self.get_input_style())
        config_layout.addRow("标签内容:", self.env_tag_content)

        # 更新方式
        self.env_tag_mode = QComboBox()
        self.env_tag_mode.addItems(["覆盖", "追加", "删除"])
        self.env_tag_mode.setStyleSheet(self.get_input_style())
        config_layout.addRow("更新方式:", self.env_tag_mode)

        # 环境ID（可选）
        self.env_tag_env_id = QLineEdit()
        self.env_tag_env_id.setPlaceholderText("留空则更新当前环境")
        self.env_tag_env_id.setStyleSheet(self.get_input_style())
        config_layout.addRow("环境ID:", self.env_tag_env_id)

        parent_layout.addWidget(config_group)

    # ==================== 流程管理类配置方法 ====================

    def create_start_new_browser_exact_config(self, parent_layout):
        """启动新浏览器 - 完全按照AdsPower原版界面"""
        config_group = QGroupBox("启动新浏览器设置")
        config_layout = QFormLayout(config_group)

        # 环境选择方式
        self.browser_select_mode = QComboBox()
        self.browser_select_mode.addItems(["指定环境ID", "随机选择", "按条件筛选"])
        self.browser_select_mode.setStyleSheet(self.get_input_style())
        config_layout.addRow("选择方式:", self.browser_select_mode)

        # 环境ID
        self.browser_env_id = QLineEdit()
        self.browser_env_id.setPlaceholderText("输入环境ID")
        self.browser_env_id.setStyleSheet(self.get_input_style())
        config_layout.addRow("环境ID:", self.browser_env_id)

        # 保存环境ID到变量
        self.browser_save_env_id = QLineEdit()
        self.browser_save_env_id.setPlaceholderText("保存环境ID的变量名")
        self.browser_save_env_id.setStyleSheet(self.get_input_style())
        config_layout.addRow("保存环境ID至:", self.browser_save_env_id)

        parent_layout.addWidget(config_group)

    def create_use_other_flow_exact_config(self, parent_layout):
        """使用其他流程 - 完全按照AdsPower原版界面"""
        config_group = QGroupBox("使用其他流程设置")
        config_layout = QFormLayout(config_group)

        # 流程文件
        file_widget = QWidget()
        file_layout = QHBoxLayout(file_widget)
        file_layout.setContentsMargins(0, 0, 0, 0)

        self.other_flow_path = QLineEdit()
        self.other_flow_path.setPlaceholderText("选择要执行的流程文件")
        self.other_flow_path.setStyleSheet(self.get_input_style())
        file_layout.addWidget(self.other_flow_path)

        browse_btn = QPushButton("浏览")
        browse_btn.setStyleSheet(self.get_button_style())
        browse_btn.clicked.connect(self.browse_flow_file)
        file_layout.addWidget(browse_btn)

        config_layout.addRow("流程文件:", file_widget)

        # 执行方式
        self.other_flow_mode = QComboBox()
        self.other_flow_mode.addItems(["同步执行", "异步执行"])
        self.other_flow_mode.setStyleSheet(self.get_input_style())
        config_layout.addRow("执行方式:", self.other_flow_mode)

        parent_layout.addWidget(config_group)

    def create_if_condition_exact_config(self, parent_layout):
        """IF条件 - 完全按照AdsPower原版界面"""
        config_group = QGroupBox("IF条件设置")
        config_layout = QFormLayout(config_group)

        # 条件类型
        self.if_condition_type = QComboBox()
        self.if_condition_type.addItems(["变量比较", "元素存在", "文本包含", "数值比较"])
        self.if_condition_type.setStyleSheet(self.get_input_style())
        config_layout.addRow("条件类型:", self.if_condition_type)

        # 左值
        self.if_left_value = QLineEdit()
        self.if_left_value.setPlaceholderText("输入左值或变量名")
        self.if_left_value.setStyleSheet(self.get_input_style())
        config_layout.addRow("左值:", self.if_left_value)

        # 比较操作符
        self.if_operator = QComboBox()
        self.if_operator.addItems(["等于", "不等于", "大于", "小于", "包含", "不包含"])
        self.if_operator.setStyleSheet(self.get_input_style())
        config_layout.addRow("操作符:", self.if_operator)

        # 右值
        self.if_right_value = QLineEdit()
        self.if_right_value.setPlaceholderText("输入右值或变量名")
        self.if_right_value.setStyleSheet(self.get_input_style())
        config_layout.addRow("右值:", self.if_right_value)

        parent_layout.addWidget(config_group)

    def create_for_element_exact_config(self, parent_layout):
        """For循环元素 - 完全按照AdsPower原版界面"""
        config_group = QGroupBox("For循环元素设置")
        config_layout = QFormLayout(config_group)

        # 元素选择器
        self.for_element_selector = QLineEdit()
        self.for_element_selector.setPlaceholderText("输入元素选择器")
        self.for_element_selector.setStyleSheet(self.get_input_style())
        config_layout.addRow("元素选择器:", self.for_element_selector)

        # 循环变量名
        self.for_element_var = QLineEdit()
        self.for_element_var.setPlaceholderText("element_item")
        self.for_element_var.setStyleSheet(self.get_input_style())
        config_layout.addRow("循环变量名:", self.for_element_var)

        # 索引变量名
        self.for_element_index_var = QLineEdit()
        self.for_element_index_var.setPlaceholderText("element_index")
        self.for_element_index_var.setStyleSheet(self.get_input_style())
        config_layout.addRow("索引变量名:", self.for_element_index_var)

        parent_layout.addWidget(config_group)

    def create_for_count_exact_config(self, parent_layout):
        """For循环次数 - 完全按照AdsPower原版界面"""
        config_group = QGroupBox("For循环次数设置")
        config_layout = QFormLayout(config_group)

        # 循环次数
        self.for_count_times = QSpinBox()
        self.for_count_times.setRange(1, 10000)
        self.for_count_times.setValue(10)
        self.for_count_times.setStyleSheet(self.get_input_style())
        config_layout.addRow("循环次数:", self.for_count_times)

        # 索引变量名
        self.for_count_index_var = QLineEdit()
        self.for_count_index_var.setPlaceholderText("loop_index")
        self.for_count_index_var.setStyleSheet(self.get_input_style())
        config_layout.addRow("索引变量名:", self.for_count_index_var)

        parent_layout.addWidget(config_group)

    def create_for_data_exact_config(self, parent_layout):
        """For循环数据 - 完全按照AdsPower原版界面"""
        config_group = QGroupBox("For循环数据设置")
        config_layout = QFormLayout(config_group)

        # 数据源
        self.for_data_source = QComboBox()
        self.for_data_source.addItems(["数组变量", "文本行", "Excel数据", "CSV数据"])
        self.for_data_source.setStyleSheet(self.get_input_style())
        config_layout.addRow("数据源:", self.for_data_source)

        # 数据变量
        self.for_data_var = QLineEdit()
        self.for_data_var.setPlaceholderText("输入数据变量名")
        self.for_data_var.setStyleSheet(self.get_input_style())
        config_layout.addRow("数据变量:", self.for_data_var)

        # 循环变量名
        self.for_data_item_var = QLineEdit()
        self.for_data_item_var.setPlaceholderText("data_item")
        self.for_data_item_var.setStyleSheet(self.get_input_style())
        config_layout.addRow("循环变量名:", self.for_data_item_var)

        # 索引变量名
        self.for_data_index_var = QLineEdit()
        self.for_data_index_var.setPlaceholderText("data_index")
        self.for_data_index_var.setStyleSheet(self.get_input_style())
        config_layout.addRow("索引变量名:", self.for_data_index_var)

        parent_layout.addWidget(config_group)

    def create_while_loop_exact_config(self, parent_layout):
        """While循环 - 完全按照AdsPower原版界面"""
        config_group = QGroupBox("While循环设置")
        config_layout = QFormLayout(config_group)

        # 条件表达式
        self.while_condition = QLineEdit()
        self.while_condition.setPlaceholderText("输入循环条件表达式")
        self.while_condition.setStyleSheet(self.get_input_style())
        config_layout.addRow("循环条件:", self.while_condition)

        # 最大循环次数
        self.while_max_count = QSpinBox()
        self.while_max_count.setRange(1, 10000)
        self.while_max_count.setValue(100)
        self.while_max_count.setStyleSheet(self.get_input_style())
        config_layout.addRow("最大循环次数:", self.while_max_count)

        parent_layout.addWidget(config_group)

    def create_exit_loop_exact_config(self, parent_layout):
        """退出循环 - 完全按照AdsPower原版界面"""
        config_group = QGroupBox("退出循环设置")
        config_layout = QFormLayout(config_group)

        # 退出类型
        self.exit_loop_type = QComboBox()
        self.exit_loop_type.addItems(["退出当前循环", "退出所有循环", "跳过当前迭代"])
        self.exit_loop_type.setStyleSheet(self.get_input_style())
        config_layout.addRow("退出类型:", self.exit_loop_type)

        # 说明文本
        info_label = QLabel("退出当前循环：跳出最近的一层循环\n退出所有循环：跳出所有嵌套循环\n跳过当前迭代：跳过本次循环，继续下次迭代")
        info_label.setStyleSheet("color: #666666; font-size: 12px; margin-top: 10px;")
        config_layout.addRow("", info_label)

        parent_layout.addWidget(config_group)

    def create_close_browser_exact_config(self, parent_layout):
        """关闭浏览器 - 完全按照AdsPower原版界面"""
        config_group = QGroupBox("关闭浏览器设置")
        config_layout = QFormLayout(config_group)

        # 关闭方式
        self.close_browser_mode = QComboBox()
        self.close_browser_mode.addItems(["关闭当前浏览器", "关闭指定浏览器", "关闭所有浏览器"])
        self.close_browser_mode.setStyleSheet(self.get_input_style())
        config_layout.addRow("关闭方式:", self.close_browser_mode)

        # 环境ID（当选择指定浏览器时）
        self.close_browser_env_id = QLineEdit()
        self.close_browser_env_id.setPlaceholderText("输入要关闭的环境ID")
        self.close_browser_env_id.setStyleSheet(self.get_input_style())
        self.close_browser_env_id.setEnabled(False)
        config_layout.addRow("环境ID:", self.close_browser_env_id)

        # 连接信号
        def on_mode_changed(text):
            self.close_browser_env_id.setEnabled(text == "关闭指定浏览器")

        self.close_browser_mode.currentTextChanged.connect(on_mode_changed)

        parent_layout.addWidget(config_group)

    # ==================== 剩余获取数据功能配置方法 ====================

    def create_download_file_exact_config(self, parent_layout):
        """下载文件 - 完全按照AdsPower原版界面"""
        config_group = QGroupBox("下载文件设置")
        config_layout = QFormLayout(config_group)

        # 下载URL
        self.download_url = QLineEdit()
        self.download_url.setPlaceholderText("输入要下载的文件URL")
        self.download_url.setStyleSheet(self.get_input_style())
        config_layout.addRow("下载URL:", self.download_url)

        # 保存路径
        file_widget = QWidget()
        file_layout = QHBoxLayout(file_widget)
        file_layout.setContentsMargins(0, 0, 0, 0)

        self.download_save_path = QLineEdit()
        self.download_save_path.setPlaceholderText("选择文件保存路径")
        self.download_save_path.setStyleSheet(self.get_input_style())
        file_layout.addWidget(self.download_save_path)

        browse_btn = QPushButton("浏览")
        browse_btn.setStyleSheet(self.get_button_style())
        file_layout.addWidget(browse_btn)

        config_layout.addRow("保存路径:", file_widget)

        # 超时时间
        self.download_timeout = QSpinBox()
        self.download_timeout.setRange(10, 300)
        self.download_timeout.setValue(60)
        self.download_timeout.setSuffix(" 秒")
        self.download_timeout.setStyleSheet(self.get_input_style())
        config_layout.addRow("超时时间:", self.download_timeout)

        parent_layout.addWidget(config_group)

    def create_import_excel_exact_config(self, parent_layout):
        """导入Excel素材 - 完全按照AdsPower原版界面"""
        config_group = QGroupBox("导入Excel素材设置")
        config_layout = QFormLayout(config_group)

        # Excel文件路径
        file_widget = QWidget()
        file_layout = QHBoxLayout(file_widget)
        file_layout.setContentsMargins(0, 0, 0, 0)

        self.import_excel_path = QLineEdit()
        self.import_excel_path.setPlaceholderText("选择要导入的Excel文件")
        self.import_excel_path.setStyleSheet(self.get_input_style())
        file_layout.addWidget(self.import_excel_path)

        browse_btn = QPushButton("浏览")
        browse_btn.setStyleSheet(self.get_button_style())
        file_layout.addWidget(browse_btn)

        config_layout.addRow("Excel文件:", file_widget)

        # 工作表名
        self.import_excel_sheet = QLineEdit()
        self.import_excel_sheet.setPlaceholderText("工作表名，留空则使用第一个工作表")
        self.import_excel_sheet.setStyleSheet(self.get_input_style())
        config_layout.addRow("工作表名:", self.import_excel_sheet)

        # 起始行
        self.import_excel_start_row = QSpinBox()
        self.import_excel_start_row.setRange(1, 1000000)
        self.import_excel_start_row.setValue(1)
        self.import_excel_start_row.setStyleSheet(self.get_input_style())
        config_layout.addRow("起始行:", self.import_excel_start_row)

        # 保存至变量
        self.import_excel_save_var = QLineEdit()
        self.import_excel_save_var.setPlaceholderText("请输入保存数据的变量名")
        self.import_excel_save_var.setStyleSheet(self.get_input_style())
        config_layout.addRow("保存至:", self.import_excel_save_var)

        parent_layout.addWidget(config_group)

    def create_auth_password_exact_config(self, parent_layout):
        """身份验证密码 - 完全按照AdsPower原版界面"""
        config_group = QGroupBox("身份验证密码设置")
        config_layout = QFormLayout(config_group)

        # 密钥
        self.auth_secret_key = QLineEdit()
        self.auth_secret_key.setPlaceholderText("输入身份验证器密钥")
        self.auth_secret_key.setStyleSheet(self.get_input_style())
        config_layout.addRow("密钥:", self.auth_secret_key)

        # 保存至变量
        self.auth_save_var = QLineEdit()
        self.auth_save_var.setPlaceholderText("请输入保存验证码的变量名")
        self.auth_save_var.setStyleSheet(self.get_input_style())
        config_layout.addRow("保存至:", self.auth_save_var)

        # 说明文本
        info_label = QLabel("生成基于时间的一次性密码(TOTP)，用于双因素身份验证")
        info_label.setStyleSheet("color: #666666; font-size: 12px; margin-top: 10px;")
        config_layout.addRow("", info_label)

        parent_layout.addWidget(config_group)

    # ==================== 辅助方法 ====================

    def browse_flow_file(self):
        """浏览流程文件"""
        from PyQt5.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择流程文件", "", "JSON文件 (*.json);;所有文件 (*)"
        )
        if file_path:
            self.other_flow_path.setText(file_path)

def main():
    """测试函数"""
    app = QApplication(sys.argv)

    # 测试不同的操作配置
    operations = ["新建标签", "关闭标签", "访问网站", "点击元素", "输入内容"]

    for operation in operations:
        dialog = AdsPowerRPAConfigDialog(operation)
        if dialog.exec_() == QDialog.Accepted:
            print(f"配置了操作: {operation}")
        break  # 只测试第一个

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
