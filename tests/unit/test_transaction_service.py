import pytest
import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
from src.services.transaction_service import TransactionService

class TestTransactionService:
    def test_add_transaction(self,temp_database,sample_transaction_data):
        service = TransactionService()
        service.add_transaction(**sample_transaction_data)
        transactions = service.get_transactions()
        assert len(transactions) == 1
        assert transactions[0]['amount'] == 100.0
        print("交易添加功能正常")


    def test_balance_calculation(self,temp_database):
        service = TransactionService()
        service.add_transaction('2024-01-01','income',1000.0,'工资')
        service.add_transaction('2024-01-02','expense',300.0,'工资')

        balance = service.get_balance()
        assert balance['balance'] == 700.0
        print("余额计算功能正常")



