---
name: docx-tracked-edits
description: Edit docx files with tracked changes and comments using AI. Generates Markdown change specs that convert to docx_revision JSON format. Use when user wants to revise Word documents with tracked edits, add comments, or modify content with revision marks.
---

# Docx Tracked Edits

## Quick Start

1. **Read source docx** to understand paragraph structure
2. **Generate changes.md** using the template below
3. **Convert to JSON**: `python scripts/md_to_json.py changes.md changes.json`
4. **Apply to docx**: Use docx_revision package to generate revised document

## Changes Markdown Template

```markdown
---
author: Tiger
source: path/to/source.docx
output: path/to/output.docx
---

# Comments

## [P24] 方法论创新建议
此处列出的三项"进展"表述清晰但部分重叠——尤其是进展二与进展三均涉及政策解读层面。建议进一步明确区分：进展一聚焦方法论创新（SFA–BSTS整合），进展二聚焦政策归因（BSTS反事实分析），进展三聚焦管理启示。

## [P88] 数据说明
Long-term ambient TP concentration provides an independent water-quality reference.

---

# Changes

## [P16] Title fix
REPLACE: `grand challenge` → `major challenge`
REPLACE: `Erhai Lake Basin–a vulnerable` → `Erhai Lake Basin, a vulnerable`

## [P20] Example references
REPLACE: `like Lake Taihu` → `such as Lake Taihu`

## [P24] Abstract improvements
REPLACE: `advances ` → `makes `
REPLACE: `three transformative contributions` → `three analytical advances`

## [P58] MC validation note
APPEND: The convergence of the posterior probability of the local linear trend supports the validity of the MC approximation.

## [P83] Grammar fix
REPLACE: `A much clearer reduction after 2017` → `was observed after the 2017`

## [P139] Limitations expansion
REPLACE: `Several limitations should also be noted. First, the SFA framework` → `Several limitations should also be noted. First, while our BSTS model controls for observed covariates, unmeasured confounders may bias the estimated policy effects. In addition, the SFA framework`

---

# Global Changes

REPLACE: `remains a major challenge for` → `remains a challenge for`
REPLACE: `Results reveal a distinct` → `Results show a`
REPLACE: `This framework advances pathway-based` → `This framework supports pathway-based`
```

## Template Syntax

### Header (YAML frontmatter)
| Field | Required | Description |
|-------|----------|-------------|
| author | Yes | Default author for all changes |
| source | Yes | Path to source docx file |
| output | Yes | Path for output docx file |

### Comment Format
```markdown
## [P{paragraph_index}] {title}
{comment text}
```
- `P24` = paragraph index 24 (0-based)
- Title is for readability only, not used in output

### Change Formats

**Replace text:**
```markdown
REPLACE: `old text` → `new text`
```

**Insert text (append to paragraph):**
```markdown
APPEND: Text to insert at end of paragraph.
```

**Insert text at position:**
```markdown
INSERT@0: Text to insert at beginning.
```

**Delete text:**
```markdown
DELETE: `text to remove`
```

### Global Changes
Apply to entire document (auto-resolve paragraph index):
```markdown
# Global Changes
REPLACE: `old text` → `new text`
```

## Workflows

### 1. AI-Generated Edits

1. User provides docx file and editing instructions
2. AI reads docx to understand paragraph structure
3. AI generates `changes.md` following template
4. Run conversion: `python scripts/md_to_json.py changes.md changes.json`
5. Apply: Use docx_revision package

### 2. Manual Specification

1. User creates `changes.md` manually
2. Run conversion script
3. Review generated JSON
4. Apply to docx

### 3. Batch Processing

```bash
# Convert multiple files
for f in changes_*.md; do
  python scripts/md_to_json.py "$f" "${f%.md}.json"
done

# Apply each
for json in changes_*.json; do
  python -c "
import json
from docx_revision import ComprehensiveDocxReviewer
with open('$json') as f: cfg = json.load(f)
r = ComprehensiveDocxReviewer(cfg['source'])
r.apply_json_config(cfg)
r.save(cfg['output'])
"
done
```

## Scripts

- `scripts/md_to_json.py` - Convert Markdown to docx_revision JSON
- `scripts/validate_json.py` - Validate JSON against docx_revision schema

## Integration with docx_revision

```python
import json
from docx_revision import ComprehensiveDocxReviewer

# Load converted config
with open('changes.json') as f:
    config = json.load(f)

# Apply changes
reviewer = ComprehensiveDocxReviewer(config['source'])
reviewer.apply_json_config(config)
reviewer.save(config['output'])
```

## Common Patterns

### Academic Paper Review
```markdown
## [P15] Abstract clarity
REPLACE: `This framework advances` → `This framework supports`

## [P42] Methodology note
APPEND: These results should be interpreted with caution due to the limited sample size.
```

### Business Document Update
```markdown
## [P5] Q4 targets
REPLACE: `20% growth` → `25% growth`

## [P12] Deadline extension
INSERT@0: Updated: 
```

### Legal Contract Revision
```markdown
## [P8] Liability clause
DELETE: `notwithstanding any other provision`

## [P15] Term extension
REPLACE: `12 months` → `24 months`
```
