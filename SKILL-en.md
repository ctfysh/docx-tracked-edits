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

## Core Design Principles

### 1. Minimalism Principle

**When generating JSON, do NOT replace whole sentences or paragraphs. Only replace key letters, words (phrases), or punctuation, and provide accurate positions whenever possible.**

#### Why?

- **Clearer revision history**: Users can see exactly what changed, not entire paragraphs marked as deleted/added
- **More precise review**: Reviewers can check changes word by word/phrase by phrase
- **Fewer conflicts**: Smaller changes are easier to merge in collaborative editing

#### Examples

| Scenario | Wrong ❌ | Right ✅ |
|----------|---------|----------|
| Fix terminology | `Replace "novel approach for flood monitoring method" with "improved method for flood detection"` | `Replace "novel" with "improved"` + `Replace "monitoring" with "detection"` |
| Delete redundancy | `Delete "as previously reported in our earlier studies"` | `Delete "as previously reported"` + `Delete "in our earlier studies"` |
| Fix spelling | `Replace "significantly differents results" with "significantly different results"` | `Replace "differents" with "different"` |
| Add content | `Insert at start: This is an important finding that needs to be highlighted.` | `Insert at start: Important: ` |

#### Position Requirement

When text appears multiple times in a paragraph, you **MUST** add position information:

```markdown
# Wrong ❌ (ambiguous)
Delete: "the"

# Right ✅ (with position)
Delete: "the" (chars 15-18)
```

### 2. Tool Diversity Principle

**Do NOT only use replace. Use delete and insert tools as appropriate based on actual needs.**

#### Three Tools and Their Use Cases

| Tool | Use Case | Example |
|------|----------|---------|
| **replace** | Modify existing text | `Replace "old" with "new"` |
| **delete** | Remove redundant/incorrect content | `Delete: "unnecessary text"` |
| **insert** | Add missing content | `Insert at start: Note: ` |

#### When to Use delete + insert Instead of replace?

| Scenario | Wrong ❌ | Right ✅ |
|----------|---------|----------|
| Delete entire paragraph | `Replace "This is a very long content..." with ""` | `Delete: "This is a very long content..."` |
| Insert at specific position | `Replace "original" with "new content original"` | `Insert at start: new content` |
| Delete and reorganize | `Replace "A, B, C" with "A, C"` | `Delete: ", B"` |
| Add prefix/suffix | `Replace "result" with "Updated: result"` | `Insert at start: Updated: ` |

#### Combined Example

```markdown
# Text Edits

Para 15: Fix terminology
Replace "novel" with "improved"

Para 23: Remove redundancy
Delete: "as previously reported"

Para 32: Add note
Insert at start: Note: 
Insert at end: (validated)

Para 45: Fix spelling
Replace "differents" with "different"
```

**This generates JSON with:**
- 1 replace (novel → improved)
- 1 delete (as previously reported)
- 2 inserts (Note: and (validated))
- 1 replace (differents → different)

**NOT** one big replace for the entire paragraph.

## Changes Markdown Template

```markdown
---
author: Tiger
source: paper.docx
output: paper_revised.docx
track_revisions: true
---

# Comments

Para 24: Methodology suggestion
The three "advances" listed here are clear but partially overlap...
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

Para 82: Delete with ambiguity
Delete: "the" (chars 15-18)

---

# Format Edits

Para 12: Paragraph format
Center align, line spacing 1.5, space before 12pt

Para 45-48: Indentation
Left indent 36pt

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

Replace all "significant difference" with "statistically significant difference"
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
> Selection range: chars {start}-{end}
> Initials: {initials}
```

### Text Edits
- **Replace**: `Replace "{old}" with "{new}"`
- **Insert at start**: `Insert at start: {text}`
- **Insert at end**: `Insert at end: {text}`
- **Delete**: `Delete: "{text}"` or `Delete: "{text}" (chars {start}-{end})`

### Format Edits
```markdown
Para {N}: {title}
{format1}, {format2}, ...
```

Supported formats:
- Center align, Left align, Right align, Justify
- Bold, Italic
- Line spacing {N}, Space before {N}pt, Space after {N}pt
- Left indent {N}pt, Right indent {N}pt
- Font size {N}pt

### Table Edits
```markdown
Table {N}:
  Insert row after row {N}
  Delete row {N}
  Merge columns {X}-{Y} in row {N}
  Merge {X} cells in row {N}
```

### Style Edits
```markdown
{StyleName} style:
  {format1}, {format2}, ...
```

### Global Changes
```markdown
Replace "{old}" with "{new}"
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