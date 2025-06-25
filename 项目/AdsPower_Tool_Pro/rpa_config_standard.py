#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AdsPower工具专业版 - RPA标准参数配置
完全按照AdsPower官方文档标准实现的参数配置
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class AdsPowerStandardConfig:
    """AdsPower标准参数配置类"""
    
    def __init__(self):
        self.config_data = {}
    
    # ==================== 页面操作配置 ====================
    
    def get_click_element_config(self):
        """点击元素 - 完全按照AdsPower官方标准"""
        return {
            "operation": "点击元素",
            "parameters": {
                "selector": {
                    "type": "string",
                    "label": "选择器",
                    "placeholder": "输入元素选择器，如#email_input、input[type=\"password\"]、.button_search等",
                    "required": True,
                    "help": "选择器使用可参考官方文档"
                },
                "stored_element": {
                    "type": "select",
                    "label": "储存的元素对象",
                    "options": ["无"],
                    "editable": True,
                    "help": "选择一个保存为对象的变量"
                },
                "element_order": {
                    "type": "complex",
                    "label": "元素顺序",
                    "sub_fields": {
                        "type": {
                            "type": "select",
                            "options": ["固定值", "区间随机"],
                            "default": "固定值"
                        },
                        "value": {
                            "type": "number",
                            "min": 1,
                            "max": 999,
                            "default": 1
                        },
                        "max_value": {
                            "type": "number",
                            "min": 1,
                            "max": 999,
                            "default": 1,
                            "visible_when": "type=区间随机"
                        }
                    },
                    "help": "固定值：选择固定顺序的元素；区间随机：在设定的区间内随机选择一个元素"
                },
                "click_type": {
                    "type": "select",
                    "label": "点击类型",
                    "options": ["鼠标左键", "鼠标中键", "鼠标右键"],
                    "default": "鼠标左键",
                    "help": "可选值：鼠标左键、中键、右键"
                },
                "key_type": {
                    "type": "select",
                    "label": "按键类型",
                    "options": ["单击", "双击"],
                    "default": "单击",
                    "help": "选择鼠标操作：单击、双击"
                }
            }
        }
    
    def get_input_content_config(self):
        """输入内容 - 完全按照AdsPower官方标准"""
        return {
            "operation": "输入内容",
            "parameters": {
                "selector": {
                    "type": "string",
                    "label": "选择器",
                    "placeholder": "仅支持<input type='text'>、<input type='password'>、<textarea>",
                    "required": True,
                    "help": "输入元素选择器，如input[type=\"password\"]、input[type=\"text\"]"
                },
                "stored_element": {
                    "type": "select",
                    "label": "储存的元素对象",
                    "options": ["无"],
                    "editable": True,
                    "help": "选择一个保存为对象的变量"
                },
                "element_order": {
                    "type": "number",
                    "label": "元素顺序",
                    "min": 1,
                    "default": 1,
                    "help": "比如输入的元素选择器在页面上有很多个，顺序则代表你想要选择第几个"
                },
                "content": {
                    "type": "textarea",
                    "label": "内容",
                    "placeholder": "输入内容：单个内容一行输入，多行内容则换行输入",
                    "required": True,
                    "help": "单个内容请在一行输入即可；多个内容请换行输入，会选取其中一个内容。内容最多50行，每行最多500个字符"
                },
                "content_type": {
                    "type": "select",
                    "label": "内容选取方式",
                    "options": ["顺序选取", "随机选取", "随机取数", "使用变量"],
                    "default": "顺序选取",
                    "help": "顺序选取：按照输入内容的顺序获取；随机选取：随机获取；随机取数：在指定区间内随机取一个数值"
                },
                "input_interval": {
                    "type": "number",
                    "label": "输入间隔时间",
                    "min": 0,
                    "max": 10000,
                    "default": 300,
                    "unit": "毫秒",
                    "help": "如获取内容1，间隔时间300，则是每隔300毫秒输入一个字符"
                },
                "clear_before": {
                    "type": "checkbox",
                    "label": "清除原内容",
                    "default": True,
                    "help": "支持用户清除掉文本框里面的数据再次输入（模拟Ctrl+A Del）"
                }
            }
        }
    
    def get_wait_element_config(self):
        """等待元素出现 - 完全按照AdsPower官方标准"""
        return {
            "operation": "等待元素出现",
            "parameters": {
                "selector": {
                    "type": "string",
                    "label": "选择器",
                    "placeholder": "元素选择器，如#email_input、input[type=\"password\"]、.button_search等",
                    "required": True,
                    "help": "支持使用变量"
                },
                "element_order": {
                    "type": "number",
                    "label": "元素顺序",
                    "min": 1,
                    "default": 1,
                    "help": "选择第几个网页元素，支持使用变量"
                },
                "is_visible": {
                    "type": "checkbox",
                    "label": "是否可见",
                    "default": True,
                    "help": "打开【是否可见】选项，表示该网页元素（图片/按钮/选项等）在网页显示的时候，才去执行下一个步骤"
                },
                "timeout": {
                    "type": "number",
                    "label": "超时等待",
                    "min": 1000,
                    "max": 300000,
                    "default": 30000,
                    "unit": "毫秒",
                    "help": "最长等待时间。如30000：即为30秒内如果没能成功执行该步骤，则会直接执行下一步"
                },
                "save_to": {
                    "type": "string",
                    "label": "保存至",
                    "placeholder": "变量名",
                    "help": "将元素是不是已经出现了的结果保存至变量，这个变量的结果是true/false"
                }
            }
        }
    
    def get_page_screenshot_config(self):
        """页面截图 - 完全按照AdsPower官方标准"""
        return {
            "operation": "页面截图",
            "parameters": {
                "screenshot_name": {
                    "type": "string",
                    "label": "截图名称",
                    "placeholder": "可输入截图保存的名称",
                    "help": "默认：任务id+用户id+时间戳组成"
                },
                "full_page": {
                    "type": "checkbox",
                    "label": "截全屏",
                    "default": False,
                    "help": "开启：截取整个网页长图；关闭：截取当前屏幕可见的页面"
                },
                "image_format": {
                    "type": "select",
                    "label": "图片格式",
                    "options": ["png", "jpeg"],
                    "default": "png",
                    "help": "选取输出图片的格式为png或jpeg"
                },
                "jpeg_quality": {
                    "type": "number",
                    "label": "JPEG质量",
                    "min": 1,
                    "max": 100,
                    "default": 80,
                    "visible_when": "image_format=jpeg",
                    "help": "选择jpeg时，可以选择输出图片的质量"
                }
            }
        }
    
    def get_hover_element_config(self):
        """经过元素 - 完全按照AdsPower官方标准"""
        return {
            "operation": "经过元素",
            "parameters": {
                "selector": {
                    "type": "string",
                    "label": "选择器",
                    "placeholder": "输入元素选择器，如#email_input、input[type=\"password\"]、.button_search等",
                    "required": True,
                    "help": "选择器使用可参考官方文档"
                },
                "stored_element": {
                    "type": "select",
                    "label": "储存的元素对象",
                    "options": ["无"],
                    "editable": True,
                    "help": "选择一个保存为对象的变量"
                },
                "element_order": {
                    "type": "complex",
                    "label": "元素顺序",
                    "sub_fields": {
                        "type": {
                            "type": "select",
                            "options": ["固定值", "随机"],
                            "default": "固定值"
                        },
                        "value": {
                            "type": "number",
                            "min": 1,
                            "max": 999,
                            "default": 1
                        },
                        "max_value": {
                            "type": "number",
                            "min": 1,
                            "max": 999,
                            "default": 1,
                            "visible_when": "type=随机"
                        }
                    },
                    "help": "固定值：选择网页里面的第几个元素；随机：在设定的区间内随机选择一个元素"
                }
            }
        }
    
    def get_dropdown_selector_config(self):
        """下拉选择器 - 完全按照AdsPower官方标准"""
        return {
            "operation": "下拉选择器",
            "parameters": {
                "selector": {
                    "type": "string",
                    "label": "元素选择器",
                    "placeholder": "下拉选择器只支持<select>元素，如：#pet-select",
                    "required": True,
                    "help": "输入能定位到<select>的选择器"
                },
                "stored_element": {
                    "type": "select",
                    "label": "储存的元素对象",
                    "options": ["无"],
                    "editable": True,
                    "help": "选择一个保存为对象的变量"
                },
                "element_order": {
                    "type": "complex",
                    "label": "元素顺序",
                    "sub_fields": {
                        "type": {
                            "type": "select",
                            "options": ["固定值", "区间随机"],
                            "default": "固定值"
                        },
                        "value": {
                            "type": "number",
                            "min": 1,
                            "max": 999,
                            "default": 1
                        },
                        "max_value": {
                            "type": "number",
                            "min": 1,
                            "max": 999,
                            "default": 1,
                            "visible_when": "type=区间随机"
                        }
                    },
                    "help": "固定值：选择网页里面的第几个元素；区间随机：在设定的区间内随机选择一个元素"
                },
                "select_value": {
                    "type": "string",
                    "label": "选择的值",
                    "placeholder": "输入想要选择的值，如value属性的值：parrot",
                    "required": True,
                    "help": "输入想要选择的值，如想选择'Parrot'，即输入value属性的值：parrot"
                },
                "use_variable": {
                    "type": "checkbox",
                    "label": "使用变量",
                    "default": False,
                    "help": "使用之前保存的变量"
                }
            }
        }
    
    # ==================== 等待操作配置 ====================
    
    def get_wait_time_config(self):
        """等待时间 - 完全按照AdsPower官方标准"""
        return {
            "operation": "等待时间",
            "parameters": {
                "wait_type": {
                    "type": "select",
                    "label": "等待类型",
                    "options": ["固定值", "区间随机"],
                    "default": "固定值",
                    "help": "固定值：设置固定的时间等待；区间随机：在设置的时间范围内，随机等待"
                },
                "wait_time": {
                    "type": "number",
                    "label": "等待时间",
                    "min": 100,
                    "max": 300000,
                    "default": 3000,
                    "unit": "毫秒",
                    "visible_when": "wait_type=固定值",
                    "help": "设置固定的时间等待，比如等待3秒"
                },
                "wait_min": {
                    "type": "number",
                    "label": "最小时间",
                    "min": 100,
                    "max": 300000,
                    "default": 2000,
                    "unit": "毫秒",
                    "visible_when": "wait_type=区间随机",
                    "help": "随机等待的最小时间"
                },
                "wait_max": {
                    "type": "number",
                    "label": "最大时间",
                    "min": 100,
                    "max": 300000,
                    "default": 5000,
                    "unit": "毫秒",
                    "visible_when": "wait_type=区间随机",
                    "help": "随机等待的最大时间"
                }
            }
        }
    
    def get_wait_request_config(self):
        """等待请求完成 - 完全按照AdsPower官方标准"""
        return {
            "operation": "等待请求完成",
            "parameters": {
                "response_url": {
                    "type": "string",
                    "label": "响应URL",
                    "placeholder": "填写URL，如：https://m.media-amazon.com/images/I/41APBn4YKcL._AC_SR38,50_.jpg",
                    "required": True,
                    "help": "你要等某张图片请求完成之后，再去做其他操作"
                },
                "timeout": {
                    "type": "number",
                    "label": "超时等待",
                    "min": 1000,
                    "max": 300000,
                    "default": 30000,
                    "unit": "毫秒",
                    "help": "最长等待时间。如30000：即为30秒内如果没能成功执行该步骤，则会直接执行下一步"
                }
            }
        }
    
    # ==================== 更多页面操作配置 ====================

    def get_new_tab_config(self):
        """新建标签 - 完全按照AdsPower官方标准"""
        return {
            "operation": "新建标签",
            "parameters": {
                "switch_to_new": {
                    "type": "checkbox",
                    "label": "切换到新标签",
                    "default": True,
                    "help": "是否切换到新建的标签页"
                }
            }
        }

    def get_goto_url_config(self):
        """访问网站 - 完全按照AdsPower官方标准"""
        return {
            "operation": "访问网站",
            "parameters": {
                "goto_url": {
                    "type": "string",
                    "label": "访问URL",
                    "placeholder": "输入网站域名，如：https://www.amazon.com",
                    "required": True,
                    "help": "输入网站域名，如：https://www.amazon.com https://www.facebook.com"
                },
                "use_variable": {
                    "type": "checkbox",
                    "label": "使用变量",
                    "default": False,
                    "help": "使用已经保存的变量"
                }
            }
        }

    def get_upload_file_config(self):
        """上传附件 - 完全按照AdsPower官方标准"""
        return {
            "operation": "上传附件",
            "parameters": {
                "selector": {
                    "type": "string",
                    "label": "选择器",
                    "placeholder": "仅支持对<input type='file'>元素操作，如input[type=\"file\"]",
                    "required": True,
                    "help": "仅支持对<input type='file'>元素操作，故输入的选择器要定位到这个元素"
                },
                "element_order": {
                    "type": "number",
                    "label": "元素顺序",
                    "min": 1,
                    "default": 1,
                    "help": "比如输入的元素选择器在页面上有很多个，顺序则代表你想要选择第几个"
                },
                "file_type": {
                    "type": "select",
                    "label": "附件类型",
                    "options": ["本地文件", "文件夹文件随机", "网络URL"],
                    "default": "本地文件",
                    "help": "本地文件：选择一个本地文件上传；文件夹文件随机：选择一个文件夹，随机上传文件夹里面的某个文件；网络URL：上传网络文件"
                },
                "file_path": {
                    "type": "file",
                    "label": "文件路径",
                    "visible_when": "file_type=本地文件",
                    "help": "选择要上传的本地文件"
                },
                "folder_path": {
                    "type": "folder",
                    "label": "文件夹路径",
                    "visible_when": "file_type=文件夹文件随机",
                    "help": "选择包含文件的文件夹"
                },
                "network_url": {
                    "type": "string",
                    "label": "网络URL",
                    "placeholder": "输入http/https开头的URL",
                    "visible_when": "file_type=网络URL",
                    "help": "上传网络文件，输入http/https开头的URL"
                },
                "timeout": {
                    "type": "number",
                    "label": "超时等待",
                    "min": 1000,
                    "max": 300000,
                    "default": 30000,
                    "unit": "毫秒",
                    "help": "最长等待时间。如30000：即为30秒内如果没能成功执行该步骤，则会直接执行下一步"
                }
            }
        }

    def get_execute_js_config(self):
        """执行JS脚本 - 完全按照AdsPower官方标准"""
        return {
            "operation": "执行JS脚本",
            "parameters": {
                "javascript": {
                    "type": "textarea",
                    "label": "JavaScript",
                    "placeholder": "可注入你的JS代码，如：console.log('hello word!')",
                    "required": True,
                    "help": "可注入你的JS代码，如：console.log('hello word!')，执行该步骤后可在浏览器中查看到上面的输出"
                },
                "inject_variables": {
                    "type": "multiselect",
                    "label": "注入变量",
                    "options": [],
                    "help": "选择注入的变量，可在js函数里使用该变量"
                },
                "return_save_to": {
                    "type": "string",
                    "label": "返回值保存至",
                    "placeholder": "变量名",
                    "help": "将Javascript脚本函数return出来的值保存到某个变量"
                }
            }
        }

    def get_scroll_page_config(self):
        """滚动页面 - 完全按照AdsPower官方标准"""
        return {
            "operation": "滚动页面",
            "parameters": {
                "scroll_type": {
                    "type": "select",
                    "label": "滚动距离",
                    "options": ["位置", "像素"],
                    "default": "位置",
                    "help": "位置：可选滚动到页面的顶部、中部、底部；像素：可输入滚动的距离"
                },
                "scroll_position": {
                    "type": "select",
                    "label": "滚动位置",
                    "options": ["顶部", "中部", "底部"],
                    "default": "底部",
                    "visible_when": "scroll_type=位置",
                    "help": "选择滚动到页面的位置"
                },
                "scroll_pixels": {
                    "type": "number",
                    "label": "滚动像素",
                    "min": -10000,
                    "max": 10000,
                    "default": 500,
                    "visible_when": "scroll_type=像素",
                    "help": "可输入滚动的距离，如：100，1000，1234像素"
                },
                "scroll_behavior": {
                    "type": "select",
                    "label": "滚动类型",
                    "options": ["平滑", "瞬间"],
                    "default": "平滑",
                    "help": "平滑：缓慢滚动到相应的位置；瞬间：快速滚动到相应的位置"
                },
                "scroll_distance": {
                    "type": "number",
                    "label": "单次滚动距离",
                    "min": 10,
                    "max": 1000,
                    "default": 100,
                    "visible_when": "scroll_behavior=平滑",
                    "help": "每一次滑动的距离"
                },
                "scroll_delay": {
                    "type": "number",
                    "label": "停止时间",
                    "min": 10,
                    "max": 5000,
                    "default": 100,
                    "unit": "毫秒",
                    "visible_when": "scroll_behavior=平滑",
                    "help": "每一次滚动之后，停留多久"
                }
            }
        }

    # ==================== 获取所有标准配置 ====================

    def get_all_standard_configs(self):
        """获取所有标准配置"""
        return {
            # 页面操作
            "新建标签": self.get_new_tab_config(),
            "访问网站": self.get_goto_url_config(),
            "点击元素": self.get_click_element_config(),
            "输入内容": self.get_input_content_config(),
            "页面截图": self.get_page_screenshot_config(),
            "经过元素": self.get_hover_element_config(),
            "下拉选择器": self.get_dropdown_selector_config(),
            "上传附件": self.get_upload_file_config(),
            "执行JS脚本": self.get_execute_js_config(),
            "滚动页面": self.get_scroll_page_config(),

            # 等待操作
            "等待时间": self.get_wait_time_config(),
            "等待元素出现": self.get_wait_element_config(),
            "等待请求完成": self.get_wait_request_config()
        }

# 全局标准配置实例
adspower_standard_config = AdsPowerStandardConfig()
