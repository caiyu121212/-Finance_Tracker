# 个人记账系统-企业版
## 项目概述
一个功能完整的个人财务管理应用，支持交易记录、统计分析、数据导出等功能。

## 技术栈
-python 3.8+
-SQLite 数据库
-Tkinter GUI
-PyInstaller打包

## 开发团队
-项目经理：caiyu
-开发工程师：caiyu
-测试工程师：caiyu

## 项目里程碑
-Week1：需求分析和设计
-Week2：核心功能开发
-Week3：Gui界面开发
-Week4：测试和打包



## 项目文件说明
1. 数据库模型层-src/models/database.py
    Class DatabaseManger:
    连接数据库
    创建数据表：交易表、分类表、预算表
    初始化默认数据
    执行查询
    获取所有结果
    获取单个结果
2. 交易服务层-src/services/transaction_service.py
    Class TransactionService
    初始构建DatabaseManager
    添加交易记录 add_transaction
    获取交易记录 get_transaction
    更新交易记录 update_transaction
    删除交易记录 delete_transaction
    获取月度统计 get_monthly_summary
    计算总余额  get_balance
3. 分类服务层-src/services/category_service.py
    Class categoryService
    获取分类列表 get_categories
    添加分类 add_category
    删除分类 delete_category
4. GUI界面开发-主界面
    Class MainWindow
5. 测试文件
    测试配置：tests/conftest.py
        创建临时数据库: temp_database
        添加测试样板交易数据:sample_transaction_date()
    渐进式测试运行器-转为finance_tracker设计:scripts/test_gradual.py
        Class FinanceTrackerTester:
            初始构造设置测试计划：数据库基础测试、交易服务测试、分类服务测试、服务集成测试、完整流程测试、最终整合测试
            运行单个测试文件：run_single_test
            运行指定步骤：run_step
            运行所有测试：run_all_tests



