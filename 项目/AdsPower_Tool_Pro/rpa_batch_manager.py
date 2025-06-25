#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AdsPower工具专业版 - RPA批量操作管理器
提供完整的RPA批量操作浏览器功能
"""

import time
import json
import threading
import concurrent.futures
from datetime import datetime
from typing import List, Dict, Any, Optional, Callable
from enum import Enum

class BatchExecutionMode(Enum):
    """批量执行模式"""
    SEQUENTIAL = "sequential"  # 顺序执行
    PARALLEL = "parallel"     # 并行执行
    RANDOM = "random"         # 随机顺序执行

class BatchTaskStatus(Enum):
    """批量任务状态"""
    PENDING = "pending"       # 等待中
    RUNNING = "running"       # 执行中
    COMPLETED = "completed"   # 已完成
    FAILED = "failed"         # 失败
    CANCELLED = "cancelled"   # 已取消

class RPABatchTask:
    """RPA批量任务"""
    
    def __init__(self, task_id: str, env_ids: List[str], flow_data: Dict[str, Any], 
                 execution_mode: BatchExecutionMode = BatchExecutionMode.SEQUENTIAL,
                 max_parallel: int = 3):
        self.task_id = task_id
        self.env_ids = env_ids
        self.flow_data = flow_data
        self.execution_mode = execution_mode
        self.max_parallel = max_parallel
        
        self.status = BatchTaskStatus.PENDING
        self.start_time = None
        self.end_time = None
        self.progress = 0
        self.current_env = None
        
        # 执行结果
        self.results = {}
        self.success_count = 0
        self.failed_count = 0
        self.error_messages = []
        
        # 回调函数
        self.progress_callback = None
        self.completion_callback = None

class RPABatchManager:
    """RPA批量操作管理器"""
    
    def __init__(self):
        self.tasks = {}
        self.running_tasks = {}
        self.task_counter = 0
        self.max_concurrent_tasks = 2
        
        # 导入必要模块
        try:
            from adspower_api import AdsPowerAPIClient
            from rpa_executor import RPAExecutor
            self.api_client = AdsPowerAPIClient()
            self.rpa_available = True
        except ImportError:
            self.api_client = None
            self.rpa_available = False
    
    def create_batch_task(self, env_ids: List[str], flow_data: Dict[str, Any],
                         execution_mode: BatchExecutionMode = BatchExecutionMode.SEQUENTIAL,
                         max_parallel: int = 3) -> str:
        """创建批量任务"""
        self.task_counter += 1
        task_id = f"batch_task_{self.task_counter}_{int(time.time())}"
        
        task = RPABatchTask(
            task_id=task_id,
            env_ids=env_ids,
            flow_data=flow_data,
            execution_mode=execution_mode,
            max_parallel=max_parallel
        )
        
        self.tasks[task_id] = task
        return task_id
    
    def start_batch_task(self, task_id: str, 
                        progress_callback: Optional[Callable] = None,
                        completion_callback: Optional[Callable] = None) -> bool:
        """启动批量任务"""
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        if task.status != BatchTaskStatus.PENDING:
            return False
        
        # 检查并发任务数量
        if len(self.running_tasks) >= self.max_concurrent_tasks:
            return False
        
        # 设置回调函数
        task.progress_callback = progress_callback
        task.completion_callback = completion_callback
        
        # 启动任务
        task.status = BatchTaskStatus.RUNNING
        task.start_time = datetime.now()
        self.running_tasks[task_id] = task
        
        # 根据执行模式启动任务
        if task.execution_mode == BatchExecutionMode.PARALLEL:
            thread = threading.Thread(target=self._execute_parallel_task, args=(task,))
        else:
            thread = threading.Thread(target=self._execute_sequential_task, args=(task,))
        
        thread.daemon = True
        thread.start()
        
        return True
    
    def _execute_sequential_task(self, task: RPABatchTask):
        """执行顺序批量任务"""
        try:
            env_list = list(task.env_ids)
            
            # 随机模式下打乱顺序
            if task.execution_mode == BatchExecutionMode.RANDOM:
                import random
                random.shuffle(env_list)
            
            total_envs = len(env_list)
            
            for i, env_id in enumerate(env_list):
                if task.status == BatchTaskStatus.CANCELLED:
                    break
                
                # 更新当前环境和进度
                task.current_env = env_id
                task.progress = int((i / total_envs) * 100)
                
                # 执行回调
                if task.progress_callback:
                    task.progress_callback(task.task_id, task.progress, env_id)
                
                # 执行单个环境的RPA任务
                result = self._execute_single_env_task(env_id, task.flow_data)
                task.results[env_id] = result
                
                if result.get("success", False):
                    task.success_count += 1
                else:
                    task.failed_count += 1
                    task.error_messages.append(f"{env_id}: {result.get('error', '未知错误')}")
                
                # 环境间延迟
                time.sleep(1)
            
            # 任务完成
            task.progress = 100
            task.status = BatchTaskStatus.COMPLETED if task.failed_count == 0 else BatchTaskStatus.FAILED
            
        except Exception as e:
            task.status = BatchTaskStatus.FAILED
            task.error_messages.append(f"批量任务执行异常: {str(e)}")
        
        finally:
            task.end_time = datetime.now()
            if task_id in self.running_tasks:
                del self.running_tasks[task.task_id]
            
            # 执行完成回调
            if task.completion_callback:
                task.completion_callback(task.task_id, task.status, task.results)
    
    def _execute_parallel_task(self, task: RPABatchTask):
        """执行并行批量任务"""
        try:
            env_list = list(task.env_ids)
            
            # 随机模式下打乱顺序
            if task.execution_mode == BatchExecutionMode.RANDOM:
                import random
                random.shuffle(env_list)
            
            total_envs = len(env_list)
            completed_count = 0
            
            # 使用线程池执行并行任务
            with concurrent.futures.ThreadPoolExecutor(max_workers=task.max_parallel) as executor:
                # 提交所有任务
                future_to_env = {
                    executor.submit(self._execute_single_env_task, env_id, task.flow_data): env_id
                    for env_id in env_list
                }
                
                # 处理完成的任务
                for future in concurrent.futures.as_completed(future_to_env):
                    if task.status == BatchTaskStatus.CANCELLED:
                        break
                    
                    env_id = future_to_env[future]
                    
                    try:
                        result = future.result()
                        task.results[env_id] = result
                        
                        if result.get("success", False):
                            task.success_count += 1
                        else:
                            task.failed_count += 1
                            task.error_messages.append(f"{env_id}: {result.get('error', '未知错误')}")
                        
                    except Exception as e:
                        task.failed_count += 1
                        task.error_messages.append(f"{env_id}: 执行异常 - {str(e)}")
                    
                    # 更新进度
                    completed_count += 1
                    task.progress = int((completed_count / total_envs) * 100)
                    
                    # 执行进度回调
                    if task.progress_callback:
                        task.progress_callback(task.task_id, task.progress, env_id)
            
            # 任务完成
            task.status = BatchTaskStatus.COMPLETED if task.failed_count == 0 else BatchTaskStatus.FAILED
            
        except Exception as e:
            task.status = BatchTaskStatus.FAILED
            task.error_messages.append(f"并行任务执行异常: {str(e)}")
        
        finally:
            task.end_time = datetime.now()
            if task.task_id in self.running_tasks:
                del self.running_tasks[task.task_id]
            
            # 执行完成回调
            if task.completion_callback:
                task.completion_callback(task.task_id, task.status, task.results)
    
    def _execute_single_env_task(self, env_id: str, flow_data: Dict[str, Any]) -> Dict[str, Any]:
        """执行单个环境的RPA任务"""
        if not self.rpa_available:
            return {"success": False, "error": "RPA功能不可用"}
        
        try:
            # 导入RPA执行器
            from rpa_executor import RPAExecutor
            
            # 创建执行器
            executor = RPAExecutor(task_name=f"BatchTask-{env_id}")
            
            # 连接到AdsPower浏览器
            connect_result = executor.connect_to_adspower_browser(env_id)
            if not connect_result.get("success"):
                return {"success": False, "error": f"连接浏览器失败: {connect_result.get('message')}"}
            
            # 执行流程步骤
            steps = flow_data.get('steps', [])
            step_results = []
            
            for step in steps:
                step_result = executor.execute_step(step)
                step_results.append(step_result)
                
                # 如果步骤失败且设置为停止，则终止执行
                if not step_result.get("success") and step.get("on_error") == "stop":
                    executor.disconnect_from_adspower_browser()
                    return {
                        "success": False,
                        "error": f"步骤执行失败: {step_result.get('message')}",
                        "completed_steps": len(step_results)
                    }
            
            # 断开浏览器连接
            executor.disconnect_from_adspower_browser()
            
            return {
                "success": True,
                "message": "RPA任务执行成功",
                "completed_steps": len(step_results),
                "step_results": step_results
            }
            
        except Exception as e:
            return {"success": False, "error": f"RPA任务执行异常: {str(e)}"}
    
    def cancel_batch_task(self, task_id: str) -> bool:
        """取消批量任务"""
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        if task.status == BatchTaskStatus.RUNNING:
            task.status = BatchTaskStatus.CANCELLED
            return True
        
        return False
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """获取任务状态"""
        if task_id not in self.tasks:
            return None
        
        task = self.tasks[task_id]
        
        return {
            "task_id": task.task_id,
            "status": task.status.value,
            "progress": task.progress,
            "current_env": task.current_env,
            "total_envs": len(task.env_ids),
            "success_count": task.success_count,
            "failed_count": task.failed_count,
            "start_time": task.start_time.isoformat() if task.start_time else None,
            "end_time": task.end_time.isoformat() if task.end_time else None,
            "execution_mode": task.execution_mode.value,
            "error_messages": task.error_messages[-5:]  # 最近5个错误
        }
    
    def get_task_results(self, task_id: str) -> Optional[Dict[str, Any]]:
        """获取任务详细结果"""
        if task_id not in self.tasks:
            return None
        
        task = self.tasks[task_id]
        
        return {
            "task_id": task.task_id,
            "status": task.status.value,
            "results": task.results,
            "summary": {
                "total_envs": len(task.env_ids),
                "success_count": task.success_count,
                "failed_count": task.failed_count,
                "success_rate": (task.success_count / len(task.env_ids)) * 100 if task.env_ids else 0
            },
            "error_messages": task.error_messages
        }
    
    def cleanup_completed_tasks(self, keep_recent: int = 10):
        """清理已完成的任务"""
        completed_tasks = [
            (task_id, task) for task_id, task in self.tasks.items()
            if task.status in [BatchTaskStatus.COMPLETED, BatchTaskStatus.FAILED, BatchTaskStatus.CANCELLED]
        ]
        
        # 按结束时间排序，保留最近的任务
        completed_tasks.sort(key=lambda x: x[1].end_time or datetime.min, reverse=True)
        
        # 删除多余的任务
        for task_id, task in completed_tasks[keep_recent:]:
            del self.tasks[task_id]
    
    def get_all_tasks_summary(self) -> Dict[str, Any]:
        """获取所有任务摘要"""
        summary = {
            "total_tasks": len(self.tasks),
            "running_tasks": len(self.running_tasks),
            "pending_tasks": 0,
            "completed_tasks": 0,
            "failed_tasks": 0,
            "cancelled_tasks": 0
        }
        
        for task in self.tasks.values():
            if task.status == BatchTaskStatus.PENDING:
                summary["pending_tasks"] += 1
            elif task.status == BatchTaskStatus.COMPLETED:
                summary["completed_tasks"] += 1
            elif task.status == BatchTaskStatus.FAILED:
                summary["failed_tasks"] += 1
            elif task.status == BatchTaskStatus.CANCELLED:
                summary["cancelled_tasks"] += 1
        
        return summary

# 全局批量管理器实例
rpa_batch_manager = RPABatchManager()

# 便捷函数
def create_batch_rpa_task(env_ids: List[str], flow_data: Dict[str, Any],
                         execution_mode: str = "sequential", max_parallel: int = 3) -> str:
    """创建批量RPA任务"""
    mode_map = {
        "sequential": BatchExecutionMode.SEQUENTIAL,
        "parallel": BatchExecutionMode.PARALLEL,
        "random": BatchExecutionMode.RANDOM
    }
    
    mode = mode_map.get(execution_mode, BatchExecutionMode.SEQUENTIAL)
    return rpa_batch_manager.create_batch_task(env_ids, flow_data, mode, max_parallel)

def start_batch_rpa_task(task_id: str, progress_callback=None, completion_callback=None) -> bool:
    """启动批量RPA任务"""
    return rpa_batch_manager.start_batch_task(task_id, progress_callback, completion_callback)

def get_batch_task_status(task_id: str) -> Optional[Dict[str, Any]]:
    """获取批量任务状态"""
    return rpa_batch_manager.get_task_status(task_id)

def cancel_batch_rpa_task(task_id: str) -> bool:
    """取消批量RPA任务"""
    return rpa_batch_manager.cancel_batch_task(task_id)
