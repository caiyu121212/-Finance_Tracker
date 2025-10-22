import os

class Config:
    # 数据库配置
    DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'database', 'finance.db')
    BACKUP_PATH = os.path.join(os.path.dirname(__file__), 'backups')

    # 应用配置
    APP_NAME = "个人记账系统"
    VERSION = "1.0.0"

    # 界面配置
    WINDOW_SIZE = "800x600"
    THEME_COLOR = "#2E86AB"

    # 默认分类
    DEFAULT_INCOME_CATEGORIES = ["工资", "奖金", "投资", "其他收入"]
    DEFAULT_EXPENSE_CATEGORIES = ["餐饮", "交通", "购物", "娱乐", "医疗", "教育", "其他支出"]