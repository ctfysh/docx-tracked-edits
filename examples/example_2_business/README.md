[English](#example-2-business-report) | [中文](#示例-2商业报告)

# Example 2: Business Report

Demonstrates a complete business report workflow: text updates, table edits (insert/delete rows), and format adjustments.

## File Description

| File | Description |
|------|-------------|
| `create_original.py` | Generate original docx (with 5-row sales data table) |
| `changes.md` | Edit instructions (text + table + format) |
| `apply_changes.py` | Apply revisions, generate revised docx |

## Demonstrated Edit Types

- **replace** — Update year (2023→2024) and amount ($1.2M→$1.5M)
- **insert_row** — Insert new row after row 2 in table
- **delete_row** — Delete row 5 in table
- **format** — Title center align + bold

## Tool Diversity in Action

- **replace**: Text replacement (year, amount)
- **insert**: Table row insertion
- **delete**: Table row deletion

## How to Run

```bash
# 1. Generate original document
python examples/example_2_business/create_original.py

# 2. Apply revisions (auto-convert MD → JSON → docx)
python examples/example_2_business/apply_changes.py
```

## Minimalism Principle in Action

All replacements are precise word/number-level modifications:
- `2023` → `2024` (year update)
- `$1.2M` → `$1.5M` (amount update)

No whole-sentence or whole-paragraph rewrites.

---

[English](#example-2-business-report) | [中文](#示例-2商业报告)

# 示例 2：商业报告

演示商业报告场景的完整工作流：文本更新、表格编辑（插入/删除行）、格式修改。

## 文件说明

| 文件 | 说明 |
|------|------|
| `create_original.py` | 生成原始 docx（含5行销售数据表格） |
| `changes.md` | 编辑指令（文本+表格+格式） |
| `apply_changes.py` | 应用修订，生成修订版 docx |

## 演示的编辑类型

- **replace** — 更新年份（2023年→2024年）和金额（$1.2M→$1.5M）
- **insert_row** — 在表格第2行下方插入新行
- **delete_row** — 删除表格第5行
- **format** — 标题居中对齐 + 加粗

## 工具多样化原则体现

- **replace**: 文本替换（年份、金额）
- **insert**: 表格插入行
- **delete**: 表格删除行

## 运行方式

```bash
# 1. 生成原始文档
python examples/example_2_business/create_original.py

# 2. 一键应用修订（自动转换 MD → JSON → docx）
python examples/example_2_business/apply_changes.py
```

## 极简原则体现

所有替换都是精确的单词/数字级别修改：
- `2023年` → `2024年`（年份更新）
- `$1.2M` → `$1.5M`（金额更新）

没有整句整段的重写。