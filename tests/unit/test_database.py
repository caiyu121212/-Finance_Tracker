import pytest
import os
from src.models.database import DatebaseManager

class TestDataManager:

    #测试数据库和表创建
    def test_database_creation(self,temp_database):
        db = DatebaseManager()
        tables = db.fetch_all("SELECT name FROM sqlite_master WHERE type='table'")
        table_names = [table['name'] for table in tables]
        assert 'transactions' in table_names
        assert 'categories' in table_names
        print("数据表创建成功")


    def test_default_categories(self):
        db = DatebaseManager()
        categories = db.fetch_all("SELECT * FROM categories")


        assert len(categories)>0
        income_categories = [c for c in categories if c['type'] == 'income']
        expense_categories = [c for c in categories if c['type']=='expense']

        assert len(income_categories)>0
        assert len(expense_categories)>0
        print("默认分类初始化成功")

