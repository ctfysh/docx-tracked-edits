# Docx Tracked Edits Examples

## Example 1: Academic Paper Editing

```markdown
---
author: Tiger
source: paper.docx
output: paper_revised.docx
---

# Comments

Para 24: 方法论建议
此处列出的三项"进展"表述清晰但部分重叠，建议合并或调整为并列结构
> 选中范围: 第10-50字符
> 缩写: T

Para 31: 数据分析
统计方法描述不够完整，需补充样本量和显著性水平
> 缩写: T

# Text Edits

Para 8: 标题修正
将 "novel approach" 改为 "improved method"

Para 15: 术语修正
将 "effect" 改为 "impact" (第22-28字符)

Para 23: 补充内容
在开头插入: Updated: 
在末尾插入: (validated)

Para 67: 删除冗余
删除: "as previously reported"

Para 42: 修正引用
将 "Ref. [5]" 改为 "Refs. [5, 6]"

# Format Edits

Para 12: 段落格式
居中对齐, 行距1.5倍, 段前12pt

Para 8: 标题格式
字号14pt, 加粗

# Style Edits

Normal 样式:
  段前6pt, 段后6pt, 行距1.15倍
```

## Example 2: Business Report

```markdown
---
author: Manager
source: report.docx
output: report_revised.docx
---

# Text Edits

Para 15: 更新数据
将 "2023年" 改为 "2024年"

Para 22: 修正季度
将 "Q3" 改为 "Q4" (第8-10字符)

Para 32: 修正金额
删除: "$1.2M" (第10-15字符)
在末尾插入: $1.5M

Para 45: 更新增长率
将 "8.5%" 改为 "9.2%"

# Table Edits

表格0: 销售数据表
第2行下方加一行
删掉第5行

表格1: 区域对比
合并第一行的A-C列

# Format Edits

Para 3: 报告标题
居中对齐, 字号18pt, 加粗

Para 5-10: 正文
两端对齐, 行距1.5倍

# Global Changes

将 "significantly" 改为 "significantly (p < 0.05)"
```

## Example 3: Legal Document

```markdown
---
author: Lawyer
source: contract.docx
output: contract_revised.docx
---

# Comments

Para 45: 条款风险
此条款可能违反《合同法》第52条，建议删除或修改
> 缩写: L

Para 67: 管辖权建议
建议将管辖法院改为北京仲裁委员会
> 缩写: L

# Text Edits

Para 12: 修正日期
将 "2023年12月31日" 改为 "2024年6月30日"

Para 28: 删除过时条款
删除: "如发生争议，双方应友好协商" (第1-20字符)

Para 33: 补充定义
在开头插入: "不可抗力"是指
在末尾插入: 等不可预见的客观情况

Para 55: 修正金额
将 "伍万元整" 改为 "拾万元整"

# Format Edits

Para 1: 封面格式
居中对齐, 字号16pt, 加粗

Para 3: 条款标题
字号12pt, 加粗
```

## Example 4: Multi-Section Complex

```markdown
---
author: Team
source: proposal.docx
output: proposal_revised.docx
---

# Comments

Para 5: 预算问题
预算数字与上一版本不一致，需核实
> 缩写: T

Para 20: 技术可行性
技术方案描述过于笼统，需补充细节
> 缩写: W

Para 38: 时间表
里程碑日期需与合同截止日期对齐
> 缩写: T

# Text Edits

Para 3: 标题
将 "项目计划" 改为 "项目提案"

Para 10: 补充背景
在开头插入: 本项目基于2023年研究成果。
在末尾插入: 具体实施方案详见附件。

Para 35: 删除冗余
删除: "众所周知"

Para 42: 修正公司名
将 "Tiger公司" 改为 "Tiger科技有限公司" (第5-11字符)

Para 58: 更新联系方式
将 "010-12345678" 改为 "010-87654321"

# Format Edits

Para 3: 标题格式
居中对齐, 字号18pt, 加粗

Para 15-20: 正文格式
两端对齐, 行距1.5倍, 左缩进24pt

Para 5: 摘要格式
字号11pt, 斜体

# Table Edits

表格0: 预算明细
第3行下方加一行
删掉第8行

表格1: 人员分工
合并第一行的A-C列
合并第3行的2个格子

表格2: 时间进度
第10行下方加一行

# Style Edits

Heading1 样式:
  字号16pt, 加粗

Heading2 样式:
  字号14pt

Normal 样式:
  段前6pt, 段后3pt, 行距1.3倍

# Global Changes

将 "Tiger公司" 改为 "Tiger科技有限公司"
将 "项目组" 改为 "项目团队"
```

## Example 5: Minimal Single Edit (简单示例)

> **Note:** This is a simplified example for quick reference. See Examples 1-4 in the `examples/` directory for complete end-to-end demonstrations with Python code.

```markdown
---
author: Editor
source: letter.docx
output: letter_revised.docx
---

# Text Edits

Para 0: 修正称呼
将 "Dear Sir" 改为 "Dear Colleague"
```

## Example 6: Formatting-Only Document (格式修改示例)

> **Note:** This is a simplified example for quick reference. See Examples 1-4 in the `examples/` directory for complete end-to-end demonstrations with Python code.

```markdown
---
author: Designer
source: brochure.docx
output: brochure_revised.docx
---

# Format Edits

Para 0: 封面标题
居中对齐, 字号28pt, 加粗, 字体SimHei

Para 1: 副标题
居中对齐, 字号16pt, 字体SimSun

Para 3-8: 正文
两端对齐, 行距1.8倍, 左缩进36pt, 右缩进36pt

Para 10: 脚注
字号9pt, 斜体

# Style Edits

Heading1 样式:
  字号20pt, 加粗, 字体SimHei

Heading2 样式:
  字号14pt, 字体SimHei

Normal 样式:
  字体SimSun, 字号10.5pt, 行距1.5倍
```

## Example 7: Table-Heavy Document (表格编辑示例)

> **Note:** This is a simplified example for quick reference. See Examples 1-4 in the `examples/` directory for complete end-to-end demonstrations with Python code.

```markdown
---
author: Analyst
source: data_report.docx
output: data_report_revised.docx
---

# Text Edits

Para 5: 修正摘要
将 "总收入" 改为 "净收入"

Para 12: 更新时间范围
将 "2023年1月至6月" 改为 "2024年1月至6月"

# Table Edits

表格0: 季度数据
第4行下方加一行
删掉第2行

表格1: 区域对比
合并第一行的A-C列
合并第2行的3个格子

表格2: 产品明细
第6行下方加一行
删掉第8行
合并第1行的第2-4列

# Format Edits

Para 3: 表格标题
居中对齐, 字号11pt, 加粗

# Style Edits

Normal 样式:
  字体Arial, 字号10pt
```

## Example 8: Minimalism Principle in Action (极简原则示例)

This example demonstrates how to apply the **Minimalism Principle** — only replace key words/phrases, not entire sentences.

### Scenario: Academic Paper Editing with Minimal Changes

**Original paragraph (Para 15):**
> The novel approach for flood monitoring method demonstrates significant improvements in accuracy compared to traditional techniques.

**Wrong approach ❌ (replacing entire sentence):**
```markdown
Para 15: 修正术语
将 "The novel approach for flood monitoring method demonstrates significant improvements in accuracy compared to traditional techniques." 改为 "The improved method for flood detection shows enhanced accuracy compared to traditional approaches."
```

**Right approach ✅ (minimal changes):**
```markdown
Para 15: 修正术语
将 "novel" 改为 "improved"
将 "monitoring" 改为 "detection"
将 "demonstrates" 改为 "shows"
将 "significant improvements" 改为 "enhanced accuracy"
将 "techniques" 改为 "approaches"
```

### What This Generates

```json
{
  "text_modifications": [
    {"type": "replace", "paragraph_index": 15, "old_text": "novel", "new_text": "improved"},
    {"type": "replace", "paragraph_index": 15, "old_text": "monitoring", "new_text": "detection"},
    {"type": "replace", "paragraph_index": 15, "old_text": "demonstrates", "new_text": "shows"},
    {"type": "replace", "paragraph_index": 15, "old_text": "significant improvements", "new_text": "enhanced accuracy"},
    {"type": "replace", "paragraph_index": 15, "old_text": "techniques", "new_text": "approaches"}
  ]
}
```

### Why This Is Better

| Aspect | Wrong ❌ | Right ✅ |
|--------|---------|----------|
| Revision history | Entire paragraph marked as deleted/added | Individual words highlighted |
| Review experience | Hard to see what changed | Easy to verify each change |
| Conflict potential | High (whole paragraph) | Low (individual words) |
| Audit trail | Opaque | Transparent |

## Example 9: Tool Diversity in Action (工具多样化示例)

This example demonstrates how to use **delete** and **insert** instead of just replace.

### Scenario: Removing Redundant Text and Adding Notes

**Original paragraph (Para 23):**
> As previously reported in our earlier studies, the results show significant correlation.

**Wrong approach ❌ (using only replace):**
```markdown
Para 23: 修改
将 "As previously reported in our earlier studies, " 改为 ""
将 "show significant" 改为 "demonstrate statistically significant"
```

**Right approach ✅ (using delete + insert + replace):**
```markdown
Para 23: 修改
删除: "As previously reported in our earlier studies, "
将 "show significant" 改为 "demonstrate statistically significant"
在末尾插入: (p < 0.05)
```

### What This Generates

```json
{
  "text_modifications": [
    {"type": "delete", "paragraph_index": 23, "text": "As previously reported in our earlier studies, "},
    {"type": "replace", "paragraph_index": 23, "old_text": "show significant", "new_text": "demonstrate statistically significant"},
    {"type": "insert", "paragraph_index": 23, "text": "(p < 0.05)", "position": null}
  ]
}
```

### Why This Is Better

| Aspect | Wrong ❌ | Right ✅ |
|--------|---------|----------|
| Clarity | Replacing empty string is confusing | Delete is explicit |
| Readability | Hard to understand intent | Clear intent: delete, replace, insert |
| Maintenance | Ambiguous operations | Unambiguous operations |
| Tool usage | Only replace | Proper use of delete, replace, insert |

## Example 10: Position-Aware Editing (位置感知编辑)

This example demonstrates when and how to use position information.

### Scenario: Text Appears Multiple Times

**Original paragraph (Para 8):**
> The the results show that the the effect is significant.

**Wrong approach ❌ (ambiguous):**
```markdown
Para 8: 修正重复
删除: "the"
```

**Right approach ✅ (with position):**
```markdown
Para 8: 修正重复
删除: "the" (第4-7字符)
删除: "the" (第18-21字符)
```

### What This Generates

```json
{
  "text_modifications": [
    {"type": "delete", "paragraph_index": 8, "text": "the", "start_pos": 4, "end_pos": 7},
    {"type": "delete", "paragraph_index": 8, "text": "the", "start_pos": 18, "end_pos": 21}
  ]
}
```

### Position Rules

1. **When to use position**: When the same text appears multiple times in a paragraph
2. **Format**: `(第{start}-{end}字符)` — 0-indexed, inclusive on both ends
3. **How to find position**: Count characters from the beginning of the paragraph

## Quick Start

### Running Complete Examples (推荐)

The `examples/` directory contains complete end-to-end demonstrations:

```bash
# Run all examples
bash examples/run_all_examples.sh

# Or run individual examples
cd examples/example_1_academic
python create_original.py      # Generate original docx
python apply_changes.py        # Apply changes
```

Each example includes:
- `create_original.py` - Generate original docx
- `changes.md` - Changes specification
- `apply_changes.py` - Apply changes pipeline
- `README.md` - Description

### Quick Reference (快速参考)

For quick syntax reference, see the simplified examples above (Examples 5-10).

1. Read source docx to understand structure
2. Copy the most relevant example above
3. Modify content to match your edits
4. Run `python scripts/md_to_json.py changes.md changes.json`
5. Apply changes to docx with the processing pipeline

### Full Workflow

```bash
# 1. List paragraphs in source docx
python scripts/list_paragraphs.py paper.docx

# 2. Create changes.md based on the template

# 3. Convert to JSON
python scripts/md_to_json.py changes.md changes.json

# 4. Apply to docx
python -c "
import json
from scripts.docx_revision import ComprehensiveDocxReviewer

with open('changes.json') as f:
    config = json.load(f)

reviewer = ComprehensiveDocxReviewer(config['source'])
reviewer.apply_json_config(config)
reviewer.save(config['output'])
print(f'✅ Generated: {config[\"output\"]}')
"
```
