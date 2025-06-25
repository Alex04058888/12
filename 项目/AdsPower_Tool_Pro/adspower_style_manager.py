#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AdsPower样式管理器
完全复刻AdsPower界面风格
"""

class AdsPowerStyleManager:
    """AdsPower风格样式管理器 - 优化性能"""

    # 样式缓存
    _style_cache = {}

    # AdsPower颜色系统
    COLORS = {
        # 主色调 - 基于AdsPower蓝色
        'primary': '#1890ff',
        'primary_hover': '#40a9ff',
        'primary_active': '#096dd9',
        'primary_light': '#e6f7ff',
        
        # 背景色 - AdsPower风格
        'background': '#f5f5f5',
        'background_white': '#ffffff',
        'background_gray': '#fafafa',
        'background_dark': '#f0f0f0',
        
        # 文本色 - AdsPower标准
        'text_primary': '#262626',
        'text_secondary': '#595959',
        'text_tertiary': '#8c8c8c',
        'text_disabled': '#bfbfbf',
        'text_white': '#ffffff',
        
        # 状态色 - AdsPower标准
        'success': '#52c41a',
        'success_hover': '#73d13d',
        'warning': '#faad14',
        'warning_hover': '#ffc53d',
        'error': '#ff4d4f',
        'error_hover': '#ff7875',
        'info': '#1890ff',
        
        # 边框色 - AdsPower标准
        'border': '#d9d9d9',
        'border_light': '#f0f0f0',
        'border_dark': '#bfbfbf',
        'border_focus': '#40a9ff',
    }
    
    # AdsPower字体系统
    FONTS = {
        'family': '"Microsoft YaHei", "PingFang SC", "Helvetica Neue", Arial, sans-serif',
        'size_xs': '12px',
        'size_sm': '13px',
        'size_base': '14px',
        'size_lg': '16px',
        'size_xl': '18px',
        'size_2xl': '20px',
        'size_3xl': '24px',
        'weight_normal': '400',
        'weight_medium': '500',
        'weight_semibold': '600',
        'weight_bold': '700',
    }
    
    # AdsPower尺寸系统
    SIZES = {
        # 按钮尺寸
        'button_xs': {'height': '24px', 'padding': '0 7px', 'font_size': '12px'},
        'button_sm': {'height': '28px', 'padding': '0 11px', 'font_size': '13px'},
        'button_base': {'height': '32px', 'padding': '0 15px', 'font_size': '14px'},
        'button_lg': {'height': '36px', 'padding': '0 19px', 'font_size': '16px'},
        
        # 输入框尺寸
        'input_sm': {'height': '28px', 'padding': '4px 11px'},
        'input_base': {'height': '32px', 'padding': '6px 11px'},
        'input_lg': {'height': '36px', 'padding': '8px 11px'},
    }
    
    @classmethod
    def get_base_style(cls):
        """获取AdsPower基础样式"""
        return f"""
            * {{
                font-family: {cls.FONTS['family']};
                outline: none;
            }}
            
            QWidget {{
                background-color: {cls.COLORS['background']};
                color: {cls.COLORS['text_primary']};
                font-size: {cls.FONTS['size_base']};
                font-weight: {cls.FONTS['weight_normal']};
            }}
            
            QMainWindow {{
                background-color: {cls.COLORS['background']};
            }}
            
            QDialog {{
                background-color: {cls.COLORS['background_white']};
                border: 1px solid {cls.COLORS['border']};
            }}
        """
    
    @classmethod
    def get_button_style(cls, variant='primary', size='base'):
        """获取AdsPower标准按钮样式 - 使用缓存优化性能"""
        cache_key = f"button_{variant}_{size}"

        # 检查缓存
        if cache_key in cls._style_cache:
            return cls._style_cache[cache_key]

        size_config = cls.SIZES[f'button_{size}']
        
        if variant == 'primary':
            return f"""
                QPushButton {{
                    background-color: {cls.COLORS['primary']};
                    color: {cls.COLORS['text_white']};
                    border: 1px solid {cls.COLORS['primary']};
                    border-radius: 4px;
                    height: {size_config['height']};
                    padding: {size_config['padding']};
                    font-size: {size_config['font_size']};
                    font-weight: {cls.FONTS['weight_normal']};
                    font-family: {cls.FONTS['family']};
                    min-width: 64px;
                }}
                QPushButton:hover {{
                    background-color: {cls.COLORS['primary_hover']};
                    border-color: {cls.COLORS['primary_hover']};
                }}
                QPushButton:pressed {{
                    background-color: {cls.COLORS['primary_active']};
                    border-color: {cls.COLORS['primary_active']};
                }}
                QPushButton:disabled {{
                    background-color: {cls.COLORS['background_dark']};
                    color: {cls.COLORS['text_disabled']};
                    border-color: {cls.COLORS['border']};
                }}
            """
        elif variant == 'secondary':
            return f"""
                QPushButton {{
                    background-color: {cls.COLORS['background_white']};
                    color: {cls.COLORS['text_primary']};
                    border: 1px solid {cls.COLORS['border']};
                    border-radius: 4px;
                    height: {size_config['height']};
                    padding: {size_config['padding']};
                    font-size: {size_config['font_size']};
                    font-weight: {cls.FONTS['weight_normal']};
                    font-family: {cls.FONTS['family']};
                    min-width: 64px;
                }}
                QPushButton:hover {{
                    color: {cls.COLORS['primary']};
                    border-color: {cls.COLORS['primary']};
                }}
                QPushButton:pressed {{
                    color: {cls.COLORS['primary_active']};
                    border-color: {cls.COLORS['primary_active']};
                }}
                QPushButton:disabled {{
                    color: {cls.COLORS['text_disabled']};
                    border-color: {cls.COLORS['border_light']};
                }}
            """
        elif variant == 'success':
            return f"""
                QPushButton {{
                    background-color: {cls.COLORS['success']};
                    color: {cls.COLORS['text_white']};
                    border: 1px solid {cls.COLORS['success']};
                    border-radius: 4px;
                    height: {size_config['height']};
                    padding: {size_config['padding']};
                    font-size: {size_config['font_size']};
                    font-weight: {cls.FONTS['weight_normal']};
                    font-family: {cls.FONTS['family']};
                    min-width: 64px;
                }}
                QPushButton:hover {{
                    background-color: {cls.COLORS['success_hover']};
                    border-color: {cls.COLORS['success_hover']};
                }}
            """
        elif variant == 'danger':
            return f"""
                QPushButton {{
                    background-color: {cls.COLORS['error']};
                    color: {cls.COLORS['text_white']};
                    border: 1px solid {cls.COLORS['error']};
                    border-radius: 4px;
                    height: {size_config['height']};
                    padding: {size_config['padding']};
                    font-size: {size_config['font_size']};
                    font-weight: {cls.FONTS['weight_normal']};
                    font-family: {cls.FONTS['family']};
                    min-width: 64px;
                }}
                QPushButton:hover {{
                    background-color: {cls.COLORS['error_hover']};
                    border-color: {cls.COLORS['error_hover']};
                }}
            """

        # 缓存样式并返回
        if 'style' in locals():
            cls._style_cache[cache_key] = style
            return style

        # 默认返回空样式
        default_style = ""
        cls._style_cache[cache_key] = default_style
        return default_style
    
    @classmethod
    def get_input_style(cls, size='base'):
        """获取AdsPower标准输入框样式"""
        size_config = cls.SIZES[f'input_{size}']
        
        return f"""
            QLineEdit, QComboBox, QSpinBox {{
                background-color: {cls.COLORS['background_white']};
                border: 1px solid {cls.COLORS['border']};
                border-radius: 4px;
                color: {cls.COLORS['text_primary']};
                height: {size_config['height']};
                padding: {size_config['padding']};
                font-size: {cls.FONTS['size_base']};
                font-weight: {cls.FONTS['weight_normal']};
                font-family: {cls.FONTS['family']};
            }}
            QLineEdit:hover, QComboBox:hover, QSpinBox:hover {{
                border-color: {cls.COLORS['border_focus']};
            }}
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus {{
                border-color: {cls.COLORS['primary']};
                outline: none;
            }}
            QLineEdit:disabled, QComboBox:disabled, QSpinBox:disabled {{
                background-color: {cls.COLORS['background_gray']};
                color: {cls.COLORS['text_disabled']};
                border-color: {cls.COLORS['border_light']};
            }}
            QComboBox::drop-down {{
                border: none;
                background: transparent;
                width: 20px;
                subcontrol-origin: padding;
                subcontrol-position: top right;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid {cls.COLORS['text_secondary']};
                margin-right: 8px;
            }}
            QComboBox QAbstractItemView {{
                border: 1px solid {cls.COLORS['border']};
                border-radius: 4px;
                background-color: {cls.COLORS['background_white']};
                selection-background-color: {cls.COLORS['primary_light']};
                selection-color: {cls.COLORS['primary']};
                padding: 4px;
                outline: none;
            }}
        """
    
    @classmethod
    def get_table_style(cls):
        """获取AdsPower表格样式"""
        return f"""
            QTableWidget {{
                background-color: {cls.COLORS['background_white']};
                border: 1px solid {cls.COLORS['border']};
                border-radius: 4px;
                gridline-color: {cls.COLORS['border_light']};
                font-size: {cls.FONTS['size_base']};
                font-family: {cls.FONTS['family']};
            }}
            QTableWidget::item {{
                padding: 8px;
                border-bottom: 1px solid {cls.COLORS['border_light']};
            }}
            QTableWidget::item:selected {{
                background-color: {cls.COLORS['primary_light']};
                color: {cls.COLORS['primary']};
            }}
            QHeaderView::section {{
                background-color: {cls.COLORS['background_gray']};
                color: {cls.COLORS['text_primary']};
                padding: 8px;
                border: none;
                border-bottom: 1px solid {cls.COLORS['border']};
                font-weight: {cls.FONTS['weight_medium']};
            }}
        """

    @classmethod
    def get_scrollbar_style(cls):
        """获取滚动条样式"""
        return f"""
        QScrollBar:vertical {{
            background: rgba(255, 255, 255, 0.1);
            width: 12px;
            border-radius: 6px;
            margin: 0px;
        }}

        QScrollBar::handle:vertical {{
            background: {cls.COLORS['primary']};
            border-radius: 6px;
            min-height: 20px;
        }}

        QScrollBar::handle:vertical:hover {{
            background: {cls.COLORS['primary_hover']};
        }}

        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}

        QScrollBar:horizontal {{
            background: rgba(255, 255, 255, 0.1);
            height: 12px;
            border-radius: 6px;
            margin: 0px;
        }}

        QScrollBar::handle:horizontal {{
            background: {cls.COLORS['primary']};
            border-radius: 6px;
            min-width: 20px;
        }}

        QScrollBar::handle:horizontal:hover {{
            background: {cls.COLORS['primary_hover']};
        }}

        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0px;
        }}
        """

    @classmethod
    def get_complete_style(cls):
        """获取完整的AdsPower样式表"""
        return (
            cls.get_base_style() +
            cls.get_button_style('primary') +
            cls.get_input_style() +
            cls.get_table_style() +
            cls.get_scrollbar_style()
        )

    @classmethod
    def setup_message_box_style(cls):
        """设置消息框样式 - AdsPower风格"""
        return f"""
        QMessageBox {{
            background-color: {cls.COLORS['background_white']};
            border: 1px solid {cls.COLORS['border']};
            border-radius: 8px;
            font-family: "Microsoft YaHei", "PingFang SC", Arial, sans-serif;
            font-size: 14px;
            color: {cls.COLORS['text_primary']};
        }}
        QMessageBox QLabel {{
            color: {cls.COLORS['text_primary']};
            font-size: 14px;
            padding: 10px;
        }}
        QMessageBox QPushButton {{
            background-color: {cls.COLORS['primary']};
            color: {cls.COLORS['text_white']};
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            font-size: 13px;
            font-weight: bold;
            min-width: 80px;
        }}
        QMessageBox QPushButton:hover {{
            background-color: {cls.COLORS['primary_hover']};
        }}
        QMessageBox QPushButton:pressed {{
            background-color: {cls.COLORS['primary_active']};
        }}
        """

# 为了兼容性，保留iOS26StyleManager别名
iOS26StyleManager = AdsPowerStyleManager
