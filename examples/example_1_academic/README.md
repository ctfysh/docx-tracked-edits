[English](#example-1-academic-paper-editing) | [中文](#示例-1学术论文编辑)

# Example 1: Academic Paper Editing

Demonstrates a complete academic paper review workflow: terminology fixes, redundancy removal, typo corrections, comments, and format adjustments.

## File Description

| File | Description |
|------|-------------|
| `create_original.py` | Generate original docx (21-paragraph academic paper structure) |
| `changes.md` | Edit instructions (following minimalism principle) |
| `apply_changes.py` | Apply revisions, generate revised docx |

## Demonstrated Edit Types

- **replace** — Multiple small replacements (novel→improved, monitoring→detection, demonstrates→shows)
- **delete** — Remove redundant opening ("As previously reported in our earlier studies, ")
- **Fix repetition** — "The the" → "The"
- **comment** — Add terminology suggestion comment on Para 8
- **format** — Para 8 center align + bold

## How to Run

```bash
# 1. Generate original document
python examples/example_1_academic/create_original.py

# 2. Apply revisions (auto-convert MD → JSON → docx)
python examples/example_1_academic/apply_changes.py
```

## Minimalism Principle in Action

All replacements are word-level precise modifications, no whole-sentence or whole-paragraph replacements:
- `novel` → `improved` (1 word)
- `monitoring` → `detection` (1 word)
- `demonstrates` → `shows` (1 word)
- `The the` → `The` (fix repetition)
- Delete redundant phrase instead of rewriting entire paragraph

---

[English](#example-1-academic-paper-editing) | [中文](#示例-1学术论文编辑)

# 示例 1：学术论文编辑

演示学术论文审阅场景的完整工作流：术语修正、冗余删除、重复词修复、批注和格式修改。

## 文件说明

| 文件 | 说明 |
|------|------|
| `create_original.py` | 生成原始 docx（21段学术论文结构） |
| `changes.md` | 编辑指令（遵循极简原则） |
| `apply_changes.py` | 应用修订，生成修订版 docx |

## 演示的编辑类型

- **replace** — 多个小替换（novel→improved, monitoring→detection, demonstrates→shows）
- **delete** — 删除冗余开头（"As previously reported in our earlier studies, "）
- **修复重复词** — "The the" → "The"
- **comment** — 在 Para 8 添加术语建议批注
- **format** — Para 8 居中对齐 + 加粗

## 运行方式

```bash
# 1. 生成原始文档
python examples/example_1_academic/create_original.py

# 2. 一键应用修订（自动转换 MD → JSON → docx）
python examples/example_1_academic/apply_changes.py
```

## 极简原则体现

所有替换都是单词级别的精确修改，没有整句整段的替换：
- `novel` → `improved`（1个词）
- `monitoring` → `detection`（1个词）
- `demonstrates` → `shows`（1个词）
- `The the` → `The`（修复重复词）
- 删除冗余短语而非整段重写