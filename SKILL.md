---
name: docx-tracked-edits
description: Edit docx files with tracked changes and comments using AI. Generates Markdown change specs that convert to docx_revision JSON format. Use when user wants to revise Word documents with tracked edits, add comments, or modify content with revision marks.
---

# Docx Tracked Edits

## Language Detection / 语言检测

**Auto-detect user language and load the appropriate skill file:**

- If user's request is in **English** → Load `SKILL-en.md`
- If user's request is in **Chinese** → Load `SKILL-zh.md`
- If ambiguous → Ask user to choose: "Please specify language: English or 中文?"

## File Structure / 文件结构

| File | Purpose |
|------|---------|
| `SKILL.md` | This file - language router |
| `SKILL-en.md` | English version of the skill |
| `SKILL-zh.md` | Chinese version of the skill |
| `REFERENCE-en.md` | English syntax reference |
| `REFERENCE-zh.md` | Chinese syntax reference |
| `examples/` | Working examples with Python code |
| `scripts/` | Implementation scripts |

## Quick Links / 快速链接

### English
- [SKILL-en.md](SKILL-en.md) - Full skill instructions
- [REFERENCE-en.md](REFERENCE-en.md) - Syntax reference

### 中文
- [SKILL-zh.md](SKILL-zh.md) - 完整技能说明
- [REFERENCE-zh.md](REFERENCE-zh.md) - 语法参考

## Core Workflow / 核心工作流

1. **List paragraphs** to understand document structure
2. **Write changes** in Markdown format
3. **Convert to JSON** using `md_to_json.py`
4. **Apply to docx** using `docx_revision`

## Examples / 示例

See `examples/` directory for complete working demos:
- `example_1_academic/` - Academic paper editing
- `example_2_business/` - Business report
- `example_3_legal/` - Legal document
- `example_4_complex/` - Complex multi-section document

Run all examples:
```bash
bash examples/run_all_examples.sh
```