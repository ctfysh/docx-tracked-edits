---
name: docx-tracked-edits
description: "Edit docx files with tracked changes and comments using AI. Generates Markdown change specs that convert to docx_revision JSON format. Bilingual skill — prompts user to choose Chinese or English. Use when user wants to revise Word documents with tracked edits, add comments, or modify content with revision marks. Triggers: 'docx tracked edits', 'Word tracked changes', 'revision marks', 'docx 修订', 'Word 修订模式', '修订标记'."
---

# Docx Tracked Edits — Bilingual Skill / 双语技能

> AI-driven docx editing with tracked changes. Tell AI what to change in natural language, and get a Word document with revision marks automatically.
>
> **Core function: This skill does two things:**
> 1. **Parse template**: Read modification instructions in standard format
> 2. **Execute revision**: Apply changes to Word document

## Language Selection / 语言选择

**IMPORTANT — You MUST use the `question` tool to present the language choice as clickable options (tabs/buttons). Do NOT ask the user to type their answer.**

Use the `question` tool like this:
```
question(questions=[{
  "header": "Language / 语言",
  "question": "请问您希望用中文还是英文交流？/ Would you like to communicate in Chinese or English?",
  "options": [
    {"label": "中文", "description": "使用中文进行对话"},
    {"label": "English", "description": "Converse in English"}
  ]
}])
```

After the user selects a language, read the corresponding file:

- **中文** → Read `SKILL-zh.md` in the same directory. Converse in Chinese, using English for key terms as noted.
- **English** → Read `SKILL-en.md` in the same directory. Converse entirely in English.
- **No selection** → Default to `SKILL-zh.md` (中文).

Do NOT read both files. Load only the one matching the user's language choice.
