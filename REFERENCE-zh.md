# Docx Tracked Edits 参考文档

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

## Markdown 模板语法

### Header

YAML frontmatter 块定义编辑会话的元数据。

```yaml
---
author: Name
source: path.docx
output: path_revised.docx
track_revisions: true
---
```

| 字段 | 必需 | 描述 |
|-------|----------|-------------|
| `author` | 是 | 修订跟踪中显示的作者姓名 |
| `source` | 是 | 源 .docx 文件的路径 |
| `output` | 是 | 修订输出 .docx 文件的路径 |
| `track_revisions` | 否 | 启用修订跟踪（默认：true） |

### Section Headers

所有编辑都在 section headers 下组织：

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

- `Para {N}` — 段落编号（0-indexed）
- `选中范围` — 可选的字符范围，用于批注锚定
- `缩写` — 可选的作者缩写

### Text Edits

```markdown
Para {N}: {title}
{edit instruction}
```

| Instruction | Description |
|-------------|-------------|
| `将 "{old}" 改为 "{new}"` | 替换文本 |
| `在开头插入: {text}` | 在段落开头插入 |
| `在末尾插入: {text}` | 在段落末尾插入 |
| `删除: "{text}"` | 删除文本（无歧义） |
| `删除: "{text}" (第{start}-{end}字符)` | 带位置的删除 |

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
| `第{N}行下方加一行` | 在第 N 行下方插入一行 |
| `删掉第{N}行` | 删除第 N 行 |
| `合并第{N}行的第{X}-{Y}列` | 合并第 N 行的第 X 到 Y 列 |
| `合并第{N}行的{X}个格子` | 合并第 N 行的 X 个单元格 |

表格索引从 1 开始。

### Style Edits

```markdown
{StyleName} 样式:
  {format1}, {format2}, ...
```

将格式更改应用于使用命名样式的所有段落。

### Global Changes

```markdown
将 "{old}" 改为 "{new}"
```

在所有段落中全局替换文本。不需要 `Para {N}:` 前缀。

## 歧义检测

如果文本在段落中多次出现，需要位置信息：

```markdown
删除: "text" (第15-18字符)
将 "text" 改为 "text" (第20-25字符)
```

### Error Format

当检测到歧义时，解析器显示所有出现位置：

```
歧义错误: "the" 在段落中出现 3 次:
  第15-18字符
  第42-45字符
  第78-81字符
请添加位置信息: (第N-M字符)
```

### Resolution

在括号中添加位置说明符以消除歧义：

```markdown
# 有歧义（错误）
删除: "the"

# 已解决（有效）
删除: "the" (第42-45字符)
```

位置范围两端都包含，且从 0 开始。

## 错误处理

| Error | Cause | Fix |
|-------|-------|-----|
| `歧义错误` | 文本多次出现 | 添加 `(第N-M字符)` 位置 |
| `找不到段落` | 无效的段落编号 | 使用 `list_paragraphs.py` 检查段落编号 |
| `格式解析失败` | 无效的格式关键词 | 使用 Format Edits 表中的关键词 |
| `表格索引越界` | 表格/行索引超出范围 | 使用 `list_paragraphs.py` 验证表格结构 |
| `缺少必要字段` | 缺少 header 字段 | 添加必需字段：author, source, output |

## 脚本

| Script | Purpose |
|--------|---------|
| `scripts/list_paragraphs.py` | 列出带编号的 docx 段落结构 |
| `scripts/md_to_json.py` | 将 Markdown 模板转换为 JSON 以供应用 |

## 快速查找

| Task | Syntax |
|------|--------|
| 替换文本 | `将 "old" 改为 "new"` |
| 在开头插入 | `在开头插入: text` |
| 在末尾插入 | `在末尾插入: text` |
| 删除文本 | `删除: "text"` |
| 加粗段落 | `Para N: 标题` 然后 `加粗` |
| 居中对齐 | `居中对齐` |
| 设置行距 | `行距1.5倍` |
| 设置字号 | `字号10pt` |
| 添加表格行 | `表格0:` 然后 `第N行下方加一行` |
| 删除表格行 | `表格0:` 然后 `删掉第N行` |
| 合并单元格 | `合并第N行的第X-Y列` |
| 更改样式 | `Normal 样式:` 然后格式列表 |
| 全局替换 | `将 "old" 改为 "new"`（无 Para 前缀） |
| 添加批注 | `Para N: 标题` 然后批注文本 |