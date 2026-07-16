[English](#docx-tracked-edits) | [中文](#docx-tracked-edits-1)

---

# Docx Tracked Edits

AI-driven docx editing with tracked changes. Edit Word documents using readable Markdown templates.

## Features

- **Markdown-based editing**: Write changes in human-readable Markdown
- **Tracked changes**: All edits shown as Word tracked changes
- **Comments support**: Add comments with selected text ranges
- **Format editing**: Change alignment, spacing, indentation, bold/italic
- **Table editing**: Insert/delete rows, merge cells
- **Style editing**: Modify paragraph styles
- **Ambiguity detection**: Error with positions when text appears multiple times
- **Chinese support**: Natural language syntax (居中对齐, 行距1.5倍, etc.)
- **Minimalism principle**: Only replace key words/phrases, not entire sentences
- **Tool diversity**: Use delete/insert tools appropriately, not just replace

## Quick Start

1. **List paragraphs** in source docx:
   ```bash
   python scripts/list_paragraphs.py paper.docx
   ```

2. **Write changes** in Markdown (see [REFERENCE.md](REFERENCE.md) for syntax)

3. **Convert to JSON**:
   ```bash
   python scripts/md_to_json.py changes.md changes.json
   ```

4. **Apply to docx**:
   ```python
   import json
   from scripts.docx_revision import ComprehensiveDocxReviewer
   
   with open('changes.json') as f:
       config = json.load(f)
   
   reviewer = ComprehensiveDocxReviewer(config['source'])
   reviewer.apply_json_config(config)
   reviewer.save(config['output'])
   ```

## Examples

### Academic Paper Editing

**Scenario**: Fix terminology, remove redundancy, correct typos, add comments, and adjust formatting.

```markdown
---
author: Tiger
source: paper.docx
output: paper_revised.docx
---

# Comments

Para 8: 术语建议
> 选中范围: 第4-9字符
> 缩写: T
此处 "novel" 在学术论文中过于泛滥，建议改为更具体的描述词。

# Text Edits

Para 8: 术语修正
将 "novel" 改为 "improved"
将 "monitoring" 改为 "detection"
将 "demonstrates" 改为 "shows"

Para 12: 删除冗余
删除: "As previously reported in our earlier studies, " (第0-47字符)

Para 15: 修复重复词
将 "The the" 改为 "The"

# Format Edits

Para 8: 标题强调
居中对齐, 加粗
```

**Full example**: [examples/example_1_academic/](examples/example_1_academic/)

### Business Report

**Scenario**: Update dates, amounts, modify tables, and adjust formatting.

```markdown
---
author: Tiger
source: report.docx
output: report_revised.docx
---

# Text Edits

Para 11: 更新年份
将 "2023年" 改为 "2024年"

Para 11: 更新金额
将 "$1.2M" 改为 "$1.5M"

# Table Edits

表格1: 表格结构调整
第2行下方加一行
删掉第5行

# Format Edits

Para 0: 标题格式
居中对齐, 加粗
```

**Full example**: [examples/example_2_business/](examples/example_2_business/)

### Legal Document

**Scenario**: Update contract dates, amounts, add definitions, and flag risks.

```markdown
---
author: Tiger
source: contract.docx
output: contract_revised.docx
---

# Comments

Para 15: 争议解决风险提示
> 选中范围: 第0-20字符
> 缩写: L
此条款仅约定向甲方所在地法院起诉，对乙方不利。建议增加仲裁条款或约定双方均可在各自所在地起诉。

# Text Edits

Para 8: 更新合同期限
将 "2023年12月31日" 改为 "2024年12月31日"

Para 12: 更新付款金额
将 "伍万元整" 改为 "捌万元整"
将 "¥50,000.00" 改为 "¥80,000.00"

Para 18: 删除过时条款
删除: "第四条 不可抗力"

Para 3: 插入定义条款
在开头插入: "定义：本合同中，"技术服务"指乙方为甲方提供的软件开发、技术咨询及相关服务。"

# Format Edits

Para 0: 标题格式
居中对齐, 加粗
```

**Full example**: [examples/example_3_legal/](examples/example_3_legal/)

### Complex Multi-Section Document

**Scenario**: All edit types - text, table, format, style, global changes, and comments.

```markdown
---
author: Tiger
source: proposal.docx
output: proposal_revised.docx
---

# Comments

Para 3: 项目概述评注
> 选中范围: 第0-12字符
> 缩写: T
项目概述需要补充项目预算总额和预期产出指标，以便评审委员会快速了解项目规模。

Para 15: 时间计划建议
> 缩写: T
建议在开发实施阶段增加一个中期检查点（第12月），便于及时调整技术方案。

Para 20: 团队组建建议
> 缩写: T
建议增加至少1名安全工程师，确保系统符合数据安全合规要求。

# Text Edits

Para 20: 公司名称修正
将 "Tiger公司" 改为 "Tiger科技有限公司"

Para 15: 时间调整
将 "第1-3月" 改为 "第1-4月"

Para 25: 年份修正
将 "Chen et al., 2022" 改为 "Chen et al., 2023"

# Table Edits

表格1: 预算表调整
第3行下方加一行
合并第四行的三个格子

# Format Edits

Para 0: 标题格式
居中对齐, 加粗

Para 3: 项目概述格式
两端对齐, 行距1.5倍

Para 12: 表格标题格式
字号12pt, 加粗

# Style Edits

Heading1 样式:
字号16pt, 加粗

Normal 样式:
行距1.2倍, 段前6pt

# Global Changes

将 "项目组" 改为 "项目团队"
```

**Full example**: [examples/example_4_complex/](examples/example_4_complex/)

## Running All Examples

```bash
# Run all 4 examples
bash examples/run_all_examples.sh

# Or run individual examples
cd examples/example_1_academic
python create_original.py      # Generate original docx
python apply_changes.py        # Apply changes
```

## Core Design Principles

### 1. Minimalism Principle (极简原则)

**When generating JSON, do NOT replace whole sentences or paragraphs. Only replace key letters, words (phrases), or punctuation, and provide accurate positions whenever possible.**

| Scenario | Wrong ❌ | Right ✅ |
|----------|---------|----------|
| Fix terminology | `将 "novel approach for flood monitoring method" 改为 "improved method for flood detection"` | `将 "novel" 改为 "improved"` + `将 "monitoring" 改为 "detection"` |
| Delete redundancy | `删除: "as previously reported in our earlier studies"` | `删除: "as previously reported"` + `删除: "in our earlier studies"` |
| Fix spelling | `将 "significantly differents results" 改为 "significantly different results"` | `将 "differents" 改为 "different"` |

### 2. Tool Diversity Principle (工具多样化原则)

**Do NOT only use replace. Use delete and insert tools as appropriate based on actual needs.**

| Scenario | Wrong ❌ | Right ✅ |
|----------|---------|----------|
| Delete entire paragraph | `将 "这是一段很长的内容..." 改为 ""` | `删除: "这是一段很长的内容..."` |
| Insert at specific position | `将 "原文" 改为 "新内容 原文"` | `在开头插入: 新内容` |
| Delete and reorganize | `将 "A, B, C" 改为 "A, C"` | `删除: ", B"` |

## Documentation

- [REFERENCE.md](REFERENCE.md) - Full syntax reference
- [EXAMPLES.md](EXAMPLES.md) - Additional examples and patterns
- [SKILL.md](SKILL.md) - OpenCode skill definition

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/list_paragraphs.py` | List docx paragraph structure |
| `scripts/md_to_json.py` | Convert Markdown to docx_revision JSON |
| `scripts/docx_revision/` | Bundled docx_revision package |

## Testing

```bash
python scripts/md_to_json.py --test
```

## License

MIT

---

[English](#docx-tracked-edits) | [中文](#docx-tracked-edits-1)

# Docx Tracked Edits

AI 驱动的 docx 修订模式编辑。使用可读的 Markdown 模板编辑 Word 文档。

## 功能特性

- **基于 Markdown 的编辑**：使用人类可读的 Markdown 编写修改
- **修订跟踪**：所有编辑显示为 Word 修订标记
- **批注支持**：添加带选中文本范围的批注
- **格式编辑**：更改对齐、间距、缩进、加粗/斜体
- **表格编辑**：插入/删除行、合并单元格
- **样式编辑**：修改段落样式
- **歧义检测**：当文本多次出现时显示带位置的错误
- **中文支持**：自然语言语法（居中对齐、行距1.5倍等）
- **极简原则**：只替换关键词/短语，不替换整句
- **工具多样化**：适当使用删除/插入工具，而非仅用替换

## 快速开始

1. **列出段落**：查看源 docx 的段落结构
   ```bash
   python scripts/list_paragraphs.py paper.docx
   ```

2. **编写修改**：用 Markdown 编写修改（语法见 [REFERENCE.md](REFERENCE.md)）

3. **转换为 JSON**：
   ```bash
   python scripts/md_to_json.py changes.md changes.json
   ```

4. **应用到 docx**：
   ```python
   import json
   from scripts.docx_revision import ComprehensiveDocxReviewer
   
   with open('changes.json') as f:
       config = json.load(f)
   
   reviewer = ComprehensiveDocxReviewer(config['source'])
   reviewer.apply_json_config(config)
   reviewer.save(config['output'])
   ```

## 示例

### 学术论文编辑

**场景**：修正术语、删除冗余、修复错别字、添加批注、调整格式。

```markdown
---
author: Tiger
source: paper.docx
output: paper_revised.docx
---

# Comments

Para 8: 术语建议
> 选中范围: 第4-9字符
> 缩写: T
此处 "novel" 在学术论文中过于泛滥，建议改为更具体的描述词。

# Text Edits

Para 8: 术语修正
将 "novel" 改为 "improved"
将 "monitoring" 改为 "detection"
将 "demonstrates" 改为 "shows"

Para 12: 删除冗余
删除: "As previously reported in our earlier studies, " (第0-47字符)

Para 15: 修复重复词
将 "The the" 改为 "The"

# Format Edits

Para 8: 标题强调
居中对齐, 加粗
```

**完整示例**：[examples/example_1_academic/](examples/example_1_academic/)

### 商业报告

**场景**：更新日期、金额、修改表格、调整格式。

```markdown
---
author: Tiger
source: report.docx
output: report_revised.docx
---

# Text Edits

Para 11: 更新年份
将 "2023年" 改为 "2024年"

Para 11: 更新金额
将 "$1.2M" 改为 "$1.5M"

# Table Edits

表格1: 表格结构调整
第2行下方加一行
删掉第5行

# Format Edits

Para 0: 标题格式
居中对齐, 加粗
```

**完整示例**：[examples/example_2_business/](examples/example_2_business/)

### 法律文档

**场景**：更新合同日期、金额、添加定义、标记风险。

```markdown
---
author: Tiger
source: contract.docx
output: contract_revised.docx
---

# Comments

Para 15: 争议解决风险提示
> 选中范围: 第0-20字符
> 缩写: L
此条款仅约定向甲方所在地法院起诉，对乙方不利。建议增加仲裁条款或约定双方均可在各自所在地起诉。

# Text Edits

Para 8: 更新合同期限
将 "2023年12月31日" 改为 "2024年12月31日"

Para 12: 更新付款金额
将 "伍万元整" 改为 "捌万元整"
将 "¥50,000.00" 改为 "¥80,000.00"

Para 18: 删除过时条款
删除: "第四条 不可抗力"

Para 3: 插入定义条款
在开头插入: "定义：本合同中，"技术服务"指乙方为甲方提供的软件开发、技术咨询及相关服务。"

# Format Edits

Para 0: 标题格式
居中对齐, 加粗
```

**完整示例**：[examples/example_3_legal/](examples/example_3_legal/)

### 复杂多章节文档

**场景**：所有编辑类型 - 文本、表格、格式、样式、全局修改、批注。

```markdown
---
author: Tiger
source: proposal.docx
output: proposal_revised.docx
---

# Comments

Para 3: 项目概述评注
> 选中范围: 第0-12字符
> 缩写: T
项目概述需要补充项目预算总额和预期产出指标，以便评审委员会快速了解项目规模。

Para 15: 时间计划建议
> 缩写: T
建议在开发实施阶段增加一个中期检查点（第12月），便于及时调整技术方案。

Para 20: 团队组建建议
> 缩写: T
建议增加至少1名安全工程师，确保系统符合数据安全合规要求。

# Text Edits

Para 20: 公司名称修正
将 "Tiger公司" 改为 "Tiger科技有限公司"

Para 15: 时间调整
将 "第1-3月" 改为 "第1-4月"

Para 25: 年份修正
将 "Chen et al., 2022" 改为 "Chen et al., 2023"

# Table Edits

表格1: 预算表调整
第3行下方加一行
合并第四行的三个格子

# Format Edits

Para 0: 标题格式
居中对齐, 加粗

Para 3: 项目概述格式
两端对齐, 行距1.5倍

Para 12: 表格标题格式
字号12pt, 加粗

# Style Edits

Heading1 样式:
字号16pt, 加粗

Normal 样式:
行距1.2倍, 段前6pt

# Global Changes

将 "项目组" 改为 "项目团队"
```

**完整示例**：[examples/example_4_complex/](examples/example_4_complex/)

## 运行所有示例

```bash
# 运行全部 4 个示例
bash examples/run_all_examples.sh

# 或运行单个示例
cd examples/example_1_academic
python create_original.py      # 生成原始 docx
python apply_changes.py        # 应用修改
```

## 核心设计原则

### 1. 极简原则

**生成 JSON 时，不要替换整句或整段。只替换关键词、词组或标点，并尽可能提供准确的位置。**

| 场景 | 错误 ❌ | 正确 ✅ |
|------|---------|----------|
| 修正术语 | `将 "novel approach for flood monitoring method" 改为 "improved method for flood detection"` | `将 "novel" 改为 "improved"` + `将 "monitoring" 改为 "detection"` |
| 删除冗余 | `删除: "as previously reported in our earlier studies"` | `删除: "as previously reported"` + `删除: "in our earlier studies"` |
| 修正拼写 | `将 "significantly differents results" 改为 "significantly different results"` | `将 "differents" 改为 "different"` |

### 2. 工具多样化原则

**不要只使用替换。根据实际需要适当使用删除和插入工具。**

| 场景 | 错误 ❌ | 正确 ✅ |
|------|---------|----------|
| 删除整段 | `将 "这是一段很长的内容..." 改为 ""` | `删除: "这是一段很长的内容..."` |
| 在指定位置插入 | `将 "原文" 改为 "新内容 原文"` | `在开头插入: 新内容` |
| 删除并重组 | `将 "A, B, C" 改为 "A, C"` | `删除: ", B"` |

## 文档

- [REFERENCE.md](REFERENCE.md) - 完整语法参考
- [EXAMPLES.md](EXAMPLES.md) - 更多示例和模式
- [SKILL.md](SKILL.md) - OpenCode 技能定义

## 脚本

| 脚本 | 用途 |
|------|------|
| `scripts/list_paragraphs.py` | 列出 docx 段落结构 |
| `scripts/md_to_json.py` | 将 Markdown 转换为 docx_revision JSON |
| `scripts/docx_revision/` | 内置的 docx_revision 包 |

## 测试

```bash
python scripts/md_to_json.py --test
```

## 许可证

MIT