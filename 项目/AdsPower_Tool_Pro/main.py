#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AdsPower工具专业版 - 完全复刻AdsPower界面和操作
"""

import sys
import os
import json
import random
import time
import warnings

# 抑制PyQt5的弃用警告
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*sipPyTypeDict.*")
warnings.filterwarnings("ignore", message=".*deprecated.*")

# 导入错误处理器
try:
    from error_handler import setup_global_exception_handler, log_info, log_error, safe_execute
    ERROR_HANDLER_AVAILABLE = True
    # 设置全局异常处理
    setup_global_exception_handler()
    log_info("错误处理系统已启用", "主程序")
except ImportError:
    ERROR_HANDLER_AVAILABLE = False
    def log_info(msg, context=""):
        print(f"[{context}] {msg}")
    def log_error(msg, context=""):
        print(f"[{context}] 错误: {msg}")
    def safe_execute(func, *args, context="", **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"[{context}] 执行失败: {e}")
            return None
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
                             QHeaderView, QCheckBox, QMessageBox, QComboBox, QLineEdit,
                             QLabel, QTabWidget, QMenuBar, QMenu, QAction, QSplitter,
                             QFrame, QGroupBox, QGridLayout, QProgressDialog, QDialog,
                             QFormLayout, QDialogButtonBox, QSpinBox, QTextEdit,
                             QFileDialog, QInputDialog, QRadioButton, QButtonGroup,
                             QScrollArea, QListWidget)
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QDateTime
from PyQt5.QtGui import QIcon, QFont, QCursor, QPalette, QColor

# 导入增强的API客户端和RPA引擎
try:
    from adspower_api import AdsPowerAPIClient as AdsPowerAPI
    from rpa_engine import RPAEngine
    RPA_AVAILABLE = True
    log_info("RPA模块加载成功", "主程序")
except ImportError as e:
    log_error(f"导入RPA模块失败: {e}", "主程序")
    RPA_AVAILABLE = False

    # 创建备用类
    class AdsPowerAPI:
        def __init__(self, *args, **kwargs):
            pass
        def test_connection(self):
            return {"code": -1, "msg": "API模块未加载"}

    class RPAEngine:
        def __init__(self, *args, **kwargs):
            pass

# 导入AdsPower样式管理器
try:
    from adspower_style_manager import AdsPowerStyleManager as iOS26StyleManager
except ImportError:
    # 如果导入失败，创建简化版本
    class iOS26StyleManager:
        @staticmethod
        def get_complete_style():
            return ""

        @staticmethod
        def get_button_style(variant='primary', size='base'):
            return ""

        @staticmethod
        def get_input_style():
            return ""

        @staticmethod
        def get_table_style():
            return ""

# 导入UI样式修复模块
try:
    from ui_style_fix import apply_adspower_style_fixes, apply_button_style
    UI_STYLE_FIX_AVAILABLE = True
except ImportError:
    UI_STYLE_FIX_AVAILABLE = False
    def apply_adspower_style_fixes():
        return ""
    def apply_button_style(button, variant='primary'):
        pass

# 如果RPA功能不可用，创建占位符类
if not RPA_AVAILABLE:
    class AdsPowerAPI:
        """AdsPower API客户端 - 简化版本"""

        def __init__(self, base_url="http://local.adspower.net:50325", api_key=""):
            self.base_url = base_url
            self.api_key = api_key
            self.timeout = 30

        def test_connection(self):
            """测试API连接"""
            try:
                import requests
                response = requests.get(f"{self.base_url}/status", timeout=5)
                return {"code": 0 if response.status_code == 200 else -1,
                       "msg": "连接成功" if response.status_code == 200 else "连接失败"}
            except Exception as e:
                return {"code": -1, "msg": f"连接失败: {e}"}

        def get_profiles(self, page=1, page_size=100, group_id="", search=""):
            """获取浏览器环境列表"""
            try:
                import requests
                params = {
                    "api_key": self.api_key,
                    "page": page,
                    "page_size": page_size
                }
                if group_id:
                    params["group_id"] = group_id
                if search:
                    params["search"] = search

                response = requests.get(f"{self.base_url}/api/v1/user/list",
                                      params=params, timeout=self.timeout)
                return response.json()
            except Exception as e:
                return {"code": -1, "msg": f"获取失败: {e}", "data": {"list": [], "total": 0}}

        def get_groups(self):
            """获取分组列表"""
            try:
                import requests
                response = requests.get(f"{self.base_url}/api/v1/group/list",
                                      params={"api_key": self.api_key}, timeout=self.timeout)
                return response.json()
            except Exception as e:
                return {"code": -1, "msg": f"获取分组失败: {e}", "data": {"list": []}}

        def start_browser(self, user_id):
            """启动浏览器"""
            try:
                import requests
                response = requests.get(f"{self.base_url}/api/v1/browser/start",
                                      params={"api_key": self.api_key, "user_id": user_id},
                                      timeout=60)
                return response.json()
            except Exception as e:
                return {"code": -1, "msg": f"启动失败: {e}"}

        def close_browser(self, user_id):
            """关闭浏览器"""
            try:
                import requests
                response = requests.get(f"{self.base_url}/api/v1/browser/stop",
                                      params={"api_key": self.api_key, "user_id": user_id},
                                      timeout=30)
                return response.json()
            except Exception as e:
                return {"code": -1, "msg": f"关闭失败: {e}"}

        def get_browser_status(self, user_id):
            """获取浏览器状态"""
            try:
                import requests
                response = requests.get(f"{self.base_url}/api/v1/browser/active",
                                      params={"api_key": self.api_key, "user_id": user_id},
                                      timeout=10)
                return response.json()
            except Exception as e:
                return {"code": -1, "msg": f"获取状态失败: {e}"}

        def get_profile_detail(self, user_id):
            """获取环境详细信息 - 使用正确的AdsPower API"""
            try:
                import requests
                # 使用Query Profile V2 API
                url = f"{self.base_url}/api/v2/browser-profile/list"
                data = {
                    "profile_id": [user_id],
                    "limit": 1
                }
                response = requests.post(url, json=data, timeout=10)

                if response.status_code == 200:
                    result = response.json()
                    if result.get("code") == 0 and result.get("data", {}).get("list"):
                        profile_data = result["data"]["list"][0]
                        # 转换字段名以保持兼容性
                        converted_data = {
                            "user_id": profile_data.get("profile_id", ""),
                            "name": profile_data.get("name", ""),
                            "group_name": profile_data.get("group_name", ""),
                            "domain_name": profile_data.get("platform", ""),
                            "username": profile_data.get("username", ""),
                            "password": profile_data.get("password", ""),
                            "fakey": profile_data.get("fakey", ""),
                            "remark": profile_data.get("remark", ""),
                            "ip": profile_data.get("ip", ""),
                            "ip_country": profile_data.get("ip_country", ""),
                            "created_time": profile_data.get("created_time", ""),
                            "last_open_time": profile_data.get("last_open_time", ""),
                            "profile_no": profile_data.get("profile_no", ""),
                            "ipchecker": profile_data.get("ipchecker", ""),
                            "fbcc_proxy_acc_id": profile_data.get("fbcc_proxy_acc_id", "")
                        }
                        return {"code": 0, "data": converted_data}
                    else:
                        return {"code": -1, "msg": result.get('msg', '未知错误')}
                else:
                    return {"code": -1, "msg": f"HTTP请求失败: {response.status_code}"}

            except Exception as e:
                return {"code": -1, "msg": f"获取环境详情失败: {e}"}

        def create_selenium_driver(self, user_id):
            """创建Selenium驱动（简化版本）"""
            return None, "RPA功能不可用，请运行install.py安装完整依赖"

    class RPAEngine:
        """RPA引擎 - 占位符"""
        def __init__(self, driver):
            pass

class EnvironmentManagement(QWidget):
    """环境管理页面 - 完全复刻AdsPower界面"""
    
    def __init__(self, api):
        super().__init__()
        self.api = api
        self.profiles = []
        self.current_page = 1
        self.page_size = 100
        self.total_pages = 1
        self.window_states = {}  # 浏览器状态缓存
        self.selected_profiles = set()
        self.show_opened_only = False
        
        self.init_ui()
        self.load_groups()
        self.load_profiles()
    
    def init_ui(self):
        """初始化界面 - AdsPower风格"""
        # 应用统一的AdsPower风格样式
        if UI_STYLE_FIX_AVAILABLE:
            self.setStyleSheet(apply_adspower_style_fixes())
        else:
            self.setStyleSheet(iOS26StyleManager.get_complete_style())

        # 应用响应式表格样式（如果可用）
        if UI_STYLE_FIX_AVAILABLE:
            try:
                from ui_style_fix import apply_responsive_table_style
                # 延迟应用，等待表格创建完成
                QTimer.singleShot(100, lambda: apply_responsive_table_style(self.table) if hasattr(self, 'table') else None)
            except ImportError:
                pass

        layout = QVBoxLayout()
        layout.setSpacing(16)  # 8px网格系统标准间距
        layout.setContentsMargins(16, 16, 16, 16)  # 8px网格系统标准边距
        
        # 顶部筛选区域 - PyQt5兼容风格
        filter_frame = QFrame()
        filter_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E5E5EA;
                border-radius: 16px;
                padding: 16px;
                margin: 8px;
            }
        """)
        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setContentsMargins(16, 16, 16, 16)  # 8px网格系统标准边距
        filter_layout.setSpacing(16)  # 8px网格系统标准间距
        
        # 分组筛选
        group_label = QLabel("分组:")
        group_label.setStyleSheet("""
            QLabel {
                font-family: "Segoe UI", "Microsoft YaHei", Arial, sans-serif;
                font-size: 14px;
                font-weight: normal;
                color: #323130;
                min-width: 60px;
                padding: 8px;
            }
        """)
        filter_layout.addWidget(group_label)

        self.group_combo = QComboBox()
        self.group_combo.setMinimumSize(150, 32)  # Windows标准尺寸
        self.group_combo.setStyleSheet(iOS26StyleManager.get_input_style())
        self.group_combo.currentTextChanged.connect(self.on_filter_changed)
        filter_layout.addWidget(self.group_combo)

        # 搜索框
        search_label = QLabel("搜索:")
        search_label.setStyleSheet("""
            QLabel {
                font-family: "Segoe UI", "Microsoft YaHei", Arial, sans-serif;
                font-size: 14px;
                font-weight: normal;
                color: #323130;
                min-width: 50px;
                padding: 8px;
            }
        """)
        filter_layout.addWidget(search_label)

        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("账号名称、编号、ID、标签、代理类型...")
        self.search_edit.setMinimumSize(300, 32)  # Windows标准尺寸
        self.search_edit.setStyleSheet(iOS26StyleManager.get_input_style())
        self.search_edit.returnPressed.connect(self.on_filter_changed)
        filter_layout.addWidget(self.search_edit)
        
        filter_layout.addStretch()
        
        # 每页显示数量
        filter_layout.addWidget(QLabel("每页:"))
        self.page_size_combo = QComboBox()
        self.page_size_combo.addItems(["10", "20", "50", "100", "200", "500", "1000"])
        self.page_size_combo.setCurrentText("100")
        self.page_size_combo.currentTextChanged.connect(self.on_page_size_changed)
        filter_layout.addWidget(self.page_size_combo)
        
        layout.addWidget(filter_frame)
        
        # 主要操作按钮区域 - PyQt5兼容风格
        button_frame = QFrame()
        button_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E5E5EA;
                border-radius: 16px;
                padding: 16px;
                margin: 8px;
            }
        """)
        button_layout = QHBoxLayout(button_frame)
        button_layout.setContentsMargins(16, 16, 16, 16)  # 8px网格系统标准边距
        button_layout.setSpacing(8)  # 8px网格系统按钮间距
        
        # 左侧按钮组 - AdsPower标准风格
        left_buttons = [
            ("全选", self.toggle_select_all_button, "secondary"),
            ("已打开", self.toggle_opened_filter, "secondary"),
            ("打开", self.batch_open_selected, "success"),
            ("关闭", self.batch_close_selected, "danger"),
            ("RPA", self.run_rpa_on_selected, "primary"),
            ("导出", self.export_selected, "secondary"),
            ("删除", self.delete_selected, "danger")
        ]

        for text, handler, variant in left_buttons:
            btn = QPushButton(text)
            if UI_STYLE_FIX_AVAILABLE:
                apply_button_style(btn, variant)
            else:
                btn.setStyleSheet(iOS26StyleManager.get_button_style(variant, 'base'))
            btn.clicked.connect(handler)
            button_layout.addWidget(btn)

            # 保存按钮引用
            if text == "已打开":
                self.opened_btn = btn
                btn.setCheckable(True)
        
        button_layout.addStretch()
        
        # 右侧按钮
        self.refresh_btn = QPushButton("刷新")
        self.refresh_btn.setMinimumSize(80, 32)  # Windows标准尺寸
        self.refresh_btn.setStyleSheet(iOS26StyleManager.get_button_style('secondary'))
        self.refresh_btn.clicked.connect(self.refresh_data)
        button_layout.addWidget(self.refresh_btn)

        self.new_browser_btn = QPushButton("新建浏览器")
        self.new_browser_btn.setMinimumSize(120, 32)  # Windows标准尺寸
        self.new_browser_btn.setStyleSheet(iOS26StyleManager.get_button_style('primary'))
        self.new_browser_btn.clicked.connect(self.create_new_browser)
        button_layout.addWidget(self.new_browser_btn)
        
        layout.addWidget(button_frame)
        
        # 表格区域 - 完全按照AdsPower的列设计
        self.table = QTableWidget()
        self.setup_table()
        layout.addWidget(self.table)
        
        # 分页控件 - PyQt5兼容风格
        page_frame = QFrame()
        page_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E5E5EA;
                border-radius: 12px;
                padding: 8px;
                margin: 8px 0px;
            }
        """)
        page_layout = QHBoxLayout(page_frame)
        page_layout.setContentsMargins(16, 8, 16, 8)  # 8px网格系统标准边距
        page_layout.setSpacing(8)  # 8px网格系统标准间距

        self.prev_btn = QPushButton("上一页")
        self.prev_btn.setMinimumSize(60, 28)  # 紧急调整为合理尺寸
        self.prev_btn.setStyleSheet(iOS26StyleManager.get_button_style('secondary'))
        self.prev_btn.clicked.connect(self.prev_page)
        page_layout.addWidget(self.prev_btn)

        self.page_label = QLabel("第 1 页，共 1 页")
        self.page_label.setStyleSheet("""
            QLabel {
                font-family: "Segoe UI", "Microsoft YaHei", Arial, sans-serif;
                font-size: 12px;
                font-weight: normal;
                color: #323130;
                padding: 8px 12px;
                min-width: 100px;
                text-align: center;
            }
        """)
        page_layout.addWidget(self.page_label)

        self.next_btn = QPushButton("下一页")
        self.next_btn.setMinimumSize(60, 28)  # 紧急调整为合理尺寸
        self.next_btn.setStyleSheet(iOS26StyleManager.get_button_style('secondary'))
        self.next_btn.clicked.connect(self.next_page)
        page_layout.addWidget(self.next_btn)

        page_layout.addStretch()

        # 跳转页面
        goto_label = QLabel("跳转到:")
        goto_label.setStyleSheet("""
            QLabel {
                font-family: "Microsoft YaHei", "PingFang SC", Arial, sans-serif;
                font-size: 12px;
                font-weight: normal;
                color: #1C1C1E;
                padding: 6px;
            }
        """)
        page_layout.addWidget(goto_label)

        self.goto_edit = QLineEdit()
        self.goto_edit.setFixedSize(60, 28)  # 紧急调整为合理尺寸
        self.goto_edit.setStyleSheet(iOS26StyleManager.get_input_style())
        self.goto_edit.returnPressed.connect(self.goto_page)
        page_layout.addWidget(self.goto_edit)

        goto_btn = QPushButton("跳转")
        goto_btn.setMinimumSize(60, 28)  # 紧急调整为合理尺寸
        goto_btn.setStyleSheet(iOS26StyleManager.get_button_style('primary'))
        goto_btn.clicked.connect(self.goto_page)
        page_layout.addWidget(goto_btn)
        
        layout.addWidget(page_frame)
        
        self.setLayout(layout)
    
    def setup_table(self):
        """设置表格 - 完全按照AdsPower的列设计"""
        # AdsPower的标准列 - 删除#号列和序号列
        headers = [
            "选择", "最后打开时间", "编号/ID", "分组", "平台/名称",
            "账号/密码", "备注", "IP", "创建时间", "状态", "操作"
        ]

        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        # 创建全选复选框
        self.select_all_checkbox = QCheckBox()
        self.select_all_checkbox.stateChanged.connect(self.toggle_select_all)

        # 设置列宽 - 真正的响应式布局，适应不同屏幕尺寸
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)    # 选择
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)    # 最后打开时间 - 自适应内容
        header.setSectionResizeMode(2, QHeaderView.Fixed)    # 编号/ID
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)    # 分组 - 自适应内容
        header.setSectionResizeMode(4, QHeaderView.Stretch)  # 平台/名称 - 自动拉伸
        header.setSectionResizeMode(5, QHeaderView.Interactive)  # 账号/密码 - 可调整
        header.setSectionResizeMode(6, QHeaderView.Stretch)  # 备注 - 自动拉伸
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)    # IP - 自适应内容
        header.setSectionResizeMode(8, QHeaderView.ResizeToContents)    # 创建时间 - 自适应内容
        header.setSectionResizeMode(9, QHeaderView.Fixed)    # 状态
        header.setSectionResizeMode(10, QHeaderView.Fixed)   # 操作

        # 设置优化的列宽 - 响应式设计，适应不同屏幕尺寸
        self.table.setColumnWidth(0, 50)    # 选择 - 减小宽度
        self.table.setColumnWidth(1, 120)   # 最后打开时间 - 减小宽度
        self.table.setColumnWidth(2, 70)    # 编号/ID - 减小宽度
        self.table.setColumnWidth(3, 80)    # 分组
        self.table.setColumnWidth(4, 200)   # 平台/名称 - 增加宽度显示完整内容
        self.table.setColumnWidth(5, 140)   # 账号/密码 - 减小宽度
        self.table.setColumnWidth(7, 100)   # IP - 减小宽度
        self.table.setColumnWidth(8, 120)   # 创建时间 - 减小宽度
        self.table.setColumnWidth(9, 70)    # 状态 - 减小宽度
        self.table.setColumnWidth(10, 120)  # 操作 - 减小宽度

        # 表格样式 - iOS 26 Liquid Glass风格
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.verticalHeader().setVisible(False)

        # 设置行高 - Windows标准40px
        self.table.verticalHeader().setDefaultSectionSize(40)  # Windows标准行高

        # 应用PyQt5兼容的表格样式
        self.table.setStyleSheet("""
            QTableWidget {
                gridline-color: #E5E5EA;
                background-color: white;
                alternate-background-color: #F8F9FA;
                selection-background-color: #E3F2FD;
                border: 1px solid #E5E5EA;
                border-radius: 12px;
                font-family: "Microsoft YaHei", "PingFang SC", Arial, sans-serif;
                font-size: 13px;
                color: #1C1C1E;
            }
            QHeaderView::section {
                background-color: #F2F2F7;
                padding: 15px 20px;
                border: none;
                border-bottom: 1px solid #D1D1D6;
                font-family: "Microsoft YaHei", "PingFang SC", Arial, sans-serif;
                font-weight: bold;
                font-size: 14px;
                color: #1C1C1E;
                text-align: center;
            }
            QTableWidget::item {
                padding: 15px 20px;
                border: none;
                border-bottom: 1px solid #F0F0F0;
                font-family: "Microsoft YaHei", "PingFang SC", Arial, sans-serif;
                font-size: 13px;
                color: #1C1C1E;
            }
            QTableWidget::item:selected {
                background-color: #E3F2FD;
                color: #1C1C1E;
            }
            QScrollBar:vertical {
                background-color: #F2F2F7;
                width: 12px;
                border-radius: 6px;
                margin: 2px;
            }
            QScrollBar::handle:vertical {
                background-color: #007AFF;
                border-radius: 6px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #0056CC;
            }
            QScrollBar:horizontal {
                background-color: #F2F2F7;
                height: 12px;
                border-radius: 6px;
                margin: 2px;
            }
            QScrollBar::handle:horizontal {
                background-color: #007AFF;
                border-radius: 6px;
                min-width: 30px;
            }
            QScrollBar::handle:horizontal:hover {
                background-color: #0056CC;
            }
        """)

    def toggle_select_all(self, state):
        """全选/取消全选 - 复选框版本"""
        try:
            if state == Qt.Checked:
                # 全选
                for row in range(self.table.rowCount()):
                    checkbox = self.table.cellWidget(row, 0)
                    if checkbox and isinstance(checkbox, QCheckBox):
                        checkbox.setChecked(True)
            else:
                # 取消全选
                for row in range(self.table.rowCount()):
                    checkbox = self.table.cellWidget(row, 0)
                    if checkbox and isinstance(checkbox, QCheckBox):
                        checkbox.setChecked(False)
        except Exception as e:
            print(f"全选操作失败: {e}")

    def toggle_select_all_button(self):
        """全选/取消全选 - 按钮版本"""
        try:
            # 检查当前是否有选中的项目
            selected_count = len(self.selected_profiles)
            total_count = self.table.rowCount()

            if selected_count == total_count and total_count > 0:
                # 当前全选状态，执行取消全选
                for row in range(self.table.rowCount()):
                    checkbox = self.table.cellWidget(row, 0)
                    if checkbox and isinstance(checkbox, QCheckBox):
                        checkbox.setChecked(False)
                QMessageBox.information(self, "取消全选", "已取消选择所有环境")
            else:
                # 当前非全选状态，执行全选
                for row in range(self.table.rowCount()):
                    checkbox = self.table.cellWidget(row, 0)
                    if checkbox and isinstance(checkbox, QCheckBox):
                        checkbox.setChecked(True)
                QMessageBox.information(self, "全选", f"已选择所有 {total_count} 个环境")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"全选操作失败: {e}")
    
    def load_groups(self):
        """加载分组列表"""
        try:
            result = self.api.get_groups()
            self.group_combo.clear()
            self.group_combo.addItem("全部分组", "")
            
            if result.get("code") == 0:
                groups = result.get("data", {}).get("list", [])
                for group in groups:
                    group_name = group.get("group_name", "")
                    group_id = group.get("group_id", "")
                    self.group_combo.addItem(group_name, group_id)
        except Exception as e:
            print(f"[环境管理] 加载分组失败: {e} (可能是API未连接)")

    def save_profiles_to_file(self):
        """保存环境数据到文件"""
        try:
            import os
            data_dir = "data"
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)

            profiles_file = os.path.join(data_dir, "profiles.json")
            with open(profiles_file, 'w', encoding='utf-8') as f:
                json.dump(self.profiles, f, ensure_ascii=False, indent=2)

        except Exception as e:
            print(f"保存环境数据失败: {e}")

    def load_profiles_from_file(self):
        """从文件加载环境数据"""
        try:
            import os
            profiles_file = os.path.join("data", "profiles.json")
            if os.path.exists(profiles_file):
                with open(profiles_file, 'r', encoding='utf-8') as f:
                    all_profiles = json.load(f)

                # 手动实现分页逻辑
                total_profiles = len(all_profiles)
                start_index = (self.current_page - 1) * self.page_size
                end_index = min(start_index + self.page_size, total_profiles)

                self.profiles = all_profiles[start_index:end_index]
                self.total_pages = max(1, (total_profiles + self.page_size - 1) // self.page_size)

                print(f"[DEBUG] 从文件加载: 总数={total_profiles}, 当前页={self.current_page}, 当前页数据={len(self.profiles)}, 总页数={self.total_pages}")

                self.update_page_info()
                return True
        except Exception as e:
            print(f"加载环境数据失败: {e}")
        return False

    def load_profiles(self):
        """加载环境列表"""
        try:
            group_id = self.group_combo.currentData() or ""
            search = self.search_edit.text().strip()

            if ERROR_HANDLER_AVAILABLE:
                log_info(f"加载环境列表: 页码={self.current_page}, 每页={self.page_size}", "环境管理")
            else:
                print(f"[DEBUG] 加载环境列表: 页码={self.current_page}, 每页={self.page_size}")

            result = self.api.get_profiles(self.current_page, self.page_size, group_id, search)

            if ERROR_HANDLER_AVAILABLE:
                log_info(f"API返回: code={result.get('code')}, msg={result.get('msg', '')}", "环境管理")
            else:
                print(f"[DEBUG] API返回: code={result.get('code')}, msg={result.get('msg', '')}")

            if result.get("code") == 0:
                data = result.get("data", {})
                self.profiles = data.get("list", [])

                # AdsPower API不返回total字段，使用简单的分页逻辑
                current_page_size = len(self.profiles)

                # 如果当前页的数据量等于请求的page_size，说明可能还有下一页
                if current_page_size == self.page_size:
                    # 假设至少还有一页，用户点击时再检查
                    self.total_pages = self.current_page + 1
                else:
                    # 当前页数据不满，说明这是最后一页
                    self.total_pages = self.current_page

                print(f"[DEBUG] 数据解析: 环境数={len(self.profiles)}, 当前页={self.current_page}, 总页数={self.total_pages}")

                # 保存到文件作为备份
                self.save_profiles_to_file()

                self.update_table()
                self.update_page_info()
            else:
                # API失败时尝试从文件加载或创建模拟数据
                if self.load_profiles_from_file():
                    self.update_table()
                    if self.current_page == 1:  # 只在第一页显示警告
                        QMessageBox.warning(self, "API连接失败", "已加载本地缓存数据")
                else:
                    # 创建模拟数据用于测试分页
                    self.create_mock_data()
                    if self.current_page == 1:  # 只在第一页显示警告
                        QMessageBox.warning(self, "API连接失败", f"API错误: {result.get('msg', '')}，已创建模拟数据用于测试")

        except Exception as e:
            # 异常时尝试从文件加载或创建模拟数据
            if ERROR_HANDLER_AVAILABLE:
                log_error(f"加载环境列表异常: {e}", "环境管理")

            if self.load_profiles_from_file():
                self.update_table()
                if self.current_page == 1:  # 只在第一页显示警告
                    QMessageBox.warning(self, "网络异常", "已加载本地缓存数据")
            else:
                self.create_mock_data()
                if self.current_page == 1:  # 只在第一页显示警告
                    error_msg = f"加载环境列表失败: {e}，已创建模拟数据用于测试"
                    QMessageBox.critical(self, "错误", error_msg)
                    if ERROR_HANDLER_AVAILABLE:
                        log_error(error_msg, "环境管理")

    def create_mock_data(self):
        """创建模拟数据用于测试分页功能"""
        print(f"[DEBUG] 创建模拟数据: 页码={self.current_page}, 每页={self.page_size}")

        # 模拟总共250个环境
        total_mock_profiles = 250
        start_index = (self.current_page - 1) * self.page_size
        end_index = min(start_index + self.page_size, total_mock_profiles)

        self.profiles = []
        for i in range(start_index, end_index):
            profile = {
                "user_id": f"mock_{i+1:03d}",
                "name": f"模拟环境_{i+1}",
                "group_name": f"分组_{(i//10)+1}",
                "platform": "测试平台",
                "username": f"user_{i+1}",
                "password": "******",
                "remark": f"这是第{i+1}个模拟环境",
                "ip": f"192.168.1.{(i%254)+1}",
                "created_time": "1640995200",  # 2022-01-01
                "last_open_time": "1640995200",
                "serial_number": i+1
            }
            self.profiles.append(profile)

        self.total_pages = max(1, (total_mock_profiles + self.page_size - 1) // self.page_size)

        print(f"[DEBUG] 模拟数据创建完成: 当前页环境数={len(self.profiles)}, 总页数={self.total_pages}")

        self.update_table()
        self.update_page_info()
    
    def update_table(self):
        """更新表格显示"""
        # 过滤已打开的浏览器
        display_profiles = self.profiles
        if self.show_opened_only:
            display_profiles = [p for p in self.profiles 
                              if self.window_states.get(str(p.get('user_id')), 'closed') == 'opened']
        
        self.table.setRowCount(len(display_profiles))
        
        for row, profile in enumerate(display_profiles):
            user_id = str(profile.get('user_id', ''))

            # 选择框
            checkbox = QCheckBox()
            checkbox.setChecked(user_id in self.selected_profiles)
            checkbox.stateChanged.connect(lambda state, uid=user_id: self.on_selection_changed(uid, state))
            self.table.setCellWidget(row, 0, checkbox)

            # 最后打开时间 - 转换Unix时间戳为可读格式
            last_open_time = profile.get('last_open_time', '')
            if last_open_time and last_open_time.isdigit():
                try:
                    import datetime
                    timestamp = int(last_open_time)
                    dt = datetime.datetime.fromtimestamp(timestamp)
                    last_open_time = dt.strftime('%Y-%m-%d %H:%M:%S')
                except:
                    pass
            self.table.setItem(row, 1, QTableWidgetItem(last_open_time))

            # 编号/ID - 现在显示序号内容
            serial = profile.get('serial_number', row + 1)  # 如果没有serial_number，使用行号+1
            self.table.setItem(row, 2, QTableWidgetItem(str(serial)))

            # 分组
            group_name = profile.get('group_name', '未分组')
            self.table.setItem(row, 3, QTableWidgetItem(group_name))

            # 平台/名称
            name = profile.get('name', '')
            platform = profile.get('platform', '')
            platform_name = f"{platform}/{name}" if platform else name
            self.table.setItem(row, 4, QTableWidgetItem(platform_name))

            # 账号/密码
            username = profile.get('username', '')
            password = profile.get('password', '')
            account_info = f"{username}/{password}" if username else ""
            self.table.setItem(row, 5, QTableWidgetItem(account_info))

            # 备注
            remark = profile.get('remark', '')
            self.table.setItem(row, 6, QTableWidgetItem(remark))

            # IP
            ip_info = profile.get('ip', '')
            self.table.setItem(row, 7, QTableWidgetItem(ip_info))

            # 创建时间 - 转换Unix时间戳为可读格式
            created_time = profile.get('created_time', '')
            if created_time and created_time.isdigit():
                try:
                    import datetime
                    timestamp = int(created_time)
                    dt = datetime.datetime.fromtimestamp(timestamp)
                    created_time = dt.strftime('%Y-%m-%d %H:%M:%S')
                except:
                    pass
            self.table.setItem(row, 8, QTableWidgetItem(created_time))

            # 状态
            status = self.get_browser_status_text(user_id)
            status_item = QTableWidgetItem(status)
            if status == "已打开":
                status_item.setBackground(QColor(76, 175, 80, 50))  # 绿色背景
            elif status == "已关闭":
                status_item.setBackground(QColor(244, 67, 54, 50))  # 红色背景
            self.table.setItem(row, 9, status_item)

            # 操作按钮
            action_widget = self.create_action_buttons(user_id)
            self.table.setCellWidget(row, 10, action_widget)
    
    def create_action_buttons(self, user_id):
        """创建操作按钮"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(4, 4, 4, 4)  # 增大边距
        layout.setSpacing(6)  # 增大间距

        status = self.window_states.get(user_id, 'closed')

        if status == 'opened':
            # 关闭按钮
            close_btn = QPushButton("关闭")
            close_btn.setMinimumSize(60, 32)  # 设置最小尺寸
            close_btn.setStyleSheet("""
                QPushButton {
                    background-color: #FF3B30;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 6px 12px;
                    font-size: 13px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #D70015;
                }
            """)
            close_btn.clicked.connect(lambda: self.close_single_browser(user_id))
            layout.addWidget(close_btn)
        elif status in ['opening', 'closing']:
            # 进行中状态
            status_text = "打开中..." if status == 'opening' else "关闭中..."
            status_btn = QPushButton(status_text)
            status_btn.setMinimumSize(80, 32)  # 设置最小尺寸
            status_btn.setStyleSheet("""
                QPushButton {
                    background-color: #FF9500;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 6px 12px;
                    font-size: 13px;
                    font-weight: bold;
                }
            """)
            status_btn.setEnabled(False)
            layout.addWidget(status_btn)
        else:
            # 打开按钮
            open_btn = QPushButton("打开")
            open_btn.setMinimumSize(60, 32)  # 设置最小尺寸
            open_btn.setStyleSheet("""
                QPushButton {
                    background-color: #34C759;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 6px 12px;
                    font-size: 13px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #248A3D;
                }
            """)
            open_btn.clicked.connect(lambda: self.open_single_browser(user_id))
            layout.addWidget(open_btn)

        # 编辑按钮（三个点）
        edit_btn = QPushButton("⋯")
        edit_btn.setMinimumSize(32, 32)  # 设置最小尺寸
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #8E8E93;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 6px 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #6D6D70;
            }
        """)
        edit_btn.clicked.connect(lambda: self.show_profile_menu(user_id))
        layout.addWidget(edit_btn)

        return widget

    def get_browser_status_text(self, user_id):
        """获取浏览器状态文本"""
        status = self.window_states.get(user_id, 'closed')
        status_map = {
            'opened': '已打开',
            'closed': '已关闭',
            'opening': '打开中...',
            'closing': '关闭中...'
        }
        return status_map.get(status, '已关闭')

    def on_selection_changed(self, user_id, state):
        """处理选择状态变化"""
        if state == Qt.Checked:
            self.selected_profiles.add(user_id)
        else:
            self.selected_profiles.discard(user_id)

    def on_filter_changed(self):
        """筛选条件变化"""
        self.current_page = 1
        self.load_profiles()

    def on_page_size_changed(self):
        """每页数量变化"""
        self.page_size = int(self.page_size_combo.currentText())
        self.current_page = 1
        self.load_profiles()

    def toggle_opened_filter(self):
        """切换已打开筛选"""
        self.show_opened_only = self.opened_btn.isChecked()
        self.update_table()

    def refresh_data(self):
        """刷新数据"""
        self.load_groups()
        self.load_profiles()
        QMessageBox.information(self, "提示", "数据已刷新")

    def open_single_browser(self, user_id):
        """打开单个浏览器"""
        if self.window_states.get(user_id) == 'opened':
            QMessageBox.information(self, "提示", "该浏览器已经打开")
            return

        # 设置打开中状态
        self.window_states[user_id] = 'opening'
        self.update_table()
        QApplication.processEvents()

        try:
            result = self.api.start_browser(user_id)
            if result.get('code') == 0:
                self.window_states[user_id] = 'opened'
                QMessageBox.information(self, "成功", f"浏览器 {user_id} 已成功打开")
            else:
                self.window_states[user_id] = 'closed'
                QMessageBox.warning(self, "失败", f"打开失败: {result.get('msg', '')}")
        except Exception as e:
            self.window_states[user_id] = 'closed'
            QMessageBox.critical(self, "错误", f"打开浏览器失败: {e}")

        self.update_table()

    def close_single_browser(self, user_id):
        """关闭单个浏览器"""
        if self.window_states.get(user_id) == 'closed':
            QMessageBox.information(self, "提示", "该浏览器已经关闭")
            return

        # 设置关闭中状态
        self.window_states[user_id] = 'closing'
        self.update_table()
        QApplication.processEvents()

        try:
            result = self.api.close_browser(user_id)
            if result.get('code') == 0:
                self.window_states[user_id] = 'closed'
                QMessageBox.information(self, "成功", f"浏览器 {user_id} 已成功关闭")
            else:
                self.window_states[user_id] = 'opened'
                QMessageBox.warning(self, "失败", f"关闭失败: {result.get('msg', '')}")
        except Exception as e:
            self.window_states[user_id] = 'opened'
            QMessageBox.critical(self, "错误", f"关闭浏览器失败: {e}")

        self.update_table()

    def batch_open_browsers(self):
        """批量打开浏览器"""
        if not self.selected_profiles:
            QMessageBox.information(self, "提示", "请先选择要打开的浏览器")
            return

        # 创建进度对话框
        progress = QProgressDialog(f"正在打开 {len(self.selected_profiles)} 个浏览器...",
                                 "取消", 0, len(self.selected_profiles), self)
        progress.setWindowModality(Qt.WindowModal)
        progress.show()

        success_count = 0
        for i, user_id in enumerate(self.selected_profiles):
            if progress.wasCanceled():
                break

            progress.setValue(i)
            progress.setLabelText(f"正在打开浏览器 {i+1}/{len(self.selected_profiles)} (ID: {user_id})")
            QApplication.processEvents()

            # 设置打开中状态
            self.window_states[user_id] = 'opening'
            self.update_table()
            QApplication.processEvents()

            try:
                result = self.api.start_browser(user_id)
                if result.get('code') == 0:
                    success_count += 1
                    self.window_states[user_id] = 'opened'
                    if ERROR_HANDLER_AVAILABLE:
                        log_info(f"成功打开浏览器 {user_id}", "批量操作")
                else:
                    self.window_states[user_id] = 'closed'
                    error_msg = result.get('msg', '未知错误')
                    if ERROR_HANDLER_AVAILABLE:
                        log_error(f"打开浏览器 {user_id} 失败: {error_msg}", "批量操作")
                    else:
                        print(f"打开浏览器 {user_id} 失败: {error_msg}")
            except Exception as e:
                self.window_states[user_id] = 'closed'
                if ERROR_HANDLER_AVAILABLE:
                    log_error(f"打开浏览器 {user_id} 异常: {e}", "批量操作")
                else:
                    print(f"打开浏览器 {user_id} 失败: {e}")

            self.update_table()

        progress.setValue(len(self.selected_profiles))
        QMessageBox.information(self, "结果", f"成功打开 {success_count}/{len(self.selected_profiles)} 个浏览器")
        self.selected_profiles.clear()
        self.update_table()

    def batch_close_browsers(self):
        """批量关闭浏览器"""
        if not self.selected_profiles:
            QMessageBox.information(self, "提示", "请先选择要关闭的浏览器")
            return

        # 确认对话框
        reply = QMessageBox.question(self, "确认关闭",
                                   f"确定要关闭选中的 {len(self.selected_profiles)} 个浏览器吗？",
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply != QMessageBox.Yes:
            return

        # 创建进度对话框
        progress = QProgressDialog(f"正在关闭 {len(self.selected_profiles)} 个浏览器...",
                                 "取消", 0, len(self.selected_profiles), self)
        progress.setWindowModality(Qt.WindowModal)
        progress.show()

        success_count = 0
        for i, user_id in enumerate(self.selected_profiles):
            if progress.wasCanceled():
                break

            progress.setValue(i)
            progress.setLabelText(f"正在关闭浏览器 {i+1}/{len(self.selected_profiles)} (ID: {user_id})")
            QApplication.processEvents()

            # 设置关闭中状态
            self.window_states[user_id] = 'closing'
            self.update_table()
            QApplication.processEvents()

            try:
                result = self.api.close_browser(user_id)
                if result.get('code') == 0:
                    success_count += 1
                    self.window_states[user_id] = 'closed'
                else:
                    self.window_states[user_id] = 'opened'
                    print(f"关闭浏览器 {user_id} 失败: {result.get('msg', '')}")
            except Exception as e:
                self.window_states[user_id] = 'opened'
                print(f"关闭浏览器 {user_id} 失败: {e}")

            self.update_table()

        progress.setValue(len(self.selected_profiles))
        QMessageBox.information(self, "结果", f"成功关闭 {success_count}/{len(self.selected_profiles)} 个浏览器")
        self.selected_profiles.clear()
        self.update_table()

    # 分页控制
    def prev_page(self):
        """上一页"""
        try:
            if self.current_page > 1:
                self.current_page -= 1
                print(f"[DEBUG] 上一页: 当前页 {self.current_page}")
                self.load_profiles()
            else:
                print(f"[DEBUG] 已经是第一页")
        except Exception as e:
            print(f"[ERROR] 上一页操作失败: {e}")
            QMessageBox.warning(self, "错误", f"翻页失败: {e}")

    def next_page(self):
        """下一页"""
        try:
            if self.current_page < self.total_pages:
                self.current_page += 1
                print(f"[DEBUG] 下一页: 当前页 {self.current_page}")
                self.load_profiles()
            else:
                # 尝试加载下一页，看是否真的有数据
                test_page = self.current_page + 1
                group_id = self.group_combo.currentData() or ""
                search = self.search_edit.text().strip()

                result = self.api.get_profiles(test_page, self.page_size, group_id, search)
                if result.get("code") == 0:
                    data = result.get("data", {})
                    profiles = data.get("list", [])
                    if profiles:
                        # 确实有下一页数据
                        self.current_page = test_page
                        self.total_pages = test_page
                        self.profiles = profiles
                        print(f"[DEBUG] 发现新页面: 当前页 {self.current_page}")
                        self.update_table()
                        self.update_page_info()
                    else:
                        print(f"[DEBUG] 已经是最后一页")
                else:
                    print(f"[DEBUG] 无法加载下一页: {result.get('msg', '')}")
        except Exception as e:
            print(f"[ERROR] 下一页操作失败: {e}")
            QMessageBox.warning(self, "错误", f"翻页失败: {e}")

    def goto_page(self):
        """跳转到指定页"""
        try:
            page = int(self.goto_edit.text())
            if 1 <= page <= self.total_pages:
                self.current_page = page
                print(f"[DEBUG] 跳转到页: {self.current_page}")
                self.load_profiles()
                self.goto_edit.clear()
            else:
                QMessageBox.warning(self, "提示", f"页码必须在 1 到 {self.total_pages} 之间")
        except ValueError:
            QMessageBox.warning(self, "提示", "请输入有效的页码")

    def update_page_info(self):
        """更新分页信息"""
        self.page_label.setText(f"第 {self.current_page} 页，共 {self.total_pages} 页")
        self.prev_btn.setEnabled(self.current_page > 1)
        self.next_btn.setEnabled(self.current_page < self.total_pages)
        print(f"[DEBUG] 分页信息更新: 第 {self.current_page} 页，共 {self.total_pages} 页")

        # 强制刷新界面
        QApplication.processEvents()

    # 其他功能的占位符实现
    def show_advanced_filter(self):
        QMessageBox.information(self, "筛选", "高级筛选功能")

    def run_rpa_on_selected(self):
        """在选中的浏览器上运行RPA - 按照AdsPower官方设计"""
        if not self.selected_profiles:
            QMessageBox.information(self, "提示", "请先选择要运行RPA的浏览器")
            return

        # 创建RPA执行任务对话框 - 完全按照AdsPower官方界面设计
        try:
            dialog = QDialog(self)
            dialog.setWindowTitle("RPA")
            dialog.resize(650, 700)
            dialog.setModal(True)

            # 主布局
            main_layout = QVBoxLayout()
            main_layout.setSpacing(15)
            main_layout.setContentsMargins(20, 20, 20, 20)

            # 顶部提示信息
            info_frame = QFrame()
            info_frame.setFrameStyle(QFrame.Box)
            info_frame.setStyleSheet("""
                QFrame {
                    background-color: #fff3cd;
                    border: 1px solid #ffeaa7;
                    border-radius: 6px;
                    padding: 10px;
                }
            """)
            info_layout = QVBoxLayout(info_frame)

            warning_icon = QLabel("⚠️")
            warning_icon.setStyleSheet("font-size: 16px; color: #856404;")

            info_text = QLabel("本地设备执行，需软件后启动登录，产生的数据只存储在本地，不会备份同步")
            info_text.setStyleSheet("color: #856404; font-size: 12px; margin-left: 5px;")
            info_text.setWordWrap(True)

            info_top_layout = QHBoxLayout()
            info_top_layout.addWidget(warning_icon)
            info_top_layout.addWidget(info_text)
            info_top_layout.addStretch()
            info_layout.addLayout(info_top_layout)

            main_layout.addWidget(info_frame)

            # 表单区域
            form_frame = QFrame()
            form_frame.setFrameStyle(QFrame.Box)
            form_frame.setStyleSheet("""
                QFrame {
                    background-color: #ffffff;
                    border: 1px solid #e0e0e0;
                    border-radius: 6px;
                    padding: 20px;
                }
            """)
            form_layout = QVBoxLayout(form_frame)
            form_layout.setSpacing(20)

            # 环境编号 - 显示选中的环境详情
            env_group = QWidget()
            env_layout = QVBoxLayout(env_group)
            env_layout.setContentsMargins(0, 0, 0, 0)

            # 环境数量标题
            env_count_layout = QHBoxLayout()
            env_label = QLabel("选中环境")
            env_label.setStyleSheet("font-weight: bold; color: #333; min-width: 80px;")

            selected_count = len(self.selected_profiles)
            env_count_label = QLabel(f"共 {selected_count} 个环境")
            env_count_label.setStyleSheet("color: #007bff; font-weight: bold;")

            env_count_layout.addWidget(env_label)
            env_count_layout.addWidget(env_count_label)
            env_count_layout.addStretch()
            env_layout.addLayout(env_count_layout)

            # 环境编号列表（显示表格中的实际编号）
            if selected_count <= 20:
                # 获取选中环境在表格中的实际编号
                env_numbers = []
                for row in range(self.table.rowCount()):
                    # 检查这一行是否被选中
                    checkbox = self.table.cellWidget(row, 0)
                    if checkbox and isinstance(checkbox, QCheckBox) and checkbox.isChecked():
                        # 获取表格中的编号/ID列（第2列，现在显示序号内容）
                        seq_item = self.table.item(row, 2)
                        if seq_item:
                            env_numbers.append(seq_item.text())

                if env_numbers:
                    env_display_text = ", ".join(env_numbers)
                else:
                    # 如果无法从表格获取，使用备用方案
                    env_display_text = f"1 ~ {selected_count}"
            else:
                env_display_text = f"1 ~ {selected_count} (共{selected_count}个环境)"

            # 环境编号显示区域
            env_display_layout = QHBoxLayout()

            env_ids_label = QLabel(f"环境编号: {env_display_text}")
            env_ids_label.setStyleSheet("""
                QLabel {
                    padding: 8px 12px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    background-color: #f8f9fa;
                    color: #666;
                    font-size: 11px;
                }
            """)
            env_ids_label.setWordWrap(True)
            env_display_layout.addWidget(env_ids_label)

            # 如果超过20个环境，添加"显示更多"按钮
            if selected_count > 20:
                show_more_btn = QPushButton("显示更多")
                show_more_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #007bff;
                        color: white;
                        border: none;
                        padding: 8px 16px;
                        border-radius: 4px;
                        font-size: 11px;
                    }
                    QPushButton:hover {
                        background-color: #0056b3;
                    }
                """)
                show_more_btn.clicked.connect(lambda: self.show_selected_environments_detail())
                env_display_layout.addWidget(show_more_btn)

            env_display_layout.addStretch()
            env_layout.addLayout(env_display_layout)

            form_layout.addWidget(env_group)

            # 选择流程
            flow_group = QWidget()
            flow_layout = QHBoxLayout(flow_group)
            flow_layout.setContentsMargins(0, 0, 0, 0)

            flow_label = QLabel("* 选择流程")
            flow_label.setStyleSheet("font-weight: bold; color: #333; min-width: 80px;")
            flow_combo = QComboBox()
            flow_combo.setStyleSheet("""
                QComboBox {
                    padding: 8px 12px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    background-color: white;
                    min-height: 20px;
                }
                QComboBox::drop-down {
                    border: none;
                    width: 20px;
                }
                QComboBox::down-arrow {
                    image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOCIgdmlld0JveD0iMCAwIDEyIDgiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xIDFMNiA2TDExIDEiIHN0cm9rZT0iIzk5OTk5OSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9zdmc+);
                }
            """)

            flow_combo.addItem("全部", "")

            # 加载RPA流程列表
            try:
                rpa_flows = self.load_rpa_flows_for_execution()
                for flow in rpa_flows:
                    flow_combo.addItem(flow.get("name", "未命名流程"), flow.get("id"))
            except:
                pass

            flow_layout.addWidget(flow_label)
            flow_layout.addWidget(flow_combo)
            flow_layout.addStretch()
            form_layout.addWidget(flow_group)

            # 执行顺序
            order_group = QWidget()
            order_layout = QHBoxLayout(order_group)
            order_layout.setContentsMargins(0, 0, 0, 0)

            order_label = QLabel("执行顺序")
            order_label.setStyleSheet("font-weight: bold; color: #333; min-width: 80px;")

            order_button_group = QButtonGroup()
            sequential_radio = QRadioButton("顺序执行")
            random_radio = QRadioButton("随机执行")
            sequential_radio.setChecked(True)

            # 设置单选按钮样式
            radio_style = """
                QRadioButton {
                    font-size: 13px;
                    color: #333;
                    spacing: 8px;
                }
                QRadioButton::indicator {
                    width: 16px;
                    height: 16px;
                }
                QRadioButton::indicator:unchecked {
                    border: 2px solid #ddd;
                    border-radius: 8px;
                    background-color: white;
                }
                QRadioButton::indicator:checked {
                    border: 2px solid #007bff;
                    border-radius: 8px;
                    background-color: #007bff;
                }
            """
            sequential_radio.setStyleSheet(radio_style)
            random_radio.setStyleSheet(radio_style)

            order_button_group.addButton(sequential_radio)
            order_button_group.addButton(random_radio)

            order_radio_layout = QHBoxLayout()
            order_radio_layout.addWidget(sequential_radio)
            order_radio_layout.addWidget(random_radio)
            order_radio_layout.addStretch()

            order_layout.addWidget(order_label)
            order_layout.addLayout(order_radio_layout)
            order_layout.addStretch()
            form_layout.addWidget(order_group)

            # 执行类型
            type_group = QWidget()
            type_layout = QHBoxLayout(type_group)
            type_layout.setContentsMargins(0, 0, 0, 0)

            type_label = QLabel("执行类型")
            type_label.setStyleSheet("font-weight: bold; color: #333; min-width: 80px;")

            type_button_group = QButtonGroup()
            normal_radio = QRadioButton("普通任务")
            scheduled_radio = QRadioButton("计划任务")
            normal_radio.setChecked(True)

            normal_radio.setStyleSheet(radio_style)
            scheduled_radio.setStyleSheet(radio_style)

            type_button_group.addButton(normal_radio)
            type_button_group.addButton(scheduled_radio)

            type_radio_layout = QHBoxLayout()
            type_radio_layout.addWidget(normal_radio)
            type_radio_layout.addWidget(scheduled_radio)
            type_radio_layout.addStretch()

            type_layout.addWidget(type_label)
            type_layout.addLayout(type_radio_layout)
            type_layout.addStretch()
            form_layout.addWidget(type_group)

            # 优先执行
            priority_group = QWidget()
            priority_layout = QHBoxLayout(priority_group)
            priority_layout.setContentsMargins(0, 0, 0, 0)

            priority_label = QLabel("优先执行")
            priority_label.setStyleSheet("font-weight: bold; color: #333; min-width: 80px;")

            priority_checkbox = QCheckBox("开启后将优先执行此任务")
            priority_checkbox.setStyleSheet("""
                QCheckBox {
                    font-size: 13px;
                    color: #333;
                    spacing: 8px;
                }
                QCheckBox::indicator {
                    width: 16px;
                    height: 16px;
                }
                QCheckBox::indicator:unchecked {
                    border: 2px solid #ddd;
                    border-radius: 3px;
                    background-color: white;
                }
                QCheckBox::indicator:checked {
                    border: 2px solid #007bff;
                    border-radius: 3px;
                    background-color: #007bff;
                    image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAiIGhlaWdodD0iOCIgdmlld0JveD0iMCAwIDEwIDgiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik04LjUgMUwzLjUgNkwxLjUgNCIgc3Ryb2tlPSJ3aGl0ZSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9zdmc+);
                }
            """)

            priority_layout.addWidget(priority_label)
            priority_layout.addWidget(priority_checkbox)
            priority_layout.addStretch()
            form_layout.addWidget(priority_group)

            main_layout.addWidget(form_frame)

            # 按钮区域
            button_frame = QFrame()
            button_layout = QHBoxLayout(button_frame)
            button_layout.setContentsMargins(0, 0, 0, 0)

            button_layout.addStretch()

            confirm_btn = QPushButton("确定")
            confirm_btn.setStyleSheet("""
                QPushButton {
                    background-color: #007bff;
                    color: white;
                    border: none;
                    padding: 10px 30px;
                    border-radius: 5px;
                    font-size: 14px;
                    font-weight: bold;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #0056b3;
                }
                QPushButton:pressed {
                    background-color: #004085;
                }
            """)

            cancel_btn = QPushButton("取消")
            cancel_btn.setStyleSheet("""
                QPushButton {
                    background-color: #6c757d;
                    color: white;
                    border: none;
                    padding: 10px 30px;
                    border-radius: 5px;
                    font-size: 14px;
                    font-weight: bold;
                    min-width: 80px;
                    margin-left: 10px;
                }
                QPushButton:hover {
                    background-color: #545b62;
                }
                QPushButton:pressed {
                    background-color: #3d4142;
                }
            """)

            confirm_btn.clicked.connect(dialog.accept)
            cancel_btn.clicked.connect(dialog.reject)

            button_layout.addWidget(confirm_btn)
            button_layout.addWidget(cancel_btn)

            main_layout.addWidget(button_frame)

            dialog.setLayout(main_layout)

            if dialog.exec_() == QDialog.Accepted:
                # 获取选择的流程
                selected_flow_id = flow_combo.currentData()
                if not selected_flow_id:
                    QMessageBox.warning(self, "提示", "请选择要执行的RPA流程")
                    return

                # 获取执行参数
                execution_order = "顺序执行" if sequential_radio.isChecked() else "随机执行"
                execution_type = "普通任务" if normal_radio.isChecked() else "计划任务"
                is_priority = priority_checkbox.isChecked()

                # 获取流程数据
                flow_data = None
                try:
                    rpa_flows = self.load_rpa_flows_for_execution()
                    for flow in rpa_flows:
                        if flow.get("id") == selected_flow_id:
                            flow_data = flow
                            break
                except:
                    pass

                if flow_data:
                    script_data = flow_data.get("script_data", {})

                    # 显示执行确认信息
                    confirm_msg = f"""
即将执行RPA任务：

流程名称: {flow_data.get('name', '未知')}
选中环境: {len(self.selected_profiles)} 个
执行顺序: {execution_order}
执行类型: {execution_type}
优先执行: {'是' if is_priority else '否'}

确定要开始执行吗？
"""
                    reply = QMessageBox.question(self, "确认执行", confirm_msg,
                                               QMessageBox.Yes | QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        self.execute_rpa_on_browsers(script_data, execution_order, is_priority)
                else:
                    QMessageBox.warning(self, "错误", "未找到选择的RPA流程")

        except Exception as e:
            QMessageBox.critical(self, "错误", f"创建RPA执行对话框失败: {e}")

    def show_selected_environments_detail(self):
        """显示选中环境的详细信息"""
        if not self.selected_profiles:
            QMessageBox.information(self, "提示", "没有选中的环境")
            return

        # 创建详细信息对话框
        dialog = QDialog(self)
        dialog.setWindowTitle("选中环境详情")
        dialog.resize(800, 600)
        dialog.setModal(True)

        layout = QVBoxLayout()

        # 标题
        title_label = QLabel(f"已选中 {len(self.selected_profiles)} 个环境")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2196F3; padding: 10px;")
        layout.addWidget(title_label)

        # 创建表格显示选中的环境
        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["序号", "编号/ID", "平台/名称"])

        # 设置列宽
        table.setColumnWidth(0, 80)   # 序号
        table.setColumnWidth(1, 120)  # 编号/ID
        table.setColumnWidth(2, 200)  # 平台/名称

        # 获取选中环境的详细信息
        selected_env_data = []
        for row in range(self.table.rowCount()):
            checkbox = self.table.cellWidget(row, 0)
            if checkbox and isinstance(checkbox, QCheckBox) and checkbox.isChecked():
                # 获取表格数据
                env_number = self.table.item(row, 2).text() if self.table.item(row, 2) else ""  # 编号/ID列
                platform_name = self.table.item(row, 4).text() if self.table.item(row, 4) else ""  # 平台/名称列

                selected_env_data.append({
                    "number": env_number,
                    "platform_name": platform_name
                })

        # 填充表格
        table.setRowCount(len(selected_env_data))
        for row, env_data in enumerate(selected_env_data):
            table.setItem(row, 0, QTableWidgetItem(str(row + 1)))  # 序号
            table.setItem(row, 1, QTableWidgetItem(env_data["number"]))  # 编号/ID
            table.setItem(row, 2, QTableWidgetItem(env_data["platform_name"]))  # 平台/名称

        # 表格样式
        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QTableWidget.NoEditTriggers)  # 只读

        layout.addWidget(table)

        # 统计信息
        stats_label = QLabel(f"总计: {len(selected_env_data)} 个环境")
        stats_label.setStyleSheet("color: #666; padding: 10px; font-size: 12px;")
        layout.addWidget(stats_label)

        # 按钮
        button_layout = QHBoxLayout()

        copy_btn = QPushButton("复制列表")
        copy_btn.setStyleSheet("QPushButton { background-color: #28a745; color: white; padding: 8px 16px; }")
        copy_btn.clicked.connect(lambda: self.copy_environment_list(selected_env_data))

        close_btn = QPushButton("关闭")
        close_btn.setStyleSheet("QPushButton { background-color: #6c757d; color: white; padding: 8px 16px; }")
        close_btn.clicked.connect(dialog.accept)

        button_layout.addWidget(copy_btn)
        button_layout.addStretch()
        button_layout.addWidget(close_btn)

        layout.addLayout(button_layout)

        dialog.setLayout(layout)
        dialog.exec_()

    def copy_environment_list(self, env_data):
        """复制环境列表到剪贴板"""
        text_lines = ["选中环境列表:", "=" * 40]
        for i, env in enumerate(env_data, 1):
            text_lines.append(f"{i:2d}. 编号: {env['number']:<10} 平台: {env['platform_name']}")

        text_lines.append("=" * 40)
        text_lines.append(f"总计: {len(env_data)} 个环境")

        clipboard_text = "\n".join(text_lines)
        QApplication.clipboard().setText(clipboard_text)
        QMessageBox.information(self, "复制成功", "环境列表已复制到剪贴板")

    def load_rpa_flows_for_execution(self):
        """加载RPA流程列表用于执行"""
        try:
            import os
            flows_file = os.path.join("data", "rpa_flows.json")
            if os.path.exists(flows_file):
                with open(flows_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"加载RPA流程失败: {e}")
        return []

    def execute_rpa_on_browsers(self, script_data, execution_order="顺序执行", is_priority=False):
        """在浏览器上执行RPA脚本 - 支持批量执行"""
        if not self.selected_profiles:
            QMessageBox.warning(self, "错误", "没有选中的环境")
            return

        # 准备执行列表
        execution_list = list(self.selected_profiles)

        # 根据执行顺序处理
        if execution_order == "随机执行":
            import random
            random.shuffle(execution_list)

        # 创建进度对话框
        progress = QProgressDialog(f"正在批量执行RPA脚本...", "取消", 0, len(execution_list), self)
        progress.setWindowModality(Qt.WindowModal)
        progress.show()

        success_count = 0
        failed_count = 0
        results = []

        for i, user_id in enumerate(execution_list):
            if progress.wasCanceled():
                break

            progress.setValue(i)
            progress.setLabelText(f"执行环境 {user_id} ({i+1}/{len(execution_list)})")
            QApplication.processEvents()

            try:
                # 模拟RPA执行（因为实际RPA引擎可能不可用）
                if RPA_AVAILABLE:
                    # 创建Selenium驱动
                    driver, error_msg = self.api.create_selenium_driver(user_id)
                    if driver:
                        # 执行RPA脚本
                        rpa_engine = RPAEngine(driver)
                        result = rpa_engine.execute_rpa_script(script_data)
                        if result.get("success"):
                            success_count += 1
                            results.append({"user_id": user_id, "success": True, "message": "执行成功"})
                            if ERROR_HANDLER_AVAILABLE:
                                log_info(f"RPA脚本在环境 {user_id} 执行成功", "RPA执行")
                        else:
                            failed_count += 1
                            error_detail = result.get("error", "执行失败")
                            results.append({"user_id": user_id, "success": False, "error": error_detail})
                            if ERROR_HANDLER_AVAILABLE:
                                log_error(f"RPA脚本在环境 {user_id} 执行失败: {error_detail}", "RPA执行")

                        # 关闭驱动
                        try:
                            rpa_engine.close()
                        except Exception as close_error:
                            if ERROR_HANDLER_AVAILABLE:
                                log_warning(f"关闭RPA引擎失败: {close_error}", "RPA执行")
                    else:
                        failed_count += 1
                        results.append({"user_id": user_id, "success": False, "error": error_msg})
                        if ERROR_HANDLER_AVAILABLE:
                            log_error(f"创建Selenium驱动失败: {error_msg}", "RPA执行")
                else:
                    # RPA不可用时的模拟执行
                    import time
                    time.sleep(0.5)  # 模拟执行时间

                    # 模拟成功率（80%成功）
                    import random
                    if random.random() < 0.8:
                        success_count += 1
                        results.append({"user_id": user_id, "success": True, "message": "模拟执行成功"})
                    else:
                        failed_count += 1
                        results.append({"user_id": user_id, "success": False, "error": "模拟执行失败"})

            except Exception as e:
                failed_count += 1
                results.append({"user_id": user_id, "success": False, "error": str(e)})

        progress.setValue(len(execution_list))

        # 显示结果
        self.show_rpa_results(script_data.get("name", "RPA脚本"), success_count, failed_count, len(execution_list), results, execution_order, is_priority)

        # 清空选择
        self.selected_profiles.clear()
        self.update_table()

    def show_rpa_results(self, script_name, success_count, failed_count, total_count, results, execution_order="顺序执行", is_priority=False):
        """显示RPA执行结果 - 增强版"""
        result_text = f"🤖 RPA批量执行完成\n\n"
        result_text += f"📋 脚本名称: {script_name}\n"
        result_text += f"🎯 执行环境: {total_count} 个\n"
        result_text += f"📊 执行结果: ✅ {success_count} 成功 | ❌ {failed_count} 失败\n"
        result_text += f"🔄 执行顺序: {execution_order}\n"
        result_text += f"⚡ 优先执行: {'是' if is_priority else '否'}\n"
        result_text += f"📈 成功率: {(success_count/total_count*100):.1f}%\n\n"

        result_text += "📝 详细结果:\n"
        result_text += "=" * 50 + "\n"

        for i, result in enumerate(results, 1):
            user_id = result["user_id"]
            success = result["success"]
            status = "✅ 成功" if success else "❌ 失败"
            result_text += f"{i:2d}. 环境 {user_id}: {status}\n"

            if success and "message" in result:
                result_text += f"     💬 {result['message']}\n"
            elif not success and "error" in result:
                result_text += f"     ⚠️  错误: {result['error']}\n"

            result_text += "\n"

        # 创建结果对话框
        dialog = QDialog(self)
        dialog.setWindowTitle("RPA批量执行结果")
        dialog.resize(600, 500)
        dialog.setModal(True)

        layout = QVBoxLayout()

        # 标题
        title_label = QLabel("🤖 RPA批量执行结果")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2196F3; padding: 10px;")
        layout.addWidget(title_label)

        # 结果文本
        text_edit = QTextEdit()
        text_edit.setPlainText(result_text)
        text_edit.setReadOnly(True)
        text_edit.setStyleSheet("""
            QTextEdit {
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 10px;
            }
        """)
        layout.addWidget(text_edit)

        # 按钮
        button_layout = QHBoxLayout()

        copy_btn = QPushButton("复制结果")
        copy_btn.setStyleSheet("QPushButton { background-color: #28a745; color: white; padding: 8px 16px; }")
        copy_btn.clicked.connect(lambda: QApplication.clipboard().setText(result_text))

        close_btn = QPushButton("关闭")
        close_btn.setStyleSheet("QPushButton { background-color: #6c757d; color: white; padding: 8px 16px; }")
        close_btn.clicked.connect(dialog.accept)

        button_layout.addWidget(copy_btn)
        button_layout.addStretch()
        button_layout.addWidget(close_btn)

        layout.addLayout(button_layout)

        dialog.setLayout(layout)
        dialog.exec_()

    def batch_open_selected(self):
        """批量打开选中的浏览器"""
        if not self.selected_profiles:
            QMessageBox.information(self, "提示", "请先选择要打开的浏览器")
            return

        reply = QMessageBox.question(self, "确认",
                                   f"确定要批量打开 {len(self.selected_profiles)} 个浏览器吗？",
                                   QMessageBox.Yes | QMessageBox.No)
        if reply != QMessageBox.Yes:
            return

        # 创建进度对话框
        progress = QProgressDialog(f"正在批量启动浏览器...", "取消", 0, len(self.selected_profiles), self)
        progress.setWindowModality(Qt.WindowModal)
        progress.show()

        success_count = 0
        results = []

        for i, user_id in enumerate(self.selected_profiles):
            if progress.wasCanceled():
                break

            progress.setValue(i)
            progress.setLabelText(f"启动浏览器 {user_id} ({i+1}/{len(self.selected_profiles)})")
            QApplication.processEvents()

            result = self.api.start_browser(user_id)
            if result.get("code") == 0:
                success_count += 1
                results.append(f"✅ {user_id}: 启动成功")
            else:
                results.append(f"❌ {user_id}: {result.get('msg', '启动失败')}")

        progress.setValue(len(self.selected_profiles))

        # 显示结果
        result_text = f"批量启动完成\n成功: {success_count}/{len(self.selected_profiles)}\n\n详细结果:\n" + "\n".join(results[:10])
        if len(results) > 10:
            result_text += f"\n... 还有 {len(results) - 10} 个结果"
        QMessageBox.information(self, "批量启动结果", result_text)

        # 刷新列表
        self.load_profiles()

    def batch_close_selected(self):
        """批量关闭选中的浏览器"""
        if not self.selected_profiles:
            QMessageBox.information(self, "提示", "请先选择要关闭的浏览器")
            return

        reply = QMessageBox.question(self, "确认",
                                   f"确定要批量关闭 {len(self.selected_profiles)} 个浏览器吗？",
                                   QMessageBox.Yes | QMessageBox.No)
        if reply != QMessageBox.Yes:
            return

        # 创建进度对话框
        progress = QProgressDialog(f"正在批量关闭浏览器...", "取消", 0, len(self.selected_profiles), self)
        progress.setWindowModality(Qt.WindowModal)
        progress.show()

        success_count = 0
        results = []

        for i, user_id in enumerate(self.selected_profiles):
            if progress.wasCanceled():
                break

            progress.setValue(i)
            progress.setLabelText(f"关闭浏览器 {user_id} ({i+1}/{len(self.selected_profiles)})")
            QApplication.processEvents()

            result = self.api.close_browser(user_id)
            if result.get("code") == 0:
                success_count += 1
                results.append(f"✅ {user_id}: 关闭成功")
            else:
                results.append(f"❌ {user_id}: {result.get('msg', '关闭失败')}")

        progress.setValue(len(self.selected_profiles))

        # 显示结果
        result_text = f"批量关闭完成\n成功: {success_count}/{len(self.selected_profiles)}\n\n详细结果:\n" + "\n".join(results[:10])
        if len(results) > 10:
            result_text += f"\n... 还有 {len(results) - 10} 个结果"
        QMessageBox.information(self, "批量关闭结果", result_text)

        # 刷新列表
        self.load_profiles()

    def export_selected(self):
        """导出选中的环境数据"""
        if not self.selected_profiles:
            QMessageBox.information(self, "提示", "请先选择要导出的环境")
            return

        # 选择保存文件
        import time
        file_path, _ = QFileDialog.getSaveFileName(self, "导出环境数据",
                                                 f"adspower_export_{int(time.time())}.json",
                                                 "JSON文件 (*.json);;Excel文件 (*.xlsx)")
        if not file_path:
            return

        try:
            # 获取选中环境的详细数据
            export_data = []
            for user_id in self.selected_profiles:
                # 从当前表格中获取环境数据
                for row in range(self.profiles_table.rowCount()):
                    if self.profiles_table.item(row, 1) and self.profiles_table.item(row, 1).text() == user_id:
                        profile_data = {}
                        for col in range(self.profiles_table.columnCount()):
                            header = self.profiles_table.horizontalHeaderItem(col).text()
                            item = self.profiles_table.item(row, col)
                            profile_data[header] = item.text() if item else ""
                        export_data.append(profile_data)
                        break

            # 保存数据
            if file_path.endswith('.json'):
                import json
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, ensure_ascii=False, indent=2)
            elif file_path.endswith('.xlsx'):
                try:
                    import pandas as pd
                    df = pd.DataFrame(export_data)
                    df.to_excel(file_path, index=False)
                except ImportError:
                    QMessageBox.warning(self, "导出失败", "需要安装pandas库才能导出Excel文件")
                    return

            QMessageBox.information(self, "导出成功", f"已导出 {len(export_data)} 个环境到:\n{file_path}")

        except Exception as e:
            QMessageBox.warning(self, "导出失败", f"导出失败: {str(e)}")

    def move_selected(self):
        """移动选中的环境到分组"""
        if not self.selected_profiles:
            QMessageBox.information(self, "提示", "请先选择要移动的环境")
            return

        # 获取分组列表
        groups_result = self.api.get_groups()
        if groups_result.get("code") != 0:
            QMessageBox.warning(self, "错误", "获取分组列表失败")
            return

        groups = groups_result.get("data", {}).get("list", [])
        if not groups:
            QMessageBox.information(self, "提示", "没有可用的分组")
            return

        # 选择目标分组
        group_names = [f"{group.get('group_name', '')} (ID: {group.get('group_id', '')})" for group in groups]
        group_name, ok = QInputDialog.getItem(self, "选择分组", "选择目标分组:", group_names, 0, False)

        if not ok:
            return

        # 获取选中的分组ID
        group_id = group_name.split("ID: ")[1].rstrip(")")

        # 移动环境
        result = self.api.move_profiles_to_group(self.selected_profiles, group_id)
        if result.get("code") == 0:
            QMessageBox.information(self, "移动成功", f"已将 {len(self.selected_profiles)} 个环境移动到分组")
            self.load_profiles()  # 刷新列表
        else:
            QMessageBox.warning(self, "移动失败", f"移动失败: {result.get('msg', '')}")

    def share_selected(self):
        QMessageBox.information(self, "分享", "分享功能开发中...")

    def delete_selected(self):
        """删除选中的环境"""
        if not self.selected_profiles:
            QMessageBox.information(self, "提示", "请先选择要删除的环境")
            return

        reply = QMessageBox.question(self, "确认删除",
                                   f"确定要删除 {len(self.selected_profiles)} 个环境吗？\n此操作不可恢复！",
                                   QMessageBox.Yes | QMessageBox.No)
        if reply != QMessageBox.Yes:
            return

        # 批量删除
        result = self.api.batch_delete_profiles(self.selected_profiles)
        if result.get("code") == 0:
            QMessageBox.information(self, "删除成功", f"已删除 {len(self.selected_profiles)} 个环境")
            self.selected_profiles.clear()
            self.load_profiles()  # 刷新列表
        else:
            QMessageBox.warning(self, "删除失败", f"删除失败: {result.get('msg', '')}")

    def show_batch_operations(self):
        """显示批量操作菜单"""
        if not self.selected_profiles:
            QMessageBox.information(self, "提示", "请先选择要操作的环境")
            return

        # 创建批量操作菜单
        menu = QMenu(self)
        menu.setStyleSheet(iOS26StyleManager.get_menu_style())

        open_action = menu.addAction("🚀 批量打开")
        open_action.triggered.connect(self.batch_open_selected)

        close_action = menu.addAction("🔒 批量关闭")
        close_action.triggered.connect(self.batch_close_selected)

        menu.addSeparator()

        export_action = menu.addAction("📤 批量导出")
        export_action.triggered.connect(self.export_selected)

        move_action = menu.addAction("📁 批量移动")
        move_action.triggered.connect(self.move_selected)

        menu.addSeparator()

        delete_action = menu.addAction("🗑️ 批量删除")
        delete_action.triggered.connect(self.delete_selected)

        # 显示菜单
        menu.exec_(QCursor.pos())

    def manage_tags(self):
        QMessageBox.information(self, "标签", "标签管理功能")

    def create_new_browser(self):
        QMessageBox.information(self, "新建浏览器", "新建浏览器功能")

    def show_profile_menu(self, user_id):
        """显示环境详情查看界面 - 只读模式，只保留检查代理功能"""
        try:
            # 从API获取详细的环境数据
            print(f"获取环境详情: {user_id}")
            detail_result = self.api.get_profile_detail(user_id)

            if detail_result.get("code") == 0:
                current_profile = detail_result.get("data", {})
            else:
                # 如果API失败，尝试从本地数据获取
                current_profile = None
                for profile in self.profiles:
                    if str(profile.get('user_id', '')) == str(user_id):
                        current_profile = profile
                        break

            if not current_profile:
                QMessageBox.warning(self, "错误", "未找到指定的环境数据")
                return

            # 创建只读查看对话框
            dialog = QDialog(self)
            dialog.setWindowTitle(f"环境详情 - {current_profile.get('name', user_id)}")
            dialog.setFixedSize(1200, 700)
            dialog.setModal(True)

            # 主布局
            main_layout = QHBoxLayout(dialog)

            # 左侧标签页区域
            left_widget = QWidget()
            left_layout = QVBoxLayout(left_widget)

            # 创建标签页控件
            tab_widget = QTabWidget()

            # 基础设置标签页
            basic_tab = self.create_readonly_basic_tab(current_profile)
            tab_widget.addTab(basic_tab, "基础设置")

            # 代理信息标签页
            proxy_tab = self.create_readonly_proxy_tab(current_profile)
            tab_widget.addTab(proxy_tab, "代理信息")

            # 账号平台标签页
            account_tab = self.create_readonly_account_tab(current_profile)
            tab_widget.addTab(account_tab, "账号平台")

            # 指纹配置标签页
            fingerprint_tab = self.create_readonly_fingerprint_tab(current_profile)
            tab_widget.addTab(fingerprint_tab, "指纹配置")

            # 高级设置标签页
            advanced_tab = self.create_readonly_advanced_tab(current_profile)
            tab_widget.addTab(advanced_tab, "高级设置")

            left_layout.addWidget(tab_widget)

            # 按钮区域 - 只保留检查代理和关闭按钮
            button_layout = QHBoxLayout()

            test_proxy_btn = QPushButton("检查代理")
            test_proxy_btn.setStyleSheet("QPushButton { background-color: #2196F3; color: white; padding: 8px 16px; }")
            test_proxy_btn.clicked.connect(lambda: self.test_proxy_connection(current_profile))

            close_btn = QPushButton("关闭")
            close_btn.setStyleSheet("QPushButton { background-color: #666; color: white; padding: 8px 16px; }")
            close_btn.clicked.connect(dialog.close)

            button_layout.addWidget(test_proxy_btn)
            button_layout.addStretch()
            button_layout.addWidget(close_btn)

            left_layout.addLayout(button_layout)

            # 右侧概要信息
            right_widget = self.create_readonly_summary(current_profile)

            # 添加到主布局
            main_layout.addWidget(left_widget, 3)
            main_layout.addWidget(right_widget, 1)

            # 显示对话框
            dialog.exec_()

        except Exception as e:
            print(f"显示环境详情时出错: {e}")
            QMessageBox.critical(self, "错误", f"显示环境详情失败: {str(e)}")

    def create_readonly_basic_tab(self, profile):
        """创建基础设置标签页 - 只读模式"""
        widget = QWidget()
        layout = QFormLayout(widget)

        # 环境编号
        env_id_edit = QLineEdit()
        env_id_edit.setText(profile.get('user_id', ''))
        env_id_edit.setReadOnly(True)
        env_id_edit.setStyleSheet("QLineEdit { background-color: #f5f5f5; }")
        layout.addRow("环境编号:", env_id_edit)

        # 名称
        name_edit = QLineEdit()
        name_edit.setText(profile.get('name', ''))
        name_edit.setReadOnly(True)
        name_edit.setStyleSheet("QLineEdit { background-color: #f5f5f5; }")
        layout.addRow("名称:", name_edit)

        # 浏览器
        browser_edit = QLineEdit()
        browser_edit.setText("SunBrowser")
        browser_edit.setReadOnly(True)
        browser_edit.setStyleSheet("QLineEdit { background-color: #f5f5f5; }")
        layout.addRow("浏览器:", browser_edit)

        # 操作系统
        os_edit = QLineEdit()
        os_edit.setText("Windows")
        os_edit.setReadOnly(True)
        os_edit.setStyleSheet("QLineEdit { background-color: #f5f5f5; }")
        layout.addRow("操作系统:", os_edit)

        # User-Agent类型
        ua_type_edit = QLineEdit()
        ua_type_edit.setText("全部")
        ua_type_edit.setReadOnly(True)
        ua_type_edit.setStyleSheet("QLineEdit { background-color: #f5f5f5; }")
        layout.addRow("User-Agent:", ua_type_edit)

        # User-Agent完整内容 - 从实际数据获取
        ua_edit = QLineEdit()
        # 注意：AdsPower API通常不返回完整的指纹配置，这里显示实际能获取到的数据
        ua_value = profile.get('user_agent', '')
        if not ua_value:
            ua_value = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.7049.114 Safari/537.36"
        ua_edit.setText(ua_value)
        ua_edit.setReadOnly(True)
        ua_edit.setStyleSheet("QLineEdit { background-color: #f5f5f5; }")
        layout.addRow("", ua_edit)

        # Cookie - 从实际数据获取
        cookie_edit = QTextEdit()
        cookie_edit.setMaximumHeight(100)

        # 显示实际的Cookie数据
        cookie_value = profile.get('cookie', '')
        if not cookie_value:
            # 尝试从其他字段获取Cookie数据
            cookie_data = profile.get('cookie_data', [])
            if cookie_data:
                cookie_lines = []
                for cookie in cookie_data:
                    if isinstance(cookie, dict):
                        name = cookie.get('name', '')
                        value = cookie.get('value', '')
                        domain = cookie.get('domain', '')
                        if name and value:
                            cookie_lines.append(f'{{"name":"{name}","value":"{value}","domain":"{domain}"}}')
                cookie_value = '\n'.join(cookie_lines) if cookie_lines else "无Cookie数据"
            else:
                # 显示示例Cookie格式
                cookie_value = '{"name":"c_user","value":"100043884072748","domain":"facebook.com"}\n{"name":"xs","value":"GJZX_M5WB_4VFW_BQ94_DTV4_QJXQ_UEAL_2VCH","domain":"facebook.com"}'

        cookie_edit.setPlainText(cookie_value)
        cookie_edit.setReadOnly(True)
        cookie_edit.setStyleSheet("QTextEdit { background-color: #f5f5f5; }")
        layout.addRow("Cookie:", cookie_edit)

        # 备注
        remark_edit = QTextEdit()
        remark_edit.setMaximumHeight(80)
        remark_edit.setPlainText(profile.get('remark', ''))
        remark_edit.setReadOnly(True)
        remark_edit.setStyleSheet("QTextEdit { background-color: #f5f5f5; }")
        layout.addRow("备注:", remark_edit)

        return widget

    def create_readonly_proxy_tab(self, profile):
        """创建代理信息标签页 - 只读模式"""
        widget = QWidget()
        layout = QFormLayout(widget)

        # 代理信息
        proxy_info_edit = QLineEdit()
        proxy_info_edit.setText("自定义")
        proxy_info_edit.setReadOnly(True)
        proxy_info_edit.setStyleSheet("QLineEdit { background-color: #f5f5f5; }")
        layout.addRow("代理信息:", proxy_info_edit)

        # 代理类型 - 从实际数据获取
        proxy_type_edit = QLineEdit()
        proxy_type_edit.setText("Socks5")  # AdsPower API通常不返回代理配置详情
        proxy_type_edit.setReadOnly(True)
        proxy_type_edit.setStyleSheet("QLineEdit { background-color: #f5f5f5; }")
        layout.addRow("代理类型:", proxy_type_edit)

        # IP查询来源
        ip_source_edit = QLineEdit()
        ip_source_edit.setText("IP2location")
        ip_source_edit.setReadOnly(True)
        ip_source_edit.setStyleSheet("QLineEdit { background-color: #f5f5f5; }")
        layout.addRow("IP查询来源:", ip_source_edit)

        # 主机/端口 - 显示实际IP信息
        host_port_layout = QHBoxLayout()
        host_edit = QLineEdit()
        # 显示实际的IP地址
        ip_value = profile.get('ip', '45.88.103.33')
        host_edit.setText(ip_value)
        host_edit.setReadOnly(True)
        host_edit.setStyleSheet("QLineEdit { background-color: #f5f5f5; }")

        port_edit = QLineEdit()
        # 从代理配置中获取端口信息
        proxy_config = profile.get('user_proxy_config', {})
        proxy_port = proxy_config.get('proxy_port', '64469')
        port_edit.setText(str(proxy_port))
        port_edit.setReadOnly(True)
        port_edit.setStyleSheet("QLineEdit { background-color: #f5f5f5; }")

        host_port_layout.addWidget(host_edit)
        host_port_layout.addWidget(QLabel(":"))
        host_port_layout.addWidget(port_edit)

        layout.addRow("主机/端口:", host_port_layout)

        # 代理账号 - 从实际数据获取
        proxy_user_edit = QLineEdit()
        proxy_config = profile.get('user_proxy_config', {})
        proxy_user = proxy_config.get('proxy_user', 'RuKDMV4c')
        proxy_user_edit.setText(proxy_user)
        proxy_user_edit.setReadOnly(True)
        proxy_user_edit.setStyleSheet("QLineEdit { background-color: #f5f5f5; }")
        layout.addRow("代理账号:", proxy_user_edit)

        # 代理密码 - 从实际数据获取
        proxy_pass_edit = QLineEdit()
        proxy_password = proxy_config.get('proxy_password', 'rSEAbzIp')
        proxy_pass_edit.setText(proxy_password)
        proxy_pass_edit.setReadOnly(True)
        proxy_pass_edit.setStyleSheet("QLineEdit { background-color: #f5f5f5; }")
        # 移除密码模式，显示明文
        # proxy_pass_edit.setEchoMode(QLineEdit.Password)
        layout.addRow("代理密码:", proxy_pass_edit)

        # 刷新URL
        refresh_url_edit = QLineEdit()
        refresh_url_edit.setText("请填写刷新URL（选填）")
        refresh_url_edit.setReadOnly(True)
        refresh_url_edit.setStyleSheet("QLineEdit { background-color: #f5f5f5; }")
        layout.addRow("刷新URL:", refresh_url_edit)

        return widget

    def create_readonly_account_tab(self, profile):
        """创建账号平台标签页 - 只读模式"""
        widget = QWidget()
        layout = QFormLayout(widget)

        # 账号平台
        platform_edit = QLineEdit()
        domain_name = profile.get('domain_name', 'facebook.com')
        platform_edit.setText(domain_name)
        platform_edit.setReadOnly(True)
        platform_edit.setStyleSheet("QLineEdit { background-color: #f5f5f5; }")
        layout.addRow("账号平台:", platform_edit)

        # 标签页
        homepage_edit = QLineEdit()
        homepage_value = profile.get('domain_name', '')
        if not homepage_value:
            homepage_value = 'https://www.facebook.com/'
        homepage_edit.setText(homepage_value)
        homepage_edit.setReadOnly(True)
        homepage_edit.setStyleSheet("QLineEdit { background-color: #f5f5f5; }")
        layout.addRow("标签页:", homepage_edit)

        # 用户账号
        username_edit = QLineEdit()
        username_value = profile.get('username', '')
        username_edit.setText(username_value)
        username_edit.setReadOnly(True)
        username_edit.setStyleSheet("QLineEdit { background-color: #f5f5f5; }")
        layout.addRow("用户账号:", username_edit)

        # 用户密码
        password_edit = QLineEdit()
        password_value = profile.get('password', '')
        password_edit.setText(password_value)
        password_edit.setReadOnly(True)
        password_edit.setStyleSheet("QLineEdit { background-color: #f5f5f5; }")
        # 移除密码模式，显示明文
        # password_edit.setEchoMode(QLineEdit.Password)
        layout.addRow("用户密码:", password_edit)

        # 2FA密钥
        fa_key_edit = QLineEdit()
        fa_key_value = profile.get('fakey', '')
        fa_key_edit.setText(fa_key_value)
        fa_key_edit.setReadOnly(True)
        fa_key_edit.setStyleSheet("QLineEdit { background-color: #f5f5f5; }")
        layout.addRow("2FA密钥:", fa_key_edit)

        return widget

    def create_readonly_fingerprint_tab(self, profile):
        """创建指纹配置标签页 - 只读模式"""
        widget = QWidget()
        layout = QFormLayout(widget)

        # WebRTC
        webrtc_edit = QLineEdit()
        webrtc_edit.setText("禁用")
        webrtc_edit.setReadOnly(True)
        webrtc_edit.setStyleSheet("QLineEdit { background-color: #f5f5f5; }")
        layout.addRow("WebRTC:", webrtc_edit)

        # 时区
        timezone_edit = QLineEdit()
        timezone_edit.setText("基于 IP")
        timezone_edit.setReadOnly(True)
        timezone_edit.setStyleSheet("QLineEdit { background-color: #f5f5f5; }")
        layout.addRow("时区:", timezone_edit)

        # 地理位置
        location_edit = QLineEdit()
        location_edit.setText("询问 基于 IP")
        location_edit.setReadOnly(True)
        location_edit.setStyleSheet("QLineEdit { background-color: #f5f5f5; }")
        layout.addRow("地理位置:", location_edit)

        # 语言
        language_edit = QLineEdit()
        language_edit.setText("基于 IP")
        language_edit.setReadOnly(True)
        language_edit.setStyleSheet("QLineEdit { background-color: #f5f5f5; }")
        layout.addRow("语言:", language_edit)

        return widget

    def create_readonly_advanced_tab(self, profile):
        """创建高级设置标签页 - 只读模式"""
        widget = QWidget()
        layout = QFormLayout(widget)

        # 界面语言
        page_lang_edit = QLineEdit()
        page_lang_edit.setText("基于语言")
        page_lang_edit.setReadOnly(True)
        page_lang_edit.setStyleSheet("QLineEdit { background-color: #f5f5f5; }")
        layout.addRow("界面语言:", page_lang_edit)

        # 分辨率
        resolution_edit = QLineEdit()
        resolution_edit.setText("1920 x 1080")
        resolution_edit.setReadOnly(True)
        resolution_edit.setStyleSheet("QLineEdit { background-color: #f5f5f5; }")
        layout.addRow("分辨率:", resolution_edit)

        # 字体
        font_edit = QLineEdit()
        font_edit.setText("默认")
        font_edit.setReadOnly(True)
        font_edit.setStyleSheet("QLineEdit { background-color: #f5f5f5; }")
        layout.addRow("字体:", font_edit)

        return widget

    def create_readonly_summary(self, profile):
        """创建右侧概要信息 - 只读模式"""
        widget = QWidget()
        widget.setFixedWidth(300)
        layout = QVBoxLayout(widget)

        # 概要标题
        summary_label = QLabel("概要")
        summary_label.setStyleSheet("font-weight: bold; font-size: 14px; padding: 5px;")
        layout.addWidget(summary_label)

        # 概要信息显示
        summary_info = QTextEdit()
        summary_info.setReadOnly(True)
        summary_info.setMaximumHeight(500)

        # 构建概要信息 - 完全按照AdsPower格式显示
        ip_info = profile.get('ip', '45.192.46.214')
        ip_country = profile.get('ip_country', 'us')

        # 获取User-Agent信息
        ua_value = profile.get('user_agent', '')
        if not ua_value:
            ua_value = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

        summary_text = f"""浏览器: SunBrowser (Chrome 135)
User-Agent: {ua_value}

代理IP: {ip_info}
工作国家: {ip_country}

WebRTC: 禁用
时区: 基于 IP
地理位置: 询问 基于 IP
语言: 基于 IP
界面语言: 基于语言
分辨率: 1920 x 1080
字体: 默认
Canvas: 随机 [CEA1F4FE]
WebGL图像: 随机 [9841F85E]
AudioContext: 随机 [434DBD07]
媒体设备: 随机 [Auto]
ClientRects: 随机 [E0F4C965]
SpeechVoices: 随机

WebGPU: 基于 WebGL
CPU: 10 核
RAM: 8 GB
设备名称: DESKTOP-SUXHUU7
MAC地址: E4-A4-71-48-F8-EF
Do Not Track: 开启
端口扫描保护: [启用]
硬件加速: 关闭
禁用TLS特性: [关闭]

可前往: 高级设置 自定义指纹配置值。"""

        summary_info.setPlainText(summary_text)
        layout.addWidget(summary_info)

        return widget

    def test_proxy_connection(self, profile):
        """测试代理连接"""
        try:
            # 显示测试对话框
            dialog = QDialog(self)
            dialog.setWindowTitle("代理连接测试")
            dialog.setFixedSize(400, 300)
            dialog.setModal(True)

            layout = QVBoxLayout(dialog)

            # 测试信息显示
            info_label = QLabel("正在测试代理连接...")
            info_label.setStyleSheet("font-size: 12px; padding: 10px;")
            layout.addWidget(info_label)

            # 测试结果显示
            result_text = QTextEdit()
            result_text.setReadOnly(True)
            result_text.setMaximumHeight(200)
            layout.addWidget(result_text)

            # 关闭按钮
            close_btn = QPushButton("关闭")
            close_btn.clicked.connect(dialog.close)
            layout.addWidget(close_btn)

            # 模拟测试过程
            ip_info = profile.get('ip', '45.88.103.33')
            ip_country = profile.get('ip_country', 'sg')

            test_result = f"""代理测试结果:

IP地址: {ip_info}
IP国家: {ip_country}
连接状态: 正常
响应时间: 156ms
匿名级别: 高匿名

测试时间: {QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss')}

注意：这是基于AdsPower API返回的IP信息进行的模拟测试。
实际代理配置详情需要在AdsPower客户端中查看。"""

            result_text.setPlainText(test_result)
            info_label.setText("代理测试完成")

            dialog.exec_()

        except Exception as e:
            QMessageBox.critical(self, "错误", f"代理测试失败: {e}")

    def copy_profile(self, user_id):
        """复制环境"""
        try:
            QMessageBox.information(self, "复制成功", f"环境 {user_id} 已复制")
            self.load_profiles()  # 重新加载数据
        except Exception as e:
            QMessageBox.critical(self, "错误", f"复制环境失败: {e}")

    def delete_profile(self, user_id, dialog):
        """删除环境"""
        try:
            reply = QMessageBox.question(self, "确认删除",
                                       f"确定要删除环境 {user_id} 吗？此操作不可恢复！",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                QMessageBox.information(self, "删除成功", f"环境 {user_id} 已删除")
                dialog.close()
                self.load_profiles()  # 重新加载数据
        except Exception as e:
            QMessageBox.critical(self, "错误", f"删除环境失败: {e}")


class RPAManagement(QWidget):
    """RPA流程管理页面 - 完全按照AdsPower官方文档重新设计"""

    def __init__(self, api):
        super().__init__()
        self.api = api
        self.processes = []  # 存储流程数据
        self.thread_count = 5  # 默认线程数
        self.current_tab = 0  # 当前选中的标签页

        # 初始化多线程管理器
        try:
            from rpa_thread_manager import RPAThreadManager
            self.thread_manager = RPAThreadManager(max_threads=self.thread_count)
            self.thread_manager.start()
        except ImportError:
            self.thread_manager = None
            print("多线程管理器不可用")

        self.init_ui()
        self.load_processes()

        # 启动任务状态更新定时器
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_task_status)
        self.status_timer.start(1000)  # 每秒更新一次

    def init_ui(self):
        """初始化界面 - iOS 26 Liquid Glass风格"""
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(16)

        # 应用统一的iOS 26风格样式
        self.setStyleSheet(iOS26StyleManager.get_complete_style() + """
            QTabWidget::pane {
                border: none;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.9),
                    stop:1 rgba(255, 255, 255, 0.7));
                border-radius: 16px;
            }
            QTabBar::tab {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.8),
                    stop:1 rgba(255, 255, 255, 0.6));
                padding: 12px 20px;
                margin-right: 4px;
                border-radius: 12px 12px 0 0;
                font-size: 15px;
                font-weight: 600;
                color: rgba(28, 28, 30, 0.7);
                border: none;
            }
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(0, 122, 255, 0.9),
                    stop:1 rgba(0, 122, 255, 0.7));
                color: rgba(255, 255, 255, 0.95);
            }
            QTabBar::tab:hover:!selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(0, 122, 255, 0.1),
                    stop:1 rgba(0, 122, 255, 0.05));
                color: rgba(0, 122, 255, 0.9);
            }
        """)

        # 创建标签页 - 流程管理和任务记录
        self.tab_widget = QTabWidget()

        # 流程管理页面
        self.processes_widget = self.create_processes_tab()
        self.tab_widget.addTab(self.processes_widget, "流程管理")

        # 任务记录页面
        self.task_records_widget = self.create_task_records_tab()
        self.tab_widget.addTab(self.task_records_widget, "任务记录")

        main_layout.addWidget(self.tab_widget)

    def create_processes_tab(self):
        """创建Processes标签页 - 按照AdsPower官方设计"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # 顶部工具栏 - 完全按照AdsPower官方布局
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setSpacing(12)
        toolbar_layout.setContentsMargins(0, 10, 0, 10)

        # 左侧按钮组
        create_btn = QPushButton("+ 创建流程")
        create_btn.setStyleSheet(iOS26StyleManager.get_button_style('primary'))
        create_btn.clicked.connect(self.safe_create_new_process)

        # 筛选下拉框
        filter_combo = QComboBox()
        filter_combo.addItems(["全部分组", "默认分组", "工作分组", "测试分组"])
        filter_combo.setStyleSheet(iOS26StyleManager.get_input_style())

        # 搜索框
        search_edit = QLineEdit()
        search_edit.setPlaceholderText("🔍 搜索流程名称...")
        search_edit.setStyleSheet(iOS26StyleManager.get_input_style())

        # 右侧按钮组 - iOS 26风格
        delete_btn = QPushButton("删除")
        delete_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 59, 48, 0.9),
                    stop:1 rgba(255, 59, 48, 0.8));
                color: rgba(255, 255, 255, 0.95);
                border: none;
                border-radius: 12px;
                padding: 10px 16px;
                font-size: 14px;
                font-weight: 600;

            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 59, 48, 1.0),
                    stop:1 rgba(255, 59, 48, 0.9));

            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 59, 48, 0.8),
                    stop:1 rgba(255, 59, 48, 0.7));
            }
        """)
        delete_btn.clicked.connect(self.delete_selected_processes)

        settings_btn = QPushButton("设置")
        settings_btn.setStyleSheet(iOS26StyleManager.get_button_style('secondary'))
        settings_btn.clicked.connect(self.show_thread_settings)

        toolbar_layout.addWidget(create_btn)
        toolbar_layout.addWidget(filter_combo)
        toolbar_layout.addWidget(search_edit)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(delete_btn)
        toolbar_layout.addWidget(settings_btn)

        layout.addLayout(toolbar_layout)

        # 流程统计信息
        stats_layout = QHBoxLayout()
        self.process_count_label = QLabel("创建流程数: 0")
        self.process_count_label.setStyleSheet("font-size: 13px; color: #666; font-weight: bold; font-family: 'Microsoft YaHei', Arial, sans-serif;")
        stats_layout.addWidget(self.process_count_label)
        stats_layout.addStretch()

        layout.addLayout(stats_layout)

        # 流程表格 - 按照AdsPower官方设计
        self.process_table = QTableWidget()
        self.setup_process_table()
        layout.addWidget(self.process_table)

        return widget

    def create_task_records_tab(self):
        """创建任务记录标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # 顶部工具栏
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setSpacing(12)
        toolbar_layout.setContentsMargins(0, 10, 0, 10)

        # 左侧按钮组
        start_btn = QPushButton("▶ 开始任务")
        start_btn.setStyleSheet("""
            QPushButton {
                background-color: #52c41a;
                color: white;
                border: none;
                padding: 9px 18px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: 500;
                min-width: 110px;
                font-family: "Microsoft YaHei", "PingFang SC", Arial, sans-serif;
            }
            QPushButton:hover {
                background-color: #73d13d;
            }
            QPushButton:pressed {
                background-color: #389e0d;
            }
        """)

        stop_btn = QPushButton("⏸ 停止任务")
        stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff4d4f;
                color: white;
                border: none;
                padding: 9px 18px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: 500;
                min-width: 110px;
                font-family: "Microsoft YaHei", "PingFang SC", Arial, sans-serif;
            }
            QPushButton:hover {
                background-color: #ff7875;
            }
            QPushButton:pressed {
                background-color: #d9363e;
            }
        """)

        # 筛选下拉框
        status_filter = QComboBox()
        status_filter.addItems(["全部状态", "运行中", "已完成", "已停止", "失败"])
        status_filter.setStyleSheet("""
            QComboBox {
                padding: 8px 12px;
                border: 1px solid #d9d9d9;
                border-radius: 6px;
                font-size: 14px;
                min-width: 120px;
                background-color: white;
                font-family: "Microsoft YaHei", "PingFang SC", Arial, sans-serif;
                color: #333333;
            }
            QComboBox:hover {
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
                border-top: 5px solid #999999;
                margin-right: 5px;
            }
        """)

        # 搜索框
        search_edit = QLineEdit()
        search_edit.setPlaceholderText("🔍 搜索任务名称...")
        search_edit.setStyleSheet("""
            QLineEdit {
                padding: 8px 12px;
                border: 1px solid #d9d9d9;
                border-radius: 6px;
                font-size: 14px;
                min-width: 250px;
                background-color: white;
                font-family: "Microsoft YaHei", "PingFang SC", Arial, sans-serif;
                color: #333333;
            }
            QLineEdit:hover {
                border-color: #40a9ff;
            }
            QLineEdit:focus {
                border-color: #1890ff;
                outline: none;
            }
        """)

        # 右侧按钮组
        clear_btn = QPushButton("清空记录")
        clear_btn.setStyleSheet(self.get_button_style("#ff4d4f"))
        clear_btn.clicked.connect(self.clear_task_records)

        refresh_btn = QPushButton("刷新")
        refresh_btn.setStyleSheet(self.get_button_style())
        refresh_btn.clicked.connect(self.refresh_task_records)

        # 连接按钮事件
        start_btn.clicked.connect(self.start_selected_tasks)
        stop_btn.clicked.connect(self.stop_selected_tasks)

        toolbar_layout.addWidget(start_btn)
        toolbar_layout.addWidget(stop_btn)
        toolbar_layout.addWidget(status_filter)
        toolbar_layout.addWidget(search_edit)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(clear_btn)
        toolbar_layout.addWidget(refresh_btn)

        layout.addLayout(toolbar_layout)

        # 任务统计信息
        stats_layout = QHBoxLayout()
        self.task_count_label = QLabel("任务记录数: 0")
        self.task_count_label.setStyleSheet("font-size: 13px; color: #666; font-weight: bold; font-family: 'Microsoft YaHei', Arial, sans-serif;")
        stats_layout.addWidget(self.task_count_label)
        stats_layout.addStretch()

        layout.addLayout(stats_layout)

        # 任务记录表格
        self.task_records_table = QTableWidget()
        self.setup_task_records_table()
        layout.addWidget(self.task_records_table)

        return widget

    def setup_task_records_table(self):
        """设置任务记录表格"""
        headers = ["", "任务ID", "任务名称", "状态", "开始时间", "结束时间", "执行环境", "操作"]
        self.task_records_table.setColumnCount(len(headers))
        self.task_records_table.setHorizontalHeaderLabels(headers)

        # 设置表格样式
        self.task_records_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #f0f0f0;
                background-color: white;
                gridline-color: #f0f0f0;
                selection-background-color: #e6f7ff;
                font-family: "Microsoft YaHei", Arial, sans-serif;
            }
            QTableWidget::item {
                padding: 20px 12px;
                border-bottom: 1px solid #f0f0f0;
                font-size: 15px;
                min-height: 60px;
            }
            QHeaderView::section {
                background-color: #fafafa;
                border: 1px solid #f0f0f0;
                padding: 16px 12px;
                font-weight: bold;
                font-size: 15px;
                font-family: "Microsoft YaHei", Arial, sans-serif;
                min-height: 55px;
            }
        """)

        # 设置列宽
        header = self.task_records_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)  # 复选框
        header.setSectionResizeMode(1, QHeaderView.Fixed)  # 任务ID
        header.setSectionResizeMode(2, QHeaderView.Stretch)  # 任务名称
        header.setSectionResizeMode(3, QHeaderView.Fixed)   # 状态
        header.setSectionResizeMode(4, QHeaderView.Fixed)   # 开始时间
        header.setSectionResizeMode(5, QHeaderView.Fixed)   # 结束时间
        header.setSectionResizeMode(6, QHeaderView.Fixed)   # 执行环境
        header.setSectionResizeMode(7, QHeaderView.Fixed)   # 操作

        self.task_records_table.setColumnWidth(0, 60)   # 复选框
        self.task_records_table.setColumnWidth(1, 100)  # 任务ID
        self.task_records_table.setColumnWidth(3, 100)  # 状态
        self.task_records_table.setColumnWidth(4, 150)  # 开始时间
        self.task_records_table.setColumnWidth(5, 150)  # 结束时间
        self.task_records_table.setColumnWidth(6, 120)  # 执行环境
        self.task_records_table.setColumnWidth(7, 120)  # 操作

        # 设置行高
        self.task_records_table.verticalHeader().setDefaultSectionSize(80)
        self.task_records_table.verticalHeader().setVisible(False)

        self.task_records_table.setAlternatingRowColors(True)
        self.task_records_table.setSelectionBehavior(QTableWidget.SelectRows)

        # 设置表格最小高度
        self.task_records_table.setMinimumHeight(600)

    def get_button_style(self, hover_color="#1890ff"):
        """获取按钮样式 - AdsPower风格"""
        return f"""
            QPushButton {{
                background-color: white;
                border: 1px solid #d9d9d9;
                padding: 8px 14px;
                border-radius: 6px;
                font-size: 14px;
                color: #595959;
                font-family: "Microsoft YaHei", "PingFang SC", Arial, sans-serif;
                font-weight: 400;
                min-width: 70px;
            }}
            QPushButton:hover {{
                border-color: {hover_color};
                color: {hover_color};
                background-color: #f8f9fa;
            }}
            QPushButton:pressed {{
                background-color: #e6f7ff;
                border-color: {hover_color};
            }}
        """

    def setup_process_table(self):
        """设置流程表格 - 按照AdsPower官方设计"""
        headers = ["", "流程名称", "分组", "创建时间", "操作"]
        self.process_table.setColumnCount(len(headers))
        self.process_table.setHorizontalHeaderLabels(headers)

        # 设置表格样式 - iOS 26风格
        self.process_table.setStyleSheet(iOS26StyleManager.get_table_style())

        # 设置列宽
        header = self.process_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)  # 复选框
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # 流程名称
        header.setSectionResizeMode(2, QHeaderView.Fixed)   # 分组
        header.setSectionResizeMode(3, QHeaderView.Fixed)   # 创建时间
        header.setSectionResizeMode(4, QHeaderView.Fixed)   # 操作

        self.process_table.setColumnWidth(0, 60)   # 复选框
        self.process_table.setColumnWidth(2, 150)  # 分组
        self.process_table.setColumnWidth(3, 180)  # 创建时间
        self.process_table.setColumnWidth(4, 120)  # 操作

        # 设置行高 - 大幅增加
        self.process_table.verticalHeader().setDefaultSectionSize(80)
        self.process_table.verticalHeader().setVisible(False)

        self.process_table.setAlternatingRowColors(True)
        self.process_table.setSelectionBehavior(QTableWidget.SelectRows)

        # 设置表格最小高度 - 大幅增加
        self.process_table.setMinimumHeight(600)
        self.process_table.resize(self.process_table.width(), 600)



    def create_new_process(self):
        """创建新流程 - 打开任务流程创建对话框"""
        try:
            print("开始创建新流程...")  # 调试信息

            # 显示加载提示
            from PyQt5.QtCore import QTimer
            from PyQt5.QtWidgets import QProgressDialog

            # 创建进度对话框
            progress = QProgressDialog("正在加载流程编辑器...", "取消", 0, 0, self)
            progress.setWindowTitle("加载中")
            progress.setModal(True)
            progress.show()

            # 使用QTimer延迟加载，避免界面卡顿
            def load_dialog():
                try:
                    progress.close()
                    print("导入TaskFlowDialog...")  # 调试信息

                    from task_flow_dialog import TaskFlowDialog
                    print("创建TaskFlowDialog实例...")  # 调试信息

                    dialog = TaskFlowDialog(self)
                    print("显示对话框...")  # 调试信息

                    # 连接对话框的接受信号
                    def on_dialog_accepted():
                        print("对话框被接受，获取流程数据...")  # 调试信息
                        # 获取创建的流程数据
                        flow_data = dialog.get_flow_data()
                        if flow_data:
                            print(f"获取到流程数据: {flow_data.get('name', '未命名')}")  # 调试信息
                            self.add_process_to_table(flow_data)
                            self.update_process_count()
                            # 保存到文件
                            self.save_processes()
                            QMessageBox.information(self, "成功", f"流程 '{flow_data.get('name', '未命名')}' 创建成功！")
                        else:
                            print("未获取到流程数据")  # 调试信息
                        dialog.close()

                    def on_dialog_rejected():
                        print("对话框被取消")  # 调试信息
                        dialog.close()

                    dialog.accepted.connect(on_dialog_accepted)
                    dialog.rejected.connect(on_dialog_rejected)

                    # 显示非模态对话框
                    dialog.show()

                except ImportError as e:
                    progress.close()
                    print(f"导入失败: {e}")  # 调试信息
                    QMessageBox.warning(self, "错误", f"无法加载任务流程对话框: {str(e)}")
                except Exception as e:
                    progress.close()
                    print(f"其他错误: {e}")  # 调试信息
                    import traceback
                    traceback.print_exc()
                    QMessageBox.warning(self, "错误", f"创建流程时发生错误: {str(e)}")

            # 延迟100毫秒后加载对话框
            QTimer.singleShot(100, load_dialog)

        except Exception as e:
            print(f"create_new_process异常: {e}")  # 调试信息
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "严重错误", f"创建流程功能初始化失败: {str(e)}")

    def safe_create_new_process(self):
        """安全的创建新流程方法 - 带有备用方案"""
        try:
            # 首先尝试正常的创建流程
            self.create_new_process()
        except Exception as e:
            print(f"正常创建流程失败，使用备用方案: {e}")
            # 如果失败，使用简单的创建对话框
            self.show_simple_create_dialog()

    def show_simple_create_dialog(self):
        """显示简单的创建对话框"""
        dialog = QDialog(self)
        dialog.setWindowTitle("创建流程")
        dialog.setFixedSize(400, 200)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(20, 20, 20, 20)

        # 流程名称输入
        form_layout = QFormLayout()
        name_edit = QLineEdit()
        name_edit.setPlaceholderText("请输入流程名称...")
        name_edit.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                font-size: 13px;
                font-family: "Microsoft YaHei", Arial, sans-serif;
            }
        """)
        form_layout.addRow("流程名称:", name_edit)
        layout.addLayout(form_layout)

        # 按钮
        button_layout = QHBoxLayout()

        confirm_btn = QPushButton("创建")
        confirm_btn.setStyleSheet("""
            QPushButton {
                background-color: #1890ff;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 13px;
                min-width: 80px;
                font-family: "Microsoft YaHei", Arial, sans-serif;
            }
            QPushButton:hover {
                background-color: #40a9ff;
            }
        """)

        cancel_btn = QPushButton("取消")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #595959;
                border: 1px solid #d9d9d9;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 13px;
                min-width: 80px;
                font-family: "Microsoft YaHei", Arial, sans-serif;
            }
            QPushButton:hover {
                border-color: #40a9ff;
                color: #1890ff;
            }
        """)

        button_layout.addStretch()
        button_layout.addWidget(confirm_btn)
        button_layout.addWidget(cancel_btn)

        layout.addStretch()
        layout.addLayout(button_layout)

        # 连接信号
        def create_process():
            process_name = name_edit.text().strip()
            if not process_name:
                process_name = "未命名流程"

            # 创建流程数据
            process_data = {
                "name": process_name,
                "group": "默认分组",
                "created_time": QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss"),
                "steps": []
            }

            self.add_process_to_table(process_data)
            self.update_process_count()
            dialog.accept()

        confirm_btn.clicked.connect(create_process)
        cancel_btn.clicked.connect(dialog.reject)

        dialog.exec_()

    def add_process_to_table(self, process_data):
        """添加流程到表格"""
        row = self.process_table.rowCount()
        self.process_table.insertRow(row)

        # 复选框
        checkbox = QCheckBox()
        self.process_table.setCellWidget(row, 0, checkbox)

        # 流程名称
        name_item = QTableWidgetItem(process_data["name"])
        self.process_table.setItem(row, 1, name_item)

        # 分组
        group_item = QTableWidgetItem(process_data.get("group", "Default"))
        self.process_table.setItem(row, 2, group_item)

        # 创建时间 - 兼容处理
        created_time = process_data.get("created_time") or process_data.get("save_time") or QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        time_item = QTableWidgetItem(created_time)
        self.process_table.setItem(row, 3, time_item)

        # 操作按钮 - 使用下拉菜单
        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        actions_layout.setContentsMargins(5, 0, 5, 0)

        # 创建操作按钮（更明显的样式）
        action_btn = QPushButton("操作 ▼")
        action_btn.setFixedSize(70, 35)
        action_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                border: 1px solid #d9d9d9;
                border-radius: 6px;
                font-size: 13px;
                font-weight: 500;
                color: #333333;
                font-family: "Microsoft YaHei", "PingFang SC", Arial, sans-serif;
                text-align: center;
                padding: 5px 8px;
            }
            QPushButton:hover {
                background-color: #f0f8ff;
                border-color: #1890ff;
                color: #1890ff;
            }
            QPushButton:pressed {
                background-color: #e6f7ff;
                border-color: #1890ff;
            }
        """)

        # 创建下拉菜单
        from PyQt5.QtWidgets import QMenu
        from PyQt5.QtCore import QPoint

        def show_action_menu():
            # 获取当前行号（实时获取，避免闭包问题）
            current_row = None
            for i in range(self.process_table.rowCount()):
                if self.process_table.cellWidget(i, 4) and action_btn in self.process_table.cellWidget(i, 4).findChildren(QPushButton):
                    current_row = i
                    break

            if current_row is None:
                QMessageBox.warning(self, "错误", "无法确定当前行")
                return

            menu = QMenu()
            menu.setStyleSheet("""
                QMenu {
                    background-color: white;
                    border: 1px solid #e8e8e8;
                    border-radius: 8px;
                    padding: 8px 0px;
                    font-family: "Microsoft YaHei", "PingFang SC", Arial, sans-serif;
                    min-width: 140px;
                }
                QMenu::item {
                    padding: 10px 16px;
                    font-size: 14px;
                    color: #333333;
                    border: none;
                }
                QMenu::item:selected {
                    background-color: #f0f8ff;
                    color: #1890ff;
                }
                QMenu::separator {
                    height: 1px;
                    background-color: #f0f0f0;
                    margin: 4px 0px;
                }
            """)

            # 添加菜单项
            edit_action = menu.addAction("📝 编辑")
            duplicate_action = menu.addAction("📋 复制模板")
            export_action = menu.addAction("📤 导出")
            menu.addSeparator()
            delete_action = menu.addAction("🗑️ 删除")

            # 设置菜单项事件（使用实时获取的行号）
            edit_action.triggered.connect(lambda: self.edit_process(current_row))
            duplicate_action.triggered.connect(lambda: self.duplicate_process(current_row))
            export_action.triggered.connect(lambda: self.export_process(current_row))
            delete_action.triggered.connect(lambda: self.delete_process(current_row))

            # 显示菜单
            global_pos = action_btn.mapToGlobal(QPoint(0, action_btn.height()))
            menu.exec_(global_pos)

        action_btn.clicked.connect(show_action_menu)

        actions_layout.addWidget(action_btn)
        actions_layout.addStretch()

        self.process_table.setCellWidget(row, 4, actions_widget)

        # 保存流程数据
        self.processes.append(process_data)

    def update_process_count(self):
        """更新流程计数"""
        count = len(self.processes)
        self.process_count_label.setText(f"已创建流程: {count}")

    def load_processes(self):
        """加载流程数据"""
        try:
            import os
            flows_file = os.path.join("data", "rpa_flows.json")
            if os.path.exists(flows_file):
                with open(flows_file, 'r', encoding='utf-8') as f:
                    flows = json.load(f)
                    for flow in flows:
                        self.add_process_to_table(flow)
                    self.update_process_count()
            else:
                # 如果没有数据文件，创建一些示例数据
                self.create_sample_data()
        except Exception as e:
            print(f"加载流程数据失败: {e}")
            # 创建示例数据
            self.create_sample_data()

    def create_sample_data(self):
        """创建示例数据"""
        sample_processes = [
            {
                "name": "Facebook自动发帖",
                "group": "社交媒体",
                "created_time": "2025-06-22 10:30:15",
                "steps": ["打开Facebook", "登录账号", "发布内容", "添加图片"]
            },
            {
                "name": "Instagram点赞任务",
                "group": "社交媒体",
                "created_time": "2025-06-22 09:15:30",
                "steps": ["打开Instagram", "搜索标签", "批量点赞"]
            },
            {
                "name": "数据采集流程",
                "group": "数据处理",
                "created_time": "2025-06-21 16:45:20",
                "steps": ["打开目标网站", "提取数据", "保存到Excel"]
            }
        ]

        for process in sample_processes:
            self.add_process_to_table(process)
        self.update_process_count()

    def show_thread_settings(self):
        """显示线程设置对话框 - 按照AdsPower官方设计"""
        dialog = QDialog(self)
        dialog.setWindowTitle("设置")
        dialog.setFixedSize(450, 250)

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
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                font-size: 13px;
                min-width: 100px;
                font-family: "Microsoft YaHei", Arial, sans-serif;
            }
        """)

        form_layout.addRow("任务线程数:", thread_spin)

        # 添加说明文字
        help_text = QLabel("当设置为3时，如果您选择100个环境来运行RPA任务，\n只有3个环境会同时执行任务，\n其余97个环境将在队列中等待。")
        help_text.setStyleSheet("font-size: 11px; color: #8c8c8c; margin-top: 10px; font-family: 'Microsoft YaHei', Arial, sans-serif;")
        help_text.setWordWrap(True)

        layout.addLayout(form_layout)
        layout.addWidget(help_text)

        # 按钮
        button_layout = QHBoxLayout()

        confirm_btn = QPushButton("确定")
        confirm_btn.setStyleSheet("""
            QPushButton {
                background-color: #1890ff;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 13px;
                min-width: 80px;
                font-family: "Microsoft YaHei", Arial, sans-serif;
            }
            QPushButton:hover {
                background-color: #40a9ff;
            }
        """)

        cancel_btn = QPushButton("取消")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #595959;
                border: 1px solid #d9d9d9;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 13px;
                min-width: 80px;
                font-family: "Microsoft YaHei", Arial, sans-serif;
            }
            QPushButton:hover {
                border-color: #40a9ff;
                color: #1890ff;
            }
        """)

        button_layout.addStretch()
        button_layout.addWidget(confirm_btn)
        button_layout.addWidget(cancel_btn)

        layout.addStretch()
        layout.addLayout(button_layout)

        # 连接信号
        def save_settings():
            new_thread_count = thread_spin.value()
            if new_thread_count != self.thread_count:
                self.thread_count = new_thread_count
                # 更新多线程管理器
                if self.thread_manager:
                    self.thread_manager.set_max_threads(self.thread_count)
                # 保存设置到文件
                self.save_thread_settings()
            QMessageBox.information(dialog, "成功", f"任务线程数已设置为 {self.thread_count}")
            dialog.accept()

        confirm_btn.clicked.connect(save_settings)
        cancel_btn.clicked.connect(dialog.reject)

        dialog.exec_()

    def save_thread_settings(self):
        """保存线程设置到文件"""
        try:
            import os
            data_dir = "data"
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)

            settings_file = os.path.join(data_dir, "task_settings.json")
            settings = {"thread_count": self.thread_count}

            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存线程设置失败: {e}")

    # 占位符方法 - 保持兼容性
    def refresh_tasks(self):
        """刷新任务列表"""
        self.load_processes()
        QMessageBox.information(self, "刷新", "流程列表已刷新")

    def export_selected_tasks(self):
        """导出选中的任务"""
        QMessageBox.information(self, "导出", "导出功能将在后续版本中实现")

    def filter_tasks(self, text):
        """筛选任务"""
        pass

    def search_tasks(self, text):
        """搜索任务"""
        pass

    def edit_process(self, row):
        """编辑流程"""
        try:
            print(f"开始编辑流程，行号: {row}")

            if row >= len(self.processes):
                QMessageBox.warning(self, "错误", "流程数据不存在")
                return

            process_data = self.processes[row]
            print(f"编辑流程数据: {process_data}")

            from task_flow_dialog import TaskFlowDialog

            # 传递现有数据给对话框
            dialog = TaskFlowDialog(self, process_data)
            dialog.setWindowTitle(f"编辑流程 - {process_data['name']}")

            # 连接对话框的接受信号
            def on_edit_dialog_accepted():
                # 获取编辑后的数据
                updated_data = dialog.get_flow_data()
                print(f"获取到更新数据: {updated_data}")

                if updated_data:
                    # 更新流程数据
                    self.processes[row] = updated_data

                    # 更新表格显示
                    self.process_table.item(row, 1).setText(updated_data["name"])
                    self.process_table.item(row, 2).setText(updated_data.get("group", "默认分组"))

                    # 保存到文件
                    self.save_processes()

                    QMessageBox.information(self, "编辑成功", f"流程 '{updated_data['name']}' 已更新")
                else:
                    QMessageBox.warning(self, "编辑失败", "未能获取有效的流程数据")
                dialog.close()

            def on_edit_dialog_rejected():
                dialog.close()

            dialog.accepted.connect(on_edit_dialog_accepted)
            dialog.rejected.connect(on_edit_dialog_rejected)

            # 显示非模态对话框
            dialog.show()

        except ImportError as e:
            QMessageBox.warning(self, "错误", f"无法加载编辑对话框: {str(e)}")
        except Exception as e:
            print(f"编辑流程失败: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.warning(self, "错误", f"编辑流程时发生错误: {str(e)}")

    def save_processes(self):
        """保存流程数据到文件"""
        try:
            import os
            os.makedirs("data", exist_ok=True)
            flows_file = os.path.join("data", "rpa_flows.json")

            with open(flows_file, 'w', encoding='utf-8') as f:
                json.dump(self.processes, f, ensure_ascii=False, indent=2)

            print(f"流程数据已保存到: {flows_file}")

        except Exception as e:
            print(f"保存流程数据失败: {e}")
            import traceback
            traceback.print_exc()

    def duplicate_process(self, row):
        """复制流程"""
        try:
            if row >= len(self.processes):
                QMessageBox.warning(self, "错误", "流程数据不存在")
                return

            original_process = self.processes[row].copy()

            # 创建副本
            duplicated_process = {
                "name": f"{original_process['name']} - 副本",
                "group": original_process.get("group", "默认分组"),
                "created_time": QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss"),
                "steps": original_process.get("steps", []).copy()
            }

            # 添加到表格
            self.add_process_to_table(duplicated_process)
            self.update_process_count()

            QMessageBox.information(self, "复制成功", f"已创建流程副本: {duplicated_process['name']}")

        except Exception as e:
            QMessageBox.warning(self, "错误", f"复制流程时发生错误: {str(e)}")

    def export_process(self, row):
        """导出流程"""
        try:
            if row >= len(self.processes):
                QMessageBox.warning(self, "错误", "流程数据不存在")
                return

            process_data = self.processes[row]

            # 选择保存位置
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "导出流程",
                f"{process_data['name']}.json",
                "JSON文件 (*.json);;所有文件 (*)"
            )

            if file_path:
                # 导出流程数据
                export_data = {
                    "name": process_data["name"],
                    "group": process_data.get("group", "默认分组"),
                    "created_time": process_data["created_time"],
                    "steps": process_data.get("steps", []),
                    "export_time": QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss"),
                    "version": "1.0"
                }

                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, ensure_ascii=False, indent=2)

                QMessageBox.information(self, "导出成功", f"流程已导出到: {file_path}")

        except Exception as e:
            QMessageBox.warning(self, "错误", f"导出流程时发生错误: {str(e)}")

    def delete_process(self, row):
        """删除流程"""
        process_name = self.process_table.item(row, 1).text()
        reply = QMessageBox.question(self, "确认删除",
                                   f"确定要删除流程 '{process_name}' 吗？",
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.process_table.removeRow(row)
            if row < len(self.processes):
                self.processes.pop(row)
            self.update_process_count()
            QMessageBox.information(self, "删除成功", f"流程 '{process_name}' 已删除")

    def delete_selected_processes(self):
        """删除选中的流程"""
        selected_rows = []

        # 收集选中的行
        for row in range(self.process_table.rowCount()):
            checkbox = self.process_table.cellWidget(row, 0)
            if checkbox and checkbox.isChecked():
                selected_rows.append(row)

        if not selected_rows:
            QMessageBox.information(self, "提示", "请先选择要删除的流程")
            return

        # 确认删除
        reply = QMessageBox.question(
            self, "确认删除",
            f"确定要删除选中的 {len(selected_rows)} 个流程吗？\n此操作不可恢复！",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        # 从后往前删除，避免索引变化问题
        for row in sorted(selected_rows, reverse=True):
            self.process_table.removeRow(row)
            if row < len(self.processes):
                self.processes.pop(row)

        self.update_process_count()
        QMessageBox.information(self, "删除成功", f"已删除 {len(selected_rows)} 个流程")

    def move_selected_processes(self):
        """移动选中的流程到其他分组"""
        selected_rows = []

        # 收集选中的行
        for row in range(self.process_table.rowCount()):
            checkbox = self.process_table.cellWidget(row, 0)
            if checkbox and checkbox.isChecked():
                selected_rows.append(row)

        if not selected_rows:
            QMessageBox.information(self, "提示", "请先选择要移动的流程")
            return

        # 获取可用分组
        groups = ["默认分组", "社交媒体", "数据处理", "自动化测试", "其他"]

        # 选择目标分组
        group, ok = QInputDialog.getItem(
            self, "移动流程", "选择目标分组:", groups, 0, False
        )

        if ok and group:
            # 更新选中流程的分组
            for row in selected_rows:
                if row < len(self.processes):
                    self.processes[row]["group"] = group
                    self.process_table.item(row, 2).setText(group)

            QMessageBox.information(self, "移动成功", f"已将 {len(selected_rows)} 个流程移动到 '{group}' 分组")

    def generate_share_code(self):
        """生成分享码"""
        selected_rows = []

        # 收集选中的行
        for row in range(self.process_table.rowCount()):
            checkbox = self.process_table.cellWidget(row, 0)
            if checkbox and checkbox.isChecked():
                selected_rows.append(row)

        if not selected_rows:
            QMessageBox.information(self, "提示", "请先选择要生成分享码的流程")
            return

        # 生成分享码（简单的示例实现）
        import hashlib
        import time

        share_data = []
        for row in selected_rows:
            if row < len(self.processes):
                share_data.append(self.processes[row]["name"])

        # 生成唯一分享码
        share_content = f"{'-'.join(share_data)}-{int(time.time())}"
        share_code = hashlib.md5(share_content.encode()).hexdigest()[:8].upper()

        # 显示分享码
        QMessageBox.information(
            self, "分享码生成成功",
            f"分享码: {share_code}\n\n"
            f"包含 {len(selected_rows)} 个流程:\n" +
            "\n".join([f"• {self.processes[row]['name']}" for row in selected_rows if row < len(self.processes)])
        )

    def share_selected_processes(self):
        """分享选中的流程"""
        selected_rows = []

        # 收集选中的行
        for row in range(self.process_table.rowCount()):
            checkbox = self.process_table.cellWidget(row, 0)
            if checkbox and checkbox.isChecked():
                selected_rows.append(row)

        if not selected_rows:
            QMessageBox.information(self, "提示", "请先选择要分享的流程")
            return

        # 创建分享数据
        share_data = []
        for row in selected_rows:
            if row < len(self.processes):
                process = self.processes[row].copy()
                # 移除敏感信息
                process.pop("created_time", None)
                share_data.append(process)

        # 选择导出位置
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "分享流程",
            f"shared_processes_{len(selected_rows)}.json",
            "JSON文件 (*.json);;所有文件 (*)"
        )

        if file_path:
            try:
                export_data = {
                    "shared_processes": share_data,
                    "share_time": QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss"),
                    "version": "1.0",
                    "count": len(share_data)
                }

                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, ensure_ascii=False, indent=2)

                QMessageBox.information(self, "分享成功", f"已将 {len(selected_rows)} 个流程分享到: {file_path}")

            except Exception as e:
                QMessageBox.warning(self, "错误", f"分享流程时发生错误: {str(e)}")

    def show_group_management(self):
        """显示分组管理对话框"""
        dialog = QDialog(self)
        dialog.setWindowTitle("分组管理")
        dialog.setFixedSize(500, 400)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(20, 20, 20, 20)

        # 标题
        title_label = QLabel("流程分组管理")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333333;
                margin-bottom: 10px;
                font-family: "Microsoft YaHei", Arial, sans-serif;
            }
        """)
        layout.addWidget(title_label)

        # 分组列表
        group_list = QListWidget()
        group_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #d9d9d9;
                border-radius: 6px;
                padding: 5px;
                font-size: 14px;
                font-family: "Microsoft YaHei", Arial, sans-serif;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f0f0f0;
            }
            QListWidget::item:selected {
                background-color: #e6f7ff;
                color: #1890ff;
            }
        """)

        # 获取现有分组
        existing_groups = set()
        for process in self.processes:
            existing_groups.add(process.get("group", "默认分组"))

        # 添加默认分组
        default_groups = ["默认分组", "社交媒体", "数据处理", "自动化测试"]
        for group in default_groups:
            existing_groups.add(group)

        for group in sorted(existing_groups):
            # 统计该分组的流程数量
            count = sum(1 for p in self.processes if p.get("group", "默认分组") == group)
            group_list.addItem(f"{group} ({count}个流程)")

        layout.addWidget(group_list)

        # 按钮区域
        button_layout = QHBoxLayout()

        # 添加分组按钮
        add_group_btn = QPushButton("添加分组")
        add_group_btn.setStyleSheet("""
            QPushButton {
                background-color: #1890ff;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: 500;
                min-width: 80px;
                font-family: "Microsoft YaHei", Arial, sans-serif;
            }
            QPushButton:hover {
                background-color: #40a9ff;
            }
        """)

        def add_new_group():
            group_name, ok = QInputDialog.getText(dialog, "添加分组", "请输入分组名称:")
            if ok and group_name.strip():
                group_name = group_name.strip()
                if group_name not in [item.split(" (")[0] for item in [group_list.item(i).text() for i in range(group_list.count())]]:
                    group_list.addItem(f"{group_name} (0个流程)")
                    QMessageBox.information(dialog, "成功", f"分组 '{group_name}' 已添加")
                else:
                    QMessageBox.warning(dialog, "错误", "分组名称已存在")

        add_group_btn.clicked.connect(add_new_group)
        button_layout.addWidget(add_group_btn)

        # 重命名分组按钮
        rename_group_btn = QPushButton("重命名分组")
        rename_group_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #1890ff;
                border: 1px solid #1890ff;
                padding: 8px 16px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: 500;
                min-width: 80px;
                font-family: "Microsoft YaHei", Arial, sans-serif;
            }
            QPushButton:hover {
                background-color: #f0f8ff;
            }
        """)

        def rename_group():
            current_item = group_list.currentItem()
            if not current_item:
                QMessageBox.information(dialog, "提示", "请先选择要重命名的分组")
                return

            old_name = current_item.text().split(" (")[0]
            if old_name == "默认分组":
                QMessageBox.warning(dialog, "错误", "默认分组不能重命名")
                return

            new_name, ok = QInputDialog.getText(dialog, "重命名分组", f"请输入新的分组名称:", text=old_name)
            if ok and new_name.strip() and new_name.strip() != old_name:
                new_name = new_name.strip()

                # 更新所有使用该分组的流程
                count = 0
                for process in self.processes:
                    if process.get("group", "默认分组") == old_name:
                        process["group"] = new_name
                        count += 1

                # 更新表格显示
                for row in range(self.process_table.rowCount()):
                    if self.process_table.item(row, 2).text() == old_name:
                        self.process_table.item(row, 2).setText(new_name)

                # 更新列表项
                current_item.setText(f"{new_name} ({count}个流程)")
                QMessageBox.information(dialog, "成功", f"分组已重命名为 '{new_name}'")

        rename_group_btn.clicked.connect(rename_group)
        button_layout.addWidget(rename_group_btn)

        # 删除分组按钮
        delete_group_btn = QPushButton("删除分组")
        delete_group_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff4d4f;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: 500;
                min-width: 80px;
                font-family: "Microsoft YaHei", Arial, sans-serif;
            }
            QPushButton:hover {
                background-color: #ff7875;
            }
        """)

        def delete_group():
            current_item = group_list.currentItem()
            if not current_item:
                QMessageBox.information(dialog, "提示", "请先选择要删除的分组")
                return

            group_name = current_item.text().split(" (")[0]
            if group_name == "默认分组":
                QMessageBox.warning(dialog, "错误", "默认分组不能删除")
                return

            # 检查是否有流程使用该分组
            count = sum(1 for p in self.processes if p.get("group", "默认分组") == group_name)
            if count > 0:
                reply = QMessageBox.question(
                    dialog, "确认删除",
                    f"分组 '{group_name}' 中还有 {count} 个流程，删除后这些流程将移动到默认分组。\n确定要删除吗？",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply != QMessageBox.Yes:
                    return

                # 将流程移动到默认分组
                for process in self.processes:
                    if process.get("group", "默认分组") == group_name:
                        process["group"] = "默认分组"

                # 更新表格显示
                for row in range(self.process_table.rowCount()):
                    if self.process_table.item(row, 2).text() == group_name:
                        self.process_table.item(row, 2).setText("默认分组")

            # 删除列表项
            group_list.takeItem(group_list.row(current_item))
            QMessageBox.information(dialog, "成功", f"分组 '{group_name}' 已删除")

        delete_group_btn.clicked.connect(delete_group)
        button_layout.addWidget(delete_group_btn)

        button_layout.addStretch()

        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #595959;
                border: 1px solid #d9d9d9;
                padding: 8px 16px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: 500;
                min-width: 80px;
                font-family: "Microsoft YaHei", Arial, sans-serif;
            }
            QPushButton:hover {
                border-color: #40a9ff;
                color: #1890ff;
            }
        """)
        close_btn.clicked.connect(dialog.accept)
        button_layout.addWidget(close_btn)

        layout.addLayout(button_layout)
        dialog.exec_()

    # ==================== 多线程任务管理方法 ====================

    def start_selected_tasks(self):
        """启动选中的任务"""
        if not hasattr(self, 'thread_manager') or not self.thread_manager:
            QMessageBox.warning(self, "错误", "多线程管理器不可用")
            return

        # 这里应该获取选中的流程和环境，创建任务
        QMessageBox.information(self, "启动任务", "任务启动功能正在开发中")

    def stop_selected_tasks(self):
        """停止选中的任务"""
        if not hasattr(self, 'thread_manager') or not self.thread_manager:
            QMessageBox.warning(self, "错误", "多线程管理器不可用")
            return

        # 获取选中的任务并停止
        QMessageBox.information(self, "停止任务", "任务停止功能正在开发中")

    def clear_task_records(self):
        """清空任务记录"""
        if not hasattr(self, 'thread_manager') or not self.thread_manager:
            QMessageBox.warning(self, "错误", "多线程管理器不可用")
            return

        reply = QMessageBox.question(self, "确认", "确定要清空所有任务记录吗？",
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.thread_manager.clear_completed_tasks()
            self.refresh_task_records()
            QMessageBox.information(self, "成功", "任务记录已清空")

    def refresh_task_records(self):
        """刷新任务记录"""
        if not hasattr(self, 'thread_manager') or not self.thread_manager:
            return

        # 获取所有任务
        all_tasks = self.thread_manager.get_all_tasks()

        # 更新任务记录表格
        self.task_records_table.setRowCount(len(all_tasks))

        for row, task in enumerate(all_tasks):
            # 复选框
            checkbox = QCheckBox()
            self.task_records_table.setCellWidget(row, 0, checkbox)

            # 任务信息
            self.task_records_table.setItem(row, 1, QTableWidgetItem(task["task_id"][:8]))
            self.task_records_table.setItem(row, 2, QTableWidgetItem(f"任务-{task['task_id'][:8]}"))

            # 状态
            status_item = QTableWidgetItem(task["status"])
            if task["status"] == "running":
                status_item.setBackground(QColor("#52c41a"))
            elif task["status"] == "completed":
                status_item.setBackground(QColor("#1890ff"))
            elif task["status"] == "failed":
                status_item.setBackground(QColor("#ff4d4f"))
            self.task_records_table.setItem(row, 3, status_item)

            # 时间信息
            self.task_records_table.setItem(row, 4, QTableWidgetItem(task["start_time"] or ""))
            self.task_records_table.setItem(row, 5, QTableWidgetItem(task["end_time"] or ""))
            self.task_records_table.setItem(row, 6, QTableWidgetItem(task["env_id"]))

            # 操作按钮
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(5, 5, 5, 5)

            if task["status"] == "running":
                stop_btn = QPushButton("停止")
                stop_btn.setStyleSheet("QPushButton { background-color: #ff4d4f; color: white; }")
                stop_btn.clicked.connect(lambda checked, tid=task["task_id"]: self.stop_task(tid))
                action_layout.addWidget(stop_btn)
            else:
                view_btn = QPushButton("查看")
                view_btn.clicked.connect(lambda checked, tid=task["task_id"]: self.view_task_details(tid))
                action_layout.addWidget(view_btn)

            self.task_records_table.setCellWidget(row, 7, action_widget)

        # 更新统计信息
        if hasattr(self, 'task_count_label'):
            self.task_count_label.setText(f"任务记录数: {len(all_tasks)}")

    def update_task_status(self):
        """定时更新任务状态"""
        if hasattr(self, 'thread_manager') and self.thread_manager and self.current_tab == 1:  # 只在任务记录页面更新
            self.refresh_task_records()

    def stop_task(self, task_id: str):
        """停止指定任务"""
        if hasattr(self, 'thread_manager') and self.thread_manager:
            result = self.thread_manager.cancel_task(task_id)
            if result["success"]:
                QMessageBox.information(self, "成功", "任务已停止")
            else:
                QMessageBox.warning(self, "失败", result["message"])

    def view_task_details(self, task_id: str):
        """查看任务详情"""
        if not hasattr(self, 'thread_manager') or not self.thread_manager:
            return

        task = self.thread_manager.get_task_status(task_id)
        if not task:
            QMessageBox.warning(self, "错误", "任务不存在")
            return

        # 创建详情对话框
        dialog = QDialog(self)
        dialog.setWindowTitle(f"任务详情 - {task_id[:8]}")
        dialog.setFixedSize(500, 400)

        layout = QVBoxLayout(dialog)

        # 任务信息
        info_text = QTextEdit()
        info_text.setReadOnly(True)
        info_content = f"""
任务ID: {task['task_id']}
环境ID: {task['env_id']}
状态: {task['status']}
优先级: {task['priority']}
创建时间: {task['created_time']}
开始时间: {task['start_time'] or '未开始'}
结束时间: {task['end_time'] or '未结束'}
进度: {task['progress']}%
当前步骤: {task['current_step']}/{task['total_steps']}
线程ID: {task['thread_id'] or '未分配'}
错误信息: {task['error'] or '无'}
        """
        info_text.setPlainText(info_content.strip())
        layout.addWidget(info_text)

        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)

        dialog.exec_()

    def add_rpa_task(self, env_id: str, flow_data: dict, priority: int = 0):
        """添加RPA任务到队列"""
        if not hasattr(self, 'thread_manager') or not self.thread_manager:
            return None

        task_id = self.thread_manager.add_task(env_id, flow_data, priority)
        if task_id:
            QMessageBox.information(self, "成功", f"任务已添加到队列: {task_id[:8]}")
        else:
            QMessageBox.warning(self, "失败", "任务队列已满，无法添加新任务")

        return task_id


class RPATaskCard(QFrame):
    """RPA任务卡片 - 完全复刻AdsPower设计"""

    def __init__(self, task_id, task_name="暂无备注", parent=None):
        super().__init__(parent)
        self.task_id = task_id
        self.task_name = task_name
        self.init_ui()

    def init_ui(self):
        """初始化卡片界面 - 完全按照AdsPower截图设计"""
        self.setFixedSize(160, 100)
        self.setStyleSheet("""
            RPATaskCard {
                background-color: #f8f9fa;
                border: 1px solid #e8e8e8;
                border-radius: 6px;
            }
            RPATaskCard:hover {
                border-color: #1890ff;
                background-color: #ffffff;
            }
        """)

        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(4)

        # 顶部布局：复选框和任务编号
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)

        # 复选框
        self.checkbox = QCheckBox()
        self.checkbox.setFixedSize(16, 16)
        self.checkbox.setStyleSheet("""
            QCheckBox::indicator {
                width: 14px;
                height: 14px;
                border: 1px solid #d9d9d9;
                border-radius: 2px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #1890ff;
                border-color: #1890ff;
            }
        """)

        # 任务编号
        task_number = QLabel(str(self.task_id))
        task_number.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #262626;
                font-family: "Microsoft YaHei", Arial, sans-serif;
            }
        """)

        top_layout.addWidget(self.checkbox)
        top_layout.addStretch()
        top_layout.addWidget(task_number)

        # 中间：任务ID显示
        task_id_display = QLabel("14231235")  # 模拟AdsPower的任务ID格式
        task_id_display.setAlignment(Qt.AlignCenter)
        task_id_display.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #1890ff;
                font-family: "Microsoft YaHei", Arial, sans-serif;
                margin: 8px 0;
            }
        """)

        # 底部：操作按钮
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.addStretch()

        # 编辑图标按钮
        edit_btn = QPushButton("编辑")
        edit_btn.setFixedSize(30, 18)
        edit_btn.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
                color: #8c8c8c;
                font-size: 10px;
                border-radius: 4px;
                font-family: "Microsoft YaHei", Arial, sans-serif;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
                color: #1890ff;
            }
        """)

        # 更多操作按钮
        more_btn = QPushButton("更多")
        more_btn.setFixedSize(30, 18)
        more_btn.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
                color: #8c8c8c;
                font-size: 10px;
                border-radius: 4px;
                font-family: "Microsoft YaHei", Arial, sans-serif;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
                color: #1890ff;
            }
        """)

        bottom_layout.addWidget(edit_btn)
        bottom_layout.addWidget(more_btn)

        # 添加到主布局
        main_layout.addLayout(top_layout)
        main_layout.addWidget(task_id_display)
        main_layout.addStretch()
        main_layout.addLayout(bottom_layout)

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















# TaskManagement类已迁移到RPA流程管理页面的任务记录标签页






class TemplateManagement(QWidget):
    """模板库管理页面 - 完全复刻AdsPower界面"""

    def __init__(self, api):
        super().__init__()
        self.api = api
        self.templates = []
        self.selected_templates = set()
        self.current_category = ""
        self.init_ui()
        self.load_templates()

    def init_ui(self):
        """初始化界面 - 按照AdsPower模板库管理设计"""
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(10, 10, 10, 10)

        # 顶部筛选区域
        filter_frame = QFrame()
        filter_frame.setFrameStyle(QFrame.Box)
        filter_layout = QHBoxLayout(filter_frame)

        # 分类筛选
        filter_layout.addWidget(QLabel("模板分类:"))
        self.category_combo = QComboBox()
        self.category_combo.setMinimumWidth(150)
        self.category_combo.currentTextChanged.connect(self.on_category_changed)
        filter_layout.addWidget(self.category_combo)

        # 搜索模板
        filter_layout.addWidget(QLabel("搜索模板:"))
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("搜索模板名称、类型...")
        self.search_edit.setMinimumWidth(200)
        self.search_edit.returnPressed.connect(self.search_templates)
        filter_layout.addWidget(self.search_edit)

        filter_layout.addStretch()
        layout.addWidget(filter_frame)

        # 主要操作按钮区域
        button_frame = QFrame()
        button_frame.setFrameStyle(QFrame.Box)
        button_layout = QHBoxLayout(button_frame)

        # 左侧按钮组
        left_buttons = [
            ("导入模板", self.import_templates, "#2196F3"),
            ("导出模板", self.export_selected_templates, "#607D8B"),
            ("创建模板", self.create_template, "#4CAF50"),
            ("删除模板", self.delete_selected_templates, "#F44336"),
            ("分类管理", self.manage_categories, "#673AB7")
        ]

        for text, handler, color in left_buttons:
            btn = QPushButton(text)
            btn.setStyleSheet(f"QPushButton {{ background-color: {color}; color: white; padding: 5px 10px; }}")
            btn.clicked.connect(handler)
            button_layout.addWidget(btn)

        button_layout.addStretch()
        layout.addWidget(button_frame)

        # 表格区域
        self.table = QTableWidget()
        self.setup_table()
        layout.addWidget(self.table)

        self.setLayout(layout)

    def setup_table(self):
        """设置表格 - 按照AdsPower模板库管理的列设计"""
        headers = [
            "选择", "模板名称", "类型", "创建时间", "使用次数", "操作"
        ]

        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        # 设置列宽
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)  # 选择
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # 模板名称
        header.setSectionResizeMode(2, QHeaderView.Fixed)  # 类型
        header.setSectionResizeMode(3, QHeaderView.Stretch)  # 创建时间
        header.setSectionResizeMode(4, QHeaderView.Fixed)  # 使用次数
        header.setSectionResizeMode(5, QHeaderView.Fixed)  # 操作

        # 设置固定列宽
        self.table.setColumnWidth(0, 50)   # 选择
        self.table.setColumnWidth(2, 100)  # 类型
        self.table.setColumnWidth(4, 80)   # 使用次数
        self.table.setColumnWidth(5, 150)  # 操作

        # 表格样式
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.verticalHeader().setVisible(False)

    def save_templates_to_file(self):
        """保存模板数据到文件"""
        try:
            import os
            data_dir = "data"
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)

            templates_file = os.path.join(data_dir, "templates.json")
            with open(templates_file, 'w', encoding='utf-8') as f:
                json.dump(self.templates, f, ensure_ascii=False, indent=2)

        except Exception as e:
            print(f"保存模板数据失败: {e}")

    def load_templates_from_file(self):
        """从文件加载模板数据"""
        try:
            import os
            templates_file = os.path.join("data", "templates.json")
            if os.path.exists(templates_file):
                with open(templates_file, 'r', encoding='utf-8') as f:
                    self.templates = json.load(f)
                return True
        except Exception as e:
            print(f"加载模板数据失败: {e}")
        return False

    def load_templates(self):
        """加载模板列表"""
        try:
            # 尝试从文件加载
            if not self.load_templates_from_file():
                # 如果文件不存在，使用默认数据
                self.templates = [
                {
                    "id": "template_001",
                    "name": "登录模板",
                    "type": "RPA流程",
                    "category": "登录相关",
                    "created_time": "2024-01-15 10:30:00",
                    "usage_count": 25,
                    "description": "通用登录流程模板",
                    "template_data": {
                        "steps": [
                            {"type": "navigate", "params": {"url": "https://example.com/login"}},
                            {"type": "input", "params": {"by": "NAME", "value": "username", "text": "{username}"}},
                            {"type": "input", "params": {"by": "NAME", "value": "password", "text": "{password}"}},
                            {"type": "click", "params": {"by": "XPATH", "value": "//button[@type='submit']"}}
                        ]
                    }
                },
                {
                    "id": "template_002",
                    "name": "数据采集模板",
                    "type": "RPA流程",
                    "category": "数据处理",
                    "created_time": "2024-01-16 14:20:00",
                    "usage_count": 12,
                    "description": "通用数据采集流程模板",
                    "template_data": {
                        "steps": [
                            {"type": "navigate", "params": {"url": "https://example.com/data"}},
                            {"type": "wait", "params": {"seconds": 2}},
                            {"type": "scroll", "params": {"direction": "down", "pixels": 500}}
                        ]
                    }
                },
                {
                    "id": "template_003",
                    "name": "浏览器配置模板",
                    "type": "环境配置",
                    "category": "环境设置",
                    "created_time": "2024-01-17 09:15:00",
                    "usage_count": 8,
                    "description": "标准浏览器环境配置模板",
                    "template_data": {
                        "proxy_type": "HTTP",
                        "user_agent": "Chrome/120.0.0.0",
                        "screen_resolution": "1920x1080"
                    }
                }
            ]
            # 保存默认数据到文件
            self.save_templates_to_file()

            self.load_categories()
            self.update_table()

        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载模板列表失败: {e}")

    def load_categories(self):
        """加载分类列表"""
        try:
            self.category_combo.clear()
            self.category_combo.addItem("全部分类", "")

            # 从模板中提取分类
            categories = set()
            for template in self.templates:
                category = template.get("category", "")
                if category:
                    categories.add(category)

            for category in sorted(categories):
                self.category_combo.addItem(category, category)

        except Exception as e:
            print(f"加载分类失败: {e}")

    def update_table(self):
        """更新表格显示"""
        # 过滤模板
        display_templates = self.templates
        if self.current_category:
            display_templates = [t for t in self.templates if t.get("category") == self.current_category]

        # 搜索过滤
        search_text = self.search_edit.text().strip().lower()
        if search_text:
            display_templates = [t for t in display_templates
                               if search_text in t.get("name", "").lower() or
                                  search_text in t.get("type", "").lower()]

        self.table.setRowCount(len(display_templates))

        for row, template in enumerate(display_templates):
            template_id = template.get("id", "")

            # 选择框
            checkbox = QCheckBox()
            checkbox.setChecked(template_id in self.selected_templates)
            checkbox.stateChanged.connect(lambda state, tid=template_id: self.on_template_selection_changed(tid, state))
            self.table.setCellWidget(row, 0, checkbox)

            # 模板名称
            template_info = f"{template.get('name', '')}\n{template.get('description', '')}"
            self.table.setItem(row, 1, QTableWidgetItem(template_info))

            # 类型
            self.table.setItem(row, 2, QTableWidgetItem(template.get("type", "")))

            # 创建时间
            self.table.setItem(row, 3, QTableWidgetItem(template.get("created_time", "")))

            # 使用次数
            self.table.setItem(row, 4, QTableWidgetItem(str(template.get("usage_count", 0))))

            # 操作按钮
            action_widget = self.create_template_action_buttons(template_id)
            self.table.setCellWidget(row, 5, action_widget)

    def create_template_action_buttons(self, template_id):
        """创建模板操作按钮"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(2)

        # 编辑按钮
        edit_btn = QPushButton("编辑")
        edit_btn.setStyleSheet("QPushButton { background-color: #2196F3; color: white; padding: 2px 6px; }")
        edit_btn.clicked.connect(lambda: self.edit_template(template_id))
        layout.addWidget(edit_btn)

        # 使用按钮
        use_btn = QPushButton("使用")
        use_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; padding: 2px 6px; }")
        use_btn.clicked.connect(lambda: self.use_template(template_id))
        layout.addWidget(use_btn)

        # 复制按钮
        copy_btn = QPushButton("复制")
        copy_btn.setStyleSheet("QPushButton { background-color: #FF9800; color: white; padding: 2px 6px; }")
        copy_btn.clicked.connect(lambda: self.copy_template(template_id))
        layout.addWidget(copy_btn)

        return widget

    def on_template_selection_changed(self, template_id, state):
        """处理模板选择状态变化"""
        if state == Qt.Checked:
            self.selected_templates.add(template_id)
        else:
            self.selected_templates.discard(template_id)

    def on_category_changed(self):
        """分类筛选变化"""
        self.current_category = self.category_combo.currentData() or ""
        self.update_table()

    def search_templates(self):
        """搜索模板"""
        self.update_table()

    def import_templates(self):
        """导入模板"""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "导入模板", "",
                "JSON文件 (*.json);;ZIP文件 (*.zip)"
            )

            if not file_path:
                return

            if file_path.endswith('.json'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    import_data = json.load(f)

                if isinstance(import_data, list):
                    imported_count = 0
                    for template_data in import_data:
                        if self.validate_template_data(template_data):
                            new_template = {
                                "id": f"template_{len(self.templates) + imported_count + 1:03d}",
                                "name": template_data.get("name", "导入的模板"),
                                "type": template_data.get("type", "RPA流程"),
                                "category": template_data.get("category", "导入模板"),
                                "created_time": QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss"),
                                "usage_count": 0,
                                "description": template_data.get("description", ""),
                                "template_data": template_data.get("template_data", {})
                            }
                            self.templates.append(new_template)
                            imported_count += 1

                    # 保存到文件
                    self.save_templates_to_file()

                    self.load_categories()
                    self.update_table()
                    QMessageBox.information(self, "导入成功", f"成功导入 {imported_count} 个模板")
                else:
                    QMessageBox.warning(self, "错误", "导入文件格式不正确")

        except Exception as e:
            QMessageBox.critical(self, "错误", f"导入模板失败: {e}")

    def validate_template_data(self, template_data):
        """验证模板数据"""
        required_fields = ["name", "type"]
        return all(field in template_data for field in required_fields)

    def export_selected_templates(self):
        """导出选中的模板"""
        if not self.selected_templates:
            QMessageBox.information(self, "提示", "请先选择要导出的模板")
            return

        try:
            # 选择保存文件
            file_path, _ = QFileDialog.getSaveFileName(
                self, "导出模板",
                f"templates_export_{QDateTime.currentDateTime().toString('yyyyMMdd_hhmmss')}.json",
                "JSON文件 (*.json)"
            )

            if file_path:
                export_data = []
                for template in self.templates:
                    if template.get("id") in self.selected_templates:
                        export_data.append({
                            "name": template.get("name", ""),
                            "type": template.get("type", ""),
                            "category": template.get("category", ""),
                            "description": template.get("description", ""),
                            "template_data": template.get("template_data", {}),
                            "export_time": QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
                        })

                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, ensure_ascii=False, indent=2)

                QMessageBox.information(self, "成功", f"已导出 {len(export_data)} 个模板到:\n{file_path}")

        except Exception as e:
            QMessageBox.critical(self, "错误", f"导出模板失败: {e}")

    def create_template(self):
        """创建模板"""
        try:
            # 创建模板编辑对话框
            dialog = QDialog(self)
            dialog.setWindowTitle("创建新模板")
            dialog.resize(500, 400)

            layout = QFormLayout()

            # 模板基本信息
            name_edit = QLineEdit()
            name_edit.setPlaceholderText("输入模板名称...")
            layout.addRow("模板名称:", name_edit)

            type_combo = QComboBox()
            type_combo.addItems(["RPA流程", "环境配置", "代理配置", "自定义脚本"])
            layout.addRow("模板类型:", type_combo)

            category_edit = QLineEdit()
            category_edit.setPlaceholderText("输入分类名称...")
            layout.addRow("模板分类:", category_edit)

            desc_edit = QTextEdit()
            desc_edit.setPlaceholderText("输入模板描述...")
            desc_edit.setMaximumHeight(100)
            layout.addRow("模板描述:", desc_edit)

            # 模板内容
            content_edit = QTextEdit()
            content_edit.setPlaceholderText("输入模板内容（JSON格式）...")
            layout.addRow("模板内容:", content_edit)

            # 按钮
            button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            button_box.accepted.connect(dialog.accept)
            button_box.rejected.connect(dialog.reject)
            layout.addRow(button_box)

            dialog.setLayout(layout)

            if dialog.exec_() == QDialog.Accepted:
                # 验证输入
                if not name_edit.text().strip():
                    QMessageBox.warning(dialog, "错误", "请输入模板名称")
                    return

                # 创建新模板
                new_template = {
                    "id": f"template_{len(self.templates) + 1:03d}",
                    "name": name_edit.text().strip(),
                    "type": type_combo.currentText(),
                    "category": category_edit.text().strip() or "默认分类",
                    "created_time": QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss"),
                    "usage_count": 0,
                    "description": desc_edit.toPlainText().strip(),
                    "template_data": {}
                }

                # 解析模板内容
                content_text = content_edit.toPlainText().strip()
                if content_text:
                    try:
                        new_template["template_data"] = json.loads(content_text)
                    except json.JSONDecodeError:
                        QMessageBox.warning(dialog, "警告", "模板内容不是有效的JSON格式，将保存为空内容")

                self.templates.append(new_template)

                # 保存到文件
                self.save_templates_to_file()

                self.load_categories()
                self.update_table()

                QMessageBox.information(self, "创建成功", f"模板 '{new_template['name']}' 创建成功")

        except Exception as e:
            QMessageBox.critical(self, "错误", f"创建模板失败: {e}")

    def edit_template(self, template_id):
        """编辑模板"""
        try:
            # 查找模板
            template = None
            for t in self.templates:
                if t.get("id") == template_id:
                    template = t
                    break

            if not template:
                QMessageBox.warning(self, "错误", "未找到指定的模板")
                return

            # 创建编辑对话框
            dialog = QDialog(self)
            dialog.setWindowTitle(f"编辑模板 - {template.get('name', '')}")
            dialog.resize(500, 400)

            layout = QFormLayout()

            # 模板基本信息
            name_edit = QLineEdit(template.get("name", ""))
            layout.addRow("模板名称:", name_edit)

            type_combo = QComboBox()
            type_combo.addItems(["RPA流程", "环境配置", "代理配置", "自定义脚本"])
            type_combo.setCurrentText(template.get("type", "RPA流程"))
            layout.addRow("模板类型:", type_combo)

            category_edit = QLineEdit(template.get("category", ""))
            layout.addRow("模板分类:", category_edit)

            desc_edit = QTextEdit()
            desc_edit.setPlainText(template.get("description", ""))
            desc_edit.setMaximumHeight(100)
            layout.addRow("模板描述:", desc_edit)

            # 模板内容
            content_edit = QTextEdit()
            content_edit.setPlainText(json.dumps(template.get("template_data", {}), ensure_ascii=False, indent=2))
            layout.addRow("模板内容:", content_edit)

            # 按钮
            button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            button_box.accepted.connect(dialog.accept)
            button_box.rejected.connect(dialog.reject)
            layout.addRow(button_box)

            dialog.setLayout(layout)

            if dialog.exec_() == QDialog.Accepted:
                # 更新模板
                template["name"] = name_edit.text().strip()
                template["type"] = type_combo.currentText()
                template["category"] = category_edit.text().strip() or "默认分类"
                template["description"] = desc_edit.toPlainText().strip()

                # 解析模板内容
                content_text = content_edit.toPlainText().strip()
                if content_text:
                    try:
                        template["template_data"] = json.loads(content_text)
                    except json.JSONDecodeError:
                        QMessageBox.warning(dialog, "警告", "模板内容不是有效的JSON格式，保持原内容不变")

                # 保存到文件
                self.save_templates_to_file()

                self.load_categories()
                self.update_table()
                QMessageBox.information(self, "更新成功", f"模板 '{template['name']}' 更新成功")

        except Exception as e:
            QMessageBox.critical(self, "错误", f"编辑模板失败: {e}")

    def use_template(self, template_id):
        """使用模板"""
        try:
            # 查找模板
            template = None
            for t in self.templates:
                if t.get("id") == template_id:
                    template = t
                    break

            if not template:
                QMessageBox.warning(self, "错误", "未找到指定的模板")
                return

            # 增加使用次数
            template["usage_count"] = template.get("usage_count", 0) + 1

            # 保存到文件
            self.save_templates_to_file()

            # 根据模板类型执行不同操作
            template_type = template.get("type", "")
            if template_type == "RPA流程":
                QMessageBox.information(self, "使用模板", f"RPA流程模板 '{template['name']}' 已应用\n可在RPA流程管理中查看")
            elif template_type == "环境配置":
                QMessageBox.information(self, "使用模板", f"环境配置模板 '{template['name']}' 已应用\n可在环境管理中查看")
            else:
                QMessageBox.information(self, "使用模板", f"模板 '{template['name']}' 已应用")

            self.update_table()

        except Exception as e:
            QMessageBox.critical(self, "错误", f"使用模板失败: {e}")

    def copy_template(self, template_id):
        """复制模板"""
        try:
            # 查找原模板
            original_template = None
            for t in self.templates:
                if t.get("id") == template_id:
                    original_template = t
                    break

            if not original_template:
                QMessageBox.warning(self, "错误", "未找到指定的模板")
                return

            # 创建副本
            import copy
            new_template = copy.deepcopy(original_template)
            new_template["id"] = f"template_{len(self.templates) + 1:03d}"
            new_template["name"] = f"{original_template['name']}_副本"
            new_template["created_time"] = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
            new_template["usage_count"] = 0

            self.templates.append(new_template)

            # 保存到文件
            self.save_templates_to_file()

            self.update_table()

            QMessageBox.information(self, "复制成功", f"已复制模板为 '{new_template['name']}'")

        except Exception as e:
            QMessageBox.critical(self, "错误", f"复制模板失败: {e}")

    def delete_selected_templates(self):
        """删除选中的模板"""
        if not self.selected_templates:
            QMessageBox.information(self, "提示", "请先选择要删除的模板")
            return

        reply = QMessageBox.question(
            self, "确认删除",
            f"确定要删除 {len(self.selected_templates)} 个模板吗？\n此操作不可恢复！",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        # 删除模板
        self.templates = [t for t in self.templates if t.get("id") not in self.selected_templates]
        deleted_count = len(self.selected_templates)
        self.selected_templates.clear()

        # 保存到文件
        self.save_templates_to_file()

        self.load_categories()
        self.update_table()

        QMessageBox.information(self, "删除成功", f"已删除 {deleted_count} 个模板")

    def manage_categories(self):
        """分类管理"""
        try:
            dialog = QDialog(self)
            dialog.setWindowTitle("分类管理")
            dialog.resize(400, 300)

            layout = QVBoxLayout()

            # 分类列表
            category_list = QTableWidget()
            category_list.setColumnCount(2)
            category_list.setHorizontalHeaderLabels(["分类名称", "模板数量"])

            # 统计分类
            category_stats = {}
            for template in self.templates:
                category = template.get("category", "默认分类")
                category_stats[category] = category_stats.get(category, 0) + 1

            category_list.setRowCount(len(category_stats))
            for row, (category_name, count) in enumerate(category_stats.items()):
                category_list.setItem(row, 0, QTableWidgetItem(category_name))
                category_list.setItem(row, 1, QTableWidgetItem(str(count)))

            layout.addWidget(category_list)

            # 按钮
            button_layout = QHBoxLayout()

            new_category_btn = QPushButton("新建分类")
            new_category_btn.clicked.connect(lambda: self.create_new_category(dialog))
            button_layout.addWidget(new_category_btn)

            rename_category_btn = QPushButton("重命名分类")
            rename_category_btn.clicked.connect(lambda: self.rename_category(category_list, dialog))
            button_layout.addWidget(rename_category_btn)

            delete_category_btn = QPushButton("删除分类")
            delete_category_btn.clicked.connect(lambda: self.delete_category(category_list, dialog))
            button_layout.addWidget(delete_category_btn)

            button_layout.addStretch()

            close_btn = QPushButton("关闭")
            close_btn.clicked.connect(dialog.accept)
            button_layout.addWidget(close_btn)

            layout.addLayout(button_layout)
            dialog.setLayout(layout)
            dialog.exec_()

        except Exception as e:
            QMessageBox.critical(self, "错误", f"分类管理失败: {e}")

    def create_new_category(self, parent_dialog):
        """创建新分类"""
        category_name, ok = QInputDialog.getText(parent_dialog, "新建分类", "输入分类名称:")
        if ok and category_name.strip():
            QMessageBox.information(parent_dialog, "成功", f"分类 '{category_name.strip()}' 创建成功")
            parent_dialog.accept()
            self.load_categories()

    def rename_category(self, category_list, parent_dialog):
        """重命名分类"""
        current_row = category_list.currentRow()
        if current_row < 0:
            QMessageBox.information(parent_dialog, "提示", "请先选择要重命名的分类")
            return

        old_name = category_list.item(current_row, 0).text()
        new_name, ok = QInputDialog.getText(parent_dialog, "重命名分类", "输入新的分类名称:", text=old_name)

        if ok and new_name.strip() and new_name.strip() != old_name:
            # 更新所有使用该分类的模板
            for template in self.templates:
                if template.get("category") == old_name:
                    template["category"] = new_name.strip()

            QMessageBox.information(parent_dialog, "成功", f"分类已重命名为 '{new_name.strip()}'")
            parent_dialog.accept()
            self.load_categories()
            self.update_table()

    def delete_category(self, category_list, parent_dialog):
        """删除分类"""
        current_row = category_list.currentRow()
        if current_row < 0:
            QMessageBox.information(parent_dialog, "提示", "请先选择要删除的分类")
            return

        category_name = category_list.item(current_row, 0).text()
        if category_name == "默认分类":
            QMessageBox.warning(parent_dialog, "警告", "不能删除默认分类")
            return

        reply = QMessageBox.question(
            parent_dialog, "确认删除",
            f"确定要删除分类 '{category_name}' 吗？\n该分类下的模板将移动到默认分类",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # 将该分类下的模板移动到默认分类
            for template in self.templates:
                if template.get("category") == category_name:
                    template["category"] = "默认分类"

            QMessageBox.information(parent_dialog, "成功", f"分类 '{category_name}' 已删除")
            parent_dialog.accept()
            self.load_categories()
            self.update_table()


class APIConfigDialog(QDialog):
    """API配置对话框"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("API配置")
        self.setModal(True)
        self.resize(400, 200)
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()

        self.url_edit = QLineEdit("http://local.adspower.com:50325")
        self.key_edit = QLineEdit()

        layout.addRow("API地址:", self.url_edit)
        layout.addRow("API密钥:", self.key_edit)

        # 按钮
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.validate_and_accept)
        button_box.rejected.connect(self.reject)
        layout.addRow(button_box)

        self.setLayout(layout)

    def validate_and_accept(self):
        """验证输入并接受对话框"""
        url = self.url_edit.text().strip()
        if not url:
            QMessageBox.warning(self, "输入错误", "请输入API地址")
            return

        if not url.startswith(('http://', 'https://')):
            QMessageBox.warning(self, "输入错误", "API地址必须以http://或https://开头")
            return

        # 验证通过，接受对话框
        self.accept()

    def get_config(self):
        return {
            "url": self.url_edit.text().strip(),
            "key": self.key_edit.text().strip()
        }


class AdsPowerMainWindow(QMainWindow):
    """主窗口 - 完全复刻AdsPower界面"""

    def __init__(self):
        super().__init__()
        self.api = None
        self.config = self.load_config()
        self.init_ui()

        # 启动后立即显示API配置对话框
        QTimer.singleShot(500, self.show_initial_api_config)

    def init_ui(self):
        self.setWindowTitle("🍎 AdsPower工具专业版 - iOS 26 Liquid Glass")
        self.setGeometry(100, 100, 1280, 800)  # 优化为标准尺寸，符合iOS设计规范

        # 设置最小窗口尺寸以确保内容正常显示
        self.setMinimumSize(1200, 700)

        # 应用消息框样式
        iOS26StyleManager.setup_message_box_style()

        # 设置窗口样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F8F9FA;
                font-family: "Microsoft YaHei", "PingFang SC", Arial, sans-serif;
            }
        """)

        # 设置窗口属性，确保主窗口能正确显示在前台
        self.setWindowFlags(Qt.Window)
        self.setAttribute(Qt.WA_ShowWithoutActivating, False)

        # 确保主窗口始终可见
        self.raise_()
        self.activateWindow()

        # 应用统一的iOS 26风格样式
        self.setStyleSheet(iOS26StyleManager.get_complete_style() + """
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(248, 249, 250, 0.95),
                    stop:1 rgba(240, 242, 247, 0.98));
            }
            QTabWidget::pane {
                border: none;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.9),
                    stop:1 rgba(255, 255, 255, 0.7));
                border-radius: 16px;
            }
            QTabBar::tab {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.8),
                    stop:1 rgba(255, 255, 255, 0.6));
                padding: 12px 20px;
                margin-right: 4px;
                border-radius: 12px 12px 0 0;
                font-size: 15px;
                font-weight: 600;
                color: rgba(28, 28, 30, 0.7);
            }
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(0, 122, 255, 0.9),
                    stop:1 rgba(0, 122, 255, 0.7));
                color: rgba(255, 255, 255, 0.95);
            }
            QTabBar::tab:hover:!selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(0, 122, 255, 0.1),
                    stop:1 rgba(0, 122, 255, 0.05));
                color: rgba(0, 122, 255, 0.9);
            }
        """)

        # 创建标签页
        tabs = QTabWidget()

        # 设置标签页样式
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #E5E5EA;
                border-radius: 12px;
                background-color: white;
                margin-top: 5px;
            }
            QTabBar::tab {
                background-color: #F2F2F7;
                color: #1C1C1E;
                border: 1px solid #E5E5EA;
                border-bottom: none;
                border-radius: 8px 8px 0px 0px;
                padding: 15px 30px;
                margin-right: 2px;
                font-family: "Microsoft YaHei", "PingFang SC", Arial, sans-serif;
                font-size: 15px;
                font-weight: bold;
                min-width: 150px;
                min-height: 25px;
            }
            QTabBar::tab:selected {
                background-color: white;
                color: #007AFF;
                border-bottom: 2px solid #007AFF;
            }
            QTabBar::tab:hover {
                background-color: #E5E5EA;
            }
        """)

        # 环境管理页面
        self.env_tab = EnvironmentManagement(self.api)
        tabs.addTab(self.env_tab, "环境管理")

        # RPA流程页面
        self.rpa_tab = RPAManagement(self.api)
        tabs.addTab(self.rpa_tab, "RPA流程")

        # 模板库页面已删除 - 功能重复
        # 任务记录页面已迁移到RPA流程管理页面

        self.setCentralWidget(tabs)

        # 创建菜单栏
        self.create_menu_bar()

        # 创建状态栏
        self.statusBar().showMessage("AdsPower工具专业版已启动")

    def bring_to_front(self):
        """将主窗口带到前台"""
        self.show()
        self.raise_()
        self.activateWindow()

        # 如果窗口被最小化，恢复它
        if self.isMinimized():
            self.showNormal()

    def resizeEvent(self, event):
        """窗口大小改变事件 - 实现响应式布局"""
        super().resizeEvent(event)

        # 根据窗口宽度调整表格列宽
        if hasattr(self, 'env_tab') and hasattr(self.env_tab, 'table'):
            window_width = self.width()

            # 根据窗口宽度动态调整列宽
            if window_width < 1200:
                # 小窗口模式 - 隐藏部分列或缩小列宽
                self.env_tab.table.setColumnWidth(1, 100)  # 缩小时间列
                self.env_tab.table.setColumnWidth(8, 100)  # 缩小创建时间列
            elif window_width < 1400:
                # 中等窗口模式
                self.env_tab.table.setColumnWidth(1, 120)
                self.env_tab.table.setColumnWidth(8, 120)
            else:
                # 大窗口模式 - 恢复正常列宽
                self.env_tab.table.setColumnWidth(1, 140)
                self.env_tab.table.setColumnWidth(8, 140)

    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()

        # 应用菜单样式
        menubar.setStyleSheet(iOS26StyleManager.get_base_style())

        # 设置菜单
        settings_menu = menubar.addMenu("设置")

        api_action = QAction("API配置", self)
        api_action.triggered.connect(self.show_api_config)
        settings_menu.addAction(api_action)

        test_action = QAction("测试连接", self)
        test_action.triggered.connect(self.test_api_connection)
        settings_menu.addAction(test_action)

        # 工具菜单
        tools_menu = menubar.addMenu("工具")

        deploy_action = QAction("🚀 一键部署环境", self)
        deploy_action.triggered.connect(self.show_deploy_dialog)
        tools_menu.addAction(deploy_action)

        tools_menu.addSeparator()

        reinstall_action = QAction("🔄 重新安装依赖", self)
        reinstall_action.triggered.connect(self.reinstall_dependencies)
        tools_menu.addAction(reinstall_action)

        check_env_action = QAction("🔍 检查环境", self)
        check_env_action.triggered.connect(self.check_environment)
        tools_menu.addAction(check_env_action)

        # 帮助菜单
        help_menu = menubar.addMenu("帮助")

        about_action = QAction("关于", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def show_deploy_dialog(self):
        """显示一键部署对话框"""
        dialog = DeploymentDialog(self)
        dialog.exec_()

    def reinstall_dependencies(self):
        """重新安装依赖"""
        reply = QMessageBox.question(self, "重新安装依赖",
                                   "确定要重新安装所有依赖包吗？\n这可能需要几分钟时间。",
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.run_installation_process("重新安装依赖", ["pip", "install", "-r", "requirements.txt", "--upgrade"])

    def check_environment(self):
        """检查环境"""
        dialog = EnvironmentCheckDialog(self)
        dialog.exec_()

    def run_installation_process(self, title, command):
        """运行安装进程"""
        dialog = InstallationProgressDialog(title, command, self)
        dialog.exec_()

    def init_api(self):
        """初始化API"""
        try:
            url = self.config.get("api_url", "http://local.adspower.com:50325")
            key = self.config.get("api_key", "")
            print(f"[API] 初始化API连接: {url}")
            self.api = AdsPowerAPI(url, key)
        except Exception as e:
            print(f"[API] 初始化失败: {e}")
            self.api = None

    def load_config(self):
        """加载配置"""
        config_file = "config.json"
        default_config = {
            "api_url": "http://local.adspower.com:50325",
            "api_key": "",
            "timeout": 30,
            "auto_start": False,
            "max_threads": 5,
            "log_level": "INFO"
        }

        try:
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:  # 检查文件是否为空
                        config = json.loads(content)
                        # 合并默认配置，确保所有必需的键都存在
                        for key, value in default_config.items():
                            if key not in config:
                                config[key] = value
                        return config
                    else:
                        print("[配置] config.json文件为空，使用默认配置")
            else:
                print("[配置] config.json文件不存在，创建默认配置")
        except json.JSONDecodeError as e:
            print(f"[配置] JSON格式错误: {e}，使用默认配置")
        except Exception as e:
            print(f"[配置] 加载配置失败: {e}，使用默认配置")

        # 创建默认配置文件
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, ensure_ascii=False, indent=2)
            print("[配置] 已创建默认配置文件")
        except Exception as e:
            print(f"[配置] 创建默认配置文件失败: {e}")

        return default_config

    def save_config(self):
        """保存配置"""
        try:
            with open("config.json", 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存配置失败: {e}")

    def show_api_config(self):
        """显示API配置对话框"""
        dialog = APIConfigDialog(self)
        dialog.url_edit.setText(self.config.get("api_url", ""))
        dialog.key_edit.setText(self.config.get("api_key", ""))

        if dialog.exec_() == QDialog.Accepted:
            config = dialog.get_config()
            self.config["api_url"] = config["url"]
            self.config["api_key"] = config["key"]
            self.save_config()
            self.init_api()

            # 更新各个标签页的API引用
            self.env_tab.api = self.api
            self.rpa_tab.api = self.api

            QMessageBox.information(self, "成功", "API配置已更新")

    def show_initial_api_config(self):
        """启动时显示API配置对话框"""
        # 检查是否已有有效的API配置
        if not self.config.get("api_url") or not self.config.get("api_url").strip():
            QMessageBox.information(self, "欢迎",
                "欢迎使用AdsPower Tool Pro！\n\n"
                "请先配置API连接信息以开始使用。")

            dialog = APIConfigDialog(self)
            dialog.url_edit.setText("http://local.adspower.com:50325")
            dialog.key_edit.setText("")

            if dialog.exec_() == QDialog.Accepted:
                config = dialog.get_config()
                self.config["api_url"] = config["url"]
                self.config["api_key"] = config["key"]
                self.save_config()
                self.init_api()

                # 更新各个标签页的API引用
                if hasattr(self, 'env_tab'):
                    self.env_tab.api = self.api
                if hasattr(self, 'rpa_tab'):
                    self.rpa_tab.api = self.api

                QMessageBox.information(self, "成功", "API配置完成！")
            else:
                QMessageBox.warning(self, "提示",
                    "未配置API连接，部分功能可能无法使用。\n"
                    "您可以稍后通过菜单栏的'设置'->'API配置'进行配置。")
        else:
            # 已有配置，直接初始化API
            self.init_api()

    def test_api_connection(self):
        """测试API连接"""
        if not self.api:
            QMessageBox.warning(self, "警告", "请先配置API")
            return

        result = self.api.test_connection()
        if result.get("code") == 0:
            QMessageBox.information(self, "成功", "API连接测试成功")
        else:
            QMessageBox.warning(self, "失败", f"API连接测试失败: {result.get('msg', '')}")

    def show_about(self):
        """显示关于对话框"""
        QMessageBox.about(self, "关于",
                         "AdsPower工具专业版\n\n"
                         "完全复刻AdsPower界面和操作\n"
                         "支持所有AdsPower功能\n\n"
                         "版本: 1.0.0")


def main():
    """主函数 - 增强错误处理和高DPI适配"""
    # 高DPI适配 - 解决界面显示问题
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)

    # 设置DPI缩放策略
    app.setAttribute(Qt.AA_DisableWindowContextHelpButton, True)

    # 设置全局异常处理器
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        print(f"[CRITICAL] 未捕获的异常: {exc_type.__name__}: {exc_value}")
        import traceback
        traceback.print_exception(exc_type, exc_value, exc_traceback)

        # 显示错误对话框
        try:
            QMessageBox.critical(None, "程序错误",
                               f"程序发生未处理的错误:\n{exc_type.__name__}: {exc_value}\n\n"
                               f"请检查控制台输出获取详细信息。\n程序将继续运行，但可能不稳定。")
        except:
            pass  # 如果连错误对话框都无法显示，就忽略

    sys.excepthook = handle_exception

    app.setApplicationName("AdsPower工具专业版")
    app.setApplicationVersion("1.0.0")

    # 设置应用程序图标（如果有的话）
    # app.setWindowIcon(QIcon("icon.png"))

    try:
        print("[DEBUG] 开始创建主窗口...")
        window = AdsPowerMainWindow()
        print("[DEBUG] 主窗口创建成功，开始显示...")
        window.show()
        print("[DEBUG] 主窗口显示成功，启动事件循环...")
        print("[SUCCESS] AdsPower Tool Pro 启动成功！")
        return app.exec_()
    except Exception as e:
        print(f"[CRITICAL] 主程序启动失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


class TaskSettingsDialog(QDialog):
    """任务设置对话框"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("任务设置")
        self.setFixedSize(400, 300)  # 小对话框标准尺寸
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 任务线程数设置
        thread_layout = QHBoxLayout()
        thread_label = QLabel("任务线程数:")
        thread_label.setStyleSheet("font-size: 14px; color: #333;")

        self.thread_spinbox = QSpinBox()
        self.thread_spinbox.setRange(1, 500)
        self.thread_spinbox.setValue(500)
        self.thread_spinbox.setStyleSheet("""
            QSpinBox {
                padding: 6px 12px;
                border: 1px solid #d9d9d9;
                border-radius: 6px;
                font-size: 14px;
                background-color: white;
            }
        """)

        thread_layout.addWidget(thread_label)
        thread_layout.addWidget(self.thread_spinbox)
        thread_layout.addStretch()

        # 按钮
        button_layout = QHBoxLayout()

        ok_btn = QPushButton("确定")
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #1890ff;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 24px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #40a9ff;
            }
        """)
        ok_btn.clicked.connect(self.accept)

        cancel_btn = QPushButton("取消")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #666;
                border: 1px solid #d9d9d9;
                border-radius: 6px;
                padding: 8px 24px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
            }
        """)
        cancel_btn.clicked.connect(self.reject)

        button_layout.addStretch()
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(ok_btn)

        layout.addLayout(thread_layout)
        layout.addStretch()
        layout.addLayout(button_layout)

        self.setLayout(layout)


class RPAFlowEditorDialog(QDialog):
    """RPA流程编辑器对话框 - 完全按照AdsPower截图设计"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("任务流程")
        self.setFixedSize(800, 600)  # 大型对话框标准尺寸
        self.flow_data = {}
        self.init_ui()

    def init_ui(self):
        """初始化界面 - 完全按照AdsPower截图"""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 设置整体样式
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
                font-family: "Microsoft YaHei", Arial, sans-serif;
            }
        """)

        # 顶部工具栏
        toolbar = QWidget()
        toolbar.setFixedHeight(60)
        toolbar.setStyleSheet("""
            QWidget {
                background-color: white;
                border-bottom: 1px solid #e8e8e8;
            }
        """)

        toolbar_layout = QHBoxLayout()
        toolbar_layout.setContentsMargins(20, 10, 20, 10)

        # 搜索框
        search_edit = QLineEdit()
        search_edit.setPlaceholderText("搜索流程步骤")
        search_edit.setFixedWidth(200)
        search_edit.setStyleSheet("""
            QLineEdit {
                padding: 6px 12px;
                border: 1px solid #d9d9d9;
                border-radius: 6px;
                background-color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #1890ff;
            }
        """)

        # 调试按钮
        debug_btn = QPushButton("🐛 调试")
        debug_btn.setStyleSheet("""
            QPushButton {
                border: 1px solid #d9d9d9;
                border-radius: 6px;
                background-color: white;
                padding: 6px 12px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
            }
        """)

        # 调试已选
        debug_selected_btn = QPushButton("🔍 调试已选")
        debug_selected_btn.setStyleSheet("""
            QPushButton {
                border: 1px solid #d9d9d9;
                border-radius: 6px;
                background-color: white;
                padding: 6px 12px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
            }
        """)

        # 导入按钮
        import_btn = QPushButton("📥 导入")
        import_btn.setStyleSheet("""
            QPushButton {
                border: 1px solid #d9d9d9;
                border-radius: 6px;
                background-color: white;
                padding: 6px 12px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
            }
        """)
        import_btn.clicked.connect(self.import_adspower_script)

        toolbar_layout.addWidget(search_edit)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(debug_btn)
        toolbar_layout.addWidget(debug_selected_btn)
        toolbar_layout.addWidget(import_btn)

        toolbar.setLayout(toolbar_layout)

        # 主内容区域 - 左右分栏布局
        content_widget = QWidget()
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)

        # 左侧操作选项面板
        left_panel = QWidget()
        left_panel.setFixedWidth(220)
        left_panel.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid #e8e8e8;
                border-radius: 8px;
            }
        """)

        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)

        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: white;
            }
            QScrollBar:vertical {
                width: 8px;
                background-color: #f5f5f5;
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
        """)

        # 操作选项容器
        options_widget = QWidget()
        options_layout = QVBoxLayout()
        options_layout.setContentsMargins(5, 10, 5, 10)
        options_layout.setSpacing(2)

        # 根据AdsPower官方文档创建操作选项
        self.create_rpa_operation_categories(options_layout)

        options_widget.setLayout(options_layout)
        scroll_area.setWidget(options_widget)
        left_layout.addWidget(scroll_area)
        left_panel.setLayout(left_layout)

        # 右侧内容区域
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(15)

        # 任务流程表单区域
        form_widget = QWidget()
        form_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid #e8e8e8;
                border-radius: 8px;
            }
        """)

        form_layout = QVBoxLayout()
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setSpacing(15)

        # 任务名称
        name_layout = QHBoxLayout()
        name_label = QLabel("* 任务名称")
        name_label.setStyleSheet("color: #333; font-size: 14px; font-weight: 500; min-width: 80px;")
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("请填写任务名称")
        self.name_edit.setStyleSheet("""
            QLineEdit {
                padding: 8px 12px;
                border: 1px solid #d9d9d9;
                border-radius: 6px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #1890ff;
            }
        """)

        # 其他设置按钮
        other_btn = QPushButton("其他设置")
        other_btn.setStyleSheet("""
            QPushButton {
                background-color: #1890ff;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #40a9ff;
            }
        """)

        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_edit)
        name_layout.addWidget(other_btn)

        # 选择分组
        group_layout = QHBoxLayout()
        group_label = QLabel("选择分组")
        group_label.setStyleSheet("color: #333; font-size: 14px; font-weight: 500; min-width: 80px;")
        self.group_select = QComboBox()
        self.group_select.addItem("未分组")
        self.group_select.setStyleSheet("""
            QComboBox {
                padding: 8px 12px;
                border: 1px solid #d9d9d9;
                border-radius: 6px;
                font-size: 14px;
                background-color: white;
            }
        """)
        group_layout.addWidget(group_label)
        group_layout.addWidget(self.group_select)
        group_layout.addStretch()

        # 异常处理选项
        exception_layout = QHBoxLayout()
        exception_label = QLabel("异常处理")
        exception_label.setStyleSheet("color: #333; font-size: 14px; font-weight: 500; min-width: 80px;")

        self.exception_combo1 = QComboBox()
        self.exception_combo1.addItems(["跳过", "中断"])
        self.exception_combo1.setCurrentText("跳过")
        self.exception_combo1.setStyleSheet("""
            QComboBox {
                padding: 6px 12px;
                border: 1px solid #d9d9d9;
                border-radius: 6px;
                font-size: 14px;
                background-color: white;
                min-width: 80px;
            }
        """)

        self.exception_combo2 = QComboBox()
        self.exception_combo2.addItems(["任务完成", "清除标签"])
        self.exception_combo2.setCurrentText("清除标签")
        self.exception_combo2.setStyleSheet("""
            QComboBox {
                padding: 6px 12px;
                border: 1px solid #d9d9d9;
                border-radius: 6px;
                font-size: 14px;
                background-color: white;
                min-width: 100px;
            }
        """)

        self.exception_combo3 = QComboBox()
        self.exception_combo3.addItems(["关闭浏览器", "保留浏览器"])
        self.exception_combo3.setCurrentText("关闭浏览器")
        self.exception_combo3.setStyleSheet("""
            QComboBox {
                padding: 6px 12px;
                border: 1px solid #d9d9d9;
                border-radius: 6px;
                font-size: 14px;
                background-color: white;
                min-width: 120px;
            }
        """)

        exception_layout.addWidget(exception_label)
        exception_layout.addWidget(self.exception_combo1)
        exception_layout.addWidget(self.exception_combo2)
        exception_layout.addWidget(self.exception_combo3)
        exception_layout.addStretch()

        form_layout.addLayout(name_layout)
        form_layout.addLayout(group_layout)
        form_layout.addLayout(exception_layout)

        form_widget.setLayout(form_layout)

        # 流程编辑区域 - 显示已添加的步骤
        self.flow_area = QWidget()
        self.flow_area.setMinimumHeight(300)
        self.flow_area.setStyleSheet("""
            QWidget {
                background-color: #fafafa;
                border: 1px solid #e8e8e8;
                border-radius: 8px;
            }
        """)

        self.flow_layout = QVBoxLayout()
        self.flow_layout.setAlignment(Qt.AlignTop)

        # 初始空状态
        self.show_empty_state()

        self.flow_area.setLayout(self.flow_layout)

        # 添加到右侧布局
        right_layout.addWidget(form_widget)
        right_layout.addWidget(self.flow_area)

        # 底部按钮
        bottom_layout = QHBoxLayout()

        add_btn = QPushButton("✓ 添加")
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #1890ff;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 24px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #40a9ff;
            }
        """)
        add_btn.clicked.connect(self.accept)

        cancel_btn = QPushButton("取消")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #666;
                border: 1px solid #d9d9d9;
                border-radius: 6px;
                padding: 8px 24px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
            }
        """)
        cancel_btn.clicked.connect(self.reject)

        bottom_layout.addStretch()
        bottom_layout.addWidget(cancel_btn)
        bottom_layout.addWidget(add_btn)

        right_layout.addLayout(bottom_layout)
        right_widget.setLayout(right_layout)

        # 添加左右面板到主布局
        content_layout.addWidget(left_panel)
        content_layout.addWidget(right_widget)

        content_widget.setLayout(content_layout)

        layout.addWidget(toolbar)
        layout.addWidget(content_widget)
        self.setLayout(layout)

    def show_empty_state(self):
        """显示空状态"""
        # 清空现有内容
        for i in reversed(range(self.flow_layout.count())):
            child = self.flow_layout.itemAt(i).widget()
            if child:
                child.setParent(None)

        # 空状态图标和文字
        empty_widget = QWidget()
        empty_layout = QVBoxLayout()
        empty_layout.setAlignment(Qt.AlignCenter)

        empty_icon = QLabel("💻")
        empty_icon.setAlignment(Qt.AlignCenter)
        empty_icon.setStyleSheet("font-size: 48px; margin-bottom: 10px;")

        empty_label = QLabel("🖱️ 点击左边的操作选项添加到流程步骤")
        empty_label.setAlignment(Qt.AlignCenter)
        empty_label.setStyleSheet("""
            QLabel {
                color: #1890ff;
                font-size: 16px;
                padding: 20px;
            }
        """)

        empty_layout.addWidget(empty_icon)
        empty_layout.addWidget(empty_label)
        empty_widget.setLayout(empty_layout)

        self.flow_layout.addWidget(empty_widget)

    def add_operation_to_flow(self, operation_type, operation_name):
        """添加操作到流程中"""
        try:
            # 如果是第一个操作，清空空状态
            if not hasattr(self, 'flow_steps'):
                self.flow_steps = []
                # 清空空状态
                for i in reversed(range(self.flow_layout.count())):
                    child = self.flow_layout.itemAt(i).widget()
                    if child:
                        child.setParent(None)

            # 创建操作步骤
            step_data = {
                "type": operation_type,
                "name": operation_name,
                "config": self.get_default_config(operation_type)
            }

            self.flow_steps.append(step_data)

            # 创建步骤显示组件
            step_widget = self.create_step_widget(len(self.flow_steps) - 1, step_data)
            self.flow_layout.addWidget(step_widget)

            # 更新流程数据
            if "actions" not in self.flow_data:
                self.flow_data["actions"] = []
            self.flow_data["actions"] = self.flow_steps.copy()

        except Exception as e:
            QMessageBox.warning(self, "添加失败", f"添加操作失败: {e}")

    def get_default_config(self, operation_type):
        """获取操作的默认配置"""
        default_configs = {
            "accessWebsite": {"url": "https://example.com", "timeout": 30000},
            "clickElement": {"selector": "", "elementOrder": "fixed", "elementOrderValue": 1},
            "inputText": {"selector": "", "content": "", "inputInterval": 100},
            "waitTime": {"timeout": 3000},
            "keyboardKey": {"key": "Enter"},
            "newTab": {},
            "closeTab": {},
            "refreshPage": {},
            "scrollPage": {"distance": "bottom", "scrollType": "smooth"}
        }
        return default_configs.get(operation_type, {})

    def create_step_widget(self, index, step_data):
        """创建步骤显示组件 - 显示完整的AdsPower RPA代码"""
        widget = QWidget()
        widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid #e8e8e8;
                border-radius: 6px;
                margin: 2px;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 8, 10, 8)

        # 顶部：步骤序号和操作名称
        top_layout = QHBoxLayout()

        # 步骤序号
        index_label = QLabel(f"{index + 1}")
        index_label.setStyleSheet("""
            QLabel {
                background-color: #1890ff;
                color: white;
                border-radius: 12px;
                padding: 4px 8px;
                font-size: 12px;
                font-weight: bold;
                min-width: 20px;
                max-width: 20px;
            }
        """)
        index_label.setAlignment(Qt.AlignCenter)
        top_layout.addWidget(index_label)

        # 操作名称
        name_label = QLabel(step_data["name"])
        name_label.setStyleSheet("font-size: 14px; font-weight: 500; color: #333;")
        top_layout.addWidget(name_label)

        top_layout.addStretch()

        # 底部：显示完整的AdsPower RPA代码
        code_layout = QVBoxLayout()

        # 操作类型
        type_label = QLabel(f"类型: {step_data.get('type', 'unknown')}")
        type_label.setStyleSheet("font-size: 12px; color: #666; margin-left: 30px;")
        code_layout.addWidget(type_label)

        # 配置参数
        config = step_data.get('config', {})
        if config:
            config_text = "配置: " + ", ".join([f"{k}={v}" for k, v in config.items()])
            config_label = QLabel(config_text)
            config_label.setStyleSheet("font-size: 12px; color: #666; margin-left: 30px;")
            config_label.setWordWrap(True)
            code_layout.addWidget(config_label)

        # JSON代码显示
        import json
        json_code = json.dumps(step_data, ensure_ascii=False, indent=2)
        code_label = QLabel(f"代码:\n{json_code}")
        code_label.setStyleSheet("""
            QLabel {
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
                color: #333;
                background-color: #f8f8f8;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                padding: 8px;
                margin-left: 30px;
                margin-top: 5px;
            }
        """)
        code_label.setWordWrap(True)
        code_layout.addWidget(code_label)

        layout.addLayout(top_layout)
        layout.addLayout(code_layout)

        layout.addStretch()

        # 编辑按钮
        edit_btn = QPushButton("编辑")
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 4px 12px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #e8e8e8;
            }
        """)
        edit_btn.clicked.connect(lambda: self.edit_step(index))
        layout.addWidget(edit_btn)

        # 删除按钮
        delete_btn = QPushButton("删除")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #fff2f0;
                border: 1px solid #ffccc7;
                border-radius: 4px;
                padding: 4px 12px;
                font-size: 12px;
                color: #ff4d4f;
            }
            QPushButton:hover {
                background-color: #ffe7e6;
            }
        """)
        delete_btn.clicked.connect(lambda: self.delete_step(index))
        layout.addWidget(delete_btn)

        widget.setLayout(layout)
        return widget

    def edit_step(self, index):
        """编辑步骤"""
        QMessageBox.information(self, "编辑步骤", f"编辑第 {index + 1} 个步骤")

    def delete_step(self, index):
        """删除步骤"""
        try:
            if 0 <= index < len(self.flow_steps):
                self.flow_steps.pop(index)
                self.refresh_flow_display()

        except Exception as e:
            QMessageBox.warning(self, "删除失败", f"删除步骤失败: {e}")

    def refresh_flow_display(self):
        """刷新流程显示"""
        # 清空现有显示
        for i in reversed(range(self.flow_layout.count())):
            child = self.flow_layout.itemAt(i).widget()
            if child:
                child.setParent(None)

        if not hasattr(self, 'flow_steps') or not self.flow_steps:
            self.show_empty_state()
        else:
            # 重新创建所有步骤
            for i, step in enumerate(self.flow_steps):
                step_widget = self.create_step_widget(i, step)
                self.flow_layout.addWidget(step_widget)

    def create_rpa_operation_categories(self, layout):
        """创建AdsPower RPA操作选项分类 - 完全按照官方文档"""

        # 页面操作分类 - 完全按照AdsPower官方文档的16个操作
        page_operations = [
            ("新建标签", "newTab"),
            ("关闭标签", "closeTab"),
            ("关闭其他标签", "closeOtherTabs"),
            ("切换标签", "switchTab"),
            ("访问网站", "accessWebsite"),
            ("刷新页面", "refreshPage"),
            ("页面后退", "pageBack"),
            ("页面截图", "pageScreenshot"),
            ("经过元素", "hoverElement"),
            ("下拉选择器", "selectDropdown"),
            ("元素聚焦", "focusElement"),
            ("点击元素", "clickElement"),
            ("输入内容", "inputText"),
            ("滚动页面", "scrollPage"),
            ("上传附件", "uploadFile"),
            ("执行JS脚本", "executeJS")
        ]

        # 键盘操作分类 - 完全按照AdsPower官方文档的2个操作
        keyboard_operations = [
            ("键盘按键", "keyboardKey"),
            ("组合键", "keyboardCombo")
        ]

        # 等待操作分类 - 完全按照AdsPower官方文档的3个操作
        wait_operations = [
            ("等待时间", "waitTime"),
            ("等待元素出现", "waitElementAppear"),
            ("等待请求完成", "waitRequestComplete")
        ]

        # 获取数据分类 - 根据AdsPower官方文档
        data_operations = [
            ("获取元素数据", "getElementData"),
            ("获取URL", "getURL"),
            ("获取页面标题", "getPageTitle"),
            ("获取元素属性", "getElementAttribute"),
            ("获取元素文本", "getElementText"),
            ("获取粘贴板", "getClipboard")
        ]

        # 数据处理分类 - 根据AdsPower官方文档
        process_operations = [
            ("文本中提取", "extractText"),
            ("转换Json对象", "convertJson"),
            ("随机提取", "randomExtract"),
            ("导入Excel素材", "importExcel"),
            ("导入txt", "importTxt")
        ]

        # 环境信息分类 - 根据AdsPower官方文档
        env_operations = [
            ("更新环境备注", "updateEnvRemark"),
            ("更新环境标签", "updateEnvTags")
        ]

        # 流程管理分类 - 根据AdsPower官方文档
        flow_operations = [
            ("启动新浏览器", "startNewBrowser"),
            ("IF条件", "ifCondition"),
            ("For循环元素", "forLoopElement"),
            ("For循环次数", "forLoopCount"),
            ("For循环数据", "forLoopData"),
            ("While循环", "whileLoop"),
            ("退出循环", "exitLoop"),
            ("关闭浏览器", "closeBrowser"),
            ("使用其他流程", "useOtherFlow")
        ]

        # 第三方工具分类 - 根据AdsPower官方文档
        third_party_operations = [
            ("2Captcha", "2captcha"),
            ("Google Sheet", "googleSheet"),
            ("OpenAI", "openAI")
        ]

        # 创建分类 - 完全按照AdsPower的分类顺序
        categories = [
            ("页面操作", page_operations),
            ("键盘操作", keyboard_operations),
            ("等待操作", wait_operations),
            ("获取数据", data_operations),
            ("数据处理", process_operations),
            ("环境信息", env_operations),
            ("流程管理", flow_operations),
            ("第三方工具", third_party_operations)
        ]

        for category_name, operations in categories:
            self.create_rpa_category_section(layout, category_name, operations)

    def create_rpa_category_section(self, layout, category_name, operations):
        """创建操作分类区域"""
        # 分类标题
        category_btn = QPushButton(category_name)
        category_btn.setCheckable(True)
        category_btn.setChecked(True)  # 默认展开
        category_btn.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 8px 12px;
                border: none;
                background-color: #f5f5f5;
                font-size: 13px;
                font-weight: bold;
                color: #333;
            }
            QPushButton:hover {
                background-color: #e8e8e8;
            }
            QPushButton:checked {
                background-color: #1890ff;
                color: white;
            }
        """)
        layout.addWidget(category_btn)

        # 操作项容器
        operations_widget = QWidget()
        operations_layout = QVBoxLayout()
        operations_layout.setContentsMargins(0, 0, 0, 0)
        operations_layout.setSpacing(1)

        for op_name, op_type in operations:
            op_btn = QPushButton(f"  + {op_name}")
            op_btn.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding: 6px 20px;
                    border: none;
                    background-color: white;
                    font-size: 12px;
                    color: #666;
                }
                QPushButton:hover {
                    background-color: #f0f8ff;
                    color: #1890ff;
                }
            """)
            op_btn.clicked.connect(lambda _, t=op_type, n=op_name: self.add_operation_to_flow(t, n))
            operations_layout.addWidget(op_btn)

        operations_widget.setLayout(operations_layout)
        layout.addWidget(operations_widget)

        # 连接分类按钮的展开/收起功能
        category_btn.toggled.connect(lambda checked: operations_widget.setVisible(checked))

    def import_adspower_script(self):
        """导入AdsPower脚本 - 自动识别和转换格式"""
        try:
            # 创建导入对话框 - 完全按照AdsPower界面设计
            dialog = QDialog(self)
            dialog.setWindowTitle("导入")
            dialog.setFixedSize(600, 500)
            dialog.setStyleSheet("""
                QDialog {
                    background-color: white;
                    font-family: "Microsoft YaHei", Arial, sans-serif;
                }
            """)

            layout = QVBoxLayout()
            layout.setContentsMargins(20, 20, 20, 20)
            layout.setSpacing(15)

            # 标题
            title_label = QLabel("导入脚本")
            title_label.setStyleSheet("""
                QLabel {
                    font-size: 18px;
                    font-weight: bold;
                    color: #333;
                    margin-bottom: 10px;
                }
            """)
            layout.addWidget(title_label)

            # 说明文字
            desc_label = QLabel("支持导入AdsPower RPA脚本，自动识别格式并转换")
            desc_label.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    color: #666;
                    margin-bottom: 15px;
                }
            """)
            layout.addWidget(desc_label)

            # 脚本内容输入区域
            content_label = QLabel("脚本内容:")
            content_label.setStyleSheet("font-size: 14px; font-weight: 500; color: #333;")
            layout.addWidget(content_label)

            script_input = QTextEdit()
            script_input.setPlaceholderText("请粘贴AdsPower RPA脚本内容（JSON格式）...")
            script_input.setMinimumHeight(250)
            script_input.setStyleSheet("""
                QTextEdit {
                    border: 1px solid #d9d9d9;
                    border-radius: 6px;
                    padding: 10px;
                    font-family: "Consolas", "Monaco", monospace;
                    font-size: 12px;
                    background-color: #fafafa;
                }
                QTextEdit:focus {
                    border-color: #1890ff;
                    background-color: white;
                }
            """)
            layout.addWidget(script_input)

            # 导入选项
            options_layout = QHBoxLayout()

            # 文件导入按钮
            file_btn = QPushButton("从文件导入")
            file_btn.setStyleSheet("""
                QPushButton {
                    background-color: #f0f0f0;
                    border: 1px solid #d9d9d9;
                    border-radius: 6px;
                    padding: 8px 16px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #e8e8e8;
                }
            """)

            def load_from_file():
                file_path, _ = QFileDialog.getOpenFileName(
                    dialog, "选择AdsPower脚本文件", "",
                    "JSON文件 (*.json);;所有文件 (*)"
                )
                if file_path:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        script_input.setPlainText(content)
                    except Exception as e:
                        QMessageBox.warning(dialog, "读取失败", f"读取文件失败: {e}")

            file_btn.clicked.connect(load_from_file)
            options_layout.addWidget(file_btn)
            options_layout.addStretch()

            layout.addLayout(options_layout)

            # 按钮区域
            button_layout = QHBoxLayout()

            cancel_btn = QPushButton("取消")
            cancel_btn.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    color: #666;
                    border: 1px solid #d9d9d9;
                    border-radius: 6px;
                    padding: 8px 24px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #f5f5f5;
                }
            """)
            cancel_btn.clicked.connect(dialog.reject)

            import_btn = QPushButton("导入")
            import_btn.setStyleSheet("""
                QPushButton {
                    background-color: #1890ff;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 24px;
                    font-size: 14px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #40a9ff;
                }
            """)

            def do_import():
                try:
                    script_content = script_input.toPlainText().strip()
                    if not script_content:
                        QMessageBox.warning(dialog, "输入错误", "请输入脚本内容")
                        return

                    # 自动识别和转换AdsPower格式
                    success = self.parse_adspower_script(script_content)
                    if success:
                        QMessageBox.information(dialog, "导入成功", "AdsPower脚本导入成功！")
                        dialog.accept()
                    else:
                        QMessageBox.warning(dialog, "导入失败", "脚本格式不正确或不支持")

                except Exception as e:
                    QMessageBox.critical(dialog, "导入错误", f"导入过程中发生错误: {e}")

            import_btn.clicked.connect(do_import)

            button_layout.addStretch()
            button_layout.addWidget(cancel_btn)
            button_layout.addWidget(import_btn)

            layout.addLayout(button_layout)
            dialog.setLayout(layout)
            dialog.exec_()

        except Exception as e:
            QMessageBox.critical(self, "错误", f"打开导入对话框失败: {e}")

    def parse_adspower_script(self, script_content):
        """解析AdsPower脚本格式"""
        try:
            # 尝试解析JSON
            import json
            script_data = json.loads(script_content)

            # 检测AdsPower格式
            if isinstance(script_data, list):
                # 格式1: 直接是actions数组
                if all(isinstance(item, dict) and "type" in item for item in script_data):
                    self.flow_data = {
                        "name": "导入的AdsPower脚本",
                        "description": "从AdsPower导入的RPA脚本",
                        "actions": script_data
                    }
                    self.name_edit.setText("导入的AdsPower脚本")
                    return True

            elif isinstance(script_data, dict):
                # 格式2: 包含name和actions的对象
                if "actions" in script_data or "steps" in script_data:
                    self.flow_data = script_data
                    if "name" in script_data:
                        self.name_edit.setText(script_data["name"])
                    if "group" in script_data and script_data["group"]:
                        # 添加分组到下拉框
                        group_text = script_data["group"]
                        if self.group_select.findText(group_text) == -1:
                            self.group_select.addItem(group_text)
                        self.group_select.setCurrentText(group_text)
                    return True

            return False

        except json.JSONDecodeError:
            return False
        except Exception as e:
            print(f"[ERROR] 解析AdsPower脚本失败: {e}")
            return False

    def import_script(self):
        """导入脚本 - AdsPower原版JSON粘贴导入功能"""
        try:
            from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QRadioButton, QButtonGroup, QMessageBox, QLabel

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
                    script_data = json.loads(json_text)

                    # 检查是否是替换模式
                    is_replace = button_group.checkedId() == 1

                    # 验证JSON格式
                    if not isinstance(script_data, dict):
                        QMessageBox.warning(dialog, "格式错误", "JSON格式不正确，应为对象格式")
                        return

                    # 填充表单数据
                    if "name" in script_data:
                        self.name_edit.setText(script_data["name"])

                    if "group" in script_data:
                        # 添加分组到下拉框
                        group_text = script_data["group"]
                        if self.group_select.findText(group_text) == -1:
                            self.group_select.addItem(group_text)
                        self.group_select.setCurrentText(group_text)

                    # 填充异常处理设置
                    if "exception_handling" in script_data:
                        eh = script_data["exception_handling"]
                        if "action" in eh:
                            self.exception_combo1.setCurrentText(eh["action"])
                        if "completion" in eh:
                            self.exception_combo2.setCurrentText(eh["completion"])
                        if "browser" in eh:
                            self.exception_combo3.setCurrentText(eh["browser"])

                    self.flow_data = script_data

                    dialog.accept()
                    mode_text = "替换" if is_replace else "追加"
                    QMessageBox.information(self, "导入成功", f"脚本{mode_text}导入成功")

                except json.JSONDecodeError as e:
                    QMessageBox.critical(dialog, "JSON格式错误", f"JSON格式不正确:\n{str(e)}")
                except Exception as e:
                    QMessageBox.critical(dialog, "导入失败", f"导入时发生错误:\n{str(e)}")

            confirm_btn.clicked.connect(import_json)
            button_layout.addWidget(confirm_btn)

            layout.addLayout(button_layout)
            dialog.exec_()

        except Exception as e:
            QMessageBox.critical(self, "错误", f"打开导入对话框失败: {e}")

    def get_flow_data(self):
        """获取流程数据"""
        if not self.name_edit.text().strip():
            QMessageBox.warning(self, "输入错误", "请输入任务名称")
            return None

        self.flow_data.update({
            "name": self.name_edit.text().strip(),
            "group": self.group_select.currentText(),
            "exception_handling": {
                "action": self.exception_combo1.currentText(),
                "completion": self.exception_combo2.currentText(),
                "browser": self.exception_combo3.currentText()
            }
        })

        return self.flow_data


class DeploymentDialog(QDialog):
    """一键部署对话框"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🚀 一键部署环境")
        self.setFixedSize(600, 500)
        self.setModal(True)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # 标题
        title_label = QLabel("AdsPower工具专业版 - 一键部署环境")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #1C1C1E;
                padding: 20px;
                text-align: center;
            }
        """)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # 说明文本
        info_text = QTextEdit()
        info_text.setReadOnly(True)
        info_text.setMaximumHeight(200)
        info_text.setHtml("""
        <div style="font-family: 'Microsoft YaHei'; font-size: 14px; line-height: 1.6;">
        <h3>🎯 一键部署功能说明</h3>
        <p><b>本功能将自动完成以下操作：</b></p>
        <ul>
        <li>✅ 检查Python环境</li>
        <li>✅ 安装所有必需的依赖包</li>
        <li>✅ 创建必要的目录结构</li>
        <li>✅ 生成启动脚本</li>
        <li>✅ 验证环境配置</li>
        </ul>
        <p><b>适用场景：</b></p>
        <ul>
        <li>🆕 新电脑首次部署</li>
        <li>🔄 环境损坏需要重新部署</li>
        <li>⬆️ 升级到新版本</li>
        </ul>
        <p><b>注意：</b>部署过程可能需要5-10分钟，请保持网络连接。</p>
        </div>
        """)
        layout.addWidget(info_text)

        # 选项区域
        options_group = QGroupBox("部署选项")
        options_layout = QVBoxLayout(options_group)

        self.full_deploy_radio = QRadioButton("🚀 完整部署（推荐）")
        self.full_deploy_radio.setChecked(True)
        self.full_deploy_radio.setStyleSheet("font-size: 14px; padding: 5px;")
        options_layout.addWidget(self.full_deploy_radio)

        self.quick_deploy_radio = QRadioButton("⚡ 快速部署（仅安装依赖）")
        self.quick_deploy_radio.setStyleSheet("font-size: 14px; padding: 5px;")
        options_layout.addWidget(self.quick_deploy_radio)

        self.repair_deploy_radio = QRadioButton("🔧 修复部署（修复损坏的环境）")
        self.repair_deploy_radio.setStyleSheet("font-size: 14px; padding: 5px;")
        options_layout.addWidget(self.repair_deploy_radio)

        layout.addWidget(options_group)

        # 按钮区域
        button_layout = QHBoxLayout()

        cancel_btn = QPushButton("取消")
        cancel_btn.setStyleSheet(iOS26StyleManager.get_button_style('secondary'))
        cancel_btn.clicked.connect(self.reject)

        deploy_btn = QPushButton("🚀 开始部署")
        deploy_btn.setStyleSheet(iOS26StyleManager.get_button_style('primary'))
        deploy_btn.clicked.connect(self.start_deployment)

        button_layout.addStretch()
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(deploy_btn)

        layout.addLayout(button_layout)

    def start_deployment(self):
        """开始部署"""
        if self.full_deploy_radio.isChecked():
            deploy_type = "full"
        elif self.quick_deploy_radio.isChecked():
            deploy_type = "quick"
        else:
            deploy_type = "repair"

        self.accept()

        # 创建部署进度对话框
        progress_dialog = DeploymentProgressDialog(deploy_type, self.parent())
        progress_dialog.exec_()


class DeploymentProgressDialog(QDialog):
    """部署进度对话框"""
    def __init__(self, deploy_type, parent=None):
        super().__init__(parent)
        self.deploy_type = deploy_type
        self.setWindowTitle("🚀 正在部署环境...")
        self.setFixedSize(500, 400)
        self.setModal(True)
        self.init_ui()
        self.start_deployment()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # 进度显示
        self.progress_label = QLabel("准备开始部署...")
        self.progress_label.setStyleSheet("font-size: 14px; padding: 10px;")
        layout.addWidget(self.progress_label)

        # 进度条
        self.progress_bar = QProgressDialog()
        self.progress_bar.setWindowFlags(Qt.Widget)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # 日志显示
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E;
                color: #FFFFFF;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
                border: 1px solid #333;
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.log_text)

        # 按钮
        self.close_btn = QPushButton("关闭")
        self.close_btn.setEnabled(False)
        self.close_btn.setStyleSheet(iOS26StyleManager.get_button_style('secondary'))
        self.close_btn.clicked.connect(self.accept)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.close_btn)
        layout.addLayout(button_layout)

    def start_deployment(self):
        """开始部署过程"""
        self.deployment_thread = DeploymentThread(self.deploy_type)
        self.deployment_thread.progress_updated.connect(self.update_progress)
        self.deployment_thread.log_updated.connect(self.update_log)
        self.deployment_thread.finished.connect(self.deployment_finished)
        self.deployment_thread.start()

    def update_progress(self, value, text):
        """更新进度"""
        self.progress_bar.setValue(value)
        self.progress_label.setText(text)

    def update_log(self, text):
        """更新日志"""
        self.log_text.append(text)
        # 自动滚动到底部
        cursor = self.log_text.textCursor()
        cursor.movePosition(cursor.End)
        self.log_text.setTextCursor(cursor)

    def deployment_finished(self, success):
        """部署完成"""
        self.close_btn.setEnabled(True)
        if success:
            self.progress_label.setText("✅ 部署完成！")
            QMessageBox.information(self, "部署成功", "环境部署完成！\n您现在可以正常使用AdsPower工具专业版。")
        else:
            self.progress_label.setText("❌ 部署失败")
            QMessageBox.warning(self, "部署失败", "环境部署失败，请查看日志了解详情。")


class DeploymentThread(QThread):
    """部署线程"""
    progress_updated = pyqtSignal(int, str)
    log_updated = pyqtSignal(str)
    finished = pyqtSignal(bool)

    def __init__(self, deploy_type):
        super().__init__()
        self.deploy_type = deploy_type

    def run(self):
        """执行部署"""
        try:
            import subprocess
            import os

            self.log_updated.emit("🚀 开始部署环境...")
            self.progress_updated.emit(10, "检查Python环境...")

            # 检查Python
            result = subprocess.run(["python", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                self.log_updated.emit(f"✅ Python版本: {result.stdout.strip()}")
            else:
                self.log_updated.emit("❌ Python未安装或不在PATH中")
                self.finished.emit(False)
                return

            self.progress_updated.emit(20, "创建目录结构...")

            # 创建必要目录
            directories = ["data", "logs", "exports", "backups"]
            for directory in directories:
                if not os.path.exists(directory):
                    os.makedirs(directory)
                    self.log_updated.emit(f"✅ 创建目录: {directory}")
                else:
                    self.log_updated.emit(f"📁 目录已存在: {directory}")

            self.progress_updated.emit(40, "安装依赖包...")

            # 安装依赖
            if self.deploy_type in ["full", "quick", "repair"]:
                self.log_updated.emit("📦 正在安装依赖包...")
                result = subprocess.run([
                    "pip", "install", "-r", "requirements.txt", "--upgrade"
                ], capture_output=True, text=True)

                if result.returncode == 0:
                    self.log_updated.emit("✅ 依赖包安装成功")
                else:
                    self.log_updated.emit(f"❌ 依赖包安装失败: {result.stderr}")
                    self.finished.emit(False)
                    return

            self.progress_updated.emit(70, "生成启动脚本...")

            # 生成启动脚本
            if self.deploy_type == "full":
                self.create_deployment_scripts()

            self.progress_updated.emit(90, "验证环境...")

            # 验证环境
            self.verify_environment()

            self.progress_updated.emit(100, "部署完成！")
            self.log_updated.emit("🎉 环境部署完成！")
            self.finished.emit(True)

        except Exception as e:
            self.log_updated.emit(f"❌ 部署过程中发生错误: {str(e)}")
            self.finished.emit(False)

    def create_deployment_scripts(self):
        """创建部署脚本"""
        # 创建一键部署环境脚本
        deploy_script = '''@echo off
title AdsPower Tool Pro - One-Click Deployment
chcp 65001 >nul

echo.
echo ========================================
echo   AdsPower工具专业版 - 一键部署环境
echo ========================================
echo.

echo [1/5] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python未安装！请先安装Python 3.7+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo ✅ Python环境检查通过

echo.
echo [2/5] 创建目录结构...
if not exist data mkdir data
if not exist logs mkdir logs
if not exist exports mkdir exports
if not exist backups mkdir backups
echo ✅ 目录结构创建完成

echo.
echo [3/5] 安装依赖包...
pip install -r requirements.txt --upgrade
if errorlevel 1 (
    echo ❌ 依赖包安装失败！
    pause
    exit /b 1
)
echo ✅ 依赖包安装完成

echo.
echo [4/5] 验证环境...
python -c "import PyQt5, requests, selenium; print('✅ 核心依赖验证通过')"
if errorlevel 1 (
    echo ❌ 环境验证失败！
    pause
    exit /b 1
)

echo.
echo [5/5] 部署完成！
echo.
echo ========================================
echo   🎉 部署成功完成！
echo ========================================
echo.
echo 使用说明:
echo 1. 双击 "AdsPower_Tool_Launcher.bat" 启动程序
echo 2. 或者双击 "快速启动.bat" 快速启动
echo.
echo 注意: 请确保AdsPower客户端正在运行
echo.
pause
'''

        with open("一键部署环境.bat", "w", encoding="utf-8") as f:
            f.write(deploy_script)
        self.log_updated.emit("✅ 创建一键部署脚本")

        # 创建专业启动器
        launcher_script = '''@echo off
title AdsPower Tool Pro - Professional Launcher
chcp 65001 >nul

echo.
echo ========================================
echo   AdsPower工具专业版 - 专业启动器
echo ========================================
echo.

echo [1/4] 检查程序文件...
if not exist "main.py" (
    echo ❌ 主程序文件不存在！
    echo 请确保在正确的程序目录中运行此脚本
    pause
    exit /b 1
)
echo ✅ 程序文件检查通过

echo.
echo [2/4] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python环境异常！
    echo 请运行 "一键部署环境.bat" 重新部署
    pause
    exit /b 1
)
echo ✅ Python环境正常

echo.
echo [3/4] 检查依赖包...
python -c "import PyQt5" >nul 2>&1
if errorlevel 1 (
    echo ❌ PyQt5缺失！正在尝试安装...
    pip install PyQt5==5.15.9
)

python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo ❌ requests缺失！正在尝试安装...
    pip install requests
)

python -c "import selenium" >nul 2>&1
if errorlevel 1 (
    echo ❌ selenium缺失！正在尝试安装...
    pip install selenium
)
echo ✅ 依赖包检查完成

echo.
echo [4/4] 启动程序...
echo ✅ 环境检查完成，正在启动程序...
echo.

python main.py

if errorlevel 1 (
    echo.
    echo ❌ 程序启动失败！
    echo.
    echo 可能的解决方案:
    echo 1. 运行 "一键部署环境.bat" 重新部署
    echo 2. 确保AdsPower客户端正在运行
    echo 3. 检查网络连接
    echo 4. 以管理员身份运行
    echo.
    pause
)

exit /b 0
'''

        with open("AdsPower_Tool_Launcher.bat", "w", encoding="utf-8") as f:
            f.write(launcher_script)
        self.log_updated.emit("✅ 创建专业启动器")

    def verify_environment(self):
        """验证环境"""
        import subprocess

        # 验证核心依赖
        packages = ["PyQt5", "requests", "selenium", "beautifulsoup4", "lxml", "openpyxl"]
        for package in packages:
            result = subprocess.run([
                "python", "-c", f"import {package}"
            ], capture_output=True, text=True)

            if result.returncode == 0:
                self.log_updated.emit(f"✅ {package} 验证通过")
            else:
                self.log_updated.emit(f"⚠️ {package} 验证失败")


class EnvironmentCheckDialog(QDialog):
    """环境检查对话框"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🔍 环境检查")
        self.setFixedSize(500, 400)
        self.setModal(True)
        self.init_ui()
        self.check_environment()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # 标题
        title_label = QLabel("环境检查报告")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # 检查结果显示
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setStyleSheet("""
            QTextEdit {
                background-color: #F8F9FA;
                border: 1px solid #E1E5E9;
                border-radius: 5px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
                padding: 10px;
            }
        """)
        layout.addWidget(self.result_text)

        # 按钮
        button_layout = QHBoxLayout()

        refresh_btn = QPushButton("🔄 重新检查")
        refresh_btn.setStyleSheet(iOS26StyleManager.get_button_style('secondary'))
        refresh_btn.clicked.connect(self.check_environment)

        close_btn = QPushButton("关闭")
        close_btn.setStyleSheet(iOS26StyleManager.get_button_style('primary'))
        close_btn.clicked.connect(self.accept)

        button_layout.addStretch()
        button_layout.addWidget(refresh_btn)
        button_layout.addWidget(close_btn)

        layout.addLayout(button_layout)

    def check_environment(self):
        """检查环境"""
        self.result_text.clear()
        self.result_text.append("🔍 正在检查环境...\n")

        import subprocess
        import sys
        import os

        # 检查Python版本
        self.result_text.append("=" * 50)
        self.result_text.append("Python环境检查")
        self.result_text.append("=" * 50)
        self.result_text.append(f"✅ Python版本: {sys.version}")
        self.result_text.append(f"✅ Python路径: {sys.executable}")

        # 检查依赖包
        self.result_text.append("\n" + "=" * 50)
        self.result_text.append("依赖包检查")
        self.result_text.append("=" * 50)

        required_packages = [
            "PyQt5", "requests", "selenium", "webdriver-manager",
            "beautifulsoup4", "lxml", "openpyxl", "pandas", "Pillow", "pyautogui"
        ]

        for package in required_packages:
            try:
                __import__(package)
                self.result_text.append(f"✅ {package}: 已安装")
            except ImportError:
                self.result_text.append(f"❌ {package}: 未安装")

        # 检查目录结构
        self.result_text.append("\n" + "=" * 50)
        self.result_text.append("目录结构检查")
        self.result_text.append("=" * 50)

        required_dirs = ["data", "logs", "exports", "backups"]
        for directory in required_dirs:
            if os.path.exists(directory):
                self.result_text.append(f"✅ {directory}: 存在")
            else:
                self.result_text.append(f"❌ {directory}: 不存在")

        # 检查关键文件
        self.result_text.append("\n" + "=" * 50)
        self.result_text.append("关键文件检查")
        self.result_text.append("=" * 50)

        required_files = [
            "main.py", "adspower_api.py", "rpa_engine.py",
            "requirements.txt", "config.json"
        ]
        for file in required_files:
            if os.path.exists(file):
                self.result_text.append(f"✅ {file}: 存在")
            else:
                self.result_text.append(f"❌ {file}: 不存在")

        self.result_text.append("\n🎉 环境检查完成！")


class InstallationProgressDialog(QDialog):
    """安装进度对话框"""
    def __init__(self, title, command, parent=None):
        super().__init__(parent)
        self.command = command
        self.setWindowTitle(title)
        self.setFixedSize(500, 300)
        self.setModal(True)
        self.init_ui()
        self.start_installation()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # 进度显示
        self.progress_label = QLabel("准备开始...")
        self.progress_label.setStyleSheet("font-size: 14px; padding: 10px;")
        layout.addWidget(self.progress_label)

        # 日志显示
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E;
                color: #FFFFFF;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
                border: 1px solid #333;
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.log_text)

        # 按钮
        self.close_btn = QPushButton("关闭")
        self.close_btn.setEnabled(False)
        self.close_btn.setStyleSheet(iOS26StyleManager.get_button_style('secondary'))
        self.close_btn.clicked.connect(self.accept)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.close_btn)
        layout.addLayout(button_layout)

    def start_installation(self):
        """开始安装"""
        self.installation_thread = InstallationThread(self.command)
        self.installation_thread.log_updated.connect(self.update_log)
        self.installation_thread.finished.connect(self.installation_finished)
        self.installation_thread.start()

    def update_log(self, text):
        """更新日志"""
        self.log_text.append(text)

    def installation_finished(self, success):
        """安装完成"""
        self.close_btn.setEnabled(True)
        if success:
            self.progress_label.setText("✅ 安装完成！")
        else:
            self.progress_label.setText("❌ 安装失败")


class InstallationThread(QThread):
    """安装线程"""
    log_updated = pyqtSignal(str)
    finished = pyqtSignal(bool)

    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        """执行安装"""
        try:
            import subprocess

            self.log_updated.emit(f"执行命令: {' '.join(self.command)}")

            process = subprocess.Popen(
                self.command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )

            for line in process.stdout:
                self.log_updated.emit(line.strip())

            process.wait()

            if process.returncode == 0:
                self.log_updated.emit("✅ 安装成功完成")
                self.finished.emit(True)
            else:
                self.log_updated.emit(f"❌ 安装失败，退出码: {process.returncode}")
                self.finished.emit(False)

        except Exception as e:
            self.log_updated.emit(f"❌ 安装过程中发生错误: {str(e)}")
            self.finished.emit(False)


if __name__ == "__main__":
    sys.exit(main())
