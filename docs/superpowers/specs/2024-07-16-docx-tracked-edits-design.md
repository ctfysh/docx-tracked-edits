# Docx Tracked Edits Skill 设计文档

**日期**: 2024-07-16
**状态**: 待批准

## 概述

创建一个 OpenCode skill，用于通过 AI 生成的 Markdown 文件来编辑 docx 文档，支持修订模式和批注。核心流程：AI 生成 MD → 转换为 JSON → 应用到 docx。

## 目标用户

- 学术论文审阅（主要场景）
- 文档批量修订
- 协作编辑工作流
- 通用文档编辑

## 目录结构

```
docx-tracked-edits/
├── SKILL.md              # 主指令文件
├── REFERENCE.md          # 详细语法文档
├── EXAMPLES.md           # 使用示例
└── scripts/
    ├── list_paragraphs.py # 列出 docx 段落结构
    ├── md_to_json.py      # MD → JSON 转换
    └── docx_revision/     # 完整包副本
        ├── __init__.py
        ├── reviewer.py
        └── ...
```

## MD 模板语法

### Header (YAML frontmatter)

```markdown
---
author: Tiger
source: paper.docx
output: paper_revised.docx
track_revisions: true
lock_revisions: false
revision_password: null
---
```

### Comments

```markdown
# Comments

Para 24: 方法论建议
此处列出的三项"进展"表述清晰但部分重叠...
> 选中范围: 第10-50字符
> 缩写: T
```

### Text Edits

```markdown
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
```

### Format Edits

```markdown
# Format Edits

Para 12: 段落格式
居中对齐, 行距1.5倍, 段前12pt

Para 45-48: 缩进
左缩进36pt
```

### Table Edits

```markdown
# Table Edits

表格0:
  第2行下方加一行
  删掉第5行
  合并第二行的三个格子
```

### Style Edits

```markdown
# Style Edits

Normal 样式:
  段前6pt, 段后6pt

Heading1 样式:
  字号16pt, 加粗
```

### Global Changes

```markdown
# Global Changes

将全文 "significant difference" 改为 "statistically significant difference"
```

## 歧义处理

转换脚本检测逻辑：
1. 检查 `old_text` 在段落中出现次数
2. 出现 1 次 → 直接替换
3. 出现多次 → 报错，显示所有位置，提示用户添加位置信息

报错示例：
```
⚠️ 歧义检测: "the" 在第24段出现3次
  位置1: 第15-18字符
  位置2: 第42-45字符  
  位置3: 第67-70字符

请在 MD 中添加位置信息:
  删除: "the" (第15-18字符)
```

## 工作流

1. 读取 docx（使用 list_paragraphs.py 或直接读取）
2. 生成 changes.md
3. 运行 `md_to_json.py changes.md changes.json`
4. 如有歧义错误，与用户对话解决后重新生成 MD
5. 应用到 docx

### 批量模式

```bash
for f in changes_*.md; do
  python scripts/md_to_json.py "$f" "${f%.md}.json"
  # 应用 JSON 到 docx
done
```

## 脚本设计

### list_paragraphs.py

```python
#!/usr/bin/env python3
"""列出 docx 文件的段落结构"""
import sys
from docx import Document

def main():
    doc = Document(sys.argv[1])
    for i, para in enumerate(doc.paragraphs):
        text = para.text[:80].replace('\n', ' ')
        print(f"{i}: {text}")

if __name__ == '__main__':
    main()
```

### md_to_json.py

核心逻辑：
1. 解析 YAML frontmatter
2. 解析各 section（Comments, Text Edits, Format Edits, etc.）
3. 对于 Text Edits：
   - 读取源 docx 获取段落内容
   - 检查 old_text 出现次数
   - 有歧义时报错并显示位置
   - 无歧义时生成 JSON
4. 输出完整 JSON 配置

## 与 docx_revision 集成

```python
import json
from docx_revision import ComprehensiveDocxReviewer

with open('changes.json') as f:
    config = json.load(f)

reviewer = ComprehensiveDocxReviewer(config['source'])
reviewer.apply_json_config(config)
reviewer.save(config['output'])
```

## 测试用例

1. 基础替换：`REPLACE: "A" → "B"`
2. 多次出现：同段落中 "the" 出现多次，需位置信息
3. 批注带范围：`> 选中范围: 第10-50字符`
4. 格式修改：居中、行距、缩进
5. 表格操作：插入行、删除行、合并单元格
6. 全局替换：跨段落的文本替换

## 待确认

- [ ] 是否需要支持密码保护的 docx？
- [ ] 是否需要支持撤销操作？
- [ ] 是否需要生成修改摘要报告？
