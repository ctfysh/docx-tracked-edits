---
name: docx-tracked-edits
description: Edit docx files with tracked changes and comments using AI. Generates Markdown change specs that convert to docx_revision JSON format. Use when user wants to revise Word documents with tracked edits, add comments, or modify content with revision marks.
---

# Docx Tracked Edits

## Language Detection

**Auto-detect user language and load the appropriate skill file:**

- If user's request is in **English** → Load `skills/SKILL-en.md`
- If user's request is in **Chinese** → Load `skills/SKILL-zh.md`
- If ambiguous → Ask user to choose: "Please specify language: English or 中文?"
