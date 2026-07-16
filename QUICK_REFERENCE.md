# Quick Reference

## Minimal Single Edit

```markdown
---
author: Editor
source: letter.docx
output: letter_revised.docx
---

# Text Edits

Para 0: Fix greeting
Replace "Dear Sir" with "Dear Colleague"
```

## Formatting-Only Document

```markdown
---
author: Designer
source: brochure.docx
output: brochure_revised.docx
---

# Format Edits

Para 0: Cover title
Center align, Font size 28pt, Bold, Font SimHei

Para 1: Subtitle
Center align, Font size 16pt, Font SimSun

Para 3-8: Body text
Justify, Line spacing 1.8, Left indent 36pt, Right indent 36pt

Para 10: Footnote
Font size 9pt, Italic

# Style Edits

Heading1 style:
  Font size 20pt, Bold, Font SimHei

Heading2 style:
  Font size 14pt, Font SimHei

Normal style:
  Font SimSun, Font size 10.5pt, Line spacing 1.5
```

## Table-Heavy Document

```markdown
---
author: Analyst
source: data_report.docx
output: data_report_revised.docx
---

# Text Edits

Para 5: Fix summary
Replace "Total Revenue" with "Net Income"

Para 12: Update time range
Replace "January to June 2023" with "January to June 2024"

# Table Edits

Table 0: Quarterly data
Insert row after row 4
Delete row 2

Table 1: Regional comparison
Merge columns A-C in row 1
Merge 3 cells in row 2

Table 2: Product details
Insert row after row 6
Delete row 8
Merge columns 2-4 in row 1

# Format Edits

Para 3: Table title
Center align, Font size 11pt, Bold

# Style Edits

Normal style:
  Font Arial, Font size 10pt
```

## Minimalism Principle Example

**Original paragraph (Para 15):**
> The novel approach for flood monitoring method demonstrates significant improvements in accuracy compared to traditional techniques.

**Wrong approach ❌ (replacing entire sentence):**
```markdown
Para 15: Fix terminology
Replace "The novel approach for flood monitoring method demonstrates significant improvements in accuracy compared to traditional techniques." with "The improved method for flood detection shows enhanced accuracy compared to traditional approaches."
```

**Right approach ✅ (minimal changes):**
```markdown
Para 15: Fix terminology
Replace "novel" with "improved"
Replace "monitoring" with "detection"
Replace "demonstrates" with "shows"
Replace "significant improvements" with "enhanced accuracy"
Replace "techniques" with "approaches"
```

## Tool Diversity Example

**Original paragraph (Para 23):**
> As previously reported in our earlier studies, the results show significant correlation.

**Wrong approach ❌ (using only replace):**
```markdown
Para 23: Edit
Replace "As previously reported in our earlier studies, " with ""
Replace "show significant" with "demonstrate statistically significant"
```

**Right approach ✅ (using delete + insert + replace):**
```markdown
Para 23: Edit
Delete: "As previously reported in our earlier studies, "
Replace "show significant" with "demonstrate statistically significant"
Insert at end: (p < 0.05)
```

## Position-Aware Editing

**Original paragraph (Para 8):**
> The the results show that the the effect is significant.

**Wrong approach ❌ (ambiguous):**
```markdown
Para 8: Fix repetition
Delete: "the"
```

**Right approach ✅ (with position):**
```markdown
Para 8: Fix repetition
Delete: "the" (chars 4-7)
Delete: "the" (chars 18-21)
```

**Position rules:**
1. Use when same text appears multiple times in a paragraph
2. Format: `(chars {start}-{end})` — 0-indexed, inclusive
3. Count characters from beginning of paragraph