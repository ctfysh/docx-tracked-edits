[English](#docx-tracked-edits) | [中文](#docx-tracked-edits-1)

---

# Docx Tracked Edits

AI-driven docx editing with tracked changes. Edit Word documents using readable Markdown templates.

## Features

- **Markdown-based editing**: Write changes in human-readable Markdown
- **Tracked changes**: All edits shown as Word tracked changes
- **Comments support**: Add comments with selected text ranges
- **Format/Table/Style editing**: Full document formatting control
- **Ambiguity detection**: Error with positions when text appears multiple times
- **Chinese support**: Natural language syntax (居中对齐, 行距1.5倍, etc.)

## Quick Start

```bash
# 1. List paragraphs
python scripts/list_paragraphs.py paper.docx

# 2. Write changes.md (see REFERENCE.md for syntax)

# 3. Convert to JSON
python scripts/md_to_json.py changes.md changes.json

# 4. Apply to docx
python -c "
import json
from scripts.docx_revision import ComprehensiveDocxReviewer
with open('changes.json') as f: config = json.load(f)
reviewer = ComprehensiveDocxReviewer(config['source'])
reviewer.apply_json_config(config)
reviewer.save(config['output'])
"
```

## Examples

| Example | Description |
|---------|-------------|
| [example_1_academic](examples/example_1_academic/) | Fix terminology, remove redundancy, add comments |
| [example_2_business](examples/example_2_business/) | Update dates, amounts, table edits |
| [example_3_legal](examples/example_3_legal/) | Contract revision, definitions, risk comments |
| [example_4_complex](examples/example_4_complex/) | All edit types combined |

```bash
bash examples/run_all_examples.sh  # Run all examples
```

## Documentation

- [REFERENCE.md](REFERENCE.md) - Full syntax reference (bilingual)
- [SKILL.md](SKILL.md) - OpenCode skill definition

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/list_paragraphs.py` | List docx paragraph structure |
| `scripts/md_to_json.py` | Convert Markdown to docx_revision JSON |
| `scripts/docx_revision/` | Bundled docx_revision package |

---

[English](#docx-tracked-edits) | [中文](#docx-tracked-edits-1)

# Docx Tracked Edits

AI 驱动的 docx 修订模式编辑。使用可读的 Markdown 模板编辑 Word 文档。

## 功能特性

- **基于 Markdown 的编辑**：使用可读的 Markdown 编写修改
- **修订跟踪**：所有编辑显示为 Word 修订标记
- **批注支持**：添加带选中范围的批注
- **格式/表格/样式编辑**：完整的文档格式控制
- **歧义检测**：文本多次出现时显示带位置的错误
- **中文支持**：自然语言语法（居中对齐, 行距1.5倍等）

## 快速开始

```bash
# 1. 列出段落
python scripts/list_paragraphs.py paper.docx

# 2. 编写 changes.md（语法见 REFERENCE.md）

# 3. 转换为 JSON
python scripts/md_to_json.py changes.md changes.json

# 4. 应用到 docx
python -c "
import json
from scripts.docx_revision import ComprehensiveDocxReviewer
with open('changes.json') as f: config = json.load(f)
reviewer = ComprehensiveDocxReviewer(config['source'])
reviewer.apply_json_config(config)
reviewer.save(config['output'])
"
```

## 示例

| 示例 | 说明 |
|------|------|
| [example_1_academic](examples/example_1_academic/) | 修正术语、删除冗余、添加批注 |
| [example_2_business](examples/example_2_business/) | 更新日期、金额、表格编辑 |
| [example_3_legal](examples/example_3_legal/) | 合同修订、定义插入、风险批注 |
| [example_4_complex](examples/example_4_complex/) | 所有编辑类型组合 |

```bash
bash examples/run_all_examples.sh  # 运行所有示例
```

## 文档

- [REFERENCE.md](REFERENCE.md) - 完整语法参考（双语）
- [SKILL.md](SKILL.md) - OpenCode 技能定义

## 脚本

| 脚本 | 用途 |
|------|------|
| `scripts/list_paragraphs.py` | 列出 docx 段落结构 |
| `scripts/md_to_json.py` | 将 Markdown 转换为 docx_revision JSON |
| `scripts/docx_revision/` | 内置的 docx_revision 包 |