import pytest
import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)
from src.services.transaction_service import TransactionService
from src.services.category_service import CategoryService

class TestServiceIntegration:
    def test_transaction_with_categories(self,temp_database):
        print(f"临时数据库路径：{temp_database}")

        transaction_service = TransactionService(temp_database)
        category_service = CategoryService(temp_database)

        print(f"transactionService数据库:{transaction_service.db.db_path}")
        print(f"CategoryService 数据库：{category_service.db.db_path}")

        categories = category_service.get_categories('expense')
        print(f"🔍 找到的支出分类: {[cat['name'] for cat in categories]}")
        valid_category = categories[0]['name']
        print(valid_category)
        print(f"🎯 使用的分类: {valid_category}")

        transaction_service.add_transaction('2024-01-01','expense',100,valid_category,'测试')

        transactions = transaction_service.get_transactions()
        print(transactions)
        assert len(transactions) == 1
        assert transactions[0]['category'] == valid_category

        print("交易和分类集成正常")