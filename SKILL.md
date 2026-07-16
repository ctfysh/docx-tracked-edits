---
name: docx-tracked-edits
description: Edit docx files with tracked changes and comments using AI. Generates Markdown change specs that convert to docx_revision JSON format. Use when user wants to revise Word documents with tracked edits, add comments, or modify content with revision marks.
---

# Docx Tracked Edits

## Quick Start

1. **Read source docx** to understand paragraph structure:
   ```bash
   python scripts/list_paragraphs.py paper.docx
   ```

2. **Generate changes.md** using the template below

3. **Convert to JSON**:
   ```bash
   python scripts/md_to_json.py changes.md changes.json
   ```

4. **Apply to docx** (using docx_revision):
   ```python
   import json
   from scripts.docx_revision import ComprehensiveDocxReviewer
   
   with open('changes.json') as f:
       config = json.load(f)
   
   reviewer = ComprehensiveDocxReviewer(config['source'])
   reviewer.apply_json_config(config)
   reviewer.save(config['output'])
   ```

## Changes Markdown Template

```markdown
---
author: Tiger
source: paper.docx
output: paper_revised.docx
track_revisions: true
---

# Comments

Para 24: 方法论建议
此处列出的三项"进展"表述清晰但部分重叠...
> 选中范围: 第10-50字符
> 缩写: T

---

# Text Edits

Para 8: 标题修正
将 "novel approach" 改为 "improved method"

Para 23: 补充内容
在开头插入: Updated: 
在末尾插入: (validated)

Para 67: 删除冗余
删除: "as previously reported"

Para 82: 删除有歧义
删除: "the" (第15-18字符)

---

# Format Edits

Para 12: 段落格式
居中对齐, 行距1.5倍, 段前12pt

Para 45-48: 缩进
左缩进36pt

---

# Table Edits

表格0:
  第2行下方加一行
  删掉第5行
  合并第二行的三个格子

---

# Style Edits

Normal 样式:
  段前6pt, 段后6pt

Heading1 样式:
  字号16pt, 加粗

---

# Global Changes

将全文 "significant difference" 改为 "statistically significant difference"
```

## Syntax Reference

### Header (YAML frontmatter)
| Field | Required | Description |
|-------|----------|-------------|
| author | Yes | Default author for all changes |
| source | Yes | Path to source docx file |
| output | Yes | Path for output docx file |
| track_revisions | No | Enable tracked changes (default: true) |

### Comments
```markdown
Para {N}: {title}
{comment text}
> 选中范围: 第{start}-{end}字符
> 缩写: {initials}
```

### Text Edits
- **Replace**: `将 "{old}" 改为 "{new}"`
- **Insert at start**: `在开头插入: {text}`
- **Insert at end**: `在末尾插入: {text}`
- **Delete**: `删除: "{text}"` or `删除: "{text}" (第{start}-{end}字符)`

### Format Edits
```markdown
Para {N}: {title}
{format1}, {format2}, ...
```

Supported formats:
- 居中对齐, 左对齐, 右对齐, 两端对齐
- 加粗, 斜体
- 行距{N}倍, 段前{N}pt, 段后{N}pt
- 左缩进{N}pt, 右缩进{N}pt
- 字号{N}pt

### Table Edits
```markdown
表格{N}:
  第{N}行下方加一行
  删掉第{N}行
  合并第{N}行的{X}-{Y}列
  合并第{N}行的{X}个格子
```

### Style Edits
```markdown
{StyleName} 样式:
  {format1}, {format2}, ...
```

### Global Changes
```markdown
将 "{old}" 改为 "{new}"
```

## Ambiguity Detection

If text appears multiple times in a paragraph, the script will show an error with all positions and ask you to add position information.

## Workflows

1. Read source docx (using list_paragraphs.py or directly)
2. Generate changes.md
3. Run `md_to_json.py changes.md changes.json`
4. If ambiguity error, resolve with user and regenerate MD
5. Apply to docx

## Scripts

- `scripts/list_paragraphs.py` - List docx paragraph structure
- `scripts/md_to_json.py` - Convert Markdown to docx_revision JSON
- `scripts/docx_revision/` - Bundled docx_revision package
