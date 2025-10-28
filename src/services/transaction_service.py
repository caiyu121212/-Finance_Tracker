from datetime import datetime,timedelta
import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)
from src.models.database import DatabaseManager

class TransactionService:
    print(project_root)
    def __init__(self,db_path=None):
        self.db = DatabaseManager()

        #添加交易记录
    def add_transaction(self,date,trans_type,amount,category,description=""):
        query = """
        INSERT INTO transactions(data,type,amount,category,description)
        VALUES (?,?,?,?,?)
        """
        self.db.execute_query(query,(date,trans_type,amount,category,description))

    def get_transactions(self,start_date=None,end_date=None,category=None,trans_type=None):
        """获取交易记录"""
        query = "SELECT * FROM transactions WHERE 1=1"
        params = []
        if start_date:
            query += "AND date>=?"
            params.append(start_date)

        if end_date:
            query += " AND date<=?"
            params.append(end_date)
        if category:
            query += " AND category=?"
            params.append(category)
        if trans_type:
            query += " AND type=?"
            params.append(trans_type)
        query += " ORDER BY data DESC"
        return self.db.fetch_all(query,params)

    def update_transaction(self,transaction_id,date,amount,category,description):
        """更新交易记录"""
        query = """
        UPDATE transactions
        SET date=?,amount=?,category=?,description=?,updated_at = ?
        WHERE id=?
        """
        updated_at = datetime.now().isoformat()
        self.db.execute_query(query,(date,amount,category,description,updated_at,transaction_id))

    def delete_transaction(self,transaction_id):
        """删除交易信息"""
        query = "DELETE FROM transactions WHERE id = ?"
        self.db.execute_query(query,(transaction_id,))

     #获取月度统计
    def get_monthly_summary(self,year,month):
        start_date = f"{year}-{month:02d}-01"
        if month == 12:
            end_date = f"{year+1}-01-01"
        else:
            end_date = f"{year}-{month+1:02d}-01"

        query = """
        SELECT
            type,
            category,
            SUM(amount) as total_amount,
            COUNT(*) as count
        FROM transactions
        WHERE date >= ? AND date <？
        GROUP BY type,category
        ORDER BY type,total_amount DESC
        """

        return self.db.fetch_all(query,(start_date,end_date))

    #计算总余额
    def get_balance(self):
        income_query = "SELECT COALESCE(SUM(amount),0) as total FROM transactions WHERE type='income'"
        expense_query = "SELECT COALESCE(SUM(amount),0) as total FROM transactions WHERE type='expense'"

        total_income = self.db.fetch_one(income_query)['total']
        total_expense = self.db.fetch_one(expense_query)['total']

        return {
            'total_income':total_income,
            'total_expense':total_expense,
            'balance':total_income - total_expense
        }


