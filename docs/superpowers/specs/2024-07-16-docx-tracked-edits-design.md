# Docx Tracked Edits Skill 设计文档

**日期**: 2024-07-16
**状态**: 待批准

## 概述

创建一个 AI 技能，用于将**已识别的修改需求**转化为 Word 文档的修订模式编辑。

## 核心功能

**本 skill 只做两件事：**

1. **套模板**：按标准格式解析修改指令
2. **执行修订**：将修改应用到 Word 文档

```
修改指令 → 解析模板 → 应用修订 → 修订文档
```

## 核心定位

**本 skill 是执行器 + 模板协议定义者。**

用户的完整工作流是：

```
1. 审查阶段（其他工具/对话）：读论文，发现问题
2. 模板阶段：其他 AI 按本 skill 定义的模板格式输出问题列表
3. 执行阶段（本 skill）：解析模板，将问题转化为 tracked changes
```

## 模板协议

**本 skill 定义了修改指令的标准模板格式。其他 AI 工具必须按此格式输出，本 skill 才能解析执行。**

### 模板格式

```markdown
---
author: [审稿人名称]
source: [原始文档路径]
output: [修订后文档路径]
---

# Comments
Para [段落号]: [标题]
[批注内容]
> 选中范围: 第[N]-[M]字符（可选）

# Text Edits
Para [段落号]: [标题]
将 "[旧文本]" 改为 "[新文本]"

Para [段落号]: [标题]
删除: "[要删除的文本]"

# Format Edits
Para [段落号]: [标题]
居中对齐, 行距1.5倍, 段前12pt

# Table Edits
表格[表格号]:
第[N]行下方加一行

# Style Edits
[样式名] 样式:
行距1.5倍, 字号12pt

# Global Changes
将 "[全文要替换的旧文本]" 改为 "[新文本]"
```

### 模板设计原则

1. **简洁性**：只包含必要的修改信息
2. **可读性**：人类和 AI 都能轻松理解
3. **可解析性**：结构清晰，易于程序解析
4. **完整性**：覆盖所有修改类型（替换、删除、插入、格式、表格、样式、批注）

### 其他 AI 工具如何使用此模板

其他 AI 工具（如 Claude、GPT、Gemini 等）在帮用户审查文档时：

1. 读取文档内容
2. 识别问题
3. **按照本模板格式输出问题列表**
4. 用户确认后，本 skill 解析并执行修改

**示例对话：**

```
用户：帮我看看这篇论文有什么需要改的
其他 AI：[读取论文，分析问题]
  我发现以下问题，已按照 Docx Tracked Edits 模板格式整理：

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

  # Comments

  Para 24: 建议
  此处需要补充数据支持
  > 选中范围: 第10-30字符

  请确认是否应用这些修改？

用户：确认
本 skill：[解析模板，应用修改，生成修订文档]
```

## 目标用户

**核心用户：不懂代码的普通用户**

- 学术论文作者
- 行政人员
- 法律文档处理者

**关键：用户只需要把修改需求告诉 AI，不需要知道任何技术细节。**

## 用户交互设计

### 完整工作流

```
1. 审查阶段：其他 AI 读文档，找问题
2. 模板阶段：其他 AI 按本 skill 定义的模板格式输出问题列表
3. 执行阶段：本 skill 解析模板，应用修改
4. 结果阶段：用户获得修订文档
```

### 场景一：用户直接告诉 AI 要改什么

```
用户：我需要把论文第8段的"novel approach"改为"improved method"，第15段删除冗余开头
AI：好的，我理解您的需求：
  1. 第8段：将 "novel" 改为 "improved"
  2. 第15段：删除 "As previously reported in our earlier studies, "
  请确认是否正确？
用户：正确
AI：正在应用修改... 完成！已生成修订后的文档。
```

### 场景二：让 AI 先找问题，再按模板执行

```
用户：帮我看看这篇论文有什么需要改的
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
用户：确认
AI：[解析模板，应用修改，生成修订文档]
```

### 场景三：用户粘贴审稿意见

```
用户：这是审稿人的意见，帮我应用：
  "第8段的术语需要更准确"
  "第15段删除冗余"
AI：[解析意见，转换为模板格式，应用修改]
```

## 设计原则

### 1. 执行器 + 模板协议定义者

- skill 定义修改指令的标准模板格式
- 其他 AI 工具必须按此模板格式输出问题列表
- skill 解析模板并执行修改
- 输入是符合模板格式的修改指令，输出是修订后的文档

### 2. 极简原则

修改指令只替换关键内容，不整句整段替换：

| 场景 | 错误做法 ❌ | 正确做法 ✅ |
|------|-----------|------------|
| 修改术语 | 将 "novel approach for flood monitoring method" 改为 "improved method for flood detection" | 将 "novel" 改为 "improved" + 将 "monitoring" 改为 "detection" |

### 3. 工具多样化原则

根据实际需求选择最合适的修改方式：

| 修改方式 | 适用场景 |
|---------|---------|
| **替换** | 修改已有内容 |
| **删除** | 去除不需要的内容 |
| **插入** | 添加新内容 |

## 修改指令来源

用户可以通过多种方式提供修改指令：

### 1. 自然语言描述

```
请帮我修改：
- 第8段：把"novel"改为"improved"
- 第15段：删除开头的冗余
- 第24段：添加批注说明
```

### 2. 复制粘贴审稿意见

```
审稿人意见：
1. The terminology in paragraph 8 needs to be more precise
2. Paragraph 15 has redundant opening
```

### 3. 结构化列表

```
Para 8: 将 "novel" 改为 "improved"
Para 15: 删除: "As previously reported in our earlier studies, "
Para 24: 批注: 建议修改术语
```

## 技术架构（用户不可见）

### 用户视角

```
用户 → AI 助手 → Word 文档
```

### 实际架构

```
用户修改指令 → AI 解析 → Markdown 指令 → JSON 配置 → Python 脚本 → Word 文档
```

**关键点：所有技术细节对用户完全透明。**

## 示例设计要求

每个示例**必须**包含以下部分，形成完整的用户视角演示：

### 1. 修改需求来源

展示修改需求从哪里来（审稿意见、用户记录、AI 分析等）。

### 2. AI 理解的需求

展示 AI 如何理解用户的意图，列出具体的修改点。

### 3. 修改前后对比

展示原始文档和修改后文档的对比。

### 4. 最终效果

展示 Word 文档中的实际效果，包括修订标记和批注。

### 示例模板

```markdown
## 示例 N：[场景名称]

### 修改需求来源

**审稿人意见：**
> "第8段的术语需要更准确，'novel approach'应该改为更专业的表述。第15段开头冗余，建议删除。"

### AI 理解的修改

1. 第8段：将 "novel" 改为 "improved"
2. 第15段：删除 "As previously reported in our earlier studies, "

### 修改前

**第8段：**
> The novel approach for flood monitoring method demonstrates significant improvements...

**第15段：**
> As previously reported in our earlier studies, the results show significant correlation.

### 修改后

**第8段：**
> The ~~novel~~ **improved** approach for flood monitoring method demonstrates significant improvements...

**第15段：**
> ~~As previously reported in our earlier studies,~~ the results show significant correlation.

### Word 文档中的效果

[展示 Word 中修订模式的显示效果]
```

## 目录结构

```
docx-tracked-edits/
├── SKILL.md              # 语言路由器（自动加载对应语言版本）
├── SKILL-en.md           # 英文版技能说明
├── SKILL-zh.md           # 中文版技能说明
├── REFERENCE-en.md       # 英文语法参考（模板协议）
├── REFERENCE-zh.md       # 中文语法参考（模板协议）
├── README.md             # 项目说明（面向用户）- 双语
├── examples/             # 使用示例
│   ├── example_1_academic/
│   ├── example_2_business/
│   ├── example_3_legal/
│   └── example_4_complex/
└── scripts/              # 后台脚本（用户不可见）
    ├── list_paragraphs.py
    ├── md_to_json.py
    └── docx_revision/
```

## 双语设计

### 设计原则

**所有面向用户的文档都提供中英文双语版本，用户可以选择适合自己语言习惯的版本。**

### 双语架构

```
SKILL.md（语言路由器）
  ├── SKILL-en.md（英文版）
  └── SKILL-zh.md（中文版）

README.md（双语在同一文件）
  ├── [English](#docx-tracked-edits) 部分
  └── [中文](#docx-修订编辑) 部分

REFERENCE 文件
  ├── REFERENCE-en.md（英文语法参考）
  └── REFERENCE-zh.md（中文语法参考）
```

### SKILL.md 语言路由

SKILL.md 作为语言路由器，根据用户语言自动加载对应的技能文件：

```markdown
## Language Detection

**Auto-detect user language and load the appropriate skill file:**

- If user's request is in **English** → Load `SKILL-en.md`
- If user's request is in **Chinese** → Load `SKILL-zh.md`
- If ambiguous → Ask user to choose: "Please specify language: English or 中文?"
```

### README.md 双语格式

README.md 使用锚点跳转实现双语导航：

```markdown
[English](#docx-tracked-edits) | [中文](#docx-修订编辑)

# Docx Tracked Edits
[English section...]

---

# Docx 修订编辑
[中文 section...]
```

### REFERENCE 文件

REFERENCE 文件分别提供中英文版本的模板协议和语法参考。两个文件内容结构相同，只是语言不同。

## 测试用例

1. **基础替换**：用户说"把第8段的'novel'改为'improved'"
2. **删除内容**：用户说"删除第15段的冗余开头"
3. **添加批注**：用户说"在第24段添加批注，建议修改术语"
4. **格式修改**：用户说"把标题居中对齐"
5. **表格操作**：用户说"在表格第2行下方插入一行"
6. **全局替换**：用户说"把全文的'significant difference'改为'statistically significant difference'"
7. **审稿意见**：用户粘贴审稿人意见，AI 解析后应用修改
8. **批量修改**：用户列出多个修改点，一次性应用

## 待确认

- [ ] 是否需要支持密码保护的 docx？
- [ ] 是否需要支持撤销操作？
- [ ] 是否需要生成修改摘要报告？
- [ ] 是否需要支持批量处理多个文档？
