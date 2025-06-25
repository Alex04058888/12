#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AdsPower工具专业版 - RPA批量操作对话框
提供RPA批量操作浏览器的用户界面
"""

import sys
import os
import json
import time
from datetime import datetime
from typing import List, Dict, Any

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QGridLayout,
                           QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox,
                           QSpinBox, QCheckBox, QProgressBar, QTableWidget, 
                           QTableWidgetItem, QHeaderView, QGroupBox, QTabWidget,
                           QWidget, QSplitter, QMessageBox, QFileDialog,
                           QApplication, QFrame)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt5.QtGui import QFont, QIcon

# 导入样式管理器
try:
    from adspower_style_manager import AdsPowerStyleManager as iOS26StyleManager
except ImportError:
    class iOS26StyleManager:
        @staticmethod
        def get_complete_style():
            return ""

class RPABatchDialog(QDialog):
    """RPA批量操作对话框"""
    
    # 信号定义
    task_started = pyqtSignal(str)  # 任务开始
    task_progress = pyqtSignal(str, int, str)  # 任务进度
    task_completed = pyqtSignal(str, str, dict)  # 任务完成
    
    def __init__(self, parent=None, selected_profiles=None):
        super().__init__(parent)
        self.selected_profiles = selected_profiles or []
        self.current_task_id = None
        self.batch_manager = None
        
        # 初始化批量管理器
        try:
            from rpa_batch_manager import rpa_batch_manager
            self.batch_manager = rpa_batch_manager
        except ImportError:
            QMessageBox.critical(self, "错误", "RPA批量管理器不可用")
            return
        
        self.init_ui()
        self.setup_connections()
        self.load_flow_templates()
        
        # 定时器用于更新任务状态
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_task_status)
        self.status_timer.start(1000)  # 每秒更新一次
    
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("RPA批量操作")
        self.setModal(True)
        
        # 响应式窗口大小
        screen = QApplication.desktop().screenGeometry()
        dialog_width = min(1200, int(screen.width() * 0.8))
        dialog_height = min(800, int(screen.height() * 0.8))
        self.resize(dialog_width, dialog_height)
        
        # 应用样式
        self.setStyleSheet(iOS26StyleManager.get_complete_style())
        
        # 主布局
        main_layout = QVBoxLayout(self)
        
        # 创建选项卡
        tab_widget = QTabWidget()
        
        # 批量配置选项卡
        config_tab = self.create_config_tab()
        tab_widget.addTab(config_tab, "📋 批量配置")
        
        # 执行监控选项卡
        monitor_tab = self.create_monitor_tab()
        tab_widget.addTab(monitor_tab, "📊 执行监控")
        
        # 结果查看选项卡
        results_tab = self.create_results_tab()
        tab_widget.addTab(results_tab, "📈 结果查看")
        
        main_layout.addWidget(tab_widget)
        
        # 底部按钮
        button_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("🚀 开始批量执行")
        self.start_btn.setMinimumHeight(40)
        self.start_btn.clicked.connect(self.start_batch_execution)
        
        self.cancel_btn = QPushButton("⏹️ 取消执行")
        self.cancel_btn.setMinimumHeight(40)
        self.cancel_btn.setEnabled(False)
        self.cancel_btn.clicked.connect(self.cancel_batch_execution)
        
        self.close_btn = QPushButton("❌ 关闭")
        self.close_btn.setMinimumHeight(40)
        self.close_btn.clicked.connect(self.close)
        
        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.cancel_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.close_btn)
        
        main_layout.addLayout(button_layout)
    
    def create_config_tab(self) -> QWidget:
        """创建批量配置选项卡"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 环境信息组
        env_group = QGroupBox("📁 选中的环境")
        env_layout = QVBoxLayout(env_group)
        
        self.env_info_label = QLabel(f"已选择 {len(self.selected_profiles)} 个环境")
        self.env_info_label.setStyleSheet("font-weight: bold; color: #1890ff;")
        env_layout.addWidget(self.env_info_label)
        
        # 环境列表（简化显示）
        env_text = QTextEdit()
        env_text.setMaximumHeight(100)
        env_text.setPlainText("\n".join(self.selected_profiles[:10]))
        if len(self.selected_profiles) > 10:
            env_text.append(f"... 还有 {len(self.selected_profiles) - 10} 个环境")
        env_text.setReadOnly(True)
        env_layout.addWidget(env_text)
        
        layout.addWidget(env_group)
        
        # 执行配置组
        config_group = QGroupBox("⚙️ 执行配置")
        config_layout = QGridLayout(config_group)
        
        # 执行模式
        config_layout.addWidget(QLabel("执行模式:"), 0, 0)
        self.execution_mode_combo = QComboBox()
        self.execution_mode_combo.addItems(["顺序执行", "并行执行", "随机执行"])
        config_layout.addWidget(self.execution_mode_combo, 0, 1)
        
        # 并行数量
        config_layout.addWidget(QLabel("并行数量:"), 1, 0)
        self.parallel_count_spin = QSpinBox()
        self.parallel_count_spin.setRange(1, 10)
        self.parallel_count_spin.setValue(3)
        config_layout.addWidget(self.parallel_count_spin, 1, 1)
        
        # 环境间延迟
        config_layout.addWidget(QLabel("环境间延迟(秒):"), 2, 0)
        self.delay_spin = QSpinBox()
        self.delay_spin.setRange(0, 60)
        self.delay_spin.setValue(1)
        config_layout.addWidget(self.delay_spin, 2, 1)
        
        # 错误处理
        config_layout.addWidget(QLabel("错误处理:"), 3, 0)
        self.error_handling_combo = QComboBox()
        self.error_handling_combo.addItems(["继续执行", "停止执行", "跳过错误"])
        config_layout.addWidget(self.error_handling_combo, 3, 1)
        
        layout.addWidget(config_group)
        
        # RPA流程组
        flow_group = QGroupBox("🤖 RPA流程")
        flow_layout = QVBoxLayout(flow_group)
        
        # 流程选择
        flow_select_layout = QHBoxLayout()
        flow_select_layout.addWidget(QLabel("选择流程:"))
        
        self.flow_template_combo = QComboBox()
        self.flow_template_combo.addItem("请选择流程模板...")
        flow_select_layout.addWidget(self.flow_template_combo)
        
        load_flow_btn = QPushButton("📂 加载流程文件")
        load_flow_btn.clicked.connect(self.load_flow_file)
        flow_select_layout.addWidget(load_flow_btn)
        
        flow_layout.addLayout(flow_select_layout)
        
        # 流程预览
        self.flow_preview = QTextEdit()
        self.flow_preview.setMaximumHeight(150)
        self.flow_preview.setPlaceholderText("流程内容将在这里显示...")
        self.flow_preview.setReadOnly(True)
        flow_layout.addWidget(self.flow_preview)
        
        layout.addWidget(flow_group)
        
        return tab
    
    def create_monitor_tab(self) -> QWidget:
        """创建执行监控选项卡"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 总体进度组
        progress_group = QGroupBox("📊 执行进度")
        progress_layout = QVBoxLayout(progress_group)
        
        # 总体进度条
        self.overall_progress = QProgressBar()
        self.overall_progress.setTextVisible(True)
        progress_layout.addWidget(self.overall_progress)
        
        # 状态信息
        status_layout = QGridLayout()
        
        self.status_label = QLabel("状态: 等待开始")
        status_layout.addWidget(self.status_label, 0, 0)
        
        self.current_env_label = QLabel("当前环境: -")
        status_layout.addWidget(self.current_env_label, 0, 1)
        
        self.success_count_label = QLabel("成功: 0")
        status_layout.addWidget(self.success_count_label, 1, 0)
        
        self.failed_count_label = QLabel("失败: 0")
        status_layout.addWidget(self.failed_count_label, 1, 1)
        
        progress_layout.addLayout(status_layout)
        layout.addWidget(progress_group)
        
        # 实时日志组
        log_group = QGroupBox("📝 执行日志")
        log_layout = QVBoxLayout(log_group)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Consolas", 9))
        log_layout.addWidget(self.log_text)
        
        # 日志控制按钮
        log_control_layout = QHBoxLayout()
        
        clear_log_btn = QPushButton("🗑️ 清空日志")
        clear_log_btn.clicked.connect(self.log_text.clear)
        log_control_layout.addWidget(clear_log_btn)
        
        save_log_btn = QPushButton("💾 保存日志")
        save_log_btn.clicked.connect(self.save_log)
        log_control_layout.addWidget(save_log_btn)
        
        log_control_layout.addStretch()
        log_layout.addLayout(log_control_layout)
        
        layout.addWidget(log_group)
        
        return tab
    
    def create_results_tab(self) -> QWidget:
        """创建结果查看选项卡"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 结果统计组
        stats_group = QGroupBox("📈 执行统计")
        stats_layout = QGridLayout(stats_group)
        
        self.total_envs_label = QLabel("总环境数: 0")
        stats_layout.addWidget(self.total_envs_label, 0, 0)
        
        self.success_rate_label = QLabel("成功率: 0%")
        stats_layout.addWidget(self.success_rate_label, 0, 1)
        
        self.execution_time_label = QLabel("执行时间: -")
        stats_layout.addWidget(self.execution_time_label, 1, 0)
        
        self.avg_time_label = QLabel("平均时间: -")
        stats_layout.addWidget(self.avg_time_label, 1, 1)
        
        layout.addWidget(stats_group)
        
        # 详细结果表格
        results_group = QGroupBox("📋 详细结果")
        results_layout = QVBoxLayout(results_group)
        
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(4)
        self.results_table.setHorizontalHeaderLabels(["环境ID", "状态", "执行时间", "错误信息"])
        
        # 设置表格样式
        header = self.results_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        
        results_layout.addWidget(self.results_table)
        
        # 结果操作按钮
        results_control_layout = QHBoxLayout()
        
        export_results_btn = QPushButton("📤 导出结果")
        export_results_btn.clicked.connect(self.export_results)
        results_control_layout.addWidget(export_results_btn)
        
        retry_failed_btn = QPushButton("🔄 重试失败")
        retry_failed_btn.clicked.connect(self.retry_failed_envs)
        results_control_layout.addWidget(retry_failed_btn)
        
        results_control_layout.addStretch()
        results_layout.addLayout(results_control_layout)
        
        layout.addWidget(results_group)
        
        return tab

    def setup_connections(self):
        """设置信号连接"""
        self.task_started.connect(self.on_task_started)
        self.task_progress.connect(self.on_task_progress)
        self.task_completed.connect(self.on_task_completed)

        # 执行模式变化时启用/禁用并行数量
        self.execution_mode_combo.currentTextChanged.connect(self.on_execution_mode_changed)

        # 流程模板选择
        self.flow_template_combo.currentTextChanged.connect(self.on_flow_template_changed)

    def on_execution_mode_changed(self, mode_text):
        """执行模式变化处理"""
        self.parallel_count_spin.setEnabled(mode_text == "并行执行")

    def load_flow_templates(self):
        """加载流程模板"""
        # 这里可以从文件或数据库加载流程模板
        templates = [
            "基础网页操作",
            "数据采集流程",
            "表单填写流程",
            "页面截图流程"
        ]

        for template in templates:
            self.flow_template_combo.addItem(template)

    def on_flow_template_changed(self, template_name):
        """流程模板选择变化"""
        if template_name and template_name != "请选择流程模板...":
            # 加载模板内容
            template_content = self.get_template_content(template_name)
            self.flow_preview.setPlainText(template_content)

    def get_template_content(self, template_name):
        """获取模板内容"""
        templates = {
            "基础网页操作": json.dumps({
                "name": "基础网页操作",
                "steps": [
                    {"action": "navigate", "url": "https://example.com"},
                    {"action": "wait", "seconds": 2},
                    {"action": "click", "selector": {"type": "id", "value": "button"}},
                    {"action": "input", "selector": {"type": "name", "value": "input"}, "text": "测试文本"}
                ]
            }, ensure_ascii=False, indent=2),

            "数据采集流程": json.dumps({
                "name": "数据采集流程",
                "steps": [
                    {"action": "navigate", "url": "https://example.com/data"},
                    {"action": "wait_for_element", "selector": {"type": "class", "value": "data-item"}},
                    {"action": "extract_text", "selector": {"type": "class", "value": "title"}, "save_to": "title"},
                    {"action": "extract_text", "selector": {"type": "class", "value": "content"}, "save_to": "content"}
                ]
            }, ensure_ascii=False, indent=2),

            "表单填写流程": json.dumps({
                "name": "表单填写流程",
                "steps": [
                    {"action": "navigate", "url": "https://example.com/form"},
                    {"action": "input", "selector": {"type": "name", "value": "username"}, "text": "{{username}}"},
                    {"action": "input", "selector": {"type": "name", "value": "email"}, "text": "{{email}}"},
                    {"action": "click", "selector": {"type": "id", "value": "submit"}}
                ]
            }, ensure_ascii=False, indent=2),

            "页面截图流程": json.dumps({
                "name": "页面截图流程",
                "steps": [
                    {"action": "navigate", "url": "{{target_url}}"},
                    {"action": "wait", "seconds": 3},
                    {"action": "screenshot", "filename": "{{env_id}}_screenshot.png"},
                    {"action": "scroll", "direction": "down", "pixels": 500},
                    {"action": "screenshot", "filename": "{{env_id}}_screenshot_2.png"}
                ]
            }, ensure_ascii=False, indent=2)
        }

        return templates.get(template_name, "")

    def load_flow_file(self):
        """加载流程文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择RPA流程文件", "", "JSON文件 (*.json);;所有文件 (*)"
        )

        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    flow_content = f.read()

                # 验证JSON格式
                json.loads(flow_content)

                self.flow_preview.setPlainText(flow_content)
                self.log_message(f"✅ 成功加载流程文件: {file_path}")

            except Exception as e:
                QMessageBox.critical(self, "错误", f"加载流程文件失败: {str(e)}")

    def start_batch_execution(self):
        """开始批量执行"""
        if not self.selected_profiles:
            QMessageBox.warning(self, "警告", "没有选择要执行的环境")
            return

        # 获取流程数据
        flow_text = self.flow_preview.toPlainText().strip()
        if not flow_text:
            QMessageBox.warning(self, "警告", "请选择或加载RPA流程")
            return

        try:
            flow_data = json.loads(flow_text)
        except json.JSONDecodeError as e:
            QMessageBox.critical(self, "错误", f"流程格式错误: {str(e)}")
            return

        # 获取执行配置
        execution_mode_map = {
            "顺序执行": "sequential",
            "并行执行": "parallel",
            "随机执行": "random"
        }

        execution_mode = execution_mode_map[self.execution_mode_combo.currentText()]
        max_parallel = self.parallel_count_spin.value()

        # 创建批量任务
        try:
            from rpa_batch_manager import BatchExecutionMode
            mode_map = {
                "sequential": BatchExecutionMode.SEQUENTIAL,
                "parallel": BatchExecutionMode.PARALLEL,
                "random": BatchExecutionMode.RANDOM
            }

            self.current_task_id = self.batch_manager.create_batch_task(
                env_ids=self.selected_profiles,
                flow_data=flow_data,
                execution_mode=mode_map[execution_mode],
                max_parallel=max_parallel
            )
        except Exception as e:
            QMessageBox.critical(self, "错误", f"创建批量任务失败: {str(e)}")
            return

        # 启动任务
        success = self.batch_manager.start_batch_task(
            task_id=self.current_task_id,
            progress_callback=self.on_progress_update,
            completion_callback=self.on_completion_update
        )

        if success:
            self.start_btn.setEnabled(False)
            self.cancel_btn.setEnabled(True)
            self.log_message(f"🚀 开始批量执行，任务ID: {self.current_task_id}")
            self.log_message(f"📋 执行模式: {self.execution_mode_combo.currentText()}")
            self.log_message(f"🎯 目标环境: {len(self.selected_profiles)} 个")
        else:
            QMessageBox.critical(self, "错误", "启动批量任务失败")

    def cancel_batch_execution(self):
        """取消批量执行"""
        if self.current_task_id:
            success = self.batch_manager.cancel_batch_task(self.current_task_id)
            if success:
                self.log_message(f"⏹️ 已取消批量任务: {self.current_task_id}")
                self.start_btn.setEnabled(True)
                self.cancel_btn.setEnabled(False)

    def on_progress_update(self, task_id, progress, current_env):
        """进度更新回调"""
        self.task_progress.emit(task_id, progress, current_env)

    def on_completion_update(self, task_id, status, results):
        """完成更新回调"""
        self.task_completed.emit(task_id, status, results)

    def on_task_started(self, task_id):
        """任务开始处理"""
        self.log_message(f"✅ 任务开始: {task_id}")

    def on_task_progress(self, task_id, progress, current_env):
        """任务进度处理"""
        self.overall_progress.setValue(progress)
        self.current_env_label.setText(f"当前环境: {current_env}")

        # 更新状态标签
        if progress < 100:
            self.status_label.setText(f"状态: 执行中 ({progress}%)")

        self.log_message(f"📊 进度更新: {progress}% - 当前环境: {current_env}")

    def on_task_completed(self, task_id, status, results):
        """任务完成处理"""
        self.start_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)

        self.status_label.setText(f"状态: {status}")
        self.log_message(f"🎉 任务完成: {task_id} - 状态: {status}")

        # 更新结果表格
        self.update_results_table(results)

    def update_task_status(self):
        """更新任务状态"""
        if not self.current_task_id:
            return

        status = self.batch_manager.get_task_status(self.current_task_id)
        if not status:
            return

        # 更新统计信息
        self.success_count_label.setText(f"成功: {status['success_count']}")
        self.failed_count_label.setText(f"失败: {status['failed_count']}")

        # 更新总体统计
        self.total_envs_label.setText(f"总环境数: {status['total_envs']}")

        if status['total_envs'] > 0:
            success_rate = (status['success_count'] / status['total_envs']) * 100
            self.success_rate_label.setText(f"成功率: {success_rate:.1f}%")

    def update_results_table(self, results):
        """更新结果表格"""
        self.results_table.setRowCount(len(results))

        for row, (env_id, result) in enumerate(results.items()):
            # 环境ID
            self.results_table.setItem(row, 0, QTableWidgetItem(env_id))

            # 状态
            status = "✅ 成功" if result.get("success", False) else "❌ 失败"
            self.results_table.setItem(row, 1, QTableWidgetItem(status))

            # 执行时间（模拟）
            exec_time = f"{result.get('duration', 0):.1f}s"
            self.results_table.setItem(row, 2, QTableWidgetItem(exec_time))

            # 错误信息
            error_msg = result.get("error", "") if not result.get("success", False) else ""
            self.results_table.setItem(row, 3, QTableWidgetItem(error_msg))

    def log_message(self, message):
        """添加日志消息"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        self.log_text.append(formatted_message)

        # 自动滚动到底部
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def save_log(self):
        """保存日志"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存执行日志", f"rpa_batch_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            "文本文件 (*.txt);;所有文件 (*)"
        )

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.log_text.toPlainText())
                QMessageBox.information(self, "成功", f"日志已保存到: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"保存日志失败: {str(e)}")

    def export_results(self):
        """导出执行结果"""
        if not self.current_task_id:
            QMessageBox.warning(self, "警告", "没有可导出的结果")
            return

        results = self.batch_manager.get_task_results(self.current_task_id)
        if not results:
            QMessageBox.warning(self, "警告", "获取结果失败")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出执行结果", f"rpa_batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            "JSON文件 (*.json);;所有文件 (*)"
        )

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(results, f, ensure_ascii=False, indent=2)
                QMessageBox.information(self, "成功", f"结果已导出到: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"导出结果失败: {str(e)}")

    def retry_failed_envs(self):
        """重试失败的环境"""
        if not self.current_task_id:
            QMessageBox.warning(self, "警告", "没有可重试的任务")
            return

        results = self.batch_manager.get_task_results(self.current_task_id)
        if not results:
            return

        # 获取失败的环境ID
        failed_envs = [
            env_id for env_id, result in results["results"].items()
            if not result.get("success", False)
        ]

        if not failed_envs:
            QMessageBox.information(self, "提示", "没有失败的环境需要重试")
            return

        reply = QMessageBox.question(
            self, "确认重试",
            f"确定要重试 {len(failed_envs)} 个失败的环境吗？",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # 使用失败的环境创建新任务
            flow_text = self.flow_preview.toPlainText().strip()
            if flow_text:
                try:
                    flow_data = json.loads(flow_text)

                    from rpa_batch_manager import BatchExecutionMode

                    # 创建重试任务
                    retry_task_id = self.batch_manager.create_batch_task(
                        env_ids=failed_envs,
                        flow_data=flow_data,
                        execution_mode=BatchExecutionMode.SEQUENTIAL
                    )

                    # 启动重试任务
                    success = self.batch_manager.start_batch_task(
                        task_id=retry_task_id,
                        progress_callback=self.on_progress_update,
                        completion_callback=self.on_completion_update
                    )

                    if success:
                        self.current_task_id = retry_task_id
                        self.start_btn.setEnabled(False)
                        self.cancel_btn.setEnabled(True)
                        self.log_message(f"🔄 开始重试失败环境，任务ID: {retry_task_id}")

                except Exception as e:
                    QMessageBox.critical(self, "错误", f"重试失败: {str(e)}")

    def closeEvent(self, event):
        """关闭事件处理"""
        if self.current_task_id and self.cancel_btn.isEnabled():
            reply = QMessageBox.question(
                self, "确认关闭",
                "批量任务正在执行中，确定要关闭对话框吗？\n任务将在后台继续执行。",
                QMessageBox.Yes | QMessageBox.No
            )

            if reply != QMessageBox.Yes:
                event.ignore()
                return

        # 停止状态更新定时器
        if hasattr(self, 'status_timer'):
            self.status_timer.stop()

        event.accept()


# 测试代码
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 模拟选中的环境
    test_profiles = ["env_001", "env_002", "env_003", "env_004", "env_005"]

    dialog = RPABatchDialog(selected_profiles=test_profiles)
    dialog.show()

    sys.exit(app.exec_())
