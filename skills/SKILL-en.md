---
name: docx-tracked-edits
description: Edit docx files with tracked changes and comments using AI. Generates Markdown change specs that convert to docx_revision JSON format. Use when user wants to revise Word documents with tracked edits, add comments, or modify content with revision marks.
---

# Docx Tracked Edits

## Core Function

**This skill does two things:**

1. **Parse template**: Read modification instructions in standard format
2. **Execute revision**: Apply changes to Word document

## Quick Start

1. **Review phase**: Other AI reads the document, identifies issues
2. **Template phase**: Other AI outputs issue list in this skill's template format
3. **Execution phase**: This skill parses the template, applies changes
4. **Result phase**: User receives the revised document

**Key: This skill defines the standard template format for modification instructions. Other AI tools must output in this format for this skill to parse and execute.**

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

## Template Format

```yaml
---
author: Tiger
source: paper.docx
output: paper_revised.docx
---
```

See [../references/REFERENCE-core-en.md](../references/REFERENCE-core-en.md) for full syntax. See [../references/REFERENCE-en.md](../references/REFERENCE-en.md) for examples and error handling.

## What NOT to Do

| ❌ Don't | ✅ Do Instead |
|---------|--------------|
| Replace entire sentences | Replace only the specific words/phrases |
| Use `Replace "long text..." with ""` | Use `Delete: "long text..."` |
| Modify document without generating changes.md | Always generate changes.md first, then apply |
| Skip ambiguity check when text appears multiple times | Add `(chars N-M)` position when ambiguity detected |
| Apply changes without user confirmation | Show changes.md to user, wait for confirmation |
| Use `Para N:` for global replacements | Omit `Para N:` prefix for global changes |

1. Read source docx (list_paragraphs.py)
2. Generate changes.md
3. Convert to JSON (md_to_json.py)
4. If ambiguity error, add position info and regenerate
5. Apply to docx

## Scripts

- `scripts/list_paragraphs.py` - List paragraph structure
- `scripts/md_to_json.py` - Convert Markdown to JSON
- `scripts/docx_revision/` - Bundled package
