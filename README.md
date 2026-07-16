[English](#docx-tracked-edits) | [中文](#docx-修订编辑)

# Docx Tracked Edits

AI-driven docx editing with tracked changes. Tell AI what to change in natural language, and get a Word document with revision marks automatically.

Compatible with OpenCode, Claude Code, Codex, and other AI coding assistants.

## Core Function

**This skill does two things:**

1. **Parse template**: Read modification instructions in standard format
2. **Execute revision**: Apply changes to Word document

```
Modification instructions → Parse template → Apply revision → Revised document
```

## Use Cases

### Case 1: You already know what to change

```
You: I need to change "novel approach" to "improved method" in paragraph 8, and delete the redundant opening in paragraph 15
AI: Got it, I understand your request:
  1. Paragraph 8: Change "novel" to "improved"
  2. Paragraph 15: Delete "As previously reported in our earlier studies, "
  Please confirm if this is correct?
You: Correct
AI: Applying changes... Done! Revised document generated.
```

### Case 2: Let AI find issues first

```
You: Help me review this paper for issues
AI: [Reads the paper, analyzes issues]
  Found the following issues, organized in Docx Tracked Edits template format:

  ---
  author: AI Assistant
  source: paper.docx
  output: paper_revised.docx
  ---

  # Text Edits
  Para 8: Terminology correction
  Replace "novel" with "improved"

  Para 15: Remove redundancy
  Delete: "As previously reported in our earlier studies, "

  Please confirm to apply these changes?
You: Confirm
AI: [Parses template, applies changes, generates revised document]
```

### Case 3: Copy-paste reviewer comments

```
You: Here are the reviewer's comments, please apply:
  "Paragraph 8 terminology needs to be more precise"
  "Paragraph 15 delete redundancy"
AI: [Parses comments, applies changes]
```

## Features

- **Markdown-based editing**: Write changes in human-readable Markdown
- **Tracked changes**: All edits shown as Word tracked changes
- **Comments support**: Add comments with selected text ranges
- **Format/Table/Style editing**: Full document formatting control
- **Ambiguity detection**: Error with positions when text appears multiple times

## Installation

### For Beginners

Just tell the AI:

```
Help me install docx-tracked-edits skill from https://github.com/ctfysh/docx-tracked-edits
```

The AI will automatically:
1. Clone the repository
2. Install Python dependencies (`python-docx`, `pyyaml`)
3. Configure the skill for use

No manual terminal commands needed.

### For Developers

```bash
# Clone the repository
git clone https://github.com/ctfysh/docx-tracked-edits.git
cd docx-tracked-edits

# Install dependencies
pip install python-docx pyyaml
```

## How to Use

### Slash Command

| Command | Description |
|---------|-------------|
| `/docx-tracked-edits` | Enter skill environment. Language selection dialog appears. All subsequent commands stay in this skill until user says "exit". |
| `/docx-tracked-edits <text>` | Same as above, but auto-detects language from input text. |

**Example:**

```
User: /docx-tracked-edits
AI: Please specify language: English or 中文?
User: English
AI: [Enters skill environment - all subsequent commands use English template]
User: Change "novel" to "improved" in paragraph 8
AI: [Applies change]
User: exit
AI: [Exits skill environment]
```

### Trigger Words

These phrases automatically activate this skill:

| English | 中文 |
|---------|------|
| docx tracked edits | docx 修订 |
| Word tracked changes | Word 修订模式 |
| revision marks | 修订标记 |
| tracked changes | 修订 |
| word revision | Word 修订 |

## Documentation

- [references/REFERENCE-core-en.md](references/REFERENCE-core-en.md) - English core syntax (compact)
- [references/REFERENCE-core-zh.md](references/REFERENCE-core-zh.md) - Chinese core syntax (compact)
- [references/REFERENCE-en.md](references/REFERENCE-en.md) - English full reference (examples & error handling)
- [references/REFERENCE-zh.md](references/REFERENCE-zh.md) - Chinese full reference (examples & error handling)
- [skills/SKILL.md](skills/SKILL.md) - Skill definition
- [examples/](examples/) - Complete working examples

## Examples

Each example includes a complete workflow: original document → edit instructions → revised document.

### Example 1: Academic Paper

**Use case**: Review and revise academic papers

| Feature | Example |
|---------|---------|
| Terminology fix | `novel` → `improved` |
| Redundancy removal | Delete "As previously reported in our earlier studies, " |
| Typo fix | "The the" → "The" |
| Comment | Add terminology suggestion on paragraph 8 |
| Format | Center align + bold on paragraph 8 |

```bash
# Generate original and apply revisions
python examples/example_1_academic/create_original.py
python examples/example_1_academic/apply_changes.py
```

### Example 2: Business Report

**Use case**: Update business documents with tables

| Feature | Example |
|---------|---------|
| Year update | `2023` → `2024` |
| Amount update | `$1.2M` → `$1.5M` |
| Table insert | Insert row after row 2 |
| Table delete | Delete row 5 |
| Format | Title center align + bold |

```bash
python examples/example_2_business/create_original.py
python examples/example_2_business/apply_changes.py
```

### Example 3: Legal Document

**Use case**: Revise contracts and legal documents

| Feature | Example |
|---------|---------|
| Date update | `2023年12月31日` → `2024年12月31日` |
| Amount update | `伍万元整` → `捌万元整` |
| Clause delete | Delete "第四条 不可抗力" |
| Definition insert | Insert definition clause at beginning |
| Risk comment | Flag dispute resolution risk |

```bash
python examples/example_3_legal/create_original.py
python examples/example_3_legal/apply_changes.py
```

### Example 4: Complex Document

**Use case**: Multi-section documents with all edit types

| Feature | Example |
|---------|---------|
| Text replacement | `Tiger公司` → `Tiger科技有限公司` |
| Table edits | Insert row + merge cells |
| Format edits | Center align, justify, font size |
| Style edits | Heading1 style (font size + bold) |
| Global changes | `项目组` → `项目团队` (across all paragraphs) |
| Comments | 3 comments on different sections |

```bash
python examples/example_4_complex/create_original.py
python examples/example_4_complex/apply_changes.py
```

### Run All Examples

```bash
bash examples/run_all_examples.sh
```

## License

MIT

---

# Docx 修订编辑

AI 驱动的 docx 修订模式编辑。用自然语言告诉 AI 想要修改什么，自动生成带有修订标记的 Word 文档。

兼容 OpenCode、Claude Code、Codex 及其他 AI 编程助手。

## 核心功能

**本 skill 只做两件事：**

1. **套模板**：按标准格式解析修改指令
2. **执行修订**：将修改应用到 Word 文档

```
修改指令 → 解析模板 → 应用修订 → 修订文档
```

## 使用场景

### 场景一：你已经知道要改什么

```
你：我需要把论文第8段的"novel approach"改为"improved method"，第15段删除冗余开头
AI：好的，我理解您的需求：
  1. 第8段：将 "novel" 改为 "improved"
  2. 第15段：删除 "As previously reported in our earlier studies, "
  请确认是否正确？
你：正确
AI：正在应用修改... 完成！已生成修订后的文档。
```

### 场景二：让 AI 先帮你找问题

```
你：帮我看看这篇论文有什么需要改的
AI：[读取论文，分析问题]
  发现以下问题，已按照 Docx Tracked Edits 模板格式整理：

  ---
  author: AI Assistant
  source: paper.docx
  output: paper_revised.docx
  ---

  # Text Edits
  Para 8: 术语修正
  将 "novel" 改为 "improved"

  Para 15: 删除冗余
  删除: "As previously reported in our earlier studies, "

  请确认是否应用这些修改？
你：确认
AI：[解析模板，应用修改，生成修订文档]
```

### 场景三：复制粘贴审稿意见

```
你：这是审稿人的意见，帮我应用：
  "第8段的术语需要更准确"
  "第15段删除冗余"
AI：[解析意见，应用修改]
```

## 功能特性

- **基于 Markdown 的编辑**：使用可读的 Markdown 编写修改
- **修订跟踪**：所有编辑显示为 Word 修订标记
- **批注支持**：添加带选中范围的批注
- **格式/表格/样式编辑**：完整的文档格式控制
- **歧义检测**：文本多次出现时显示带位置的错误

## 安装

### 新手入门

直接告诉 AI：

```
帮我安装 docx-tracked-edits 技能，仓库地址：https://github.com/ctfysh/docx-tracked-edits
```

AI 会自动：
1. 克隆仓库
2. 安装 Python 依赖（`python-docx`、`pyyaml`）
3. 配置技能供使用

无需手动运行终端命令。

### 开发者安装

```bash
# 克隆仓库
git clone https://github.com/ctfysh/docx-tracked-edits.git
cd docx-tracked-edits

# 安装依赖
pip install python-docx pyyaml
```

## 如何使用

### 斜杠命令

| 命令 | 说明 |
|------|------|
| `/docx-tracked-edits` | 进入技能环境。弹出语言选择窗口，后续所有命令都在此技能环境中执行，直到用户说"exit"退出。 |
| `/docx-tracked-edits <文字>` | 同上，但根据输入文字自动判断语言。 |

**示例：**

```
用户：/docx-tracked-edits
AI：请选择语言：English 或 中文？
用户：中文
AI：[进入技能环境 - 后续所有命令使用中文模板]
用户：把第8段的"novel"改成"improved"
AI：[应用修改]
用户：exit
AI：[退出技能环境]
```

### 激活词语

以下短语会自动激活此技能：

| English | 中文 |
|---------|------|
| docx tracked edits | docx 修订 |
| Word tracked changes | Word 修订模式 |
| revision marks | 修订标记 |
| tracked changes | 修订 |
| word revision | Word 修订 |

## 文档

- [references/REFERENCE-core-zh.md](references/REFERENCE-core-zh.md) - 中文核心语法（精简版）
- [references/REFERENCE-core-en.md](references/REFERENCE-core-en.md) - 英文核心语法（精简版）
- [references/REFERENCE-zh.md](references/REFERENCE-zh.md) - 中文完整参考（示例和错误处理）
- [references/REFERENCE-en.md](references/REFERENCE-en.md) - 英文完整参考（示例和错误处理）
- [skills/SKILL.md](skills/SKILL.md) - 技能定义
- [examples/](examples/) - 完整工作示例

## 示例

每个示例包含完整工作流：原始文档 → 编辑指令 → 修订文档。

### 示例 1：学术论文

**使用场景**：审阅和修订学术论文

| 功能 | 示例 |
|------|------|
| 术语修正 | `novel` → `improved` |
| 冗余删除 | 删除 "As previously reported in our earlier studies, " |
| 错误修复 | "The the" → "The" |
| 批注 | 在第8段添加术语建议 |
| 格式 | 第8段居中对齐 + 加粗 |

```bash
# 生成原始文档并应用修订
python examples/example_1_academic/create_original.py
python examples/example_1_academic/apply_changes.py
```

### 示例 2：商业报告

**使用场景**：更新带表格的商业文档

| 功能 | 示例 |
|------|------|
| 年份更新 | `2023` → `2024` |
| 金额更新 | `$1.2M` → `$1.5M` |
| 表格插入 | 在第2行下方插入新行 |
| 表格删除 | 删除第5行 |
| 格式 | 标题居中对齐 + 加粗 |

```bash
python examples/example_2_business/create_original.py
python examples/example_2_business/apply_changes.py
```

### 示例 3：法律文档

**使用场景**：修订合同和法律文档

| 功能 | 示例 |
|------|------|
| 日期更新 | `2023年12月31日` → `2024年12月31日` |
| 金额更新 | `伍万元整` → `捌万元整` |
| 条款删除 | 删除 "第四条 不可抗力" |
| 定义插入 | 在开头插入定义条款 |
| 风险批注 | 标记争议解决条款风险 |

```bash
python examples/example_3_legal/create_original.py
python examples/example_3_legal/apply_changes.py
```

### 示例 4：复杂文档

**使用场景**：多节文档，综合使用所有编辑类型

| 功能 | 示例 |
|------|------|
| 文本替换 | `Tiger公司` → `Tiger科技有限公司` |
| 表格编辑 | 插入行 + 合并单元格 |
| 格式编辑 | 居中对齐、两端对齐、字号 |
| 样式编辑 | Heading1 样式（字号 + 加粗） |
| 全局替换 | `项目组` → `项目团队`（跨所有段落） |
| 批注 | 3处批注，覆盖不同节 |

```bash
python examples/example_4_complex/create_original.py
python examples/example_4_complex/apply_changes.py
```

### 运行所有示例

```bash
bash examples/run_all_examples.sh
```

## 许可证

MIT
