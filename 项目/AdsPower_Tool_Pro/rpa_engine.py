#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AdsPower RPA执行引擎
支持多种自动化操作和脚本执行
"""

import time
import json
import random
from typing import Dict, List, Any, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class RPAEngine:
    """RPA执行引擎 - 优化资源管理"""

    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10) if driver else None
        self.actions = ActionChains(driver) if driver else None
        self.execution_log = []
        self._is_closed = False
        
    def log_action(self, action: str, result: str = "成功", details: str = ""):
        """记录操作日志"""
        log_entry = {
            "timestamp": time.time(),
            "action": action,
            "result": result,
            "details": details
        }
        self.execution_log.append(log_entry)
        print(f"[RPA] {action} - {result} {details}")

    def __enter__(self):
        """上下文管理器入口"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口，确保资源清理"""
        self.close()

    def close(self):
        """关闭RPA引擎，释放资源"""
        if self._is_closed:
            return

        try:
            if self.driver:
                # 清理WebDriver资源
                try:
                    self.driver.quit()
                    print("[RPA] WebDriver已关闭")
                except Exception as e:
                    print(f"[RPA] 关闭WebDriver时出错: {e}")

            self._is_closed = True

        except Exception as e:
            print(f"[RPA] 关闭RPA引擎时出错: {e}")

    def __del__(self):
        """析构函数，确保资源释放"""
        if not self._is_closed:
            self.close()

    def is_valid(self):
        """检查引擎是否有效"""
        return not self._is_closed and self.driver is not None
    
    def wait_random(self, min_seconds: float = 1.0, max_seconds: float = 3.0):
        """随机等待，模拟人类操作"""
        wait_time = random.uniform(min_seconds, max_seconds)
        time.sleep(wait_time)
    
    def navigate_to_url(self, url: str) -> bool:
        """导航到指定URL"""
        if not self.is_valid():
            self.log_action("导航失败", "失败", "RPA引擎已关闭")
            return False

        try:
            self.driver.get(url)
            self.log_action(f"导航到 {url}")
            self.wait_random()
            return True
        except Exception as e:
            self.log_action(f"导航到 {url}", "失败", str(e))
            return False
    
    def find_element_safe(self, by: By, value: str, timeout: int = 10):
        """安全查找元素"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.presence_of_element_located((by, value)))
            return element
        except TimeoutException:
            return None
    
    def click_element(self, by: By, value: str, timeout: int = 10) -> bool:
        """点击元素"""
        try:
            element = self.find_element_safe(by, value, timeout)
            if element:
                # 滚动到元素可见
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                self.wait_random(0.5, 1.0)
                
                # 点击元素
                element.click()
                self.log_action(f"点击元素 {value}")
                self.wait_random()
                return True
            else:
                self.log_action(f"点击元素 {value}", "失败", "元素未找到")
                return False
        except Exception as e:
            self.log_action(f"点击元素 {value}", "失败", str(e))
            return False
    
    def input_text(self, by: By, value: str, text: str, clear_first: bool = True, timeout: int = 10) -> bool:
        """输入文本"""
        try:
            element = self.find_element_safe(by, value, timeout)
            if element:
                # 滚动到元素可见
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                self.wait_random(0.5, 1.0)
                
                # 清空输入框
                if clear_first:
                    element.clear()
                    self.wait_random(0.2, 0.5)
                
                # 模拟人类输入
                for char in text:
                    element.send_keys(char)
                    time.sleep(random.uniform(0.05, 0.15))
                
                self.log_action(f"输入文本到 {value}", "成功", f"文本: {text}")
                self.wait_random()
                return True
            else:
                self.log_action(f"输入文本到 {value}", "失败", "元素未找到")
                return False
        except Exception as e:
            self.log_action(f"输入文本到 {value}", "失败", str(e))
            return False
    
    def wait_for_element(self, by: By, value: str, timeout: int = 30) -> bool:
        """等待元素出现"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.presence_of_element_located((by, value)))
            self.log_action(f"等待元素 {value}", "成功")
            return True
        except TimeoutException:
            self.log_action(f"等待元素 {value}", "失败", "超时")
            return False
    
    def scroll_page(self, direction: str = "down", pixels: int = 500) -> bool:
        """滚动页面"""
        try:
            if direction.lower() == "down":
                self.driver.execute_script(f"window.scrollBy(0, {pixels});")
            elif direction.lower() == "up":
                self.driver.execute_script(f"window.scrollBy(0, -{pixels});")
            elif direction.lower() == "top":
                self.driver.execute_script("window.scrollTo(0, 0);")
            elif direction.lower() == "bottom":
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            self.log_action(f"滚动页面 {direction}")
            self.wait_random()
            return True
        except Exception as e:
            self.log_action(f"滚动页面 {direction}", "失败", str(e))
            return False
    
    def take_screenshot(self, filename: str = None) -> bool:
        """截图"""
        try:
            if filename is None:
                filename = f"screenshot_{int(time.time())}.png"
            
            self.driver.save_screenshot(filename)
            self.log_action("截图", "成功", f"文件: {filename}")
            return True
        except Exception as e:
            self.log_action("截图", "失败", str(e))
            return False
    
    def execute_javascript(self, script: str) -> Any:
        """执行JavaScript代码"""
        try:
            result = self.driver.execute_script(script)
            self.log_action("执行JavaScript", "成功", f"脚本: {script[:50]}...")
            return result
        except Exception as e:
            self.log_action("执行JavaScript", "失败", str(e))
            return None
    
    def switch_to_frame(self, frame_reference) -> bool:
        """切换到iframe"""
        try:
            self.driver.switch_to.frame(frame_reference)
            self.log_action(f"切换到frame {frame_reference}")
            return True
        except Exception as e:
            self.log_action(f"切换到frame {frame_reference}", "失败", str(e))
            return False
    
    def switch_to_default_content(self) -> bool:
        """切换回主页面"""
        try:
            self.driver.switch_to.default_content()
            self.log_action("切换回主页面")
            return True
        except Exception as e:
            self.log_action("切换回主页面", "失败", str(e))
            return False
    
    def handle_alert(self, action: str = "accept") -> bool:
        """处理弹窗"""
        try:
            alert = self.driver.switch_to.alert
            if action.lower() == "accept":
                alert.accept()
            elif action.lower() == "dismiss":
                alert.dismiss()
            
            self.log_action(f"处理弹窗 {action}")
            return True
        except Exception as e:
            self.log_action(f"处理弹窗 {action}", "失败", str(e))
            return False
    
    def execute_rpa_script(self, script_data: Dict) -> Dict:
        """执行RPA脚本"""
        try:
            script_name = script_data.get("name", "未命名脚本")
            steps = script_data.get("steps", [])
            
            self.log_action(f"开始执行RPA脚本: {script_name}")
            
            success_count = 0
            total_steps = len(steps)
            
            for i, step in enumerate(steps):
                step_type = step.get("type", "")
                step_params = step.get("params", {})
                
                self.log_action(f"执行步骤 {i+1}/{total_steps}: {step_type}")
                
                success = False
                
                if step_type == "navigate":
                    success = self.navigate_to_url(step_params.get("url", ""))
                
                elif step_type == "click":
                    by_type = getattr(By, step_params.get("by", "XPATH").upper())
                    success = self.click_element(by_type, step_params.get("value", ""))
                
                elif step_type == "input":
                    by_type = getattr(By, step_params.get("by", "XPATH").upper())
                    success = self.input_text(
                        by_type, 
                        step_params.get("value", ""), 
                        step_params.get("text", ""),
                        step_params.get("clear_first", True)
                    )
                
                elif step_type == "wait":
                    wait_time = step_params.get("seconds", 1)
                    time.sleep(wait_time)
                    success = True
                
                elif step_type == "scroll":
                    success = self.scroll_page(
                        step_params.get("direction", "down"),
                        step_params.get("pixels", 500)
                    )
                
                elif step_type == "screenshot":
                    success = self.take_screenshot(step_params.get("filename"))
                
                elif step_type == "javascript":
                    result = self.execute_javascript(step_params.get("script", ""))
                    success = result is not None
                
                if success:
                    success_count += 1
                
                # 检查是否需要在失败时停止
                if not success and step_params.get("stop_on_error", False):
                    self.log_action(f"脚本执行中断", "失败", f"步骤 {i+1} 失败")
                    break
            
            # 返回执行结果
            result = {
                "success": success_count == total_steps,
                "total_steps": total_steps,
                "success_steps": success_count,
                "failed_steps": total_steps - success_count,
                "execution_log": self.execution_log.copy()
            }
            
            self.log_action(f"RPA脚本执行完成", "成功" if result["success"] else "部分失败", 
                          f"成功: {success_count}/{total_steps}")
            
            return result
            
        except Exception as e:
            self.log_action("RPA脚本执行", "失败", str(e))
            return {
                "success": False,
                "error": str(e),
                "execution_log": self.execution_log.copy()
            }
    
    def get_execution_log(self) -> List[Dict]:
        """获取执行日志"""
        return self.execution_log.copy()
    
    def clear_log(self):
        """清空执行日志"""
        self.execution_log.clear()
        self.log_action("清空执行日志")
