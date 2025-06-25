#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RPA多线程执行管理器
实现多线程RPA执行控制，支持同时运行多个RPA任务，提供线程数量控制和任务队列管理
"""

import threading
import queue
import time
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from concurrent.futures import ThreadPoolExecutor, Future
from enum import Enum

class TaskStatus(Enum):
    """任务状态枚举"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PAUSED = "paused"

class RPATask:
    """RPA任务对象"""
    
    def __init__(self, task_id: str, env_id: str, flow_data: Dict[str, Any], 
                 priority: int = 0, callback: Callable = None):
        self.task_id = task_id
        self.env_id = env_id
        self.flow_data = flow_data
        self.priority = priority
        self.callback = callback
        
        self.status = TaskStatus.PENDING
        self.created_time = datetime.now()
        self.start_time = None
        self.end_time = None
        self.result = None
        self.error = None
        self.progress = 0
        self.current_step = 0
        self.total_steps = len(flow_data.get('steps', []))
        
        # 线程相关
        self.thread_id = None
        self.executor_instance = None
        self.future = None
    
    def __lt__(self, other):
        """支持优先级队列排序"""
        return self.priority > other.priority  # 高优先级在前
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "task_id": self.task_id,
            "env_id": self.env_id,
            "status": self.status.value,
            "priority": self.priority,
            "created_time": self.created_time.isoformat(),
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "progress": self.progress,
            "current_step": self.current_step,
            "total_steps": self.total_steps,
            "thread_id": self.thread_id,
            "error": self.error
        }

class RPAThreadManager:
    """RPA多线程管理器"""
    
    def __init__(self, max_threads: int = 5, max_queue_size: int = 100):
        self.max_threads = max_threads
        self.max_queue_size = max_queue_size
        
        # 任务队列和管理
        self.task_queue = queue.PriorityQueue(maxsize=max_queue_size)
        self.running_tasks = {}  # task_id -> RPATask
        self.completed_tasks = {}  # task_id -> RPATask
        self.all_tasks = {}  # task_id -> RPATask
        
        # 线程池
        self.executor = ThreadPoolExecutor(max_workers=max_threads, thread_name_prefix="RPA-Worker")
        
        # 控制变量
        self.is_running = False
        self.is_paused = False
        self._lock = threading.RLock()
        self._stop_event = threading.Event()
        self._shutdown_event = threading.Event()
        
        # 统计信息
        self.stats = {
            "total_tasks": 0,
            "completed_tasks": 0,
            "failed_tasks": 0,
            "cancelled_tasks": 0,
            "start_time": None
        }
        
        # 监控线程
        self.monitor_thread = None
    
    def start(self):
        """启动线程管理器"""
        with self._lock:
            if self.is_running:
                return {"success": False, "message": "管理器已在运行"}
            
            self.is_running = True
            self.is_paused = False
            self._stop_event.clear()
            self.stats["start_time"] = datetime.now()
            
            # 启动监控线程
            self.monitor_thread = threading.Thread(target=self._monitor_tasks, daemon=True)
            self.monitor_thread.start()
            
            return {"success": True, "message": "线程管理器已启动"}
    
    def stop(self, wait: bool = True):
        """停止线程管理器 - 优化安全性"""
        with self._lock:
            if not self.is_running:
                return {"success": False, "message": "管理器未运行"}

            self.is_running = False
            self._stop_event.set()
            self._shutdown_event.set()

            # 取消所有待执行任务
            self._cancel_pending_tasks()

            # 停止监控线程
            if hasattr(self, 'monitor_thread') and self.monitor_thread and self.monitor_thread.is_alive():
                try:
                    self.monitor_thread.join(timeout=5)
                    if self.monitor_thread.is_alive():
                        print("[线程管理器] 警告: 监控线程未能正常关闭")
                except Exception as e:
                    print(f"[线程管理器] 停止监控线程时出错: {e}")

            # 安全关闭线程池
            try:
                self.executor.shutdown(wait=wait)
            except Exception as e:
                print(f"[线程管理器] 关闭线程池时出错: {e}")
                # 强制关闭
                try:
                    self.executor.shutdown(wait=False)
                except:
                    pass

            return {"success": True, "message": "线程管理器已停止"}
    
    def pause(self):
        """暂停任务执行"""
        with self._lock:
            self.is_paused = True
            return {"success": True, "message": "任务执行已暂停"}
    
    def resume(self):
        """恢复任务执行"""
        with self._lock:
            self.is_paused = False
            return {"success": True, "message": "任务执行已恢复"}
    
    def add_task(self, env_id: str, flow_data: Dict[str, Any], 
                priority: int = 0, callback: Callable = None) -> str:
        """添加RPA任务"""
        task_id = str(uuid.uuid4())
        task = RPATask(task_id, env_id, flow_data, priority, callback)
        
        try:
            # 检查队列是否已满
            if self.task_queue.full():
                return None
            
            # 添加到队列
            self.task_queue.put((task.priority, time.time(), task))
            
            with self._lock:
                self.all_tasks[task_id] = task
                self.stats["total_tasks"] += 1
            
            return task_id
            
        except queue.Full:
            return None
    
    def cancel_task(self, task_id: str) -> Dict[str, Any]:
        """取消任务"""
        with self._lock:
            if task_id not in self.all_tasks:
                return {"success": False, "message": "任务不存在"}
            
            task = self.all_tasks[task_id]
            
            if task.status == TaskStatus.RUNNING:
                # 取消正在运行的任务
                if task.future:
                    task.future.cancel()
                task.status = TaskStatus.CANCELLED
                if task_id in self.running_tasks:
                    del self.running_tasks[task_id]
                self.completed_tasks[task_id] = task
                self.stats["cancelled_tasks"] += 1
                
            elif task.status == TaskStatus.PENDING:
                # 标记待执行任务为取消
                task.status = TaskStatus.CANCELLED
                self.stats["cancelled_tasks"] += 1
            
            return {"success": True, "message": "任务已取消"}
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """获取任务状态"""
        with self._lock:
            if task_id in self.all_tasks:
                return self.all_tasks[task_id].to_dict()
            return None
    
    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """获取所有任务状态"""
        with self._lock:
            return [task.to_dict() for task in self.all_tasks.values()]
    
    def get_running_tasks(self) -> List[Dict[str, Any]]:
        """获取正在运行的任务"""
        with self._lock:
            return [task.to_dict() for task in self.running_tasks.values()]
    
    def get_queue_size(self) -> int:
        """获取队列大小"""
        return self.task_queue.qsize()
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        with self._lock:
            current_stats = self.stats.copy()
            current_stats.update({
                "running_tasks": len(self.running_tasks),
                "queue_size": self.task_queue.qsize(),
                "max_threads": self.max_threads,
                "is_running": self.is_running,
                "is_paused": self.is_paused
            })
            return current_stats
    
    def set_max_threads(self, max_threads: int):
        """动态调整最大线程数"""
        if max_threads > 0:
            self.max_threads = max_threads
            # 重新创建线程池
            old_executor = self.executor
            self.executor = ThreadPoolExecutor(max_workers=max_threads, thread_name_prefix="RPA-Worker")
            old_executor.shutdown(wait=False)
    
    def _monitor_tasks(self):
        """监控任务执行"""
        while self.is_running and not self._stop_event.is_set():
            try:
                if self.is_paused:
                    time.sleep(1)
                    continue
                
                # 检查是否有可用线程和待执行任务
                if len(self.running_tasks) < self.max_threads and not self.task_queue.empty():
                    try:
                        # 获取下一个任务
                        priority, timestamp, task = self.task_queue.get_nowait()
                        
                        # 检查任务是否已被取消
                        if task.status == TaskStatus.CANCELLED:
                            continue
                        
                        # 提交任务执行
                        future = self.executor.submit(self._execute_task, task)
                        task.future = future
                        task.status = TaskStatus.RUNNING
                        task.start_time = datetime.now()
                        task.thread_id = threading.current_thread().ident
                        
                        with self._lock:
                            self.running_tasks[task.task_id] = task
                        
                    except queue.Empty:
                        pass
                
                # 检查已完成的任务
                self._check_completed_tasks()
                
                time.sleep(0.1)  # 避免CPU占用过高
                
            except Exception as e:
                print(f"监控线程错误: {e}")
                time.sleep(1)
    
    def _execute_task(self, task: RPATask) -> Dict[str, Any]:
        """执行单个RPA任务"""
        try:
            # 导入RPA执行器
            from rpa_executor import RPAExecutor
            
            # 创建执行器实例
            executor = RPAExecutor(task_name=f"Task-{task.task_id}")
            task.executor_instance = executor
            
            # 连接到AdsPower浏览器
            connect_result = executor.connect_to_adspower_browser(task.env_id)
            if not connect_result.get("success"):
                raise Exception(f"连接浏览器失败: {connect_result.get('message')}")
            
            # 执行流程步骤
            steps = task.flow_data.get('steps', [])
            results = []
            
            for i, step in enumerate(steps):
                # 检查是否被取消
                if task.status == TaskStatus.CANCELLED:
                    break
                
                # 更新进度
                task.current_step = i + 1
                task.progress = int((i + 1) / len(steps) * 100)
                
                # 执行步骤
                step_result = executor.execute_step(step)
                results.append(step_result)
                
                # 如果步骤失败且设置为停止，则终止执行
                if not step_result.get("success") and step.get("on_error") == "stop":
                    raise Exception(f"步骤执行失败: {step_result.get('message')}")
            
            # 断开浏览器连接
            executor.disconnect_from_adspower_browser()
            
            return {
                "success": True,
                "results": results,
                "completed_steps": len(results)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _check_completed_tasks(self):
        """检查已完成的任务"""
        completed_task_ids = []
        
        with self._lock:
            for task_id, task in self.running_tasks.items():
                if task.future and task.future.done():
                    completed_task_ids.append(task_id)
        
        # 处理已完成的任务
        for task_id in completed_task_ids:
            task = self.running_tasks[task_id]
            
            try:
                result = task.future.result()
                task.result = result
                
                if result.get("success"):
                    task.status = TaskStatus.COMPLETED
                    self.stats["completed_tasks"] += 1
                else:
                    task.status = TaskStatus.FAILED
                    task.error = result.get("error")
                    self.stats["failed_tasks"] += 1
                    
            except Exception as e:
                task.status = TaskStatus.FAILED
                task.error = str(e)
                self.stats["failed_tasks"] += 1
            
            task.end_time = datetime.now()
            
            # 调用回调函数
            if task.callback:
                try:
                    task.callback(task)
                except Exception as e:
                    print(f"回调函数执行失败: {e}")
            
            # 移动到已完成任务
            with self._lock:
                del self.running_tasks[task_id]
                self.completed_tasks[task_id] = task
    
    def _cancel_pending_tasks(self):
        """取消所有待执行任务"""
        cancelled_count = 0
        
        # 清空队列中的待执行任务
        while not self.task_queue.empty():
            try:
                priority, timestamp, task = self.task_queue.get_nowait()
                task.status = TaskStatus.CANCELLED
                self.completed_tasks[task.task_id] = task
                cancelled_count += 1
            except queue.Empty:
                break
        
        self.stats["cancelled_tasks"] += cancelled_count
    
    def clear_completed_tasks(self):
        """清除已完成的任务记录"""
        with self._lock:
            self.completed_tasks.clear()
            # 从all_tasks中移除已完成的任务
            completed_ids = [task_id for task_id, task in self.all_tasks.items() 
                           if task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]]
            for task_id in completed_ids:
                del self.all_tasks[task_id]

# 全局线程管理器实例
rpa_thread_manager = RPAThreadManager()

# 便捷函数
def start_thread_manager(max_threads: int = 5):
    """启动线程管理器"""
    rpa_thread_manager.set_max_threads(max_threads)
    return rpa_thread_manager.start()

def add_rpa_task(env_id: str, flow_data: Dict[str, Any], priority: int = 0) -> str:
    """添加RPA任务"""
    return rpa_thread_manager.add_task(env_id, flow_data, priority)

def get_task_status(task_id: str) -> Optional[Dict[str, Any]]:
    """获取任务状态"""
    return rpa_thread_manager.get_task_status(task_id)
