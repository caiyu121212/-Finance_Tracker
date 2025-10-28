import tkinter as tk
import sys
import os
from tkinter import ttk,messagebox
from datetime import datetime,timedelta
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)
from src.services.transaction_service import TransactionService
from src.services.category_service import CategoryService
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class MainWindow:
    def __init__(self,root):
        self.root = root
        self.root.title("个人记账系统 V1.0")
        self.root.geometry("1000x700")

        #初始化服务
        self.transaction_service = TransactionService()
        self.category_service = CategoryService()
        self.setup_ui()
        self.refresh_data()

    def setup_ui(self):
        """设置界面布局"""
        #创建主框架
        main_frame = ttk.Frame(self.root,padding="10")
        main_frame.grid(row=0,column=0,sticky=(tk.W,tk.E,tk.N,tk.S))

        self.root.columnconfigure(0,weight=1)
        self.root.rowconfigure(0,weight=1)
        main_frame.columnconfigure(0,weight=1)
        main_frame.rowconfigure(0,weight=1)

        self.setup_stats_frame(main_frame)
        self.setup_transaction_frame(main_frame)
        self.setup_actions_frame(main_frame)

    def setup_stats_frame(self, parent):
        """设置统计信息区域"""
        stats_frame = ttk.LabelFrame(parent, text="账户概览", padding="10")
        stats_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        # 统计信息标签
        self.balance_label = ttk.Label(stats_frame, text="总余额: 加载中...", font=('', 12, 'bold'))
        self.balance_label.grid(row=0, column=0, padx=(0, 20))

        self.income_label = ttk.Label(stats_frame, text="总收入: 加载中...", foreground="green")
        self.income_label.grid(row=0, column=1, padx=(0, 20))

        self.expense_label = ttk.Label(stats_frame, text="总支出: 加载中...", foreground="red")
        self.expense_label.grid(row=0, column=2)

    def setup_transaction_frame(self, parent):
        """设置交易记录区域"""
        # 左侧操作面板
        operation_frame = ttk.LabelFrame(parent, text="交易操作", padding="10")
        operation_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))

        self.setup_operation_panel(operation_frame)

        # 右侧交易列表
        list_frame = ttk.LabelFrame(parent, text="交易记录", padding="10")
        list_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        self.setup_transaction_list(list_frame)

    def setup_operation_panel(self, parent):
        """设置操作面板"""
        # 交易类型
        ttk.Label(parent, text="交易类型:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.trans_type = tk.StringVar(value="expense")
        ttk.Radiobutton(parent, text="支出", variable=self.trans_type, value="expense").grid(row=0, column=1,
                                                                                             sticky=tk.W)
        ttk.Radiobutton(parent, text="收入", variable=self.trans_type, value="income").grid(row=0, column=2,
                                                                                            sticky=tk.W)

        # 金额
        ttk.Label(parent, text="金额:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.amount_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.amount_var, width=15).grid(row=1, column=1, columnspan=2,
                                                                       sticky=(tk.W, tk.E))

        # 分类
        ttk.Label(parent, text="分类:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(parent, textvariable=self.category_var, width=13)
        self.category_combo.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E))

        # 日期
        ttk.Label(parent, text="日期:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(parent, textvariable=self.date_var, width=15).grid(row=3, column=1, columnspan=2, sticky=(tk.W, tk.E))

        # 描述
        ttk.Label(parent, text="描述:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.desc_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.desc_var, width=15).grid(row=4, column=1, columnspan=2, sticky=(tk.W, tk.E))

        # 按钮
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=5, column=0, columnspan=3, pady=10)

        ttk.Button(button_frame, text="添加交易", command=self.add_transaction).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="清空", command=self.clear_form).pack(side=tk.LEFT)

    def setup_transaction_list(self, parent):
        """设置交易列表"""
        # 创建树形视图
        columns = ("ID", "日期", "类型", "金额", "分类", "描述")
        self.tree = ttk.Treeview(parent, columns=columns, show="headings", height=20)

        # 设置列
        self.tree.heading("ID", text="ID")
        self.tree.heading("日期", text="日期")
        self.tree.heading("类型", text="类型")
        self.tree.heading("金额", text="金额")
        self.tree.heading("分类", text="分类")
        self.tree.heading("描述", text="描述")

        # 设置列宽
        self.tree.column("ID", width=50)
        self.tree.column("日期", width=100)
        self.tree.column("类型", width=80)
        self.tree.column("金额", width=100)
        self.tree.column("分类", width=100)
        self.tree.column("描述", width=200)

        # 滚动条
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # 绑定双击事件
        self.tree.bind("<Double-1>", self.on_item_double_click)

    def setup_actions_frame(self, parent):
        """设置操作按钮区域"""
        actions_frame = ttk.Frame(parent)
        actions_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))

        ttk.Button(actions_frame, text="刷新", command=self.refresh_data).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(actions_frame, text="统计报表", command=self.show_report).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(actions_frame, text="导出数据", command=self.export_data).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(actions_frame, text="退出", command=self.root.quit).pack(side=tk.LEFT)

    def refresh_data(self):
        """刷新数据"""
        # 更新分类下拉框
        categories = self.category_service.get_categories()
        self.category_combo['values'] = [cat['name'] for cat in categories]

        # 更新交易列表
        self.refresh_transaction_list()

        # 更新统计信息
        self.refresh_stats()

    def refresh_transaction_list(self):
        """刷新交易列表"""
        # 清空现有数据
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 获取交易记录
        transactions = self.transaction_service.get_transactions()

        # 添加数据到列表
        for trans in transactions:
            amount_text = f"+{trans['amount']}" if trans['type'] == 'income' else f"-{trans['amount']}"
            self.tree.insert("", "end", values=(
                trans['id'],
                trans['data'],
                "收入" if trans['type'] == 'income' else "支出",
                amount_text,
                trans['category'],
                trans['description'] or ""
            ))

    def refresh_stats(self):
        """刷新统计信息"""
        balance_info = self.transaction_service.get_balance()

        self.balance_label.config(text=f"总余额: ¥{balance_info['balance']:.2f}")
        self.income_label.config(text=f"总收入: ¥{balance_info['total_income']:.2f}")
        self.expense_label.config(text=f"总支出: ¥{balance_info['total_expense']:.2f}")

    def add_transaction(self):
        """添加交易记录"""
        try:
            # 验证数据
            amount = float(self.amount_var.get())
            if amount <= 0:
                messagebox.showerror("错误", "金额必须大于0")
                return

            category = self.category_var.get()
            if not category:
                messagebox.showerror("错误", "请选择分类")
                return

            date = self.date_var.get()
            description = self.desc_var.get()

            # 添加交易
            self.transaction_service.add_transaction(
                date, self.trans_type.get(), amount, category, description
            )

            # 清空表单并刷新
            self.clear_form()
            self.refresh_data()
            messagebox.showinfo("成功", "交易记录添加成功")

        except ValueError:
            messagebox.showerror("错误", "请输入有效的金额")
        except Exception as e:
            messagebox.showerror("错误", f"添加失败: {str(e)}")

    def clear_form(self):
        """清空表单"""
        self.amount_var.set("")
        self.desc_var.set("")

    def on_item_double_click(self, event):
        """双击交易记录事件"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            self.edit_transaction(values[0])

    def edit_transaction(self, transaction_id):
        """编辑交易记录"""
        # 这里可以实现编辑功能
        messagebox.showinfo("提示", f"编辑交易 {transaction_id} (功能开发中)")

    def show_report(self):
        """显示统计报表"""
        messagebox.showinfo("提示", "统计报表功能开发中")

    def export_data(self):
        """导出数据"""
        messagebox.showinfo("提示", "数据导出功能开发中")


