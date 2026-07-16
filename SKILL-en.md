---
name: docx-tracked-edits
description: Edit docx files with tracked changes and comments using AI. Generates Markdown change specs that convert to docx_revision JSON format. Use when user wants to revise Word documents with tracked edits, add comments, or modify content with revision marks.
---

# Docx Tracked Edits

## Quick Start

1. **List paragraphs**: `python scripts/list_paragraphs.py paper.docx`
2. **Write changes.md** (see template below)
3. **Convert**: `python scripts/md_to_json.py changes.md changes.json`
4. **Apply**:
```python
import json
from scripts.docx_revision import ComprehensiveDocxReviewer
with open('changes.json') as f: config = json.load(f)
reviewer = ComprehensiveDocxReviewer(config['source'])
reviewer.apply_json_config(config)
reviewer.save(config['output'])
```

## Core Principles

### Minimalism
Replace key words/phrases only, NOT whole sentences. Provide positions when text appears multiple times.

| Wrong ❌ | Right ✅ |
|---------|----------|
| `Replace "novel approach for flood monitoring method" with "improved method"` | `Replace "novel" with "improved"` + `Replace "monitoring" with "detection"` |
| `Delete "as previously reported in our earlier studies"` | `Delete "as previously reported"` + `Delete "in our earlier studies"` |

### Tool Diversity
Use delete/insert when appropriate, not just replace.

| Wrong ❌ | Right ✅ |
|---------|----------|
| `Replace "long content..." with ""` | `Delete: "long content..."` |
| `Replace "original" with "new original"` | `Insert at start: new content` |

## Template

```markdown
---
author: Tiger
source: paper.docx
output: paper_revised.docx
---

# Comments

Para 24: Methodology suggestion
The three "advances" listed here overlap...
> Selection range: chars 10-50
> Initials: T

---

# Text Edits

Para 8: Title correction
Replace "novel approach" with "improved method"

Para 23: Add content
Insert at start: Updated: 
Insert at end: (validated)

Para 67: Remove redundancy
Delete: "as previously reported"

---

# Format Edits

Para 12: Paragraph format
Center align, line spacing 1.5, space before 12pt

---

# Table Edits

Table 0:
  Insert row after row 2
  Delete row 5
  Merge cells in row 2

---

# Style Edits

Normal style:
  Space before 6pt, space after 6pt

Heading1 style:
  Font size 16pt, bold

---

# Global Changes

Replace "significant difference" with "statistically significant difference"
```

## Quick Syntax

| Type | Syntax |
|------|--------|
| Replace | `Replace "old" with "new"` |
| Insert start | `Insert at start: text` |
| Insert end | `Insert at end: text` |
| Delete | `Delete: "text"` or `Delete: "text" (chars 15-18)` |
| Format | `Center align, Bold, Line spacing 1.5` |
| Table | `Insert row after row N`, `Delete row N`, `Merge columns X-Y in row N` |
| Style | `Normal style: Font size 10pt, Bold` |
| Global | `Replace "old" with "new"` (no Para prefix) |

See [REFERENCE.md](REFERENCE.md) for full syntax reference.

## Workflow

1. Read source docx (list_paragraphs.py)
2. Generate changes.md
3. Convert to JSON (md_to_json.py)
4. If ambiguity error, add position info and regenerate
5. Apply to docx

## Scripts

- `scripts/list_paragraphs.py` - List paragraph structure
- `scripts/md_to_json.py` - Convert Markdown to JSON
- `scripts/docx_revision/` - Bundled package