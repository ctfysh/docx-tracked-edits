---
name: docx-tracked-edits
description: 使用 AI 编辑带有修订和批注的 docx 文件。生成可转换为 docx_revision JSON 格式的 Markdown 修改规范。当用户想要修订 Word 文档、添加批注或使用修订标记修改内容时使用。
---

# Docx Tracked Edits

## 核心功能

**本 skill 只做两件事：**

1. **套模板**：按标准格式解析修改指令
2. **执行修订**：将修改应用到 Word 文档

## 快速开始

1. **审查阶段**：其他 AI 读文档，找问题
2. **模板阶段**：其他 AI 按本 skill 定义的模板格式输出问题列表
3. **执行阶段**：本 skill 解析模板，应用修改
4. **结果阶段**：用户获得修订文档

**关键：本 skill 定义了修改指令的标准模板格式。其他 AI 工具必须按此格式输出，本 skill 才能解析执行。**

## 核心原则

### 极简原则
只替换关键词/词组，不要替换整句。文本多次出现时提供位置信息。

| 错误 ❌ | 正确 ✅ |
|---------|----------|
| `将 "novel approach for flood monitoring method" 改为 "improved method"` | `将 "novel" 改为 "improved"` + `将 "monitoring" 改为 "detection"` |
| `删除: "as previously reported in our earlier studies"` | `删除: "as previously reported"` + `删除: "in our earlier studies"` |

### 工具多样化原则
适当使用删除/插入，不要只用替换。

| 错误 ❌ | 正确 ✅ |
|---------|----------|
| `将 "很长的内容..." 改为 ""` | `删除: "很长的内容..."` |
| `将 "原文" 改为 "新内容 原文"` | `在开头插入: 新内容` |

## 模板格式

```yaml
---
author: Tiger
source: paper.docx
output: paper_revised.docx
---
```

## 快速语法

| 类型 | 语法 |
|------|------|
| 替换 | `将 "old" 改为 "new"` |
| 开头插入 | `在开头插入: text` |
| 末尾插入 | `在末尾插入: text` |
| 删除 | `删除: "text"` 或 `删除: "text" (第15-18字符)` |
| 格式 | `居中对齐, 加粗, 行距1.5倍` |
| 表格 | `第N行下方加一行`, `删掉第N行`, `合并第N行的第X-Y列` |
| 样式 | `Normal 样式: 字号10pt, 加粗` |
| 全局 | `将 "old" 改为 "new"`（无 Para 前缀） |

## 模板格式

```yaml
---
author: Tiger
source: paper.docx
output: paper_revised.docx
---
```

完整语法见 [../references/REFERENCE-core-zh.md](../references/REFERENCE-core-zh.md)。完整示例和错误处理见 [../references/REFERENCE-zh.md](../references/REFERENCE-zh.md)。

## 失败模式与恢复

| 症状 | 触发条件 | 恢复方法 |
|------|---------|---------|
| 歧义检测错误 | 文本在段落中出现多次 | 添加 `(第N-M字符)` 位置信息指定精确匹配 |
| 段落未找到 | 段落索引无效 | 运行 `list_paragraphs.py` 获取有效段落索引 |
| 文本未找到 | 目标文本不存在于段落中 | 检查拼写，运行 `list_paragraphs.py` 验证内容 |
| 格式解析错误 | 格式关键字无效 | 只能使用：`居中对齐`、`加粗`、`两端对齐`、`行距N倍`、`字号Npt` |
| 表格索引越界 | 表格编号超过文档表格数 | 检查文档结构，确认表格存在 |
| JSON 解析错误 | changes.md 格式无效 | 确保 YAML frontmatter 包含 `author`、`source`、`output` 字段 |

## 不要做什么

| ❌ 不要 | ✅ 应该 |
|---------|--------|
| 替换整个句子 | 只替换特定的词/词组 |
| 使用 `将 "很长的文本..." 改为 ""` | 使用 `删除: "很长的文本..."` |
| 不生成 changes.md 直接修改文档 | 先生成 changes.md，再应用 |
| 文本多次出现时跳过歧义检查 | 添加 `(第N-M字符)` 位置信息 |
| 不经用户确认直接应用修改 | 展示 changes.md 给用户，等待确认 |
| 全局替换使用 `Para N:` 前缀 | 全局替换省略 `Para N:` 前缀 |

## 工作流程

1. 读取源 docx（list_paragraphs.py）
2. 生成 changes.md
3. 转换为 JSON（md_to_json.py）
4. 如有歧义错误，添加位置信息并重新生成
5. 应用到 docx

## 脚本

- `scripts/list_paragraphs.py` - 列出段落结构
- `scripts/md_to_json.py` - 将 Markdown 转换为 JSON
- `scripts/docx_revision/` - 内置包
