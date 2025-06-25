#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RPA操作参数配置对话框
根据AdsPower官方文档实现各种操作的参数配置界面
"""

import sys
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QLineEdit, QComboBox, QWidget, QScrollArea,
                             QTextEdit, QSpinBox, QCheckBox, QGroupBox, QFormLayout,
                             QApplication, QMessageBox, QTabWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class RPAOperationConfigDialog(QDialog):
    """RPA操作参数配置对话框"""
    
    def __init__(self, operation_name, parent=None):
        super().__init__(parent)
        self.operation_name = operation_name
        self.config_data = {}
        self.init_ui()
        
    def init_ui(self):
        """初始化界面 - 使用更好的UI设计"""
        self.setWindowTitle(self.operation_name)  # 窗口标题就是操作名称
        self.setFixedSize(700, 600)  # 增大窗口尺寸
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
                border: 1px solid #e1e4e8;
                border-radius: 8px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)  # 增加边距
        layout.setSpacing(0)

        # 配置内容区域 - 直接显示，不需要额外的标题区域
        self.create_config_interface(layout)

        # 底部按钮区域
        self.create_buttons(layout)
        
    def create_config_interface(self, parent_layout):
        """创建配置内容区域 - 添加滚动功能以支持更多内容"""
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #f5f5f5;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #c1c1c1;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #a8a8a8;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)

        # 创建滚动内容容器
        config_widget = QWidget()
        config_layout = QVBoxLayout(config_widget)
        config_layout.setContentsMargins(0, 0, 0, 0)
        config_layout.setSpacing(0)

        # 根据操作名称创建不同的配置界面 - 完整支持所有50个AdsPower RPA功能

        # 页面操作 (10个功能)
        if self.operation_name == "新建标签":
            self.create_new_tab_config(config_layout)
        elif self.operation_name == "关闭标签":
            self.create_close_tab_config(config_layout)
        elif self.operation_name == "关闭其他标签":
            self.create_close_other_tabs_config(config_layout)
        elif self.operation_name == "切换标签":
            self.create_switch_tab_config(config_layout)
        elif self.operation_name == "访问网站":
            self.create_goto_url_config(config_layout)
        elif self.operation_name == "刷新页面":
            self.create_page_navigation_config(config_layout)
        elif self.operation_name == "页面后退":
            self.create_page_navigation_config(config_layout)
        elif self.operation_name == "页面截图":
            self.create_page_screenshot_config(config_layout)
        elif self.operation_name == "经过元素":
            self.create_hover_element_config(config_layout)
        elif self.operation_name == "下拉选择器":
            self.create_dropdown_selector_config(config_layout)

        # 元素操作 (10个功能)
        elif self.operation_name == "元素聚焦":
            self.create_focus_element_config(config_layout)
        elif self.operation_name == "点击元素":
            self.create_click_element_config(config_layout)
        elif self.operation_name == "输入内容":
            self.create_input_content_config(config_layout)
        elif self.operation_name == "上传附件":
            self.create_upload_file_config(config_layout)
        elif self.operation_name == "执行JS脚本":
            self.create_execute_js_config(config_layout)
        elif self.operation_name == "键盘按键":
            self.create_keyboard_key_config(config_layout)
        elif self.operation_name == "组合键":
            self.create_keyboard_combo_config(config_layout)
        elif self.operation_name == "等待时间":
            self.create_wait_time_config(config_layout)
        elif self.operation_name == "等待元素出现":
            self.create_wait_element_config(config_layout)
        elif self.operation_name == "等待请求完成":
            self.create_wait_request_config(config_layout)

        # 数据获取 (10个功能)
        elif self.operation_name == "获取URL":
            self.create_get_url_config(config_layout)
        elif self.operation_name == "获取粘贴板内容":
            self.create_get_clipboard_config(config_layout)
        elif self.operation_name == "元素数据":
            self.create_get_element_data_config(config_layout)
        elif self.operation_name == "当前焦点元素":
            self.create_get_focused_element_config(config_layout)
        elif self.operation_name == "存到文件":
            self.create_save_to_file_config(config_layout)
        elif self.operation_name == "存到Excel":
            self.create_save_to_excel_config(config_layout)
        elif self.operation_name == "导入txt":
            self.create_import_txt_config(config_layout)
        elif self.operation_name == "获取邮件":
            self.create_get_email_config(config_layout)
        elif self.operation_name == "身份验证器码":
            self.create_get_totp_config(config_layout)

        # 网络监听 (5个功能)
        elif self.operation_name == "监听请求触发":
            self.create_listen_request_trigger_config(config_layout)
        elif self.operation_name == "监听请求结果":
            self.create_listen_request_result_config(config_layout)
        elif self.operation_name == "停止页面监听":
            self.create_stop_page_listening_config(config_layout)
        elif self.operation_name == "获取页面Cookie":
            self.create_get_page_cookies_config(config_layout)
        elif self.operation_name == "清除页面Cookie":
            self.create_clear_page_cookies_config(config_layout)

        # 数据处理 (5个功能)
        elif self.operation_name == "文本中提取":
            self.create_text_extract_config(config_layout)
        elif self.operation_name == "转换Json对象":
            self.create_json_convert_config(config_layout)
        elif self.operation_name == "字段提取":
            self.create_field_extract_config(config_layout)
        elif self.operation_name == "随机提取":
            self.create_random_extract_config(config_layout)
        elif self.operation_name == "更新环境备注":
            self.create_update_env_note_config(config_layout)

        # 流程控制 (7个功能)
        elif self.operation_name == "更新环境标签":
            self.create_update_env_tag_config(config_layout)
        elif self.operation_name == "启动新浏览器":
            self.create_start_new_browser_config(config_layout)
        elif self.operation_name == "使用其他流程":
            self.create_use_other_flow_config(config_layout)
        elif self.operation_name == "IF条件":
            self.create_if_condition_config(config_layout)
        elif self.operation_name == "For循环元素":
            self.create_for_loop_elements_config(config_layout)
        elif self.operation_name == "For循环次数":
            self.create_for_loop_count_config(config_layout)
        elif self.operation_name == "For循环数据":
            self.create_for_loop_data_config(config_layout)

        # 循环控制 (3个功能)
        elif self.operation_name == "While循环":
            self.create_while_loop_config(config_layout)
        elif self.operation_name == "退出循环":
            self.create_exit_loop_config(config_layout)
        elif self.operation_name == "关闭浏览器":
            self.create_close_browser_config(config_layout)

        # 兼容旧版本操作名称和AdsPower原始操作名称
        elif self.operation_name in ["新建标签页"]:
            self.create_new_tab_config(config_layout)
        elif self.operation_name in ["前往网址"]:
            self.create_goto_url_config(config_layout)
        elif self.operation_name in ["点击", "点击元素"]:
            self.create_click_config(config_layout)
        elif self.operation_name in ["悬停", "经过元素"]:
            self.create_hover_config(config_layout)
        elif self.operation_name in ["输入内容", "inputContent"]:  # 修复inputContent映射
            self.create_input_config(config_layout)
        elif self.operation_name in ["元素聚焦"]:
            self.create_focus_config(config_layout)
        elif self.operation_name in ["关闭标签页"]:
            self.create_close_tab_config(config_layout)
        elif self.operation_name in ["切换标签页"]:
            self.create_switch_tab_config(config_layout)
        elif self.operation_name in ["键盘按键", "组合键", "keyboard"]:  # 修复keyboard映射
            self.create_keyboard_config(config_layout)
        elif self.operation_name in ["等待元素"]:
            self.create_wait_element_config(config_layout)
        elif self.operation_name in ["等待页面"]:
            self.create_wait_page_config(config_layout)
        elif self.operation_name in ["等待弹窗"]:
            self.create_wait_popup_config(config_layout)
        elif self.operation_name in ["获取元素"]:
            self.create_get_element_config(config_layout)
        elif self.operation_name in ["获取页面"]:
            self.create_get_page_config(config_layout)
        elif self.operation_name in ["获取弹窗"]:
            self.create_get_popup_config(config_layout)
        elif self.operation_name in ["获取Cookie"]:
            self.create_get_cookie_config(config_layout)
        elif self.operation_name in ["获取环境信息"]:
            self.create_get_env_config(config_layout)
        elif self.operation_name in ["导入txt素材"]:
            self.create_import_txt_config(config_layout)
        else:
            self.create_default_config(config_layout)

        # 添加弹性空间，确保内容顶部对齐
        config_layout.addStretch()

        # 设置滚动区域的内容
        scroll_area.setWidget(config_widget)
        parent_layout.addWidget(scroll_area)

    # ==================== 简化的配置方法 ====================

    def create_exit_loop_config(self, parent_layout):
        """创建退出循环配置 - 无参数，直接执行"""
        info_label = QLabel("退出循环操作无需配置参数，将直接跳出当前循环")
        info_label.setStyleSheet("color: #666; font-size: 13px; padding: 20px;")
        parent_layout.addWidget(info_label)

    def create_close_browser_config(self, parent_layout):
        """创建关闭浏览器配置 - 无参数，直接执行"""
        info_label = QLabel("关闭浏览器操作无需配置参数，将直接关闭当前浏览器")
        info_label.setStyleSheet("color: #666; font-size: 13px; padding: 20px;")
        parent_layout.addWidget(info_label)

    def create_execute_js_config(self, parent_layout):
        """创建执行JS脚本配置"""
        js_group = QGroupBox("JavaScript设置")
        js_layout = QFormLayout(js_group)

        # JS代码输入
        self.js_code = QTextEdit()
        self.js_code.setFixedHeight(120)
        self.js_code.setPlaceholderText("请输入JavaScript代码")
        self.js_code.setStyleSheet(self.get_input_style())
        js_layout.addRow("JavaScript代码:", self.js_code)

        # 注入变量
        self.js_inject_vars = QLineEdit()
        self.js_inject_vars.setPlaceholderText("请选择要注入的变量")
        self.js_inject_vars.setStyleSheet(self.get_input_style())
        js_layout.addRow("注入变量:", self.js_inject_vars)

        # 返回值保存
        self.js_return_var = QLineEdit()
        self.js_return_var.setPlaceholderText("请输入保存返回值的变量名")
        self.js_return_var.setStyleSheet(self.get_input_style())
        js_layout.addRow("返回值保存至:", self.js_return_var)

        # 说明
        self.js_description = QLineEdit()
        self.js_description.setPlaceholderText("选填")
        self.js_description.setStyleSheet(self.get_input_style())
        js_layout.addRow("说明:", self.js_description)

        parent_layout.addWidget(js_group)

    def create_get_url_config(self, parent_layout):
        """创建获取URL配置"""
        url_group = QGroupBox("获取URL设置")
        url_layout = QFormLayout(url_group)

        # 保存变量
        self.get_url_save_var = QLineEdit()
        self.get_url_save_var.setPlaceholderText("请输入保存URL的变量名")
        self.get_url_save_var.setStyleSheet(self.get_input_style())
        url_layout.addRow("保存至变量:", self.get_url_save_var)

        # 说明
        self.get_url_description = QLineEdit()
        self.get_url_description.setPlaceholderText("选填")
        self.get_url_description.setStyleSheet(self.get_input_style())
        url_layout.addRow("说明:", self.get_url_description)

        parent_layout.addWidget(url_group)

    def create_get_clipboard_config(self, parent_layout):
        """创建获取粘贴板内容配置"""
        clipboard_group = QGroupBox("获取粘贴板设置")
        clipboard_layout = QFormLayout(clipboard_group)

        # 保存变量
        self.clipboard_save_var = QLineEdit()
        self.clipboard_save_var.setPlaceholderText("请输入保存内容的变量名")
        self.clipboard_save_var.setStyleSheet(self.get_input_style())
        clipboard_layout.addRow("保存至变量:", self.clipboard_save_var)

        # 说明
        self.clipboard_description = QLineEdit()
        self.clipboard_description.setPlaceholderText("选填")
        self.clipboard_description.setStyleSheet(self.get_input_style())
        clipboard_layout.addRow("说明:", self.clipboard_description)

        parent_layout.addWidget(clipboard_group)

    def create_get_element_data_config(self, parent_layout):
        """创建获取元素数据配置"""
        element_group = QGroupBox("元素数据设置")
        element_layout = QFormLayout(element_group)

        # 选择器类型
        self.element_data_selector_type = QComboBox()
        self.element_data_selector_type.addItems(["Selector", "XPath", "文本"])
        self.element_data_selector_type.setStyleSheet(self.get_input_style())
        element_layout.addRow("选择器类型:", self.element_data_selector_type)

        # 元素选择器
        self.element_data_selector = QLineEdit()
        self.element_data_selector.setPlaceholderText("请输入元素选择器")
        self.element_data_selector.setStyleSheet(self.get_input_style())
        element_layout.addRow("元素选择器:", self.element_data_selector)

        # 提取类型
        self.element_data_extract_type = QComboBox()
        self.element_data_extract_type.addItems(["文本", "属性", "HTML", "值"])
        self.element_data_extract_type.setStyleSheet(self.get_input_style())
        element_layout.addRow("提取类型:", self.element_data_extract_type)

        # 保存变量
        self.element_data_save_var = QLineEdit()
        self.element_data_save_var.setPlaceholderText("请输入保存数据的变量名")
        self.element_data_save_var.setStyleSheet(self.get_input_style())
        element_layout.addRow("保存至变量:", self.element_data_save_var)

        # 元素顺序
        self.element_data_order = QSpinBox()
        self.element_data_order.setMinimum(1)
        self.element_data_order.setValue(1)
        self.element_data_order.setStyleSheet(self.get_input_style())
        element_layout.addRow("元素顺序:", self.element_data_order)

        # 说明
        self.element_data_description = QLineEdit()
        self.element_data_description.setPlaceholderText("选填")
        self.element_data_description.setStyleSheet(self.get_input_style())
        element_layout.addRow("说明:", self.element_data_description)

        parent_layout.addWidget(element_group)

    # ==================== 其他缺失的配置方法 ====================

    def create_close_tab_config(self, parent_layout):
        """创建关闭标签配置"""
        close_group = QGroupBox("关闭标签设置")
        close_layout = QFormLayout(close_group)

        # 关闭类型
        self.close_tab_type = QComboBox()
        self.close_tab_type.addItems(["当前标签", "指定标签"])
        self.close_tab_type.setStyleSheet(self.get_input_style())
        close_layout.addRow("关闭类型:", self.close_tab_type)

        # 标签索引（当选择指定标签时）
        self.close_tab_index = QSpinBox()
        self.close_tab_index.setMinimum(1)
        self.close_tab_index.setValue(1)
        self.close_tab_index.setStyleSheet(self.get_input_style())
        close_layout.addRow("标签索引:", self.close_tab_index)

        parent_layout.addWidget(close_group)

    def create_close_other_tabs_config(self, parent_layout):
        """创建关闭其他标签配置 - 无参数"""
        info_label = QLabel("关闭除当前标签外的所有其他标签页")
        info_label.setStyleSheet("color: #666; font-size: 13px; padding: 20px;")
        parent_layout.addWidget(info_label)

    def create_switch_tab_config(self, parent_layout):
        """创建切换标签配置"""
        switch_group = QGroupBox("切换标签设置")
        switch_layout = QFormLayout(switch_group)

        # 切换方式
        self.switch_tab_type = QComboBox()
        self.switch_tab_type.addItems(["按序号", "按标题", "按URL"])
        self.switch_tab_type.setStyleSheet(self.get_input_style())
        switch_layout.addRow("切换方式:", self.switch_tab_type)

        # 目标值
        self.switch_tab_target = QLineEdit()
        self.switch_tab_target.setPlaceholderText("请输入序号、标题或URL")
        self.switch_tab_target.setStyleSheet(self.get_input_style())
        switch_layout.addRow("目标值:", self.switch_tab_target)

        parent_layout.addWidget(switch_group)

    def create_page_navigation_config(self, parent_layout):
        """创建页面导航配置（刷新、后退等）"""
        nav_group = QGroupBox("页面导航设置")
        nav_layout = QFormLayout(nav_group)

        # 等待加载完成
        self.nav_wait_load = QCheckBox("等待页面加载完成")
        self.nav_wait_load.setChecked(True)
        nav_layout.addRow("", self.nav_wait_load)

        parent_layout.addWidget(nav_group)

    def create_page_screenshot_config(self, parent_layout):
        """创建页面截图配置"""
        screenshot_group = QGroupBox("页面截图设置")
        screenshot_layout = QFormLayout(screenshot_group)

        # 截图名称
        self.screenshot_name = QLineEdit()
        self.screenshot_name.setPlaceholderText("请输入截图文件名")
        self.screenshot_name.setStyleSheet(self.get_input_style())
        screenshot_layout.addRow("截图名称:", self.screenshot_name)

        # 截图类型
        self.screenshot_type = QComboBox()
        self.screenshot_type.addItems(["当前可见区域", "整个页面"])
        self.screenshot_type.setStyleSheet(self.get_input_style())
        screenshot_layout.addRow("截图类型:", self.screenshot_type)

        # 图片格式
        self.screenshot_format = QComboBox()
        self.screenshot_format.addItems(["PNG", "JPEG"])
        self.screenshot_format.setStyleSheet(self.get_input_style())
        screenshot_layout.addRow("图片格式:", self.screenshot_format)

        parent_layout.addWidget(screenshot_group)

    def create_keyboard_key_config(self, parent_layout):
        """创建键盘按键配置"""
        key_group = QGroupBox("键盘按键设置")
        key_layout = QFormLayout(key_group)

        # 按键类型
        self.keyboard_key_type = QComboBox()
        self.keyboard_key_type.addItems([
            "退格键", "Tab键", "回车键", "空格键", "Esc键", "删除键",
            "方向上键", "方向下键", "方向左键", "方向右键"
        ])
        self.keyboard_key_type.setStyleSheet(self.get_input_style())
        key_layout.addRow("按键类型:", self.keyboard_key_type)

        # 按键延迟
        self.keyboard_key_delay = QSpinBox()
        self.keyboard_key_delay.setMinimum(0)
        self.keyboard_key_delay.setMaximum(5000)
        self.keyboard_key_delay.setValue(100)
        self.keyboard_key_delay.setSuffix(" 毫秒")
        self.keyboard_key_delay.setStyleSheet(self.get_input_style())
        key_layout.addRow("按键延迟:", self.keyboard_key_delay)

        parent_layout.addWidget(key_group)

    def create_keyboard_combo_config(self, parent_layout):
        """创建组合键配置"""
        combo_group = QGroupBox("组合键设置")
        combo_layout = QFormLayout(combo_group)

        # 组合键类型
        self.keyboard_combo_type = QComboBox()
        self.keyboard_combo_type.addItems([
            "Ctrl+A", "Ctrl+C", "Ctrl+V", "Ctrl+X", "Ctrl+Z", "Ctrl+Y",
            "Ctrl+S", "Ctrl+F", "Ctrl+R", "Alt+Tab", "Alt+F4"
        ])
        self.keyboard_combo_type.setStyleSheet(self.get_input_style())
        combo_layout.addRow("组合键:", self.keyboard_combo_type)

        parent_layout.addWidget(combo_group)

    def create_wait_element_config(self, parent_layout):
        """创建等待元素出现配置"""
        wait_group = QGroupBox("等待元素设置")
        wait_layout = QFormLayout(wait_group)

        # 选择器类型
        self.wait_selector_type = QComboBox()
        self.wait_selector_type.addItems(["Selector", "XPath", "文本"])
        self.wait_selector_type.setStyleSheet(self.get_input_style())
        wait_layout.addRow("选择器类型:", self.wait_selector_type)

        # 元素选择器
        self.wait_element_selector = QLineEdit()
        self.wait_element_selector.setPlaceholderText("请输入元素选择器")
        self.wait_element_selector.setStyleSheet(self.get_input_style())
        wait_layout.addRow("元素选择器:", self.wait_element_selector)

        # 超时时间
        self.wait_element_timeout = QSpinBox()
        self.wait_element_timeout.setMinimum(1000)
        self.wait_element_timeout.setMaximum(60000)
        self.wait_element_timeout.setValue(10000)
        self.wait_element_timeout.setSuffix(" 毫秒")
        self.wait_element_timeout.setStyleSheet(self.get_input_style())
        wait_layout.addRow("超时时间:", self.wait_element_timeout)

        parent_layout.addWidget(wait_group)

    def create_wait_request_config(self, parent_layout):
        """创建等待请求完成配置"""
        request_group = QGroupBox("等待请求设置")
        request_layout = QFormLayout(request_group)

        # 请求URL模式
        self.wait_request_url = QLineEdit()
        self.wait_request_url.setPlaceholderText("请输入请求URL模式（支持通配符）")
        self.wait_request_url.setStyleSheet(self.get_input_style())
        request_layout.addRow("请求URL:", self.wait_request_url)

        # 超时时间
        self.wait_request_timeout = QSpinBox()
        self.wait_request_timeout.setMinimum(1000)
        self.wait_request_timeout.setMaximum(60000)
        self.wait_request_timeout.setValue(5000)
        self.wait_request_timeout.setSuffix(" 毫秒")
        self.wait_request_timeout.setStyleSheet(self.get_input_style())
        request_layout.addRow("超时时间:", self.wait_request_timeout)

        parent_layout.addWidget(request_group)

    def create_get_focused_element_config(self, parent_layout):
        """创建获取当前焦点元素配置"""
        focus_group = QGroupBox("焦点元素设置")
        focus_layout = QFormLayout(focus_group)

        # 保存变量
        self.focus_element_save_var = QLineEdit()
        self.focus_element_save_var.setPlaceholderText("请输入保存焦点元素信息的变量名")
        self.focus_element_save_var.setStyleSheet(self.get_input_style())
        focus_layout.addRow("保存至变量:", self.focus_element_save_var)

        # 获取类型
        self.focus_element_type = QComboBox()
        self.focus_element_type.addItems(["元素标签", "元素文本", "元素属性", "元素位置"])
        self.focus_element_type.setStyleSheet(self.get_input_style())
        focus_layout.addRow("获取类型:", self.focus_element_type)

        parent_layout.addWidget(focus_group)

    def create_save_to_file_config(self, parent_layout):
        """创建存到文件配置"""
        file_group = QGroupBox("文件保存设置")
        file_layout = QFormLayout(file_group)

        # 文件路径
        self.save_file_path = QLineEdit()
        self.save_file_path.setPlaceholderText("请输入文件保存路径")
        self.save_file_path.setStyleSheet(self.get_input_style())
        file_layout.addRow("文件路径:", self.save_file_path)

        # 保存内容
        self.save_file_content = QTextEdit()
        self.save_file_content.setFixedHeight(80)
        self.save_file_content.setPlaceholderText("请输入要保存的内容或变量名")
        self.save_file_content.setStyleSheet(self.get_input_style())
        file_layout.addRow("保存内容:", self.save_file_content)

        # 文件编码
        self.save_file_encoding = QComboBox()
        self.save_file_encoding.addItems(["UTF-8", "GBK", "ASCII"])
        self.save_file_encoding.setStyleSheet(self.get_input_style())
        file_layout.addRow("文件编码:", self.save_file_encoding)

        # 写入模式
        self.save_file_mode = QComboBox()
        self.save_file_mode.addItems(["覆盖写入", "追加写入"])
        self.save_file_mode.setStyleSheet(self.get_input_style())
        file_layout.addRow("写入模式:", self.save_file_mode)

        parent_layout.addWidget(file_group)

    def create_save_to_excel_config(self, parent_layout):
        """创建存到Excel配置"""
        excel_group = QGroupBox("Excel保存设置")
        excel_layout = QFormLayout(excel_group)

        # Excel文件路径
        self.save_excel_file = QLineEdit()
        self.save_excel_file.setPlaceholderText("请输入Excel文件路径")
        self.save_excel_file.setStyleSheet(self.get_input_style())
        excel_layout.addRow("Excel文件:", self.save_excel_file)

        # 工作表名称
        self.save_excel_sheet = QLineEdit()
        self.save_excel_sheet.setPlaceholderText("请输入工作表名称")
        self.save_excel_sheet.setText("Sheet1")
        self.save_excel_sheet.setStyleSheet(self.get_input_style())
        excel_layout.addRow("工作表:", self.save_excel_sheet)

        # 起始行
        self.save_excel_row = QSpinBox()
        self.save_excel_row.setMinimum(1)
        self.save_excel_row.setValue(1)
        self.save_excel_row.setStyleSheet(self.get_input_style())
        excel_layout.addRow("起始行:", self.save_excel_row)

        # 起始列
        self.save_excel_col = QSpinBox()
        self.save_excel_col.setMinimum(1)
        self.save_excel_col.setValue(1)
        self.save_excel_col.setStyleSheet(self.get_input_style())
        excel_layout.addRow("起始列:", self.save_excel_col)

        # 保存数据
        self.save_excel_data = QTextEdit()
        self.save_excel_data.setFixedHeight(80)
        self.save_excel_data.setPlaceholderText("请输入要保存的数据或变量名")
        self.save_excel_data.setStyleSheet(self.get_input_style())
        excel_layout.addRow("保存数据:", self.save_excel_data)

        parent_layout.addWidget(excel_group)

    def create_import_txt_config(self, parent_layout):
        """创建导入txt配置"""
        import_group = QGroupBox("导入txt设置")
        import_layout = QFormLayout(import_group)

        # 文件路径
        self.import_txt_file = QLineEdit()
        self.import_txt_file.setPlaceholderText("请输入txt文件路径")
        self.import_txt_file.setStyleSheet(self.get_input_style())
        import_layout.addRow("文件路径:", self.import_txt_file)

        # 保存变量
        self.import_txt_save_var = QLineEdit()
        self.import_txt_save_var.setPlaceholderText("请输入保存内容的变量名")
        self.import_txt_save_var.setStyleSheet(self.get_input_style())
        import_layout.addRow("保存至变量:", self.import_txt_save_var)

        # 文件编码
        self.import_txt_encoding = QComboBox()
        self.import_txt_encoding.addItems(["UTF-8", "GBK", "ASCII"])
        self.import_txt_encoding.setStyleSheet(self.get_input_style())
        import_layout.addRow("文件编码:", self.import_txt_encoding)

        # 读取模式
        self.import_txt_mode = QComboBox()
        self.import_txt_mode.addItems(["全部内容", "按行读取", "随机一行"])
        self.import_txt_mode.setStyleSheet(self.get_input_style())
        import_layout.addRow("读取模式:", self.import_txt_mode)

        parent_layout.addWidget(import_group)

    def create_wait_request_config(self, parent_layout):
        """创建等待请求完成配置"""
        request_group = QGroupBox("等待请求设置")
        request_layout = QFormLayout(request_group)

        # 请求URL模式
        self.wait_request_url = QLineEdit()
        self.wait_request_url.setPlaceholderText("请输入要等待的请求URL模式")
        self.wait_request_url.setStyleSheet(self.get_input_style())
        request_layout.addRow("请求URL:", self.wait_request_url)

        # 等待时间
        self.wait_request_timeout = QSpinBox()
        self.wait_request_timeout.setMinimum(1)
        self.wait_request_timeout.setMaximum(300)
        self.wait_request_timeout.setValue(30)
        self.wait_request_timeout.setSuffix(" 秒")
        self.wait_request_timeout.setStyleSheet(self.get_input_style())
        request_layout.addRow("超时时间:", self.wait_request_timeout)

        parent_layout.addWidget(request_group)

    # ==================== 网络监听功能配置方法 ====================

    def create_listen_request_trigger_config(self, parent_layout):
        """创建监听请求触发配置 - 完全按照AdsPower原版"""
        listen_group = QGroupBox("监听请求触发设置")
        listen_layout = QFormLayout(listen_group)

        # URL模式
        self.listen_url_pattern = QLineEdit()
        self.listen_url_pattern.setPlaceholderText("请输入要监听的URL模式，如：api/login")
        self.listen_url_pattern.setStyleSheet(self.get_input_style())
        listen_layout.addRow("URL模式:", self.listen_url_pattern)

        # 监听方法
        self.listen_method = QComboBox()
        self.listen_method.addItems(["所有方法", "GET", "POST", "PUT", "DELETE", "PATCH"])
        self.listen_method.setStyleSheet(self.get_input_style())
        listen_layout.addRow("请求方法:", self.listen_method)

        # 超时时间
        self.listen_timeout = QSpinBox()
        self.listen_timeout.setMinimum(1)
        self.listen_timeout.setMaximum(300)
        self.listen_timeout.setValue(30)
        self.listen_timeout.setSuffix(" 秒")
        self.listen_timeout.setStyleSheet(self.get_input_style())
        listen_layout.addRow("超时时间:", self.listen_timeout)

        # 保存变量
        self.listen_save_var = QLineEdit()
        self.listen_save_var.setPlaceholderText("请输入保存请求数据的变量名")
        self.listen_save_var.setStyleSheet(self.get_input_style())
        listen_layout.addRow("保存至变量:", self.listen_save_var)

        # 说明
        self.listen_description = QLineEdit()
        self.listen_description.setPlaceholderText("选填")
        self.listen_description.setStyleSheet(self.get_input_style())
        listen_layout.addRow("说明:", self.listen_description)

        parent_layout.addWidget(listen_group)

    def create_listen_request_result_config(self, parent_layout):
        """创建监听请求结果配置 - 完全按照AdsPower原版"""
        result_group = QGroupBox("监听请求结果设置")
        result_layout = QFormLayout(result_group)

        # URL模式
        self.result_url_pattern = QLineEdit()
        self.result_url_pattern.setPlaceholderText("请输入要监听的URL模式")
        self.result_url_pattern.setStyleSheet(self.get_input_style())
        result_layout.addRow("URL模式:", self.result_url_pattern)

        # 响应状态码
        self.result_status_code = QComboBox()
        self.result_status_code.addItems(["所有状态", "200", "201", "400", "401", "403", "404", "500"])
        self.result_status_code.setEditable(True)
        self.result_status_code.setStyleSheet(self.get_input_style())
        result_layout.addRow("状态码:", self.result_status_code)

        # 数据提取类型
        self.result_extract_type = QComboBox()
        self.result_extract_type.addItems(["完整响应", "响应体", "响应头", "状态码", "JSON字段"])
        self.result_extract_type.setStyleSheet(self.get_input_style())
        result_layout.addRow("提取类型:", self.result_extract_type)

        # JSON字段路径（当选择JSON字段时）
        self.result_json_path = QLineEdit()
        self.result_json_path.setPlaceholderText("如：data.user.name")
        self.result_json_path.setStyleSheet(self.get_input_style())
        result_layout.addRow("JSON路径:", self.result_json_path)

        # 超时时间
        self.result_timeout = QSpinBox()
        self.result_timeout.setMinimum(1)
        self.result_timeout.setMaximum(300)
        self.result_timeout.setValue(30)
        self.result_timeout.setSuffix(" 秒")
        self.result_timeout.setStyleSheet(self.get_input_style())
        result_layout.addRow("超时时间:", self.result_timeout)

        # 保存变量
        self.result_save_var = QLineEdit()
        self.result_save_var.setPlaceholderText("请输入保存响应数据的变量名")
        self.result_save_var.setStyleSheet(self.get_input_style())
        result_layout.addRow("保存至变量:", self.result_save_var)

        # 说明
        self.result_description = QLineEdit()
        self.result_description.setPlaceholderText("选填")
        self.result_description.setStyleSheet(self.get_input_style())
        result_layout.addRow("说明:", self.result_description)

        parent_layout.addWidget(result_group)

    def create_stop_page_listening_config(self, parent_layout):
        """创建停止页面监听配置 - 无参数，直接执行"""
        info_label = QLabel("停止页面监听操作无需配置参数，将清除所有网络监听脚本")
        info_label.setStyleSheet("color: #666; font-size: 13px; padding: 20px;")
        parent_layout.addWidget(info_label)

    def create_get_page_cookies_config(self, parent_layout):
        """创建获取页面Cookie配置 - 完全按照AdsPower原版"""
        cookie_group = QGroupBox("获取页面Cookie设置")
        cookie_layout = QFormLayout(cookie_group)

        # Cookie类型
        self.cookie_type = QComboBox()
        self.cookie_type.addItems(["所有Cookie", "指定Cookie", "Cookie数量"])
        self.cookie_type.setStyleSheet(self.get_input_style())
        cookie_layout.addRow("Cookie类型:", self.cookie_type)

        # Cookie名称（当选择指定Cookie时）
        self.cookie_name = QLineEdit()
        self.cookie_name.setPlaceholderText("请输入Cookie名称")
        self.cookie_name.setStyleSheet(self.get_input_style())
        cookie_layout.addRow("Cookie名称:", self.cookie_name)

        # 保存变量
        self.cookie_save_var = QLineEdit()
        self.cookie_save_var.setPlaceholderText("请输入保存Cookie的变量名")
        self.cookie_save_var.setStyleSheet(self.get_input_style())
        cookie_layout.addRow("保存至变量:", self.cookie_save_var)

        # 说明
        self.cookie_description = QLineEdit()
        self.cookie_description.setPlaceholderText("选填")
        self.cookie_description.setStyleSheet(self.get_input_style())
        cookie_layout.addRow("说明:", self.cookie_description)

        parent_layout.addWidget(cookie_group)

    def create_clear_page_cookies_config(self, parent_layout):
        """创建清除页面Cookie配置 - 完全按照AdsPower原版"""
        clear_group = QGroupBox("清除页面Cookie设置")
        clear_layout = QFormLayout(clear_group)

        # 清除类型
        self.clear_cookie_type = QComboBox()
        self.clear_cookie_type.addItems(["所有Cookie", "指定Cookie", "指定域名Cookie"])
        self.clear_cookie_type.setStyleSheet(self.get_input_style())
        clear_layout.addRow("清除类型:", self.clear_cookie_type)

        # Cookie名称或域名
        self.clear_cookie_target = QLineEdit()
        self.clear_cookie_target.setPlaceholderText("请输入Cookie名称或域名")
        self.clear_cookie_target.setStyleSheet(self.get_input_style())
        clear_layout.addRow("目标:", self.clear_cookie_target)

        # 说明
        self.clear_cookie_description = QLineEdit()
        self.clear_cookie_description.setPlaceholderText("选填")
        self.clear_cookie_description.setStyleSheet(self.get_input_style())
        clear_layout.addRow("说明:", self.clear_cookie_description)

        parent_layout.addWidget(clear_group)

    def create_operation_info(self, parent_layout):
        """创建操作说明信息区域"""
        info_widget = QWidget()
        info_widget.setStyleSheet("""
            QWidget {
                background-color: #f6f8fa;
                border: 1px solid #e1e4e8;
                border-radius: 6px;
                padding: 10px;
            }
        """)
        info_layout = QVBoxLayout(info_widget)
        info_layout.setContentsMargins(10, 10, 10, 10)

        # 操作说明
        operation_descriptions = {
            "新建标签": "创建一个新的浏览器标签页",
            "关闭标签": "关闭当前或指定的浏览器标签页",
            "关闭其他标签": "关闭除当前标签外的所有其他标签页",
            "切换标签": "切换到指定的浏览器标签页",
            "访问网站": "在当前标签页中访问指定的网址",
            "刷新页面": "刷新当前页面",
            "页面后退": "返回到上一个页面",
            "页面截图": "对当前页面进行截图保存",
            "经过元素": "鼠标悬停在指定元素上",
            "下拉选择器": "操作页面中的下拉选择框",
            "元素聚焦": "将焦点设置到指定元素上",
            "点击元素": "点击页面中的指定元素",
            "输入内容": "在指定元素中输入文本内容",
            "上传附件": "上传文件到指定的文件输入框",
            "执行JS脚本": "在页面中执行JavaScript代码",
            "键盘按键": "模拟键盘按键操作",
            "组合键": "模拟键盘组合键操作",
            "等待时间": "等待指定的时间",
            "等待元素出现": "等待页面元素出现",
            "等待请求完成": "等待网络请求完成",
            "获取URL": "获取当前页面的URL地址",
            "获取粘贴板内容": "获取系统剪贴板中的内容",
            "元素数据": "获取指定元素的数据信息",
            "当前焦点元素": "获取当前获得焦点的元素",
            "存到文件": "将数据保存到文件中",
            "存到Excel": "将数据保存到Excel文件中",
            "导入txt": "从txt文件中导入数据",
            "获取邮件": "从邮箱中获取邮件内容",
            "身份验证器码": "获取身份验证器的验证码",
            "监听请求触发": "监听网络请求的触发",
            "监听请求结果": "监听网络请求的结果",
            "停止页面监听": "停止对页面的监听",
            "获取页面Cookie": "获取当前页面的Cookie信息",
            "清除页面Cookie": "清除当前页面的Cookie",
            "文本中提取": "从文本中提取指定内容",
            "转换Json对象": "将数据转换为JSON对象",
            "字段提取": "从数据中提取指定字段",
            "随机提取": "随机提取数据内容",
            "更新环境备注": "更新AdsPower环境的备注信息",
            "更新环境标签": "更新AdsPower环境的标签",
            "启动新浏览器": "启动一个新的浏览器环境",
            "使用其他流程": "调用其他的RPA流程",
            "IF条件": "根据条件执行不同的操作",
            "For循环元素": "循环遍历页面元素",
            "For循环次数": "按指定次数循环执行",
            "For循环数据": "循环遍历数据集合",
            "While循环": "根据条件循环执行",
            "退出循环": "跳出当前循环",
            "关闭浏览器": "关闭当前浏览器"
        }

        desc_text = operation_descriptions.get(self.operation_name, "执行指定的RPA操作")
        desc_label = QLabel(f"📝 {desc_text}")
        desc_label.setStyleSheet("color: #586069; font-size: 13px;")
        info_layout.addWidget(desc_label)

        parent_layout.addWidget(info_widget)

    def create_variable_selector(self, label_text="变量", placeholder="请选择变量"):
        """创建变量选择器组件"""
        variable_combo = QComboBox()
        variable_combo.setEditable(True)
        variable_combo.setPlaceholderText(placeholder)

        # 添加常用的AdsPower环境变量
        adspower_variables = [
            "task_id",           # 任务ID
            "task_name",         # 任务名称
            "serial_number",     # 环境编号
            "browser_name",      # 环境名称
            "acc_id",           # 环境ID
            "comment",          # 环境备注
            "user_name",        # 平台账户
            "password",         # 平台密码
            "for_elements_item", # For循环元素项
            "for_elements_index", # For循环元素索引
            "for_times_index",   # For循环次数索引
            "for_list_item",     # For循环数据项
            "for_list_index"     # For循环数据索引
        ]

        variable_combo.addItems(adspower_variables)
        variable_combo.setStyleSheet(self.get_input_style())
        return variable_combo

    def create_element_config(self, parent_layout):
        """创建元素操作配置"""
        # 选择器配置
        selector_group = QGroupBox("元素选择器")
        selector_layout = QFormLayout(selector_group)
        
        self.selector_input = QLineEdit()
        self.selector_input.setPlaceholderText("如: #email_input, .button_search")
        self.selector_input.setStyleSheet(self.get_input_style())
        selector_layout.addRow("选择器:", self.selector_input)
        
        # 元素顺序
        self.element_order = QSpinBox()
        self.element_order.setMinimum(1)
        self.element_order.setValue(1)
        self.element_order.setStyleSheet(self.get_input_style())
        selector_layout.addRow("元素顺序:", self.element_order)
        
        parent_layout.addWidget(selector_group)
        
        # 如果是输入内容，添加内容配置
        if self.operation_name == "输入内容":
            content_group = QGroupBox("输入内容")
            content_layout = QFormLayout(content_group)
            
            self.content_input = QTextEdit()
            self.content_input.setFixedHeight(100)
            self.content_input.setPlaceholderText("输入要填写的内容")
            self.content_input.setStyleSheet(self.get_input_style())
            content_layout.addRow("内容:", self.content_input)
            
            self.input_interval = QSpinBox()
            self.input_interval.setMinimum(0)
            self.input_interval.setMaximum(5000)
            self.input_interval.setValue(100)
            self.input_interval.setSuffix(" 毫秒")
            self.input_interval.setStyleSheet(self.get_input_style())
            content_layout.addRow("输入间隔:", self.input_interval)
            
            parent_layout.addWidget(content_group)
            
        # 如果是点击元素，添加点击配置
        if self.operation_name == "点击元素":
            click_group = QGroupBox("点击配置")
            click_layout = QFormLayout(click_group)
            
            self.click_type = QComboBox()
            self.click_type.addItems(["鼠标左键", "鼠标中键", "鼠标右键"])
            self.click_type.setStyleSheet(self.get_input_style())
            click_layout.addRow("点击类型:", self.click_type)
            
            self.click_action = QComboBox()
            self.click_action.addItems(["单击", "双击"])
            self.click_action.setStyleSheet(self.get_input_style())
            click_layout.addRow("按键类型:", self.click_action)
            
            parent_layout.addWidget(click_group)
            
    def create_navigate_config(self, parent_layout):
        """创建访问网站配置"""
        nav_group = QGroupBox("网站访问")
        nav_layout = QFormLayout(nav_group)
        
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://www.example.com")
        self.url_input.setStyleSheet(self.get_input_style())
        nav_layout.addRow("访问URL:", self.url_input)
        
        parent_layout.addWidget(nav_group)

    # ==================== 新增的50个AdsPower RPA功能配置方法 ====================

    def create_hover_element_config(self, parent_layout):
        """创建经过元素配置 - 完全按照AdsPower原版"""
        hover_group = QGroupBox("经过元素设置")
        hover_layout = QFormLayout(hover_group)

        # 选择器类型
        self.hover_selector_type = QComboBox()
        self.hover_selector_type.addItems(["Selector", "XPath", "文本"])
        self.hover_selector_type.setStyleSheet(self.get_input_style())
        hover_layout.addRow("选择器类型:", self.hover_selector_type)

        # 元素选择器
        self.hover_selector = QLineEdit()
        self.hover_selector.setPlaceholderText("请输入元素选择器，比如 #email input")
        self.hover_selector.setStyleSheet(self.get_input_style())
        hover_layout.addRow("元素选择器:", self.hover_selector)

        # 使用变量按钮
        use_var_btn = QPushButton("使用变量")
        use_var_btn.setStyleSheet("color: #1890ff; border: none; text-decoration: underline;")
        hover_layout.addRow("", use_var_btn)

        # 元素顺序
        self.hover_element_order = QSpinBox()
        self.hover_element_order.setMinimum(1)
        self.hover_element_order.setValue(1)
        self.hover_element_order.setStyleSheet(self.get_input_style())
        hover_layout.addRow("元素顺序:", self.hover_element_order)

        # 说明
        self.hover_description = QLineEdit()
        self.hover_description.setPlaceholderText("选填")
        self.hover_description.setStyleSheet(self.get_input_style())
        hover_layout.addRow("说明:", self.hover_description)

        parent_layout.addWidget(hover_group)

    def create_dropdown_selector_config(self, parent_layout):
        """创建下拉选择器配置 - 完全按照AdsPower原版"""
        dropdown_group = QGroupBox("下拉选择器设置")
        dropdown_layout = QFormLayout(dropdown_group)

        # 选择器类型
        self.dropdown_selector_type = QComboBox()
        self.dropdown_selector_type.addItems(["Selector", "XPath", "文本"])
        self.dropdown_selector_type.setStyleSheet(self.get_input_style())
        dropdown_layout.addRow("选择器类型:", self.dropdown_selector_type)

        # 元素选择器
        self.dropdown_selector = QLineEdit()
        self.dropdown_selector.setPlaceholderText("请输入元素选择器，比如 #email input")
        self.dropdown_selector.setStyleSheet(self.get_input_style())
        dropdown_layout.addRow("元素选择器:", self.dropdown_selector)

        # 使用变量按钮
        use_var_btn = QPushButton("使用变量")
        use_var_btn.setStyleSheet("color: #1890ff; border: none; text-decoration: underline;")
        dropdown_layout.addRow("", use_var_btn)

        # 选择方式
        self.dropdown_select_type = QComboBox()
        self.dropdown_select_type.addItems(["按文本", "按值", "按索引"])
        self.dropdown_select_type.setStyleSheet(self.get_input_style())
        dropdown_layout.addRow("选择方式:", self.dropdown_select_type)

        # 选择值
        self.dropdown_select_value = QLineEdit()
        self.dropdown_select_value.setPlaceholderText("请输入选择值")
        self.dropdown_select_value.setStyleSheet(self.get_input_style())
        dropdown_layout.addRow("选择值:", self.dropdown_select_value)

        # 元素顺序
        self.dropdown_element_order = QSpinBox()
        self.dropdown_element_order.setMinimum(1)
        self.dropdown_element_order.setValue(1)
        self.dropdown_element_order.setStyleSheet(self.get_input_style())
        dropdown_layout.addRow("元素顺序:", self.dropdown_element_order)

        # 说明
        self.dropdown_description = QLineEdit()
        self.dropdown_description.setPlaceholderText("选填")
        self.dropdown_description.setStyleSheet(self.get_input_style())
        dropdown_layout.addRow("说明:", self.dropdown_description)

        parent_layout.addWidget(dropdown_group)

    def create_focus_element_config(self, parent_layout):
        """创建元素聚焦配置 - 完全按照AdsPower原版"""
        focus_group = QGroupBox("元素聚焦设置")
        focus_layout = QFormLayout(focus_group)

        # 选择器类型
        self.focus_selector_type = QComboBox()
        self.focus_selector_type.addItems(["Selector", "XPath", "文本"])
        self.focus_selector_type.setStyleSheet(self.get_input_style())
        focus_layout.addRow("选择器类型:", self.focus_selector_type)

        # 元素选择器
        self.focus_selector = QLineEdit()
        self.focus_selector.setPlaceholderText("请输入元素选择器，比如 #email input")
        self.focus_selector.setStyleSheet(self.get_input_style())
        focus_layout.addRow("元素选择器:", self.focus_selector)

        # 使用变量按钮
        use_var_btn = QPushButton("使用变量")
        use_var_btn.setStyleSheet("color: #1890ff; border: none; text-decoration: underline;")
        focus_layout.addRow("", use_var_btn)

        # 元素顺序
        self.focus_element_order = QSpinBox()
        self.focus_element_order.setMinimum(1)
        self.focus_element_order.setValue(1)
        self.focus_element_order.setStyleSheet(self.get_input_style())
        focus_layout.addRow("元素顺序:", self.focus_element_order)

        # 说明
        self.focus_description = QLineEdit()
        self.focus_description.setPlaceholderText("选填")
        self.focus_description.setStyleSheet(self.get_input_style())
        focus_layout.addRow("说明:", self.focus_description)

        parent_layout.addWidget(focus_group)

    def create_wait_time_config(self, parent_layout):
        """创建等待时间配置 - 完全按照AdsPower原版"""
        wait_group = QGroupBox("等待时间设置")
        wait_layout = QFormLayout(wait_group)

        # 等待类型
        self.wait_time_type = QComboBox()
        self.wait_time_type.addItems(["固定时间", "随机时间"])
        self.wait_time_type.setStyleSheet(self.get_input_style())
        wait_layout.addRow("等待类型:", self.wait_time_type)

        # 等待时间
        self.wait_time_value = QSpinBox()
        self.wait_time_value.setMinimum(100)
        self.wait_time_value.setMaximum(300000)
        self.wait_time_value.setValue(1000)
        self.wait_time_value.setSuffix(" 毫秒")
        self.wait_time_value.setStyleSheet(self.get_input_style())
        wait_layout.addRow("等待时间:", self.wait_time_value)

        # 随机范围（当选择随机时间时）
        self.wait_time_max = QSpinBox()
        self.wait_time_max.setMinimum(100)
        self.wait_time_max.setMaximum(300000)
        self.wait_time_max.setValue(3000)
        self.wait_time_max.setSuffix(" 毫秒")
        self.wait_time_max.setStyleSheet(self.get_input_style())
        wait_layout.addRow("最大时间:", self.wait_time_max)

        # 说明
        self.wait_time_description = QLineEdit()
        self.wait_time_description.setPlaceholderText("选填")
        self.wait_time_description.setStyleSheet(self.get_input_style())
        wait_layout.addRow("说明:", self.wait_time_description)

        parent_layout.addWidget(wait_group)

    def create_get_email_config(self, parent_layout):
        """创建获取邮件配置 - 完全按照AdsPower原版"""
        email_group = QGroupBox("获取邮件设置")
        email_layout = QFormLayout(email_group)

        # 邮箱服务器
        self.email_server = QLineEdit()
        self.email_server.setPlaceholderText("如：imap.gmail.com")
        self.email_server.setStyleSheet(self.get_input_style())
        email_layout.addRow("邮箱服务器:", self.email_server)

        # 端口
        self.email_port = QSpinBox()
        self.email_port.setMinimum(1)
        self.email_port.setMaximum(65535)
        self.email_port.setValue(993)
        self.email_port.setStyleSheet(self.get_input_style())
        email_layout.addRow("端口:", self.email_port)

        # 邮箱账号
        self.email_user = QLineEdit()
        self.email_user.setPlaceholderText("请输入邮箱账号")
        self.email_user.setStyleSheet(self.get_input_style())
        email_layout.addRow("邮箱账号:", self.email_user)

        # 邮箱密码
        self.email_password = QLineEdit()
        self.email_password.setEchoMode(QLineEdit.Password)
        self.email_password.setPlaceholderText("请输入邮箱密码")
        self.email_password.setStyleSheet(self.get_input_style())
        email_layout.addRow("邮箱密码:", self.email_password)

        # 邮件数量
        self.email_count = QSpinBox()
        self.email_count.setMinimum(1)
        self.email_count.setMaximum(100)
        self.email_count.setValue(1)
        self.email_count.setStyleSheet(self.get_input_style())
        email_layout.addRow("获取数量:", self.email_count)

        # 保存变量
        self.email_save_var = QLineEdit()
        self.email_save_var.setPlaceholderText("请输入保存邮件的变量名")
        self.email_save_var.setStyleSheet(self.get_input_style())
        email_layout.addRow("保存至变量:", self.email_save_var)

        parent_layout.addWidget(email_group)

    def create_get_totp_config(self, parent_layout):
        """创建身份验证器码配置 - 完全按照AdsPower原版"""
        totp_group = QGroupBox("身份验证器设置")
        totp_layout = QFormLayout(totp_group)

        # 密钥
        self.totp_secret = QLineEdit()
        self.totp_secret.setPlaceholderText("请输入TOTP密钥")
        self.totp_secret.setStyleSheet(self.get_input_style())
        totp_layout.addRow("TOTP密钥:", self.totp_secret)

        # 保存变量
        self.totp_save_var = QLineEdit()
        self.totp_save_var.setPlaceholderText("请输入保存验证码的变量名")
        self.totp_save_var.setStyleSheet(self.get_input_style())
        totp_layout.addRow("保存至变量:", self.totp_save_var)

        # 说明
        self.totp_description = QLineEdit()
        self.totp_description.setPlaceholderText("选填")
        self.totp_description.setStyleSheet(self.get_input_style())
        totp_layout.addRow("说明:", self.totp_description)

        parent_layout.addWidget(totp_group)

    def create_text_extract_config(self, parent_layout):
        """创建文本中提取配置 - 完全按照AdsPower原版"""
        extract_group = QGroupBox("文本提取设置")
        extract_layout = QFormLayout(extract_group)

        # 源变量
        self.extract_source_var = QLineEdit()
        self.extract_source_var.setPlaceholderText("请输入源文本变量名")
        self.extract_source_var.setStyleSheet(self.get_input_style())
        extract_layout.addRow("源变量:", self.extract_source_var)

        # 提取模式
        self.extract_pattern = QLineEdit()
        self.extract_pattern.setPlaceholderText("请输入正则表达式")
        self.extract_pattern.setStyleSheet(self.get_input_style())
        extract_layout.addRow("提取模式:", self.extract_pattern)

        # 提取类型
        self.extract_type = QComboBox()
        self.extract_type.addItems(["第一个匹配", "所有匹配", "最后一个匹配", "匹配数量"])
        self.extract_type.setStyleSheet(self.get_input_style())
        extract_layout.addRow("提取类型:", self.extract_type)

        # 分组索引
        self.extract_group_index = QSpinBox()
        self.extract_group_index.setMinimum(0)
        self.extract_group_index.setValue(0)
        self.extract_group_index.setStyleSheet(self.get_input_style())
        extract_layout.addRow("分组索引:", self.extract_group_index)

        # 保存变量
        self.extract_save_var = QLineEdit()
        self.extract_save_var.setPlaceholderText("请输入保存结果的变量名")
        self.extract_save_var.setStyleSheet(self.get_input_style())
        extract_layout.addRow("保存至变量:", self.extract_save_var)

        # 大小写敏感
        self.extract_case_sensitive = QCheckBox("大小写敏感")
        self.extract_case_sensitive.setChecked(True)
        extract_layout.addRow("", self.extract_case_sensitive)

        parent_layout.addWidget(extract_group)

    def create_json_convert_config(self, parent_layout):
        """创建转换Json对象配置 - 完全按照AdsPower原版"""
        json_group = QGroupBox("JSON转换设置")
        json_layout = QFormLayout(json_group)

        # 转换类型
        self.json_convert_type = QComboBox()
        self.json_convert_type.addItems(["对象转JSON", "JSON转对象", "格式化JSON", "压缩JSON"])
        self.json_convert_type.setStyleSheet(self.get_input_style())
        json_layout.addRow("转换类型:", self.json_convert_type)

        # 源数据
        self.json_source_var = QLineEdit()
        self.json_source_var.setPlaceholderText("请输入源数据变量名")
        self.json_source_var.setStyleSheet(self.get_input_style())
        json_layout.addRow("源数据:", self.json_source_var)

        # 保存变量
        self.json_save_var = QLineEdit()
        self.json_save_var.setPlaceholderText("请输入保存结果的变量名")
        self.json_save_var.setStyleSheet(self.get_input_style())
        json_layout.addRow("保存至变量:", self.json_save_var)

        parent_layout.addWidget(json_group)

    def create_field_extract_config(self, parent_layout):
        """创建字段提取配置 - 完全按照AdsPower原版"""
        field_group = QGroupBox("字段提取设置")
        field_layout = QFormLayout(field_group)

        # 源变量
        self.field_source_var = QLineEdit()
        self.field_source_var.setPlaceholderText("请输入源数据变量名")
        self.field_source_var.setStyleSheet(self.get_input_style())
        field_layout.addRow("源变量:", self.field_source_var)

        # 字段路径
        self.field_path = QLineEdit()
        self.field_path.setPlaceholderText("如：user.name 或 data[0].title")
        self.field_path.setStyleSheet(self.get_input_style())
        field_layout.addRow("字段路径:", self.field_path)

        # 默认值
        self.field_default_value = QLineEdit()
        self.field_default_value.setPlaceholderText("字段不存在时的默认值")
        self.field_default_value.setStyleSheet(self.get_input_style())
        field_layout.addRow("默认值:", self.field_default_value)

        # 保存变量
        self.field_save_var = QLineEdit()
        self.field_save_var.setPlaceholderText("请输入保存结果的变量名")
        self.field_save_var.setStyleSheet(self.get_input_style())
        field_layout.addRow("保存至变量:", self.field_save_var)

        parent_layout.addWidget(field_group)

    def create_random_extract_config(self, parent_layout):
        """创建随机提取配置 - 完全按照AdsPower原版"""
        random_group = QGroupBox("随机提取设置")
        random_layout = QFormLayout(random_group)

        # 源变量
        self.random_source_var = QLineEdit()
        self.random_source_var.setPlaceholderText("请输入源数据变量名")
        self.random_source_var.setStyleSheet(self.get_input_style())
        random_layout.addRow("源变量:", self.random_source_var)

        # 提取类型
        self.random_extract_type = QComboBox()
        self.random_extract_type.addItems(["随机行", "随机元素", "随机字符", "随机单词"])
        self.random_extract_type.setStyleSheet(self.get_input_style())
        random_layout.addRow("提取类型:", self.random_extract_type)

        # 提取数量
        self.random_count = QSpinBox()
        self.random_count.setMinimum(1)
        self.random_count.setMaximum(1000)
        self.random_count.setValue(1)
        self.random_count.setStyleSheet(self.get_input_style())
        random_layout.addRow("提取数量:", self.random_count)

        # 唯一性
        self.random_unique = QCheckBox("确保唯一性（不重复）")
        self.random_unique.setChecked(True)
        random_layout.addRow("", self.random_unique)

        # 保存变量
        self.random_save_var = QLineEdit()
        self.random_save_var.setPlaceholderText("请输入保存结果的变量名")
        self.random_save_var.setStyleSheet(self.get_input_style())
        random_layout.addRow("保存至变量:", self.random_save_var)

        parent_layout.addWidget(random_group)

    def create_update_env_note_config(self, parent_layout):
        """创建更新环境备注配置 - 完全按照AdsPower原版"""
        env_group = QGroupBox("更新环境备注设置")
        env_layout = QFormLayout(env_group)

        # 环境ID
        self.env_note_id = QLineEdit()
        self.env_note_id.setPlaceholderText("请输入环境ID")
        self.env_note_id.setStyleSheet(self.get_input_style())
        env_layout.addRow("环境ID:", self.env_note_id)

        # 备注内容
        self.env_note_content = QTextEdit()
        self.env_note_content.setFixedHeight(80)
        self.env_note_content.setPlaceholderText("请输入备注内容")
        self.env_note_content.setStyleSheet(self.get_input_style())
        env_layout.addRow("备注内容:", self.env_note_content)

        # 更新方式
        self.env_note_mode = QComboBox()
        self.env_note_mode.addItems(["覆盖", "追加"])
        self.env_note_mode.setStyleSheet(self.get_input_style())
        env_layout.addRow("更新方式:", self.env_note_mode)

        parent_layout.addWidget(env_group)

    def create_update_env_tag_config(self, parent_layout):
        """创建更新环境标签配置 - 完全按照AdsPower原版"""
        tag_group = QGroupBox("更新环境标签设置")
        tag_layout = QFormLayout(tag_group)

        # 环境ID
        self.env_tag_id = QLineEdit()
        self.env_tag_id.setPlaceholderText("请输入环境ID")
        self.env_tag_id.setStyleSheet(self.get_input_style())
        tag_layout.addRow("环境ID:", self.env_tag_id)

        # 操作类型
        self.env_tag_operation = QComboBox()
        self.env_tag_operation.addItems(["添加", "删除", "替换"])
        self.env_tag_operation.setStyleSheet(self.get_input_style())
        tag_layout.addRow("操作类型:", self.env_tag_operation)

        # 标签值
        self.env_tag_value = QLineEdit()
        self.env_tag_value.setPlaceholderText("请输入标签值")
        self.env_tag_value.setStyleSheet(self.get_input_style())
        tag_layout.addRow("标签值:", self.env_tag_value)

        parent_layout.addWidget(tag_group)

    def create_for_loop_elements_config(self, parent_layout):
        """创建For循环元素配置 - 完全按照AdsPower原版"""
        # 顶部提示信息
        info_widget = QWidget()
        info_widget.setStyleSheet("""
            QWidget {
                background-color: #f6f8fa;
                border: 1px solid #e1e4e8;
                border-radius: 6px;
                padding: 10px;
                margin-bottom: 15px;
            }
        """)
        info_layout = QVBoxLayout(info_widget)
        info_layout.setContentsMargins(10, 10, 10, 10)

        info_label = QLabel("获取元素选择器在页面上所有相同的元素的循环执行 了解详情")
        info_label.setStyleSheet("color: #586069; font-size: 13px;")
        info_layout.addWidget(info_label)
        parent_layout.addWidget(info_widget)

        # 主要配置区域
        for_group = QGroupBox("For循环元素设置")
        for_layout = QFormLayout(for_group)

        # 选择器类型
        self.for_selector_type = QComboBox()
        self.for_selector_type.addItems(["Selector", "XPath", "文本"])
        self.for_selector_type.setStyleSheet(self.get_input_style())
        for_layout.addRow("选择器类型:", self.for_selector_type)

        # 元素选择器
        self.for_element_selector = QLineEdit()
        self.for_element_selector.setPlaceholderText("请输入元素选择器，比如 #email input")
        self.for_element_selector.setStyleSheet(self.get_input_style())
        for_layout.addRow("元素选择器:", self.for_element_selector)

        # 使用变量按钮
        use_var_btn = QPushButton("使用变量")
        use_var_btn.setStyleSheet("color: #1890ff; border: none; text-decoration: underline;")
        for_layout.addRow("", use_var_btn)

        # 提取类型
        self.for_extract_type = QComboBox()
        self.for_extract_type.addItems(["文本", "对象", "IFrame框架", "源码", "属性", "子元素"])
        self.for_extract_type.setStyleSheet(self.get_input_style())
        for_layout.addRow("提取类型:", self.for_extract_type)

        # 循环对象保存至
        self.for_object_var = QLineEdit()
        self.for_object_var.setText("for_elements_item")
        self.for_object_var.setStyleSheet(self.get_input_style())
        for_layout.addRow("循环对象保存至:", self.for_object_var)

        # 循环位置保存至
        self.for_index_var = QLineEdit()
        self.for_index_var.setText("for_elements_index")
        self.for_index_var.setStyleSheet(self.get_input_style())
        for_layout.addRow("循环位置保存至:", self.for_index_var)

        # 说明
        self.for_elements_description = QLineEdit()
        self.for_elements_description.setPlaceholderText("选填")
        self.for_elements_description.setStyleSheet(self.get_input_style())
        for_layout.addRow("说明:", self.for_elements_description)

        parent_layout.addWidget(for_group)

    def create_for_loop_count_config(self, parent_layout):
        """创建For循环次数配置 - 完全按照AdsPower原版"""
        for_count_group = QGroupBox("For循环次数设置")
        for_count_layout = QFormLayout(for_count_group)

        # 次数设置
        self.for_count_input = QSpinBox()
        self.for_count_input.setMinimum(1)
        self.for_count_input.setMaximum(999999)
        self.for_count_input.setValue(10)
        self.for_count_input.setStyleSheet(self.get_input_style())
        for_count_layout.addRow("次数:", self.for_count_input)

        # 使用变量选择
        self.for_count_variable = self.create_variable_selector("变量", "请选择变量")
        for_count_layout.addRow("或使用变量:", self.for_count_variable)

        # 循环位置保存至
        self.for_count_index_var = QLineEdit()
        self.for_count_index_var.setText("for_times_index")
        self.for_count_index_var.setStyleSheet(self.get_input_style())
        for_count_layout.addRow("循环位置保存至:", self.for_count_index_var)

        # 说明
        self.for_count_description = QLineEdit()
        self.for_count_description.setPlaceholderText("选填")
        self.for_count_description.setStyleSheet(self.get_input_style())
        for_count_layout.addRow("说明:", self.for_count_description)

        parent_layout.addWidget(for_count_group)

    def create_for_loop_data_config(self, parent_layout):
        """创建For循环数据配置 - 完全按照AdsPower原版"""
        # 顶部提示信息
        info_widget = QWidget()
        info_widget.setStyleSheet("""
            QWidget {
                background-color: #f6f8fa;
                border: 1px solid #e1e4e8;
                border-radius: 6px;
                padding: 10px;
                margin-bottom: 15px;
            }
        """)
        info_layout = QVBoxLayout(info_widget)
        info_layout.setContentsMargins(10, 10, 10, 10)

        info_label = QLabel("以数组数据循环执行")
        info_label.setStyleSheet("color: #586069; font-size: 13px;")
        info_layout.addWidget(info_label)
        parent_layout.addWidget(info_widget)

        # 主要配置区域
        for_data_group = QGroupBox("For循环数据设置")
        for_data_layout = QFormLayout(for_data_group)

        # 数据选择
        self.for_data_variable = self.create_variable_selector("数据", "请选择变量")
        for_data_layout.addRow("数据选择:", self.for_data_variable)

        # 无数据提示
        no_data_label = QLabel("无数据")
        no_data_label.setStyleSheet("color: #999; font-size: 12px;")
        for_data_layout.addRow("", no_data_label)

        # 循环对象保存至
        self.for_data_object_var = QLineEdit()
        self.for_data_object_var.setText("for_list_item")
        self.for_data_object_var.setStyleSheet(self.get_input_style())
        for_data_layout.addRow("循环对象保存至:", self.for_data_object_var)

        # 循环位置保存至
        self.for_data_index_var = QLineEdit()
        self.for_data_index_var.setText("for_list_index")
        self.for_data_index_var.setStyleSheet(self.get_input_style())
        for_data_layout.addRow("循环位置保存至:", self.for_data_index_var)

        # 说明
        self.for_data_description = QLineEdit()
        self.for_data_description.setPlaceholderText("选填")
        self.for_data_description.setStyleSheet(self.get_input_style())
        for_data_layout.addRow("说明:", self.for_data_description)

        parent_layout.addWidget(for_data_group)

    def create_while_loop_config(self, parent_layout):
        """创建While循环配置 - 完全按照AdsPower原版"""
        # 顶部提示信息
        info_widget = QWidget()
        info_widget.setStyleSheet("""
            QWidget {
                background-color: #f6f8fa;
                border: 1px solid #e1e4e8;
                border-radius: 6px;
                padding: 10px;
                margin-bottom: 15px;
            }
        """)
        info_layout = QVBoxLayout(info_widget)
        info_layout.setContentsMargins(10, 10, 10, 10)

        info_label = QLabel("判断条件成立时执行相应的任务 了解详情")
        info_label.setStyleSheet("color: #586069; font-size: 13px;")
        info_layout.addWidget(info_label)
        parent_layout.addWidget(info_widget)

        # 主要配置区域
        while_group = QGroupBox("While循环设置")
        while_layout = QFormLayout(while_group)

        # 变量选择
        self.while_variable = self.create_variable_selector("变量", "请选择变量")
        while_layout.addRow("变量:", self.while_variable)

        # 条件操作符
        self.while_condition = QComboBox()
        self.while_condition.addItems([
            "存在", "不存在", "小于", "小于等于", "等于", "不等于",
            "大于", "大于等于", "包含", "不包含", "在其中", "不在其中"
        ])
        self.while_condition.setStyleSheet(self.get_input_style())
        while_layout.addRow("条件:", self.while_condition)

        # 说明
        self.while_description = QLineEdit()
        self.while_description.setPlaceholderText("选填")
        self.while_description.setStyleSheet(self.get_input_style())
        while_layout.addRow("说明:", self.while_description)

        parent_layout.addWidget(while_group)

    def create_scroll_config(self, parent_layout):
        """创建滚动页面配置"""
        scroll_group = QGroupBox("滚动设置")
        scroll_layout = QFormLayout(scroll_group)
        
        self.scroll_type = QComboBox()
        self.scroll_type.addItems(["位置", "像素"])
        self.scroll_type.setStyleSheet(self.get_input_style())
        scroll_layout.addRow("滚动距离:", self.scroll_type)
        
        self.scroll_position = QComboBox()
        self.scroll_position.addItems(["顶部", "中部", "底部"])
        self.scroll_position.setStyleSheet(self.get_input_style())
        scroll_layout.addRow("滚动位置:", self.scroll_position)
        
        self.scroll_pixels = QSpinBox()
        self.scroll_pixels.setMinimum(0)
        self.scroll_pixels.setMaximum(10000)
        self.scroll_pixels.setValue(500)
        self.scroll_pixels.setSuffix(" 像素")
        self.scroll_pixels.setStyleSheet(self.get_input_style())
        scroll_layout.addRow("滚动像素:", self.scroll_pixels)
        
        self.scroll_behavior = QComboBox()
        self.scroll_behavior.addItems(["平滑", "瞬间"])
        self.scroll_behavior.setStyleSheet(self.get_input_style())
        scroll_layout.addRow("滚动类型:", self.scroll_behavior)
        
        parent_layout.addWidget(scroll_group)
        
    def create_upload_config(self, parent_layout):
        """创建上传附件配置"""
        upload_group = QGroupBox("上传设置")
        upload_layout = QFormLayout(upload_group)
        
        self.upload_selector = QLineEdit()
        self.upload_selector.setPlaceholderText('input[type="file"]')
        self.upload_selector.setStyleSheet(self.get_input_style())
        upload_layout.addRow("选择器:", self.upload_selector)
        
        self.upload_type = QComboBox()
        self.upload_type.addItems(["本地文件", "文件夹文件随机", "网络URL"])
        self.upload_type.setStyleSheet(self.get_input_style())
        upload_layout.addRow("附件类型:", self.upload_type)
        
        self.file_path = QLineEdit()
        self.file_path.setPlaceholderText("文件路径或URL")
        self.file_path.setStyleSheet(self.get_input_style())
        upload_layout.addRow("文件路径:", self.file_path)
        
        parent_layout.addWidget(upload_group)
        
    def create_javascript_config(self, parent_layout):
        """创建JS脚本配置"""
        js_group = QGroupBox("JavaScript设置")
        js_layout = QFormLayout(js_group)
        
        self.js_code = QTextEdit()
        self.js_code.setFixedHeight(150)
        self.js_code.setPlaceholderText("console.log('Hello World!');")
        self.js_code.setStyleSheet(self.get_input_style())
        js_layout.addRow("JavaScript代码:", self.js_code)
        
        self.return_variable = QLineEdit()
        self.return_variable.setPlaceholderText("保存返回值的变量名")
        self.return_variable.setStyleSheet(self.get_input_style())
        js_layout.addRow("返回值保存至:", self.return_variable)
        
        parent_layout.addWidget(js_group)
        
    def create_keyboard_config(self, parent_layout):
        """创建键盘操作配置"""
        keyboard_group = QGroupBox("键盘设置")
        keyboard_layout = QFormLayout(keyboard_group)

        # 支持多种操作名称：键盘按键、keyboard等
        if self.operation_name in ["键盘按键", "keyboard"]:
            self.key_type = QComboBox()
            self.key_type.addItems([
                "退格键", "Tab键", "回车键", "空格键", "Esc键", "删除键",
                "方向上键", "方向下键", "方向左键", "方向右键"
            ])
            self.key_type.setStyleSheet(self.get_input_style())
            keyboard_layout.addRow("按键类型:", self.key_type)

            # 添加延迟设置
            self.keyboard_delay = QSpinBox()
            self.keyboard_delay.setMinimum(0)
            self.keyboard_delay.setMaximum(5000)
            self.keyboard_delay.setValue(100)
            self.keyboard_delay.setSuffix(" 毫秒")
            self.keyboard_delay.setStyleSheet(self.get_input_style())
            keyboard_layout.addRow("按键延迟:", self.keyboard_delay)
        else:  # 组合键
            self.combo_key = QComboBox()
            self.combo_key.addItems(["Ctrl+A", "Ctrl+C", "Ctrl+V", "Ctrl+R"])
            self.combo_key.setStyleSheet(self.get_input_style())
            keyboard_layout.addRow("组合键:", self.combo_key)

        parent_layout.addWidget(keyboard_group)

    def create_click_element_config(self, parent_layout):
        """创建点击元素配置 - 完全按照AdsPower原版"""
        click_group = QGroupBox("点击元素设置")
        click_layout = QFormLayout(click_group)

        # 选择器类型
        self.click_selector_type = QComboBox()
        self.click_selector_type.addItems(["Selector", "XPath", "文本"])
        self.click_selector_type.setStyleSheet(self.get_input_style())
        click_layout.addRow("选择器类型:", self.click_selector_type)

        # 元素选择器
        self.click_selector = QLineEdit()
        self.click_selector.setPlaceholderText("请输入元素选择器，比如 #email input")
        self.click_selector.setStyleSheet(self.get_input_style())
        click_layout.addRow("元素选择器:", self.click_selector)

        # 使用变量按钮
        use_var_btn = QPushButton("使用变量")
        use_var_btn.setStyleSheet("color: #1890ff; border: none; text-decoration: underline;")
        click_layout.addRow("", use_var_btn)

        # 点击类型
        self.click_type = QComboBox()
        self.click_type.addItems(["鼠标左键", "鼠标中键", "鼠标右键"])
        self.click_type.setStyleSheet(self.get_input_style())
        click_layout.addRow("点击类型:", self.click_type)

        # 按键类型
        self.click_action = QComboBox()
        self.click_action.addItems(["单击", "双击"])
        self.click_action.setStyleSheet(self.get_input_style())
        click_layout.addRow("按键类型:", self.click_action)

        # 元素顺序
        self.click_element_order = QSpinBox()
        self.click_element_order.setMinimum(1)
        self.click_element_order.setValue(1)
        self.click_element_order.setStyleSheet(self.get_input_style())
        click_layout.addRow("元素顺序:", self.click_element_order)

        # 说明
        self.click_description = QLineEdit()
        self.click_description.setPlaceholderText("选填")
        self.click_description.setStyleSheet(self.get_input_style())
        click_layout.addRow("说明:", self.click_description)

        parent_layout.addWidget(click_group)

    def create_input_content_config(self, parent_layout):
        """创建输入内容配置 - 完全按照AdsPower原版"""
        input_group = QGroupBox("输入内容设置")
        input_layout = QFormLayout(input_group)

        # 选择器类型
        self.input_selector_type = QComboBox()
        self.input_selector_type.addItems(["Selector", "XPath", "文本"])
        self.input_selector_type.setStyleSheet(self.get_input_style())
        input_layout.addRow("选择器类型:", self.input_selector_type)

        # 元素选择器
        self.input_selector = QLineEdit()
        self.input_selector.setPlaceholderText("请输入元素选择器，比如 #email input")
        self.input_selector.setStyleSheet(self.get_input_style())
        input_layout.addRow("元素选择器:", self.input_selector)

        # 使用变量按钮
        use_var_btn = QPushButton("使用变量")
        use_var_btn.setStyleSheet("color: #1890ff; border: none; text-decoration: underline;")
        input_layout.addRow("", use_var_btn)

        # 输入内容
        self.input_content = QTextEdit()
        self.input_content.setFixedHeight(80)
        self.input_content.setPlaceholderText("请输入要填写的内容")
        self.input_content.setStyleSheet(self.get_input_style())
        input_layout.addRow("输入内容:", self.input_content)

        # 输入方式
        self.input_method = QComboBox()
        self.input_method.addItems(["覆盖", "追加"])
        self.input_method.setStyleSheet(self.get_input_style())
        input_layout.addRow("输入方式:", self.input_method)

        # 输入间隔
        self.input_interval = QSpinBox()
        self.input_interval.setMinimum(0)
        self.input_interval.setMaximum(5000)
        self.input_interval.setValue(100)
        self.input_interval.setSuffix(" 毫秒")
        self.input_interval.setStyleSheet(self.get_input_style())
        input_layout.addRow("输入间隔:", self.input_interval)

        # 元素顺序
        self.input_element_order = QSpinBox()
        self.input_element_order.setMinimum(1)
        self.input_element_order.setValue(1)
        self.input_element_order.setStyleSheet(self.get_input_style())
        input_layout.addRow("元素顺序:", self.input_element_order)

        # 说明
        self.input_description = QLineEdit()
        self.input_description.setPlaceholderText("选填")
        self.input_description.setStyleSheet(self.get_input_style())
        input_layout.addRow("说明:", self.input_description)

        parent_layout.addWidget(input_group)

    def create_upload_file_config(self, parent_layout):
        """创建上传附件配置 - 完全按照AdsPower原版"""
        upload_group = QGroupBox("上传附件设置")
        upload_layout = QFormLayout(upload_group)

        # 选择器类型
        self.upload_selector_type = QComboBox()
        self.upload_selector_type.addItems(["Selector", "XPath", "文本"])
        self.upload_selector_type.setStyleSheet(self.get_input_style())
        upload_layout.addRow("选择器类型:", self.upload_selector_type)

        # 元素选择器
        self.upload_selector = QLineEdit()
        self.upload_selector.setPlaceholderText("请输入元素选择器，比如 #email input")
        self.upload_selector.setStyleSheet(self.get_input_style())
        upload_layout.addRow("元素选择器:", self.upload_selector)

        # 使用变量按钮
        use_var_btn = QPushButton("使用变量")
        use_var_btn.setStyleSheet("color: #1890ff; border: none; text-decoration: underline;")
        upload_layout.addRow("", use_var_btn)

        # 附件类型
        self.upload_type = QComboBox()
        self.upload_type.addItems(["本地文件", "文件夹文件随机", "网络URL"])
        self.upload_type.setStyleSheet(self.get_input_style())
        upload_layout.addRow("附件类型:", self.upload_type)

        # 文件路径
        self.upload_file_path = QLineEdit()
        self.upload_file_path.setPlaceholderText("请输入文件路径")
        self.upload_file_path.setStyleSheet(self.get_input_style())
        upload_layout.addRow("文件路径:", self.upload_file_path)

        # 元素顺序
        self.upload_element_order = QSpinBox()
        self.upload_element_order.setMinimum(1)
        self.upload_element_order.setValue(1)
        self.upload_element_order.setStyleSheet(self.get_input_style())
        upload_layout.addRow("元素顺序:", self.upload_element_order)

        # 说明
        self.upload_description = QLineEdit()
        self.upload_description.setPlaceholderText("选填")
        self.upload_description.setStyleSheet(self.get_input_style())
        upload_layout.addRow("说明:", self.upload_description)

        parent_layout.addWidget(upload_group)

    # ==================== 页面操作配置方法 ====================

    def create_new_tab_config(self, parent_layout):
        """创建新建标签页配置 - 完全按照AdsPower原版"""
        if self.operation_name == "新建标签":
            # AdsPower原版：新建标签是直接执行，只有切换选项
            tab_group = QGroupBox("新建标签设置")
            tab_layout = QFormLayout(tab_group)

            # 只有切换到新标签选项
            self.switch_to_new = QCheckBox("切换到新标签")
            self.switch_to_new.setChecked(True)
            tab_layout.addRow("", self.switch_to_new)

            # 添加说明文字，与AdsPower原版一致
            info_label = QLabel("创建一个新的空白标签页")
            info_label.setStyleSheet("color: #666; font-size: 12px;")
            tab_layout.addRow("说明:", info_label)

        else:
            # 新建标签页操作 - 包含URL输入（保留原有功能）
            tab_group = QGroupBox("新建标签页设置")
            tab_layout = QFormLayout(tab_group)

            self.tab_url = QLineEdit()
            self.tab_url.setPlaceholderText("https://www.example.com (可选)")
            self.tab_url.setStyleSheet(self.get_input_style())
            tab_layout.addRow("打开URL:", self.tab_url)

            self.switch_to_new = QCheckBox("切换到新标签页")
            self.switch_to_new.setChecked(True)
            tab_layout.addRow("", self.switch_to_new)

        parent_layout.addWidget(tab_group)

    def create_goto_url_config(self, parent_layout):
        """创建访问网站配置 - 完全按照AdsPower原版"""
        url_group = QGroupBox("网站设置")
        url_layout = QFormLayout(url_group)

        # AdsPower原版：访问URL输入框
        self.goto_url = QLineEdit()
        self.goto_url.setPlaceholderText("请输入正确的URL")
        self.goto_url.setStyleSheet(self.get_input_style())
        url_layout.addRow("访问URL:", self.goto_url)

        # AdsPower原版：使用变量按钮（暂时用文本显示）
        use_var_label = QLabel("使用变量")
        use_var_label.setStyleSheet("color: #1890ff; cursor: pointer; text-decoration: underline;")
        url_layout.addRow("", use_var_label)

        # AdsPower原版：超时等待设置
        self.timeout_seconds = QSpinBox()
        self.timeout_seconds.setMinimum(1000)
        self.timeout_seconds.setMaximum(300000)
        self.timeout_seconds.setValue(30000)
        self.timeout_seconds.setSuffix(" 毫秒")
        self.timeout_seconds.setStyleSheet(self.get_input_style())
        url_layout.addRow("超时等待:", self.timeout_seconds)

        # AdsPower原版：说明文字
        desc_label = QLabel("1秒 = 1000毫秒")
        desc_label.setStyleSheet("color: #666; font-size: 12px;")
        url_layout.addRow("", desc_label)

        parent_layout.addWidget(url_group)

    def create_wait_time_config(self, parent_layout):
        """创建等待时间配置"""
        wait_group = QGroupBox("等待时间设置")
        wait_layout = QFormLayout(wait_group)

        self.wait_type = QComboBox()
        self.wait_type.addItems(["固定时间", "随机时间"])
        self.wait_type.setStyleSheet(self.get_input_style())
        wait_layout.addRow("等待类型:", self.wait_type)

        self.wait_min = QSpinBox()
        self.wait_min.setMinimum(1)
        self.wait_min.setMaximum(300)
        self.wait_min.setValue(3)
        self.wait_min.setSuffix(" 秒")
        self.wait_min.setStyleSheet(self.get_input_style())
        wait_layout.addRow("最小时间:", self.wait_min)

        self.wait_max = QSpinBox()
        self.wait_max.setMinimum(1)
        self.wait_max.setMaximum(300)
        self.wait_max.setValue(5)
        self.wait_max.setSuffix(" 秒")
        self.wait_max.setStyleSheet(self.get_input_style())
        wait_layout.addRow("最大时间:", self.wait_max)

        parent_layout.addWidget(wait_group)

    def create_scroll_page_config(self, parent_layout):
        """创建滚动页面配置"""
        scroll_group = QGroupBox("滚动设置")
        scroll_layout = QFormLayout(scroll_group)

        self.scroll_range_type = QComboBox()
        self.scroll_range_type.addItems(["窗口", "元素"])
        self.scroll_range_type.setStyleSheet(self.get_input_style())
        scroll_layout.addRow("滚动范围:", self.scroll_range_type)

        self.scroll_selector = QLineEdit()
        self.scroll_selector.setPlaceholderText("CSS选择器 (元素滚动时使用)")
        self.scroll_selector.setStyleSheet(self.get_input_style())
        scroll_layout.addRow("元素选择器:", self.scroll_selector)

        self.scroll_distance = QSpinBox()
        self.scroll_distance.setMinimum(0)
        self.scroll_distance.setMaximum(10000)
        self.scroll_distance.setValue(500)
        self.scroll_distance.setSuffix(" 像素")
        self.scroll_distance.setStyleSheet(self.get_input_style())
        scroll_layout.addRow("滚动距离:", self.scroll_distance)

        self.scroll_type_detail = QComboBox()
        self.scroll_type_detail.addItems(["平滑", "瞬间"])
        self.scroll_type_detail.setStyleSheet(self.get_input_style())
        scroll_layout.addRow("滚动类型:", self.scroll_type_detail)

        self.scroll_position_type = QComboBox()
        self.scroll_position_type.addItems(["顶部", "底部", "位置"])
        self.scroll_position_type.setStyleSheet(self.get_input_style())
        scroll_layout.addRow("滚动位置:", self.scroll_position_type)

        parent_layout.addWidget(scroll_group)

    def create_click_config(self, parent_layout):
        """创建点击配置"""
        click_group = QGroupBox("点击设置")
        click_layout = QFormLayout(click_group)

        self.click_selector = QLineEdit()
        self.click_selector.setPlaceholderText('//button[@aria-label="Like"]')
        self.click_selector.setStyleSheet(self.get_input_style())
        click_layout.addRow("元素选择器:", self.click_selector)

        self.selector_type = QComboBox()
        self.selector_type.addItems(["CSS", "XPath"])
        self.selector_type.setStyleSheet(self.get_input_style())
        click_layout.addRow("选择器类型:", self.selector_type)

        self.click_button = QComboBox()
        self.click_button.addItems(["左键", "右键", "中键"])
        self.click_button.setStyleSheet(self.get_input_style())
        click_layout.addRow("鼠标按键:", self.click_button)

        self.click_count = QComboBox()
        self.click_count.addItems(["单击", "双击"])
        self.click_count.setStyleSheet(self.get_input_style())
        click_layout.addRow("点击次数:", self.click_count)

        self.element_index = QSpinBox()
        self.element_index.setMinimum(1)
        self.element_index.setValue(1)
        self.element_index.setStyleSheet(self.get_input_style())
        click_layout.addRow("元素序号:", self.element_index)

        parent_layout.addWidget(click_group)

    def create_hover_config(self, parent_layout):
        """创建悬停配置"""
        hover_group = QGroupBox("悬停设置")
        hover_layout = QFormLayout(hover_group)

        self.hover_selector = QLineEdit()
        self.hover_selector.setPlaceholderText('.menu-item')
        self.hover_selector.setStyleSheet(self.get_input_style())
        hover_layout.addRow("元素选择器:", self.hover_selector)

        self.hover_duration = QSpinBox()
        self.hover_duration.setMinimum(100)
        self.hover_duration.setMaximum(10000)
        self.hover_duration.setValue(1000)
        self.hover_duration.setSuffix(" 毫秒")
        self.hover_duration.setStyleSheet(self.get_input_style())
        hover_layout.addRow("悬停时长:", self.hover_duration)

        parent_layout.addWidget(hover_group)

    def create_page_navigation_config(self, parent_layout):
        """创建页面导航配置"""
        nav_group = QGroupBox("页面导航设置")
        nav_layout = QFormLayout(nav_group)

        operation_desc = {
            "页面后退": "返回到上一个页面",
            "页面前进": "前进到下一个页面",
            "刷新页面": "重新加载当前页面"
        }

        desc_label = QLabel(operation_desc.get(self.operation_name, "页面导航操作"))
        desc_label.setStyleSheet("color: #666666; font-size: 14px;")
        nav_layout.addRow("操作说明:", desc_label)

        self.nav_wait_load = QCheckBox("等待页面加载完成")
        self.nav_wait_load.setChecked(True)
        nav_layout.addRow("", self.nav_wait_load)

        parent_layout.addWidget(nav_group)

    def create_tab_management_config(self, parent_layout):
        """创建标签页管理配置"""
        tab_group = QGroupBox("标签页管理设置")
        tab_layout = QFormLayout(tab_group)

        if self.operation_name == "关闭标签页":
            self.close_type = QComboBox()
            self.close_type.addItems(["当前标签页", "指定标签页", "其他标签页"])
            self.close_type.setStyleSheet(self.get_input_style())
            tab_layout.addRow("关闭类型:", self.close_type)

            self.tab_index = QSpinBox()
            self.tab_index.setMinimum(1)
            self.tab_index.setValue(1)
            self.tab_index.setStyleSheet(self.get_input_style())
            tab_layout.addRow("标签页序号:", self.tab_index)

        elif self.operation_name == "切换标签页":
            self.switch_type = QComboBox()
            self.switch_type.addItems(["按序号", "按标题", "按URL"])
            self.switch_type.setStyleSheet(self.get_input_style())
            tab_layout.addRow("切换方式:", self.switch_type)

            self.switch_target = QLineEdit()
            self.switch_target.setPlaceholderText("标签页序号/标题/URL")
            self.switch_target.setStyleSheet(self.get_input_style())
            tab_layout.addRow("目标标签页:", self.switch_target)

        parent_layout.addWidget(tab_group)

    def create_close_tab_config(self, parent_layout):
        """创建关闭标签配置 - 完全按照AdsPower原版"""
        tab_group = QGroupBox("关闭标签设置")
        tab_layout = QFormLayout(tab_group)

        # AdsPower原版：关闭类型下拉框
        self.close_type = QComboBox()
        self.close_type.addItems(["当前标签页"])  # AdsPower原版默认选项
        self.close_type.setStyleSheet(self.get_input_style())
        tab_layout.addRow("关闭类型:", self.close_type)

        # AdsPower原版：标签页序号输入框
        self.tab_index = QSpinBox()
        self.tab_index.setMinimum(1)
        self.tab_index.setMaximum(999)
        self.tab_index.setValue(1)
        self.tab_index.setStyleSheet(self.get_input_style())
        tab_layout.addRow("标签页序号:", self.tab_index)

        parent_layout.addWidget(tab_group)

    def create_close_other_tabs_config(self, parent_layout):
        """创建关闭其他标签配置 - 完全按照AdsPower原版"""
        tab_group = QGroupBox("关闭其他标签设置")
        tab_layout = QFormLayout(tab_group)

        # AdsPower原版：只有操作说明，无其他配置
        desc_label = QLabel("关闭除当前标签页外的所有其他标签页")
        desc_label.setStyleSheet("color: #666666; font-size: 14px;")
        tab_layout.addRow("操作说明:", desc_label)

        parent_layout.addWidget(tab_group)

    def create_switch_tab_config(self, parent_layout):
        """创建切换标签配置 - 完全按照AdsPower原版"""
        tab_group = QGroupBox("切换标签设置")
        tab_layout = QFormLayout(tab_group)

        # AdsPower原版：切换方式下拉框
        self.switch_type = QComboBox()
        self.switch_type.addItems(["按序号"])  # AdsPower原版默认选项
        self.switch_type.setStyleSheet(self.get_input_style())
        tab_layout.addRow("切换方式:", self.switch_type)

        # AdsPower原版：目标标签页输入框
        self.switch_target = QLineEdit()
        self.switch_target.setPlaceholderText("标签页序号/标题/URL")
        self.switch_target.setStyleSheet(self.get_input_style())
        tab_layout.addRow("目标标签页:", self.switch_target)

        parent_layout.addWidget(tab_group)

    def create_page_screenshot_config(self, parent_layout):
        """创建页面截图配置"""
        screenshot_group = QGroupBox("页面截图设置")
        screenshot_layout = QFormLayout(screenshot_group)

        self.screenshot_name = QLineEdit()
        self.screenshot_name.setPlaceholderText("截图文件名（可选）")
        self.screenshot_name.setStyleSheet(self.get_input_style())
        screenshot_layout.addRow("截图名称:", self.screenshot_name)

        self.full_screen = QCheckBox("截取整个网页长图")
        screenshot_layout.addRow("截全屏:", self.full_screen)

        self.image_format = QComboBox()
        self.image_format.addItems(["png", "jpeg"])
        self.image_format.setStyleSheet(self.get_input_style())
        screenshot_layout.addRow("图片格式:", self.image_format)

        parent_layout.addWidget(screenshot_group)

    def create_dropdown_config(self, parent_layout):
        """创建下拉选择器配置"""
        dropdown_group = QGroupBox("下拉选择器设置")
        dropdown_layout = QFormLayout(dropdown_group)

        self.dropdown_selector = QLineEdit()
        self.dropdown_selector.setPlaceholderText("#pet-select")
        self.dropdown_selector.setStyleSheet(self.get_input_style())
        dropdown_layout.addRow("元素选择器:", self.dropdown_selector)

        self.dropdown_element_order = QSpinBox()
        self.dropdown_element_order.setMinimum(1)
        self.dropdown_element_order.setValue(1)
        self.dropdown_element_order.setStyleSheet(self.get_input_style())
        dropdown_layout.addRow("元素顺序:", self.dropdown_element_order)

        self.select_value = QLineEdit()
        self.select_value.setPlaceholderText("选择的值（value属性）")
        self.select_value.setStyleSheet(self.get_input_style())
        dropdown_layout.addRow("选择的值:", self.select_value)

        parent_layout.addWidget(dropdown_group)

    def create_focus_config(self, parent_layout):
        """创建元素聚焦配置"""
        focus_group = QGroupBox("元素聚焦设置")
        focus_layout = QFormLayout(focus_group)

        self.focus_selector = QLineEdit()
        self.focus_selector.setPlaceholderText("#email_input")
        self.focus_selector.setStyleSheet(self.get_input_style())
        focus_layout.addRow("元素选择器:", self.focus_selector)

        self.focus_element_order = QSpinBox()
        self.focus_element_order.setMinimum(1)
        self.focus_element_order.setValue(1)
        self.focus_element_order.setStyleSheet(self.get_input_style())
        focus_layout.addRow("元素顺序:", self.focus_element_order)

        parent_layout.addWidget(focus_group)

    def create_input_config(self, parent_layout):
        """创建输入内容配置"""
        input_group = QGroupBox("输入内容设置")
        input_layout = QFormLayout(input_group)

        self.input_selector = QLineEdit()
        self.input_selector.setPlaceholderText('input[type="text"]')
        self.input_selector.setStyleSheet(self.get_input_style())
        input_layout.addRow("元素选择器:", self.input_selector)

        self.input_element_order = QSpinBox()
        self.input_element_order.setMinimum(1)
        self.input_element_order.setValue(1)
        self.input_element_order.setStyleSheet(self.get_input_style())
        input_layout.addRow("元素顺序:", self.input_element_order)

        self.input_content = QTextEdit()
        self.input_content.setFixedHeight(100)
        self.input_content.setPlaceholderText("输入要填写的内容")
        self.input_content.setStyleSheet(self.get_input_style())
        input_layout.addRow("内容:", self.input_content)

        self.input_interval = QSpinBox()
        self.input_interval.setMinimum(0)
        self.input_interval.setMaximum(5000)
        self.input_interval.setValue(100)
        self.input_interval.setSuffix(" 毫秒")
        self.input_interval.setStyleSheet(self.get_input_style())
        input_layout.addRow("输入间隔:", self.input_interval)

        self.clear_first = QCheckBox("清除现有内容")
        self.clear_first.setChecked(True)
        input_layout.addRow("", self.clear_first)

        parent_layout.addWidget(input_group)

    # ==================== 键盘操作配置方法 ====================

    def create_keyboard_key_config(self, parent_layout):
        """创建键盘按键配置"""
        keyboard_group = QGroupBox("键盘按键设置")
        keyboard_layout = QFormLayout(keyboard_group)

        self.key_type = QComboBox()
        self.key_type.addItems([
            "退格键", "Tab键", "回车键", "空格键", "Esc键", "删除键",
            "方向上键", "方向下键", "方向左键", "方向右键"
        ])
        self.key_type.setStyleSheet(self.get_input_style())
        keyboard_layout.addRow("按键类型:", self.key_type)

        self.keyboard_delay = QSpinBox()
        self.keyboard_delay.setMinimum(0)
        self.keyboard_delay.setMaximum(5000)
        self.keyboard_delay.setValue(100)
        self.keyboard_delay.setSuffix(" 毫秒")
        self.keyboard_delay.setStyleSheet(self.get_input_style())
        keyboard_layout.addRow("按键延迟:", self.keyboard_delay)

        parent_layout.addWidget(keyboard_group)

    def create_keyboard_combo_config(self, parent_layout):
        """创建组合键配置"""
        keyboard_group = QGroupBox("组合键设置")
        keyboard_layout = QFormLayout(keyboard_group)

        self.combo_key = QComboBox()
        self.combo_key.addItems([
            "Ctrl+A", "Ctrl+C", "Ctrl+V", "Ctrl+R", "Ctrl+Z", "Ctrl+Y",
            "Ctrl+S", "Ctrl+F", "Ctrl+T", "Ctrl+W", "Ctrl+Tab",
            "Alt+Tab", "Shift+Tab"
        ])
        self.combo_key.setStyleSheet(self.get_input_style())
        keyboard_layout.addRow("组合键:", self.combo_key)

        self.combo_delay = QSpinBox()
        self.combo_delay.setMinimum(0)
        self.combo_delay.setMaximum(5000)
        self.combo_delay.setValue(100)
        self.combo_delay.setSuffix(" 毫秒")
        self.combo_delay.setStyleSheet(self.get_input_style())
        keyboard_layout.addRow("按键延迟:", self.combo_delay)

        parent_layout.addWidget(keyboard_group)

    # ==================== 等待操作配置方法 ====================

    def create_wait_request_config(self, parent_layout):
        """创建等待请求完成配置"""
        wait_group = QGroupBox("等待请求设置")
        wait_layout = QFormLayout(wait_group)

        self.wait_request_type = QComboBox()
        self.wait_request_type.addItems(["网络请求完成", "特定请求"])
        self.wait_request_type.setStyleSheet(self.get_input_style())
        wait_layout.addRow("等待类型:", self.wait_request_type)

        self.request_url = QLineEdit()
        self.request_url.setPlaceholderText("特定请求URL（可选）")
        self.request_url.setStyleSheet(self.get_input_style())
        wait_layout.addRow("请求URL:", self.request_url)

        self.request_timeout = QSpinBox()
        self.request_timeout.setMinimum(1)
        self.request_timeout.setMaximum(300)
        self.request_timeout.setValue(30)
        self.request_timeout.setSuffix(" 秒")
        self.request_timeout.setStyleSheet(self.get_input_style())
        wait_layout.addRow("超时时间:", self.request_timeout)

        parent_layout.addWidget(wait_group)

    def create_keyboard_tab_config(self, parent_layout):
        """创建键盘标签页操作配置"""
        keyboard_group = QGroupBox("键盘操作设置")
        keyboard_layout = QFormLayout(keyboard_group)

        operation_keys = {
            "新建标签页": "Ctrl+T",
            "关闭标签页": "Ctrl+W",
            "切换标签页": "Ctrl+Tab"
        }

        key_label = QLabel(f"快捷键: {operation_keys.get(self.operation_name, 'N/A')}")
        key_label.setStyleSheet("color: #666666; font-size: 14px;")
        keyboard_layout.addRow("操作快捷键:", key_label)

        self.keyboard_delay = QSpinBox()
        self.keyboard_delay.setMinimum(0)
        self.keyboard_delay.setMaximum(5000)
        self.keyboard_delay.setValue(100)
        self.keyboard_delay.setSuffix(" 毫秒")
        self.keyboard_delay.setStyleSheet(self.get_input_style())
        keyboard_layout.addRow("按键延迟:", self.keyboard_delay)

        parent_layout.addWidget(keyboard_group)

    # ==================== 等待操作配置方法 ====================

    def create_wait_element_config(self, parent_layout):
        """创建等待元素配置"""
        wait_group = QGroupBox("等待元素设置")
        wait_layout = QFormLayout(wait_group)

        self.wait_element_selector = QLineEdit()
        self.wait_element_selector.setPlaceholderText('#submit-button')
        self.wait_element_selector.setStyleSheet(self.get_input_style())
        wait_layout.addRow("元素选择器:", self.wait_element_selector)

        self.wait_condition = QComboBox()
        self.wait_condition.addItems(["出现", "消失", "可见", "隐藏", "可点击"])
        self.wait_condition.setStyleSheet(self.get_input_style())
        wait_layout.addRow("等待条件:", self.wait_condition)

        self.wait_timeout = QSpinBox()
        self.wait_timeout.setMinimum(1)
        self.wait_timeout.setMaximum(300)
        self.wait_timeout.setValue(30)
        self.wait_timeout.setSuffix(" 秒")
        self.wait_timeout.setStyleSheet(self.get_input_style())
        wait_layout.addRow("超时时间:", self.wait_timeout)

        parent_layout.addWidget(wait_group)

    def create_wait_page_config(self, parent_layout):
        """创建等待页面配置"""
        wait_group = QGroupBox("等待页面设置")
        wait_layout = QFormLayout(wait_group)

        self.page_wait_type = QComboBox()
        self.page_wait_type.addItems(["页面加载完成", "DOM加载完成", "网络请求完成"])
        self.page_wait_type.setStyleSheet(self.get_input_style())
        wait_layout.addRow("等待类型:", self.page_wait_type)

        self.page_timeout = QSpinBox()
        self.page_timeout.setMinimum(5)
        self.page_timeout.setMaximum(300)
        self.page_timeout.setValue(30)
        self.page_timeout.setSuffix(" 秒")
        self.page_timeout.setStyleSheet(self.get_input_style())
        wait_layout.addRow("超时时间:", self.page_timeout)

        parent_layout.addWidget(wait_group)

    def create_wait_popup_config(self, parent_layout):
        """创建等待弹窗配置"""
        wait_group = QGroupBox("等待弹窗设置")
        wait_layout = QFormLayout(wait_group)

        self.popup_type = QComboBox()
        self.popup_type.addItems(["Alert弹窗", "Confirm弹窗", "Prompt弹窗", "自定义弹窗"])
        self.popup_type.setStyleSheet(self.get_input_style())
        wait_layout.addRow("弹窗类型:", self.popup_type)

        self.popup_action = QComboBox()
        self.popup_action.addItems(["接受", "取消", "获取文本"])
        self.popup_action.setStyleSheet(self.get_input_style())
        wait_layout.addRow("处理方式:", self.popup_action)

        self.popup_timeout = QSpinBox()
        self.popup_timeout.setMinimum(1)
        self.popup_timeout.setMaximum(300)
        self.popup_timeout.setValue(10)
        self.popup_timeout.setSuffix(" 秒")
        self.popup_timeout.setStyleSheet(self.get_input_style())
        wait_layout.addRow("超时时间:", self.popup_timeout)

        parent_layout.addWidget(wait_group)

    # ==================== 获取数据配置方法 ====================

    def create_get_url_config(self, parent_layout):
        """创建获取URL配置"""
        url_group = QGroupBox("获取URL设置")
        url_layout = QFormLayout(url_group)

        self.url_type = QComboBox()
        self.url_type.addItems(["完整地址", "根地址", "参数值"])
        self.url_type.setStyleSheet(self.get_input_style())
        url_layout.addRow("URL类型:", self.url_type)

        self.param_name = QLineEdit()
        self.param_name.setPlaceholderText("参数名称（参数值类型时使用）")
        self.param_name.setStyleSheet(self.get_input_style())
        url_layout.addRow("参数名称:", self.param_name)

        self.url_save_variable = QLineEdit()
        self.url_save_variable.setPlaceholderText("current_url")
        self.url_save_variable.setStyleSheet(self.get_input_style())
        url_layout.addRow("保存到变量:", self.url_save_variable)

        parent_layout.addWidget(url_group)

    def create_get_clipboard_config(self, parent_layout):
        """创建获取粘贴板内容配置"""
        clipboard_group = QGroupBox("获取粘贴板设置")
        clipboard_layout = QFormLayout(clipboard_group)

        self.clipboard_save_variable = QLineEdit()
        self.clipboard_save_variable.setPlaceholderText("clipboard_content")
        self.clipboard_save_variable.setStyleSheet(self.get_input_style())
        clipboard_layout.addRow("保存到变量:", self.clipboard_save_variable)

        parent_layout.addWidget(clipboard_group)

    def create_get_focused_element_config(self, parent_layout):
        """创建获取当前焦点元素配置"""
        focused_group = QGroupBox("获取焦点元素设置")
        focused_layout = QFormLayout(focused_group)

        self.focused_save_variable = QLineEdit()
        self.focused_save_variable.setPlaceholderText("focused_element")
        self.focused_save_variable.setStyleSheet(self.get_input_style())
        focused_layout.addRow("保存到变量:", self.focused_save_variable)

        parent_layout.addWidget(focused_group)

    def create_save_to_file_config(self, parent_layout):
        """创建存到文件配置"""
        file_group = QGroupBox("存到文件设置")
        file_layout = QFormLayout(file_group)

        self.data_variable = QLineEdit()
        self.data_variable.setPlaceholderText("要保存的数据变量")
        self.data_variable.setStyleSheet(self.get_input_style())
        file_layout.addRow("数据变量:", self.data_variable)

        self.file_path = QLineEdit()
        self.file_path.setPlaceholderText("C:/data/output.txt")
        self.file_path.setStyleSheet(self.get_input_style())
        file_layout.addRow("文件路径:", self.file_path)

        self.file_encoding = QComboBox()
        self.file_encoding.addItems(["utf-8", "gbk", "ascii"])
        self.file_encoding.setStyleSheet(self.get_input_style())
        file_layout.addRow("文件编码:", self.file_encoding)

        self.append_mode = QCheckBox("追加模式")
        file_layout.addRow("", self.append_mode)

        parent_layout.addWidget(file_group)

    def create_save_to_excel_config(self, parent_layout):
        """创建存到Excel配置"""
        excel_group = QGroupBox("存到Excel设置")
        excel_layout = QFormLayout(excel_group)

        self.excel_data_variable = QLineEdit()
        self.excel_data_variable.setPlaceholderText("要保存的数据变量")
        self.excel_data_variable.setStyleSheet(self.get_input_style())
        excel_layout.addRow("数据变量:", self.excel_data_variable)

        self.excel_file_path = QLineEdit()
        self.excel_file_path.setPlaceholderText("C:/data/output.xlsx")
        self.excel_file_path.setStyleSheet(self.get_input_style())
        excel_layout.addRow("文件路径:", self.excel_file_path)

        self.excel_sheet_name = QLineEdit()
        self.excel_sheet_name.setPlaceholderText("Sheet1")
        self.excel_sheet_name.setStyleSheet(self.get_input_style())
        excel_layout.addRow("工作表名称:", self.excel_sheet_name)

        self.excel_start_row = QSpinBox()
        self.excel_start_row.setMinimum(1)
        self.excel_start_row.setValue(1)
        self.excel_start_row.setStyleSheet(self.get_input_style())
        excel_layout.addRow("起始行:", self.excel_start_row)

        self.excel_start_col = QSpinBox()
        self.excel_start_col.setMinimum(1)
        self.excel_start_col.setValue(1)
        self.excel_start_col.setStyleSheet(self.get_input_style())
        excel_layout.addRow("起始列:", self.excel_start_col)

        parent_layout.addWidget(excel_group)

    def create_download_file_config(self, parent_layout):
        """创建下载文件配置"""
        download_group = QGroupBox("下载文件设置")
        download_layout = QFormLayout(download_group)

        self.download_url = QLineEdit()
        self.download_url.setPlaceholderText("https://example.com/file.pdf")
        self.download_url.setStyleSheet(self.get_input_style())
        download_layout.addRow("下载URL:", self.download_url)

        self.download_save_path = QLineEdit()
        self.download_save_path.setPlaceholderText("保存路径（可选）")
        self.download_save_path.setStyleSheet(self.get_input_style())
        download_layout.addRow("保存路径:", self.download_save_path)

        self.download_timeout = QSpinBox()
        self.download_timeout.setMinimum(1)
        self.download_timeout.setMaximum(300)
        self.download_timeout.setValue(30)
        self.download_timeout.setSuffix(" 秒")
        self.download_timeout.setStyleSheet(self.get_input_style())
        download_layout.addRow("超时时间:", self.download_timeout)

        parent_layout.addWidget(download_group)

    def create_get_element_config(self, parent_layout):
        """创建获取元素配置"""
        get_group = QGroupBox("获取元素设置")
        get_layout = QFormLayout(get_group)

        self.get_element_selector = QLineEdit()
        self.get_element_selector.setPlaceholderText('.product-title')
        self.get_element_selector.setStyleSheet(self.get_input_style())
        get_layout.addRow("元素选择器:", self.get_element_selector)

        self.extract_type = QComboBox()
        self.extract_type.addItems(["文本内容", "属性值", "HTML内容", "外部HTML"])
        self.extract_type.setStyleSheet(self.get_input_style())
        get_layout.addRow("提取类型:", self.extract_type)

        self.attribute_name = QLineEdit()
        self.attribute_name.setPlaceholderText("href, src, data-id 等")
        self.attribute_name.setStyleSheet(self.get_input_style())
        get_layout.addRow("属性名称:", self.attribute_name)

        self.save_variable = QLineEdit()
        self.save_variable.setPlaceholderText("product_title")
        self.save_variable.setStyleSheet(self.get_input_style())
        get_layout.addRow("保存到变量:", self.save_variable)

        parent_layout.addWidget(get_group)

    def create_get_page_config(self, parent_layout):
        """创建获取页面配置"""
        get_group = QGroupBox("获取页面设置")
        get_layout = QFormLayout(get_group)

        self.page_info_type = QComboBox()
        self.page_info_type.addItems(["页面标题", "页面URL", "页面源码", "页面截图"])
        self.page_info_type.setStyleSheet(self.get_input_style())
        get_layout.addRow("获取类型:", self.page_info_type)

        self.page_save_variable = QLineEdit()
        self.page_save_variable.setPlaceholderText("page_title")
        self.page_save_variable.setStyleSheet(self.get_input_style())
        get_layout.addRow("保存到变量:", self.page_save_variable)

        parent_layout.addWidget(get_group)

    def create_get_popup_config(self, parent_layout):
        """创建获取弹窗配置"""
        get_group = QGroupBox("获取弹窗设置")
        get_layout = QFormLayout(get_group)

        self.popup_get_type = QComboBox()
        self.popup_get_type.addItems(["弹窗文本", "弹窗类型", "弹窗存在状态"])
        self.popup_get_type.setStyleSheet(self.get_input_style())
        get_layout.addRow("获取类型:", self.popup_get_type)

        self.popup_save_variable = QLineEdit()
        self.popup_save_variable.setPlaceholderText("popup_text")
        self.popup_save_variable.setStyleSheet(self.get_input_style())
        get_layout.addRow("保存到变量:", self.popup_save_variable)

        parent_layout.addWidget(get_group)

    def create_get_cookie_config(self, parent_layout):
        """创建获取Cookie配置"""
        get_group = QGroupBox("获取Cookie设置")
        get_layout = QFormLayout(get_group)

        self.cookie_type = QComboBox()
        self.cookie_type.addItems(["所有Cookie", "指定Cookie", "Cookie数量"])
        self.cookie_type.setStyleSheet(self.get_input_style())
        get_layout.addRow("获取类型:", self.cookie_type)

        self.cookie_name = QLineEdit()
        self.cookie_name.setPlaceholderText("session_id")
        self.cookie_name.setStyleSheet(self.get_input_style())
        get_layout.addRow("Cookie名称:", self.cookie_name)

        self.cookie_save_variable = QLineEdit()
        self.cookie_save_variable.setPlaceholderText("cookies")
        self.cookie_save_variable.setStyleSheet(self.get_input_style())
        get_layout.addRow("保存到变量:", self.cookie_save_variable)

        parent_layout.addWidget(get_group)

    def create_get_env_config(self, parent_layout):
        """创建获取环境信息配置"""
        get_group = QGroupBox("获取环境信息设置")
        get_layout = QFormLayout(get_group)

        self.env_info_type = QComboBox()
        self.env_info_type.addItems(["环境编号", "环境名称", "代理信息", "User-Agent", "分辨率"])
        self.env_info_type.setStyleSheet(self.get_input_style())
        get_layout.addRow("信息类型:", self.env_info_type)

        self.env_save_variable = QLineEdit()
        self.env_save_variable.setPlaceholderText("env_id")
        self.env_save_variable.setStyleSheet(self.get_input_style())
        get_layout.addRow("保存到变量:", self.env_save_variable)

        parent_layout.addWidget(get_group)

    def create_import_excel_config(self, parent_layout):
        """创建导入Excel配置"""
        import_group = QGroupBox("导入Excel设置")
        import_layout = QFormLayout(import_group)

        self.excel_path = QLineEdit()
        self.excel_path.setPlaceholderText("C:/data/accounts.xlsx")
        self.excel_path.setStyleSheet(self.get_input_style())
        import_layout.addRow("Excel文件路径:", self.excel_path)

        self.sheet_name = QLineEdit()
        self.sheet_name.setPlaceholderText("Sheet1")
        self.sheet_name.setStyleSheet(self.get_input_style())
        import_layout.addRow("工作表名称:", self.sheet_name)

        self.start_row = QSpinBox()
        self.start_row.setMinimum(1)
        self.start_row.setValue(2)
        self.start_row.setStyleSheet(self.get_input_style())
        import_layout.addRow("起始行:", self.start_row)

        self.excel_save_variable = QLineEdit()
        self.excel_save_variable.setPlaceholderText("excel_data")
        self.excel_save_variable.setStyleSheet(self.get_input_style())
        import_layout.addRow("保存到变量:", self.excel_save_variable)

        parent_layout.addWidget(import_group)

    def create_import_txt_config(self, parent_layout):
        """创建导入txt配置"""
        import_group = QGroupBox("导入txt设置")
        import_layout = QFormLayout(import_group)

        self.txt_path = QLineEdit()
        self.txt_path.setPlaceholderText("C:/data/keywords.txt")
        self.txt_path.setStyleSheet(self.get_input_style())
        import_layout.addRow("txt文件路径:", self.txt_path)

        self.txt_encoding = QComboBox()
        self.txt_encoding.addItems(["UTF-8", "GBK", "ASCII"])
        self.txt_encoding.setStyleSheet(self.get_input_style())
        import_layout.addRow("文件编码:", self.txt_encoding)

        self.txt_delimiter = QLineEdit()
        self.txt_delimiter.setPlaceholderText("\\n (换行符)")
        self.txt_delimiter.setStyleSheet(self.get_input_style())
        import_layout.addRow("分隔符:", self.txt_delimiter)

        self.txt_save_variable = QLineEdit()
        self.txt_save_variable.setPlaceholderText("txt_data")
        self.txt_save_variable.setStyleSheet(self.get_input_style())
        import_layout.addRow("保存到变量:", self.txt_save_variable)

        parent_layout.addWidget(import_group)

    def create_get_email_config(self, parent_layout):
        """创建获取邮件配置"""
        email_group = QGroupBox("获取邮件设置")
        email_layout = QFormLayout(email_group)

        self.imap_server = QLineEdit()
        self.imap_server.setPlaceholderText("imap.gmail.com")
        self.imap_server.setStyleSheet(self.get_input_style())
        email_layout.addRow("IMAP服务器:", self.imap_server)

        self.email_username = QLineEdit()
        self.email_username.setPlaceholderText("your_email@gmail.com")
        self.email_username.setStyleSheet(self.get_input_style())
        email_layout.addRow("用户名:", self.email_username)

        self.email_password = QLineEdit()
        self.email_password.setEchoMode(QLineEdit.Password)
        self.email_password.setPlaceholderText("邮箱密码或应用密码")
        self.email_password.setStyleSheet(self.get_input_style())
        email_layout.addRow("密码:", self.email_password)

        self.email_folder = QLineEdit()
        self.email_folder.setPlaceholderText("INBOX")
        self.email_folder.setStyleSheet(self.get_input_style())
        email_layout.addRow("邮件文件夹:", self.email_folder)

        self.email_count = QSpinBox()
        self.email_count.setMinimum(1)
        self.email_count.setMaximum(100)
        self.email_count.setValue(1)
        self.email_count.setStyleSheet(self.get_input_style())
        email_layout.addRow("获取数量:", self.email_count)

        self.email_save_variable = QLineEdit()
        self.email_save_variable.setPlaceholderText("emails")
        self.email_save_variable.setStyleSheet(self.get_input_style())
        email_layout.addRow("保存到变量:", self.email_save_variable)

        parent_layout.addWidget(email_group)

    def create_get_totp_config(self, parent_layout):
        """创建身份验证密码配置"""
        totp_group = QGroupBox("身份验证密码设置")
        totp_layout = QFormLayout(totp_group)

        self.secret_key = QLineEdit()
        self.secret_key.setPlaceholderText("TOTP密钥")
        self.secret_key.setStyleSheet(self.get_input_style())
        totp_layout.addRow("密钥:", self.secret_key)

        self.totp_save_variable = QLineEdit()
        self.totp_save_variable.setPlaceholderText("totp_code")
        self.totp_save_variable.setStyleSheet(self.get_input_style())
        totp_layout.addRow("保存到变量:", self.totp_save_variable)

        parent_layout.addWidget(totp_group)

    def create_listen_request_trigger_config(self, parent_layout):
        """创建监听请求触发配置"""
        listen_group = QGroupBox("监听请求触发设置")
        listen_layout = QFormLayout(listen_group)

        self.trigger_url_pattern = QLineEdit()
        self.trigger_url_pattern.setPlaceholderText("URL匹配模式（可选）")
        self.trigger_url_pattern.setStyleSheet(self.get_input_style())
        listen_layout.addRow("URL模式:", self.trigger_url_pattern)

        self.trigger_timeout = QSpinBox()
        self.trigger_timeout.setMinimum(1)
        self.trigger_timeout.setMaximum(300)
        self.trigger_timeout.setValue(30)
        self.trigger_timeout.setSuffix(" 秒")
        self.trigger_timeout.setStyleSheet(self.get_input_style())
        listen_layout.addRow("超时时间:", self.trigger_timeout)

        self.trigger_save_variable = QLineEdit()
        self.trigger_save_variable.setPlaceholderText("request_data")
        self.trigger_save_variable.setStyleSheet(self.get_input_style())
        listen_layout.addRow("保存到变量:", self.trigger_save_variable)

        parent_layout.addWidget(listen_group)

    def create_listen_request_result_config(self, parent_layout):
        """创建监听请求结果配置"""
        result_group = QGroupBox("监听请求结果设置")
        result_layout = QFormLayout(result_group)

        self.result_url_pattern = QLineEdit()
        self.result_url_pattern.setPlaceholderText("URL匹配模式（可选）")
        self.result_url_pattern.setStyleSheet(self.get_input_style())
        result_layout.addRow("URL模式:", self.result_url_pattern)

        self.result_timeout = QSpinBox()
        self.result_timeout.setMinimum(1)
        self.result_timeout.setMaximum(300)
        self.result_timeout.setValue(30)
        self.result_timeout.setSuffix(" 秒")
        self.result_timeout.setStyleSheet(self.get_input_style())
        result_layout.addRow("超时时间:", self.result_timeout)

        self.result_save_variable = QLineEdit()
        self.result_save_variable.setPlaceholderText("response_data")
        self.result_save_variable.setStyleSheet(self.get_input_style())
        result_layout.addRow("保存到变量:", self.result_save_variable)

        parent_layout.addWidget(result_group)

    def create_stop_listening_config(self, parent_layout):
        """创建停止页面监听配置"""
        stop_group = QGroupBox("停止页面监听设置")
        stop_layout = QFormLayout(stop_group)

        desc_label = QLabel("停止当前页面的网络请求监听")
        desc_label.setStyleSheet("color: #666666; font-size: 14px;")
        stop_layout.addRow("操作说明:", desc_label)

        parent_layout.addWidget(stop_group)

    def create_clear_cookie_config(self, parent_layout):
        """创建清除Cookie配置"""
        clear_group = QGroupBox("清除Cookie设置")
        clear_layout = QFormLayout(clear_group)

        self.clear_cookie_type = QComboBox()
        self.clear_cookie_type.addItems(["所有Cookie", "指定Cookie"])
        self.clear_cookie_type.setStyleSheet(self.get_input_style())
        clear_layout.addRow("清除类型:", self.clear_cookie_type)

        self.clear_cookie_name = QLineEdit()
        self.clear_cookie_name.setPlaceholderText("Cookie名称")
        self.clear_cookie_name.setStyleSheet(self.get_input_style())
        clear_layout.addRow("Cookie名称:", self.clear_cookie_name)

        parent_layout.addWidget(clear_group)

    # ==================== 数据处理配置方法 ====================

    def create_text_extract_config(self, parent_layout):
        """创建文本提取配置"""
        extract_group = QGroupBox("文本提取设置")
        extract_layout = QFormLayout(extract_group)

        self.source_variable = QLineEdit()
        self.source_variable.setPlaceholderText("source_text")
        self.source_variable.setStyleSheet(self.get_input_style())
        extract_layout.addRow("源变量:", self.source_variable)

        self.extract_pattern = QTextEdit()
        self.extract_pattern.setFixedHeight(80)
        self.extract_pattern.setPlaceholderText(r"(\d{4}-\d{2}-\d{2})")
        self.extract_pattern.setStyleSheet(self.get_input_style())
        extract_layout.addRow("正则表达式:", self.extract_pattern)

        self.extract_group_index = QSpinBox()
        self.extract_group_index.setMinimum(0)
        self.extract_group_index.setValue(1)
        self.extract_group_index.setStyleSheet(self.get_input_style())
        extract_layout.addRow("提取组索引:", self.extract_group_index)

        self.extract_save_variable = QLineEdit()
        self.extract_save_variable.setPlaceholderText("extracted_text")
        self.extract_save_variable.setStyleSheet(self.get_input_style())
        extract_layout.addRow("保存到变量:", self.extract_save_variable)

        parent_layout.addWidget(extract_group)

    def create_json_convert_config(self, parent_layout):
        """创建JSON转换配置"""
        json_group = QGroupBox("JSON转换设置")
        json_layout = QFormLayout(json_group)

        self.json_source_variable = QLineEdit()
        self.json_source_variable.setPlaceholderText("source_data")
        self.json_source_variable.setStyleSheet(self.get_input_style())
        json_layout.addRow("源变量:", self.json_source_variable)

        self.json_convert_type = QComboBox()
        self.json_convert_type.addItems(["对象转JSON", "JSON转对象", "格式化JSON"])
        self.json_convert_type.setStyleSheet(self.get_input_style())
        json_layout.addRow("转换类型:", self.json_convert_type)

        self.json_save_variable = QLineEdit()
        self.json_save_variable.setPlaceholderText("json_result")
        self.json_save_variable.setStyleSheet(self.get_input_style())
        json_layout.addRow("保存到变量:", self.json_save_variable)

        parent_layout.addWidget(json_group)

    def create_field_extract_config(self, parent_layout):
        """创建字段提取配置"""
        field_group = QGroupBox("字段提取设置")
        field_layout = QFormLayout(field_group)

        self.field_source_variable = QLineEdit()
        self.field_source_variable.setPlaceholderText("data_array")
        self.field_source_variable.setStyleSheet(self.get_input_style())
        field_layout.addRow("源变量:", self.field_source_variable)

        self.field_path = QLineEdit()
        self.field_path.setPlaceholderText("user.name 或 [0].title")
        self.field_path.setStyleSheet(self.get_input_style())
        field_layout.addRow("字段路径:", self.field_path)

        self.field_save_variable = QLineEdit()
        self.field_save_variable.setPlaceholderText("extracted_field")
        self.field_save_variable.setStyleSheet(self.get_input_style())
        field_layout.addRow("保存到变量:", self.field_save_variable)

        parent_layout.addWidget(field_group)

    def create_random_extract_config(self, parent_layout):
        """创建随机提取配置"""
        random_group = QGroupBox("随机提取设置")
        random_layout = QFormLayout(random_group)

        self.random_source_variable = QLineEdit()
        self.random_source_variable.setPlaceholderText("data_list")
        self.random_source_variable.setStyleSheet(self.get_input_style())
        random_layout.addRow("源变量:", self.random_source_variable)

        self.random_count = QSpinBox()
        self.random_count.setMinimum(1)
        self.random_count.setMaximum(100)
        self.random_count.setValue(1)
        self.random_count.setStyleSheet(self.get_input_style())
        random_layout.addRow("提取数量:", self.random_count)

        self.random_unique = QCheckBox("不重复提取")
        self.random_unique.setChecked(True)
        random_layout.addRow("", self.random_unique)

        self.random_save_variable = QLineEdit()
        self.random_save_variable.setPlaceholderText("random_item")
        self.random_save_variable.setStyleSheet(self.get_input_style())
        random_layout.addRow("保存到变量:", self.random_save_variable)

        parent_layout.addWidget(random_group)

    # ==================== 环境信息配置方法 ====================

    def create_update_env_note_config(self, parent_layout):
        """创建更新环境备注配置"""
        env_group = QGroupBox("更新环境备注设置")
        env_layout = QFormLayout(env_group)

        self.env_note_content = QTextEdit()
        self.env_note_content.setFixedHeight(100)
        self.env_note_content.setPlaceholderText("输入新的环境备注内容")
        self.env_note_content.setStyleSheet(self.get_input_style())
        env_layout.addRow("备注内容:", self.env_note_content)

        self.env_note_append = QCheckBox("追加到现有备注")
        env_layout.addRow("", self.env_note_append)

        parent_layout.addWidget(env_group)

    def create_update_env_tag_config(self, parent_layout):
        """创建更新环境标签配置"""
        env_group = QGroupBox("更新环境标签设置")
        env_layout = QFormLayout(env_group)

        self.env_tag_content = QLineEdit()
        self.env_tag_content.setPlaceholderText("标签1,标签2,标签3")
        self.env_tag_content.setStyleSheet(self.get_input_style())
        env_layout.addRow("标签内容:", self.env_tag_content)

        self.env_tag_operation = QComboBox()
        self.env_tag_operation.addItems(["替换", "添加", "删除"])
        self.env_tag_operation.setStyleSheet(self.get_input_style())
        env_layout.addRow("操作类型:", self.env_tag_operation)

        parent_layout.addWidget(env_group)

    # ==================== 流程管理配置方法 ====================

    def create_start_browser_config(self, parent_layout):
        """创建启动新浏览器配置"""
        browser_group = QGroupBox("启动新浏览器设置")
        browser_layout = QFormLayout(browser_group)

        self.browser_env_id = QLineEdit()
        self.browser_env_id.setPlaceholderText("36289")
        self.browser_env_id.setStyleSheet(self.get_input_style())
        browser_layout.addRow("环境编号:", self.browser_env_id)

        self.browser_exception_handling = QComboBox()
        self.browser_exception_handling.addItems(["跳过", "中断"])
        self.browser_exception_handling.setStyleSheet(self.get_input_style())
        browser_layout.addRow("异常处理:", self.browser_exception_handling)

        self.browser_completion_handling = QComboBox()
        self.browser_completion_handling.addItems(["保留浏览器", "关闭浏览器"])
        self.browser_completion_handling.setStyleSheet(self.get_input_style())
        browser_layout.addRow("完成处理:", self.browser_completion_handling)

        parent_layout.addWidget(browser_group)

    def create_if_condition_config(self, parent_layout):
        """创建IF条件配置"""
        if_group = QGroupBox("IF条件设置")
        if_layout = QFormLayout(if_group)

        self.if_variable = QLineEdit()
        self.if_variable.setPlaceholderText("phone_name")
        self.if_variable.setStyleSheet(self.get_input_style())
        if_layout.addRow("判断变量:", self.if_variable)

        self.if_condition = QComboBox()
        self.if_condition.addItems([
            "存在", "不存在", "等于", "不等于", "大于", "大于等于",
            "小于", "小于等于", "包含", "不包含", "在其中", "不在其中"
        ])
        self.if_condition.setStyleSheet(self.get_input_style())
        if_layout.addRow("条件:", self.if_condition)

        self.if_result = QLineEdit()
        self.if_result.setPlaceholderText("比较值或变量")
        self.if_result.setStyleSheet(self.get_input_style())
        if_layout.addRow("比较结果:", self.if_result)

        parent_layout.addWidget(if_group)

    def create_for_element_config(self, parent_layout):
        """创建For循环元素配置"""
        for_group = QGroupBox("For循环元素设置")
        for_layout = QFormLayout(for_group)

        self.for_element_selector = QLineEdit()
        self.for_element_selector.setPlaceholderText(".product-item")
        self.for_element_selector.setStyleSheet(self.get_input_style())
        for_layout.addRow("元素选择器:", self.for_element_selector)

        self.for_element_save_object = QLineEdit()
        self.for_element_save_object.setPlaceholderText("current_element")
        self.for_element_save_object.setStyleSheet(self.get_input_style())
        for_layout.addRow("循环对象保存至:", self.for_element_save_object)

        self.for_element_save_index = QLineEdit()
        self.for_element_save_index.setPlaceholderText("element_index")
        self.for_element_save_index.setStyleSheet(self.get_input_style())
        for_layout.addRow("循环位置保存至:", self.for_element_save_index)

        parent_layout.addWidget(for_group)

    def create_for_count_config(self, parent_layout):
        """创建For循环次数配置"""
        for_group = QGroupBox("For循环次数设置")
        for_layout = QFormLayout(for_group)

        self.for_count_times = QSpinBox()
        self.for_count_times.setMinimum(1)
        self.for_count_times.setMaximum(1000)
        self.for_count_times.setValue(5)
        self.for_count_times.setStyleSheet(self.get_input_style())
        for_layout.addRow("循环次数:", self.for_count_times)

        self.for_count_save_index = QLineEdit()
        self.for_count_save_index.setPlaceholderText("loop_index")
        self.for_count_save_index.setStyleSheet(self.get_input_style())
        for_layout.addRow("循环位置保存至:", self.for_count_save_index)

        parent_layout.addWidget(for_group)

    def create_for_data_config(self, parent_layout):
        """创建For循环数据配置"""
        for_group = QGroupBox("For循环数据设置")
        for_layout = QFormLayout(for_group)

        self.for_data_variable = QLineEdit()
        self.for_data_variable.setPlaceholderText("website_list")
        self.for_data_variable.setStyleSheet(self.get_input_style())
        for_layout.addRow("数据变量:", self.for_data_variable)

        self.for_data_save_object = QLineEdit()
        self.for_data_save_object.setPlaceholderText("current_data")
        self.for_data_save_object.setStyleSheet(self.get_input_style())
        for_layout.addRow("循环对象保存至:", self.for_data_save_object)

        self.for_data_save_index = QLineEdit()
        self.for_data_save_index.setPlaceholderText("data_index")
        self.for_data_save_index.setStyleSheet(self.get_input_style())
        for_layout.addRow("循环位置保存至:", self.for_data_save_index)

        parent_layout.addWidget(for_group)

    def create_break_loop_config(self, parent_layout):
        """创建退出循环配置"""
        break_group = QGroupBox("退出循环设置")
        break_layout = QFormLayout(break_group)

        desc_label = QLabel("退出当前循环，继续执行循环后的步骤")
        desc_label.setStyleSheet("color: #666666; font-size: 14px;")
        break_layout.addRow("操作说明:", desc_label)

        self.break_condition = QCheckBox("仅在满足条件时退出")
        break_layout.addRow("", self.break_condition)

        parent_layout.addWidget(break_group)

    def create_close_browser_config(self, parent_layout):
        """创建关闭浏览器配置"""
        close_group = QGroupBox("关闭浏览器设置")
        close_layout = QFormLayout(close_group)

        desc_label = QLabel("关闭当前浏览器环境")
        desc_label.setStyleSheet("color: #666666; font-size: 14px;")
        close_layout.addRow("操作说明:", desc_label)

        self.close_save_data = QCheckBox("保存浏览器数据")
        self.close_save_data.setChecked(True)
        close_layout.addRow("", self.close_save_data)

        parent_layout.addWidget(close_group)

    def create_while_loop_config(self, parent_layout):
        """创建While循环配置"""
        while_group = QGroupBox("While循环设置")
        while_layout = QFormLayout(while_group)

        self.while_variable = QLineEdit()
        self.while_variable.setPlaceholderText("loop_condition")
        self.while_variable.setStyleSheet(self.get_input_style())
        while_layout.addRow("条件变量:", self.while_variable)

        self.while_condition = QComboBox()
        self.while_condition.addItems([
            "存在", "不存在", "等于", "不等于", "大于", "大于等于",
            "小于", "小于等于", "包含", "不包含"
        ])
        self.while_condition.setStyleSheet(self.get_input_style())
        while_layout.addRow("条件:", self.while_condition)

        self.while_result = QLineEdit()
        self.while_result.setPlaceholderText("比较值")
        self.while_result.setStyleSheet(self.get_input_style())
        while_layout.addRow("比较结果:", self.while_result)

        self.while_max_iterations = QSpinBox()
        self.while_max_iterations.setMinimum(1)
        self.while_max_iterations.setMaximum(10000)
        self.while_max_iterations.setValue(100)
        self.while_max_iterations.setStyleSheet(self.get_input_style())
        while_layout.addRow("最大循环次数:", self.while_max_iterations)

        parent_layout.addWidget(while_group)

    def create_use_other_flow_config(self, parent_layout):
        """创建使用其他流程配置"""
        flow_group = QGroupBox("使用其他流程设置")
        flow_layout = QFormLayout(flow_group)

        self.other_flow_name = QComboBox()
        self.other_flow_name.addItems(["选择流程..."])  # 这里应该动态加载已有流程
        self.other_flow_name.setStyleSheet(self.get_input_style())
        flow_layout.addRow("选择流程:", self.other_flow_name)

        self.flow_variable_mapping = QTextEdit()
        self.flow_variable_mapping.setFixedHeight(80)
        self.flow_variable_mapping.setPlaceholderText("变量映射配置 (JSON格式)")
        self.flow_variable_mapping.setStyleSheet(self.get_input_style())
        flow_layout.addRow("变量映射:", self.flow_variable_mapping)

        parent_layout.addWidget(flow_group)

    # ==================== 第三方工具配置方法 ====================

    def create_captcha_config(self, parent_layout):
        """创建2Captcha配置"""
        captcha_group = QGroupBox("2Captcha设置")
        captcha_layout = QFormLayout(captcha_group)

        self.captcha_api_key = QLineEdit()
        self.captcha_api_key.setPlaceholderText("2Captcha API密钥")
        self.captcha_api_key.setStyleSheet(self.get_input_style())
        captcha_layout.addRow("API密钥:", self.captcha_api_key)

        self.captcha_type = QComboBox()
        self.captcha_type.addItems([
            "Normal CAPTCHA", "reCAPTCHA V2", "reCAPTCHA V3",
            "hCaptcha", "Cloudflare Turnstile"
        ])
        self.captcha_type.setStyleSheet(self.get_input_style())
        captcha_layout.addRow("验证码类型:", self.captcha_type)

        self.captcha_site_key = QLineEdit()
        self.captcha_site_key.setPlaceholderText("站点密钥（reCAPTCHA等需要）")
        self.captcha_site_key.setStyleSheet(self.get_input_style())
        captcha_layout.addRow("站点密钥:", self.captcha_site_key)

        self.captcha_page_url = QLineEdit()
        self.captcha_page_url.setPlaceholderText("页面URL（reCAPTCHA等需要）")
        self.captcha_page_url.setStyleSheet(self.get_input_style())
        captcha_layout.addRow("页面URL:", self.captcha_page_url)

        self.captcha_save_variable = QLineEdit()
        self.captcha_save_variable.setPlaceholderText("captcha_result")
        self.captcha_save_variable.setStyleSheet(self.get_input_style())
        captcha_layout.addRow("保存到变量:", self.captcha_save_variable)

        parent_layout.addWidget(captcha_group)

    def create_google_sheet_config(self, parent_layout):
        """创建Google Sheet配置"""
        sheet_group = QGroupBox("Google Sheet设置")
        sheet_layout = QFormLayout(sheet_group)

        self.sheet_operation_type = QComboBox()
        self.sheet_operation_type.addItems(["读取", "写入", "清除"])
        self.sheet_operation_type.setStyleSheet(self.get_input_style())
        sheet_layout.addRow("操作类型:", self.sheet_operation_type)

        self.sheet_id = QLineEdit()
        self.sheet_id.setPlaceholderText("Google Sheet ID")
        self.sheet_id.setStyleSheet(self.get_input_style())
        sheet_layout.addRow("表格ID:", self.sheet_id)

        self.sheet_range = QLineEdit()
        self.sheet_range.setPlaceholderText("A1:Z1000")
        self.sheet_range.setStyleSheet(self.get_input_style())
        sheet_layout.addRow("数据范围:", self.sheet_range)

        self.sheet_data_variable = QLineEdit()
        self.sheet_data_variable.setPlaceholderText("数据变量名")
        self.sheet_data_variable.setStyleSheet(self.get_input_style())
        sheet_layout.addRow("数据变量:", self.sheet_data_variable)

        self.sheet_save_variable = QLineEdit()
        self.sheet_save_variable.setPlaceholderText("sheet_data")
        self.sheet_save_variable.setStyleSheet(self.get_input_style())
        sheet_layout.addRow("保存到变量:", self.sheet_save_variable)

        parent_layout.addWidget(sheet_group)



    def create_openai_config(self, parent_layout):
        """创建OpenAI配置"""
        openai_group = QGroupBox("OpenAI设置")
        openai_layout = QFormLayout(openai_group)

        self.openai_api_key = QLineEdit()
        self.openai_api_key.setPlaceholderText("您的OpenAI API Key")
        self.openai_api_key.setStyleSheet(self.get_input_style())
        openai_layout.addRow("API Key:", self.openai_api_key)

        self.openai_output_type = QComboBox()
        self.openai_output_type.addItems(["文本", "图像"])
        self.openai_output_type.setStyleSheet(self.get_input_style())
        openai_layout.addRow("输出类型:", self.openai_output_type)

        self.openai_model = QComboBox()
        self.openai_model.addItems(["GPT-4o mini", "GPT-4o", "DALL·E-3"])
        self.openai_model.setStyleSheet(self.get_input_style())
        openai_layout.addRow("模型:", self.openai_model)

        self.openai_prompt = QTextEdit()
        self.openai_prompt.setFixedHeight(100)
        self.openai_prompt.setPlaceholderText("输入您的提问内容或图像描述")
        self.openai_prompt.setStyleSheet(self.get_input_style())
        openai_layout.addRow("提问内容:", self.openai_prompt)

        # 图像专用设置
        self.image_size = QComboBox()
        self.image_size.addItems(["1024x1024", "1792x1024", "1024x1792"])
        self.image_size.setStyleSheet(self.get_input_style())
        openai_layout.addRow("图像尺寸:", self.image_size)

        self.image_format = QComboBox()
        self.image_format.addItems(["URL", "Base64"])
        self.image_format.setStyleSheet(self.get_input_style())
        openai_layout.addRow("输出格式:", self.image_format)

        self.image_quality = QComboBox()
        self.image_quality.addItems(["标清", "高清"])
        self.image_quality.setStyleSheet(self.get_input_style())
        openai_layout.addRow("图像质量:", self.image_quality)

        self.openai_save_variable = QLineEdit()
        self.openai_save_variable.setPlaceholderText("ai_result")
        self.openai_save_variable.setStyleSheet(self.get_input_style())
        openai_layout.addRow("结果保存至:", self.openai_save_variable)

        parent_layout.addWidget(openai_group)

    def create_default_config(self, parent_layout):
        """创建默认配置"""
        default_group = QGroupBox("基本设置")
        default_layout = QFormLayout(default_group)
        
        self.timeout = QSpinBox()
        self.timeout.setMinimum(1)
        self.timeout.setMaximum(300)
        self.timeout.setValue(30)
        self.timeout.setSuffix(" 秒")
        self.timeout.setStyleSheet(self.get_input_style())
        default_layout.addRow("超时等待:", self.timeout)
        
        self.stop_on_error = QCheckBox("失败时停止执行")
        self.stop_on_error.setStyleSheet("""
            QCheckBox {
                font-size: 14px;
                color: #333333;
            }
        """)
        default_layout.addRow("错误处理:", self.stop_on_error)
        
        parent_layout.addWidget(default_group)
        
    def create_buttons(self, parent_layout):
        """创建底部按钮区域 - 完全按照截图样式"""
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.setContentsMargins(0, 20, 0, 0)
        button_layout.setSpacing(12)

        # 左侧留空
        button_layout.addStretch()

        # 确定按钮 - 蓝色，完全按照截图
        ok_btn = QPushButton("确定")
        ok_btn.setFixedSize(80, 32)
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #0969da;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #0860ca;
            }
            QPushButton:pressed {
                background-color: #0757ba;
            }
        """)
        ok_btn.clicked.connect(self.accept_config)
        button_layout.addWidget(ok_btn)

        # 取消按钮 - 灰色，完全按照截图
        cancel_btn = QPushButton("取消")
        cancel_btn.setFixedSize(80, 32)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #656d76;
                border: none;
                border-radius: 6px;
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #f3f4f6;
                color: #24292f;
            }
            QPushButton:pressed {
                background-color: #e5e7ea;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)

        parent_layout.addWidget(button_widget)
        
    def get_input_style(self):
        """获取输入框样式 - 完全按照截图设计"""
        return """
            QLineEdit, QTextEdit, QSpinBox, QComboBox {
                border: 1px solid #d0d7de;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 13px;
                background-color: white;
                min-height: 20px;
            }
            QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QComboBox:focus {
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
        """
        
    def accept_config(self):
        """确认配置"""
        # 收集配置数据
        self.config_data = {
            "operation": self.operation_name,
            "timestamp": self.get_current_timestamp()
        }

        # 收集所有可能的配置项
        config_fields = [
            # 页面操作
            'tab_url', 'switch_to_new', 'goto_url', 'timeout_seconds', 'wait_load',
            'wait_type', 'wait_min', 'wait_max', 'scroll_range_type', 'scroll_selector',
            'scroll_distance', 'scroll_type_detail', 'scroll_position_type',
            'click_selector', 'selector_type', 'click_button', 'click_count', 'element_index',
            'hover_selector', 'hover_duration', 'nav_wait_load', 'close_type', 'tab_index',
            'switch_type', 'switch_target',

            # 键盘操作
            'keyboard_delay',

            # 等待操作
            'wait_element_selector', 'wait_condition', 'wait_timeout',
            'page_wait_type', 'page_timeout', 'popup_type', 'popup_action', 'popup_timeout',

            # 获取数据
            'get_element_selector', 'extract_type', 'attribute_name', 'save_variable',
            'page_info_type', 'page_save_variable', 'popup_get_type', 'popup_save_variable',
            'cookie_type', 'cookie_name', 'cookie_save_variable', 'env_info_type', 'env_save_variable',
            'excel_path', 'sheet_name', 'start_row', 'excel_save_variable',
            'txt_path', 'txt_encoding', 'txt_delimiter', 'txt_save_variable',

            # 数据处理
            'source_variable', 'extract_group_index', 'extract_save_variable',
            'json_source_variable', 'json_convert_type', 'json_save_variable',
            'field_source_variable', 'field_path', 'field_save_variable',
            'random_source_variable', 'random_count', 'random_unique', 'random_save_variable',

            # 环境信息
            'env_note_append', 'env_tag_operation',

            # 流程管理
            'browser_env_id', 'browser_exception_handling', 'browser_completion_handling',
            'if_variable', 'if_condition', 'if_result', 'for_element_selector',
            'for_element_save_object', 'for_element_save_index', 'for_count_times',
            'for_count_save_index', 'for_data_variable', 'for_data_save_object',
            'for_data_save_index', 'break_condition', 'close_save_data',
            'while_variable', 'while_condition', 'while_result', 'while_max_iterations',
            'other_flow_name', 'flow_variable_mapping',

            # 第三方工具
            'captcha_api_key', 'captcha_type', 'captcha_site_key', 'captcha_page_url', 'captcha_save_variable',
            'openai_api_key', 'openai_output_type', 'openai_model', 'image_size',
            'image_format', 'image_quality', 'openai_save_variable',

            # 兼容旧版本
            'selector_input', 'element_order', 'content_input', 'input_interval',
            'url_input', 'wait_time', 'timeout'
        ]

        # 收集所有存在的配置项
        for field in config_fields:
            if hasattr(self, field):
                widget = getattr(self, field)
                if isinstance(widget, QLineEdit):
                    self.config_data[field] = widget.text()
                elif isinstance(widget, QTextEdit):
                    self.config_data[field] = widget.toPlainText()
                elif isinstance(widget, QSpinBox):
                    self.config_data[field] = widget.value()
                elif isinstance(widget, QComboBox):
                    self.config_data[field] = widget.currentText()
                elif isinstance(widget, QCheckBox):
                    self.config_data[field] = widget.isChecked()

        # 特殊处理一些复合字段
        if hasattr(self, 'extract_pattern'):
            self.config_data['extract_pattern'] = self.extract_pattern.toPlainText()
        if hasattr(self, 'env_note_content'):
            self.config_data['env_note_content'] = self.env_note_content.toPlainText()
        if hasattr(self, 'env_tag_content'):
            self.config_data['env_tag_content'] = self.env_tag_content.text()
        if hasattr(self, 'openai_prompt'):
            self.config_data['openai_prompt'] = self.openai_prompt.toPlainText()
        if hasattr(self, 'js_code'):
            self.config_data['js_code'] = self.js_code.toPlainText()
        if hasattr(self, 'return_variable'):
            self.config_data['return_variable'] = self.return_variable.text()

        # 验证必填字段
        if not self.validate_config():
            return

        self.accept()
        
    def validate_config(self):
        """验证配置"""
        # 页面操作验证
        if self.operation_name == "前往网址" and hasattr(self, 'goto_url'):
            if not self.goto_url.text().strip():
                QMessageBox.warning(self, "警告", "请输入目标URL")
                return False

        if self.operation_name == "点击" and hasattr(self, 'click_selector'):
            if not self.click_selector.text().strip():
                QMessageBox.warning(self, "警告", "请输入点击元素的选择器")
                return False

        if self.operation_name == "悬停" and hasattr(self, 'hover_selector'):
            if not self.hover_selector.text().strip():
                QMessageBox.warning(self, "警告", "请输入悬停元素的选择器")
                return False

        # 等待操作验证
        if self.operation_name == "等待元素" and hasattr(self, 'wait_element_selector'):
            if not self.wait_element_selector.text().strip():
                QMessageBox.warning(self, "警告", "请输入等待元素的选择器")
                return False

        # 获取数据验证
        if self.operation_name == "获取元素" and hasattr(self, 'get_element_selector'):
            if not self.get_element_selector.text().strip():
                QMessageBox.warning(self, "警告", "请输入获取元素的选择器")
                return False
            if not self.save_variable.text().strip():
                QMessageBox.warning(self, "警告", "请输入保存变量名")
                return False

        if self.operation_name == "导入Excel素材" and hasattr(self, 'excel_path'):
            if not self.excel_path.text().strip():
                QMessageBox.warning(self, "警告", "请输入Excel文件路径")
                return False

        if self.operation_name == "导入txt素材" and hasattr(self, 'txt_path'):
            if not self.txt_path.text().strip():
                QMessageBox.warning(self, "警告", "请输入txt文件路径")
                return False

        # 数据处理验证
        if self.operation_name == "文本中提取" and hasattr(self, 'source_variable'):
            if not self.source_variable.text().strip():
                QMessageBox.warning(self, "警告", "请输入源变量名")
                return False
            if not self.extract_pattern.toPlainText().strip():
                QMessageBox.warning(self, "警告", "请输入正则表达式")
                return False

        # 流程管理验证
        if self.operation_name == "启动新浏览器" and hasattr(self, 'browser_env_id'):
            if not self.browser_env_id.text().strip():
                QMessageBox.warning(self, "警告", "请输入环境编号")
                return False

        if self.operation_name == "IF条件" and hasattr(self, 'if_variable'):
            if not self.if_variable.text().strip():
                QMessageBox.warning(self, "警告", "请输入判断变量")
                return False

        # 第三方工具验证
        if self.operation_name == "2Captcha" and hasattr(self, 'captcha_api_key'):
            if not self.captcha_api_key.text().strip():
                QMessageBox.warning(self, "警告", "请输入2Captcha API Key")
                return False

        if self.operation_name == "OpenAI" and hasattr(self, 'openai_api_key'):
            if not self.openai_api_key.text().strip():
                QMessageBox.warning(self, "警告", "请输入OpenAI API Key")
                return False
            if not self.openai_prompt.toPlainText().strip():
                QMessageBox.warning(self, "警告", "请输入提问内容")
                return False

        # 兼容旧版本验证
        if self.operation_name == "访问网站" and hasattr(self, 'url_input'):
            if not self.url_input.text().strip():
                QMessageBox.warning(self, "警告", "请输入访问的URL")
                return False

        if self.operation_name in ["点击元素", "输入内容"] and hasattr(self, 'selector_input'):
            if not self.selector_input.text().strip():
                QMessageBox.warning(self, "警告", "请输入元素选择器")
                return False

        return True
        
    def get_current_timestamp(self):
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def get_config_data(self):
        """获取配置数据"""
        return self.config_data

    def set_config_data(self, config_data):
        """设置配置数据 - 用于编辑现有步骤"""
        if not isinstance(config_data, dict):
            return

        # 保存配置数据
        self.config_data = config_data.copy()

        # 设置所有可能的配置项到对应的控件
        config_fields = [
            # 页面操作
            'tab_url', 'switch_to_new', 'goto_url', 'timeout_seconds', 'wait_load',
            'wait_type', 'wait_min', 'wait_max', 'scroll_range_type', 'scroll_selector',
            'scroll_distance', 'scroll_type_detail', 'scroll_position_type',
            'click_selector', 'selector_type', 'click_button', 'click_count', 'element_index',
            'hover_selector', 'hover_duration', 'nav_wait_load', 'close_type', 'tab_index',
            'switch_type', 'switch_target',

            # 键盘操作
            'keyboard_delay',

            # 等待操作
            'wait_element_selector', 'wait_condition', 'wait_timeout',
            'page_wait_type', 'page_timeout', 'popup_type', 'popup_action', 'popup_timeout',

            # 获取数据
            'get_element_selector', 'extract_type', 'attribute_name', 'save_variable',
            'page_info_type', 'page_save_variable', 'popup_get_type', 'popup_save_variable',
            'cookie_type', 'cookie_name', 'cookie_save_variable', 'env_info_type', 'env_save_variable',
            'excel_path', 'sheet_name', 'start_row', 'excel_save_variable',
            'txt_path', 'txt_encoding', 'txt_delimiter', 'txt_save_variable',

            # 数据处理
            'source_variable', 'extract_group_index', 'extract_save_variable',
            'json_source_variable', 'json_convert_type', 'json_save_variable',
            'field_source_variable', 'field_path', 'field_save_variable',
            'random_source_variable', 'random_count', 'random_unique', 'random_save_variable',

            # 环境信息
            'env_note_append', 'env_tag_operation',

            # 流程管理
            'browser_env_id', 'browser_exception_handling', 'browser_completion_handling',
            'if_variable', 'if_condition', 'if_result', 'for_element_selector',
            'for_element_save_object', 'for_element_save_index', 'for_count_times',
            'for_count_save_index', 'for_data_variable', 'for_data_save_object',
            'for_data_save_index', 'break_condition', 'close_save_data',
            'while_variable', 'while_condition', 'while_result', 'while_max_iterations',
            'other_flow_name', 'flow_variable_mapping',

            # 第三方工具
            'captcha_api_key', 'captcha_type', 'captcha_site_key', 'captcha_page_url', 'captcha_save_variable',
            'openai_api_key', 'openai_output_type', 'openai_model', 'image_size',
            'image_format', 'image_quality', 'openai_save_variable',

            # 兼容旧版本
            'selector_input', 'element_order', 'content_input', 'input_interval',
            'url_input', 'wait_time', 'timeout'
        ]

        # 设置所有存在的配置项到对应控件
        for field in config_fields:
            if field in config_data and hasattr(self, field):
                widget = getattr(self, field)
                value = config_data[field]

                try:
                    if isinstance(widget, QLineEdit):
                        widget.setText(str(value))
                    elif isinstance(widget, QTextEdit):
                        widget.setPlainText(str(value))
                    elif isinstance(widget, QSpinBox):
                        widget.setValue(int(value) if isinstance(value, (int, float)) else 0)
                    elif isinstance(widget, QComboBox):
                        # 查找匹配的项目
                        index = widget.findText(str(value))
                        if index >= 0:
                            widget.setCurrentIndex(index)
                    elif isinstance(widget, QCheckBox):
                        widget.setChecked(bool(value))
                except Exception as e:
                    print(f"设置配置项 {field} 时出错: {e}")

        # 特殊处理一些复合字段
        if 'extract_pattern' in config_data and hasattr(self, 'extract_pattern'):
            self.extract_pattern.setPlainText(str(config_data['extract_pattern']))
        if 'env_note_content' in config_data and hasattr(self, 'env_note_content'):
            self.env_note_content.setPlainText(str(config_data['env_note_content']))
        if 'env_tag_content' in config_data and hasattr(self, 'env_tag_content'):
            self.env_tag_content.setText(str(config_data['env_tag_content']))
        if 'openai_prompt' in config_data and hasattr(self, 'openai_prompt'):
            self.openai_prompt.setPlainText(str(config_data['openai_prompt']))
        if 'js_code' in config_data and hasattr(self, 'js_code'):
            self.js_code.setPlainText(str(config_data['js_code']))
        if 'return_variable' in config_data and hasattr(self, 'return_variable'):
            self.return_variable.setText(str(config_data['return_variable']))

        # ===== 修复数据不一致问题 - AdsPower格式映射 =====

        # 根据操作类型进行特殊处理
        operation = config_data.get('operation', self.operation_name)

        # 新建标签操作 - 只处理切换选项
        if operation == "新建标签" and hasattr(self, 'switch_to_new'):
            # 新建标签操作通常默认切换到新标签
            self.switch_to_new.setChecked(True)
            print("设置新建标签操作: 切换到新标签")

        # 访问网站操作 - 处理URL和超时
        elif operation == "访问网站":
            if 'url' in config_data and hasattr(self, 'goto_url'):
                self.goto_url.setText(str(config_data['url']))

            if 'timeout' in config_data and hasattr(self, 'timeout_seconds'):
                timeout_val = config_data['timeout']
                # 转换毫秒到秒
                if isinstance(timeout_val, (int, float)) and timeout_val > 1000:
                    self.timeout_seconds.setValue(int(timeout_val / 1000))
                else:
                    self.timeout_seconds.setValue(int(timeout_val))

        # 等待时间操作的特殊处理
        elif operation == "等待时间":
            print("处理等待时间操作数据映射")

            # 等待类型映射
            if 'timeoutType' in config_data and hasattr(self, 'wait_type'):
                timeout_type = config_data['timeoutType']
                if timeout_type == 'randomInterval':
                    self.wait_type.setCurrentText('随机时间')
                else:
                    self.wait_type.setCurrentText('固定时间')
                print(f"设置等待类型: {timeout_type}")

            # 修复等待时间数据不一致问题 - 正确处理毫秒到秒的转换
            if 'timeoutMin' in config_data and hasattr(self, 'wait_min'):
                min_val = config_data['timeoutMin']
                if isinstance(min_val, (int, float)):
                    # 确保正确转换毫秒到秒
                    seconds_val = int(min_val / 1000) if min_val >= 1000 else int(min_val)
                    self.wait_min.setValue(seconds_val)
                    print(f"设置最小等待时间: {min_val}ms -> {seconds_val}s")

            if 'timeoutMax' in config_data and hasattr(self, 'wait_max'):
                max_val = config_data['timeoutMax']
                if isinstance(max_val, (int, float)):
                    # 确保正确转换毫秒到秒
                    seconds_val = int(max_val / 1000) if max_val >= 1000 else int(max_val)
                    self.wait_max.setValue(seconds_val)
                    print(f"设置最大等待时间: {max_val}ms -> {seconds_val}s")

        # 点击元素操作的特殊处理
        elif operation == "点击元素":
            print("处理点击元素操作数据映射")

            # 选择器映射
            if 'selector' in config_data and hasattr(self, 'click_selector'):
                self.click_selector.setText(str(config_data['selector']))
                print(f"设置点击选择器: {config_data['selector']}")

            if 'selectorRadio' in config_data and hasattr(self, 'selector_type'):
                selector_radio = config_data['selectorRadio']
                if selector_radio == 'XPath':
                    self.selector_type.setCurrentText('XPath')
                else:
                    self.selector_type.setCurrentText('CSS')
                print(f"设置选择器类型: {selector_radio}")

            # 点击按钮映射
            if 'button' in config_data and hasattr(self, 'click_button'):
                button_val = config_data['button']
                if button_val == 'left':
                    self.click_button.setCurrentText('左键')
                elif button_val == 'right':
                    self.click_button.setCurrentText('右键')
                elif button_val == 'middle':
                    self.click_button.setCurrentText('中键')
                print(f"设置点击按钮: {button_val}")

            # 点击次数映射
            if 'type' in config_data and hasattr(self, 'click_count'):
                click_type = config_data['type']
                if click_type == 'doubleClick':
                    self.click_count.setCurrentText('双击')
                else:
                    self.click_count.setCurrentText('单击')
                print(f"设置点击次数: {click_type}")

            # 元素序号映射
            if 'serial' in config_data and hasattr(self, 'element_index'):
                serial_val = config_data['serial']
                if isinstance(serial_val, (int, float)):
                    self.element_index.setValue(int(serial_val))
                    print(f"设置元素序号: {serial_val}")

        # 滚动页面操作的特殊处理
        elif operation == "滚动页面":
            print("处理滚动页面操作数据映射")

            # 滚动范围映射
            if 'rangeType' in config_data and hasattr(self, 'scroll_range_type'):
                range_type = config_data['rangeType']
                if range_type == 'window':
                    self.scroll_range_type.setCurrentText('窗口')
                elif range_type == 'element':
                    self.scroll_range_type.setCurrentText('元素')
                print(f"设置滚动范围: {range_type}")

            # 滚动位置映射
            if 'position' in config_data and hasattr(self, 'scroll_position_type'):
                position = config_data['position']
                if position == 'top':
                    self.scroll_position_type.setCurrentText('顶部')
                elif position == 'bottom':
                    self.scroll_position_type.setCurrentText('底部')
                elif position == 'center':
                    self.scroll_position_type.setCurrentText('中间')
                print(f"设置滚动位置: {position}")

            # 滚动类型映射
            if 'scrollType' in config_data and hasattr(self, 'scroll_type_detail'):
                scroll_type = config_data['scrollType']
                if scroll_type == 'position':
                    self.scroll_type_detail.setCurrentText('位置')
                elif scroll_type == 'distance':
                    self.scroll_type_detail.setCurrentText('距离')
                print(f"设置滚动类型: {scroll_type}")

            # 滚动距离映射
            if 'distance' in config_data and hasattr(self, 'scroll_distance'):
                distance = config_data['distance']
                if isinstance(distance, (int, float)):
                    self.scroll_distance.setValue(int(distance))
                    print(f"设置滚动距离: {distance}")

        # 特殊处理：备注字段映射
        if 'remark' in config_data and hasattr(self, 'return_variable'):
            self.return_variable.setText(str(config_data['remark']))

        # ===== 扩展所有操作类型的数据映射 =====

        # 访问网站操作的字段映射
        if 'url' in config_data and hasattr(self, 'goto_url'):
            self.goto_url.setText(str(config_data['url']))

        # 滚动页面操作的字段映射
        if 'rangeType' in config_data and hasattr(self, 'scroll_range_type'):
            range_type = config_data['rangeType']
            if range_type == 'window':
                self.scroll_range_type.setCurrentText('窗口')
            elif range_type == 'element':
                self.scroll_range_type.setCurrentText('元素')

        if 'position' in config_data and hasattr(self, 'scroll_position_type'):
            position = config_data['position']
            if position == 'top':
                self.scroll_position_type.setCurrentText('顶部')
            elif position == 'bottom':
                self.scroll_position_type.setCurrentText('底部')
            elif position == 'center':
                self.scroll_position_type.setCurrentText('中间')

        if 'scrollType' in config_data and hasattr(self, 'scroll_type_detail'):
            scroll_type = config_data['scrollType']
            if scroll_type == 'position':
                self.scroll_type_detail.setCurrentText('位置')
            elif scroll_type == 'distance':
                self.scroll_type_detail.setCurrentText('距离')

        if 'distance' in config_data and hasattr(self, 'scroll_distance'):
            distance = config_data['distance']
            if isinstance(distance, (int, float)):
                self.scroll_distance.setValue(int(distance))

        # inputContent操作的字段映射
        elif operation == "inputContent" or self.operation_name == "inputContent":
            print("处理inputContent操作数据映射")

            # 选择器映射
            if 'selector' in config_data and hasattr(self, 'input_selector'):
                self.input_selector.setText(str(config_data['selector']))

            if 'selectorRadio' in config_data and hasattr(self, 'input_selector_type'):
                selector_radio = config_data['selectorRadio']
                if selector_radio == 'XPath':
                    self.input_selector_type.setCurrentText('XPath')
                else:
                    self.input_selector_type.setCurrentText('CSS')

            # 输入内容映射
            if 'content' in config_data:
                # 尝试多个可能的控件名称
                for content_field in ['input_content', 'content_input']:
                    if hasattr(self, content_field):
                        widget = getattr(self, content_field)
                        if hasattr(widget, 'setPlainText'):
                            widget.setPlainText(str(config_data['content']))
                        elif hasattr(widget, 'setText'):
                            widget.setText(str(config_data['content']))
                        print(f"设置输入内容: {config_data['content']}")
                        break

            # 输入间隔映射
            if 'intervals' in config_data and hasattr(self, 'input_interval'):
                intervals = config_data['intervals']
                if isinstance(intervals, (int, float)):
                    self.input_interval.setValue(int(intervals))
                    print(f"设置输入间隔: {intervals}ms")

            # 随机内容映射
            if 'isRandom' in config_data and hasattr(self, 'random_content'):
                is_random = config_data['isRandom']
                self.random_content.setChecked(str(is_random) == '1')

            if 'randomContent' in config_data and hasattr(self, 'random_content_text'):
                self.random_content_text.setPlainText(str(config_data['randomContent']))

            # 清除选项映射
            if 'isClear' in config_data and hasattr(self, 'clear_before_input'):
                is_clear = config_data['isClear']
                self.clear_before_input.setChecked(str(is_clear) == '1')

            # 元素序号映射
            if 'serial' in config_data and hasattr(self, 'input_element_index'):
                serial_val = config_data['serial']
                if isinstance(serial_val, (int, float)):
                    self.input_element_index.setValue(int(serial_val))

        if 'isRandom' in config_data and hasattr(self, 'random_content'):
            is_random = config_data['isRandom']
            if hasattr(self, 'random_content'):
                self.random_content.setChecked(str(is_random) == '1')

        if 'randomContent' in config_data and hasattr(self, 'random_content_text'):
            self.random_content_text.setPlainText(str(config_data['randomContent']))

        if 'isClear' in config_data and hasattr(self, 'clear_before_input'):
            is_clear = config_data['isClear']
            if hasattr(self, 'clear_before_input'):
                self.clear_before_input.setChecked(str(is_clear) == '1')

        # keyboard操作的字段映射
        elif operation == "keyboard" or self.operation_name == "keyboard":
            print("处理keyboard操作数据映射")

            if 'type' in config_data and hasattr(self, 'key_type'):
                key_type = config_data['type']
                # 映射AdsPower的键盘类型到中文
                key_mapping = {
                    'Enter': '回车键',
                    'Escape': 'Esc键',
                    'Tab': 'Tab键',
                    'Space': '空格键',
                    'Backspace': '退格键',
                    'Delete': '删除键',
                    'ArrowUp': '方向上键',
                    'ArrowDown': '方向下键',
                    'ArrowLeft': '方向左键',
                    'ArrowRight': '方向右键'
                }
                chinese_key = key_mapping.get(key_type, key_type)
                index = self.key_type.findText(chinese_key)
                if index >= 0:
                    self.key_type.setCurrentIndex(index)
                    print(f"设置按键类型: {key_type} -> {chinese_key}")
                else:
                    print(f"未找到按键类型: {key_type}")

        # 获取元素操作的字段映射
        if 'attribute' in config_data and hasattr(self, 'attribute_name'):
            self.attribute_name.setText(str(config_data['attribute']))

        if 'saveVariable' in config_data and hasattr(self, 'save_variable'):
            self.save_variable.setText(str(config_data['saveVariable']))

        # 等待元素操作的字段映射
        if 'condition' in config_data and hasattr(self, 'wait_condition'):
            condition = config_data['condition']
            condition_mapping = {
                'appear': '出现',
                'disappear': '消失',
                'visible': '可见',
                'hidden': '隐藏',
                'clickable': '可点击'
            }
            chinese_condition = condition_mapping.get(condition, condition)
            index = self.wait_condition.findText(chinese_condition)
            if index >= 0:
                self.wait_condition.setCurrentIndex(index)

        print(f"已设置配置数据: {len(config_data)} 个配置项，包含完整的AdsPower格式映射")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = RPAOperationConfigDialog("点击元素")
    if dialog.exec_() == QDialog.Accepted:
        print("配置数据:", dialog.get_config_data())
    sys.exit(app.exec_())
