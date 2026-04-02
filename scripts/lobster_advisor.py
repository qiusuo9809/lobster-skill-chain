#!/usr/bin/env python3
"""
🦞 龙虾顾问脚本
只给评分和建议，加密决策交给开发者
"""

import argparse
import sys
from pathlib import Path

from evaluate_skill import evaluate_skill


def lobster_advice(skill_path: Path):
    """
    🦞 龙虾给出评分和建议
    不自动执行任何操作
    """
    
    print(f"\n🦞 ========== 龙虾 Skill 顾问 ==========")
    print(f"Skill: {skill_path.name}")
    print("=" * 50)
    
    # 自动评估
    print("\n📊 龙虾评估中...")
    evaluation = evaluate_skill(skill_path)
    
    score = evaluation['overall_score']
    
    # 显示评分
    print(f"\n📈 四维评分:")
    print(f"   商业价值: {evaluation['commercial_value']}/100")
    print(f"   独特性:   {evaluation['uniqueness']}/100") 
    print(f"   被窃风险: {evaluation['theft_risk']}/100")
    print(f"   作者意愿: {evaluation['author_wish']}/100")
    print(f"   ─────────────────────")
    print(f"   综合评分: {score:.1f}/100")
    
    print(f"\n📝 评估理由:")
    for reason in evaluation["reasoning"]:
        print(f"   • {reason}")
    
    # 龙虾建议
    print(f"\n🦞 龙虾的建议:")
    print("-" * 50)
    
    if score >= 80:
        print("   🔒 强烈建议加密")
        print("   💡 理由: 这个 skill 很有价值，被复制的风险较高。")
        print("   💡 建议: 使用 AES 加密保护，添加数字签名。")
    elif score >= 50:
        print("   ⚠️  建议加密")
        print("   💡 理由: 这个 skill 有一定价值，但风险中等。")
        print("   💡 建议: 如果包含敏感逻辑，建议加密保护。")
    else:
        print("   ✓ 可选加密")
        print("   💡 理由: 这个 skill 加密意义不大，或风险较低。")
        print("   💡 建议: 可以只添加龙虾签名，不加密。")
    
    # 下一步建议
    print(f"\n📋 下一步操作建议:")
    print("-" * 50)
    print(f"   1. 查看评分详情:")
    print(f"      已显示在上文")
    print(f"")
    print(f"   2. 如果决定加密:")
    print(f"      python encrypt_skill.py encrypt {skill_path}")
    print(f"")
    print(f"   3. 添加龙虾签名:")
    print(f"      python evaluate_skill.py {skill_path} --block-id N --apply")
    print(f"")
    print(f"   4. 打包输出:")
    print(f"      python package_skill.py {skill_path} ./dist")
    print(f"")
    print(f"   5. 添加到区块链:")
    print(f"      python add_to_chain.py --add {skill_path}")
    
    print(f"\n🦞 ========== 顾问服务完成 ==========")
    print(f"💬 龙虾只是建议，最终决策权在你！")
    
    return evaluation


def main():
    parser = argparse.ArgumentParser(description="🦞 龙虾顾问 - 只给建议，不自动执行")
    parser.add_argument("skill_path", help="Skill 目录路径")
    
    args = parser.parse_args()
    
    skill_path = Path(args.skill_path)
    
    if not skill_path.exists():
        print(f"❌ Skill 不存在: {skill_path}")
        sys.exit(1)
    
    lobster_advice(skill_path)


if __name__ == "__main__":
    main()
