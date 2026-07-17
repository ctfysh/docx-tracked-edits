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

## Failure Modes & Recovery

| Symptom | Trigger | Recovery |
|---------|---------|----------|
| Ambiguity error | Text appears multiple times in paragraph | Add `(chars N-M)` position to specify exact match |
| Paragraph not found | Invalid paragraph number | Run `list_paragraphs.py` to get valid paragraph indices |
| Text not found | Target text doesn't exist in paragraph | Check spelling, run `list_paragraphs.py` to verify content |
| Format parse error | Invalid format keyword | Use only: `Center align`, `Bold`, `Justify align`, `Line spacing N`, `Font size Npt` |
| Table index out of range | Table number exceeds document tables | Check document structure, verify table exists |
| JSON parse error | Invalid changes.md format | Ensure YAML frontmatter with `author`, `source`, `output` fields |

| ❌ Don't | ✅ Do Instead |
|---------|--------------|
| Replace entire sentences | Replace only the specific words/phrases |
| Use `Replace "long text..." with ""` | Use `Delete: "long text..."` |
| Modify document without generating changes.md | Always generate changes.md first, then apply |
| Skip ambiguity check when text appears multiple times | Add `(chars N-M)` position when ambiguity detected |
| Apply changes without user confirmation | Show changes.md to user, wait for confirmation |
| Use `Para N:` for global replacements | Omit `Para N:` prefix for global changes |

## Workflow

### Step 1: Read Source Document
```bash
python scripts/list_paragraphs.py source.docx
```
- **Input**: source.docx
- **Output**: Paragraph list with indices and preview text
- **Purpose**: Understand document structure, identify paragraph numbers for edits

### Step 2: Generate changes.md
Create modification instructions in template format:
```yaml
---
author: Your Name
source: source.docx
output: revised.docx
---

# Text Edits
Para N: Description
Replace "old" with "new"

# Format Edits
Para N: Description
Center align, Bold
```
- **Input**: User requirements + paragraph structure from Step 1
- **Output**: changes.md file

### Step 3: Convert to JSON
```bash
python scripts/md_to_json.py changes.md changes.json
```
- **Input**: changes.md
- **Output**: changes.json (or error with position suggestions)
- **Error handling**: If ambiguity error, add position info and regenerate

### Step 4: Apply Revisions
```bash
python scripts/docx_revision/reviewer.py changes.json
```
- **Input**: changes.json + source.docx
- **Output**: revised.docx with tracked changes
- **Verification**: Open in Word to review tracked changes

## Scripts

- `scripts/list_paragraphs.py` - List paragraph structure
- `scripts/md_to_json.py` - Convert Markdown to JSON
- `scripts/docx_revision/` - Bundled package
