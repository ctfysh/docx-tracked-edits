# Docx Tracked Edits - Core Syntax

## Template Header

```yaml
---
author: Name
source: path.docx
output: path_revised.docx
---
```

## Edit Types

| Type | Syntax |
|------|--------|
| **Replace** | `Replace "old" with "new"` |
| **Insert start** | `Insert at start: text` |
| **Insert end** | `Insert at end: text` |
| **Delete** | `Delete: "text"` or `Delete: "text" (chars 15-18)` |
| **Format** | `Center align, Bold, Line spacing 1.5` |
| **Table** | `Insert row after row N`, `Delete row N`, `Merge columns X-Y in row N` |
| **Style** | `Normal style: Font size 10pt, Bold` |
| **Global** | `Replace "old" with "new"` (no Para prefix) |

## Section Headers

```
# Comments
# Text Edits
# Format Edits
# Table Edits
# Style Edits
# Global Changes
```

## Comment Format

```
Para {N}: {title}
{comment text}
> Selection range: chars {start}-{end}
> Initials: {initials}
```

## Rules

1. **Minimalism**: Replace words, not sentences
2. **Position**: Add `(chars N-M)` when text appears multiple times
3. **Tool diversity**: Use delete/insert, not just replace

See REFERENCE-en.md for full examples and error handling.
