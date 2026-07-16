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
    
    if 'Comments' in sections:
        config["comments"] = parse_comments(sections['Comments'])
    
    json_path.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"✅ 已生成: {json_path}")

if __name__ == '__main__':
    main()
