# Docx Tracked Edits Examples

## Working Examples

The `examples/` directory contains complete working demos with Python code:

| Example | Description | Directory |
|---------|-------------|-----------|
| Academic Paper | Fix terminology, remove redundancy, correct typos | [examples/example_1_academic/](examples/example_1_academic/) |
| Business Report | Update dates, amounts, modify tables | [examples/example_2_business/](examples/example_2_business/) |
| Legal Document | Update contract dates, add definitions, flag risks | [examples/example_3_legal/](examples/example_3_legal/) |
| Complex Document | All edit types - text, table, format, style, global | [examples/example_4_complex/](examples/example_4_complex/) |

### Running Examples

```bash
# Run all examples
bash examples/run_all_examples.sh

# Or run individual examples
cd examples/example_1_academic
python create_original.py      # Generate original docx
python apply_changes.py        # Apply changes
```

### Each Example Contains

- `create_original.py` - Generate original docx
- `changes.md` - Changes specification
- `apply_changes.py` - Apply changes pipeline
- `README.md` - Description

## Quick Syntax Reference

For simplified syntax-only examples (no Python code), see [QUICK_REFERENCE.md](QUICK_REFERENCE.md).

## Full Workflow

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