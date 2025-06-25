#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QLineEdit, QComboBox, QWidget, QScrollArea,
                             QFrame, QApplication, QSizePolicy, QSpacerItem)
from PyQt5.QtCore import Qt, pyqtSignal, QDateTime
from PyQt5.QtGui import QFont, QPainter, QPen, QColor, QPixmap, QIcon

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

class TaskFlowDialog(QDialog):
    """任务流程创建对话框 - 完全按照AdsPower设计"""
    
    def __init__(self, parent=None, flow_data=None):
        super().__init__(parent)
        self.setWindowTitle("创建任务流程")
        self.setFixedSize(1200, 800)
        self.setModal(False)  # 设置为非模态对话框，允许操作主界面

        # 用于编辑时预填充数据
        self.flow_data = flow_data
        self.parent_window = parent  # 保存父窗口引用以访问API

        # AdsPower操作名称映射表 - 完全按照截图重建
        self.adspower_operation_mapping = {
            # 页面操作 - 按照截图顺序
            'newPage': '新建标签',
            'closePage': '关闭标签',
            'closeOtherPages': '关闭其他标签',
            'switchPage': '切换标签',
            'gotoUrl': '访问网站',
            'refreshPage': '刷新页面',
            'pageBack': '页面后退',
            'pageScreenshot': '页面截图',
            'hoverElement': '经过元素',
            'selectDropdown': '下拉选择器',
            'focusElement': '元素聚焦',
            'click': '点击元素',
            'input': '输入内容',
            'inputContent': '输入内容',
            'scrollPage': '滚动页面',
            'uploadFile': '上传附件',
            'executeScript': '执行JS脚本',

            # 键盘操作
            'keyboard': '键盘操作',
            'keyboardKey': '键盘按键',
            'keyboardCombo': '组合键',

            # 等待操作
            'waitTime': '等待时间',
            'waitElement': '等待元素出现',
            'waitRequest': '等待请求完成',

            # 获取数据
            'getUrl': '获取URL',
            'getClipboard': '获取粘贴板内容',
            'getElementData': '元素数据',
            'getCurrentFocus': '当前焦点元素',
            'saveToFile': '存到文件',
            'saveToExcel': '存到Excel',
            'downloadFile': '下载文件',
            'importExcel': '导入Excel素材',
            'importTxt': '导入txt',
            'getEmail': '获取邮件',
            'getAuthCode': '身份验证密码',
            'listenRequest': '监听请求触发',
            'listenResponse': '监听请求结果',
            'stopListen': '停止页面监听',
            'getCookie': '获取页面Cookie',
            'clearCookie': '清除页面Cookie',

            # 数据处理
            'extractText': '文本中提取',
            'convertJson': '转换Json对象',
            'extractField': '字段提取',
            'randomExtract': '随机提取',

            # 环境信息
            'updateNote': '更新环境备注',
            'updateTag': '更新环境标签',

            # 流程管理
            'startBrowser': '启动新浏览器',
            'useOtherFlow': '使用其他流程',
            'ifCondition': 'IF条件',
            'forElement': 'For循环元素',
            'forCount': 'For循环次数',
            'forData': 'For循环数据',
            'whileLoop': 'While循环',
            'exitLoop': '退出循环',
            'closeBrowser': '关闭浏览器'
        }




        # 应用统一的iOS 26 Liquid Glass风格
        self.setStyleSheet(iOS26StyleManager.get_complete_style())

        # 设置窗口属性，确保不阻塞主窗口且可以正常切换
        self.setWindowFlags(
            Qt.Window |  # 独立窗口类型，不阻塞主窗口
            Qt.WindowCloseButtonHint |  # 关闭按钮
            Qt.WindowMinimizeButtonHint |  # 最小化按钮
            Qt.WindowMaximizeButtonHint  # 最大化按钮
        )
        self.setModal(False)  # 非模态对话框
        self.setAttribute(Qt.WA_DeleteOnClose, False)  # 不自动删除，允许重复使用

        # 确保窗口可以正常激活和切换
        self.setAttribute(Qt.WA_ShowWithoutActivating, False)  # 允许正常激活
        self.setWindowModality(Qt.NonModal)  # 非模态

        # 设置窗口保持在前台但不阻塞
        self.setWindowState(Qt.WindowActive)

        # 设置窗口图标（可选）
        try:
            from PyQt5.QtGui import QIcon
            self.setWindowIcon(QIcon())  # 设置空图标或自定义图标
        except:
            pass

        self.init_ui()

        # 如果有流程数据，预填充
        if self.flow_data:
            self.load_flow_data(self.flow_data)

    def init_ui(self):
        """初始化界面 - AdsPower风格"""
        # 应用AdsPower标准样式
        try:
            from ui_style_fix import apply_adspower_style_fixes
            self.setStyleSheet(apply_adspower_style_fixes())
        except ImportError:
            self.setStyleSheet(iOS26StyleManager.get_complete_style())

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 左侧操作选项面板
        self.create_left_panel(main_layout)

        # 右侧主要内容区域
        self.create_right_panel(main_layout)
        
    def create_left_panel(self, main_layout):
        """创建左侧操作选项面板 - AdsPower风格"""
        left_widget = QWidget()
        left_widget.setFixedWidth(260)
        left_widget.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border-right: 1px solid #d9d9d9;
            }
        """)
        
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)
        
        # 顶部搜索区域
        search_widget = QWidget()
        search_widget.setFixedHeight(120)
        search_widget.setStyleSheet("background-color: white; border-bottom: 1px solid #e8e8e8;")
        search_layout = QVBoxLayout(search_widget)
        search_layout.setContentsMargins(15, 15, 15, 15)
        

        
        # 搜索框
        search_input = QLineEdit()
        search_input.setPlaceholderText("关键字搜索")
        search_input.setStyleSheet(iOS26StyleManager.get_input_style())
        search_layout.addWidget(search_input)
        
        left_layout.addWidget(search_widget)
        
        # 滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet(iOS26StyleManager.get_scrollbar_style() + """
            QScrollArea {
                border: none;
                background: transparent;
                border-radius: 16px;
            }
        """)
        
        # 创建操作选项内容
        self.create_operation_options(scroll_area)
        
        left_layout.addWidget(scroll_area)
        main_layout.addWidget(left_widget)
        
    def create_operation_options(self, scroll_area):
        """创建操作选项内容 - 完全按照AdsPower原版样式"""
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # 完全按照AdsPower原版界面排序
        operations = [
            # 页面操作组 - 默认展开，AdsPower最常用功能
            {"type": "group", "title": "页面操作", "expanded": True, "items": [
                "新建标签", "关闭标签", "关闭其他标签", "切换标签",
                "访问网站", "刷新页面", "页面后退", "页面截图",
                "经过元素", "下拉选择器", "元素聚焦", "点击元素",
                "输入内容", "滚动页面", "上传附件", "执行JS脚本"
            ]},

            # 键盘操作组
            {"type": "group", "title": "键盘操作", "expanded": False, "items": [
                "键盘按键", "组合键"
            ]},

            # 等待操作组
            {"type": "group", "title": "等待操作", "expanded": False, "items": [
                "等待时间", "等待元素出现", "等待请求完成"
            ]},

            # 获取数据组
            {"type": "group", "title": "获取数据", "expanded": False, "items": [
                "获取URL", "获取粘贴板内容", "元素数据", "当前焦点元素",
                "存到文件", "存到Excel", "下载文件", "导入Excel素材",
                "导入txt", "获取邮件", "身份验证密码", "监听请求触发",
                "监听请求结果", "停止页面监听", "获取页面Cookie", "清除页面Cookie"
            ]},

            # 数据处理组
            {"type": "group", "title": "数据处理", "expanded": False, "items": [
                "文本中提取", "转换Json对象", "字段提取", "随机提取"
            ]},

            # 环境信息组
            {"type": "group", "title": "环境信息", "expanded": False, "items": [
                "更新环境备注", "更新环境标签"
            ]},

            # 流程管理组
            {"type": "group", "title": "流程管理", "expanded": False, "items": [
                "启动新浏览器", "使用其他流程", "IF条件",
                "For循环元素", "For循环次数", "For循环数据",
                "While循环", "退出循环", "关闭浏览器"
            ]}
        ]

        for operation in operations:
            if operation["type"] == "group":
                self.create_adspower_group(content_layout, operation["title"],
                                         operation["items"], operation["expanded"])
            elif operation["type"] == "special_group":
                # 页面操作特殊分组 - 红色标题，可折叠，包含所有页面操作
                self.create_special_collapsible_group(content_layout, operation["title"], operation["items"])
            elif operation["type"] == "item":
                self.create_adspower_item(content_layout, operation["name"],
                                        operation.get("has_red_dot", False))

        content_layout.addStretch()
        scroll_area.setWidget(content_widget)
        



    def create_right_panel(self, main_layout):
        """创建右侧主要内容区域"""
        right_widget = QWidget()
        right_widget.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.95),
                    stop:1 rgba(255, 255, 255, 0.85));
                backdrop-filter: blur(30px);
            }
        """)

        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        # 顶部标题栏
        self.create_title_bar(right_layout)

        # 任务配置区域
        self.create_task_config_area(right_layout)

        # 流程设计区域
        self.create_flow_design_area(right_layout)

        # 底部按钮区域
        self.create_bottom_buttons(right_layout)

        main_layout.addWidget(right_widget)

    def create_title_bar(self, parent_layout):
        """创建顶部标题栏"""
        title_widget = QWidget()
        title_widget.setFixedHeight(60)
        title_widget.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.9),
                    stop:1 rgba(255, 255, 255, 0.7));
                border-bottom: 1px solid rgba(0, 122, 255, 0.1);
                backdrop-filter: blur(20px);
            }
        """)

        title_layout = QHBoxLayout(title_widget)
        title_layout.setContentsMargins(20, 0, 20, 0)

        # 标题
        title_label = QLabel("任务流程(0)")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: 600;
                color: #333333;
            }
        """)
        title_layout.addWidget(title_label)

        title_layout.addStretch()

        # 右侧按钮组
        buttons = [
            ("搜索流程步骤", "🔍", self.search_flow_steps),
            ("调试", "🐛", self.debug_flow),
            ("调试日志", "📋", self.show_debug_log),
            ("导入", "📥", self.import_flow),
            ("加载", "📂", self.load_flow),
            ("导出", "📤", self.export_flow),
            ("保存", "💾", self.save_flow)
        ]

        for btn_text, icon, callback in buttons:
            btn = QPushButton(f"{icon} {btn_text}")
            btn.setStyleSheet(iOS26StyleManager.get_button_style('secondary'))
            btn.clicked.connect(callback)
            title_layout.addWidget(btn)

        parent_layout.addWidget(title_widget)

    def create_task_config_area(self, parent_layout):
        """创建任务配置区域"""
        config_widget = QWidget()
        config_widget.setFixedHeight(120)
        config_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border-bottom: 1px solid #e8e8e8;
            }
        """)

        config_layout = QVBoxLayout(config_widget)
        config_layout.setContentsMargins(20, 15, 20, 15)
        config_layout.setSpacing(15)

        # 第一行：任务名称
        first_row = QHBoxLayout()

        name_label = QLabel("* 任务名称")
        name_label.setStyleSheet("font-size: 14px; color: #333333; font-weight: 500;")
        name_label.setFixedWidth(80)
        first_row.addWidget(name_label)

        name_input = QLineEdit()
        name_input.setPlaceholderText("请填写任务名称")
        name_input.setStyleSheet(iOS26StyleManager.get_input_style())
        first_row.addWidget(name_input)

        # 其他设置按钮
        other_btn = QPushButton("其他设置")
        other_btn.setStyleSheet(iOS26StyleManager.get_button_style('secondary'))
        first_row.addWidget(other_btn)

        config_layout.addLayout(first_row)

        # 第二行：选择分组和其他设置
        second_row = QHBoxLayout()

        # 选择分组
        group_label = QLabel("选择分组")
        group_label.setStyleSheet("font-size: 14px; color: #333333; font-weight: 500;")
        group_label.setFixedWidth(80)
        second_row.addWidget(group_label)

        group_combo = QComboBox()
        group_combo.addItem("未分组")
        group_combo.setStyleSheet(iOS26StyleManager.get_input_style())
        second_row.addWidget(group_combo)

        second_row.addSpacing(20)

        # 异常处理
        exception_label = QLabel("异常处理")
        exception_label.setStyleSheet("font-size: 14px; color: #333333; font-weight: 500;")
        exception_label.setFixedWidth(80)
        second_row.addWidget(exception_label)

        exception_combo = QComboBox()
        exception_combo.addItem("跳过")
        exception_combo.setStyleSheet("""
            QComboBox {
                padding: 8px 12px;
                border: 1px solid #d9d9d9;
                border-radius: 6px;
                font-size: 14px;
                background-color: white;
                min-width: 100px;
            }
        """)
        second_row.addWidget(exception_combo)

        second_row.addSpacing(20)

        # 任务完成
        complete_label = QLabel("任务完成")
        complete_label.setStyleSheet("font-size: 14px; color: #333333; font-weight: 500;")
        complete_label.setFixedWidth(80)
        second_row.addWidget(complete_label)

        complete_combo = QComboBox()
        complete_combo.addItem("清除标签")
        complete_combo.setStyleSheet("""
            QComboBox {
                padding: 8px 12px;
                border: 1px solid #d9d9d9;
                border-radius: 6px;
                font-size: 14px;
                background-color: white;
                min-width: 100px;
            }
        """)
        second_row.addWidget(complete_combo)

        # 关闭浏览器
        close_browser_label = QLabel("关闭浏览器")
        close_browser_label.setStyleSheet("font-size: 14px; color: #333333; font-weight: 500;")
        close_browser_label.setFixedWidth(80)
        second_row.addWidget(close_browser_label)

        second_row.addStretch()

        config_layout.addLayout(second_row)
        parent_layout.addWidget(config_widget)

    def create_flow_design_area(self, parent_layout):
        """创建流程设计区域 - 带滚动功能"""
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: #fafafa;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #f0f0f0;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background-color: #c0c0c0;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #a0a0a0;
            }
        """)

        # 流程内容容器
        flow_widget = QWidget()
        flow_widget.setStyleSheet("background-color: #fafafa;")

        flow_layout = QVBoxLayout(flow_widget)
        flow_layout.setContentsMargins(0, 0, 0, 0)
        flow_layout.setSpacing(0)

        # 创建流程步骤容器（用于测试滚动功能）
        self.flow_steps_container = QWidget()
        self.flow_steps_container.setStyleSheet("background-color: #fafafa;")
        self.flow_steps_layout = QVBoxLayout(self.flow_steps_container)
        self.flow_steps_layout.setContentsMargins(15, 20, 15, 20)  # 减少左右边距，为按钮留出空间
        self.flow_steps_layout.setSpacing(10)

        # 初始化为空的流程步骤容器

        # 空状态提示（当没有步骤时显示）
        empty_state = QWidget()
        empty_state.setStyleSheet("background-color: #fafafa;")
        empty_layout = QVBoxLayout(empty_state)
        empty_layout.setContentsMargins(50, 100, 50, 100)

        # 图标区域
        icon_widget = QWidget()
        icon_widget.setFixedHeight(120)
        icon_layout = QVBoxLayout(icon_widget)

        # 创建流程图标效果
        icon_container = QWidget()
        icon_container.setFixedSize(200, 80)
        icon_container.setStyleSheet("""
            QWidget {
                background-color: transparent;
            }
        """)

        # 使用简单的方块来模拟流程图
        boxes_layout = QHBoxLayout(icon_container)
        boxes_layout.setContentsMargins(20, 10, 20, 10)
        boxes_layout.setSpacing(15)

        # 创建三个连接的方块
        for i in range(3):
            box = QLabel()
            box.setFixedSize(40, 30)
            box.setStyleSheet("""
                QLabel {
                    background-color: #e6f7ff;
                    border: 2px solid #91d5ff;
                    border-radius: 6px;
                }
            """)
            boxes_layout.addWidget(box)

            # 添加连接线（除了最后一个）
            if i < 2:
                line = QLabel("→")
                line.setStyleSheet("""
                    QLabel {
                        color: #91d5ff;
                        font-size: 16px;
                        font-weight: bold;
                    }
                """)
                line.setAlignment(Qt.AlignCenter)
                boxes_layout.addWidget(line)

        icon_layout.addWidget(icon_container, 0, Qt.AlignCenter)
        empty_layout.addWidget(icon_widget)

        # 提示文字
        tip_label = QLabel("拖动左边的操作选项添加到流程步骤")
        tip_label.setAlignment(Qt.AlignCenter)
        tip_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #8c8c8c;
                font-weight: 500;
                margin-top: 20px;
            }
        """)
        empty_layout.addWidget(tip_label)

        # 鼠标指针图标
        pointer_label = QLabel("👆")
        pointer_label.setAlignment(Qt.AlignCenter)
        pointer_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                margin-top: 10px;
            }
        """)
        empty_layout.addWidget(pointer_label)

        empty_layout.addStretch()

        # 默认显示空状态，当添加步骤时再切换
        flow_layout.addWidget(empty_state)

        # 保存引用以便后续切换
        self.empty_state = empty_state
        self.flow_widget = flow_widget
        self.flow_layout = flow_layout

        # 设置滚动区域的内容
        scroll_area.setWidget(flow_widget)
        parent_layout.addWidget(scroll_area)

    def create_flow_step(self, title, description):
        """创建流程步骤项目"""
        step_widget = QWidget()
        step_widget.setFixedHeight(90)  # 增加高度以确保按钮可见
        step_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid #e8e8e8;
                border-radius: 8px;
                margin: 2px;
            }
            QWidget:hover {
                border-color: #1890ff;
                background-color: #f8f9fa;
            }
        """)

        step_layout = QHBoxLayout(step_widget)
        step_layout.setContentsMargins(15, 15, 15, 15)  # 增加边距

        # 步骤序号
        step_number = QLabel("1")
        step_number.setFixedSize(30, 30)
        step_number.setAlignment(Qt.AlignCenter)
        step_number.setStyleSheet("""
            QLabel {
                background-color: #1890ff;
                color: white;
                border-radius: 15px;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        step_layout.addWidget(step_number)

        # 步骤内容 - 限制宽度确保按钮可见
        content_widget = QWidget()
        content_widget.setMaximumWidth(600)  # 限制最大宽度
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(5)

        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: 600;
                color: #333333;
            }
        """)
        title_label.setWordWrap(True)  # 允许换行
        content_layout.addWidget(title_label)

        desc_label = QLabel(description)
        desc_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #666666;
            }
        """)
        desc_label.setWordWrap(True)  # 允许换行
        desc_label.setMaximumWidth(580)  # 限制描述文本宽度
        content_layout.addWidget(desc_label)

        step_layout.addWidget(content_widget)

        # 添加一个固定宽度的间隔，确保按钮区域不被挤压
        step_layout.addSpacing(20)

        # 操作按钮容器 - 固定宽度确保按钮始终可见
        button_container = QWidget()
        button_container.setFixedWidth(180)  # 固定按钮区域宽度
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(10)

        # 编辑按钮
        edit_btn = QPushButton("编辑")
        edit_btn.setFixedSize(80, 36)
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #f0f8ff;
                color: #1890ff;
                border: 2px solid #1890ff;
                border-radius: 6px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #1890ff;
                color: white;
            }
            QPushButton:pressed {
                background-color: #096dd9;
            }
        """)
        edit_btn.clicked.connect(lambda: self.edit_step(step_widget, title, description))
        button_layout.addWidget(edit_btn)

        # 删除按钮
        delete_btn = QPushButton("删除")
        delete_btn.setFixedSize(80, 36)
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #fff2f0;
                color: #ff4d4f;
                border: 2px solid #ff4d4f;
                border-radius: 6px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #ff4d4f;
                color: white;
            }
            QPushButton:pressed {
                background-color: #d9363e;
            }
        """)
        delete_btn.clicked.connect(lambda: self.delete_step(step_widget))
        button_layout.addWidget(delete_btn)

        step_layout.addWidget(button_container)

        return step_widget

    def edit_step(self, step_widget, title, description):
        """编辑流程步骤 - 支持完整配置编辑"""
        # 检查步骤是否有配置数据
        if hasattr(step_widget, 'config_data') and hasattr(step_widget, 'operation_type'):
            # 有配置数据，打开完整的配置编辑对话框
            self.edit_step_with_config(step_widget)
        else:
            # 没有配置数据，使用简单的文本编辑
            self.edit_step_simple(step_widget, title, description)

    def edit_step_with_config(self, step_widget):
        """编辑有配置数据的步骤"""
        from PyQt5.QtWidgets import QDialog

        try:
            operation_type = step_widget.operation_type
            config_data = step_widget.config_data.copy()  # 复制配置数据

            # 打开配置对话框 - 优先使用精确配置系统
            try:
                from adspower_rpa_config_exact import AdsPowerRPAConfigDialog
                config_dialog = AdsPowerRPAConfigDialog(operation_type, self)
                # 设置当前配置数据
                config_dialog.config_data = config_data
            except ImportError:
                # 备用：使用原有配置系统
                from rpa_operation_config import RPAOperationConfigDialog
                config_dialog = RPAOperationConfigDialog(operation_type, self)
                # 设置当前配置数据
                config_dialog.set_config_data(config_data)

            # 设置当前配置数据
            config_dialog.set_config_data(config_data)

            if config_dialog.exec_() == QDialog.Accepted:
                # 获取新的配置数据
                new_config_data = config_dialog.get_config_data()

                # 更新步骤的配置数据
                step_widget.config_data = new_config_data

                # 重新生成步骤描述
                new_description = self.format_step_description(new_config_data)

                # 更新步骤显示
                step_title = f"步骤 {self.get_step_number(step_widget)}: {operation_type}"
                self.update_step_display(step_widget, step_title, new_description)

                print(f"步骤配置已更新: {operation_type}")

        except Exception as e:
            print(f"编辑步骤配置时出错: {e}")
            # 如果配置编辑失败，回退到简单编辑
            self.edit_step_simple(step_widget,
                                self.get_step_title(step_widget),
                                self.get_step_description(step_widget))

    def edit_step_simple(self, step_widget, title, description):
        """简单的步骤文本编辑"""
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox

        dialog = QDialog(self)
        dialog.setWindowTitle("编辑步骤")
        dialog.setFixedSize(500, 400)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
            }
        """)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # 标题编辑
        title_label = QLabel("步骤标题:")
        title_label.setStyleSheet("font-size: 14px; font-weight: 500; color: #333333;")
        layout.addWidget(title_label)

        title_edit = QLineEdit(title)
        title_edit.setStyleSheet("""
            QLineEdit {
                padding: 8px 12px;
                border: 1px solid #d9d9d9;
                border-radius: 6px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #1890ff;
            }
        """)
        layout.addWidget(title_edit)

        # 描述编辑
        desc_label = QLabel("步骤描述:")
        desc_label.setStyleSheet("font-size: 14px; font-weight: 500; color: #333333;")
        layout.addWidget(desc_label)

        desc_edit = QTextEdit(description)
        desc_edit.setFixedHeight(150)
        desc_edit.setStyleSheet("""
            QTextEdit {
                padding: 8px 12px;
                border: 1px solid #d9d9d9;
                border-radius: 6px;
                font-size: 14px;
            }
            QTextEdit:focus {
                border-color: #1890ff;
            }
        """)
        layout.addWidget(desc_edit)

        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        cancel_btn = QPushButton("取消")
        cancel_btn.setFixedSize(80, 36)
        cancel_btn.setStyleSheet("""
            QPushButton {
                border: 1px solid #d9d9d9;
                border-radius: 6px;
                background-color: white;
                color: #333333;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
            }
        """)
        cancel_btn.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_btn)

        save_btn = QPushButton("保存")
        save_btn.setFixedSize(80, 36)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #1890ff;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #40a9ff;
            }
        """)

        def save_changes():
            new_title = title_edit.text().strip()
            new_desc = desc_edit.toPlainText().strip()

            if not new_title:
                QMessageBox.warning(dialog, "警告", "步骤标题不能为空")
                return

            # 更新步骤显示
            self.update_step_display(step_widget, new_title, new_desc)
            dialog.accept()

        save_btn.clicked.connect(save_changes)
        button_layout.addWidget(save_btn)

        layout.addLayout(button_layout)
        dialog.exec_()

    def get_step_number(self, step_widget):
        """获取步骤编号"""
        for i in range(self.flow_steps_layout.count()):
            item = self.flow_steps_layout.itemAt(i)
            if item and item.widget() == step_widget:
                return i + 1
        return 1

    def get_step_title(self, step_widget):
        """获取步骤标题"""
        labels = step_widget.findChildren(QLabel)
        for label in labels:
            if label.styleSheet() and "font-weight: 600" in label.styleSheet():
                return label.text()
        return "未知步骤"

    def get_step_description(self, step_widget):
        """获取步骤描述"""
        labels = step_widget.findChildren(QLabel)
        for label in labels:
            if label.styleSheet() and "color: #666666" in label.styleSheet():
                return label.text()
        return "无描述"

    def delete_step(self, step_widget):
        """删除流程步骤"""
        from PyQt5.QtWidgets import QMessageBox

        reply = QMessageBox.question(self, "确认删除",
                                   "确定要删除这个步骤吗？",
                                   QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            # 从布局中移除步骤
            self.flow_steps_layout.removeWidget(step_widget)
            step_widget.deleteLater()

            # 重新编号剩余步骤
            self.renumber_steps()

            # 如果没有步骤了，切换回空状态
            if self.flow_steps_layout.count() == 0:
                self.flow_layout.removeWidget(self.flow_steps_container)
                self.flow_steps_container.setParent(None)
                self.flow_layout.addWidget(self.empty_state)

    def update_step_display(self, step_widget, new_title, new_desc):
        """更新步骤显示内容"""
        # 查找步骤中的标题和描述标签并更新
        labels = step_widget.findChildren(QLabel)
        for child in labels:
            # 更新标题（查找有font-weight: 600样式的标签）
            if child.styleSheet() and "font-weight: 600" in child.styleSheet():
                child.setText(new_title)
            # 更新描述（查找有color: #666666样式的标签）
            elif child.styleSheet() and "color: #666666" in child.styleSheet():
                child.setText(new_desc)

    def renumber_steps(self):
        """重新编号步骤"""
        for i in range(self.flow_steps_layout.count()):
            item = self.flow_steps_layout.itemAt(i)
            if item and item.widget():
                step_widget = item.widget()
                # 更新步骤编号
                for child in step_widget.findChildren(QLabel):
                    if child.styleSheet() and "background-color: #1890ff" in child.styleSheet():
                        child.setText(str(i + 1))
                        break

    def add_operation_to_flow(self, operation_name):
        """添加操作到流程中"""
        # 打开参数配置对话框 - 优先使用精确配置系统
        try:
            from adspower_rpa_config_exact import AdsPowerRPAConfigDialog
            config_dialog = AdsPowerRPAConfigDialog(operation_name, self)
            if config_dialog.exec_() == QDialog.Accepted:
                config_data = config_dialog.config_data
        except ImportError:
            # 备用：使用原有配置系统
            from rpa_operation_config import RPAOperationConfigDialog
            config_dialog = RPAOperationConfigDialog(operation_name, self)
            if config_dialog.exec_() == QDialog.Accepted:
                config_data = config_dialog.get_config_data()
            else:
                return

        if config_dialog.result() == QDialog.Accepted:

            # 获取当前步骤数量
            current_step_count = self.flow_steps_layout.count()
            step_number = current_step_count + 1

            # 创建新的流程步骤
            step_title = f"步骤 {step_number}: {operation_name}"
            step_description = self.format_step_description(config_data)

            # 创建步骤widget
            step_widget = self.create_flow_step(step_title, step_description)

            # 保存配置数据和操作类型到步骤widget
            step_widget.config_data = config_data
            step_widget.operation_type = operation_name
            step_widget.operation_name = operation_name

            # 添加到流程布局中
            self.flow_steps_layout.addWidget(step_widget)

            # 如果这是第一个步骤，需要切换显示
            if current_step_count == 0:
                # 清除当前布局并添加步骤容器
                self.flow_layout.removeWidget(self.empty_state)
                self.empty_state.setParent(None)
                self.flow_layout.addWidget(self.flow_steps_container)

            # 自动保存流程数据
            self.auto_save_flow()

    def auto_save_flow(self):
        """自动保存流程数据"""
        try:
            # 获取任务名称
            task_name = ""
            for widget in self.findChildren(QLineEdit):
                if widget.placeholderText() == "请填写任务名称":
                    task_name = widget.text().strip()
                    break

            # 如果没有任务名称，使用默认名称
            if not task_name:
                from PyQt5.QtCore import QDateTime
                current_time = QDateTime.currentDateTime().toString("yyyyMMdd_hhmmss")
                task_name = f"自动保存_{current_time}"
                # 设置任务名称到输入框
                for widget in self.findChildren(QLineEdit):
                    if widget.placeholderText() == "请填写任务名称":
                        widget.setText(task_name)
                        break

            # 收集流程数据
            steps = []
            for i in range(self.flow_steps_layout.count()):
                item = self.flow_steps_layout.itemAt(i)
                if item and item.widget():
                    step_widget = item.widget()
                    # 提取步骤信息
                    title = ""
                    description = ""
                    for child in step_widget.findChildren(QLabel):
                        if child.styleSheet() and "font-weight: 600" in child.styleSheet():
                            title = child.text()
                        elif child.styleSheet() and "color: #666666" in child.styleSheet():
                            description = child.text()

                    # 获取完整的步骤配置
                    config_data = getattr(step_widget, 'config_data', {})
                    operation_type = getattr(step_widget, 'operation_type', '')
                    operation_name = getattr(step_widget, 'operation_name', '')

                    # 确保配置数据包含操作类型
                    if operation_type and 'operation' not in config_data:
                        config_data['operation'] = operation_type

                    steps.append({
                        "title": title,
                        "description": description,
                        "config": config_data,
                        "operation_type": operation_type,
                        "operation_name": operation_name
                    })

            flow_data = {
                "name": task_name,
                "steps": steps,
                "save_time": QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss"),
                "auto_saved": True
            }

            # 保存到data目录
            import os
            import json
            os.makedirs("data", exist_ok=True)
            file_path = f"data/{task_name}_flow.json"

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(flow_data, f, ensure_ascii=False, indent=2)

            print(f"自动保存流程成功: {file_path}")

        except Exception as e:
            print(f"自动保存流程失败: {e}")

    def format_step_description(self, config_data):
        """格式化步骤描述"""
        operation = config_data.get("operation", "")

        # 根据不同操作类型生成详细描述
        if operation == "前往网址":
            url = config_data.get('goto_url', '未指定URL')
            return f"前往网址: {url}"
        elif operation == "点击":
            selector = config_data.get('click_selector', '未指定选择器')
            return f"点击元素: {selector}"
        elif operation == "等待时间":
            wait_type = config_data.get('wait_type', '固定时间')
            if wait_type == '随机时间':
                min_time = config_data.get('wait_min', 3)
                max_time = config_data.get('wait_max', 5)
                return f"等待时间: {min_time}-{max_time}秒"
            else:
                wait_time = config_data.get('wait_min', 3)
                return f"等待时间: {wait_time}秒"
        elif operation == "获取元素":
            selector = config_data.get('get_element_selector', '未指定选择器')
            save_var = config_data.get('save_variable', '未指定变量')
            return f"获取元素: {selector} → {save_var}"
        elif operation == "执行JS脚本":
            js_code = config_data.get('js_code', '')
            return f"执行JS: {js_code[:30]}..."
        elif operation == "IF条件":
            variable = config_data.get('if_variable', '')
            condition = config_data.get('if_condition', '')
            return f"IF条件: {variable} {condition}"
        elif operation == "For循环元素":
            selector = config_data.get('for_element_selector', '')
            return f"For循环元素: {selector}"
        elif operation == "启动新浏览器":
            env_id = config_data.get('browser_env_id', '')
            return f"启动浏览器: 环境{env_id}"
        elif operation == "悬停":
            selector = config_data.get('hover_selector', '')
            return f"悬停元素: {selector}"
        elif operation == "等待元素":
            selector = config_data.get('wait_element_selector', '')
            condition = config_data.get('wait_condition', '出现')
            return f"等待元素{condition}: {selector}"
        elif operation == "获取页面":
            info_type = config_data.get('page_info_type', '页面标题')
            return f"获取页面{info_type}"
        elif operation == "文本中提取":
            source_var = config_data.get('source_variable', '')
            pattern = config_data.get('extract_pattern', '')[:20]
            return f"文本提取: {source_var} → {pattern}..."
        else:
            # 通用描述生成
            description_parts = []

            # 检查常见字段
            key_fields = [
                ('goto_url', 'URL'),
                ('click_selector', '选择器'),
                ('hover_selector', '选择器'),
                ('wait_element_selector', '选择器'),
                ('get_element_selector', '选择器'),
                ('source_variable', '源变量'),
                ('if_variable', '变量'),
                ('browser_env_id', '环境ID'),
                ('captcha_type', '验证码类型'),
                ('openai_model', '模型')
            ]

            for field, label in key_fields:
                if config_data.get(field):
                    description_parts.append(f"{label}: {config_data[field]}")
                    break

            return " | ".join(description_parts) if description_parts else f"{operation}操作"

    def format_imported_step_description(self, step):
        """格式化导入步骤的描述"""
        try:
            # 获取步骤配置
            config = step.get('config', {})
            operation_type = step.get('type', '')

            # 根据操作类型格式化描述
            if operation_type == 'gotoUrl':
                url = config.get('url', '未指定URL')
                timeout = config.get('timeout', 30000)
                return f"访问网址: {url} (超时: {timeout/1000}秒)"

            elif operation_type == 'waitTime':
                timeout_type = config.get('timeoutType', 'randomInterval')
                timeout_val = config.get('timeout', 10000)
                timeout_min = config.get('timeoutMin', 8000)
                timeout_max = config.get('timeoutMax', 12000)

                if timeout_type == 'randomInterval':
                    return f"等待时间: {timeout_min/1000}-{timeout_max/1000}秒 (随机)"
                else:
                    return f"等待时间: {timeout_val/1000}秒"

            elif operation_type == 'click':
                selector_radio = config.get('selectorRadio', 'XPath')
                selector = config.get('selector', '')
                element_num = config.get('element', 1)
                return f"点击元素: {selector} (第{element_num}个, {selector_radio})"

            elif operation_type == 'scrollPage':
                range_type = config.get('rangeType', 'window')
                scroll_type = config.get('scrollType', 'position')
                position = config.get('position', 'bottom')
                distance = config.get('distance', 0)

                if scroll_type == 'position':
                    return f"滚动页面: 滚动到{position} ({range_type})"
                else:
                    return f"滚动页面: 滚动{distance}像素 ({range_type})"

            elif operation_type == 'newPage':
                return "新建标签页"

            elif operation_type == 'input' or operation_type == 'inputContent':
                selector = config.get('selector', '')
                content = config.get('content', '')
                element_num = config.get('element', 1)
                # 按照AdsPower格式显示
                return f"selector: {selector[:50]}{'...' if len(selector) > 50 else ''} | element: {element_num} | content: {content[:30]}{'...' if len(content) > 30 else ''}"

            elif operation_type == 'keyboard':
                # 处理keyboard操作，显示为中文
                key_type = config.get('keyType', 'key')
                key_value = config.get('key', '')
                modifier_keys = config.get('modifierKeys', [])

                # 如果key_value为空，尝试从keyType获取
                if not key_value and key_type:
                    key_value = key_type

                if modifier_keys:
                    return f"键盘操作: {'+'.join(modifier_keys)}+{key_value}"
                else:
                    return f"键盘操作: {key_value}" if key_value else "键盘操作"

            elif operation_type == 'hoverElement':
                selector = config.get('selector', '')
                return f"悬停元素: {selector}"

            else:
                # 通用格式化
                if isinstance(config, dict) and config:
                    # 提取关键信息
                    key_info = []
                    for key, value in config.items():
                        if key in ['url', 'selector', 'content', 'timeout', 'element']:
                            if isinstance(value, str) and len(value) > 30:
                                value = value[:30] + "..."
                            key_info.append(f"{key}: {value}")

                    if key_info:
                        return " | ".join(key_info[:3])  # 最多显示3个关键信息

                return f"{operation_type} 操作"

        except Exception as e:
            return f"导入的步骤 (解析错误: {str(e)})"

    def create_bottom_buttons(self, parent_layout):
        """创建底部按钮区域"""
        button_widget = QWidget()
        button_widget.setFixedHeight(70)
        button_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border-top: 1px solid #e8e8e8;
            }
        """)

        button_layout = QHBoxLayout(button_widget)
        button_layout.setContentsMargins(20, 15, 20, 15)

        button_layout.addStretch()

        # 取消按钮
        cancel_btn = QPushButton("取消")
        cancel_btn.setFixedSize(80, 36)
        cancel_btn.setStyleSheet("""
            QPushButton {
                border: 1px solid #d9d9d9;
                border-radius: 6px;
                background-color: white;
                color: #333333;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
                border-color: #40a9ff;
            }
        """)
        cancel_btn.clicked.connect(self.handle_cancel)
        button_layout.addWidget(cancel_btn)

        button_layout.addSpacing(10)

        # 添加按钮
        add_btn = QPushButton("✓ 添加")
        add_btn.setFixedSize(80, 36)
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #1890ff;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #40a9ff;
            }
            QPushButton:pressed {
                background-color: #096dd9;
            }
        """)
        add_btn.clicked.connect(self.handle_accept)
        button_layout.addWidget(add_btn)

        parent_layout.addWidget(button_widget)

    def create_adspower_group(self, parent_layout, title, items, expanded=True):
        """创建AdsPower样式的分组 - 完全按照截图样式"""
        # 分组标题
        title_widget = QWidget()
        title_widget.setFixedHeight(36)
        title_widget.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border-bottom: 1px solid #e8e8e8;
            }
            QWidget:hover {
                background-color: #f0f0f0;
            }
        """)

        title_layout = QHBoxLayout(title_widget)
        title_layout.setContentsMargins(15, 0, 15, 0)

        # 折叠图标
        collapse_icon = QLabel("▼" if expanded else "▶")
        collapse_icon.setStyleSheet("""
            QLabel {
                font-size: 10px;
                color: #666666;
                font-weight: bold;
            }
        """)
        title_layout.addWidget(collapse_icon)

        # 标题文字
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 13px;
                font-weight: 500;
                color: #333333;
                margin-left: 8px;
                font-family: "Microsoft YaHei", Arial, sans-serif;
            }
        """)
        title_layout.addWidget(title_label)
        title_layout.addStretch()

        parent_layout.addWidget(title_widget)

        # 创建分组项目容器
        items_container = QWidget()
        items_layout = QVBoxLayout(items_container)
        items_layout.setContentsMargins(0, 0, 0, 0)
        items_layout.setSpacing(0)

        # 添加分组项目
        for item in items:
            self.create_adspower_group_item(items_layout, item)

        # 设置初始显示状态
        items_container.setVisible(expanded)
        parent_layout.addWidget(items_container)

        # 添加点击事件处理
        def toggle_group():
            is_visible = items_container.isVisible()
            items_container.setVisible(not is_visible)
            collapse_icon.setText("▶" if is_visible else "▼")

        title_widget.mousePressEvent = lambda event: toggle_group()

    def create_adspower_group_item(self, parent_layout, item_name):
        """创建AdsPower样式的分组内项目"""
        item_widget = QWidget()
        item_widget.setFixedHeight(34)
        item_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border-bottom: 1px solid #f8f8f8;
            }
            QWidget:hover {
                background-color: #f8f9fa;
            }
        """)

        item_layout = QHBoxLayout(item_widget)
        item_layout.setContentsMargins(35, 0, 15, 0)

        item_label = QLabel(item_name)
        item_label.setStyleSheet("""
            QLabel {
                font-size: 13px;
                color: #333333;
                font-family: "Microsoft YaHei", Arial, sans-serif;
            }
        """)
        item_layout.addWidget(item_label)
        item_layout.addStretch()

        # 添加按钮 - 圆形样式
        add_btn = QPushButton("+")
        add_btn.setFixedSize(20, 20)
        add_btn.setStyleSheet("""
            QPushButton {
                border: 1px solid #d9d9d9;
                border-radius: 10px;
                background-color: white;
                font-size: 12px;
                font-weight: bold;
                color: #666666;
            }
            QPushButton:hover {
                background-color: #1890ff;
                color: white;
                border-color: #1890ff;
            }
        """)
        add_btn.clicked.connect(lambda: self.add_operation_to_flow(item_name))
        item_layout.addWidget(add_btn)

        parent_layout.addWidget(item_widget)

    def create_adspower_item(self, parent_layout, item_name, has_red_dot=False):
        """创建AdsPower样式的单独项目"""
        item_widget = QWidget()
        item_widget.setFixedHeight(36)
        item_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border-bottom: 1px solid #f8f8f8;
            }
            QWidget:hover {
                background-color: #f8f9fa;
            }
        """)

        item_layout = QHBoxLayout(item_widget)
        item_layout.setContentsMargins(15, 0, 15, 0)

        # 红色圆点（如果需要）
        if has_red_dot:
            red_dot = QLabel("●")
            red_dot.setStyleSheet("""
                QLabel {
                    color: #ff4d4f;
                    font-size: 8px;
                    margin-right: 5px;
                }
            """)
            item_layout.addWidget(red_dot)

        item_label = QLabel(item_name)
        item_label.setStyleSheet("""
            QLabel {
                font-size: 13px;
                color: #333333;
                font-family: "Microsoft YaHei", Arial, sans-serif;
            }
        """)
        item_layout.addWidget(item_label)
        item_layout.addStretch()

        # 添加按钮 - 圆形样式
        add_btn = QPushButton("+")
        add_btn.setFixedSize(20, 20)
        add_btn.setStyleSheet("""
            QPushButton {
                border: 1px solid #d9d9d9;
                border-radius: 10px;
                background-color: white;
                font-size: 12px;
                font-weight: bold;
                color: #666666;
            }
            QPushButton:hover {
                background-color: #1890ff;
                color: white;
                border-color: #1890ff;
            }
        """)
        add_btn.clicked.connect(lambda: self.add_operation_to_flow(item_name))
        item_layout.addWidget(add_btn)

        parent_layout.addWidget(item_widget)


    def create_special_collapsible_group(self, parent_layout, title, items):
        """创建特殊可折叠分组 - 页面操作的特殊样式，支持折叠"""
        # 分组标题 - 修复红线问题，使用更合适的样式
        title_widget = QWidget()
        title_widget.setFixedHeight(40)
        title_widget.setStyleSheet("""
            QWidget {
                background-color: #fafafa;
                border-bottom: 1px solid #e8e8e8;
                border-left: 3px solid #1890ff;
            }
            QWidget:hover {
                background-color: #f0f8ff;
            }
        """)

        title_layout = QHBoxLayout(title_widget)
        title_layout.setContentsMargins(15, 0, 15, 0)

        # 折叠图标 - 蓝色主题
        collapse_icon = QLabel("▶")  # 默认折叠状态
        collapse_icon.setStyleSheet("""
            QLabel {
                font-size: 10px;
                color: #1890ff;
                font-weight: bold;
            }
        """)
        title_layout.addWidget(collapse_icon)

        # 标题文字 - 蓝色主题
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: 600;
                color: #1890ff;
                font-family: "Microsoft YaHei", Arial, sans-serif;
                margin-left: 8px;
            }
        """)
        title_layout.addWidget(title_label)
        title_layout.addStretch()

        parent_layout.addWidget(title_widget)

        # 创建分组项目容器
        items_container = QWidget()
        items_layout = QVBoxLayout(items_container)
        items_layout.setContentsMargins(0, 0, 0, 0)
        items_layout.setSpacing(0)

        # 添加分组项目
        for item in items:
            self.create_page_operation_item(items_layout, item)

        # 设置初始显示状态（折叠）
        items_container.setVisible(False)
        parent_layout.addWidget(items_container)

        # 添加点击事件处理
        def toggle_group():
            is_visible = items_container.isVisible()
            items_container.setVisible(not is_visible)
            collapse_icon.setText("▶" if is_visible else "▼")

        title_widget.mousePressEvent = lambda event: toggle_group()

    def create_page_operation_item(self, parent_layout, item_name):
        """创建页面操作项 - 修复红线问题的特殊样式"""
        item_widget = QWidget()
        item_widget.setFixedHeight(36)
        item_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border-bottom: 1px solid #f8f8f8;
            }
            QWidget:hover {
                background-color: #f0f8ff;
            }
        """)

        item_layout = QHBoxLayout(item_widget)
        item_layout.setContentsMargins(25, 0, 15, 0)

        item_label = QLabel(item_name)
        item_label.setStyleSheet("""
            QLabel {
                font-size: 13px;
                color: #333333;
                font-family: "Microsoft YaHei", Arial, sans-serif;
            }
        """)
        item_layout.addWidget(item_label)
        item_layout.addStretch()

        # 添加按钮 - 修复红线问题，使用蓝色主题
        add_btn = QPushButton("+")
        add_btn.setFixedSize(20, 20)
        add_btn.setStyleSheet("""
            QPushButton {
                border: 1px solid #d9d9d9;
                border-radius: 10px;
                background-color: white;
                font-size: 12px;
                font-weight: bold;
                color: #666666;
            }
            QPushButton:hover {
                background-color: #1890ff;
                color: white;
                border-color: #1890ff;
            }
        """)
        add_btn.clicked.connect(lambda: self.add_operation_to_flow(item_name))
        item_layout.addWidget(add_btn)

        parent_layout.addWidget(item_widget)

    def create_collapsible_section(self, parent_layout, title, items, collapsed=True):
        """创建可折叠分组"""
        # 分组标题
        title_widget = QWidget()
        title_widget.setFixedHeight(36)
        title_widget.setStyleSheet("""
            QWidget {
                background-color: #fafafa;
                border-bottom: 1px solid #e8e8e8;
            }
            QWidget:hover {
                background-color: #f0f0f0;
            }
        """)

        title_layout = QHBoxLayout(title_widget)
        title_layout.setContentsMargins(15, 0, 15, 0)

        # 折叠图标
        collapse_icon = QLabel("▶" if collapsed else "▼")
        collapse_icon.setStyleSheet("""
            QLabel {
                font-size: 10px;
                color: #666666;
                font-weight: bold;
            }
        """)
        title_layout.addWidget(collapse_icon)

        # 标题文字
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 13px;
                font-weight: 500;
                color: #333333;
                margin-left: 8px;
                font-family: "Microsoft YaHei", Arial, sans-serif;
            }
        """)
        title_layout.addWidget(title_label)
        title_layout.addStretch()

        parent_layout.addWidget(title_widget)

        # 分组项目 - 只有未折叠时才显示
        if not collapsed:
            for item in items:
                self.create_group_operation_item(parent_layout, item)

    def create_group_operation_item(self, parent_layout, item_name):
        """创建分组内的操作项"""
        item_widget = QWidget()
        item_widget.setFixedHeight(34)
        item_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border-bottom: 1px solid #f8f8f8;
            }
            QWidget:hover {
                background-color: #f8f9fa;
            }
        """)

        item_layout = QHBoxLayout(item_widget)
        item_layout.setContentsMargins(35, 0, 15, 0)

        item_label = QLabel(item_name)
        item_label.setStyleSheet("""
            QLabel {
                font-size: 13px;
                color: #333333;
                font-family: "Microsoft YaHei", Arial, sans-serif;
            }
        """)
        item_layout.addWidget(item_label)
        item_layout.addStretch()

        # 添加按钮
        add_btn = QPushButton("+")
        add_btn.setFixedSize(20, 20)
        add_btn.setStyleSheet("""
            QPushButton {
                border: 1px solid #d9d9d9;
                border-radius: 10px;
                background-color: white;
                font-size: 12px;
                font-weight: bold;
                color: #666666;
            }
            QPushButton:hover {
                background-color: #1890ff;
                color: white;
                border-color: #1890ff;
            }
        """)
        add_btn.clicked.connect(lambda: self.add_operation_to_flow(item_name))
        item_layout.addWidget(add_btn)

        parent_layout.addWidget(item_widget)

    def get_flow_data(self):
        """获取流程数据"""
        from PyQt5.QtCore import QDateTime

        # 获取任务名称
        task_name = "新建流程"
        for widget in self.findChildren(QLineEdit):
            if widget.placeholderText() == "请填写任务名称":
                task_name = widget.text() or "新建流程"
                break

        # 获取选择的分组
        group_name = "未分组"
        for widget in self.findChildren(QComboBox):
            if "未分组" in [widget.itemText(i) for i in range(widget.count())]:
                group_name = widget.currentText()
                break

        # 收集当前添加的流程步骤
        steps = []
        for i in range(self.flow_steps_layout.count()):
            item = self.flow_steps_layout.itemAt(i)
            if item and item.widget():
                step_widget = item.widget()
                # 提取步骤信息
                title = ""
                description = ""
                for child in step_widget.findChildren(QLabel):
                    if child.styleSheet() and "font-weight: 600" in child.styleSheet():
                        title = child.text()
                    elif child.styleSheet() and "color: #666666" in child.styleSheet():
                        description = child.text()

                steps.append({
                    "title": title,
                    "description": description,
                    "config": getattr(step_widget, 'config_data', {}),
                    "type": getattr(step_widget, 'operation_type', 'unknown'),
                    "step_number": i + 1
                })

        # 返回创建的流程数据
        return {
            "name": task_name,
            "group": group_name,
            "created_time": QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss"),
            "steps": steps,
            "status": "未运行",
            "description": f"任务流程: {task_name}",
            "step_count": len(steps)
        }

    def search_flow_steps(self):
        """搜索流程步骤功能"""
        from PyQt5.QtWidgets import QInputDialog, QMessageBox

        text, ok = QInputDialog.getText(self, '搜索流程步骤', '请输入搜索关键词:')
        if ok and text:
            # 搜索逻辑
            found_steps = []
            for i in range(self.flow_steps_layout.count()):
                item = self.flow_steps_layout.itemAt(i)
                if item and item.widget():
                    step_widget = item.widget()
                    # 在步骤标题和描述中搜索
                    for child in step_widget.findChildren(QLabel):
                        if text.lower() in child.text().lower():
                            found_steps.append(i + 1)
                            break

            if found_steps:
                QMessageBox.information(self, "搜索结果",
                                      f"找到 {len(found_steps)} 个匹配的步骤:\n步骤 {', '.join(map(str, found_steps))}")
            else:
                QMessageBox.information(self, "搜索结果", "未找到匹配的步骤")

    def debug_flow(self):
        """调试流程功能 - AdsPower样式"""
        from debug_dialog import DebugDialog
        from PyQt5.QtWidgets import QMessageBox

        # 检查是否有流程步骤
        if self.flow_steps_layout.count() == 0:
            QMessageBox.warning(self, "调试", "当前没有流程步骤可以调试")
            return

        # 打开调试对话框
        debug_dialog = DebugDialog(self)
        if debug_dialog.exec_() == debug_dialog.Accepted:
            env_id = debug_dialog.get_env_id()

            # 显示调试日志并开始执行
            self.show_debug_log_and_execute(env_id)

    def show_debug_log_and_execute(self, env_id):
        """显示调试日志并执行RPA流程"""
        from debug_log_dialog import DebugLogDialog
        from PyQt5.QtCore import QThread, pyqtSignal, QTimer
        import time

        # 创建调试日志对话框
        log_dialog = DebugLogDialog(self)

        # 创建真实RPA执行线程
        class RealRPAExecutionThread(QThread):
            log_signal = pyqtSignal(str, str)  # message, log_type
            finished_signal = pyqtSignal()

            def __init__(self, flow_steps_layout, env_id, api_instance=None):
                super().__init__()
                self.flow_steps_layout = flow_steps_layout
                self.env_id = env_id
                self.driver = None
                self.api = api_instance  # 直接传递API实例

            def run(self):
                try:
                    self.log_signal.emit("开始执行任务", "info")

                    # 尝试启动真实浏览器
                    if self.start_real_browser():
                        # 执行每个步骤
                        for i in range(self.flow_steps_layout.count()):
                            item = self.flow_steps_layout.itemAt(i)
                            if item and item.widget():
                                step_widget = item.widget()

                                # 获取步骤信息
                                operation_type = getattr(step_widget, 'operation_type', '')
                                config_data = getattr(step_widget, 'config_data', {})

                                # 执行步骤
                                self.execute_real_step(operation_type, config_data, i + 1)

                        self.log_signal.emit("任务执行完成", "success")
                    else:
                        self.log_signal.emit("无法启动浏览器，使用模拟模式", "warning")
                        self.simulate_execution()

                    self.finished_signal.emit()

                except Exception as e:
                    self.log_signal.emit(f"执行出错: {str(e)}", "error")
                    self.finished_signal.emit()
                finally:
                    self.cleanup_browser()

            def start_real_browser(self):
                """启动真实浏览器 - 通过AdsPower API"""
                try:
                    # 使用传递的API实例
                    if self.api:
                        api = self.api
                        self.log_signal.emit(f"使用传递的API实例启动AdsPower浏览器，类型: {type(api)}", "info")
                        self.log_signal.emit(f"API基础URL: {getattr(api, 'base_url', '未知')}", "info")
                    else:
                        self.log_signal.emit("API实例未传递，无法启动AdsPower浏览器", "error")
                        return self.fallback_to_chrome()

                    self.log_signal.emit(f"正在通过AdsPower API启动环境: {self.env_id}", "info")

                    # 通过AdsPower API启动浏览器
                    start_result = api.start_browser(self.env_id)
                    self.log_signal.emit(f"API返回结果: {start_result}", "info")

                    if start_result.get("code") != 0:
                        error_msg = start_result.get("msg", "未知错误")
                        self.log_signal.emit(f"启动AdsPower浏览器失败: {error_msg}", "error")

                        # 提供详细的错误说明
                        if "Profile does not exist" in error_msg or "does not exist" in error_msg:
                            self.log_signal.emit(f"错误原因：环境ID '{self.env_id}' 不存在", "error")
                            self.log_signal.emit("解决方案：请检查环境ID是否正确，确保使用的是环境ID而不是环境编号", "error")
                            self.log_signal.emit("提示：环境ID通常是字母数字组合（如：knhoewu），可在AdsPower环境管理页面查看", "info")

                        return self.fallback_to_chrome()

                    # 获取WebDriver连接信息
                    data = start_result.get("data", {})
                    ws_info = data.get("ws", {})
                    selenium_address = ws_info.get("selenium", "")
                    webdriver_path = data.get("webdriver", "")

                    if not selenium_address:
                        self.log_signal.emit("未获取到WebDriver连接信息", "error")
                        return self.fallback_to_chrome()

                    self.log_signal.emit(f"获取到WebDriver地址: {selenium_address}", "info")

                    # 连接到AdsPower浏览器
                    from selenium import webdriver
                    from selenium.webdriver.chrome.options import Options
                    from selenium.webdriver.chrome.service import Service

                    chrome_options = Options()
                    # 连接到已启动的AdsPower浏览器
                    chrome_options.add_experimental_option("debuggerAddress", selenium_address)

                    # 创建WebDriver连接
                    if webdriver_path:
                        service = Service(webdriver_path)
                        self.driver = webdriver.Chrome(service=service, options=chrome_options)
                    else:
                        self.driver = webdriver.Chrome(options=chrome_options)

                    self.log_signal.emit("成功连接到AdsPower浏览器", "info")
                    time.sleep(2)
                    return True

                except ImportError:
                    self.log_signal.emit("未安装selenium，请运行: pip install selenium", "error")
                    return False
                except Exception as e:
                    self.log_signal.emit(f"连接AdsPower浏览器失败: {str(e)}", "error")
                    return self.fallback_to_chrome()

            def fallback_to_chrome(self):
                """回退到普通Chrome浏览器"""
                try:
                    self.log_signal.emit("AdsPower浏览器启动失败，回退到普通Chrome浏览器...", "warning")
                    self.log_signal.emit("注意：使用普通Chrome浏览器无法获得AdsPower的指纹保护功能", "warning")

                    from selenium import webdriver
                    from selenium.webdriver.chrome.options import Options

                    chrome_options = Options()
                    chrome_options.add_argument("--no-sandbox")
                    chrome_options.add_argument("--disable-dev-shm-usage")
                    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
                    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
                    chrome_options.add_experimental_option('useAutomationExtension', False)

                    self.driver = webdriver.Chrome(options=chrome_options)
                    self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

                    self.log_signal.emit("普通Chrome浏览器启动成功", "info")
                    time.sleep(2)
                    return True

                except ImportError:
                    self.log_signal.emit("未安装selenium，请运行: pip install selenium", "error")
                    return False
                except Exception as e:
                    error_str = str(e)
                    self.log_signal.emit(f"启动普通Chrome浏览器也失败: {error_str}", "error")

                    # 提供具体的解决方案
                    if "chromedriver" in error_str.lower():
                        self.log_signal.emit("解决方案：请下载并安装ChromeDriver", "info")
                        self.log_signal.emit("下载地址：https://chromedriver.chromium.org/", "info")
                    elif "chrome" in error_str.lower():
                        self.log_signal.emit("解决方案：请安装Google Chrome浏览器", "info")
                    else:
                        self.log_signal.emit("解决方案：请确保已安装Chrome浏览器和ChromeDriver", "info")

                    return False

            def execute_real_step(self, operation_type, config_data, step_num):
                """执行真实的RPA步骤"""
                try:
                    if not self.driver:
                        self.log_signal.emit(f"步骤 {step_num}: 浏览器未启动", "error")
                        return

                    # 获取中文操作名称用于显示
                    chinese_name = self.adspower_operation_mapping.get(operation_type, operation_type)

                    # 统一处理所有操作类型
                    if operation_type in ["访问网站", "前往网址", "gotoUrl"]:
                        self.execute_goto_url(config_data)

                    elif operation_type in ["等待时间", "waitTime"]:
                        self.execute_wait_time(config_data)

                    elif operation_type in ["点击", "点击元素", "click"]:
                        self.execute_click(config_data)

                    elif operation_type in ["滚动页面", "scrollPage"]:
                        self.execute_scroll_page(config_data)

                    elif operation_type in ["keyboard", "键盘操作", "keyboardKey"]:
                        self.execute_keyboard_operation(config_data)

                    elif operation_type in ["inputContent", "输入内容", "input"]:
                        self.execute_input_content(config_data)

                    elif operation_type in ["新建标签", "新建标签页", "newPage"]:
                        self.execute_new_page(config_data)

                    elif operation_type in ["刷新页面", "refreshPage"]:
                        self.execute_refresh_page(config_data)

                    elif operation_type in ["关闭标签", "关闭标签页", "closePage"]:
                        self.execute_close_page(config_data)

                    else:
                        self.log_signal.emit(f"未知操作类型: {chinese_name} ({operation_type})，跳过执行", "warning")
                        time.sleep(1)

                except Exception as e:
                    self.log_signal.emit(f"步骤 {step_num} 执行失败: {str(e)}", "error")

            def simulate_execution(self):
                """模拟执行（当无法启动真实浏览器时）"""
                self.log_signal.emit("启动浏览器", "info")
                time.sleep(2)

                self.log_signal.emit("创建新的TAB", "info")
                time.sleep(1)

                # 执行每个步骤的模拟
                for i in range(self.flow_steps_layout.count()):
                    item = self.flow_steps_layout.itemAt(i)
                    if item and item.widget():
                        step_widget = item.widget()
                        operation_type = getattr(step_widget, 'operation_type', '')
                        self.log_signal.emit(f"模拟执行步骤 {i + 1}: {operation_type}", "info")
                        time.sleep(1)

            def execute_scroll_page(self, config_data):
                """执行滚动页面操作 - 完全按照AdsPower规范"""
                try:
                    # 从AdsPower配置中提取滚动参数
                    scroll_type = config_data.get('scrollType', 'position')
                    position = config_data.get('position', 'bottom')
                    distance = config_data.get('distance', 0)
                    range_type = config_data.get('range', 'window')

                    self.log_signal.emit(f"滚动页面: 类型={scroll_type}, 位置={position}, 距离={distance}, 范围={range_type}", "info")

                    # 根据AdsPower的滚动逻辑执行
                    if scroll_type == 'position':
                        if position == 'bottom':
                            # 平滑滚动到底部，避免卡顿
                            self.driver.execute_script("""
                                window.scrollTo({
                                    top: document.body.scrollHeight,
                                    behavior: 'smooth'
                                });
                            """)
                        elif position == 'top':
                            self.driver.execute_script("""
                                window.scrollTo({
                                    top: 0,
                                    behavior: 'smooth'
                                });
                            """)
                        elif position == 'middle':
                            self.driver.execute_script("""
                                window.scrollTo({
                                    top: document.body.scrollHeight / 2,
                                    behavior: 'smooth'
                                });
                            """)
                    elif scroll_type == 'distance':
                        # 平滑滚动指定距离
                        self.driver.execute_script(f"""
                            window.scrollBy({{
                                top: {distance},
                                behavior: 'smooth'
                            }});
                        """)

                    # 等待滚动完成
                    time.sleep(2)
                    self.log_signal.emit("滚动页面操作完成", "info")

                except Exception as e:
                    self.log_signal.emit(f"滚动页面操作失败: {str(e)}", "error")

            def execute_keyboard_operation(self, config_data):
                """执行键盘操作 - 完全按照AdsPower规范"""
                try:
                    from selenium.webdriver.common.keys import Keys
                    from selenium.webdriver.common.action_chains import ActionChains

                    # 从AdsPower配置中提取键盘参数，处理多种可能的字段名
                    key_type = config_data.get('keyType', config_data.get('type', 'key'))
                    key_value = config_data.get('key', config_data.get('keyValue', config_data.get('value', '')))
                    modifier_keys = config_data.get('modifierKeys', config_data.get('modifiers', []))

                    # 如果key_value仍然为空，尝试从操作类型中获取
                    if not key_value and key_type:
                        # 如果操作类型本身就是按键名，使用操作类型作为按键值
                        if key_type.lower() in ['enter', 'escape', 'tab', 'space', 'backspace', 'delete']:
                            key_value = key_type
                            self.log_signal.emit(f"从操作类型中获取按键值: {key_value}", "info")

                    # 如果仍然为空，尝试从其他字段获取
                    if not key_value:
                        for possible_key in ['keyCode', 'keyName', 'text', 'input', 'action']:
                            if possible_key in config_data:
                                key_value = config_data[possible_key]
                                break

                    self.log_signal.emit(f"键盘操作: 类型={key_type}, 按键={key_value}, 修饰键={modifier_keys}", "info")

                    if not key_value:
                        self.log_signal.emit("键盘按键值为空，跳过操作", "warning")
                        return

                    actions = ActionChains(self.driver)

                    # 处理修饰键
                    for modifier in modifier_keys:
                        modifier_lower = modifier.lower()
                        if modifier_lower in ['ctrl', 'control']:
                            actions.key_down(Keys.CONTROL)
                        elif modifier_lower == 'shift':
                            actions.key_down(Keys.SHIFT)
                        elif modifier_lower == 'alt':
                            actions.key_down(Keys.ALT)
                        elif modifier_lower in ['cmd', 'command', 'meta']:
                            actions.key_down(Keys.COMMAND)

                    # 处理主按键 - 支持更多按键类型
                    key_lower = key_value.lower()
                    if key_lower in ['enter', 'return']:
                        actions.send_keys(Keys.ENTER)
                    elif key_lower == 'tab':
                        actions.send_keys(Keys.TAB)
                    elif key_lower in ['escape', 'esc']:
                        actions.send_keys(Keys.ESCAPE)
                    elif key_lower == 'space':
                        actions.send_keys(Keys.SPACE)
                    elif key_lower in ['backspace', 'back']:
                        actions.send_keys(Keys.BACKSPACE)
                    elif key_lower in ['delete', 'del']:
                        actions.send_keys(Keys.DELETE)
                    elif key_lower == 'home':
                        actions.send_keys(Keys.HOME)
                    elif key_lower == 'end':
                        actions.send_keys(Keys.END)
                    elif key_lower in ['pageup', 'page_up']:
                        actions.send_keys(Keys.PAGE_UP)
                    elif key_lower in ['pagedown', 'page_down']:
                        actions.send_keys(Keys.PAGE_DOWN)
                    elif key_lower in ['arrowup', 'up']:
                        actions.send_keys(Keys.ARROW_UP)
                    elif key_lower in ['arrowdown', 'down']:
                        actions.send_keys(Keys.ARROW_DOWN)
                    elif key_lower in ['arrowleft', 'left']:
                        actions.send_keys(Keys.ARROW_LEFT)
                    elif key_lower in ['arrowright', 'right']:
                        actions.send_keys(Keys.ARROW_RIGHT)
                    elif len(key_value) == 1:
                        # 单个字符
                        actions.send_keys(key_value)
                    else:
                        # 其他情况，直接发送
                        actions.send_keys(key_value)

                    # 释放修饰键
                    for modifier in modifier_keys:
                        modifier_lower = modifier.lower()
                        if modifier_lower in ['ctrl', 'control']:
                            actions.key_up(Keys.CONTROL)
                        elif modifier_lower == 'shift':
                            actions.key_up(Keys.SHIFT)
                        elif modifier_lower == 'alt':
                            actions.key_up(Keys.ALT)
                        elif modifier_lower in ['cmd', 'command', 'meta']:
                            actions.key_up(Keys.COMMAND)

                    actions.perform()
                    time.sleep(0.5)
                    self.log_signal.emit("键盘操作完成", "info")

                except Exception as e:
                    self.log_signal.emit(f"键盘操作失败: {str(e)}", "error")

            def execute_input_content(self, config_data):
                """执行输入内容操作 - 增强版本"""
                try:
                    from selenium.webdriver.common.by import By
                    from selenium.webdriver.support.ui import WebDriverWait
                    from selenium.webdriver.support import expected_conditions as EC
                    from selenium.webdriver.common.action_chains import ActionChains
                    from selenium.webdriver.common.keys import Keys

                    # 从AdsPower配置中提取输入参数，处理类型转换
                    selector = config_data.get('selector', '')
                    element_raw = config_data.get('element', 1)

                    # 安全地转换element为整数
                    try:
                        if element_raw == '' or element_raw is None:
                            element_index = 0
                            self.log_signal.emit(f"元素索引为空，使用默认值1", "warning")
                        else:
                            element_index = int(element_raw) - 1  # AdsPower从1开始，Selenium从0开始
                    except (ValueError, TypeError):
                        element_index = 0  # 默认第一个元素
                        self.log_signal.emit(f"元素索引转换失败，使用默认值1: {element_raw}", "warning")

                    content = config_data.get('content', '')
                    clear_before = config_data.get('clearBefore', True)

                    self.log_signal.emit(f"输入内容: 选择器={selector[:50]}..., 元素序号={element_index + 1}, 内容={content[:30]}...", "info")

                    if not selector:
                        self.log_signal.emit("选择器为空，跳过输入操作", "warning")
                        return

                    if not content:
                        self.log_signal.emit("输入内容为空，跳过输入操作", "warning")
                        return

                    # 等待元素出现
                    wait = WebDriverWait(self.driver, 15)
                    elements = []

                    try:
                        # 根据选择器类型查找元素
                        if selector.startswith('//'):
                            elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, selector)))
                        elif selector.startswith('#'):
                            elements = wait.until(EC.presence_of_all_elements_located((By.ID, selector[1:])))
                        elif selector.startswith('.'):
                            elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, selector[1:])))
                        else:
                            elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))
                    except Exception as find_error:
                        self.log_signal.emit(f"输入元素查找失败: {str(find_error)}", "error")
                        return

                    if len(elements) > element_index:
                        element = elements[element_index]

                        # 多种输入策略
                        input_success = False

                        # 策略1: 滚动到元素并直接输入
                        try:
                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                            time.sleep(1)

                            # 点击元素获得焦点
                            element.click()
                            time.sleep(0.5)

                            # 清空输入框（如果需要）
                            if clear_before:
                                element.clear()
                                # 或者使用Ctrl+A + Delete
                                element.send_keys(Keys.CONTROL + "a")
                                element.send_keys(Keys.DELETE)

                            # 输入内容
                            element.send_keys(content)
                            input_success = True
                            self.log_signal.emit("策略1成功: 直接输入", "info")

                        except Exception as e1:
                            self.log_signal.emit(f"策略1失败: {str(e1)}", "warning")

                        # 策略2: 使用ActionChains输入
                        if not input_success:
                            try:
                                actions = ActionChains(self.driver)
                                actions.move_to_element(element).click()

                                if clear_before:
                                    actions.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL)
                                    actions.send_keys(Keys.DELETE)

                                actions.send_keys(content).perform()
                                input_success = True
                                self.log_signal.emit("策略2成功: ActionChains输入", "info")

                            except Exception as e2:
                                self.log_signal.emit(f"策略2失败: {str(e2)}", "warning")

                        # 策略3: JavaScript输入
                        if not input_success:
                            try:
                                # 使用JavaScript设置值
                                if clear_before:
                                    self.driver.execute_script("arguments[0].value = '';", element)
                                    self.driver.execute_script("arguments[0].innerHTML = '';", element)

                                self.driver.execute_script("arguments[0].value = arguments[1];", element, content)
                                self.driver.execute_script("arguments[0].innerHTML = arguments[1];", element, content)

                                # 触发输入事件
                                self.driver.execute_script("""
                                    var element = arguments[0];
                                    var event = new Event('input', { bubbles: true });
                                    element.dispatchEvent(event);
                                """, element)

                                input_success = True
                                self.log_signal.emit("策略3成功: JavaScript输入", "info")

                            except Exception as e3:
                                self.log_signal.emit(f"策略3失败: {str(e3)}", "warning")

                        if input_success:
                            time.sleep(0.5)
                            self.log_signal.emit("输入内容操作完成", "info")
                        else:
                            self.log_signal.emit("所有输入策略都失败", "error")
                    else:
                        self.log_signal.emit(f"找到 {len(elements)} 个元素，但需要第 {element_index + 1} 个", "warning")

                except Exception as e:
                    self.log_signal.emit(f"输入内容操作失败: {str(e)}", "error")

            def execute_goto_url(self, config_data):
                """执行访问网址操作"""
                try:
                    url = config_data.get('goto_url', config_data.get('url', 'https://www.facebook.com/'))
                    timeout = config_data.get('timeout_seconds', config_data.get('timeout', 30000) / 1000)

                    self.log_signal.emit(f"访问URL {url} , 超时等待 {timeout * 1000} 毫秒", "info")

                    self.driver.set_page_load_timeout(timeout)
                    self.driver.get(url)
                    time.sleep(2)

                except Exception as e:
                    self.log_signal.emit(f"访问网址失败: {str(e)}", "error")

            def execute_wait_time(self, config_data):
                """执行等待时间操作"""
                try:
                    wait_type = config_data.get('wait_type', config_data.get('timeoutType', '固定时间'))

                    if wait_type in ['随机时间', 'randomInterval']:
                        import random
                        min_time = config_data.get('wait_min', config_data.get('timeoutMin', 8000)) / 1000
                        max_time = config_data.get('wait_max', config_data.get('timeoutMax', 12000)) / 1000
                        wait_time = random.uniform(min_time, max_time)
                        self.log_signal.emit(f"等待 {min_time * 1000} - {max_time * 1000} 毫秒", "info")
                    else:
                        wait_time = config_data.get('wait_min', config_data.get('timeout', 3000)) / 1000
                        self.log_signal.emit(f"等待 {wait_time * 1000} 毫秒", "info")

                    time.sleep(wait_time)

                except Exception as e:
                    self.log_signal.emit(f"等待时间操作失败: {str(e)}", "error")

            def execute_click(self, config_data):
                """执行点击操作 - 增强版本"""
                try:
                    from selenium.webdriver.common.by import By
                    from selenium.webdriver.support.ui import WebDriverWait
                    from selenium.webdriver.support import expected_conditions as EC
                    from selenium.webdriver.common.action_chains import ActionChains

                    selector = config_data.get('click_selector', config_data.get('selector', ''))
                    element_num_raw = config_data.get('element_index', config_data.get('element', 1))
                    click_type = config_data.get('click_type', '左键')

                    # 安全地转换element为整数
                    try:
                        if element_num_raw == '' or element_num_raw is None:
                            element_num = 1
                            self.log_signal.emit(f"元素序号为空，使用默认值1", "warning")
                        else:
                            element_num = int(element_num_raw)
                    except (ValueError, TypeError):
                        element_num = 1
                        self.log_signal.emit(f"元素序号转换失败，使用默认值1: {element_num_raw}", "warning")

                    self.log_signal.emit(f"选择器: {selector[:50]}... , 元素序号: {element_num} , 点击类型: {click_type}", "info")

                    if not selector:
                        self.log_signal.emit("选择器为空，跳过点击操作", "warning")
                        return

                    # 修复XPath选择器格式问题
                    if selector.startswith('(//') and '...' in selector:
                        # 处理被截断的XPath选择器
                        if 'Comment' in selector:
                            selector = "//span[text()='Comment']/ancestor::div[@role='button']"
                        elif 'Like' in selector:
                            selector = "//*[@role='button' and @aria-label='Like']"
                        self.log_signal.emit(f"修复后的选择器: {selector}", "info")

                    # 等待元素出现并点击
                    wait = WebDriverWait(self.driver, 15)
                    elements = []

                    try:
                        # 根据选择器类型查找元素
                        if selector.startswith('//'):
                            elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, selector)))
                        elif selector.startswith('#'):
                            elements = wait.until(EC.presence_of_all_elements_located((By.ID, selector[1:])))
                        elif selector.startswith('.'):
                            elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, selector[1:])))
                        else:
                            elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))
                    except Exception as find_error:
                        self.log_signal.emit(f"元素查找失败: {str(find_error)}", "error")
                        return

                    if len(elements) >= element_num:
                        element = elements[element_num - 1]

                        # 多种点击策略
                        click_success = False

                        # 策略1: 滚动到元素并直接点击
                        try:
                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                            time.sleep(1)

                            # 检查元素是否可见和可点击
                            if element.is_displayed() and element.is_enabled():
                                element.click()
                                click_success = True
                                self.log_signal.emit("策略1成功: 直接点击", "info")
                        except Exception as e1:
                            self.log_signal.emit(f"策略1失败: {str(e1)}", "warning")

                        # 策略2: 使用ActionChains点击
                        if not click_success:
                            try:
                                actions = ActionChains(self.driver)
                                actions.move_to_element(element).click().perform()
                                click_success = True
                                self.log_signal.emit("策略2成功: ActionChains点击", "info")
                            except Exception as e2:
                                self.log_signal.emit(f"策略2失败: {str(e2)}", "warning")

                        # 策略3: JavaScript点击
                        if not click_success:
                            try:
                                self.driver.execute_script("arguments[0].click();", element)
                                click_success = True
                                self.log_signal.emit("策略3成功: JavaScript点击", "info")
                            except Exception as e3:
                                self.log_signal.emit(f"策略3失败: {str(e3)}", "warning")

                        if click_success:
                            self.log_signal.emit(f"成功点击元素", "info")
                        else:
                            self.log_signal.emit(f"所有点击策略都失败", "error")
                    else:
                        self.log_signal.emit(f"找到 {len(elements)} 个元素，但需要第 {element_num} 个", "warning")

                    time.sleep(1)

                except Exception as e:
                    self.log_signal.emit(f"点击操作失败: {str(e)}", "error")

            def execute_new_page(self, config_data):
                """执行新建标签页操作"""
                try:
                    self.log_signal.emit("新建标签页", "info")
                    self.driver.execute_script("window.open('');")

                    # 切换到新标签页
                    handles = self.driver.window_handles
                    if len(handles) > 1:
                        self.driver.switch_to.window(handles[-1])
                        self.log_signal.emit("已切换到新标签页", "info")

                    time.sleep(1)

                except Exception as e:
                    self.log_signal.emit(f"新建标签页失败: {str(e)}", "error")

            def execute_refresh_page(self, config_data):
                """执行刷新页面操作"""
                try:
                    self.log_signal.emit("刷新页面", "info")
                    self.driver.refresh()
                    time.sleep(2)

                except Exception as e:
                    self.log_signal.emit(f"刷新页面失败: {str(e)}", "error")

            def execute_close_page(self, config_data):
                """执行关闭标签页操作"""
                try:
                    self.log_signal.emit("关闭标签页", "info")
                    self.driver.close()

                    # 如果还有其他标签页，切换到第一个
                    handles = self.driver.window_handles
                    if handles:
                        self.driver.switch_to.window(handles[0])
                        self.log_signal.emit("已切换到其他标签页", "info")

                    time.sleep(1)

                except Exception as e:
                    self.log_signal.emit(f"关闭标签页失败: {str(e)}", "error")

            def cleanup_browser(self):
                """清理浏览器资源"""
                if self.driver:
                    try:
                        self.driver.quit()
                        self.log_signal.emit("浏览器已关闭", "info")
                    except:
                        pass

        # 获取API实例 - 增强调试信息
        api_instance = None

        # 尝试多种方式获取API实例
        if hasattr(self.parent(), 'api') and self.parent().api:
            api_instance = self.parent().api
            print(f"[DEBUG] 从parent()获取到API实例: {type(api_instance)}")
        elif hasattr(self, 'parent_window') and hasattr(self.parent_window, 'api'):
            api_instance = self.parent_window.api
            print(f"[DEBUG] 从parent_window获取到API实例: {type(api_instance)}")
        else:
            # 尝试从主窗口获取
            try:
                from PyQt5.QtWidgets import QApplication
                app = QApplication.instance()
                if app:
                    for widget in app.topLevelWidgets():
                        if hasattr(widget, 'api') and widget.api:
                            api_instance = widget.api
                            print(f"[DEBUG] 从顶级窗口获取到API实例: {type(api_instance)}")
                            break
            except Exception as e:
                print(f"[DEBUG] 从顶级窗口获取API失败: {e}")

        if api_instance:
            print(f"[DEBUG] 成功获取API实例，类型: {type(api_instance)}")
        else:
            print("[DEBUG] 未能获取到API实例")

        # 创建执行线程，传递API实例
        execution_thread = RealRPAExecutionThread(self.flow_steps_layout, env_id, api_instance)

        # 连接信号
        execution_thread.log_signal.connect(log_dialog.add_log)
        execution_thread.finished_signal.connect(lambda: print("RPA执行完成"))

        # 启动执行线程
        execution_thread.start()

        # 显示日志对话框
        log_dialog.exec_()

    def show_debug_log(self):
        """显示调试日志功能 - AdsPower样式"""
        from debug_log_dialog import DebugLogDialog

        # 打开调试日志对话框
        log_dialog = DebugLogDialog(self)
        log_dialog.exec_()

    def import_flow(self):
        """导入流程功能 - AdsPower原版样式"""
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QRadioButton, QButtonGroup, QMessageBox, QLabel
        import json

        # 创建导入对话框
        dialog = QDialog(self)
        dialog.setWindowTitle("导入")
        dialog.setFixedSize(600, 450)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
            }
        """)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # 添加JSON标签
        json_label = QLabel("添加JSON")
        json_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: 500;
                color: #333333;
                margin-bottom: 5px;
            }
        """)
        layout.addWidget(json_label)

        # JSON输入文本框
        json_input = QTextEdit()
        json_input.setPlaceholderText("请将相应流程的 JSON 粘贴在此处")
        json_input.setStyleSheet("""
            QTextEdit {
                border: 1px solid #d9d9d9;
                border-radius: 6px;
                padding: 12px;
                font-size: 14px;
                font-family: "Consolas", "Monaco", monospace;
                background-color: #fafafa;
                min-height: 200px;
            }
            QTextEdit:focus {
                border-color: #1890ff;
                background-color: white;
            }
        """)
        layout.addWidget(json_input)

        # 导入内容选项
        content_label = QLabel("导入内容")
        content_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: 500;
                color: #333333;
                margin-top: 10px;
                margin-bottom: 5px;
            }
        """)
        layout.addWidget(content_label)

        # 单选按钮组
        radio_layout = QHBoxLayout()
        radio_layout.setSpacing(20)

        button_group = QButtonGroup()

        add_radio = QRadioButton("追加")
        add_radio.setChecked(True)
        add_radio.setStyleSheet("""
            QRadioButton {
                font-size: 14px;
                color: #333333;
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
        button_group.addButton(add_radio, 0)
        radio_layout.addWidget(add_radio)

        replace_radio = QRadioButton("替换")
        replace_radio.setStyleSheet(add_radio.styleSheet())
        button_group.addButton(replace_radio, 1)
        radio_layout.addWidget(replace_radio)

        radio_layout.addStretch()
        layout.addLayout(radio_layout)

        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        # 取消按钮
        cancel_btn = QPushButton("取消")
        cancel_btn.setFixedSize(80, 36)
        cancel_btn.setStyleSheet("""
            QPushButton {
                border: 1px solid #d9d9d9;
                border-radius: 6px;
                background-color: white;
                color: #333333;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
                border-color: #40a9ff;
            }
        """)
        cancel_btn.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_btn)

        button_layout.addSpacing(10)

        # 确定按钮
        confirm_btn = QPushButton("确定")
        confirm_btn.setFixedSize(80, 36)
        confirm_btn.setStyleSheet("""
            QPushButton {
                background-color: #1890ff;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #40a9ff;
            }
            QPushButton:pressed {
                background-color: #096dd9;
            }
        """)

        def import_json():
            json_text = json_input.toPlainText().strip()
            if not json_text:
                QMessageBox.warning(dialog, "警告", "请输入JSON代码")
                return

            try:
                # 解析JSON
                flow_data = json.loads(json_text)

                # 检查是否是替换模式
                is_replace = button_group.checkedId() == 1

                if is_replace:
                    # 替换模式：清空当前流程
                    while self.flow_steps_layout.count():
                        child = self.flow_steps_layout.takeAt(0)
                        if child.widget():
                            child.widget().deleteLater()

                # 导入流程步骤
                imported_count = 0
                if isinstance(flow_data, list):
                    # 如果是步骤数组
                    for i, step in enumerate(flow_data):
                        # 获取操作类型并转换为中文名称
                        operation_type = step.get('type', f'步骤 {i+1}')
                        chinese_name = self.adspower_operation_mapping.get(operation_type, operation_type)

                        step_title = f"步骤 {i+1}: {chinese_name}"
                        step_desc = self.format_imported_step_description(step)

                        step_widget = self.create_flow_step(step_title, step_desc)
                        # 保存完整的原始配置数据
                        step_widget.config_data = step.get('config', step)
                        step_widget.operation_type = operation_type  # 保存原始AdsPower类型用于执行
                        step_widget.operation_name = chinese_name  # 中文名称用于显示
                        step_widget.chinese_name = chinese_name  # 中文名称
                        step_widget.original_adspower_type = operation_type  # 保存原始类型

                        self.flow_steps_layout.addWidget(step_widget)
                        imported_count += 1
                elif isinstance(flow_data, dict) and 'steps' in flow_data:
                    # 如果是包含steps的对象
                    for i, step in enumerate(flow_data['steps']):
                        # 获取操作类型并转换为中文名称
                        operation_type = step.get('type', step.get('title', f'步骤 {i+1}'))
                        chinese_name = self.adspower_operation_mapping.get(operation_type, operation_type)

                        step_title = f"步骤 {i+1}: {chinese_name}"
                        step_desc = self.format_imported_step_description(step)

                        step_widget = self.create_flow_step(step_title, step_desc)
                        # 保存完整的原始配置数据
                        step_widget.config_data = step.get('config', step.get('description', step))
                        step_widget.operation_type = operation_type  # 保存原始AdsPower类型用于执行
                        step_widget.operation_name = chinese_name  # 中文名称用于显示
                        step_widget.chinese_name = chinese_name  # 中文名称
                        step_widget.original_adspower_type = operation_type  # 保存原始类型

                        self.flow_steps_layout.addWidget(step_widget)
                        imported_count += 1

                # 切换显示状态
                if self.flow_steps_layout.count() > 0:
                    if hasattr(self, 'empty_state') and self.empty_state.parent():
                        self.flow_layout.removeWidget(self.empty_state)
                        self.empty_state.setParent(None)
                        self.flow_layout.addWidget(self.flow_steps_container)

                # 重新编号步骤
                self.renumber_steps()

                dialog.accept()
                mode_text = "替换" if is_replace else "追加"
                QMessageBox.information(self, "导入成功", f"成功{mode_text}导入 {imported_count} 个步骤")

            except json.JSONDecodeError as e:
                QMessageBox.critical(dialog, "JSON格式错误", f"JSON格式不正确:\n{str(e)}")
            except Exception as e:
                QMessageBox.critical(dialog, "导入失败", f"导入时发生错误:\n{str(e)}")

        confirm_btn.clicked.connect(import_json)
        button_layout.addWidget(confirm_btn)

        layout.addLayout(button_layout)
        dialog.exec_()

    def export_flow(self):
        """导出流程功能 - 使用新的流程管理器"""
        from PyQt5.QtWidgets import QFileDialog, QMessageBox
        from rpa_flow_manager import RPAFlowManager
        import json

        if self.flow_steps_layout.count() == 0:
            QMessageBox.warning(self, "导出", "当前没有流程步骤可以导出")
            return

        # 初始化流程管理器
        flow_manager = RPAFlowManager()

        file_path, _ = QFileDialog.getSaveFileName(self, "导出流程", "", "JSON文件 (*.json)")
        if file_path:
            try:
                # 获取当前流程数据
                flow_data = self.get_flow_data()
                if not flow_data:
                    QMessageBox.warning(self, "导出失败", "无法获取流程数据")
                    return

                # 使用流程管理器导出
                export_content = flow_manager.export_flow(flow_data, "json")

                # 保存到文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(export_content)

                # 检查兼容性
                compatibility = flow_manager.check_adspower_compatibility(flow_data)

                success_msg = f"成功导出 {len(flow_data.get('steps', []))} 个步骤到文件"
                if compatibility["warnings"]:
                    success_msg += "\n\n兼容性提醒：\n" + "\n".join(compatibility["warnings"])

                QMessageBox.information(self, "导出成功", success_msg)

            except Exception as e:
                QMessageBox.critical(self, "导出失败", f"导出文件时发生错误:\n{str(e)}")

    def save_flow(self):
        """保存流程功能"""
        from PyQt5.QtWidgets import QMessageBox
        import json
        import os

        # 获取任务名称
        task_name = ""
        for widget in self.findChildren(QLineEdit):
            if widget.placeholderText() == "请填写任务名称":
                task_name = widget.text().strip()
                break

        if not task_name:
            QMessageBox.warning(self, "保存失败", "请先填写任务名称")
            return

        try:
            # 收集流程数据
            steps = []
            for i in range(self.flow_steps_layout.count()):
                item = self.flow_steps_layout.itemAt(i)
                if item and item.widget():
                    step_widget = item.widget()
                    # 提取步骤信息
                    title = ""
                    description = ""
                    for child in step_widget.findChildren(QLabel):
                        if child.styleSheet() and "font-weight: 600" in child.styleSheet():
                            title = child.text()
                        elif child.styleSheet() and "color: #666666" in child.styleSheet():
                            description = child.text()

                    # 获取完整的步骤配置
                    config_data = getattr(step_widget, 'config_data', {})
                    operation_type = getattr(step_widget, 'operation_type', '')
                    operation_name = getattr(step_widget, 'operation_name', '')

                    # 确保配置数据包含操作类型
                    if operation_type and 'operation' not in config_data:
                        config_data['operation'] = operation_type

                    steps.append({
                        "title": title,
                        "description": description,
                        "config": config_data,
                        "operation_type": operation_type,
                        "operation_name": operation_name
                    })

            flow_data = {
                "name": task_name,
                "steps": steps,
                "save_time": QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
            }

            # 保存到data目录
            os.makedirs("data", exist_ok=True)
            file_path = f"data/{task_name}_flow.json"

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(flow_data, f, ensure_ascii=False, indent=2)

            QMessageBox.information(self, "保存成功", f"流程已保存到: {file_path}")

        except Exception as e:
            QMessageBox.critical(self, "保存失败", f"保存流程时发生错误:\n{str(e)}")

    def load_flow(self):
        """加载已保存的流程功能"""
        from PyQt5.QtWidgets import QFileDialog, QMessageBox
        import json
        import os

        try:
            # 检查data目录是否存在
            if not os.path.exists("data"):
                QMessageBox.information(self, "提示", "没有找到已保存的流程文件")
                return

            # 打开文件选择对话框
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "选择要加载的流程文件",
                "data",
                "JSON文件 (*.json);;所有文件 (*.*)"
            )

            if not file_path:
                return

            # 读取文件
            with open(file_path, 'r', encoding='utf-8') as f:
                flow_data = json.load(f)

            # 验证文件格式
            if not isinstance(flow_data, dict) or 'steps' not in flow_data:
                QMessageBox.warning(self, "加载失败", "文件格式不正确，不是有效的流程文件")
                return

            # 询问是否替换当前流程
            if self.flow_steps_layout.count() > 0:
                reply = QMessageBox.question(
                    self,
                    "加载流程",
                    "当前已有流程步骤，是否替换？\n选择'是'将清空当前流程，选择'否'将追加到当前流程",
                    QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
                )

                if reply == QMessageBox.Cancel:
                    return
                elif reply == QMessageBox.Yes:
                    # 清空当前流程
                    while self.flow_steps_layout.count():
                        child = self.flow_steps_layout.takeAt(0)
                        if child.widget():
                            child.widget().deleteLater()

            # 设置任务名称
            if 'name' in flow_data:
                for widget in self.findChildren(QLineEdit):
                    if widget.placeholderText() == "请填写任务名称":
                        widget.setText(flow_data['name'])
                        break

            # 加载流程步骤
            steps = flow_data.get('steps', [])
            loaded_count = 0

            for i, step_data in enumerate(steps):
                try:
                    # 获取步骤信息
                    title = step_data.get('title', f'步骤 {i+1}')
                    description = step_data.get('description', '无描述')
                    config_data = step_data.get('config', {})

                    # 创建步骤控件
                    step_widget = self.create_flow_step(title, description)

                    # 设置配置数据
                    if config_data:
                        step_widget.config_data = config_data

                    # 设置操作类型
                    operation_type = step_data.get('operation_type', '')
                    operation_name = step_data.get('operation_name', '')

                    if not operation_type:
                        # 尝试从配置数据中提取操作类型
                        operation_type = config_data.get('operation', '')

                    if not operation_type:
                        # 从标题中提取操作类型
                        if ':' in title:
                            operation_type = title.split(':', 1)[1].strip()

                    if operation_type:
                        step_widget.operation_type = operation_type
                        step_widget.operation_name = operation_name or operation_type

                    # 添加到布局
                    self.flow_steps_layout.addWidget(step_widget)
                    loaded_count += 1

                except Exception as e:
                    print(f"加载步骤 {i+1} 时出错: {e}")
                    continue

            # 切换到流程显示状态
            if loaded_count > 0:
                if hasattr(self, 'empty_state') and self.empty_state.parent():
                    self.flow_layout.removeWidget(self.empty_state)
                    self.empty_state.setParent(None)
                    self.flow_layout.addWidget(self.flow_steps_container)

                # 重新编号步骤
                self.renumber_steps()

            # 显示加载结果
            save_time = flow_data.get('save_time', '未知时间')
            QMessageBox.information(
                self,
                "加载成功",
                f"成功加载流程: {flow_data.get('name', '未命名')}\n"
                f"保存时间: {save_time}\n"
                f"加载步骤数: {loaded_count}"
            )

        except json.JSONDecodeError as e:
            QMessageBox.critical(self, "加载失败", f"文件格式错误:\n{str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "加载失败", f"加载流程时发生错误:\n{str(e)}")

    def load_flow_data(self, flow_data):
        """加载流程数据用于编辑"""
        try:
            print(f"加载流程数据: {flow_data}")

            # 设置任务名称
            if 'name' in flow_data:
                for widget in self.findChildren(QLineEdit):
                    if widget.placeholderText() == "请填写任务名称":
                        widget.setText(flow_data['name'])
                        break

            # 设置分组
            if 'group' in flow_data:
                for widget in self.findChildren(QComboBox):
                    # 找到分组下拉框并设置值
                    if hasattr(widget, 'addItem'):
                        index = widget.findText(flow_data['group'])
                        if index >= 0:
                            widget.setCurrentIndex(index)
                        else:
                            widget.addItem(flow_data['group'])
                            widget.setCurrentText(flow_data['group'])
                        break

            # 加载流程步骤
            if 'steps' in flow_data and flow_data['steps']:
                steps = flow_data['steps']
                for i, step_data in enumerate(steps):
                    try:
                        # 获取步骤信息
                        title = step_data.get('title', f'步骤 {i+1}')
                        description = step_data.get('description', '无描述')
                        config_data = step_data.get('config', {})

                        # 创建步骤控件
                        step_widget = self.create_flow_step(title, description)

                        # 设置配置数据
                        if config_data:
                            step_widget.config_data = config_data

                        # 设置操作类型
                        operation_type = step_data.get('operation_type', '')
                        operation_name = step_data.get('operation_name', '')

                        if not operation_type:
                            operation_type = config_data.get('operation', '')

                        if operation_type:
                            step_widget.operation_type = operation_type
                            step_widget.operation_name = operation_name or operation_type

                        # 添加到布局
                        self.flow_steps_layout.addWidget(step_widget)

                    except Exception as e:
                        print(f"加载步骤 {i+1} 时出错: {e}")
                        continue

                # 切换到流程显示状态
                if self.flow_steps_layout.count() > 0:
                    if hasattr(self, 'empty_state') and self.empty_state.parent():
                        self.flow_layout.removeWidget(self.empty_state)
                        self.empty_state.setParent(None)
                        self.flow_layout.addWidget(self.flow_steps_container)

                    # 重新编号步骤
                    self.renumber_steps()

                    # 更新标题
                    self.update_title_count()

            print(f"流程数据加载完成，步骤数: {self.flow_steps_layout.count()}")

        except Exception as e:
            print(f"加载流程数据失败: {e}")
            import traceback
            traceback.print_exc()

    def get_flow_data(self):
        """获取当前流程数据"""
        try:
            # 获取任务名称
            task_name = ""
            for widget in self.findChildren(QLineEdit):
                if widget.placeholderText() == "请填写任务名称":
                    task_name = widget.text().strip()
                    break

            if not task_name:
                return None

            # 获取分组
            group = "未分组"
            for widget in self.findChildren(QComboBox):
                if hasattr(widget, 'currentText'):
                    group = widget.currentText()
                    break

            # 收集流程步骤
            steps = []
            for i in range(self.flow_steps_layout.count()):
                item = self.flow_steps_layout.itemAt(i)
                if item and item.widget():
                    step_widget = item.widget()

                    # 提取步骤信息
                    title = ""
                    description = ""
                    for child in step_widget.findChildren(QLabel):
                        if child.styleSheet() and "font-weight: 600" in child.styleSheet():
                            title = child.text()
                        elif child.styleSheet() and "color: #666666" in child.styleSheet():
                            description = child.text()

                    # 获取完整的步骤配置
                    config_data = getattr(step_widget, 'config_data', {})
                    operation_type = getattr(step_widget, 'operation_type', '')
                    operation_name = getattr(step_widget, 'operation_name', '')

                    # 确保配置数据包含操作类型
                    if operation_type and 'operation' not in config_data:
                        config_data['operation'] = operation_type

                    steps.append({
                        "title": title,
                        "description": description,
                        "config": config_data,
                        "operation_type": operation_type,
                        "operation_name": operation_name
                    })

            # 构建流程数据
            current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
            flow_data = {
                "name": task_name,
                "group": group,
                "steps": steps,
                "created_time": current_time,  # 添加created_time字段
                "save_time": current_time,
                "step_count": len(steps)
            }

            print(f"获取流程数据: 名称={task_name}, 分组={group}, 步骤数={len(steps)}")
            return flow_data

        except Exception as e:
            print(f"获取流程数据失败: {e}")
            import traceback
            traceback.print_exc()
            return None

    def update_title_count(self):
        """更新标题中的步骤计数"""
        try:
            count = self.flow_steps_layout.count()
            for widget in self.findChildren(QLabel):
                if "任务流程(" in widget.text():
                    widget.setText(f"任务流程({count})")
                    break
        except Exception as e:
            print(f"更新标题计数失败: {e}")

    def handle_accept(self):
        """处理接受按钮点击"""
        try:
            # 验证任务名称
            task_name = ""
            for widget in self.findChildren(QLineEdit):
                if widget.placeholderText() == "请填写任务名称":
                    task_name = widget.text().strip()
                    break

            if not task_name:
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.warning(self, "提示", "请填写任务名称")
                return

            # 发送accepted信号
            self.accepted.emit()

        except Exception as e:
            print(f"处理接受事件失败: {e}")

    def handle_cancel(self):
        """处理取消按钮点击"""
        try:
            # 检查是否有未保存的更改
            if self.flow_steps_layout.count() > 0:
                from PyQt5.QtWidgets import QMessageBox
                reply = QMessageBox.question(
                    self,
                    "确认取消",
                    "是否要取消编辑？\n未保存的更改将丢失。",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )

                if reply == QMessageBox.No:
                    return

            # 发送rejected信号
            self.rejected.emit()

        except Exception as e:
            print(f"处理取消事件失败: {e}")

    def closeEvent(self, event):
        """处理窗口关闭事件"""
        try:
            # 检查是否有未保存的更改
            if self.flow_steps_layout.count() > 0:
                from PyQt5.QtWidgets import QMessageBox
                reply = QMessageBox.question(
                    self,
                    "确认关闭",
                    "是否要关闭任务流程编辑器？\n未保存的更改将丢失。",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )

                if reply == QMessageBox.No:
                    event.ignore()
                    return

            # 发送rejected信号
            self.rejected.emit()

            # 确保主窗口重新获得焦点
            if self.parent():
                try:
                    # 如果父窗口有bring_to_front方法，调用它
                    if hasattr(self.parent(), 'bring_to_front'):
                        self.parent().bring_to_front()
                    else:
                        # 否则使用标准方法
                        self.parent().raise_()
                        self.parent().activateWindow()
                except:
                    pass

            event.accept()

        except Exception as e:
            print(f"关闭事件处理失败: {e}")
            event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = TaskFlowDialog()
    dialog.show()
    sys.exit(app.exec_())
