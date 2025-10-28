import os
import sys
import sqlite3
from datetime import datetime

current_dir = os.path.abspath(__file__)
models_dir = os.path.dirname(current_dir)
src_dir = os.path.dirname(models_dir)
project_root = os.path.dirname(src_dir)
sys.path.insert(0,project_root)

from config import Config


# ====== 数据库管理器类 ======
class DatabaseManager:
    def __init__(self,db_path=None):
        self.db_path = db_path or Config.DATABASE_PATH
        self._create_tables()
        self._init_default_data()

    #获取数据库连接
    def _get_connection(self):
        os.makedirs(os.path.dirname(self.db_path),exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        conn.row_factory =sqlite3.Row
        return conn

    #创建数据表
    def _create_tables(self):
        conn = self._get_connection()
        try:
            #交易表
            conn.execute('''
                CREATE TABLE IF NOT EXISTS transactions(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL,
                type TEXT NOT NULL CHECK(type IN ('income','expense')),
                amount REAL NOT NULL CHECK(amount > 0),
                category TEXT NOT NULL,
                description TEXT ,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                ''')

            #分类表
            conn.execute('''
                CREATE TABLE IF NOT EXISTS categories(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL CHECK(type IN ('income','expense')),
                color TEXT DEFAULT '#000000')
                ''')


            #预算表
            conn.execute('''
                CREATE TABLE IF NOT EXISTS budgets(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                 category TEXT NOT NULL,
                 amount REAL NOT NULL CHECK(amount>0),
                 month TEXT NOT NULL,
                 created_at TEXT DEFAULT CURRENT_TIMESTAMP)
            ''')
            conn.commit()
        finally:
            conn.close()

    #初始化默认数据
    def _init_default_data(self):
        print("📝 开始初始化默认数据...")
        conn = self._get_connection()
        try:
            default_categories = [
                ('工资','income','#4CAF50'),
                ('奖金','income','#8BC34A'),
                ('投资','income','#CDDC39'),
                ('其他收入','income','#FFC107'),
                ('餐饮','expense','#F44336'),
                ('交通','expense','#E91E63'),
                ('购物','expense','#9C27B0'),
                ('娱乐','expense','#673AB7'),
                ('医疗','expense','#3F51B5'),
                ('教育','expense','#2196F3'),
                ('其他支出','expense','#00BCD4')
            ]
            for name,type,color in default_categories:
                conn.execute(
                    'INSERT OR IGNORE INTO categories(name,type,color) VALUES (?,?,?)',
                    (name,type,color)
                )
            conn.commit()
        finally:
            conn.close()

    #执行查询
    def execute_query(self,query,params=()):
        conn = self._get_connection()
        try:
            cursor = conn.execute(query,params)
            conn.commit()
            return cursor
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    #获取所有结果
    def fetch_all(self,query,params=()):
        conn = self._get_connection()
        try:
            cursor = conn.execute(query,params)
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    #获取单个结果
    def fetch_one(self,query,params=()):
        conn = self._get_connection()
        try:
            cursor = conn.execute(query,params)
            result = cursor.fetchone()
            return dict(result) if result else None
        finally:
            conn.close()





