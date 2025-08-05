# 家庭支出看板 / Family Expense Dashboard

这是一个使用 Python + Dash 构建的家庭支出可视化应用，旨在帮助用户记录、分析和理解家庭日常支出情况。它支持按分类、按时间、按支付人等维度进行可视化展示，适合家庭成员共用、监督预算。

This is a household expense dashboard built with Python and Dash, designed to help users track, analyze, and understand family spending. It supports multi-dimensional visualizations by category, date, and payer. Ideal for collaborative household budgeting.

---

## ✨ 功能 Features

- 📊 支出分类饼图（按“分类”字段）
- 📈 每日支出趋势图（按“日期”字段）
- 📅 月度支出趋势图（含预算线）
- 👨‍👩‍👧‍👦 按“支付人”堆叠柱状图
- 📌 预算使用进度条 + 超额提示
- 🔄 一键更新图表（重新读取 CSV 文件）

---

## 📂 数据格式（CSV 示例）

程序读取 `family_budget.csv` 文件，要求包含以下列：

| 日期        | 分类   | 支付人 | 金额 |
|-------------|--------|--------|------|
| 2025/08/01  | 餐饮   | 妈妈   | 80   |
| 2025/08/02  | 交通   | 爸爸   | 50   |

> ⚠️ 日期建议格式为 `YYYY/MM/DD`，程序会自动解析为日期格式。

---

## 🚀 如何运行 How to Run

1. 克隆项目到本地：

```bash
git clone https://github.com/jiaxin-aidi-wu/family-expense-dashboard.git
cd family-expense-dashboard
```
2. 安装依赖：

```
pip install dash pandas plotly
```

3. 运行程序：

```
python app.py
```
默认将在浏览器打开：http://127.0.0.1:8050

一个最小可用的家庭支出看板就完成了✅
✅ The MVP of the family expense dashboard is done!
