---
name: docx-tracked-edits
description: 使用 AI 编辑带有修订和批注的 docx 文件。生成可转换为 docx_revision JSON 格式的 Markdown 修改规范。当用户想要修订 Word 文档、添加批注或使用修订标记修改内容时使用。
---

# Docx Tracked Edits

## 快速开始

1. **列出段落**: `python scripts/list_paragraphs.py paper.docx`
2. **编写 changes.md**（见下方模板）
3. **转换**: `python scripts/md_to_json.py changes.md changes.json`
4. **应用**:
```python
import json
from scripts.docx_revision import ComprehensiveDocxReviewer
with open('changes.json') as f: config = json.load(f)
reviewer = ComprehensiveDocxReviewer(config['source'])
reviewer.apply_json_config(config)
reviewer.save(config['output'])
```

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

## 模板

```markdown
---
author: Tiger
source: paper.docx
output: paper_revised.docx
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

---

# Format Edits

Para 12: 段落格式
居中对齐, 行距1.5倍, 段前12pt

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

完整语法参考见 [REFERENCE.md](REFERENCE.md)。

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