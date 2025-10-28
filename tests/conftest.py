import pytest
import tempfile
import os
import sys
from datetime import datetime,timedelta
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,project_root)


@pytest.fixture
def temp_database():
      #创建临时数据库
    import tempfile
    db_fd,db_path = tempfile.mkstemp()
      #修改配置使用临时数据库
    import config
    original_db_path = config.Config.DATABASE_PATH
    config.Config.DATABASE_PATH = db_path

    yield db_path

    #清理
    os.close(db_fd)
    if os.path.exists(db_path):
        os.unlink(db_path)
    config.Config.DATABASE_PATH = original_db_path


@pytest.fixture
def sample_transaction_data():
    #样本交易数据
    return {
        'date':'2024-01-01',
        'trans_type':'expense',
        'amount':100.0,
        'category':'餐饮',
        'description':'午餐'
    }


