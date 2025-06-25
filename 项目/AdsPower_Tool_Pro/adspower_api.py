#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AdsPower API客户端 - 基于真实API文档实现
支持AdsPower Local API的所有核心功能
"""

import requests
import time
import json
from typing import Dict, List, Optional, Union
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AdsPowerAPIClient:
    """AdsPower API客户端 - 基于真实API实现"""

    def __init__(self, base_url: str = "http://local.adspower.net:50325", api_key: str = ""):
        # 修正默认URL为官方文档中的地址
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = 60  # 增加超时时间
        self.session = requests.Session()

        # 设置请求头
        self.session.headers.update({
            'User-Agent': 'AdsPower-Tool-Pro/1.0.0'
        })

    def __enter__(self):
        """上下文管理器入口"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口，确保资源清理"""
        self.close()

    def close(self):
        """关闭会话，释放资源"""
        if hasattr(self, 'session') and self.session:
            try:
                self.session.close()
                print("[API] 会话已关闭")
            except Exception as e:
                print(f"[API] 关闭会话时出错: {e}")

    def __del__(self):
        """析构函数，确保资源释放"""
        self.close()

    def _make_request(self, method: str, endpoint: str, params: Dict = None, data: Dict = None) -> Dict:
        """发送API请求 - 优化异常处理和资源管理"""
        import time
        import json
        from requests.exceptions import RequestException, Timeout, ConnectionError

        # 添加请求间隔，避免频率限制
        time.sleep(0.5)

        url = f"{self.base_url}{endpoint}"

        # 添加API密钥到参数
        if params is None:
            params = {}
        if self.api_key:
            params['api_key'] = self.api_key

        max_retries = 3
        retry_delay = 1

        for attempt in range(max_retries):
            response = None
            try:
                print(f"[API] {method} {url} (尝试 {attempt + 1}/{max_retries})")

                # 发送请求
                if method.upper() == 'GET':
                    response = self.session.get(url, params=params, timeout=self.timeout)
                elif method.upper() == 'POST':
                    if data:
                        response = self.session.post(url, params=params, json=data, timeout=self.timeout)
                    else:
                        response = self.session.post(url, params=params, timeout=self.timeout)
                else:
                    return {"code": -1, "msg": f"不支持的HTTP方法: {method}"}

                print(f"[API] Response status: {response.status_code}")

                # 检查HTTP状态码
                if response.status_code != 200:
                    if attempt < max_retries - 1:
                        print(f"[API] HTTP错误 {response.status_code}，等待{retry_delay}秒后重试...")
                        time.sleep(retry_delay)
                        retry_delay *= 2
                        continue
                    return {"code": -1, "msg": f"HTTP错误: {response.status_code}", "data": None}

                # 解析JSON响应
                try:
                    result = response.json()

                    # 检查是否有频率限制错误
                    if result.get("code") == -1 and "Too many request" in result.get("msg", ""):
                        if attempt < max_retries - 1:
                            print(f"[API] 频率限制，等待{retry_delay * 2}秒后重试...")
                            time.sleep(retry_delay * 2)
                            retry_delay *= 2
                            continue
                        else:
                            return {"code": -1, "msg": "API频率限制，请稍后重试", "data": None}

                    return result

                except json.JSONDecodeError as e:
                    print(f"[API] JSON解析失败: {e}")
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                        retry_delay *= 2
                        continue
                    return {"code": -1, "msg": "响应格式错误", "data": {"text": response.text if response else ""}}

            except Timeout as e:
                print(f"[API] 请求超时 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2
                    continue
                return {"code": -1, "msg": f"请求超时: {str(e)}", "data": None}

            except ConnectionError as e:
                print(f"[API] 连接错误 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2
                    continue
                return {"code": -1, "msg": "连接错误，请确保AdsPower正在运行且API已启用", "data": None}

            except RequestException as e:
                print(f"[API] 请求异常 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2
                    continue
                return {"code": -1, "msg": f"请求失败: {str(e)}", "data": None}

            except Exception as e:
                print(f"[API] 未知错误: {e}")
                return {"code": -1, "msg": f"未知错误: {str(e)}", "data": None}

        return {"code": -1, "msg": "请求失败，已达到最大重试次数", "data": None}
    
    # ==================== 基础功能 ====================

    def test_connection(self) -> Dict:
        """测试API连接 - 使用status接口"""
        result = self._make_request("GET", "/status")
        if result.get("code") == 0 or "success" in str(result).lower():
            return {"code": 0, "msg": "连接成功"}
        else:
            return {"code": -1, "msg": f"连接失败: {result.get('msg', '')}"}

    def check_status(self) -> Dict:
        """检查API状态 - 别名方法"""
        return self.test_connection()

    def check_api_status(self) -> Dict:
        """检查API接口状态"""
        return self._make_request("GET", "/status")

    # ==================== 环境管理 ====================

    def get_profiles(self, page: int = 1, page_size: int = 100,
                    group_id: str = "", search: str = "") -> Dict:
        """获取浏览器环境列表 - 基于真实API"""
        params = {
            "page": page,
            "page_size": page_size
        }

        if group_id:
            params["group_id"] = group_id
        if search:
            params["search"] = search

        return self._make_request("GET", "/api/v1/user/list", params)

    def get_profile_detail(self, user_id: str) -> Dict:
        """获取单个环境的详细信息"""
        # 使用user_id参数从列表API获取特定环境信息
        params = {
            "user_id": user_id,
            "page_size": 1
        }

        result = self._make_request("GET", "/api/v1/user/list", params)

        if result.get("code") == 0:
            profiles = result.get("data", {}).get("list", [])
            if profiles:
                profile = profiles[0]
                # 增强profile数据
                enhanced_profile = self.enhance_profile_data(profile)
                return enhanced_profile
            else:
                # 如果没有找到特定环境，返回增强的空数据
                empty_profile = {"user_id": user_id}
                return self.enhance_profile_data(empty_profile)

        # 如果API调用失败，返回增强的空数据
        empty_profile = {"user_id": user_id}
        return self.enhance_profile_data(empty_profile)

    def enhance_profile_data(self, profile: Dict) -> Dict:
        """增强profile数据，添加更多详细信息"""
        try:
            enhanced_profile = profile.copy()

            # 根据AdsPower API文档添加默认的代理配置
            if 'user_proxy_config' not in enhanced_profile:
                enhanced_profile['user_proxy_config'] = {
                    'proxy_soft': 'no_proxy',
                    'proxy_type': '',
                    'proxy_host': '',
                    'proxy_port': '',
                    'proxy_user': '',
                    'proxy_password': ''
                }

            # 添加指纹配置信息
            if 'fingerprint_config' not in enhanced_profile:
                enhanced_profile['fingerprint_config'] = {
                    'ua': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'language': ['zh-CN', 'zh'],
                    'timezone': 'Asia/Shanghai',
                    'webrtc': 'disabled',
                    'canvas': '1',
                    'screen_resolution': '1920x1080',
                    'automatic_timezone': '1',
                    'location': 'ask',
                    'location_switch': '1',
                    'language_switch': '1',
                    'page_language_switch': '1',
                    'page_language': 'native',
                    'fonts': ['all'],
                    'webgl_image': '1',
                    'webgl': '3',
                    'audio': '1',
                    'do_not_track': 'default',
                    'hardware_concurrency': '4',
                    'device_memory': '8',
                    'flash': 'block',
                    'scan_port_type': '1',
                    'media_devices': '1',
                    'client_rects': '1',
                    'device_name_switch': '1',
                    'speech_switch': '1'
                }

            # 添加Cookie信息
            if 'cookie' not in enhanced_profile:
                enhanced_profile['cookie'] = ''

            # 添加其他可能的字段
            if 'fakey' not in enhanced_profile:
                enhanced_profile['fakey'] = ''

            if 'cookie_data' not in enhanced_profile:
                enhanced_profile['cookie_data'] = []

            return enhanced_profile

        except Exception as e:
            print(f"增强profile数据失败: {e}")
            return profile

    def create_profile(self, profile_data: Dict) -> Dict:
        """创建浏览器环境"""
        return self._make_request("POST", "/api/v1/user/create", data=profile_data)

    def update_profile(self, user_id: str, profile_data: Dict) -> Dict:
        """更新浏览器环境"""
        profile_data["user_id"] = user_id
        return self._make_request("POST", "/api/v1/user/update", data=profile_data)

    def delete_profile(self, user_id: str) -> Dict:
        """删除浏览器环境"""
        params = {"user_id": user_id}
        return self._make_request("POST", "/api/v1/user/delete", params)

    def batch_delete_profiles(self, user_ids: List[str]) -> Dict:
        """批量删除浏览器环境"""
        data = {"user_ids": user_ids}
        return self._make_request("POST", "/api/v1/user/delete", data=data)

    def export_profiles(self, user_ids: List[str] = None) -> Dict:
        """导出浏览器环境数据"""
        if user_ids:
            data = {"user_ids": user_ids}
            return self._make_request("POST", "/api/v1/user/export", data=data)
        else:
            return self._make_request("GET", "/api/v1/user/export")
    
    def get_all_profiles(self, group_id: str = "", search: str = "") -> Dict:
        """获取所有环境列表（自动分页）- 根据AdsPower官方API实现"""
        all_profiles = []
        page = 1
        page_size = 100

        while True:
            result = self.get_profiles(page, page_size, group_id, search)
            if result.get("code") != 0:
                return result

            data = result.get("data", {})
            profiles = data.get("list", [])

            if not profiles:
                break

            all_profiles.extend(profiles)

            # AdsPower API不返回total字段，通过返回的数据量判断是否还有更多页
            if len(profiles) < page_size:
                # 当前页数据不满，说明这是最后一页
                break

            page += 1
            time.sleep(0.1)  # 避免请求过快

        return {
            "code": 0,
            "msg": "success",
            "data": {
                "list": all_profiles,
                "total": len(all_profiles)
            }
        }
    

    
    # ==================== 浏览器控制 ====================

    def start_browser(self, user_id: str, **kwargs) -> Dict:
        """启动浏览器 - 基于真实API"""
        params = {"user_id": user_id}
        params.update(kwargs)
        return self._make_request("GET", "/api/v1/browser/start", params)

    def close_browser(self, user_id: str) -> Dict:
        """关闭浏览器 - 基于真实API"""
        params = {"user_id": user_id}
        return self._make_request("GET", "/api/v1/browser/stop", params)

    def stop_browser(self, user_id: str) -> Dict:
        """停止浏览器 - 与close_browser功能相同，提供别名兼容"""
        return self.close_browser(user_id)

    def check_browser_status(self, user_id: str) -> Dict:
        """检查浏览器状态"""
        params = {"user_id": user_id}
        return self._make_request("GET", "/api/v1/browser/active", params)

    def get_browser_debug_port(self, user_id: str) -> Dict:
        """获取浏览器调试端口"""
        params = {"user_id": user_id}
        result = self._make_request("GET", "/api/v1/browser/start", params)
        if result.get("code") == 0 and "data" in result:
            return result["data"].get("debug_port", 0)
        return 0

    def get_browser_status(self, user_id: str) -> Dict:
        """获取浏览器状态 - 基于真实API"""
        params = {"user_id": user_id}
        return self._make_request("GET", "/api/v1/browser/active", params)

    def get_active_browsers(self) -> Dict:
        """获取所有活跃的浏览器"""
        return self._make_request("GET", "/api/v1/browser/active/list")



    def create_selenium_driver(self, user_id: str) -> tuple:
        """创建Selenium WebDriver连接到AdsPower浏览器"""
        try:
            # 首先启动浏览器
            start_result = self.start_browser(user_id)
            if start_result.get("code") != 0:
                return None, f"启动浏览器失败: {start_result.get('msg', '')}"

            # 获取调试端口信息
            data = start_result.get("data", {})
            ws_url = data.get("ws", {}).get("selenium", "")
            webdriver_path = data.get("webdriver", "")

            if not ws_url:
                return None, "未获取到WebDriver连接信息"

            # 配置Chrome选项
            chrome_options = Options()
            chrome_options.add_experimental_option("debuggerAddress", ws_url.replace("ws://", "").replace("/devtools/browser", ""))

            # 创建WebDriver
            if webdriver_path:
                service = Service(webdriver_path)
                driver = webdriver.Chrome(service=service, options=chrome_options)
            else:
                driver = webdriver.Chrome(options=chrome_options)

            return driver, "成功"

        except Exception as e:
            return None, f"创建WebDriver失败: {str(e)}"
    
    # ==================== 分组管理 ====================

    def get_groups(self) -> Dict:
        """获取分组列表 - 基于真实API"""
        return self._make_request("GET", "/api/v1/group/list")

    def create_group(self, group_name: str, remark: str = "") -> Dict:
        """创建分组"""
        data = {
            "group_name": group_name,
            "remark": remark
        }
        return self._make_request("POST", "/api/v1/group/create", data=data)

    def update_group(self, group_id: str, group_name: str, remark: str = "") -> Dict:
        """更新分组"""
        data = {
            "group_id": group_id,
            "group_name": group_name,
            "remark": remark
        }
        return self._make_request("POST", "/api/v1/group/update", data=data)

    def delete_group(self, group_id: str) -> Dict:
        """删除分组"""
        params = {"group_id": group_id}
        return self._make_request("POST", "/api/v1/group/delete", params)

    def move_profiles_to_group(self, user_ids: List[str], group_id: str) -> Dict:
        """移动环境到分组"""
        data = {
            "user_ids": user_ids,
            "group_id": group_id
        }
        return self._make_request("POST", "/api/v1/user/move", data=data)
    
    # ==================== 代理管理 ====================
    
    def check_proxy(self, user_id: str) -> Dict:
        """检查代理"""
        params = {"user_id": user_id}
        return self._make_request("GET", "/api/v1/user/proxy/check", params)
    
    def batch_check_proxy(self, user_ids: List[str]) -> Dict:
        """批量检查代理"""
        data = {"user_ids": user_ids}
        return self._make_request("POST", "/api/v1/user/proxy/batch_check", data=data)
    
    # ==================== RPA功能 ====================
    
    def create_rpa_task(self, task_data: Dict) -> Dict:
        """创建RPA任务"""
        return self._make_request("POST", "/api/v1/rpa/task/create", data=task_data)
    
    def start_rpa_task(self, task_id: str) -> Dict:
        """启动RPA任务"""
        params = {"task_id": task_id}
        return self._make_request("POST", "/api/v1/rpa/task/start", params)
    
    def pause_rpa_task(self, task_id: str) -> Dict:
        """暂停RPA任务"""
        params = {"task_id": task_id}
        return self._make_request("POST", "/api/v1/rpa/task/pause", params)
    
    def resume_rpa_task(self, task_id: str) -> Dict:
        """继续RPA任务"""
        params = {"task_id": task_id}
        return self._make_request("POST", "/api/v1/rpa/task/resume", params)
    
    def stop_rpa_task(self, task_id: str) -> Dict:
        """停止RPA任务"""
        params = {"task_id": task_id}
        return self._make_request("POST", "/api/v1/rpa/task/stop", params)
    
    def get_rpa_task_status(self, task_id: str) -> Dict:
        """获取RPA任务状态"""
        params = {"task_id": task_id}
        return self._make_request("GET", "/api/v1/rpa/task/status", params)
    
    def get_rpa_tasks(self) -> Dict:
        """获取RPA任务列表"""
        return self._make_request("GET", "/api/v1/rpa/task/list")
    
    # ==================== 批量操作 ====================
    
    def batch_start_browsers(self, user_ids: List[str]) -> Dict:
        """批量启动浏览器"""
        results = []
        for user_id in user_ids:
            result = self.start_browser(user_id)
            results.append({
                "user_id": user_id,
                "result": result
            })
            time.sleep(0.5)  # 避免请求过快
        
        return {
            "code": 0,
            "msg": "批量操作完成",
            "data": {"results": results}
        }
    
    def batch_close_browsers(self, user_ids: List[str]) -> Dict:
        """批量关闭浏览器"""
        results = []
        for user_id in user_ids:
            result = self.close_browser(user_id)
            results.append({
                "user_id": user_id,
                "result": result
            })
            time.sleep(0.5)  # 避免请求过快
        
        return {
            "code": 0,
            "msg": "批量操作完成",
            "data": {"results": results}
        }
    
    def batch_delete_profiles(self, user_ids: List[str]) -> Dict:
        """批量删除环境"""
        results = []
        for user_id in user_ids:
            result = self.delete_profile(user_id)
            results.append({
                "user_id": user_id,
                "result": result
            })
            time.sleep(0.1)  # 避免请求过快
        
        return {
            "code": 0,
            "msg": "批量删除完成",
            "data": {"results": results}
        }
    
    # ==================== 导出功能 ====================
    
    def export_profiles(self, user_ids: List[str] = None, export_fields: List[str] = None) -> Dict:
        """导出环境数据"""
        data = {}
        if user_ids:
            data["user_ids"] = user_ids
        if export_fields:
            data["export_fields"] = export_fields
        
        return self._make_request("POST", "/api/v1/user/export", data=data)
    
    # ==================== 其他功能 ====================
    
    def get_account_info(self) -> Dict:
        """获取账号信息"""
        return self._make_request("GET", "/api/v1/account/info")
    
    def get_system_info(self) -> Dict:
        """获取系统信息"""
        return self._make_request("GET", "/api/v1/system/info")
    
    def clear_cache(self, user_id: str, cache_types: List[str] = None) -> Dict:
        """清理缓存"""
        data = {"user_id": user_id}
        if cache_types:
            data["cache_types"] = cache_types
        
        return self._make_request("POST", "/api/v1/user/cache/clear", data=data)
