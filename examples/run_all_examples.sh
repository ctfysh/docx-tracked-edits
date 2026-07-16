#!/bin/bash
# Run all examples for docx-tracked-edits

set -e

echo "🚀 运行所有示例..."
echo ""

# Get the script's directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

for dir in "$SCRIPT_DIR"/example_*/; do
    if [ -d "$dir" ]; then
        example_name=$(basename "$dir")
        echo "📁 运行示例: $example_name"
        
        cd "$dir"
        
        # Generate original document
        if [ -f "create_original.py" ]; then
            echo "  生成原始文档..."
            python create_original.py
        fi
        
        # Convert changes.md to JSON
        if [ -f "changes.md" ]; then
            echo "  转换 changes.md 到 JSON..."
            python "$PROJECT_DIR/scripts/md_to_json.py" changes.md changes.json
        fi
        
        # Apply changes
        if [ -f "apply_changes.py" ]; then
            echo "  应用修订..."
            python apply_changes.py
        fi
        
        echo "  ✅ 完成"
        echo ""
    fi
done

echo "✅ 所有示例运行完成!"
echo ""
echo "生成的文件:"
echo "  原始文档:"
ls -la "$SCRIPT_DIR"/example_*/*_original.docx 2>/dev/null || echo "    (无原始文档)"
echo ""
echo "  修订文档:"
ls -la "$SCRIPT_DIR"/example_*/*_revised.docx 2>/dev/null || echo "    (无修订文档)"
