# Docx Tracked Edits Skill 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 创建一个 OpenCode skill，通过 AI 生成的 Markdown 文件编辑 docx 文档，支持修订模式和批注。

**Architecture:** 单文件 skill，捆绑 docx_revision 包。包含 SKILL.md 主指令、list_paragraphs.py 段落查看器、md_to_json.py 转换脚本。

**Tech Stack:** Python, python-docx, PyYAML

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

**计划完成！**

执行选项：

1. **Subagent-Driven（推荐）** - 每个 task 派发一个子 agent，快速迭代
2. **Inline Execution** - 在当前会话中按顺序执行

选哪个？
