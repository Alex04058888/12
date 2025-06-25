#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AdsPower工具专业版 - RPA执行器标准适配
完全按照AdsPower官方标准实现的RPA执行器
"""

import time
import json
import random
import os
from datetime import datetime
from typing import Dict, Any, Optional

class AdsPowerStandardExecutor:
    """AdsPower标准RPA执行器"""
    
    def __init__(self, driver=None, task_name="StandardRPA"):
        self.driver = driver
        self.task_name = task_name
        self.variables = {}
        self.execution_log = []
        
    def log_action(self, action: str, result: Dict[str, Any]):
        """记录执行动作"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "result": result
        }
        self.execution_log.append(log_entry)
    
    # ==================== 页面操作 - 完全按照AdsPower官方标准 ====================
    
    def click_element(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """点击元素 - 完全按照AdsPower官方标准"""
        try:
            # 使用官方标准参数名
            selector = config.get('selector', '')
            stored_element = config.get('stored_element')
            element_order = config.get('element_order', {})
            click_type = config.get('click_type', '鼠标左键')
            key_type = config.get('key_type', '单击')
            
            if not selector and not stored_element:
                return {"success": False, "message": "选择器或储存的元素对象不能为空"}
            
            # 处理元素顺序
            if isinstance(element_order, dict):
                order_type = element_order.get('type', '固定值')
                if order_type == '区间随机':
                    min_val = element_order.get('value', 1)
                    max_val = element_order.get('max_value', 1)
                    element_index = random.randint(min_val, max_val)
                else:
                    element_index = element_order.get('value', 1)
            else:
                element_index = element_order if element_order else 1
            
            # 转换点击类型
            click_type_map = {
                '鼠标左键': 'left',
                '鼠标中键': 'middle', 
                '鼠标右键': 'right'
            }
            selenium_click_type = click_type_map.get(click_type, 'left')
            
            # 转换按键类型
            is_double_click = (key_type == '双击')
            
            # 执行点击逻辑
            if self.driver:
                from selenium.webdriver.common.by import By
                from selenium.webdriver.common.action_chains import ActionChains
                
                # 查找元素
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if not elements:
                    return {"success": False, "message": f"未找到元素: {selector}"}
                
                if element_index > len(elements):
                    return {"success": False, "message": f"元素索引超出范围: {element_index}/{len(elements)}"}
                
                target_element = elements[element_index - 1]  # 转换为0基索引
                
                # 执行点击
                actions = ActionChains(self.driver)
                if selenium_click_type == 'right':
                    actions.context_click(target_element)
                elif selenium_click_type == 'middle':
                    # 中键点击需要特殊处理
                    self.driver.execute_script("arguments[0].click();", target_element)
                else:
                    if is_double_click:
                        actions.double_click(target_element)
                    else:
                        actions.click(target_element)
                
                actions.perform()
            
            result = {
                "success": True,
                "message": f"成功点击元素 - 选择器: {selector}, 索引: {element_index}, 类型: {click_type}({key_type})"
            }
            
            self.log_action("点击元素", result)
            return result
            
        except Exception as e:
            result = {"success": False, "message": f"点击元素失败: {str(e)}"}
            self.log_action("点击元素", result)
            return result
    
    def input_content(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """输入内容 - 完全按照AdsPower官方标准"""
        try:
            # 使用官方标准参数名
            selector = config.get('selector', '')
            stored_element = config.get('stored_element')
            element_order = config.get('element_order', 1)
            content = config.get('content', '')
            content_type = config.get('content_type', '顺序选取')
            input_interval = config.get('input_interval', 300)
            clear_before = config.get('clear_before', True)
            
            if not selector and not stored_element:
                return {"success": False, "message": "选择器或储存的元素对象不能为空"}
            
            if not content:
                return {"success": False, "message": "输入内容不能为空"}
            
            # 处理多行内容
            content_lines = content.strip().split('\n')
            
            # 根据内容类型选择内容
            if content_type == '随机选取':
                selected_content = random.choice(content_lines)
            elif content_type == '随机取数':
                # 假设内容格式为 "min-max"
                if '-' in content:
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
                selected_content = self.variables.get(var_name, content)
            else:  # 顺序选取
                # 这里可以根据环境ID或其他逻辑选择
                selected_content = content_lines[0]
            
            # 执行输入逻辑
            if self.driver:
                from selenium.webdriver.common.by import By
                from selenium.webdriver.common.keys import Keys
                
                # 查找元素
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if not elements:
                    return {"success": False, "message": f"未找到元素: {selector}"}
                
                if element_order > len(elements):
                    return {"success": False, "message": f"元素索引超出范围: {element_order}/{len(elements)}"}
                
                target_element = elements[element_order - 1]  # 转换为0基索引
                
                # 清除原内容
                if clear_before:
                    target_element.clear()
                    # 或者使用 Ctrl+A + Delete
                    target_element.send_keys(Keys.CONTROL + "a")
                    target_element.send_keys(Keys.DELETE)
                
                # 按间隔时间输入
                if input_interval > 0:
                    for char in selected_content:
                        target_element.send_keys(char)
                        time.sleep(input_interval / 1000.0)  # 转换为秒
                else:
                    target_element.send_keys(selected_content)
            
            result = {
                "success": True,
                "message": f"成功输入内容 - 选择器: {selector}, 内容长度: {len(selected_content)}"
            }
            
            self.log_action("输入内容", result)
            return result
            
        except Exception as e:
            result = {"success": False, "message": f"输入内容失败: {str(e)}"}
            self.log_action("输入内容", result)
            return result
    
    def wait_element(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """等待元素出现 - 完全按照AdsPower官方标准"""
        try:
            # 使用官方标准参数名
            selector = config.get('selector', '')
            element_order = config.get('element_order', 1)
            is_visible = config.get('is_visible', True)
            timeout = config.get('timeout', 30000)
            save_to = config.get('save_to', '')
            
            if not selector:
                return {"success": False, "message": "选择器不能为空"}
            
            # 转换超时时间为秒
            timeout_seconds = timeout / 1000.0
            
            start_time = time.time()
            element_found = False
            
            # 等待元素出现
            while time.time() - start_time < timeout_seconds:
                try:
                    if self.driver:
                        from selenium.webdriver.common.by import By
                        from selenium.webdriver.support.ui import WebDriverWait
                        from selenium.webdriver.support import expected_conditions as EC
                        
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        
                        if elements and len(elements) >= element_order:
                            target_element = elements[element_order - 1]
                            
                            if is_visible:
                                # 检查元素是否可见
                                if target_element.is_displayed():
                                    element_found = True
                                    break
                            else:
                                # 只检查元素是否存在
                                element_found = True
                                break
                    
                    time.sleep(0.5)  # 检查间隔0.5秒
                    
                except Exception:
                    time.sleep(0.5)
                    continue
            
            # 保存结果到变量
            if save_to:
                self.variables[save_to] = element_found
            
            if element_found:
                result = {
                    "success": True,
                    "message": f"元素已出现 - 选择器: {selector}, 等待时间: {time.time() - start_time:.2f}秒"
                }
            else:
                result = {
                    "success": False,
                    "message": f"等待元素超时 - 选择器: {selector}, 超时时间: {timeout_seconds}秒"
                }
            
            self.log_action("等待元素出现", result)
            return result
            
        except Exception as e:
            result = {"success": False, "message": f"等待元素失败: {str(e)}"}
            self.log_action("等待元素出现", result)
            return result
    
    def page_screenshot(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """页面截图 - 完全按照AdsPower官方标准"""
        try:
            # 使用官方标准参数名
            screenshot_name = config.get('screenshot_name', '')
            full_page = config.get('full_page', False)
            image_format = config.get('image_format', 'png')
            jpeg_quality = config.get('jpeg_quality', 80)
            
            # 生成截图文件名
            if not screenshot_name:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                screenshot_name = f"{self.task_name}_{timestamp}"
            
            # 确保文件扩展名正确
            if not screenshot_name.endswith(f'.{image_format}'):
                screenshot_name = f"{screenshot_name}.{image_format}"
            
            # 执行截图
            if self.driver:
                if full_page:
                    # 全页截图
                    original_size = self.driver.get_window_size()
                    required_width = self.driver.execute_script('return document.body.parentNode.scrollWidth')
                    required_height = self.driver.execute_script('return document.body.parentNode.scrollHeight')
                    self.driver.set_window_size(required_width, required_height)
                    
                    screenshot_data = self.driver.get_screenshot_as_png()
                    
                    # 恢复原始窗口大小
                    self.driver.set_window_size(original_size['width'], original_size['height'])
                else:
                    # 当前可见区域截图
                    screenshot_data = self.driver.get_screenshot_as_png()
                
                # 保存截图
                screenshots_dir = "screenshots"
                if not os.path.exists(screenshots_dir):
                    os.makedirs(screenshots_dir)
                
                screenshot_path = os.path.join(screenshots_dir, screenshot_name)
                
                if image_format == 'jpeg':
                    # 转换为JPEG格式
                    from PIL import Image
                    import io
                    
                    image = Image.open(io.BytesIO(screenshot_data))
                    image = image.convert('RGB')
                    image.save(screenshot_path, 'JPEG', quality=jpeg_quality)
                else:
                    # PNG格式
                    with open(screenshot_path, 'wb') as f:
                        f.write(screenshot_data)
            
            result = {
                "success": True,
                "message": f"截图成功 - 文件: {screenshot_name}, 格式: {image_format}, 全页: {full_page}",
                "screenshot_path": screenshot_path
            }
            
            self.log_action("页面截图", result)
            return result
            
        except Exception as e:
            result = {"success": False, "message": f"页面截图失败: {str(e)}"}
            self.log_action("页面截图", result)
            return result
    
    def wait_time(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """等待时间 - 完全按照AdsPower官方标准"""
        try:
            # 使用官方标准参数名
            wait_type = config.get('wait_type', '固定值')
            wait_time = config.get('wait_time', 3000)
            wait_min = config.get('wait_min', 2000)
            wait_max = config.get('wait_max', 5000)
            
            # 计算实际等待时间
            if wait_type == '区间随机':
                actual_wait = random.randint(wait_min, wait_max)
            else:
                actual_wait = wait_time
            
            # 转换为秒并等待
            wait_seconds = actual_wait / 1000.0
            time.sleep(wait_seconds)
            
            result = {
                "success": True,
                "message": f"等待完成 - 类型: {wait_type}, 时间: {actual_wait}毫秒"
            }
            
            self.log_action("等待时间", result)
            return result
            
        except Exception as e:
            result = {"success": False, "message": f"等待时间失败: {str(e)}"}
            self.log_action("等待时间", result)
            return result
    
    # ==================== 执行步骤的统一入口 ====================
    
    def execute_step(self, step_config: Dict[str, Any]) -> Dict[str, Any]:
        """执行单个步骤 - 使用AdsPower官方标准"""
        operation = step_config.get('operation', '')
        
        # 操作映射表
        operation_map = {
            '点击元素': self.click_element,
            '输入内容': self.input_content,
            '等待元素出现': self.wait_element,
            '页面截图': self.page_screenshot,
            '等待时间': self.wait_time,
            # 可以继续添加其他操作
        }
        
        if operation in operation_map:
            return operation_map[operation](step_config)
        else:
            return {
                "success": False,
                "message": f"不支持的操作: {operation}"
            }
    
    def get_execution_log(self) -> list:
        """获取执行日志"""
        return self.execution_log
    
    def clear_log(self):
        """清空执行日志"""
        self.execution_log.clear()
    
    def get_variables(self) -> dict:
        """获取所有变量"""
        return self.variables.copy()
    
    def set_variable(self, name: str, value: Any):
        """设置变量"""
        self.variables[name] = value
    
    def close(self):
        """关闭执行器"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
