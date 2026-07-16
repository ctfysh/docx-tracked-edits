---
name: docx-tracked-edits
description: Edit docx files with tracked changes and comments using AI. Generates Markdown change specs that convert to docx_revision JSON format. Use when user wants to revise Word documents with tracked edits, add comments, or modify content with revision marks.
---

[English](#docx-tracked-edits) | [中文](#docx-tracked-edits-1)

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

#### Combined Example

```markdown
# Text Edits

Para 15: 修正术语
将 "novel" 改为 "improved"

Para 23: 删除冗余
删除: "as previously reported"

Para 32: 补充说明
在开头插入: Note: 
在末尾插入: (validated)

Para 45: 修正拼写
将 "differents" 改为 "different"
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

---

[English](#docx-tracked-edits) | [中文](#docx-tracked-edits-1)

# Docx Tracked Edits

## 快速开始

1. **读取源 docx** 以了解段落结构：
   ```bash
   python scripts/list_paragraphs.py paper.docx
   ```

2. **生成 changes.md** 使用以下模板

3. **转换为 JSON**：
   ```bash
   python scripts/md_to_json.py changes.md changes.json
   ```

4. **应用到 docx**（使用 docx_revision）：
   ```python
   import json
   from scripts.docx_revision import ComprehensiveDocxReviewer
   
   with open('changes.json') as f:
       config = json.load(f)
   
   reviewer = ComprehensiveDocxReviewer(config['source'])
   reviewer.apply_json_config(config)
   reviewer.save(config['output'])
   ```

## 核心设计原则

### 1. 极简原则

**生成 JSON 时，不要替换整句或整段。只替换关键词、词组或标点，并尽可能提供准确的位置。**

#### 为什么？

- **更清晰的修订历史**：用户可以看到确切的更改，而不是整段标记为删除/添加
- **更精确的审查**：审阅者可以逐词/逐词组检查更改
- **更少的冲突**：更小的更改在协作编辑中更容易合并

#### 示例

| 场景 | 错误 ❌ | 正确 ✅ |
|------|---------|----------|
| 修正术语 | `将 "novel approach for flood monitoring method" 改为 "improved method for flood detection"` | `将 "novel" 改为 "improved"` + `将 "monitoring" 改为 "detection"` |
| 删除冗余 | `删除: "as previously reported in our earlier studies"` | `删除: "as previously reported"` + `删除: "in our earlier studies"` |
| 修正拼写 | `将 "significantly differents results" 改为 "significantly different results"` | `将 "differents" 改为 "different"` |
| 添加内容 | `在开头插入: This is an important finding that needs to be highlighted.` | `在开头插入: Important: ` |

#### 位置要求

当文本在段落中多次出现时，你**必须**添加位置信息：

```markdown
# 错误 ❌（有歧义）
删除: "the"

# 正确 ✅（带位置）
删除: "the" (第15-18字符)
```

### 2. 工具多样化原则

**不要只使用替换。根据实际需要适当使用删除和插入工具。**

#### 三种工具及其使用场景

| 工具 | 使用场景 | 示例 |
|------|----------|---------|
| **replace** | 修改现有文本 | `将 "old" 改为 "new"` |
| **delete** | 删除冗余/不正确内容 | `删除: "unnecessary text"` |
| **insert** | 添加缺失内容 | `在开头插入: Note: ` |

#### 何时使用 delete + insert 而不是 replace？

| 场景 | 错误 ❌ | 正确 ✅ |
|------|---------|----------|
| 删除整段 | `将 "这是一段很长的内容..." 改为 ""` | `删除: "这是一段很长的内容..."` |
| 在指定位置插入 | `将 "原文" 改为 "新内容 原文"` | `在开头插入: 新内容` |
| 删除并重组 | `将 "A, B, C" 改为 "A, C"` | `删除: ", B"` |
| 添加前缀/后缀 | `将 "result" 改为 "Updated: result"` | `在开头插入: Updated: ` |

#### 组合示例

```markdown
# Text Edits

Para 15: 修正术语
将 "novel" 改为 "improved"

Para 23: 删除冗余
删除: "as previously reported"

Para 32: 补充说明
在开头插入: Note: 
在末尾插入: (validated)

Para 45: 修正拼写
将 "differents" 改为 "different"
```

**这将生成包含以下内容的 JSON：**
- 1 个 replace（novel → improved）
- 1 个 delete（as previously reported）
- 2 个 insert（Note: 和 (validated)）
- 1 个 replace（differents → different）

**不是**对整个段落的一个大替换。

## Changes Markdown 模板

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

## 语法参考

### Header (YAML frontmatter)
| 字段 | 必需 | 描述 |
|-------|----------|-------------|
| author | 是 | 所有更改的默认作者 |
| source | 是 | 源 docx 文件路径 |
| output | 是 | 输出 docx 文件路径 |
| track_revisions | 否 | 启用修订跟踪（默认：true） |

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

支持的格式：
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

## 歧义检测

如果文本在段落中多次出现，脚本将显示包含所有位置的错误，并要求你添加位置信息。

## 工作流程

1. 读取源 docx（使用 list_paragraphs.py 或直接读取）
2. 生成 changes.md
3. 运行 `md_to_json.py changes.md changes.json`
4. 如果出现歧义错误，与用户解决并重新生成 MD
5. 应用到 docx

## 脚本

- `scripts/list_paragraphs.py` - 列出 docx 段落结构
- `scripts/md_to_json.py` - 将 Markdown 转换为 docx_revision JSON
- `scripts/docx_revision/` - 内置的 docx_revision 包
