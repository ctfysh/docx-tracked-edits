# Docx Tracked Edits Reference

## Core Design Principles

### 1. Minimalism Principle (极简原则)

**When generating JSON, do NOT replace whole sentences or paragraphs. Only replace key letters, words (phrases), or punctuation, and provide accurate positions whenever possible.**

#### Why?

- **Clearer revision history**: Users can see exactly what changed, not entire paragraphs marked as deleted/added
- **More precise review**: Reviewers can check changes word by word/phrase by phrase
- **Fewer conflicts**: Smaller changes are easier to merge in collaborative editing

#### Examples

| Scenario | Wrong ❌ | Right ✅ |
|----------|---------|----------|
| Fix terminology | `将 "novel approach for flood monitoring method" 改为 "improved method for flood detection"` | `将 "novel" 改为 "improved"` + `将 "monitoring" 改为 "detection"` |
| Delete redundancy | `删除: "as previously reported in our earlier studies"` | `删除: "as previously reported"` + `删除: "in our earlier studies"` |
| Fix spelling | `将 "significantly differents results" 改为 "significantly different results"` | `将 "differents" 改为 "different"` |
| Add content | `在开头插入: This is an important finding that needs to be highlighted.` | `在开头插入: Important: ` |

#### Position Requirement

When text appears multiple times in a paragraph, you **MUST** add position information:

```markdown
# Wrong ❌ (ambiguous)
删除: "the"

# Right ✅ (with position)
删除: "the" (第15-18字符)
```

### 2. Tool Diversity Principle (工具多样化原则)

**Do NOT only use replace. Use delete and insert tools as appropriate based on actual needs.**

#### Three Tools and Their Use Cases

| Tool | Use Case | Example |
|------|----------|---------|
| **replace** | Modify existing text | `将 "old" 改为 "new"` |
| **delete** | Remove redundant/incorrect content | `删除: "unnecessary text"` |
| **insert** | Add missing content | `在开头插入: Note: ` |

#### When to Use delete + insert Instead of replace?

| Scenario | Wrong ❌ | Right ✅ |
|----------|---------|----------|
| Delete entire paragraph | `将 "这是一段很长的内容..." 改为 ""` | `删除: "这是一段很长的内容..."` |
| Insert at specific position | `将 "原文" 改为 "新内容 原文"` | `在开头插入: 新内容` |
| Delete and reorganize | `将 "A, B, C" 改为 "A, C"` | `删除: ", B"` |
| Add prefix/suffix | `将 "result" 改为 "Updated: result"` | `在开头插入: Updated: ` |

## Markdown Template Syntax

### Header

The YAML frontmatter block defines metadata for the edit session.

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

All edits are organized under section headers:

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
> 选中范围: 第{start}-{end}字符
> 缩写: {initials}
```

- `Para {N}` — Paragraph number (0-indexed)
- `选中范围` — Optional character range for comment anchoring
- `缩写` — Optional author initials

### Text Edits

```markdown
Para {N}: {title}
{edit instruction}
```

| Instruction | Description |
|-------------|-------------|
| `将 "{old}" 改为 "{new}"` | Replace text |
| `在开头插入: {text}` | Insert at paragraph start |
| `在末尾插入: {text}` | Insert at paragraph end |
| `删除: "{text}"` | Delete text (no ambiguity) |
| `删除: "{text}" (第{start}-{end}字符)` | Delete with position |

### Format Edits

```markdown
Para {N}: {title}
{format1}, {format2}, ...
```

| Format | Example | Output Key |
|--------|---------|------------|
| Alignment | 居中对齐 | alignment: center |
| Alignment | 左对齐 | alignment: left |
| Alignment | 右对齐 | alignment: right |
| Alignment | 两端对齐 | alignment: justified |
| Bold | 加粗 | bold: true |
| Italic | 斜体 | italic: true |
| Underline | 下划线 | underline: true |
| Line spacing | 行距1.5倍 | line_spacing: 1.5 |
| Space before | 段前12pt | space_before: 12.0 |
| Space after | 段后6pt | space_after: 6.0 |
| Indent left | 左缩进36pt | indent_left: 36.0 |
| Indent right | 右缩进12pt | indent_right: 12.0 |
| Font size | 字号10pt | font_size: 10.0 |
| Font name | 字体SimSun | font_name: SimSun |

### Table Edits

```markdown
表格{N}:
  第{N}行下方加一行
  删掉第{N}行
  合并第{N}行的第{X}-{Y}列
  合并第{N}行的{X}个格子
```

| Instruction | Description |
|-------------|-------------|
| `第{N}行下方加一行` | Insert row after row N |
| `删掉第{N}行` | Delete row N |
| `合并第{N}行的第{X}-{Y}列` | Merge columns X through Y in row N |
| `合并第{N}行的{X}个格子` | Merge X cells in row N |

Table indices are 1-based.

### Style Edits

```markdown
{StyleName} 样式:
  {format1}, {format2}, ...
```

Applies format changes to all paragraphs using the named style.

### Global Changes

```markdown
将 "{old}" 改为 "{new}"
```

Replace text globally across all paragraphs. No `Para {N}:` prefix needed.

## Ambiguity Detection

If text appears multiple times in a paragraph, position info is required:

```markdown
删除: "text" (第15-18字符)
将 "text" 改为 "text" (第20-25字符)
```

### Error Format

When ambiguity is detected, the parser shows all occurrences:

```
歧义错误: "the" 在段落中出现 3 次:
  第15-18字符
  第42-45字符
  第78-81字符
请添加位置信息: (第N-M字符)
```

### Resolution

Add the position specifier in parentheses to disambiguate:

```markdown
# Ambiguous (error)
删除: "the"

# Resolved (valid)
删除: "the" (第42-45字符)
```

Position ranges are inclusive on both ends and 0-indexed.

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `歧义错误` | Text appears multiple times | Add `(第N-M字符)` position |
| `找不到段落` | Invalid paragraph number | Check paragraph numbering with `list_paragraphs.py` |
| `格式解析失败` | Invalid format keyword | Use keywords from the Format Edits table |
| `表格索引越界` | Table/row index out of range | Verify table structure with `list_paragraphs.py` |
| `缺少必要字段` | Missing header field | Add required fields: author, source, output |

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/list_paragraphs.py` | List docx paragraph structure with numbering |
| `scripts/md_to_json.py` | Convert Markdown template to JSON for application |

## Quick Lookup

| Task | Syntax |
|------|--------|
| Replace text | `将 "old" 改为 "new"` |
| Insert at start | `在开头插入: text` |
| Insert at end | `在末尾插入: text` |
| Delete text | `删除: "text"` |
| Bold paragraph | `Para N: 标题` then `加粗` |
| Center align | `居中对齐` |
| Set line spacing | `行距1.5倍` |
| Set font size | `字号10pt` |
| Add table row | `表格0:` then `第N行下方加一行` |
| Delete table row | `表格0:` then `删掉第N行` |
| Merge cells | `合并第N行的第X-Y列` |
| Change style | `Normal 样式:` then format list |
| Global replace | `将 "old" 改为 "new"` (no Para prefix) |
| Add comment | `Para N: 标题` then comment text |
