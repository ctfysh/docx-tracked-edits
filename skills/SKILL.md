---
name: docx-tracked-edits
description: Edit docx files with tracked changes and comments using AI. Generates Markdown change specs that convert to docx_revision JSON format. Use when user wants to revise Word documents with tracked edits, add comments, or modify content with revision marks.
---

# Docx Tracked Edits

## Language Detection

**Auto-detect user language and load the appropriate skill file:**

- If user's request is in **English** → Load `SKILL-en.md`
- If user's request is in **Chinese** → Load `SKILL-zh.md`
- If ambiguous → Ask user to choose: "Please specify language: English or 中文?"

## Core Function

**This skill does two things:**

1. **Parse template**: Read modification instructions in standard format
2. **Execute revision**: Apply changes to Word document

## Quick Start

1. **Review phase**: Other AI reads the document, identifies issues
2. **Template phase**: Other AI outputs issue list in this skill's template format
3. **Execution phase**: This skill parses the template, applies changes
4. **Result phase**: User receives the revised document

**Key: This skill defines the standard template format for modification instructions. Other AI tools must output in this format for this skill to parse and execute.**
