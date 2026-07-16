# Example 4: 多节复杂文档

演示多节文档中所有编辑类型的综合应用：文本替换、表格编辑、格式修改、样式修改、全局替换和批注。

## 文件说明

| 文件 | 说明 |
|------|------|
| `create_original.py` | 生成原始 docx（26段含标题、项目概述、技术方案、预算表、时间计划、团队、参考文献） |
| `changes.md` | 编辑指令（涵盖全部6种编辑类型） |
| `apply_changes.py` | 应用修订，生成修订版 docx |

## 演示的编辑类型

| 类型 | 具体操作 |
|------|----------|
| **Text Edits** | Tiger公司→Tiger科技有限公司、年份修正、时间调整 |
| **Table Edits** | 预算表插入行 + 合并单元格 |
| **Format Edits** | 标题居中加粗、概述两端对齐+行距、表格标题字号 |
| **Style Edits** | Heading1 样式(字号+加粗)、Normal 样式(行距+段前) |
| **Global Changes** | "项目组" → "项目团队"（全局替换，跨3个段落） |
| **Comments** | 3处批注：项目概述、时间计划、团队组建 |

## 运行方式

```bash
# 1. 生成原始文档
python examples/example_4_complex/create_original.py

# 2. 一键应用修订（自动转换 MD → JSON → docx）
python examples/example_4_complex/apply_changes.py
```

## 极简原则体现

所有文本替换均为词组级别精确修改：
- `Tiger公司` → `Tiger科技有限公司`（公司全称）
- `第1-3月` → `第1-4月`（时间微调）
- `Chen et al., 2022` → `Chen et al., 2023`（年份修正）
- 全局替换 `项目组` → `项目团队`（统一术语）
