import pytest
import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

from src.services.transaction_service import TransactionService
from src.services.category_service import CategoryService

class TestFullWorkflow:
    def test_complete_workflow(self,temp_database):
        transaction_service = TransactionService(temp_database)
        category_service = CategoryService(temp_database)

        #初始状态
        initial_balance = transaction_service.get_balance()
        assert initial_balance['balance'] ==0

        # 2. 添加收入
        transaction_service.add_transaction('2024-01-01', 'income', 5000.0, '工资', '月薪')

        # 3. 添加支出
        transaction_service.add_transaction('2024-01-02', 'expense', 100.0, '餐饮', '午餐')
        transaction_service.add_transaction('2024-01-03', 'expense', 200.0, '交通', '地铁')

        # 4. 验证结果
        balance = transaction_service.get_balance()
        assert balance['total_income'] == 5000.0
        assert balance['total_expense'] == 300.0
        assert balance['balance'] == 4700.0

        transactions = transaction_service.get_transactions()
        assert len(transactions) == 3

        print("✅ 完整记账流程测试通过")