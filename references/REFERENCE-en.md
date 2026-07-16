# Docx Tracked Edits Reference

**This skill does two things:**

1. **Parse template**: Read modification instructions in standard format
2. **Execute revision**: Apply changes to Word document

**This file defines the standard template format for modification instructions (template protocol). Other AI tools must output issue lists in this format for this skill to parse and execute.**

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

#### When to Use delete + Insert Instead of replace?

| Scenario | Wrong ❌ | Right ✅ |
|----------|---------|----------|
| Delete entire paragraph | `Replace "This is a very long content..." with ""` | `Delete: "This is a very long content..."` |
| Insert at specific position | `Replace "original" with "new content original"` | `Insert at start: new content` |
| Delete and reorganize | `Replace "A, B, C" with "A, C"` | `Delete: ", B"` |
| Add prefix/suffix | `Replace "result" with "Updated: result"` | `Insert at start: Updated: ` |

## Markdown Template Syntax

### Header

```yaml
---
author: Name
source: path.docx
output: path_revised.docx
track_revisions: true
---
```

| Field | Required | Description |
|-------|----------|-------------|
| `author` | Yes | Author name shown in tracked changes |
| `source` | Yes | Path to the source .docx file |
| `output` | Yes | Path for the revised output .docx file |
| `track_revisions` | No | Enable revision tracking (default: true) |

### Section Headers

```markdown
# Comments
# Text Edits
# Format Edits
# Table Edits
# Style Edits
# Global Changes
```

### Comments

```markdown
Para {N}: {title}
{comment text}
> Selection range: chars {start}-{end}
> Initials: {initials}
```

### Text Edits

| Instruction | Description |
|-------------|-------------|
| `Replace "{old}" with "{new}"` | Replace text |
| `Insert at start: {text}` | Insert at paragraph start |
| `Insert at end: {text}` | Insert at paragraph end |
| `Delete: "{text}"` | Delete text (no ambiguity) |
| `Delete: "{text}" (chars {start}-{end})` | Delete with position |

### Format Edits

```markdown
Para {N}: {title}
{format1}, {format2}, ...
```

| Format | Example | Output Key |
|--------|---------|------------|
| Alignment | Center align | alignment: center |
| Alignment | Left align | alignment: left |
| Alignment | Right align | alignment: right |
| Alignment | Justify | alignment: justified |
| Bold | Bold | bold: true |
| Italic | Italic | italic: true |
| Underline | Underline | underline: true |
| Line spacing | Line spacing 1.5 | line_spacing: 1.5 |
| Space before | Space before 12pt | space_before: 12.0 |
| Space after | Space after 6pt | space_after: 6.0 |
| Indent left | Left indent 36pt | indent_left: 36.0 |
| Indent right | Right indent 12pt | indent_right: 12.0 |
| Font size | Font size 10pt | font_size: 10.0 |
| Font name | Font SimSun | font_name: SimSun |

### Table Edits

```markdown
Table {N}:
  Insert row after row {N}
  Delete row {N}
  Merge columns {X}-{Y} in row {N}
  Merge {X} cells in row {N}
```

Table indices are 1-based.

### Style Edits

```markdown
{StyleName} style:
  {format1}, {format2}, ...
```

### Global Changes

```markdown
Replace "{old}" with "{new}"
```

No `Para {N}:` prefix needed.

## Ambiguity Detection

If text appears multiple times, add position:

```markdown
Delete: "text" (chars 15-18)
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `Ambiguity error` | Text appears multiple times | Add `(chars N-M)` position |
| `Paragraph not found` | Invalid paragraph number | Check with `list_paragraphs.py` |
| `Format parse failed` | Invalid format keyword | Use keywords from Format table |
| `Table index out of range` | Index out of range | Verify with `list_paragraphs.py` |
| `Missing required field` | Missing header field | Add: author, source, output |

## Quick Lookup

| Task | Syntax |
|------|--------|
| Replace text | `Replace "old" with "new"` |
| Insert at start | `Insert at start: text` |
| Insert at end | `Insert at end: text` |
| Delete text | `Delete: "text"` |
| Bold paragraph | `Para N: Title` then `Bold` |
| Center align | `Center align` |
| Set line spacing | `Line spacing 1.5` |
| Set font size | `Font size 10pt` |
| Add table row | `Table 0:` then `Insert row after row N` |
| Delete table row | `Table 0:` then `Delete row N` |
| Merge cells | `Merge columns X-Y in row N` |
| Change style | `Normal style:` then format list |
| Global replace | `Replace "old" with "new"` (no Para prefix) |
| Add comment | `Para N: Title` then comment text |
