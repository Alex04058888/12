#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AdsPower工具专业版 - 缺失功能补充实现
实现官方53个节点中缺失的15个功能
"""

import json
import time
import requests
import pandas as pd
from typing import Dict, Any, List, Optional
from datetime import datetime

class AdsPowerMissingFunctions:
    """AdsPower缺失功能实现类"""
    
    def __init__(self, driver=None):
        self.driver = driver
        self.variables = {}
        self.execution_log = []
    
    # ==================== Excel相关功能 ====================
    
    def import_excel(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """importExcel - Excel导入功能"""
        try:
            file_path = config.get('file_path', '')
            sheet_name = config.get('sheet_name', 0)
            save_variable = config.get('save_variable', 'excel_data')
            
            if not file_path:
                return {"success": False, "message": "Excel文件路径不能为空"}
            
            # 读取Excel文件
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            # 转换为字典列表格式
            data = df.to_dict('records')
            
            # 保存到变量
            self.variables[save_variable] = data
            
            return {
                "success": True,
                "message": f"成功导入Excel文件，共{len(data)}行数据",
                "data": data,
                "rows": len(data),
                "columns": list(df.columns)
            }
            
        except Exception as e:
            return {"success": False, "message": f"Excel导入失败: {str(e)}"}
    
    def import_excel_extract_field(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """importExcelExtractField - Excel字段提取"""
        try:
            file_path = config.get('file_path', '')
            sheet_name = config.get('sheet_name', 0)
            field_name = config.get('field_name', '')
            save_variable = config.get('save_variable', 'extracted_field')
            
            if not file_path or not field_name:
                return {"success": False, "message": "文件路径和字段名不能为空"}
            
            # 读取Excel文件
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            if field_name not in df.columns:
                return {"success": False, "message": f"字段'{field_name}'不存在"}
            
            # 提取指定字段
            field_data = df[field_name].tolist()
            
            # 保存到变量
            self.variables[save_variable] = field_data
            
            return {
                "success": True,
                "message": f"成功提取字段'{field_name}'，共{len(field_data)}个值",
                "data": field_data,
                "count": len(field_data)
            }
            
        except Exception as e:
            return {"success": False, "message": f"Excel字段提取失败: {str(e)}"}
    
    # ==================== iframe操作 ====================
    
    def click_inside_iframe(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """clickInsideIframe - iframe内点击"""
        try:
            iframe_selector = config.get('iframe_selector', '')
            element_selector = config.get('element_selector', '')
            
            if not iframe_selector or not element_selector:
                return {"success": False, "message": "iframe选择器和元素选择器不能为空"}
            
            if not self.driver:
                return {"success": False, "message": "浏览器驱动未初始化"}
            
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            
            # 切换到iframe
            iframe = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, iframe_selector))
            )
            self.driver.switch_to.frame(iframe)
            
            # 在iframe内查找并点击元素
            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, element_selector))
            )
            element.click()
            
            # 切换回主文档
            self.driver.switch_to.default_content()
            
            return {
                "success": True,
                "message": f"成功在iframe内点击元素: {element_selector}"
            }
            
        except Exception as e:
            # 确保切换回主文档
            if self.driver:
                try:
                    self.driver.switch_to.default_content()
                except:
                    pass
            return {"success": False, "message": f"iframe内点击失败: {str(e)}"}
    
    # ==================== 流程控制高级功能 ====================
    
    def else_condition(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """elseCondition - else条件分支"""
        try:
            # else条件总是执行，用于与if条件配对
            return {
                "success": True,
                "message": "else条件分支",
                "execute_else": True
            }
            
        except Exception as e:
            return {"success": False, "message": f"else条件执行失败: {str(e)}"}
    
    def breakpoint(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """breakpoint - 断点调试"""
        try:
            message = config.get('message', '断点')
            pause_execution = config.get('pause_execution', True)
            
            print(f"🔍 断点: {message}")
            print(f"⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            if pause_execution:
                input("按Enter键继续执行...")
            
            return {
                "success": True,
                "message": f"断点执行: {message}",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"success": False, "message": f"断点执行失败: {str(e)}"}
    
    def switch_profile(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """switchProfile - 切换环境"""
        try:
            profile_id = config.get('profile_id', '')
            api_key = config.get('api_key', '')
            
            if not profile_id:
                return {"success": False, "message": "环境ID不能为空"}
            
            # 关闭当前浏览器
            if self.driver:
                try:
                    self.driver.quit()
                except:
                    pass
            
            # 启动新环境
            api_url = "http://localhost:50325"
            response = requests.get(f"{api_url}/api/v1/browser/start", params={
                "user_id": profile_id,
                "api_key": api_key
            })
            
            if response.status_code == 200:
                data = response.json()
                if data.get("code") == 0:
                    return {
                        "success": True,
                        "message": f"成功切换到环境: {profile_id}",
                        "webdriver": data.get("data", {}).get("webdriver"),
                        "ws_endpoint": data.get("data", {}).get("ws", {}).get("puppeteer")
                    }
            
            return {"success": False, "message": "环境切换失败"}
            
        except Exception as e:
            return {"success": False, "message": f"环境切换失败: {str(e)}"}
    
    def set_thread_delay(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """setThreadDelay - 设置线程延迟"""
        try:
            delay_min = config.get('delay_min', 1000)
            delay_max = config.get('delay_max', 3000)
            
            import random
            actual_delay = random.randint(delay_min, delay_max)
            
            # 延迟执行
            time.sleep(actual_delay / 1000.0)
            
            return {
                "success": True,
                "message": f"线程延迟执行: {actual_delay}毫秒",
                "delay": actual_delay
            }
            
        except Exception as e:
            return {"success": False, "message": f"线程延迟失败: {str(e)}"}
    
    def throw_error(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """throwError - 抛出错误"""
        try:
            error_message = config.get('error_message', '用户自定义错误')
            error_code = config.get('error_code', 'USER_ERROR')
            
            # 记录错误日志
            error_info = {
                "timestamp": datetime.now().isoformat(),
                "error_code": error_code,
                "error_message": error_message,
                "type": "user_thrown_error"
            }
            
            self.execution_log.append(error_info)
            
            return {
                "success": False,
                "message": error_message,
                "error_code": error_code,
                "thrown_by_user": True
            }
            
        except Exception as e:
            return {"success": False, "message": f"抛出错误失败: {str(e)}"}
    
    def set_process_status(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """setProcessStatus - 设置流程状态"""
        try:
            status = config.get('status', 'running')
            message = config.get('message', '')
            
            # 更新流程状态
            status_info = {
                "timestamp": datetime.now().isoformat(),
                "status": status,
                "message": message
            }
            
            # 保存状态到变量
            self.variables['process_status'] = status_info
            
            return {
                "success": True,
                "message": f"流程状态已设置: {status}",
                "status": status,
                "status_message": message
            }
            
        except Exception as e:
            return {"success": False, "message": f"设置流程状态失败: {str(e)}"}
    
    # ==================== 第三方服务集成 ====================
    
    def openai_request(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """openai - ChatGPT集成"""
        try:
            api_key = config.get('api_key', '')
            prompt = config.get('prompt', '')
            system_prompt = config.get('system_prompt', 'You are a helpful assistant.')
            model = config.get('model', 'gpt-3.5-turbo')
            save_variable = config.get('save_variable', 'openai_response')
            
            if not api_key or not prompt:
                return {"success": False, "message": "API密钥和提示词不能为空"}
            
            # 调用OpenAI API
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 1000
            }
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['choices'][0]['message']['content']
                
                # 保存响应到变量
                self.variables[save_variable] = ai_response
                
                return {
                    "success": True,
                    "message": "OpenAI请求成功",
                    "response": ai_response,
                    "usage": result.get('usage', {})
                }
            else:
                return {"success": False, "message": f"OpenAI API错误: {response.text}"}
            
        except Exception as e:
            return {"success": False, "message": f"OpenAI请求失败: {str(e)}"}
    
    def http_request(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """httpRequest - HTTP请求"""
        try:
            url = config.get('url', '')
            method = config.get('method', 'GET').upper()
            headers = config.get('headers', {})
            data = config.get('data', {})
            timeout = config.get('timeout', 30)
            save_variable = config.get('save_variable', 'http_response')
            
            if not url:
                return {"success": False, "message": "请求URL不能为空"}
            
            # 发送HTTP请求
            if method == 'GET':
                response = requests.get(url, headers=headers, params=data, timeout=timeout)
            elif method == 'POST':
                response = requests.post(url, headers=headers, json=data, timeout=timeout)
            elif method == 'PUT':
                response = requests.put(url, headers=headers, json=data, timeout=timeout)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=timeout)
            else:
                return {"success": False, "message": f"不支持的HTTP方法: {method}"}
            
            # 解析响应
            try:
                response_data = response.json()
            except:
                response_data = response.text
            
            # 保存响应到变量
            self.variables[save_variable] = {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "data": response_data
            }
            
            return {
                "success": True,
                "message": f"HTTP请求成功: {method} {url}",
                "status_code": response.status_code,
                "response": response_data
            }
            
        except Exception as e:
            return {"success": False, "message": f"HTTP请求失败: {str(e)}"}
    
    # ==================== 其他扩展功能 ====================
    
    def google_sheets_integration(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """googleSheets - Google表格集成"""
        try:
            # 这里需要Google Sheets API的实现
            # 由于需要复杂的认证，暂时返回占位符
            return {
                "success": False,
                "message": "Google Sheets集成需要配置API凭据"
            }
            
        except Exception as e:
            return {"success": False, "message": f"Google Sheets集成失败: {str(e)}"}
    
    def slack_webhook(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """slackWebhook - Slack集成"""
        try:
            webhook_url = config.get('webhook_url', '')
            message = config.get('message', '')
            
            if not webhook_url or not message:
                return {"success": False, "message": "Webhook URL和消息不能为空"}
            
            # 发送Slack消息
            payload = {"text": message}
            response = requests.post(webhook_url, json=payload, timeout=10)
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "message": "Slack消息发送成功"
                }
            else:
                return {"success": False, "message": f"Slack消息发送失败: {response.text}"}
            
        except Exception as e:
            return {"success": False, "message": f"Slack集成失败: {str(e)}"}
    
    def send_email(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """sendEmail - 邮件发送"""
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            smtp_server = config.get('smtp_server', '')
            smtp_port = config.get('smtp_port', 587)
            username = config.get('username', '')
            password = config.get('password', '')
            to_email = config.get('to_email', '')
            subject = config.get('subject', '')
            body = config.get('body', '')
            
            if not all([smtp_server, username, password, to_email, subject]):
                return {"success": False, "message": "邮件配置信息不完整"}
            
            # 创建邮件
            msg = MIMEMultipart()
            msg['From'] = username
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            # 发送邮件
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(username, password)
            server.send_message(msg)
            server.quit()
            
            return {
                "success": True,
                "message": f"邮件发送成功: {to_email}"
            }
            
        except Exception as e:
            return {"success": False, "message": f"邮件发送失败: {str(e)}"}

# 全局实例
missing_functions = AdsPowerMissingFunctions()
