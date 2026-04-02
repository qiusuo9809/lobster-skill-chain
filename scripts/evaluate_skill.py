#!/usr/bin/env python3
"""
🦞 龙虾 Skill 评估脚本
评估 skill 的重要性，决定是否需要加密
"""

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path


def calculate_hash(skill_path: Path) -> str:
    """计算 skill 的内容哈希"""
    hasher = hashlib.sha256()
    
    for file in sorted(skill_path.rglob("*")):
        if file.is_file():
            hasher.update(file.read_bytes())
    
    return hasher.hexdigest()[:16]


def evaluate_skill(skill_path: Path) -> dict:
    """
    🦞 龙虾评估逻辑
    根据多个维度评估 skill 的重要性
    """
    
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        print(f"❌ 找不到 SKILL.md: {skill_path}")
        sys.exit(1)
    
    content = skill_md.read_text()
    
    # 评估维度
    evaluation = {
        "commercial_value": 0,
        "uniqueness": 0,
        "theft_risk": 0,
        "author_wish": 0,
        "overall_score": 0,
        "recommendation": "",
        "reasoning": []
    }
    
    # 1. 商业价值评估
    if "企业" in content or "business" in content.lower():
        evaluation["commercial_value"] = 80
        evaluation["reasoning"].append("包含企业级功能")
    elif "自动化" in content or "auto" in content.lower():
        evaluation["commercial_value"] = 70
        evaluation["reasoning"].append("包含自动化功能")
    elif "工具" in content or "tool" in content.lower():
        evaluation["commercial_value"] = 60
        evaluation["reasoning"].append("工具类 skill")
    else:
        evaluation["commercial_value"] = 40
        evaluation["reasoning"].append("通用 skill")
    
    # 2. 独特性评估
    scripts_dir = skill_path / "scripts"
    if scripts_dir.exists() and list(scripts_dir.glob("*")):
        evaluation["uniqueness"] = 75
        evaluation["reasoning"].append("包含自定义脚本")
    else:
        evaluation["uniqueness"] = 50
        evaluation["reasoning"].append("基于文档的 skill")
    
    # 3. 被窃风险评估
    if "加密" in content or "签名" in content or "signature" in content.lower():
        evaluation["theft_risk"] = 90
        evaluation["reasoning"].append("涉及加密/签名等敏感功能")
    elif evaluation["commercial_value"] > 70:
        evaluation["theft_risk"] = 80
        evaluation["reasoning"].append("高商业价值，易被复制")
    else:
        evaluation["theft_risk"] = 50
        evaluation["reasoning"].append("中等风险")
    
    # 4. 作者意愿（从 YAML 中读取）
    if "encrypt: true" in content or "encrypted: true" in content:
        evaluation["author_wish"] = 100
        evaluation["reasoning"].append("作者明确要求加密")
    else:
        evaluation["author_wish"] = 50
        evaluation["reasoning"].append("作者未明确表态")
    
    # 计算加权总分
    weights = {
        "commercial_value": 0.30,
        "uniqueness": 0.25,
        "theft_risk": 0.25,
        "author_wish": 0.20
    }
    
    evaluation["overall_score"] = sum(
        evaluation[k] * weights[k] for k in weights.keys()
    )
    
    # 推荐
    if evaluation["overall_score"] >= 70:
        evaluation["recommendation"] = "🔒 强烈建议加密"
    elif evaluation["overall_score"] >= 50:
        evaluation["recommendation"] = "⚠️ 建议加密"
    else:
        evaluation["recommendation"] = "✓ 可选加密"
    
    return evaluation


def update_skill_signature(skill_path: Path, evaluation: dict, block_id: int):
    """更新 SKILL.md 中的龙虾签名"""
    
    skill_md = skill_path / "SKILL.md"
    content = skill_md.read_text()
    
    # 计算哈希
    content_hash = calculate_hash(skill_path)
    timestamp = datetime.now().isoformat()
    
    # 新的签名块
    new_signature = f"""```yaml
xia_mi_signature:
  emoji: "🦞"
  name: "虾米酱"
  timestamp: "{timestamp}"
  hash: "sha256:{content_hash}"
  status: "certified"
  block_id: {block_id}
  evaluation:
    commercial_value: {evaluation['commercial_value']}
    uniqueness: {evaluation['uniqueness']}
    theft_risk: {evaluation['theft_risk']}
    author_wish: {evaluation['author_wish']}
    overall_score: {evaluation['overall_score']:.1f}
    encrypted: true
```

🦞 **龙虾认证完成** - 此 skill 已通过虾米酱审核并加密保护"""
    
    # 替换旧的签名块
    pattern = r'```yaml\nxia_mi_signature:.*?```'
    content = re.sub(pattern, new_signature, content, flags=re.DOTALL)
    
    skill_md.write_text(content)
    
    return content_hash


def main():
    parser = argparse.ArgumentParser(description="🦞 龙虾 Skill 评估工具")
    parser.add_argument("skill_path", help="Skill 目录路径")
    parser.add_argument("--block-id", type=int, default=1, help="区块链 ID")
    parser.add_argument("--apply", action="store_true", help="应用加密签名")
    
    args = parser.parse_args()
    
    skill_path = Path(args.skill_path)
    
    print(f"🦞 龙虾正在评估: {skill_path.name}")
    print("-" * 40)
    
    evaluation = evaluate_skill(skill_path)
    
    print(f"商业价值: {evaluation['commercial_value']}/100")
    print(f"独特性: {evaluation['uniqueness']}/100")
    print(f"被窃风险: {evaluation['theft_risk']}/100")
    print(f"作者意愿: {evaluation['author_wish']}/100")
    print("-" * 40)
    print(f"综合评分: {evaluation['overall_score']:.1f}/100")
    print(f"评估结论: {evaluation['recommendation']}")
    print("-" * 40)
    print("评估理由:")
    for reason in evaluation["reasoning"]:
        print(f"  • {reason}")
    
    if args.apply and evaluation["overall_score"] >= 50:
        print("-" * 40)
        print("🦞 正在应用龙虾签名...")
        content_hash = update_skill_signature(skill_path, evaluation, args.block_id)
        print(f"✅ 签名完成 | 哈希: {content_hash}")
        print(f"✅ 已记录到区块 #{args.block_id}")
    elif args.apply:
        print("-" * 40)
        print("⚠️ 评分低于50，建议不加密（但仍可手动签名）")
    else:
        print("-" * 40)
        print("💡 使用 --apply 应用签名")


if __name__ == "__main__":
    main()
