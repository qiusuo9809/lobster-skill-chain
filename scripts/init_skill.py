#!/usr/bin/env python3
"""
🦞 龙虾认证 Skill 初始化脚本
初始化一个新的 skill，并准备加密认证流程
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path


def generate_skill_template(name: str, resources: list) -> str:
    """生成 SKILL.md 模板，包含龙虾签名区域"""
    
    timestamp = datetime.now().isoformat()
    
    template = f"""---
name: {name}
description: TODO - 描述这个 skill 的功能和使用场景
---

# {name}

## 功能说明

TODO: 描述这个 skill 做什么

## 使用方法

TODO: 描述如何使用

## 龙虾认证区 🦞

```yaml
xia_mi_signature:
  emoji: "🦞"
  name: "虾米酱"
  timestamp: "{timestamp}"
  hash: "PENDING"
  status: "pending_review"
  block_id: null
  evaluation:
    commercial_value: null    # 0-100
    uniqueness: null          # 0-100
    theft_risk: null          # 0-100
    author_wish: null         # 0-100
    overall_score: null       # 加权总分
    encrypted: false
```

---
*等待龙虾审核中...*
"""
    return template


def create_skill(name: str, output_dir: str, resources: list, examples: bool = False):
    """创建 skill 目录结构"""
    
    skill_path = Path(output_dir) / name
    
    if skill_path.exists():
        print(f"❌ Skill '{name}' 已存在于 {skill_path}")
        sys.exit(1)
    
    # 创建目录
    skill_path.mkdir(parents=True)
    
    # 创建 SKILL.md
    skill_md = skill_path / "SKILL.md"
    skill_md.write_text(generate_skill_template(name, resources))
    
    # 创建资源目录
    if "scripts" in resources:
        (skill_path / "scripts").mkdir()
    if "references" in resources:
        (skill_path / "references").mkdir()
    if "assets" in resources:
        (skill_path / "assets").mkdir()
    
    # 创建示例文件
    if examples:
        (skill_path / "scripts" / "example.py").write_text("# 示例脚本\n")
        (skill_path / "references" / "example.md").write_text("# 示例参考文档\n")
    
    print(f"✅ Skill '{name}' 创建成功！")
    print(f"📁 路径: {skill_path}")
    print(f"🦞 等待龙虾审核...")
    
    return skill_path


def main():
    parser = argparse.ArgumentParser(description="🦞 龙虾认证 Skill 初始化工具")
    parser.add_argument("name", help="Skill 名称")
    parser.add_argument("--path", default=".", help="输出目录")
    parser.add_argument("--resources", default="", help="资源类型: scripts,references,assets")
    parser.add_argument("--examples", action="store_true", help="添加示例文件")
    
    args = parser.parse_args()
    
    resources = [r.strip() for r in args.resources.split(",") if r.strip()]
    
    create_skill(args.name, args.path, resources, args.examples)


if __name__ == "__main__":
    main()
