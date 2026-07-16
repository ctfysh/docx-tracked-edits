# Docx Tracked Edits Skill 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 创建一个 OpenCode skill，用于将**已识别的修改需求**转化为 Word 文档的修订模式编辑。

**核心定位：本 skill 是执行器，不是审查工具。**

## 核心功能

**本 skill 只做两件事：**

1. **套模板**：按标准格式解析修改指令
2. **执行修订**：将修改应用到 Word 文档

```
修改指令 → 解析模板 → 应用修订 → 修订文档
```

## 工作流

```
1. 审查阶段（其他工具/对话）：读论文，发现问题
2. 模板阶段：其他 AI 按本 skill 定义的模板格式输出问题列表
3. 执行阶段（本 skill）：解析模板，将问题转化为 tracked changes
```

### 模板协议

**本 skill 定义了修改指令的标准模板格式。其他 AI 工具必须按此格式输出，本 skill 才能解析执行。**

模板格式详见 REFERENCE-zh.md 和 REFERENCE-en.md。

### 审查阶段（不在本 skill 范围内）

用户可能通过多种方式识别需要修改的内容：

- 让 AI 阅读论文并提出修改建议
- 自己审阅后记录修改点
- 用其他工具（如 Grammarly）检查问题
- 同事/导师的审稿意见
- 期刊审稿人的反馈

### 执行阶段（本 skill 的职责）

将识别出的修改需求转化为 Word 修订标记。

**Architecture:** 单文件 skill，捆绑 docx_revision 包。包含 SKILL.md 主指令、list_paragraphs.py 段落查看器、md_to_json.py 转换脚本。

**Tech Stack:** Python, python-docx, PyYAML

## 双语设计

### 设计原则

**所有面向用户的文档都提供中英文双语版本。**

### 双语架构

| 文件 | 语言 | 用途 |
|------|------|------|
| `SKILL.md` | 路由器 | 根据用户语言自动加载对应技能文件 |
| `SKILL-en.md` | 英文 | 英文版技能说明 |
| `SKILL-zh.md` | 中文 | 中文版技能说明 |
| `REFERENCE-en.md` | 英文 | 英文语法参考（模板协议） |
| `REFERENCE-zh.md` | 中文 | 中文语法参考（模板协议） |
| `README.md` | 双语 | 项目说明，使用锚点跳转切换语言 |

### SKILL.md 语言路由

SKILL.md 只是路由器，根据用户语言自动加载对应的技能文件：

```markdown
## Language Detection

**Auto-detect user language and load the appropriate skill file:**

- If user's request is in **English** → Load `SKILL-en.md`
- If user's request is in **Chinese** → Load `SKILL-zh.md`
- If ambiguous → Ask user to choose: "Please specify language: English or 中文?"
```

## 面向非技术用户的设计原则

**核心理念：用户只需要把修改需求告诉 AI，所有技术操作都在后台自动完成。**

### 用户体验流程

```
用户 → AI 助手 → Word 文档
```

- 用户不需要知道什么是 Markdown
- 用户不需要知道什么是 JSON
- 用户不需要执行任何命令
- 用户不需要安装任何软件
- 所有技术细节对用户完全透明

### 修改指令来源

用户可以通过多种方式提供修改指令：

1. **自然语言描述**："把第8段的'novel'改为'improved'"
2. **复制粘贴审稿意见**：期刊审稿人的反馈
3. **结构化列表**：用户自己记录的修改点

## Global Constraints

- 捆绑 docx_revision 包，不依赖外部安装
- MD 语法以可读性优先，覆盖 docx_revision 全部 JSON 功能
- 歧义处理：出现多次时报错并显示位置
- 输出路径：`/Users/tiger/Desktop/OpenSource/docx-tracked-edits/`

### Core Design Principles

#### 1. Minimalism Principle (极简原则)

**生成 JSON 文档时不要出现成句成段的替换，只替换关键字母、单词（词组）或者标点就可以了，并且尽可能给出准确位置。**

- 更清晰的修订历史
- 更精确的审核
- 减少冲突

#### 2. Tool Diversity Principle (工具多样化原则)

**不能只用 replace，还要根据实际需要用 delete 和 insert 等工具。**

- replace: 修改已有文本
- delete: 删除冗余/错误内容
- insert: 添加缺失内容

---

### Task 1: 复制 docx_revision 包

**Files:**
- Create: `scripts/docx_revision/__init__.py`
- Create: `scripts/docx_revision/reviewer.py`
- Create: `scripts/docx_revision/__main__.py`

**Interfaces:**
- Consumes: `/Users/tiger/Desktop/mess/docx修订模式/docx_revision/` 源码
- Produces: 完整的 docx_revision 包副本

- [ ] **Step 1: 创建目标目录**

```bash
mkdir -p /Users/tiger/Desktop/OpenSource/docx-tracked-edits/scripts/docx_revision
```

- [ ] **Step 2: 复制所有 Python 文件**

```bash
cp /Users/tiger/Desktop/mess/docx修订模式/docx_revision/*.py \
   /Users/tiger/Desktop/OpenSource/docx-tracked-edits/scripts/docx_revision/
```

- [ ] **Step 3: 验证包可导入**

```bash
cd /Users/tiger/Desktop/OpenSource/docx-tracked-edits/scripts
python -c "from docx_revision import ComprehensiveDocxReviewer; print('OK')"
```

Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add scripts/docx_revision/
git commit -m "feat: bundle docx_revision package"
```

---

### Task 2: 创建 list_paragraphs.py

**Files:**
- Create: `scripts/list_paragraphs.py`

**Interfaces:**
- Consumes: docx 文件路径
- Produces: 带索引的段落列表输出

- [ ] **Step 1: 编写脚本**

```python
#!/usr/bin/env python3
"""列出 docx 文件的段落结构，用于确定 Para N 索引"""
import sys
from docx import Document

def main():
    if len(sys.argv) < 2:
        print("用法: python list_paragraphs.py <file.docx>")
        sys.exit(1)
    
    doc = Document(sys.argv[1])
    print(f"段落列表 (共{len(doc.paragraphs)}段):\n")
    for i, para in enumerate(doc.paragraphs):
        text = para.text[:80].replace('\n', ' ').strip()
        if text:
            print(f"{i}: {text}")
        else:
            print(f"{i}: (空段落)")

if __name__ == '__main__':
    main()
```

- [ ] **Step 2: 测试脚本**

```bash
python /Users/tiger/Desktop/OpenSource/docx-tracked-edits/scripts/list_paragraphs.py \
  "/Users/tiger/Desktop/mess/程靖雯论文/V2/Shifting phosphorus pathways and cumulative policy effects in Erhai Lake basin A 30-year SFA–BSTS analysis (1992–2022).docx" \
  | head -30
```

Expected: 显示段落列表

- [ ] **Step 3: Commit**

```bash
git add scripts/list_paragraphs.py
git commit -m "feat: add list_paragraphs.py script"
```

---

### Task 3: 创建 md_to_json.py - 基础框架

**Files:**
- Create: `scripts/md_to_json.py`

**Interfaces:**
- Consumes: MD 文件路径
- Produces: JSON 文件

- [ ] **Step 1: 编写基础解析框架**

```python
#!/usr/bin/env python3
"""将 MD 变更文件转换为 docx_revision JSON 配置"""
import json
import re
import sys
from pathlib import Path

def parse_frontmatter(content):
    """解析 YAML frontmatter"""
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not match:
        raise ValueError("缺少 YAML frontmatter")
    
    frontmatter = {}
    for line in match.group(1).split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            frontmatter[key.strip()] = value.strip()
    
    return frontmatter, content[match.end():]

def parse_sections(body):
    """解析各 section"""
    sections = {}
    current_section = None
    
    for line in body.split('\n'):
        if line.startswith('# '):
            current_section = line[2:].strip()
            sections[current_section] = []
        elif current_section and line.strip():
            sections[current_section].append(line)
    
    return sections

def main():
    if len(sys.argv) < 3:
        print("用法: python md_to_json.py <input.md> <output.json>")
        sys.exit(1)
    
    md_path = Path(sys.argv[1])
    json_path = Path(sys.argv[2])
    
    content = md_path.read_text(encoding='utf-8')
    frontmatter, body = parse_frontmatter(content)
    sections = parse_sections(body)
    
    config = {
        "enable_track_revisions": frontmatter.get('track_revisions', 'true') == 'true',
        "lock_revisions": frontmatter.get('lock_revisions', 'false') == 'true',
        "revision_password": frontmatter.get('revision_password'),
        "author": frontmatter.get('author', 'Reviewer'),
        "source": frontmatter.get('source'),
        "output": frontmatter.get('output'),
        "comments": [],
        "text_modifications": [],
        "format_modifications": [],
        "table_modifications": [],
        "style_modifications": []
    }
    
    json_path.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"✅ 已生成: {json_path}")

if __name__ == '__main__':
    main()
```

- [ ] **Step 2: 测试基础框架**

创建测试 MD 文件 `test_basic.md`:
```markdown
---
author: Test
source: test.docx
output: test_out.docx
---

# Comments

测试批注内容

---

# Text Edits

测试替换内容
```

运行:
```bash
python /Users/tiger/Desktop/OpenSource/docx-tracked-edits/scripts/md_to_json.py test_basic.md test_output.json
cat test_output.json
```

Expected: JSON 文件包含 frontmatter 信息

- [ ] **Step 3: Commit**

```bash
git add scripts/md_to_json.py test_basic.md
git commit -m "feat: add md_to_json.py basic framework"
```

---

### Task 4: 实现 Comments 解析

**Files:**
- Modify: `scripts/md_to_json.py`

**Interfaces:**
- Consumes: `# Comments` section 内容
- Produces: `config["comments"]` 列表

- [ ] **Step 1: 添加 Comments 解析函数**

```python
def parse_comments(lines):
    """解析 Comments section"""
    comments = []
    current = None
    
    for line in lines:
        # 匹配 "Para N: title" 或 "Para N: title (范围)"
        match = re.match(r'^Para\s+(\d+):\s*(.+)', line)
        if match:
            if current:
                comments.append(current)
            current = {
                "paragraph_index": int(match.group(1)),
                "text": "",
                "author": None,
                "initials": None,
                "start_pos": None,
                "end_pos": None
            }
            continue
        
        # 匹配范围信息
        range_match = re.match(r'^>\s*选中范围:\s*第(\d+)-(\d+)字符', line)
        if range_match and current:
            current["start_pos"] = int(range_match.group(1))
            current["end_pos"] = int(range_match.group(2))
            continue
        
        # 匹配缩写
        initials_match = re.match(r'^>\s*缩写:\s*(\w+)', line)
        if initials_match and current:
            current["initials"] = initials_match.group(1)
            continue
        
        # 普通文本行
        if current and line.strip() and not line.startswith('>'):
            if current["text"]:
                current["text"] += "\n" + line.strip()
            else:
                current["text"] = line.strip()
    
    if current:
        comments.append(current)
    
    return comments
```

- [ ] **Step 2: 在 main 中调用**

```python
if 'Comments' in sections:
    config["comments"] = parse_comments(sections['Comments'])
```

- [ ] **Step 3: 测试 Comments 解析**

更新 `test_basic.md`:
```markdown
---
author: Tiger
source: test.docx
output: test_out.docx
---

# Comments

Para 24: 方法论建议
此处列出的三项"进展"表述清晰但部分重叠...
> 选中范围: 第10-50字符
> 缩写: T

Para 45: 图表问题
Figure 3 图例字体过小。
```

运行并检查 JSON 输出

- [ ] **Step 4: Commit**

```bash
git add scripts/md_to_json.py
git commit -m "feat: add Comments parsing"
```

---

### Task 5: 实现 Text Edits 解析

**Files:**
- Modify: `scripts/md_to_json.py`

**Interfaces:**
- Consumes: `# Text Edits` section 内容
- Produces: `config["text_modifications"]` 列表

- [ ] **Step 1: 添加 Text Edits 解析函数**

```python
def parse_text_edits(lines):
    """解析 Text Edits section"""
    edits = []
    current_para = None
    current_title = None
    
    for line in lines:
        # 匹配 "Para N: title"
        para_match = re.match(r'^Para\s+(\d+):\s*(.+)', line)
        if para_match:
            current_para = int(para_match.group(1))
            current_title = para_match.group(2)
            continue
        
        if current_para is None:
            continue
        
        # 替换: 将 "old" 改为 "new"
        replace_match = re.match(r'^将\s*"(.+?)"\s*改为\s*"(.+?)"', line)
        if replace_match:
            edits.append({
                "type": "replace",
                "paragraph_index": current_para,
                "old_text": replace_match.group(1),
                "new_text": replace_match.group(2),
                "author": None
            })
            continue
        
        # 插入: 在开头/末尾插入: text
        insert_match = re.match(r'^在(开头|末尾)插入:\s*(.+)', line)
        if insert_match:
            position = 0 if insert_match.group(1) == '开头' else None
            edits.append({
                "type": "insert",
                "paragraph_index": current_para,
                "text": insert_match.group(2),
                "position": position,
                "author": None
            })
            continue
        
        # 删除: 删除: "text" 或 删除: "text" (第N-M字符)
        delete_match = re.match(r'^删除:\s*"(.+?)"(?:\s*\(第(\d+)-(\d+)字符\))?', line)
        if delete_match:
            edit = {
                "type": "delete",
                "paragraph_index": current_para,
                "text": delete_match.group(1),
                "author": None
            }
            if delete_match.group(2):
                edit["start_pos"] = int(delete_match.group(2))
                edit["end_pos"] = int(delete_match.group(3))
            edits.append(edit)
            continue
    
    return edits
```

- [ ] **Step 2: 在 main 中调用**

```python
if 'Text Edits' in sections:
    config["text_modifications"] = parse_text_edits(sections['Text Edits'])
```

- [ ] **Step 3: 测试 Text Edits 解析**

更新测试 MD 并验证 JSON 输出

- [ ] **Step 4: Commit**

```bash
git add scripts/md_to_json.py
git commit -m "feat: add Text Edits parsing"
```

---

### Task 6: 实现歧义检测

**Files:**
- Modify: `scripts/md_to_json.py`

**Interfaces:**
- Consumes: Text Edits + 源 docx 段落内容
- Produces: 错误信息或通过

- [ ] **Step 1: 添加歧义检测函数**

```python
def check_ambiguity(edit, doc):
    """检查文本在段落中是否出现多次"""
    if edit["type"] not in ("replace", "delete"):
        return None
    
    para_idx = edit["paragraph_index"]
    if para_idx >= len(doc.paragraphs):
        return f"段落索引 {para_idx} 超出范围"
    
    para_text = doc.paragraphs[para_idx].text
    old_text = edit.get("old_text") or edit.get("text")
    
    if old_text not in para_text:
        return f"文本 '{old_text[:30]}...' 未在段落 {para_idx} 中找到"
    
    # 检查出现次数
    count = para_text.count(old_text)
    if count > 1:
        # 找出所有位置
        positions = []
        start = 0
        while True:
            pos = para_text.find(old_text, start)
            if pos == -1:
                break
            positions.append((pos, pos + len(old_text)))
            start = pos + 1
        
        pos_str = "\n".join([f"  位置{i+1}: 第{p[0]}-{p[1]}字符" for i, p in enumerate(positions)])
        return f"⚠️ 歧义检测: \"{old_text[:30]}...\" 在段落 {para_idx} 出现{count}次\n{pos_str}\n\n请在 MD 中添加位置信息:\n  删除: \"{old_text}\" (第{positions[0][0]}-{positions[0][1]}字符)"
    
    return None
```

- [ ] **Step 2: 在 main 中集成**

```python
from docx import Document

# 在解析完 text_modifications 后
if config["text_modifications"]:
    doc = Document(config["source"])
    errors = []
    for edit in config["text_modifications"]:
        error = check_ambiguity(edit, doc)
        if error:
            errors.append(error)
    
    if errors:
        print("\n".join(errors))
        sys.exit(1)
```

- [ ] **Step 3: 测试歧义检测**

创建包含重复文本的测试 MD，验证报错信息

- [ ] **Step 4: Commit**

```bash
git add scripts/md_to_json.py
git commit -m "feat: add ambiguity detection"
```

---

### Task 7: 实现 Format Edits 解析

**Files:**
- Modify: `scripts/md_to_json.py`

**Interfaces:**
- Consumes: `# Format Edits` section 内容
- Produces: `config["format_modifications"]` 列表

- [ ] **Step 1: 添加 Format Edits 解析函数**

```python
# 格式关键词映射
FORMAT_KEYWORDS = {
    '居中对齐': ('alignment', 'center'),
    '左对齐': ('alignment', 'left'),
    '右对齐': ('alignment', 'right'),
    '两端对齐': ('alignment', 'justify'),
    '加粗': ('bold', True),
    '斜体': ('italic', True),
}

def parse_format_value(text):
    """解析格式值，如 '行距1.5倍' → ('line_spacing', 1.5)"""
    # 行距
    match = re.match(r'行距([\d.]+)倍', text)
    if match:
        return ('line_spacing', float(match.group(1)))
    
    # 段前/段后
    match = re.match(r'段前([\d.]+)pt', text)
    if match:
        return ('space_before', float(match.group(1)))
    
    match = re.match(r'段后([\d.]+)pt', text)
    if match:
        return ('space_after', float(match.group(1)))
    
    # 缩进
    match = re.match(r'左缩进([\d.]+)pt', text)
    if match:
        return ('indent_left', float(match.group(1)))
    
    match = re.match(r'右缩进([\d.]+)pt', text)
    if match:
        return ('indent_right', float(match.group(1)))
    
    # 字号
    match = re.match(r'字号([\d.]+)pt', text)
    if match:
        return ('font_size', float(match.group(1)))
    
    return None

def parse_format_edits(lines):
    """解析 Format Edits section"""
    edits = []
    current_para = None
    current_changes = {}
    
    for line in lines:
        # 匹配段落范围 "Para N-M:" 或 "Para N:"
        para_match = re.match(r'^Para\s+(\d+)(?:-(\d+))?:\s*(.*)', line)
        if para_match:
            if current_para is not None and current_changes:
                edits.append({
                    "scope": "paragraph",
                    "paragraph_index": current_para,
                    "changes": current_changes.copy(),
                    "author": None
                })
            current_para = int(para_match.group(1))
            current_changes = {}
            continue
        
        if current_para is None:
            continue
        
        # 解析格式项，用逗号分隔
        items = [x.strip() for x in line.split(',')]
        for item in items:
            # 关键词匹配
            for keyword, (key, value) in FORMAT_KEYWORDS.items():
                if keyword in item:
                    current_changes[key] = value
                    break
            else:
                # 值匹配
                result = parse_format_value(item)
                if result:
                    current_changes[result[0]] = result[1]
    
    if current_para is not None and current_changes:
        edits.append({
            "scope": "paragraph",
            "paragraph_index": current_para,
            "changes": current_changes,
            "author": None
        })
    
    return edits
```

- [ ] **Step 2: 在 main 中调用**

```python
if 'Format Edits' in sections:
    config["format_modifications"] = parse_format_edits(sections['Format Edits'])
```

- [ ] **Step 3: 测试 Format Edits 解析**

- [ ] **Step 4: Commit**

```bash
git add scripts/md_to_json.py
git commit -m "feat: add Format Edits parsing"
```

---

### Task 8: 实现 Table Edits 解析

**Files:**
- Modify: `scripts/md_to_json.py`

**Interfaces:**
- Consumes: `# Table Edits` section 内容
- Produces: `config["table_modifications"]` 列表

- [ ] **Step 1: 添加 Table Edits 解析函数**

```python
def parse_table_edits(lines):
    """解析 Table Edits section"""
    edits = []
    current_table = None
    
    for line in lines:
        # 匹配 "表格N:" 或 "表格N: title"
        table_match = re.match(r'^表格(\d+):', line)
        if table_match:
            current_table = int(table_match.group(1))
            continue
        
        if current_table is None:
            continue
        
        # 第N行下方加一行
        insert_match = re.match(r'^\s*第(\d+)行下方加一行', line)
        if insert_match:
            edits.append({
                "type": "insert_row",
                "table_index": current_table,
                "row_index": int(insert_match.group(1)),
                "author": None
            })
            continue
        
        # 删掉第N行
        delete_match = re.match(r'^\s*删掉第(\d+)行', line)
        if delete_match:
            edits.append({
                "type": "delete_row",
                "table_index": current_table,
                "row_index": int(delete_match.group(1)),
                "author": None
            })
            continue
        
        # 合并第N行的X-Y列
        merge_match = re.match(r'^\s*合并第(\d+)行的第?([A-Z])-([A-Z])列', line)
        if merge_match:
            row = int(merge_match.group(1)) - 1  # 转为0-based
            start_col = ord(merge_match.group(2)) - ord('A')
            end_col = ord(merge_match.group(3)) - ord('A')
            edits.append({
                "type": "merge_cells",
                "table_index": current_table,
                "start_cell": [row, start_col],
                "end_cell": [row, end_col],
                "author": None
            })
            continue
        
        # 合并第二行的三个格子 (自然语言)
        merge_natural = re.match(r'^\s*合并第?([一二三四五六七八九十\d]+)行的([一二三四五六七八九十\d]+)个格子', line)
        if merge_natural:
            # 中文数字转换
            cn_num = {'一':1, '二':2, '三':3, '四':4, '五':5, '六':6, '七':7, '八':8, '九':9, '十':10}
            row_str = merge_natural.group(1)
            count_str = merge_natural.group(2)
            
            row = cn_num.get(row_str, int(row_str)) - 1
            count = cn_num.get(count_str, int(count_str))
            
            edits.append({
                "type": "merge_cells",
                "table_index": current_table,
                "start_cell": [row, 0],
                "end_cell": [row, count - 1],
                "author": None
            })
            continue
    
    return edits
```

- [ ] **Step 2: 在 main 中调用**

```python
if 'Table Edits' in sections:
    config["table_modifications"] = parse_table_edits(sections['Table Edits'])
```

- [ ] **Step 3: 测试 Table Edits 解析**

- [ ] **Step 4: Commit**

```bash
git add scripts/md_to_json.py
git commit -m "feat: add Table Edits parsing"
```

---

### Task 9: 实现 Style Edits 和 Global Changes 解析

**Files:**
- Modify: `scripts/md_to_json.py`

**Interfaces:**
- Consumes: `# Style Edits` 和 `# Global Changes` section 内容
- Produces: `config["style_modifications"]` 和全局替换列表

- [ ] **Step 1: 添加 Style Edits 解析**

```python
def parse_style_edits(lines):
    """解析 Style Edits section"""
    edits = []
    current_style = None
    current_changes = {}
    
    for line in lines:
        # 匹配 "StyleName 样式:"
        style_match = re.match(r'^(\S+)\s*样式:', line)
        if style_match:
            if current_style and current_changes:
                edits.append({
                    "style_name": current_style,
                    "changes": current_changes.copy(),
                    "author": None
                })
            current_style = style_match.group(1)
            current_changes = {}
            continue
        
        if current_style is None:
            continue
        
        # 解析格式项
        items = [x.strip() for x in line.split(',')]
        for item in items:
            result = parse_format_value(item)
            if result:
                current_changes[result[0]] = result[1]
    
    if current_style and current_changes:
        edits.append({
            "style_name": current_style,
            "changes": current_changes,
            "author": None
        })
    
    return edits
```

- [ ] **Step 2: 添加 Global Changes 解析**

```python
def parse_global_changes(lines):
    """解析 Global Changes section，返回待全局替换的列表"""
    replacements = []
    
    for line in lines:
        # 将 "old" 改为 "new"
        match = re.match(r'^将\s*"?([^"]+)"?\s*改为\s*"?([^"]+)"?', line)
        if match:
            replacements.append({
                "old": match.group(1),
                "new": match.group(2)
            })
    
    return replacements
```

- [ ] **Step 3: 在 main 中集成全局替换**

```python
# 全局替换需要遍历所有段落
if 'Global Changes' in sections:
    global_replacements = parse_global_changes(sections['Global Changes'])
    if global_replacements:
        doc = Document(config["source"])
        for repl in global_replacements:
            for i, para in enumerate(doc.paragraphs):
                if repl["old"] in para.text:
                    config["text_modifications"].append({
                        "type": "replace",
                        "paragraph_index": i,
                        "old_text": repl["old"],
                        "new_text": repl["new"],
                        "author": None
                    })
                    break  # 只替换第一个找到的
```

- [ ] **Step 4: 测试**

- [ ] **Step 5: Commit**

```bash
git add scripts/md_to_json.py
git commit -m "feat: add Style Edits and Global Changes parsing"
```

---

### Task 10: 创建 SKILL.md

**Files:**
- Create: `SKILL.md`

**Interfaces:**
- Consumes: 设计文档
- Produces: 完整的 SKILL.md 指令文件

- [ ] **Step 1: 编写 SKILL.md**

基于设计文档，创建完整的 SKILL.md，包含：
- 描述（触发条件）
- 快速开始
- MD 语法说明
- 工作流程
- 脚本使用说明
- 示例

- [ ] **Step 2: 验证格式**

确保 SKILL.md 符合 OpenCode skill 格式要求

- [ ] **Step 3: Commit**

```bash
git add SKILL.md
git commit -m "feat: add SKILL.md"
```

---

### Task 11: 创建 REFERENCE.md 和 EXAMPLES.md

**Files:**
- Create: `REFERENCE.md`
- Create: `EXAMPLES.md`

**Interfaces:**
- Consumes: 设计文档
- Produces: 详细文档和示例

- [ ] **Step 1: 编写 REFERENCE.md**

完整语法参考，包括：
- 所有语法元素
- 高级用法
- 错误处理说明

- [ ] **Step 2: 编写 EXAMPLES.md**

3-5 个完整示例：
- 学术论文审阅
- 商业文档更新
- 合同修订
- 批量处理

- [ ] **Step 3: Commit**

```bash
git add REFERENCE.md EXAMPLES.md
git commit -m "docs: add REFERENCE.md and EXAMPLES.md"
```

---

### Task 12: 端到端测试

**Files:**
- Create: `test_e2e.md`
- Create: `test_output.json`

**Interfaces:**
- Consumes: 所有脚本
- Produces: 完整的 JSON 输出

- [ ] **Step 1: 创建完整测试 MD**

```markdown
---
author: Tiger
source: /Users/tiger/Desktop/mess/程靖雯论文/V2/Shifting phosphorus pathways and cumulative policy effects in Erhai Lake basin A 30-year SFA–BSTS analysis (1992–2022).docx
output: /tmp/test_revised.docx
---

# Comments

Para 24: 方法论建议
此处列出的三项"进展"表述清晰但部分重叠...
> 选中范围: 第10-50字符

---

# Text Edits

Para 16: 标题修正
将 "grand challenge" 改为 "major challenge"

---

# Global Changes

将 "remains a major challenge for" 改为 "remains a challenge for"
```

- [ ] **Step 2: 运行转换**

```bash
python scripts/md_to_json.py test_e2e.md test_output.json
```

- [ ] **Step 3: 检查输出 JSON**

```bash
cat test_output.json | python -m json.tool
```

- [ ] **Step 4: 应用到 docx（可选）**

```python
import json
from scripts.docx_revision import ComprehensiveDocxReviewer

with open('test_output.json') as f:
    config = json.load(f)

reviewer = ComprehensiveDocxReviewer(config['source'])
reviewer.apply_json_config(config)
reviewer.save(config['output'])
```

- [ ] **Step 5: 清理和 Commit**

```bash
rm test_e2e.md test_output.json /tmp/test_revised.docx
git add -A
git commit -m "test: add end-to-end test"
```

---

### Task 13: 文档和 README

**Files:**
- Create: `README.md`

**Interfaces:**
- Consumes: 所有已完成的文件
- Produces: 项目 README

- [ ] **Step 1: 编写 README.md**

```markdown
# Docx Tracked Edits

AI 驱动的 docx 修订编辑工具。

## 快速开始

1. 查看段落结构: `python scripts/list_paragraphs.py paper.docx`
2. 生成 changes.md
3. 转换: `python scripts/md_to_json.py changes.md changes.json`
4. 应用到 docx

## 文档

- [SKILL.md](SKILL.md) - 主指令
- [REFERENCE.md](REFERENCE.md) - 语法参考
- [EXAMPLES.md](EXAMPLES.md) - 使用示例
```

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: add README.md"
```

---

### Task 14: 完善示例文档

**Files:**
- Modify: `EXAMPLES.md`

**Interfaces:**
- Consumes: 设计文档中的示例设计要求
- Produces: 完善后的 EXAMPLES.md

**Goal:** 将现有示例升级为完整的端到端演示，每个示例包含四个部分：
1. 原始文档内容
2. 生成的 Changes Markdown
3. 生成的 JSON
4. 最终文档效果

- [ ] **Step 1: 设计示例结构**

每个示例必须包含五个部分：

```markdown
## Example N: [场景名称]

### 原始文档

**Para 8:**
> The novel approach for flood monitoring method demonstrates significant improvements in accuracy compared to traditional techniques.

**Para 15:**
> As previously reported in our earlier studies, the results show significant correlation.

### 生成原始文档的代码

\```python
#!/usr/bin/env python3
"""生成 Example N 的原始 docx 文档"""
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

def create_original_doc():
    doc = Document()
    
    # Para 0: 标题
    title = doc.add_heading('Example N: Academic Paper', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Para 8: 需要修改的段落
    doc.add_paragraph(
        'The novel approach for flood monitoring method demonstrates '
        'significant improvements in accuracy compared to traditional techniques.'
    )
    
    # Para 15: 需要删除冗余的段落
    doc.add_paragraph(
        'As previously reported in our earlier studies, the results show '
        'significant correlation between the variables.'
    )
    
    # 保存
    doc.save('example_n_original.docx')
    print('✅ 已生成: example_n_original.docx')

if __name__ == '__main__':
    create_original_doc()
\```

### Changes Markdown

\```markdown
---
author: Tiger
source: example_n_original.docx
output: example_n_revised.docx
---

# Text Edits

Para 8: 修正术语
将 "novel" 改为 "improved"
将 "monitoring" 改为 "detection"

Para 15: 删除冗余
删除: "As previously reported in our earlier studies, "
\```

### 生成的 JSON

\```json
{
  "author": "Tiger",
  "source": "example_n_original.docx",
  "output": "example_n_revised.docx",
  "text_modifications": [
    {"type": "replace", "paragraph_index": 8, "old_text": "novel", "new_text": "improved"},
    {"type": "replace", "paragraph_index": 8, "old_text": "monitoring", "new_text": "detection"},
    {"type": "delete", "paragraph_index": 15, "text": "As previously reported in our earlier studies, "}
  ]
}
\```

### 应用修订的代码

\```python
#!/usr/bin/env python3
"""将修订应用到 Example N 的 docx 文档"""
import json
import sys
sys.path.insert(0, 'scripts')
from docx_revision import ComprehensiveDocxReviewer

def apply_changes():
    with open('example_n_changes.json') as f:
        config = json.load(f)
    
    reviewer = ComprehensiveDocxReviewer(config['source'])
    reviewer.apply_json_config(config)
    reviewer.save(config['output'])
    print(f'✅ 已生成修订文档: {config["output"]}')

if __name__ == '__main__':
    apply_changes()
\```

### 最终效果

**Para 8 (Revised):**
> The ~~novel~~ **improved** approach for flood ~~monitoring~~ **detection** method demonstrates significant improvements in accuracy compared to traditional techniques.

**Para 15 (Revised):**
> ~~As previously reported in our earlier studies,~~ the results show significant correlation.

**批注:**
> [T] 修正术语：novel → improved, monitoring → detection
```

### 目录结构

```
examples/
├── example_1_academic/
│   ├── create_original.py
│   ├── changes.md
│   ├── apply_changes.py
│   └── README.md
├── example_2_business/
│   ├── create_original.py
│   ├── changes.md
│   ├── apply_changes.py
│   └── README.md
├── example_3_legal/
│   ├── create_original.py
│   ├── changes.md
│   ├── apply_changes.py
│   └── README.md
├── example_4_complex/
│   ├── create_original.py
│   ├── changes.md
│   ├── apply_changes.py
│   └── README.md
└── run_all_examples.sh
```

### 完整运行流程

```bash
# 1. 生成原始文档
python examples/example_n/create_original.py

# 2. 转换 changes.md 到 JSON
python scripts/md_to_json.py examples/example_n/changes.md examples/example_n/changes.json

# 3. 应用修订
python examples/example_n/apply_changes.py

# 4. 查看结果
ls -la example_n_*.docx
```

- [ ] **Step 2: 重写 Example 1 (学术论文编辑)**

包含：
- 3-5 个段落的原始内容
- 体现极简原则的多个小替换
- 体现工具多样性的 delete + insert 组合
- 批注和格式修改
- 完整的 JSON 输出
- 最终效果展示

- [ ] **Step 3: 重写 Example 2 (商业报告)**

包含：
- 表格数据的原始内容
- 表格编辑（插入行、删除行、合并单元格）
- 数据更新的极简替换
- 完整的 JSON 输出

- [ ] **Step 4: 重写 Example 3 (法律文档)**

包含：
- 条款的原始内容
- 条款删除和插入
- 日期和金额的精确修改
- 完整的 JSON 输出

- [ ] **Step 5: 重写 Example 4 (多节复杂文档)**

包含：
- 多个节的原始内容
- 跨节的修改
- 样式修改
- 全局替换
- 完整的 JSON 输出

- [ ] **Step 6: 保留 Example 5-7 (简单示例)**

保留现有的简单示例作为快速参考，但添加说明：

```markdown
## Example 5: Minimal Single Edit (简单示例)

> **Note:** This is a simplified example for quick reference. See Examples 1-4 for complete end-to-end demonstrations.
```

- [ ] **Step 7: 更新 Example 8-10 (原则示例)**

更新现有的原则示例，添加完整的四部分结构：

```markdown
## Example 8: Minimalism Principle in Action (极简原则示例)

### 原始文档

**Para 15:**
> The novel approach for flood monitoring method demonstrates significant improvements in accuracy compared to traditional techniques.

### Changes Markdown

\```markdown
Para 15: 修正术语
将 "novel" 改为 "improved"
将 "monitoring" 改为 "detection"
将 "demonstrates" 改为 "shows"
\```

### 生成的 JSON

\```json
{
  "text_modifications": [
    {"type": "replace", "paragraph_index": 15, "old_text": "novel", "new_text": "improved"},
    {"type": "replace", "paragraph_index": 15, "old_text": "monitoring", "new_text": "detection"},
    {"type": "replace", "paragraph_index": 15, "old_text": "demonstrates", "new_text": "shows"}
  ]
}
\```

### 最终效果

**Para 15 (Revised):**
> The ~~novel~~ **improved** approach for flood ~~monitoring~~ **detection** method ~~demonstrates~~ **shows** significant improvements in accuracy compared to traditional techniques.
```

- [ ] **Step 8: 创建目录结构和运行脚本**

创建 examples 目录结构：

```bash
mkdir -p examples/example_1_academic
mkdir -p examples/example_2_business
mkdir -p examples/example_3_legal
mkdir -p examples/example_4_complex
```

创建 `examples/run_all_examples.sh`:

```bash
#!/bin/bash
# 运行所有示例

set -e

echo "🚀 运行所有示例..."

for dir in examples/example_*/; do
    echo ""
    echo "📁 运行示例: $dir"
    
    # 生成原始文档
    if [ -f "$dir/create_original.py" ]; then
        echo "  生成原始文档..."
        python "$dir/create_original.py"
    fi
    
    # 转换 changes.md 到 JSON
    if [ -f "$dir/changes.md" ]; then
        echo "  转换 changes.md 到 JSON..."
        python scripts/md_to_json.py "$dir/changes.md" "$dir/changes.json"
    fi
    
    # 应用修订
    if [ -f "$dir/apply_changes.py" ]; then
        echo "  应用修订..."
        python "$dir/apply_changes.py"
    fi
    
    echo "  ✅ 完成"
done

echo ""
echo "✅ 所有示例运行完成!"
echo ""
echo "生成的文件:"
ls -la examples/*/*.docx 2>/dev/null || echo "  (无 docx 文件)"
```

```bash
chmod +x examples/run_all_examples.sh
```

- [ ] **Step 9: 测试示例**

运行所有示例验证：

```bash
bash examples/run_all_examples.sh
```

验证：
1. 所有原始文档生成成功
2. 所有 changes.md 转换成功
3. 所有修订应用成功
4. 生成的 docx 文件可正常打开

- [ ] **Step 10: Commit**

```bash
git add examples/ EXAMPLES.md
git commit -m "docs: enhance examples with full end-to-end demonstrations"
```

---

**计划完成！**

执行选项：

1. **Subagent-Driven（推荐）** - 每个 task 派发一个子 agent，快速迭代
2. **Inline Execution** - 在当前会话中按顺序执行

选哪个？
