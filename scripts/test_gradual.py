#!/usr/bin/env/ python3

# 渐进式测试运行器
import subprocess
import sys
import os
import time

class FinanceTrackerTester:
    def __init__(self):
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.test_plan = [
            {
                'name':'数据库基础测试',
                'file':'tests/unit/test_database.py',
                'command':'database',
                'description':'测试数据库创建、表结构和基本操作'
            },
            {
                'name':'交易服务测试',
                'file':'tests/unit/test_transaction_service.py',
                'command':'transaction',
                'description':'测试交易添加、查询、余额计算'
            },
            {
                'name':'分类测试服务',
                'file':'tests/unit/test_transaction_service.py',
                'command':'category',
                'description':'测试分类管理和验证'
            },
            {
                'name':'服务集成测试',
                'file':'tests/integration/test_service_integration.py',
                'command':'integration',
                'description':'测试服务间协作和数据流'
            },
            {
                'name':'完整流程测试',
                'file':'tests/e2e/test_full_workflow.py',
                'command':'workflow',
                'description':'测试端到业务流程'
            },
            {
                'name':'最终整合测试',
                'command':'all',
                'description':'运行完整测试套件'
            }
        ]
    def get_full_path(self,relative_path):
        return os.path.join(self.project_root,relative_path)

#运行单个测试文件
    def run_single_test(self,test_file):
        if not os.path.exists(test_file):
            print(f"测试文件不存在：{test_file}")
            return False

        print(f"开始测试{test_file}")
        start_time = time.time()

        python_executable = sys.executable

        result = subprocess.run([
              python_executable,'-m','pytest',
            test_file,
            '-v','--tb=short','--color=yes'
        ],capture_output=True,text=True)

        elapsed_time = time.time()-start_time

        print(result.stdout)

        if result.returncode == 0:
            print(f"测试通过！耗时{elapsed_time:.2f}秒")
            return True
        else:
            print(f"测试失败！耗时：{elapsed_time:.2f}秒")
            if result.stderr:
                print("错误信息：")
                print(result.stderr)
            return False

#显示测试进度
    def show_progress(self):
        print("\n 当前测试进度：")
        print("="*60)

        completed = 0
        for i,step in enumerate(self.test_plan,1):
            exists = os.path.exists(step['file']) if 'file' in step else True
            status = "已完成" if exists else "待完成"

            print(f"{i}/{step['name']:20}{status}")
            if exists and 'file' in step:
                completed += 1

        total = len([s for s in self.test_plan if 'file' in s])
        print("="*60)
        print(f"进度：{completed}/{total}({completed/total*100:.1f}%)")

    #运行指定步骤
    def run_step(self,step_name):
        for step in self.test_plan:
            if step['command'] == step_name:
                print(f"执行：{step['name']}")
                print(f"{step['description']}")
                if 'file' in step:
                    return self.run_single_test(step['file'])
                elif step['command'] == 'all':
                    return self.run_all_tests()
                else:
                    print("未知的测试步骤")
                    return False

        print(f"未找到测试步骤：{step_name}")
        return False

#运行所有测试
    def run_all_tests(self):
        print("\n 开始完整测试套件...")
        success = True

        for step in self.test_plan:
            if 'file' in step and os.path.exists(step['file']):
                if not self.run_single_test(step['file']):
                    success = False
                    print(f"{step['name']}失败，停止测试")
                    break
                print("-"*50)

        if success:
            print("所有测试通过！系统就绪！")
        else:
            print("部分测试失败，请检查问题")

        return success


def main():
    tester = FinanceTrackerTester()
    if len(sys.argv)<2:
        print("🔧 Finance Tracker 渐进式测试系统")
        print("用法: python scripts/test_gradual.py <步骤>")
        print("\n可用测试步骤:")
        for step in tester.test_plan:
            print(f"  {step['command']:15} - {step['name']}")
        print("\n示例:")
        print("  python scripts/test_gradual.py progress    # 查看进度")
        print("  python scripts/test_gradual.py database    # 测试数据库")
        print("  python scripts/test_gradual.py transaction # 测试交易服务")
        print("  python scripts/test_gradual.py all         # 运行所有测试")
        sys.exit(1)

    command =sys.argv[1]

    if command == 'progress':
        tester.show_progress()
    else:
        success = tester.run_step(command)
        sys.exit(0 if success else 1)

if __name__ == '__main__':
        print("python 路径：",sys.executable)
        main()


