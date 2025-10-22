# 数据库设计文档

## 表结构设计
### transactions 交易表
- id: INTEGER PRIMARY KEY
- date: TEXT (交易日期)
- type: TEXT (income/expense)
- amount: REAL (金额)
- category: TEXT (分类)
- description: TEXT (描述)
- created_at: TEXT (创建时间)
- updated_at: TEXT (更新时间)

### categories 分类表
- id: INTEGER PRIMARY KEY
- name: TEXT (分类名称)
- type: TEXT (income/expense)
- color: TEXT (显示颜色)

### budgets 预算表
- id: INTEGER PRIMARY KEY
- category: TEXT (分类)
- amount: REAL (预算金额)
- month: TEXT (月份)git