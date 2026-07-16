# Docx Tracked Edits

AI-driven docx editing with tracked changes. Edit Word documents using readable Markdown templates.

## Features

- **Markdown-based editing**: Write changes in human-readable Markdown
- **Tracked changes**: All edits shown as Word tracked changes
- **Comments support**: Add comments with selected text ranges
- **Format editing**: Change alignment, spacing, indentation, bold/italic
- **Table editing**: Insert/delete rows, merge cells
- **Style editing**: Modify paragraph styles
- **Ambiguity detection**: Error with positions when text appears multiple times
- **Chinese support**: Natural language syntax (居中对齐, 行距1.5倍, etc.)

## Installation

Copy the `scripts/` directory to your OpenCode skills folder:

```bash
cp -r scripts/ ~/.config/opencode/skills/docx-tracked-edits/scripts/
cp SKILL.md ~/.config/opencode/skills/docx-tracked-edits/
cp REFERENCE.md ~/.config/opencode/skills/docx-tracked-edits/
cp EXAMPLES.md ~/.config/opencode/skills/docx-tracked-edits/
```

## Quick Start

1. **List paragraphs** in source docx:
   ```bash
   python scripts/list_paragraphs.py paper.docx
   ```

2. **Write changes** in Markdown (see REFERENCE.md for syntax)

3. **Convert to JSON**:
   ```bash
   python scripts/md_to_json.py changes.md changes.json
   ```

4. **Apply to docx**:
   ```python
   import json
   from scripts.docx_revision import ComprehensiveDocxReviewer
   
   with open('changes.json') as f:
       config = json.load(f)
   
   reviewer = ComprehensiveDocxReviewer(config['source'])
   reviewer.apply_json_config(config)
   reviewer.save(config['output'])
   ```

## Markdown Syntax

```markdown
---
author: Name
source: input.docx
output: output.docx
---

# Comments
Para 24: Title
Comment text here
> 选中范围: 第10-50字符
> 缩写: T

# Text Edits
将 "old" 改为 "new"
在开头插入: text
在末尾插入: text
删除: "text"

# Format Edits
Para 12: 标题
居中对齐, 行距1.5倍, 段前12pt

# Table Edits
表格0:
  第2行下方加一行
  删掉第5行
  合并第一行的A-C列

# Style Edits
Normal 样式:
  段前6pt, 段后6pt

# Global Changes
将 "old" 改为 "new"
```

## Scripts

| Script | Purpose |
|--------|---------|
| `list_paragraphs.py` | List docx paragraph structure |
| `md_to_json.py` | Convert Markdown to docx_revision JSON |
| `docx_revision/` | Bundled docx_revision package |

## Testing

```bash
python scripts/md_to_json.py --test
```

## Documentation

- [REFERENCE.md](REFERENCE.md) - Full syntax reference
- [EXAMPLES.md](EXAMPLES.md) - Real-world examples
- [SKILL.md](SKILL.md) - OpenCode skill definition

## License

MIT
