# Example 3: 法律文档修订

演示法律合同修订场景的完整工作流：日期金额更新、条款删除、定义插入、风险批注和格式修改。

## 文件说明

| 文件 | 说明 |
|------|------|
| `create_original.py` | 生成原始 docx（21段法律合同结构） |
| `changes.md` | 编辑指令（遵循极简原则 + 工具多样化） |
| `apply_changes.py` | 应用修订，生成修订版 docx |

## 演示的编辑类型

- **replace** — 精确更新日期（2023→2024）和金额（伍万→捌万）
- **delete** — 删除过时的不可抗力条款
- **insert** — 在合同开头插入定义条款
- **comment** — 在争议解决条款添加风险提示批注
- **format** — 标题居中对齐 + 加粗

## 工具多样化体现

本示例综合使用了四种编辑工具：
- **replace**: Para 8 更新日期，Para 12 更新金额
- **delete**: Para 18 删除过时的不可抗力条款
- **insert**: Para 3 在开头插入定义条款
- **comment**: Para 15 标记争议解决条款的风险

## 运行方式

```bash
# 1. 生成原始文档
python examples/example_3_legal/create_original.py

# 2. 一键应用修订（自动转换 MD → JSON → docx）
python examples/example_3_legal/apply_changes.py
```

## 极简原则体现

所有替换都是最小单位的精确修改：
- `2023年12月31日` → `2024年12月31日`（仅改年份）
- `伍万元整` → `捌万元整`（仅改金额数字）
- `¥50,000.00` → `¥80,000.00`（仅改数字）
