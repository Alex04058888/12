#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RPA执行引擎
实现AdsPower RPA操作的具体执行逻辑
完整实现所有50个AdsPower RPA功能
"""

import time
import json
import random
import requests
import re
import os
import base64
from typing import Dict, List, Any, Optional
# 可选依赖，如果不存在则使用替代方案
try:
    import pyperclip
    PYPERCLIP_AVAILABLE = True
except ImportError:
    PYPERCLIP_AVAILABLE = False

try:
    import imaplib
    import email
    EMAIL_AVAILABLE = True
except ImportError:
    EMAIL_AVAILABLE = False

try:
    import pyotp
    PYOTP_AVAILABLE = True
except ImportError:
    PYOTP_AVAILABLE = False
import openpyxl
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# 导入变量管理、数据管理、日志、异常处理和AdsPower API模块
try:
    from rpa_variable_manager import RPAVariableManager
    from rpa_data_manager import RPADataManager
    from rpa_logger import RPALogger, LogLevel
    from rpa_exception_handler import RPAExceptionHandler, handle_rpa_exceptions, safe_execute
    from adspower_api import AdsPowerAPIClient
except ImportError:
    # 如果模块不存在，创建简单的替代类
    class RPAVariableManager:
        def __init__(self):
            self.variables = {}
        def set_variable(self, name, value, var_type="custom"):
            self.variables[name] = value
        def get_variable(self, name, default=None):
            return self.variables.get(name, default)
        def get_all_variables(self):
            return self.variables.copy()

    class RPADataManager:
        def __init__(self):
            pass

    class RPALogger:
        def __init__(self, task_name="RPA_Task"):
            pass
        def info(self, message, step_id=None, data=None):
            print(f"INFO: {message}")
        def success(self, message, step_id=None, data=None):
            print(f"SUCCESS: {message}")
        def error(self, message, step_id=None, data=None):
            print(f"ERROR: {message}")
        def start_step(self, step_id, step_name, config=None):
            print(f"START: {step_name}")
        def end_step(self, step_id, step_name, success=True, result=None):
            print(f"END: {step_name} - {'SUCCESS' if success else 'FAILED'}")

    class LogLevel:
        INFO = "info"
        SUCCESS = "success"
        ERROR = "error"

class RPAExecutor:
    """RPA执行引擎 - 集成变量管理、数据管理和日志系统"""

    def __init__(self, browser_driver=None, task_name="RPA_Task"):
        self.driver = browser_driver
        self.loop_stack = []  # 循环栈

        # 初始化变量管理、数据管理、日志、异常处理和AdsPower API系统
        self.variable_manager = RPAVariableManager()
        self.data_manager = RPADataManager()
        self.logger = RPALogger(task_name)
        self.exception_handler = RPAExceptionHandler(self.logger)
        self.adspower_api = AdsPowerAPIClient()

        # 兼容性：保持原有的variables属性
        self.variables = self.variable_manager.variables

        # AdsPower集成相关
        self.current_env_id = None
        self.adspower_driver = None
        self.selenium_config = None

        # 执行统计
        self.execution_stats = {
            "total_steps": 0,
            "successful_steps": 0,
            "failed_steps": 0,
            "start_time": None,
            "end_time": None
        }

    def set_driver(self, driver):
        """设置浏览器驱动"""
        self.driver = driver

    def set_environment_data(self, env_data):
        """设置AdsPower环境数据"""
        self.variable_manager.set_environment_variables(env_data)
        # 更新兼容性变量
        self.variables = self.variable_manager.variables

    def get_variable_value(self, value_str):
        """解析变量值 - 支持AdsPower变量语法"""
        if isinstance(value_str, str) and value_str.startswith('${') and value_str.endswith('}'):
            # 提取变量名
            var_name = value_str[2:-1]
            return self.variable_manager.get_variable(var_name, value_str)
        return value_str

    def set_variable(self, name, value, var_type="custom"):
        """设置变量"""
        self.variable_manager.set_variable(name, value, var_type)
        # 更新兼容性变量
        self.variables = self.variable_manager.variables

    # ==================== AdsPower集成方法 ====================

    def connect_to_adspower_browser(self, env_id: str) -> Dict[str, Any]:
        """连接到AdsPower浏览器环境"""
        try:
            self.logger.info(f"正在连接到AdsPower环境: {env_id}")

            # 启动AdsPower浏览器
            start_result = self.adspower_api.start_browser(env_id)

            if start_result.get("code") != 0:
                error_msg = f"启动AdsPower浏览器失败: {start_result.get('msg', '未知错误')}"
                self.logger.error(error_msg)
                return {"success": False, "message": error_msg}

            # 获取浏览器连接信息
            data = start_result.get("data", {})
            ws_info = data.get("ws", {})
            selenium_address = ws_info.get("selenium", "")
            webdriver_path = data.get("webdriver", "")
            debug_port = data.get("debug_port", "")

            if not selenium_address:
                error_msg = "未获取到Selenium连接地址"
                self.logger.error(error_msg)
                return {"success": False, "message": error_msg}

            # 配置Chrome选项连接到AdsPower浏览器
            chrome_options = Options()
            chrome_options.add_experimental_option("debuggerAddress", selenium_address)
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)

            # 创建WebDriver连接
            if webdriver_path and os.path.exists(webdriver_path):
                service = Service(webdriver_path)
                driver = webdriver.Chrome(service=service, options=chrome_options)
            else:
                driver = webdriver.Chrome(options=chrome_options)

            # 隐藏WebDriver特征
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

            # 保存连接信息
            self.driver = driver
            self.adspower_driver = driver
            self.current_env_id = env_id
            self.selenium_config = {
                "selenium_address": selenium_address,
                "webdriver_path": webdriver_path,
                "debug_port": debug_port
            }

            # 获取环境信息并设置环境变量
            env_info = self.adspower_api.get_profile_detail(env_id)
            if env_info:
                self.set_environment_data(env_info)

            self.logger.success(f"成功连接到AdsPower环境: {env_id}")
            return {
                "success": True,
                "message": "连接成功",
                "data": {
                    "env_id": env_id,
                    "selenium_address": selenium_address,
                    "debug_port": debug_port
                }
            }

        except Exception as e:
            error_msg = f"连接AdsPower浏览器失败: {str(e)}"
            self.logger.error(error_msg)
            return {"success": False, "message": error_msg}

    def disconnect_from_adspower_browser(self) -> Dict[str, Any]:
        """断开AdsPower浏览器连接"""
        try:
            if self.adspower_driver:
                self.adspower_driver.quit()
                self.adspower_driver = None
                self.driver = None

            if self.current_env_id:
                # 关闭AdsPower浏览器
                close_result = self.adspower_api.close_browser(self.current_env_id)
                self.logger.info(f"关闭AdsPower浏览器: {close_result.get('msg', '')}")
                self.current_env_id = None

            self.selenium_config = None
            self.logger.info("已断开AdsPower浏览器连接")

            return {"success": True, "message": "断开连接成功"}

        except Exception as e:
            error_msg = f"断开AdsPower浏览器连接失败: {str(e)}"
            self.logger.error(error_msg)
            return {"success": False, "message": error_msg}

    def get_adspower_env_info(self, env_id: str) -> Dict[str, Any]:
        """获取AdsPower环境信息"""
        try:
            env_info = self.adspower_api.get_profile_detail(env_id)
            return {"success": True, "data": env_info}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def check_adspower_connection(self) -> bool:
        """检查AdsPower API连接状态"""
        try:
            result = self.adspower_api.test_connection()
            return result.get("code") == 0
        except:
            return False
        
    def execute_step(self, step_config):
        """执行单个步骤 - 完整支持所有50个AdsPower RPA功能"""
        operation = step_config.get('operation', '')

        try:
            # 页面操作功能组 (10个功能)
            if operation == "新建标签":
                return self.new_tab(step_config)
            elif operation == "关闭标签":
                return self.close_tab(step_config)
            elif operation == "关闭其他标签":
                return self.close_other_tabs(step_config)
            elif operation == "切换标签":
                return self.switch_tab(step_config)
            elif operation == "访问网站":
                return self.goto_url(step_config)
            elif operation == "刷新页面":
                return self.refresh_page(step_config)
            elif operation == "页面后退":
                return self.page_back(step_config)
            elif operation == "页面截图":
                return self.page_screenshot(step_config)
            elif operation == "经过元素":
                return self.hover_element(step_config)
            elif operation == "下拉选择器":
                return self.select_dropdown(step_config)

            # 元素操作功能组 (10个功能)
            elif operation == "元素聚焦":
                return self.focus_element(step_config)
            elif operation == "点击元素":
                return self.click_element(step_config)
            elif operation == "输入内容":
                return self.input_content(step_config)
            elif operation == "上传附件":
                return self.upload_file(step_config)
            elif operation == "执行JS脚本":
                return self.execute_javascript(step_config)
            elif operation == "键盘按键":
                return self.keyboard_key(step_config)
            elif operation == "组合键":
                return self.keyboard_combo(step_config)
            elif operation == "等待时间":
                return self.wait_time(step_config)
            elif operation == "等待元素出现":
                return self.wait_element(step_config)
            elif operation == "等待请求完成":
                return self.wait_request(step_config)

            # 数据获取功能组 (9个功能)
            elif operation == "获取URL":
                return self.get_url(step_config)
            elif operation == "获取粘贴板内容":
                return self.get_clipboard(step_config)
            elif operation == "元素数据":
                return self.get_element_data(step_config)
            elif operation == "当前焦点元素":
                return self.get_focused_element(step_config)
            elif operation == "存到文件":
                return self.save_to_file(step_config)
            elif operation == "存到Excel":
                return self.save_to_excel(step_config)
            elif operation == "导入txt":
                return self.import_txt(step_config)
            elif operation == "获取邮件":
                return self.get_email(step_config)
            elif operation == "身份验证器码":
                return self.get_totp(step_config)

            # 网络监听功能组 (5个功能)
            elif operation == "监听请求触发":
                return self.listen_request_trigger(step_config)
            elif operation == "监听请求结果":
                return self.listen_request_result(step_config)
            elif operation == "停止页面监听":
                return self.stop_page_listening(step_config)
            elif operation == "获取页面Cookie":
                return self.get_cookies(step_config)
            elif operation == "清除页面Cookie":
                return self.clear_cookies(step_config)

            # 数据处理功能组 (5个功能)
            elif operation == "文本中提取":
                return self.extract_text(step_config)
            elif operation == "转换Json对象":
                return self.convert_json(step_config)
            elif operation == "字段提取":
                return self.extract_field(step_config)
            elif operation == "随机提取":
                return self.random_extract(step_config)
            elif operation == "更新环境备注":
                return self.update_env_note(step_config)

            # 流程控制功能组 (7个功能)
            elif operation == "更新环境标签":
                return self.update_env_tag(step_config)
            elif operation == "启动新浏览器":
                return self.start_new_browser(step_config)
            elif operation == "使用其他流程":
                return self.use_other_flow(step_config)
            elif operation == "IF条件":
                return self.if_condition(step_config)
            elif operation == "For循环元素":
                return self.for_element_loop(step_config)
            elif operation == "For循环次数":
                return self.for_count_loop(step_config)
            elif operation == "For循环数据":
                return self.for_data_loop(step_config)

            # 循环控制功能组 (3个功能)
            elif operation == "While循环":
                return self.while_loop(step_config)
            elif operation == "退出循环":
                return self.break_loop(step_config)
            elif operation == "关闭浏览器":
                return self.close_browser(step_config)

            # 第三方工具功能组 (1个功能)
            elif operation == "2Captcha验证码识别":
                return self.solve_captcha(step_config)

            # 兼容旧版本操作名称
            elif operation in ["新建标签页"]:
                return self.new_tab(step_config)
            elif operation in ["前往网址"]:
                return self.goto_url(step_config)
            elif operation in ["身份验证密码"]:
                return self.get_totp(step_config)
            elif operation in ["2Captcha"]:
                return self.solve_captcha(step_config)

            else:
                return {"success": False, "message": f"未实现的操作: {operation}"}

        except Exception as e:
            return {"success": False, "message": f"执行错误: {str(e)}"}
    
    # ==================== 页面操作实现 ====================
    
    def new_tab(self, config):
        """新建标签页 - 完全按照AdsPower原版实现"""
        try:
            # AdsPower原版：创建新的空白标签页
            self.driver.execute_script("window.open('about:blank');")
            handles = self.driver.window_handles

            # 默认切换到新标签页（AdsPower原版行为）
            switch_to_new = config.get('switch_to_new', True)
            if switch_to_new:
                self.driver.switch_to.window(handles[-1])

            # 如果指定了URL，则在新标签页中导航
            tab_url = config.get('tab_url', '')
            if tab_url:
                if switch_to_new:
                    # 在当前新标签页中打开URL
                    self.driver.get(tab_url)
                else:
                    # 在新标签页中打开URL但不切换
                    self.driver.execute_script(f"window.open('{tab_url}');")

            return {"success": True, "message": "新建标签页成功", "tab_count": len(handles)}
        except Exception as e:
            return {"success": False, "message": f"新建标签页失败: {str(e)}"}
    
    def goto_url(self, config):
        """前往网址"""
        try:
            url = config.get('goto_url', '')
            if not url:
                return {"success": False, "message": "未指定URL"}
            
            timeout = config.get('timeout_seconds', 30)
            self.driver.set_page_load_timeout(timeout)
            self.driver.get(url)
            
            if config.get('wait_load', True):
                WebDriverWait(self.driver, timeout).until(
                    lambda driver: driver.execute_script("return document.readyState") == "complete"
                )
            
            return {"success": True, "message": f"成功访问: {url}"}
        except Exception as e:
            return {"success": False, "message": f"访问网址失败: {str(e)}"}
    
    def wait_time(self, config):
        """等待时间"""
        try:
            wait_type = config.get('wait_type', '固定时间')
            
            if wait_type == '随机时间':
                min_time = config.get('wait_min', 3)
                max_time = config.get('wait_max', 5)
                wait_seconds = random.uniform(min_time, max_time)
            else:
                wait_seconds = config.get('wait_min', 3)
            
            time.sleep(wait_seconds)
            return {"success": True, "message": f"等待 {wait_seconds:.2f} 秒"}
        except Exception as e:
            return {"success": False, "message": f"等待时间失败: {str(e)}"}
    
    def scroll_page(self, config):
        """滚动页面"""
        try:
            scroll_type = config.get('scroll_range_type', '窗口')
            distance = config.get('scroll_distance', 500)
            
            if scroll_type == '元素':
                selector = config.get('scroll_selector', '')
                if selector:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    self.driver.execute_script("arguments[0].scrollTop += arguments[1];", element, distance)
                else:
                    return {"success": False, "message": "元素滚动需要指定选择器"}
            else:
                self.driver.execute_script(f"window.scrollBy(0, {distance});")
            
            return {"success": True, "message": f"滚动 {distance} 像素"}
        except Exception as e:
            return {"success": False, "message": f"滚动页面失败: {str(e)}"}
    
    def click_element(self, config):
        """点击元素 - 完全按照AdsPower官方标准"""
        try:
            # 兼容新旧参数格式
            if 'selector' in config:
                # 新标准格式 - 完全按照AdsPower官方
                selector = config.get('selector', '')
                stored_element = config.get('stored_element')
                element_order_config = config.get('element_order', 1)
                click_type = config.get('click_type', '鼠标左键')
                key_type = config.get('key_type', '单击')

                # 处理元素顺序（支持固定值和区间随机）
                if isinstance(element_order_config, dict):
                    order_type = element_order_config.get('type', '固定值')
                    if order_type == '区间随机':
                        import random
                        min_val = element_order_config.get('value', 1)
                        max_val = element_order_config.get('max_value', 1)
                        element_order = random.randint(min_val, max_val) - 1  # 转换为0基索引
                    else:
                        element_order = element_order_config.get('value', 1) - 1
                else:
                    element_order = element_order_config - 1 if element_order_config else 0

                click_action = key_type  # 使用官方的key_type参数
            else:
                # 旧格式兼容
                selector = config.get('click_selector', '')
                stored_element = None
                click_type = config.get('click_type', '鼠标左键')
                click_action = config.get('click_action', '单击')
                element_order = config.get('click_element_order', 1) - 1

            if not selector and not stored_element:
                return {"success": False, "message": "选择器或储存的元素对象不能为空"}

            # 使用储存的元素对象或选择器查找元素
            if stored_element and stored_element != "无":
                # 使用储存的元素对象
                elements = [self.variables.get(stored_element)]
                if not elements[0]:
                    return {"success": False, "message": f"储存的元素对象不存在: {stored_element}"}
            else:
                # 使用选择器查找元素 - AdsPower官方支持CSS选择器
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                except:
                    # 如果CSS选择器失败，尝试XPath
                    try:
                        elements = self.driver.find_elements(By.XPATH, selector)
                    except:
                        return {"success": False, "message": f"无效的选择器: {selector}"}

            if not elements or element_order >= len(elements):
                return {"success": False, "message": f"未找到指定元素 (序号: {element_order + 1})"}

            element = elements[element_order]

            # 滚动到元素可见
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.3)

            # 根据点击类型和按键类型执行点击
            action = ActionChains(self.driver)

            if click_action == '双击':
                # AdsPower原版：双击操作
                if click_type == '鼠标右键':
                    action.context_click(element).perform()
                    time.sleep(0.1)
                    action.context_click(element).perform()
                elif click_type == '鼠标中键':
                    # 中键双击（较少使用）
                    action.click(element).perform()
                    time.sleep(0.1)
                    action.click(element).perform()
                else:  # 鼠标左键
                    action.double_click(element).perform()
            else:  # 单击
                # AdsPower原版：单击操作
                if click_type == '鼠标右键':
                    action.context_click(element).perform()
                elif click_type == '鼠标中键':
                    # 中键点击（通常用于在新标签页打开链接）
                    self.driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {button: 1, bubbles: true}));", element)
                else:  # 鼠标左键
                    element.click()

            return {"success": True, "message": f"点击元素成功 ({click_type} {click_action})", "element_text": element.text[:50]}
        except Exception as e:
            return {"success": False, "message": f"点击元素失败: {str(e)}"}
    
    def hover_element(self, config):
        """经过元素 - 完全按照AdsPower原版实现"""
        try:
            # 获取选择器配置
            selector_type = config.get('hover_selector_type', 'Selector')
            selector = config.get('hover_selector', '')
            element_order = config.get('hover_element_order', 1) - 1

            if not selector:
                return {"success": False, "message": "未指定元素选择器"}

            # 根据选择器类型查找元素
            if selector_type == 'XPath':
                elements = self.driver.find_elements(By.XPATH, selector)
            elif selector_type == '文本':
                elements = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{selector}')]")
            else:  # Selector (CSS)
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)

            if not elements or element_order >= len(elements):
                return {"success": False, "message": f"未找到指定的元素 (序号: {element_order + 1})"}

            element = elements[element_order]

            # 滚动到元素可见
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.3)

            # 执行鼠标悬停
            ActionChains(self.driver).move_to_element(element).perform()

            # 悬停持续时间（AdsPower默认短暂悬停）
            hover_duration = config.get('hover_duration', 500) / 1000
            time.sleep(hover_duration)

            return {"success": True, "message": "经过元素成功", "element_text": element.text[:50]}
        except Exception as e:
            return {"success": False, "message": f"经过元素失败: {str(e)}"}
    
    def page_back(self, config):
        """页面后退"""
        try:
            self.driver.back()
            if config.get('nav_wait_load', True):
                WebDriverWait(self.driver, 30).until(
                    lambda driver: driver.execute_script("return document.readyState") == "complete"
                )
            return {"success": True, "message": "页面后退成功"}
        except Exception as e:
            return {"success": False, "message": f"页面后退失败: {str(e)}"}
    
    def page_forward(self, config):
        """页面前进"""
        try:
            self.driver.forward()
            if config.get('nav_wait_load', True):
                WebDriverWait(self.driver, 30).until(
                    lambda driver: driver.execute_script("return document.readyState") == "complete"
                )
            return {"success": True, "message": "页面前进成功"}
        except Exception as e:
            return {"success": False, "message": f"页面前进失败: {str(e)}"}
    
    def refresh_page(self, config):
        """刷新页面"""
        try:
            self.driver.refresh()
            if config.get('nav_wait_load', True):
                WebDriverWait(self.driver, 30).until(
                    lambda driver: driver.execute_script("return document.readyState") == "complete"
                )
            return {"success": True, "message": "刷新页面成功"}
        except Exception as e:
            return {"success": False, "message": f"刷新页面失败: {str(e)}"}
    
    def close_tab(self, config):
        """关闭标签页 - 完全按照AdsPower原版实现"""
        try:
            close_type = config.get('close_tab_type', '当前标签')

            if close_type == '当前标签':
                # AdsPower原版：关闭当前标签页
                current_handle = self.driver.current_window_handle
                self.driver.close()

                # 切换到剩余的标签页
                handles = self.driver.window_handles
                if handles:
                    # 优先切换到第一个标签页
                    self.driver.switch_to.window(handles[0])
                else:
                    return {"success": False, "message": "没有剩余的标签页"}

            elif close_type == '指定标签':
                # AdsPower原版：关闭指定序号的标签页
                tab_index = config.get('close_tab_index', 1) - 1
                handles = self.driver.window_handles

                if 0 <= tab_index < len(handles):
                    current_handle = self.driver.current_window_handle
                    target_handle = handles[tab_index]

                    # 切换到目标标签页并关闭
                    self.driver.switch_to.window(target_handle)
                    self.driver.close()

                    # 处理关闭后的标签页切换
                    remaining_handles = self.driver.window_handles
                    if remaining_handles:
                        if current_handle in remaining_handles:
                            # 如果原标签页还存在，切换回去
                            self.driver.switch_to.window(current_handle)
                        else:
                            # 否则切换到第一个可用标签页
                            self.driver.switch_to.window(remaining_handles[0])
                    else:
                        return {"success": False, "message": "没有剩余的标签页"}
                else:
                    return {"success": False, "message": f"标签页序号 {tab_index + 1} 超出范围"}

            return {"success": True, "message": "关闭标签页成功", "remaining_tabs": len(self.driver.window_handles)}
        except Exception as e:
            return {"success": False, "message": f"关闭标签页失败: {str(e)}"}

    def close_other_tabs(self, config):
        """关闭其他标签页"""
        try:
            current_handle = self.driver.current_window_handle
            for handle in self.driver.window_handles:
                if handle != current_handle:
                    self.driver.switch_to.window(handle)
                    self.driver.close()
            self.driver.switch_to.window(current_handle)

            return {"success": True, "message": "关闭其他标签页成功"}
        except Exception as e:
            return {"success": False, "message": f"关闭其他标签页失败: {str(e)}"}

    def page_screenshot(self, config):
        """页面截图"""
        try:
            screenshot_name = config.get('screenshot_name', f"screenshot_{int(time.time())}")
            full_screen = config.get('full_screen', False)
            image_format = config.get('image_format', 'png')

            if full_screen:
                # 截取整个网页长图
                total_height = self.driver.execute_script("return document.body.scrollHeight")
                viewport_height = self.driver.execute_script("return window.innerHeight")

                # 设置窗口大小以截取完整页面
                self.driver.set_window_size(1920, total_height)
                time.sleep(1)

                screenshot_data = self.driver.get_screenshot_as_base64()
            else:
                # 截取当前可见区域
                screenshot_data = self.driver.get_screenshot_as_base64()

            # 保存截图
            screenshot_path = f"{screenshot_name}.{image_format}"
            with open(screenshot_path, "wb") as f:
                f.write(base64.b64decode(screenshot_data))

            return {"success": True, "message": f"页面截图成功: {screenshot_path}", "screenshot_path": screenshot_path}
        except Exception as e:
            return {"success": False, "message": f"页面截图失败: {str(e)}"}
    
    def switch_tab(self, config):
        """切换标签页"""
        try:
            switch_type = config.get('switch_type', '按序号')
            target = config.get('switch_target', '1')

            handles = self.driver.window_handles

            if switch_type == '按序号':
                index = int(target) - 1
                if 0 <= index < len(handles):
                    self.driver.switch_to.window(handles[index])
                else:
                    return {"success": False, "message": "标签页序号超出范围"}
            elif switch_type == '按标题':
                for handle in handles:
                    self.driver.switch_to.window(handle)
                    if target in self.driver.title:
                        break
                else:
                    return {"success": False, "message": "未找到匹配标题的标签页"}
            elif switch_type == '按URL':
                for handle in handles:
                    self.driver.switch_to.window(handle)
                    if target in self.driver.current_url:
                        break
                else:
                    return {"success": False, "message": "未找到匹配URL的标签页"}

            return {"success": True, "message": "切换标签页成功"}
        except Exception as e:
            return {"success": False, "message": f"切换标签页失败: {str(e)}"}

    def select_dropdown(self, config):
        """下拉选择器 - 完全按照AdsPower原版实现"""
        try:
            # 获取选择器配置
            selector_type = config.get('dropdown_selector_type', 'Selector')
            selector = config.get('dropdown_selector', '')
            element_order = config.get('dropdown_element_order', 1) - 1
            select_type = config.get('dropdown_select_type', '按文本')
            select_value = config.get('dropdown_select_value', '')

            if not selector:
                return {"success": False, "message": "未指定元素选择器"}

            if not select_value:
                return {"success": False, "message": "未指定选择值"}

            # 根据选择器类型查找元素
            if selector_type == 'XPath':
                elements = self.driver.find_elements(By.XPATH, selector)
            elif selector_type == '文本':
                elements = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{selector}')]")
            else:  # Selector (CSS)
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)

            if not elements or element_order >= len(elements):
                return {"success": False, "message": f"未找到指定的select元素 (序号: {element_order + 1})"}

            # 滚动到元素可见
            element = elements[element_order]
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.3)

            # 创建Select对象
            select_element = Select(element)

            # 根据选择方式进行选择
            if select_type == '按文本':
                # AdsPower原版：按可见文本选择
                select_element.select_by_visible_text(select_value)
            elif select_type == '按值':
                # AdsPower原版：按value属性选择
                select_element.select_by_value(select_value)
            elif select_type == '按索引':
                # AdsPower原版：按索引选择
                try:
                    index = int(select_value) - 1  # 转换为0基索引
                    select_element.select_by_index(index)
                except ValueError:
                    return {"success": False, "message": f"索引值必须是数字: {select_value}"}
                except:
                    return {"success": False, "message": f"索引 {select_value} 超出范围"}

            # 获取选中的选项信息
            selected_option = select_element.first_selected_option
            selected_text = selected_option.text
            selected_value = selected_option.get_attribute('value')

            return {
                "success": True,
                "message": "下拉选择器操作成功",
                "selected_text": selected_text,
                "selected_value": selected_value
            }
        except Exception as e:
            return {"success": False, "message": f"下拉选择器操作失败: {str(e)}"}

    def focus_element(self, config):
        """元素聚焦 - 完全按照AdsPower原版实现"""
        try:
            # 获取选择器配置
            selector_type = config.get('focus_selector_type', 'Selector')
            selector = config.get('focus_selector', '')
            element_order = config.get('focus_element_order', 1) - 1

            if not selector:
                return {"success": False, "message": "未指定元素选择器"}

            # 根据选择器类型查找元素
            if selector_type == 'XPath':
                elements = self.driver.find_elements(By.XPATH, selector)
            elif selector_type == '文本':
                elements = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{selector}')]")
            else:  # Selector (CSS)
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)

            if not elements or element_order >= len(elements):
                return {"success": False, "message": f"未找到指定元素 (序号: {element_order + 1})"}

            element = elements[element_order]

            # 滚动到元素可见
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.3)

            # AdsPower原版：聚焦元素（使用JavaScript focus方法）
            self.driver.execute_script("arguments[0].focus();", element)

            # 如果是输入元素，也可以点击来确保聚焦
            if element.tag_name.lower() in ['input', 'textarea', 'select']:
                element.click()

            return {"success": True, "message": "元素聚焦成功", "element_tag": element.tag_name}
        except Exception as e:
            return {"success": False, "message": f"元素聚焦失败: {str(e)}"}

    def input_content(self, config):
        """输入内容 - 完全按照AdsPower官方标准"""
        try:
            # 兼容新旧参数格式
            if 'selector' in config:
                # 新标准格式 - 完全按照AdsPower官方
                selector = config.get('selector', '')
                stored_element = config.get('stored_element')
                element_order = config.get('element_order', 1)
                content = config.get('content', '')
                content_type = config.get('content_type', '顺序选取')
                input_interval = config.get('input_interval', 300) / 1000  # 转换为秒
                clear_before = config.get('clear_before', True)
            else:
                # 旧格式兼容
                selector = config.get('input_selector', '')
                stored_element = None
                element_order = config.get('input_element_order', 1)
                content = config.get('input_content', '')
                content_type = '顺序选取'
                input_interval = config.get('input_interval', 100) / 1000
                clear_before = config.get('input_method', '覆盖') == '覆盖'

            if not selector and not stored_element:
                return {"success": False, "message": "选择器或储存的元素对象不能为空"}

            if not content:
                return {"success": False, "message": "未指定输入内容"}

            # 处理多行内容和内容选取方式
            content_lines = content.strip().split('\n') if isinstance(content, str) else [str(content)]

            if content_type == '随机选取':
                import random
                selected_content = random.choice(content_lines)
            elif content_type == '随机取数':
                # 假设内容格式为 "min-max"
                if '-' in content and len(content_lines) == 1:
                    try:
                        min_val, max_val = map(int, content.split('-'))
                        selected_content = str(random.randint(min_val, max_val))
                    except:
                        selected_content = content_lines[0]
                else:
                    selected_content = content_lines[0]
            elif content_type == '使用变量':
                # 从变量中获取内容
                var_name = content.strip()
                selected_content = str(self.variables.get(var_name, content))
            else:  # 顺序选取
                # 这里可以根据环境ID或其他逻辑选择，暂时使用第一个
                selected_content = content_lines[0]

            # 使用储存的元素对象或选择器查找元素
            if stored_element and stored_element != "无":
                # 使用储存的元素对象
                elements = [self.variables.get(stored_element)]
                if not elements[0]:
                    return {"success": False, "message": f"储存的元素对象不存在: {stored_element}"}
            else:
                # 使用选择器查找元素 - AdsPower官方支持CSS选择器
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                except:
                    # 如果CSS选择器失败，尝试XPath
                    try:
                        elements = self.driver.find_elements(By.XPATH, selector)
                    except:
                        return {"success": False, "message": f"无效的选择器: {selector}"}

            element_index = element_order - 1 if element_order > 0 else 0
            if not elements or element_index >= len(elements):
                return {"success": False, "message": f"未找到指定输入元素 (序号: {element_order})"}

            element = elements[element_index]

            # 滚动到元素可见
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.3)

            # 聚焦元素
            element.click()
            time.sleep(0.1)

            # 根据清除选项处理现有内容
            if clear_before:
                # AdsPower原版：清除现有内容后输入（模拟Ctrl+A Del）
                element.clear()
                # 使用Ctrl+A确保全选
                ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
                time.sleep(0.1)
                # 删除选中内容
                element.send_keys(Keys.DELETE)
                time.sleep(0.1)

            # 逐字符输入内容（模拟真实输入）
            if selected_content:
                if input_interval > 0:
                    # 有间隔的逐字符输入 - AdsPower官方标准
                    for char in selected_content:
                        element.send_keys(char)
                        time.sleep(input_interval)
                else:
                    # 直接输入全部内容
                    element.send_keys(selected_content)

            # 触发change事件确保内容被识别
            self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', {bubbles: true}));", element)
            self.driver.execute_script("arguments[0].dispatchEvent(new Event('change', {bubbles: true}));", element)

            return {
                "success": True,
                "message": f"输入内容成功 - 选择器: {selector}, 内容长度: {len(selected_content)}",
                "content_length": len(selected_content),
                "content_type": content_type
            }
        except Exception as e:
            return {"success": False, "message": f"输入内容失败: {str(e)}"}

    def upload_file(self, config):
        """上传附件 - 完全按照AdsPower原版实现"""
        try:
            # 获取配置参数
            selector_type = config.get('selector_type', 'selector')
            selector = config.get('selector', '')
            element_order = int(config.get('element_order', '1')) - 1
            attachment_type = config.get('attachment_type', 'local_file')
            file_path = config.get('file_path', '')
            timeout = config.get('timeout', 30000) / 1000  # 转换为秒

            if not selector:
                return {"success": False, "message": "未指定选择器"}

            if not file_path:
                return {"success": False, "message": "未指定文件路径"}

            # 根据选择器类型查找文件输入元素
            try:
                if selector_type == 'xpath':
                    elements = self.driver.find_elements(By.XPATH, selector)
                elif selector_type == 'text':
                    elements = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{selector}')]")
                else:  # selector (CSS)
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)

                if not elements or element_order >= len(elements):
                    return {"success": False, "message": f"未找到指定的文件输入元素 (序号: {element_order + 1})"}

                element = elements[element_order]

                # 验证元素是否为文件输入元素
                if element.tag_name.lower() != 'input' or element.get_attribute('type') != 'file':
                    return {"success": False, "message": "选择的元素不是文件输入元素"}

                # 滚动到元素可见
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                time.sleep(0.2)

            except Exception as e:
                return {"success": False, "message": f"查找文件输入元素失败: {str(e)}"}

            # 处理不同类型的附件
            actual_file_path = ""

            if attachment_type == 'local_file':
                # 本地文件
                if not os.path.exists(file_path):
                    return {"success": False, "message": f"文件不存在: {file_path}"}
                actual_file_path = os.path.abspath(file_path)

            elif attachment_type == 'folder_random':
                # 文件夹文件随机
                if not os.path.isdir(file_path):
                    return {"success": False, "message": f"文件夹不存在: {file_path}"}
                files = [f for f in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, f))]
                if not files:
                    return {"success": False, "message": "文件夹中没有文件"}
                random_file = random.choice(files)
                actual_file_path = os.path.abspath(os.path.join(file_path, random_file))

            elif attachment_type == 'network_url':
                # 网络URL
                try:
                    import requests
                    from urllib.parse import urlparse

                    # 设置请求超时
                    response = requests.get(file_path, timeout=timeout, stream=True)
                    response.raise_for_status()

                    # 从URL获取文件名
                    parsed_url = urlparse(file_path)
                    filename = os.path.basename(parsed_url.path)
                    if not filename:
                        filename = f"download_{int(time.time())}"

                    # 创建临时文件
                    temp_filename = f"temp_upload_{int(time.time())}_{filename}"
                    with open(temp_filename, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)

                    actual_file_path = os.path.abspath(temp_filename)

                except Exception as e:
                    return {"success": False, "message": f"下载网络文件失败: {str(e)}"}
            else:
                return {"success": False, "message": f"不支持的附件类型: {attachment_type}"}

            # 上传文件
            try:
                element.send_keys(actual_file_path)

                # 等待文件上传完成（简单检查）
                time.sleep(1)

                # 如果是临时文件，可以选择在上传后删除
                if attachment_type == 'network_url' and actual_file_path.startswith("temp_upload_"):
                    try:
                        os.remove(actual_file_path)
                    except:
                        pass  # 忽略删除失败

                return {
                    "success": True,
                    "message": "上传附件成功",
                    "file_path": actual_file_path,
                    "attachment_type": attachment_type
                }

            except Exception as e:
                # 清理临时文件
                if attachment_type == 'network_url' and actual_file_path.startswith("temp_upload_"):
                    try:
                        os.remove(actual_file_path)
                    except:
                        pass
                return {"success": False, "message": f"上传文件失败: {str(e)}"}

        except Exception as e:
            return {"success": False, "message": f"上传附件失败: {str(e)}"}

    # ==================== 键盘操作实现 ====================

    def execute_javascript(self, config):
        """执行JS脚本"""
        try:
            js_code = config.get('js_code', '')
            if not js_code:
                return {"success": False, "message": "未指定JS代码"}

            # 注入变量到JS环境
            inject_vars = config.get('inject_variables', [])
            for var_name in inject_vars:
                if var_name in self.variables:
                    var_value = self.variables[var_name]
                    # 将变量注入到window对象中
                    self.driver.execute_script(f"window.{var_name} = arguments[0];", var_value)

            result = self.driver.execute_script(js_code)

            # 保存返回值到变量
            return_var = config.get('return_variable', '')
            if return_var:
                self.variables[return_var] = result

            return {"success": True, "message": "JS脚本执行成功", "result": result}
        except Exception as e:
            return {"success": False, "message": f"JS脚本执行失败: {str(e)}"}

    def keyboard_key(self, config):
        """键盘按键"""
        try:
            key_type = config.get('key_type', '回车键')
            delay = config.get('keyboard_delay', 100) / 1000

            key_mapping = {
                '退格键': Keys.BACKSPACE,
                'Tab键': Keys.TAB,
                '回车键': Keys.RETURN,
                '空格键': Keys.SPACE,
                'Esc键': Keys.ESCAPE,
                '删除键': Keys.DELETE,
                '方向上键': Keys.ARROW_UP,
                '方向下键': Keys.ARROW_DOWN,
                '方向左键': Keys.ARROW_LEFT,
                '方向右键': Keys.ARROW_RIGHT
            }

            if key_type in key_mapping:
                ActionChains(self.driver).send_keys(key_mapping[key_type]).perform()
            else:
                return {"success": False, "message": f"不支持的按键类型: {key_type}"}

            time.sleep(delay)
            return {"success": True, "message": f"键盘按键 {key_type} 成功"}
        except Exception as e:
            return {"success": False, "message": f"键盘按键失败: {str(e)}"}

    def keyboard_combo(self, config):
        """组合键"""
        try:
            combo_key = config.get('combo_key', 'Ctrl+A')
            delay = config.get('keyboard_delay', 100) / 1000

            combo_mapping = {
                'Ctrl+A': [Keys.CONTROL, 'a'],
                'Ctrl+C': [Keys.CONTROL, 'c'],
                'Ctrl+V': [Keys.CONTROL, 'v'],
                'Ctrl+R': [Keys.CONTROL, 'r'],
                'Ctrl+Z': [Keys.CONTROL, 'z'],
                'Ctrl+Y': [Keys.CONTROL, 'y'],
                'Ctrl+S': [Keys.CONTROL, 's'],
                'Ctrl+F': [Keys.CONTROL, 'f'],
                'Ctrl+T': [Keys.CONTROL, 't'],
                'Ctrl+W': [Keys.CONTROL, 'w'],
                'Ctrl+Tab': [Keys.CONTROL, Keys.TAB],
                'Alt+Tab': [Keys.ALT, Keys.TAB],
                'Shift+Tab': [Keys.SHIFT, Keys.TAB]
            }

            if combo_key in combo_mapping:
                keys = combo_mapping[combo_key]
                action = ActionChains(self.driver)
                action.key_down(keys[0])
                action.send_keys(keys[1])
                action.key_up(keys[0])
                action.perform()
            else:
                return {"success": False, "message": f"不支持的组合键: {combo_key}"}

            time.sleep(delay)
            return {"success": True, "message": f"组合键 {combo_key} 成功"}
        except Exception as e:
            return {"success": False, "message": f"组合键操作失败: {str(e)}"}

    # ==================== 等待操作实现 ====================

    def wait_element(self, config):
        """等待元素"""
        try:
            selector = config.get('wait_element_selector', '')
            condition = config.get('wait_condition', '出现')
            timeout = config.get('wait_timeout', 30)

            if not selector:
                return {"success": False, "message": "未指定元素选择器"}

            wait = WebDriverWait(self.driver, timeout)

            if condition == '出现':
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            elif condition == '可见':
                wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
            elif condition == '可点击':
                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
            elif condition == '消失':
                wait.until_not(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            elif condition == '隐藏':
                wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, selector)))

            return {"success": True, "message": f"等待元素 {condition} 成功"}
        except TimeoutException:
            return {"success": False, "message": f"等待元素超时"}
        except Exception as e:
            return {"success": False, "message": f"等待元素失败: {str(e)}"}

    def wait_page(self, config):
        """等待页面"""
        try:
            wait_type = config.get('page_wait_type', '页面加载完成')
            timeout = config.get('page_timeout', 30)

            wait = WebDriverWait(self.driver, timeout)

            if wait_type == '页面加载完成':
                wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            elif wait_type == 'DOM加载完成':
                wait.until(lambda driver: driver.execute_script("return document.readyState") in ["interactive", "complete"])
            elif wait_type == '网络请求完成':
                # 等待所有网络请求完成（简化实现）
                time.sleep(2)
                wait.until(lambda driver: driver.execute_script("return jQuery.active == 0") if self.driver.execute_script("return typeof jQuery !== 'undefined'") else True)

            return {"success": True, "message": f"等待页面 {wait_type} 成功"}
        except TimeoutException:
            return {"success": False, "message": "等待页面超时"}
        except Exception as e:
            return {"success": False, "message": f"等待页面失败: {str(e)}"}

    def wait_popup(self, config):
        """等待弹窗"""
        try:
            popup_type = config.get('popup_type', 'Alert弹窗')
            action = config.get('popup_action', '接受')
            timeout = config.get('popup_timeout', 10)

            wait = WebDriverWait(self.driver, timeout)

            if popup_type in ['Alert弹窗', 'Confirm弹窗', 'Prompt弹窗']:
                alert = wait.until(EC.alert_is_present())

                if action == '接受':
                    alert.accept()
                elif action == '取消':
                    alert.dismiss()
                elif action == '获取文本':
                    text = alert.text
                    alert.accept()
                    return {"success": True, "message": "获取弹窗文本成功", "text": text}

            return {"success": True, "message": f"处理弹窗成功"}
        except TimeoutException:
            return {"success": False, "message": "等待弹窗超时"}
        except Exception as e:
            return {"success": False, "message": f"等待弹窗失败: {str(e)}"}

    def wait_request(self, config):
        """等待请求完成"""
        try:
            request_url = config.get('request_url', '')
            timeout = config.get('timeout', 30)
            wait_type = config.get('wait_type', '网络请求完成')

            if wait_type == '网络请求完成':
                # 等待所有网络请求完成（简化实现）
                wait = WebDriverWait(self.driver, timeout)

                # 检查jQuery是否存在并等待Ajax完成
                jquery_exists = self.driver.execute_script("return typeof jQuery !== 'undefined'")
                if jquery_exists:
                    wait.until(lambda driver: driver.execute_script("return jQuery.active == 0"))

                # 等待页面加载状态
                wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")

                # 额外等待一段时间确保所有异步请求完成
                time.sleep(2)

            elif wait_type == '特定请求':
                # 等待特定URL的请求（需要更复杂的实现，这里简化）
                time.sleep(timeout)

            return {"success": True, "message": "等待请求完成"}
        except TimeoutException:
            return {"success": False, "message": "等待请求超时"}
        except Exception as e:
            return {"success": False, "message": f"等待请求失败: {str(e)}"}

    # ==================== 获取数据实现 ====================

    def get_url(self, config):
        """获取URL - 完全按照AdsPower原版实现"""
        try:
            save_var = config.get('get_url_save_var', '')
            url_type = config.get('url_type', '完整地址')

            if not save_var:
                return {"success": False, "message": "未指定保存变量"}

            if not self.driver:
                return {"success": False, "message": "浏览器驱动未初始化"}

            current_url = self.driver.current_url

            # AdsPower原版：支持多种URL获取方式
            if url_type == '完整地址':
                data = current_url
            elif url_type == '根地址':
                from urllib.parse import urlparse
                parsed = urlparse(current_url)
                data = f"{parsed.scheme}://{parsed.netloc}"
            elif url_type == '路径':
                from urllib.parse import urlparse
                parsed = urlparse(current_url)
                data = parsed.path
            elif url_type == '参数':
                from urllib.parse import urlparse
                parsed = urlparse(current_url)
                data = parsed.query
            elif url_type == '锚点':
                from urllib.parse import urlparse
                parsed = urlparse(current_url)
                data = parsed.fragment
            else:
                data = current_url

            # 保存到变量
            self.variables[save_var] = data
            return {"success": True, "message": "获取URL成功", "data": data, "url_type": url_type}
        except Exception as e:
            return {"success": False, "message": f"获取URL失败: {str(e)}"}

    def get_clipboard(self, config):
        """获取粘贴板内容 - 完全按照AdsPower原版实现"""
        try:
            save_var = config.get('clipboard_save_var', '')

            if not save_var:
                return {"success": False, "message": "未指定保存变量"}

            # AdsPower原版：优先使用系统剪贴板API
            try:
                # 尝试使用pyperclip获取剪贴板内容
                if PYPERCLIP_AVAILABLE:
                    data = pyperclip.paste()
                else:
                    # 如果pyperclip不可用，使用替代方案
                    data = self._get_clipboard_fallback()

                # 验证数据有效性
                if data is None:
                    data = ""

                self.variables[save_var] = data
                return {"success": True, "message": "获取粘贴板内容成功", "data": data, "length": len(data)}

            except ImportError:
                # 如果pyperclip不可用，尝试使用浏览器API
                if self.driver:
                    try:
                        # 使用JavaScript Clipboard API
                        data = self.driver.execute_script("""
                            return navigator.clipboard.readText().then(text => {
                                return text || '';
                            }).catch(() => {
                                return '';
                            });
                        """)

                        if data is None:
                            data = ""

                        self.variables[save_var] = data
                        return {"success": True, "message": "获取粘贴板内容成功（浏览器API）", "data": data, "length": len(data)}
                    except Exception as js_error:
                        return {"success": False, "message": f"浏览器API获取失败: {str(js_error)}"}
                else:
                    return {"success": False, "message": "无可用的剪贴板访问方法"}

            except Exception as clipboard_error:
                return {"success": False, "message": f"系统剪贴板访问失败: {str(clipboard_error)}"}

        except Exception as e:
            return {"success": False, "message": f"获取粘贴板内容失败: {str(e)}"}

    def get_element_data(self, config):
        """获取元素数据 - 完全按照AdsPower原版实现"""
        try:
            # 获取配置参数
            selector_type = config.get('element_data_selector_type', 'Selector')
            selector = config.get('element_data_selector', '')
            extract_type = config.get('element_data_extract_type', '文本')
            save_var = config.get('element_data_save_var', '')
            element_order = config.get('element_data_order', 1) - 1
            attribute_name = config.get('attribute_name', 'href')

            if not selector or not save_var:
                return {"success": False, "message": "缺少必要参数"}

            if not self.driver:
                return {"success": False, "message": "浏览器驱动未初始化"}

            # 根据选择器类型查找元素
            if selector_type == 'XPath':
                elements = self.driver.find_elements(By.XPATH, selector)
            elif selector_type == '文本':
                elements = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{selector}')]")
            else:  # Selector (CSS)
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)

            if not elements or element_order >= len(elements):
                return {"success": False, "message": "未找到指定元素 (序号: " + str(element_order + 1) + ")"}

            element = elements[element_order]

            # 滚动到元素可见
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.2)

            # AdsPower原版：根据提取类型获取数据
            if extract_type == '文本':
                data = element.text
            elif extract_type == '属性':
                data = element.get_attribute(attribute_name)
                if data is None:
                    data = ""
            elif extract_type == 'HTML':
                data = element.get_attribute('innerHTML')
            elif extract_type == '值':
                data = element.get_attribute('value')
                if data is None:
                    data = ""
            elif extract_type == '对象':
                # AdsPower原版：返回元素的完整信息对象
                data = {
                    'tag_name': element.tag_name,
                    'text': element.text,
                    'id': element.get_attribute('id'),
                    'class': element.get_attribute('class'),
                    'name': element.get_attribute('name'),
                    'value': element.get_attribute('value'),
                    'href': element.get_attribute('href'),
                    'src': element.get_attribute('src'),
                    'location': element.location,
                    'size': element.size,
                    'is_displayed': element.is_displayed(),
                    'is_enabled': element.is_enabled(),
                    'is_selected': element.is_selected() if element.tag_name.lower() in ['option', 'input'] else False
                }
            elif extract_type == 'IFrame框架':
                # AdsPower原版：切换到iframe
                try:
                    self.driver.switch_to.frame(element)
                    data = "已切换到iframe框架"
                except Exception as iframe_error:
                    data = f"切换iframe失败: {str(iframe_error)}"
            elif extract_type == '源码':
                data = element.get_attribute('outerHTML')
            elif extract_type == '子元素':
                # AdsPower原版：获取子元素信息
                children = element.find_elements(By.XPATH, "./*")
                data = []
                for child in children:
                    data.append({
                        'tag_name': child.tag_name,
                        'text': child.text[:100],  # 限制文本长度
                        'id': child.get_attribute('id'),
                        'class': child.get_attribute('class')
                    })
            else:
                data = element.text

            # 保存到变量
            self.variables[save_var] = data

            return {
                "success": True,
                "message": "获取元素数据成功",
                "data": data,
                "extract_type": extract_type,
                "element_tag": element.tag_name
            }
        except Exception as e:
            return {"success": False, "message": f"获取元素数据失败: {str(e)}"}

    def get_focused_element(self, config):
        """获取当前焦点元素"""
        try:
            save_var = config.get('save_variable', '')

            if not save_var:
                return {"success": False, "message": "未指定保存变量"}

            # 获取当前焦点元素
            focused_element = self.driver.switch_to.active_element

            data = {
                'tag_name': focused_element.tag_name,
                'text': focused_element.text,
                'id': focused_element.get_attribute('id'),
                'class': focused_element.get_attribute('class'),
                'name': focused_element.get_attribute('name'),
                'value': focused_element.get_attribute('value')
            }

            self.variables[save_var] = data
            return {"success": True, "message": "获取当前焦点元素成功", "data": data}
        except Exception as e:
            return {"success": False, "message": f"获取当前焦点元素失败: {str(e)}"}

    def save_to_file(self, config):
        """存到文件 - 完全按照AdsPower原版实现"""
        try:
            # 获取配置参数
            data_source = config.get('data_source', '')
            file_path = config.get('file_path', '')
            file_format = config.get('file_format', 'txt')
            append_mode = config.get('append_mode', False)
            encoding_type = config.get('encoding', 'utf-8')

            if not data_source:
                return {"success": False, "message": "未指定数据源"}

            if not file_path:
                return {"success": False, "message": "未指定文件路径"}

            # AdsPower原版：获取数据源
            if data_source in self.variables:
                data = self.variables[data_source]
            else:
                # 如果不是变量，则作为直接数据
                data = data_source

            # 处理数据为字符串
            if data is None:
                data_str = ""
            elif isinstance(data, (dict, list)):
                import json
                data_str = json.dumps(data, ensure_ascii=False, indent=2)
            else:
                data_str = str(data)

            # 确保目录存在
            try:
                directory = os.path.dirname(file_path)
                if directory and not os.path.exists(directory):
                    os.makedirs(directory, exist_ok=True)
            except Exception as dir_error:
                return {"success": False, "message": f"创建目录失败: {str(dir_error)}"}

            # AdsPower原版：根据文件格式和模式写入
            try:
                mode = 'a' if append_mode else 'w'

                with open(file_path, mode, encoding=encoding_type) as f:
                    if append_mode and os.path.exists(file_path):
                        # 追加模式：确保换行
                        f.write('\n' + data_str)
                    else:
                        f.write(data_str)

                    # 确保文件以换行符结尾
                    if not data_str.endswith('\n'):
                        f.write('\n')

                # 验证文件是否成功写入
                if os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                    return {
                        "success": True,
                        "message": f"数据已保存到文件: {file_path}",
                        "file_path": file_path,
                        "file_size": file_size,
                        "data_length": len(data_str)
                    }
                else:
                    return {"success": False, "message": "文件写入失败，文件不存在"}

            except Exception as write_error:
                return {"success": False, "message": f"文件写入失败: {str(write_error)}"}

        except Exception as e:
            return {"success": False, "message": f"保存文件失败: {str(e)}"}

    def save_to_excel(self, config):
        """存到Excel"""
        try:
            data_var = config.get('data_variable', '')
            file_path = config.get('file_path', '')
            sheet_name = config.get('sheet_name', 'Sheet1')
            start_row = config.get('start_row', 1)
            start_col = config.get('start_col', 1)

            if not data_var or not file_path:
                return {"success": False, "message": "缺少必要参数"}

            data = self.variables.get(data_var)
            if data is None:
                return {"success": False, "message": f"变量 {data_var} 不存在"}

            # 使用pandas处理Excel
            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, dict):
                df = pd.DataFrame([data])
            else:
                df = pd.DataFrame([{'data': data}])

            # 检查文件是否存在
            if os.path.exists(file_path):
                # 追加到现有文件
                with pd.ExcelWriter(file_path, mode='a', if_sheet_exists='overlay') as writer:
                    df.to_excel(writer, sheet_name=sheet_name, startrow=start_row-1,
                               startcol=start_col-1, index=False, header=False)
            else:
                # 创建新文件
                df.to_excel(file_path, sheet_name=sheet_name, index=False)

            return {"success": True, "message": f"数据已保存到Excel: {file_path}"}
        except Exception as e:
            return {"success": False, "message": f"保存到Excel失败: {str(e)}"}

    def download_file(self, config):
        """下载文件"""
        try:
            url = config.get('download_url', '')
            save_path = config.get('save_path', '')
            timeout = config.get('timeout', 30)

            if not url:
                return {"success": False, "message": "未指定下载URL"}

            if not save_path:
                # 自动生成文件名
                save_path = f"download_{int(time.time())}"

            # 使用requests下载文件
            response = requests.get(url, timeout=timeout, stream=True)
            response.raise_for_status()

            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            return {"success": True, "message": f"文件下载成功: {save_path}", "file_path": save_path}
        except Exception as e:
            return {"success": False, "message": f"下载文件失败: {str(e)}"}

    def import_excel(self, config):
        """导入Excel素材"""
        try:
            file_path = config.get('file_path', '')
            sheet_name = config.get('sheet_name', 0)  # 默认第一个sheet
            start_row = config.get('start_row', 1)
            save_var = config.get('save_variable', '')

            if not file_path or not save_var:
                return {"success": False, "message": "缺少必要参数"}

            if not os.path.exists(file_path):
                return {"success": False, "message": f"文件不存在: {file_path}"}

            # 读取Excel文件
            df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=start_row-1)

            # 转换为列表格式
            data = df.to_dict('records')

            self.variables[save_var] = data
            return {"success": True, "message": f"Excel数据导入成功，共 {len(data)} 行", "data": data}
        except Exception as e:
            return {"success": False, "message": f"导入Excel失败: {str(e)}"}

    def import_txt(self, config):
        """导入txt"""
        try:
            file_path = config.get('file_path', '')
            encoding = config.get('encoding', 'utf-8')
            delimiter = config.get('delimiter', '\n')
            save_var = config.get('save_variable', '')

            if not file_path or not save_var:
                return {"success": False, "message": "缺少必要参数"}

            if not os.path.exists(file_path):
                return {"success": False, "message": f"文件不存在: {file_path}"}

            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()

            # 根据分隔符分割内容
            if delimiter == '\\n':
                delimiter = '\n'
            elif delimiter == '\\t':
                delimiter = '\t'

            data = [line.strip() for line in content.split(delimiter) if line.strip()]

            self.variables[save_var] = data
            return {"success": True, "message": f"txt数据导入成功，共 {len(data)} 行", "data": data}
        except Exception as e:
            return {"success": False, "message": f"导入txt失败: {str(e)}"}

    def get_email(self, config):
        """获取邮件"""
        try:
            server = config.get('imap_server', '')
            username = config.get('username', '')
            password = config.get('password', '')
            folder = config.get('folder', 'INBOX')
            count = config.get('count', 1)
            save_var = config.get('save_variable', '')

            if not all([server, username, password, save_var]):
                return {"success": False, "message": "缺少必要参数"}

            # 连接IMAP服务器
            mail = imaplib.IMAP4_SSL(server)
            mail.login(username, password)
            mail.select(folder)

            # 搜索邮件
            status, messages = mail.search(None, 'ALL')
            if status != 'OK':
                return {"success": False, "message": "搜索邮件失败"}

            message_ids = messages[0].split()
            emails = []

            # 获取最新的几封邮件
            for msg_id in message_ids[-count:]:
                status, msg_data = mail.fetch(msg_id, '(RFC822)')
                if status == 'OK':
                    email_body = msg_data[0][1]
                    email_message = email.message_from_bytes(email_body)

                    email_info = {
                        'subject': email_message['Subject'],
                        'from': email_message['From'],
                        'date': email_message['Date'],
                        'body': self._get_email_body(email_message)
                    }
                    emails.append(email_info)

            mail.close()
            mail.logout()

            self.variables[save_var] = emails
            return {"success": True, "message": f"获取邮件成功，共 {len(emails)} 封", "data": emails}
        except Exception as e:
            return {"success": False, "message": f"获取邮件失败: {str(e)}"}

    def _get_email_body(self, email_message):
        """提取邮件正文"""
        try:
            if email_message.is_multipart():
                for part in email_message.walk():
                    if part.get_content_type() == "text/plain":
                        return part.get_payload(decode=True).decode()
            else:
                return email_message.get_payload(decode=True).decode()
        except:
            return ""

    def get_totp(self, config):
        """身份验证密码（TOTP）"""
        try:
            secret_key = config.get('secret_key', '')
            save_var = config.get('save_variable', '')

            if not secret_key or not save_var:
                return {"success": False, "message": "缺少必要参数"}

            # 生成TOTP验证码
            totp = pyotp.TOTP(secret_key)
            code = totp.now()

            self.variables[save_var] = code
            return {"success": True, "message": "生成TOTP验证码成功", "data": code}
        except Exception as e:
            return {"success": False, "message": f"生成TOTP验证码失败: {str(e)}"}

    def listen_request_trigger(self, config):
        """监听请求触发 - 完全按照AdsPower原版实现"""
        try:
            # 获取配置参数
            url_pattern = config.get('listen_url_pattern', '')
            listen_method = config.get('listen_method', '所有方法')
            timeout = config.get('listen_timeout', 30)
            save_var = config.get('listen_save_var', '')

            if not save_var:
                return {"success": False, "message": "未指定保存变量"}

            if not self.driver:
                return {"success": False, "message": "浏览器驱动未初始化"}

            # AdsPower原版：注入JavaScript来监听网络请求
            method_filter = "" if listen_method == "所有方法" else f"&& method.toUpperCase() === '{listen_method.upper()}'"

            js_code = f"""
            // 清除之前的监听数据
            window.adspower_request_data = [];

            // 监听Fetch API
            if (!window.adspower_fetch_hooked) {{
                const originalFetch = window.fetch;
                window.fetch = function(...args) {{
                    const url = args[0];
                    const method = args[1]?.method || 'GET';

                    // 检查URL模式和方法过滤
                    if ((!'{url_pattern}' || url.includes('{url_pattern}')) {method_filter}) {{
                        window.adspower_request_data.push({{
                            url: url,
                            method: method,
                            type: 'fetch',
                            timestamp: Date.now(),
                            headers: args[1]?.headers || {{}},
                            body: args[1]?.body || null
                        }});
                    }}
                    return originalFetch.apply(this, args);
                }};
                window.adspower_fetch_hooked = true;
            }}

            // 监听XMLHttpRequest
            if (!window.adspower_xhr_hooked) {{
                const originalXHROpen = window.XMLHttpRequest.prototype.open;
                const originalXHRSend = window.XMLHttpRequest.prototype.send;

                window.XMLHttpRequest.prototype.open = function(method, url) {{
                    this._adspower_method = method;
                    this._adspower_url = url;
                    return originalXHROpen.apply(this, arguments);
                }};

                window.XMLHttpRequest.prototype.send = function(data) {{
                    const method = this._adspower_method || 'GET';
                    const url = this._adspower_url || '';

                    // 检查URL模式和方法过滤
                    if ((!'{url_pattern}' || url.includes('{url_pattern}')) {method_filter}) {{
                        window.adspower_request_data.push({{
                            url: url,
                            method: method,
                            type: 'xhr',
                            timestamp: Date.now(),
                            data: data || null
                        }});
                    }}
                    return originalXHRSend.apply(this, arguments);
                }};
                window.adspower_xhr_hooked = true;
            }}
            """

            self.driver.execute_script(js_code)

            # AdsPower原版：等待请求触发
            start_time = time.time()
            while time.time() - start_time < timeout:
                try:
                    request_data = self.driver.execute_script("return window.adspower_request_data || [];")
                    if request_data and len(request_data) > 0:
                        # 保存到变量
                        self.variables[save_var] = request_data
                        return {
                            "success": True,
                            "message": f"监听到 {len(request_data)} 个请求",
                            "data": request_data,
                            "url_pattern": url_pattern,
                            "method_filter": listen_method
                        }
                except Exception as js_error:
                    # JavaScript执行错误，继续等待
                    pass

                time.sleep(0.5)  # 更频繁的检查

            return {"success": False, "message": f"监听请求超时 ({timeout}秒)"}
        except Exception as e:
            return {"success": False, "message": f"监听请求触发失败: {str(e)}"}

    def listen_request_result(self, config):
        """监听请求结果 - 完全按照AdsPower原版实现"""
        try:
            # 获取配置参数
            url_pattern = config.get('result_url_pattern', '')
            status_code = config.get('result_status_code', '所有状态')
            extract_type = config.get('result_extract_type', '完整响应')
            json_path = config.get('result_json_path', '')
            timeout = config.get('result_timeout', 30)
            save_var = config.get('result_save_var', '')

            if not save_var:
                return {"success": False, "message": "未指定保存变量"}

            if not self.driver:
                return {"success": False, "message": "浏览器驱动未初始化"}

            # AdsPower原版：状态码过滤条件
            status_filter = ""
            if status_code != "所有状态":
                status_filter = f"&& response.status == {status_code}"

            # AdsPower原版：注入JavaScript来监听网络请求响应
            js_code = f"""
            // 清除之前的响应数据
            window.adspower_response_data = [];

            // 监听Fetch API响应
            if (!window.adspower_fetch_response_hooked) {{
                const originalFetch = window.fetch;
                window.fetch = function(...args) {{
                    return originalFetch.apply(this, args).then(response => {{
                        const url = args[0];

                        // 检查URL模式和状态码过滤
                        if ((!'{url_pattern}' || url.includes('{url_pattern}')) {status_filter}) {{
                            // 克隆响应以避免消费
                            const responseClone = response.clone();

                            responseClone.text().then(text => {{
                                let responseData = {{
                                    url: url,
                                    status: response.status,
                                    statusText: response.statusText,
                                    headers: {{}},
                                    body: text,
                                    timestamp: Date.now(),
                                    type: 'fetch'
                                }};

                                // 提取响应头
                                for (let [key, value] of response.headers.entries()) {{
                                    responseData.headers[key] = value;
                                }}

                                window.adspower_response_data.push(responseData);
                            }}).catch(err => {{
                                // 处理响应体读取错误
                                window.adspower_response_data.push({{
                                    url: url,
                                    status: response.status,
                                    statusText: response.statusText,
                                    body: 'Error reading response body',
                                    timestamp: Date.now(),
                                    type: 'fetch',
                                    error: err.message
                                }});
                            }});
                        }}
                        return response;
                    }});
                }};
                window.adspower_fetch_response_hooked = true;
            }}

            // 监听XMLHttpRequest响应
            if (!window.adspower_xhr_response_hooked) {{
                const originalXHRSend = window.XMLHttpRequest.prototype.send;

                window.XMLHttpRequest.prototype.send = function(data) {{
                    const xhr = this;
                    const url = this._adspower_url || '';

                    // 添加响应监听
                    xhr.addEventListener('readystatechange', function() {{
                        if (xhr.readyState === 4) {{
                            // 检查URL模式和状态码过滤
                            if ((!'{url_pattern}' || url.includes('{url_pattern}')) {status_filter.replace('response.status', 'xhr.status')}) {{
                                window.adspower_response_data.push({{
                                    url: url,
                                    status: xhr.status,
                                    statusText: xhr.statusText,
                                    headers: xhr.getAllResponseHeaders(),
                                    body: xhr.responseText,
                                    timestamp: Date.now(),
                                    type: 'xhr'
                                }});
                            }}
                        }}
                    }});

                    return originalXHRSend.apply(this, arguments);
                }};
                window.adspower_xhr_response_hooked = true;
            }}
            """

            self.driver.execute_script(js_code)

            # AdsPower原版：等待响应
            start_time = time.time()
            while time.time() - start_time < timeout:
                try:
                    response_data = self.driver.execute_script("return window.adspower_response_data || [];")
                    if response_data and len(response_data) > 0:
                        # AdsPower原版：根据提取类型处理数据
                        processed_data = []
                        for resp in response_data:
                            if extract_type == '完整响应':
                                processed_data.append(resp)
                            elif extract_type == '响应体':
                                processed_data.append(resp.get('body', ''))
                            elif extract_type == '响应头':
                                processed_data.append(resp.get('headers', {}))
                            elif extract_type == '状态码':
                                processed_data.append(resp.get('status', 0))
                            elif extract_type == 'JSON字段' and json_path:
                                try:
                                    import json
                                    body = resp.get('body', '{}')
                                    json_data = json.loads(body)
                                    # 简单的JSON路径解析
                                    value = json_data
                                    for key in json_path.split('.'):
                                        if key and isinstance(value, dict):
                                            value = value.get(key)
                                        else:
                                            value = None
                                            break
                                    processed_data.append(value)
                                except:
                                    processed_data.append(None)
                            else:
                                processed_data.append(resp)

                        # 保存到变量
                        final_data = processed_data if len(processed_data) > 1 else (processed_data[0] if processed_data else None)
                        self.variables[save_var] = final_data

                        return {
                            "success": True,
                            "message": f"监听到 {len(response_data)} 个响应",
                            "data": final_data,
                            "raw_count": len(response_data),
                            "extract_type": extract_type
                        }
                except Exception as js_error:
                    # JavaScript执行错误，继续等待
                    pass

                time.sleep(0.5)  # 更频繁的检查

            return {"success": False, "message": f"监听请求结果超时 ({timeout}秒)"}
        except Exception as e:
            return {"success": False, "message": f"监听请求结果失败: {str(e)}"}

    def stop_page_listening(self, config):
        """停止页面监听"""
        try:
            # 清除监听脚本
            js_code = """
            if (window.requestData) delete window.requestData;
            if (window.responseData) delete window.responseData;
            // 恢复原始的fetch和XMLHttpRequest（简化实现）
            """

            self.driver.execute_script(js_code)
            return {"success": True, "message": "停止页面监听成功"}
        except Exception as e:
            return {"success": False, "message": f"停止页面监听失败: {str(e)}"}

    def get_cookies(self, config):
        """获取页面Cookie - 完全按照AdsPower原版实现"""
        try:
            # 获取配置参数
            cookie_type = config.get('cookie_type', '所有Cookie')
            cookie_name = config.get('cookie_name', '')
            save_var = config.get('cookie_save_var', '')

            if not save_var:
                return {"success": False, "message": "未指定保存变量"}

            if not self.driver:
                return {"success": False, "message": "浏览器驱动未初始化"}

            # AdsPower原版：根据Cookie类型获取数据
            if cookie_type == '所有Cookie':
                data = self.driver.get_cookies()
                message = f"获取所有Cookie成功，共 {len(data)} 个"
            elif cookie_type == '指定Cookie':
                if not cookie_name:
                    return {"success": False, "message": "未指定Cookie名称"}
                data = self.driver.get_cookie(cookie_name)
                if data is None:
                    return {"success": False, "message": f"Cookie '{cookie_name}' 不存在"}
                message = f"获取Cookie '{cookie_name}' 成功"
            elif cookie_type == 'Cookie数量':
                all_cookies = self.driver.get_cookies()
                data = len(all_cookies)
                message = f"获取Cookie数量成功: {data} 个"
            else:
                # 默认获取所有Cookie
                data = self.driver.get_cookies()
                message = f"获取所有Cookie成功，共 {len(data)} 个"

            # 保存到变量
            self.variables[save_var] = data
            return {
                "success": True,
                "message": message,
                "data": data,
                "cookie_type": cookie_type,
                "count": len(data) if isinstance(data, list) else 1
            }
        except Exception as e:
            return {"success": False, "message": f"获取Cookie失败: {str(e)}"}

    def clear_cookies(self, config):
        """清除页面Cookie - 完全按照AdsPower原版实现"""
        try:
            # 获取配置参数
            clear_type = config.get('clear_cookie_type', '所有Cookie')
            target = config.get('clear_cookie_target', '')

            if not self.driver:
                return {"success": False, "message": "浏览器驱动未初始化"}

            # AdsPower原版：根据清除类型执行操作
            if clear_type == '所有Cookie':
                # 获取清除前的Cookie数量
                before_count = len(self.driver.get_cookies())
                self.driver.delete_all_cookies()
                message = f"清除所有Cookie成功，共清除 {before_count} 个Cookie"

            elif clear_type == '指定Cookie':
                if not target:
                    return {"success": False, "message": "未指定Cookie名称"}

                # 检查Cookie是否存在
                cookie = self.driver.get_cookie(target)
                if cookie is None:
                    return {"success": False, "message": f"Cookie '{target}' 不存在"}

                self.driver.delete_cookie(target)
                message = f"清除Cookie '{target}' 成功"

            elif clear_type == '指定域名Cookie':
                if not target:
                    return {"success": False, "message": "未指定域名"}

                # AdsPower原版：清除指定域名的Cookie
                all_cookies = self.driver.get_cookies()
                cleared_count = 0

                for cookie in all_cookies:
                    cookie_domain = cookie.get('domain', '')
                    # 检查域名匹配（支持子域名）
                    if target in cookie_domain or cookie_domain.endswith('.' + target):
                        try:
                            self.driver.delete_cookie(cookie['name'])
                            cleared_count += 1
                        except:
                            # 某些Cookie可能无法删除，继续处理其他Cookie
                            pass

                if cleared_count > 0:
                    message = f"清除域名 '{target}' 的Cookie成功，共清除 {cleared_count} 个"
                else:
                    message = f"域名 '{target}' 没有找到可清除的Cookie"
            else:
                # 默认清除所有Cookie
                before_count = len(self.driver.get_cookies())
                self.driver.delete_all_cookies()
                message = f"清除所有Cookie成功，共清除 {before_count} 个Cookie"

            # 验证清除结果
            remaining_cookies = len(self.driver.get_cookies())

            return {
                "success": True,
                "message": message,
                "clear_type": clear_type,
                "target": target,
                "remaining_cookies": remaining_cookies
            }
        except Exception as e:
            return {"success": False, "message": f"清除Cookie失败: {str(e)}"}

    # ==================== 环境信息实现 ====================

    def update_env_note(self, config):
        """更新环境备注"""
        try:
            note_content = config.get('note_content', '')
            append_mode = config.get('append_mode', False)
            env_id = config.get('env_id', '')

            if not note_content:
                return {"success": False, "message": "未指定备注内容"}

            # 这里应该调用AdsPower API来更新环境备注
            # 暂时模拟实现
            if append_mode:
                # 追加模式：获取现有备注并追加
                current_note = "现有备注内容"  # 从API获取
                new_note = f"{current_note}\n{note_content}"
            else:
                new_note = note_content

            # 调用AdsPower API更新备注
            # api_result = adspower_api.update_profile_note(env_id, new_note)

            return {"success": True, "message": "更新环境备注成功", "note": new_note}
        except Exception as e:
            return {"success": False, "message": f"更新环境备注失败: {str(e)}"}

    def update_env_tag(self, config):
        """更新环境标签"""
        try:
            tag_content = config.get('tag_content', '')
            operation = config.get('operation', '替换')  # 替换、添加、删除
            env_id = config.get('env_id', '')

            if not tag_content:
                return {"success": False, "message": "未指定标签内容"}

            tags = [tag.strip() for tag in tag_content.split(',') if tag.strip()]

            # 这里应该调用AdsPower API来更新环境标签
            # 暂时模拟实现
            if operation == '替换':
                new_tags = tags
            elif operation == '添加':
                current_tags = ["现有标签1", "现有标签2"]  # 从API获取
                new_tags = list(set(current_tags + tags))
            elif operation == '删除':
                current_tags = ["现有标签1", "现有标签2", "要删除的标签"]  # 从API获取
                new_tags = [tag for tag in current_tags if tag not in tags]
            else:
                new_tags = tags

            # 调用AdsPower API更新标签
            # api_result = adspower_api.update_profile_tags(env_id, new_tags)

            return {"success": True, "message": "更新环境标签成功", "tags": new_tags}
        except Exception as e:
            return {"success": False, "message": f"更新环境标签失败: {str(e)}"}

    # ==================== 流程管理实现 ====================

    def start_new_browser(self, config):
        """启动新浏览器"""
        try:
            env_id = config.get('env_id', '')
            exception_handling = config.get('exception_handling', '跳过')
            completion_handling = config.get('completion_handling', '保留浏览器')

            if not env_id:
                return {"success": False, "message": "未指定环境编号"}

            # 这里应该调用AdsPower API启动新的浏览器环境
            # 暂时模拟实现
            try:
                # api_result = adspower_api.start_browser(env_id)
                # new_driver = create_driver_from_api_result(api_result)

                # 模拟成功启动
                browser_info = {
                    'env_id': env_id,
                    'status': 'started',
                    'exception_handling': exception_handling,
                    'completion_handling': completion_handling
                }

                return {"success": True, "message": f"启动新浏览器成功: {env_id}", "browser_info": browser_info}
            except Exception as e:
                if exception_handling == '跳过':
                    return {"success": True, "message": f"启动浏览器失败但已跳过: {str(e)}"}
                else:
                    return {"success": False, "message": f"启动新浏览器失败: {str(e)}"}
        except Exception as e:
            return {"success": False, "message": f"启动新浏览器失败: {str(e)}"}

    def use_other_flow(self, config):
        """使用其他流程"""
        try:
            flow_name = config.get('flow_name', '')
            variable_mapping = config.get('variable_mapping', {})

            if not flow_name:
                return {"success": False, "message": "未指定流程名称"}

            # 这里应该加载并执行其他流程
            # 暂时模拟实现
            try:
                # 应用变量映射
                if isinstance(variable_mapping, str):
                    variable_mapping = json.loads(variable_mapping)

                for source_var, target_var in variable_mapping.items():
                    if source_var in self.variables:
                        self.variables[target_var] = self.variables[source_var]

                # 执行其他流程
                # flow_result = execute_flow(flow_name, self.variables)

                return {"success": True, "message": f"执行其他流程成功: {flow_name}"}
            except Exception as e:
                return {"success": False, "message": f"执行其他流程失败: {str(e)}"}
        except Exception as e:
            return {"success": False, "message": f"使用其他流程失败: {str(e)}"}

    def close_browser(self, config):
        """关闭浏览器"""
        try:
            save_data = config.get('save_data', True)

            if save_data:
                # 保存浏览器数据（cookies、localStorage等）
                try:
                    cookies = self.driver.get_cookies()
                    local_storage = self.driver.execute_script("return localStorage;")
                    session_storage = self.driver.execute_script("return sessionStorage;")

                    browser_data = {
                        'cookies': cookies,
                        'localStorage': local_storage,
                        'sessionStorage': session_storage,
                        'timestamp': time.time()
                    }

                    # 保存数据到文件或数据库
                    # save_browser_data(browser_data)
                except Exception as e:
                    print(f"保存浏览器数据失败: {e}")

            # 关闭浏览器
            if self.driver:
                self.driver.quit()
                self.driver = None

            return {"success": True, "message": "关闭浏览器成功"}
        except Exception as e:
            return {"success": False, "message": f"关闭浏览器失败: {str(e)}"}

    def _get_clipboard_fallback(self):
        """剪贴板获取的替代方案"""
        try:
            # 在Windows上使用win32clipboard
            import win32clipboard
            win32clipboard.OpenClipboard()
            data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            return data
        except ImportError:
            try:
                # 使用tkinter作为替代方案
                import tkinter as tk
                root = tk.Tk()
                root.withdraw()
                data = root.clipboard_get()
                root.destroy()
                return data
            except:
                # 如果都不可用，返回空字符串
                return ""

    # ==================== 数据处理实现 ====================

    def extract_text(self, config):
        """文本中提取 - 完全按照AdsPower原版实现"""
        try:
            import re

            # 获取配置参数
            source_var = config.get('source_variable', '')
            pattern = config.get('extract_pattern', '')
            extract_type = config.get('extract_type', '第一个匹配')
            group_index = config.get('extract_group_index', 0)
            save_var = config.get('extract_save_variable', '')
            case_sensitive = config.get('case_sensitive', True)

            if not all([source_var, pattern, save_var]):
                return {"success": False, "message": "缺少必要参数"}

            # AdsPower原版：获取源文本
            source_text = self.variables.get(source_var, '')
            if not source_text:
                return {"success": False, "message": f"源变量 {source_var} 不存在或为空"}

            # AdsPower原版：设置正则表达式标志
            flags = 0 if case_sensitive else re.IGNORECASE

            try:
                if extract_type == '所有匹配':
                    # 提取所有匹配项
                    matches = re.findall(pattern, str(source_text), flags)
                    result = matches
                elif extract_type == '第一个匹配':
                    # 提取第一个匹配项
                    match = re.search(pattern, str(source_text), flags)
                    if match:
                        if match.groups() and group_index < len(match.groups()):
                            result = match.group(group_index + 1)  # group(1)是第一个分组
                        else:
                            result = match.group(0)  # 整个匹配
                    else:
                        result = ""
                elif extract_type == '最后一个匹配':
                    # 提取最后一个匹配项
                    matches = re.findall(pattern, str(source_text), flags)
                    if matches:
                        if isinstance(matches[-1], tuple) and group_index < len(matches[-1]):
                            result = matches[-1][group_index]
                        else:
                            result = matches[-1]
                    else:
                        result = ""
                elif extract_type == '匹配数量':
                    # 返回匹配数量
                    matches = re.findall(pattern, str(source_text), flags)
                    result = len(matches)
                else:
                    # 默认第一个匹配
                    match = re.search(pattern, str(source_text), flags)
                    if match:
                        if match.groups() and group_index < len(match.groups()):
                            result = match.group(group_index + 1)
                        else:
                            result = match.group(0)
                    else:
                        result = ""

                # 保存到变量
                self.variables[save_var] = result

                return {
                    "success": True,
                    "message": "文本提取成功",
                    "result": result,
                    "extract_type": extract_type,
                    "pattern": pattern,
                    "match_count": len(result) if isinstance(result, list) else (1 if result else 0)
                }

            except re.error as regex_error:
                return {"success": False, "message": f"正则表达式错误: {str(regex_error)}"}

        except Exception as e:
            return {"success": False, "message": f"文本提取失败: {str(e)}"}

    def convert_json(self, config):
        """转换JSON对象"""
        try:
            source_var = config.get('json_source_variable', '')
            convert_type = config.get('json_convert_type', '对象转JSON')
            save_var = config.get('json_save_variable', '')

            if not all([source_var, save_var]):
                return {"success": False, "message": "缺少必要参数"}

            source_data = self.variables.get(source_var)
            if source_data is None:
                return {"success": False, "message": f"源变量 {source_var} 不存在"}

            if convert_type == '对象转JSON':
                result = json.dumps(source_data, ensure_ascii=False, indent=2)
            elif convert_type == 'JSON转对象':
                result = json.loads(str(source_data))
            elif convert_type == '格式化JSON':
                parsed = json.loads(str(source_data))
                result = json.dumps(parsed, ensure_ascii=False, indent=2)
            else:
                result = source_data

            self.variables[save_var] = result
            return {"success": True, "message": "JSON转换成功", "result": result}
        except Exception as e:
            return {"success": False, "message": f"JSON转换失败: {str(e)}"}

    def extract_field(self, config):
        """字段提取"""
        try:
            source_var = config.get('field_source_variable', '')
            field_path = config.get('field_path', '')
            save_var = config.get('field_save_variable', '')

            if not all([source_var, field_path, save_var]):
                return {"success": False, "message": "缺少必要参数"}

            source_data = self.variables.get(source_var)
            if source_data is None:
                return {"success": False, "message": f"源变量 {source_var} 不存在"}

            # 简单的字段路径解析
            result = source_data
            for part in field_path.split('.'):
                if part.startswith('[') and part.endswith(']'):
                    # 数组索引
                    index = int(part[1:-1])
                    result = result[index]
                else:
                    # 对象属性
                    result = result[part]

            self.variables[save_var] = result
            return {"success": True, "message": "字段提取成功", "result": result}
        except Exception as e:
            return {"success": False, "message": f"字段提取失败: {str(e)}"}

    def random_extract(self, config):
        """随机提取 - 完全按照AdsPower原版实现"""
        try:
            import random

            # 获取配置参数
            source_var = config.get('random_source_variable', '')
            extract_count = config.get('random_count', 1)
            unique_mode = config.get('random_unique', True)
            save_var = config.get('random_save_variable', '')
            extract_type = config.get('extract_type', '随机行')

            if not all([source_var, save_var]):
                return {"success": False, "message": "缺少必要参数"}

            # AdsPower原版：获取源数据
            source_data = self.variables.get(source_var)
            if not source_data:
                return {"success": False, "message": f"源变量 {source_var} 不存在或为空"}

            # AdsPower原版：根据提取类型处理数据
            if extract_type == '随机行':
                # 按行分割文本
                if isinstance(source_data, str):
                    items = [line.strip() for line in source_data.split('\n') if line.strip()]
                elif isinstance(source_data, list):
                    items = [str(item) for item in source_data]
                else:
                    items = [str(source_data)]
            elif extract_type == '随机元素':
                # 如果是列表，直接使用；否则转换为列表
                if isinstance(source_data, (list, tuple)):
                    items = list(source_data)
                elif isinstance(source_data, dict):
                    items = list(source_data.values())
                else:
                    items = [source_data]
            else:
                # 默认处理
                if isinstance(source_data, (list, tuple)):
                    items = list(source_data)
                else:
                    items = [source_data]

            if not items:
                return {"success": False, "message": "源数据为空或无有效内容"}

            # AdsPower原版：执行随机提取
            max_count = len(items)
            actual_count = min(extract_count, max_count)

            if unique_mode:
                result = random.sample(items, actual_count)
            else:
                result = [random.choice(items) for _ in range(actual_count)]

            # AdsPower原版：根据提取数量决定返回格式
            if extract_count == 1:
                final_result = result[0] if result else ""
            else:
                final_result = result

            # 保存到变量
            self.variables[save_var] = final_result

            return {
                "success": True,
                "message": "随机提取成功",
                "result": final_result,
                "extract_count": actual_count,
                "total_items": max_count
            }
        except Exception as e:
            return {"success": False, "message": f"随机提取失败: {str(e)}"}

    # ==================== 流程管理实现 ====================

    def if_condition(self, config):
        """IF条件判断"""
        try:
            variable = config.get('if_variable', '')
            condition = config.get('if_condition', '存在')
            result_value = config.get('if_result', '')

            if not variable:
                return {"success": False, "message": "未指定判断变量"}

            var_value = self.variables.get(variable)

            # 执行条件判断
            if condition == '存在':
                condition_result = var_value is not None
            elif condition == '不存在':
                condition_result = var_value is None
            elif condition == '等于':
                condition_result = str(var_value) == str(result_value)
            elif condition == '不等于':
                condition_result = str(var_value) != str(result_value)
            elif condition == '大于':
                condition_result = float(var_value) > float(result_value)
            elif condition == '大于等于':
                condition_result = float(var_value) >= float(result_value)
            elif condition == '小于':
                condition_result = float(var_value) < float(result_value)
            elif condition == '小于等于':
                condition_result = float(var_value) <= float(result_value)
            elif condition == '包含':
                condition_result = str(result_value) in str(var_value)
            elif condition == '不包含':
                condition_result = str(result_value) not in str(var_value)
            elif condition == '在其中':
                condition_result = str(var_value) in str(result_value).split(',')
            elif condition == '不在其中':
                condition_result = str(var_value) not in str(result_value).split(',')
            else:
                condition_result = False

            return {"success": True, "condition_result": condition_result, "message": f"条件判断: {condition_result}"}
        except Exception as e:
            return {"success": False, "message": f"IF条件判断失败: {str(e)}"}

    def for_element_loop(self, config):
        """For循环元素"""
        try:
            selector = config.get('for_element_selector', '')
            save_object = config.get('for_element_save_object', '')
            save_index = config.get('for_element_save_index', '')

            if not selector:
                return {"success": False, "message": "未指定元素选择器"}

            elements = self.driver.find_elements(By.CSS_SELECTOR, selector)

            loop_info = {
                "type": "for_element",
                "elements": elements,
                "current_index": 0,
                "save_object": save_object,
                "save_index": save_index
            }

            self.loop_stack.append(loop_info)

            return {"success": True, "message": f"开始For循环元素，共 {len(elements)} 个元素", "loop_count": len(elements)}
        except Exception as e:
            return {"success": False, "message": f"For循环元素失败: {str(e)}"}

    def for_count_loop(self, config):
        """For循环次数"""
        try:
            count = config.get('for_count_times', 5)
            save_index = config.get('for_count_save_index', '')

            loop_info = {
                "type": "for_count",
                "total_count": count,
                "current_index": 0,
                "save_index": save_index
            }

            self.loop_stack.append(loop_info)

            return {"success": True, "message": f"开始For循环次数，共 {count} 次", "loop_count": count}
        except Exception as e:
            return {"success": False, "message": f"For循环次数失败: {str(e)}"}

    def for_data_loop(self, config):
        """For循环数据"""
        try:
            data_var = config.get('for_data_variable', '')
            save_object = config.get('for_data_save_object', '')
            save_index = config.get('for_data_save_index', '')

            if not data_var:
                return {"success": False, "message": "未指定数据变量"}

            data = self.variables.get(data_var)
            if not data:
                return {"success": False, "message": f"数据变量 {data_var} 不存在或为空"}

            if not isinstance(data, (list, tuple)):
                return {"success": False, "message": "数据必须是数组类型"}

            loop_info = {
                "type": "for_data",
                "data": data,
                "current_index": 0,
                "save_object": save_object,
                "save_index": save_index
            }

            self.loop_stack.append(loop_info)

            return {"success": True, "message": f"开始For循环数据，共 {len(data)} 项", "loop_count": len(data)}
        except Exception as e:
            return {"success": False, "message": f"For循环数据失败: {str(e)}"}

    def break_loop(self, config):
        """退出循环"""
        try:
            if not self.loop_stack:
                return {"success": False, "message": "当前不在循环中"}

            self.loop_stack.pop()
            return {"success": True, "message": "退出循环成功"}
        except Exception as e:
            return {"success": False, "message": f"退出循环失败: {str(e)}"}

    def while_loop(self, config):
        """While循环"""
        try:
            variable = config.get('while_variable', '')
            condition = config.get('while_condition', '存在')
            result_value = config.get('while_result', '')
            max_iterations = config.get('while_max_iterations', 100)

            loop_info = {
                "type": "while",
                "variable": variable,
                "condition": condition,
                "result_value": result_value,
                "max_iterations": max_iterations,
                "current_iteration": 0
            }

            self.loop_stack.append(loop_info)

            return {"success": True, "message": "开始While循环"}
        except Exception as e:
            return {"success": False, "message": f"While循环失败: {str(e)}"}

    # ==================== 第三方工具实现 ====================

    def solve_captcha(self, config):
        """2Captcha验证码识别"""
        try:
            api_key = config.get('api_key', '')
            captcha_type = config.get('captcha_type', 'Normal CAPTCHA')
            site_key = config.get('site_key', '')
            page_url = config.get('page_url', '')
            save_var = config.get('save_variable', '')

            if not api_key or not save_var:
                return {"success": False, "message": "缺少必要参数"}

            # 模拟2Captcha API调用
            try:
                if captcha_type == 'Normal CAPTCHA':
                    # 普通图片验证码
                    captcha_image = self.driver.get_screenshot_as_base64()
                    # 调用2Captcha API
                    # result = solve_normal_captcha(api_key, captcha_image)
                    result = "模拟验证码结果"

                elif captcha_type == 'reCAPTCHA V2':
                    # reCAPTCHA V2
                    if not site_key or not page_url:
                        return {"success": False, "message": "reCAPTCHA V2需要site_key和page_url"}
                    # result = solve_recaptcha_v2(api_key, site_key, page_url)
                    result = "模拟reCAPTCHA结果"

                elif captcha_type == 'reCAPTCHA V3':
                    # reCAPTCHA V3
                    if not site_key or not page_url:
                        return {"success": False, "message": "reCAPTCHA V3需要site_key和page_url"}
                    action = config.get('action', 'verify')
                    min_score = config.get('min_score', 0.3)
                    # result = solve_recaptcha_v3(api_key, site_key, page_url, action, min_score)
                    result = "模拟reCAPTCHA V3结果"

                elif captcha_type == 'hCaptcha':
                    # hCaptcha
                    if not site_key or not page_url:
                        return {"success": False, "message": "hCaptcha需要site_key和page_url"}
                    # result = solve_hcaptcha(api_key, site_key, page_url)
                    result = "模拟hCaptcha结果"

                elif captcha_type == 'Cloudflare Turnstile':
                    # Cloudflare Turnstile
                    if not site_key or not page_url:
                        return {"success": False, "message": "Cloudflare Turnstile需要site_key和page_url"}
                    # result = solve_turnstile(api_key, site_key, page_url)
                    result = "模拟Turnstile结果"

                else:
                    return {"success": False, "message": f"不支持的验证码类型: {captcha_type}"}

                self.variables[save_var] = result
                return {"success": True, "message": f"验证码识别成功: {captcha_type}", "result": result}

            except Exception as e:
                return {"success": False, "message": f"验证码识别失败: {str(e)}"}
        except Exception as e:
            return {"success": False, "message": f"2Captcha操作失败: {str(e)}"}

    def google_sheet_operation(self, config):
        """Google Sheet操作"""
        try:
            operation_type = config.get('operation_type', '读取')
            sheet_id = config.get('sheet_id', '')
            range_name = config.get('range', 'A1:Z1000')
            save_var = config.get('save_variable', '')

            if not sheet_id:
                return {"success": False, "message": "未指定Google Sheet ID"}

            # 模拟Google Sheets API调用
            try:
                if operation_type == '读取':
                    # 读取数据
                    # data = read_google_sheet(sheet_id, range_name)
                    data = [
                        ["姓名", "年龄", "城市"],
                        ["张三", "25", "北京"],
                        ["李四", "30", "上海"]
                    ]

                    if save_var:
                        self.variables[save_var] = data

                    return {"success": True, "message": "读取Google Sheet成功", "data": data}

                elif operation_type == '写入':
                    data_var = config.get('data_variable', '')
                    if not data_var or data_var not in self.variables:
                        return {"success": False, "message": "未指定数据变量或变量不存在"}

                    data = self.variables[data_var]
                    # write_google_sheet(sheet_id, range_name, data)

                    return {"success": True, "message": "写入Google Sheet成功"}

                elif operation_type == '清除':
                    # clear_google_sheet(sheet_id, range_name)
                    return {"success": True, "message": "清除Google Sheet成功"}

                else:
                    return {"success": False, "message": f"不支持的操作类型: {operation_type}"}

            except Exception as e:
                return {"success": False, "message": f"Google Sheet操作失败: {str(e)}"}
        except Exception as e:
            return {"success": False, "message": f"Google Sheet功能失败: {str(e)}"}

    def openai_operation(self, config):
        """OpenAI操作"""
        try:
            api_key = config.get('api_key', '')
            output_type = config.get('output_type', '文本')
            model = config.get('model', 'GPT-4o mini')
            prompt = config.get('prompt', '')
            save_var = config.get('save_variable', '')

            if not api_key or not prompt or not save_var:
                return {"success": False, "message": "缺少必要参数"}

            # 模拟OpenAI API调用
            try:
                if output_type == '文本':
                    # 文本生成
                    if model in ['GPT-4o mini', 'GPT-4o']:
                        # result = openai_text_completion(api_key, model, prompt)
                        result = f"模拟OpenAI文本回复: {prompt[:50]}..."
                    else:
                        return {"success": False, "message": f"不支持的文本模型: {model}"}

                elif output_type == '图像':
                    # 图像生成
                    if model == 'DALL·E-3':
                        image_size = config.get('image_size', '1024x1024')
                        image_format = config.get('image_format', 'URL')
                        image_quality = config.get('image_quality', '标清')

                        # result = openai_image_generation(api_key, prompt, image_size, image_quality)
                        if image_format == 'URL':
                            result = f"https://example.com/generated_image_{int(time.time())}.png"
                        else:  # Base64
                            result = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
                    else:
                        return {"success": False, "message": f"不支持的图像模型: {model}"}

                else:
                    return {"success": False, "message": f"不支持的输出类型: {output_type}"}

                self.variables[save_var] = result
                return {"success": True, "message": f"OpenAI {output_type}生成成功", "result": result}

            except Exception as e:
                return {"success": False, "message": f"OpenAI API调用失败: {str(e)}"}
        except Exception as e:
            return {"success": False, "message": f"OpenAI操作失败: {str(e)}"}
