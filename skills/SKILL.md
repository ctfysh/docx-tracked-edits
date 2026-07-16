---
name: docx-tracked-edits
description: Edit docx files with tracked changes and comments using AI. Generates Markdown change specs that convert to docx_revision JSON format. Use when user wants to revise Word documents with tracked edits, add comments, or modify content with revision marks.
---

# Docx Tracked Edits

## Core Function

**This skill does two things:**

1. **Parse template**: Read modification instructions in standard format
2. **Execute revision**: Apply changes to Word document

```
Modification instructions → Parse template → Apply revision → Revised document
```

## Language Detection

**Auto-detect user language and load the appropriate skill file:**

- If user's request is in **English** → Load `SKILL-en.md`
- If user's request is in **Chinese** → Load `SKILL-zh.md`
- If ambiguous → Ask user to choose: "Please specify language: English or 中文?"

## Quick Start

1. **Review phase**: Other AI reads the document, identifies issues
2. **Template phase**: Other AI outputs issue list in this skill's template format
3. **Execution phase**: This skill parses the template, applies changes
4. **Result phase**: User receives the revised document

**Key: This skill defines the standard template format for modification instructions. Other AI tools must output in this format for this skill to parse and execute.**

## Template Format

```yaml
---
author: Tiger
source: paper.docx
output: paper_revised.docx
---
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

See [../references/REFERENCE-core-en.md](../references/REFERENCE-core-en.md) for full syntax. See [../references/REFERENCE-en.md](../references/REFERENCE-en.md) for examples and error handling.

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
