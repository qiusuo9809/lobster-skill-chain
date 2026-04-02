#!/usr/bin/env python3
"""
🦞 龙虾 Skill 人工审查脚本
自动评估 + 龙虾确认机制
"""

import argparse
import sys
from pathlib import Path

# 导入评估函数
from evaluate_skill import evaluate_skill


def review_skill(skill_path: Path, block_id: int = None):
    """
    🦞 龙虾审查流程
    1. 自动评估
    2. 龙虾确认
    3. 执行签名
    """
    
    print(f"\n🦞 ========== 龙虾 Skill 审查 ==========")
    print(f"正在审查: {skill_path.name}")
    print("=" * 40)
    
    # 1. 自动评估
    evaluation = evaluate_skill(skill_path)
    
    print(f"\n📊 自动评估结果:")
    print(f"   商业价值: {evaluation['commercial_value']}/100")
    print(f"   独特性:   {evaluation['uniqueness']}/100")
    print(f"   被窃风险: {evaluation['theft_risk']}/100")
    print(f"   作者意愿: {evaluation['author_wish']}/100")
    print(f"   ─────────────────────")
    print(f"   综合评分: {evaluation['overall_score']:.1f}/100")
    print(f"   评估结论: {evaluation['recommendation']}")
    
    print(f"\n📝 评估理由:")
    for reason in evaluation["reasoning"]:
        print(f"   • {reason}")
    
    # 2. 龙虾人工确认
    print(f"\n🦞 ========== 龙虾确认环节 ==========")
    
    if evaluation["overall_score"] >= 80:
        print("✅ 高评分 skill，龙虾建议：自动通过")
        suggestion = "auto_approve"
    elif evaluation["overall_score"] >= 50:
        print("⚠️  中等评分 skill，龙虾建议：人工确认")
        suggestion = "manual_review"
    else:
        print("❓ 低评分 skill，龙虾建议：可选加密")
        suggestion = "optional"
    
    # 交互式确认
    print(f"\n💬 龙虾的意见:")
    if suggestion == "auto_approve":
        print("   这个 skill 很有价值，建议加密保护！")
    elif suggestion == "manual_review":
        print("   这个 skill 还不错，但让我再想想...")
    else:
        print("   这个 skill 加密意义不大，但如果你想保护也可以。")
    
    # 返回评估结果，等待调用者决定
    return {
        "evaluation": evaluation,
        "suggestion": suggestion,
        "skill_path": skill_path,
        "block_id": block_id
    }


def main():
    parser = argparse.ArgumentParser(description="🦞 龙虾 Skill 审查工具")
    parser.add_argument("skill_path", help="Skill 目录路径")
    parser.add_argument("--block-id", type=int, help="区块 ID")
    
    args = parser.parse_args()
    
    skill_path = Path(args.skill_path)
    result = review_skill(skill_path, args.block_id)
    
    print(f"\n🦞 ========== 审查完成 ==========")
    print(f"评分: {result['evaluation']['overall_score']:.1f}")
    print(f"建议: {result['suggestion']}")
    print(f"\n下一步:")
    print(f"   运行: python evaluate_skill.py {skill_path} --block-id {args.block_id or 'N'} --apply")


if __name__ == "__main__":
    main()
