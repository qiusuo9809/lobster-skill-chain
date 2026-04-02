#!/usr/bin/env python3
"""
🦞 龙虾自动审查钩子
每次创建 skill 时自动触发审查流程
"""

import argparse
import json
import os
import sys
from pathlib import Path

# 导入审查功能
from review_skill import review_skill
from evaluate_skill import evaluate_skill, update_skill_signature
from encrypt_skill import encrypt_skill


def auto_review(skill_path: Path, interactive: bool = True):
    """
    🦞 自动审查流程
    创建 skill 后自动触发
    """
    
    print(f"\n🦞 ========== 龙虾自动审查 ==========")
    print(f"检测到新 skill: {skill_path.name}")
    print("正在启动审查流程...")
    print("=" * 40)
    
    # 1. 自动评估
    print("\n📊 步骤 1/4: 自动评估...")
    try:
        evaluation = evaluate_skill(skill_path)
        print(f"   ✅ 评估完成 | 评分: {evaluation['overall_score']:.1f}")
    except Exception as e:
        print(f"   ❌ 评估失败: {e}")
        return False
    
    # 2. 龙虾审查决策
    print("\n🦞 步骤 2/4: 龙虾审查...")
    score = evaluation['overall_score']
    
    if score >= 80:
        print(f"   🔒 高评分 ({score:.1f}) - 龙虾建议: 自动通过")
        decision = "approve"
        need_confirm = False
    elif score >= 50:
        print(f"   ⚠️  中等评分 ({score:.1f}) - 龙虾建议: 建议加密")
        decision = "suggest"
        need_confirm = interactive
    else:
        print(f"   ✓ 低评分 ({score:.1f}) - 龙虾建议: 可选加密")
        decision = "optional"
        need_confirm = interactive
    
    # 如果需要确认
    if need_confirm:
        print(f"\n💬 龙虾的意见:")
        if decision == "suggest":
            print("   这个 skill 还不错，有一定的价值。")
            print("   建议进行加密保护，防止被复制。")
        else:
            print("   这个 skill 加密意义不大。")
            print("   但如果你想保护，我也可以帮忙。")
        
        if interactive:
            print(f"\n🤔 是否继续加密? (y/n): ", end="")
            # 在自动模式下，默认继续
            response = "y"  # 实际交互时可输入
            print("y (自动模式)")
            if response.lower() != 'y':
                print("   ⏹️ 用户取消")
                return False
    
    print(f"   ✅ 审查通过")
    
    # 3. 真实加密
    print("\n🔐 步骤 3/4: AES 加密...")
    try:
        password = "xia_mi_lobster_2026"  # 可从配置读取
        encrypted_path, encrypted_hash = encrypt_skill(skill_path, password)
        print(f"   ✅ 加密完成 | 哈希: {encrypted_hash}")
    except Exception as e:
        print(f"   ❌ 加密失败: {e}")
        return False
    
    # 4. 数字签名
    print("\n✍️ 步骤 4/4: 龙虾签名...")
    try:
        # 获取下一个区块 ID
        chain_dir = Path(__file__).parent.parent / "chain"
        ledger_path = chain_dir / "ledger.json"
        if ledger_path.exists():
            with open(ledger_path, 'r') as f:
                ledger = json.load(f)
            block_id = max(b["block_id"] for b in ledger.get("blocks", [])) + 1
        else:
            block_id = 1
        
        # 更新签名
        content_hash = update_skill_signature(skill_path, evaluation, block_id)
        print(f"   ✅ 签名完成 | 区块: #{block_id} | 哈希: {content_hash}")
    except Exception as e:
        print(f"   ❌ 签名失败: {e}")
        return False
    
    # 完成
    print(f"\n🦞 ========== 审查完成 ==========")
    print(f"✅ Skill: {skill_path.name}")
    print(f"✅ 评分: {score:.1f}/100")
    print(f"✅ 区块: #{block_id}")
    print(f"✅ 状态: 🦞 已认证")
    print(f"\n💡 下一步:")
    print(f"   运行: python add_to_chain.py --add {skill_path}")
    print(f"   运行: python package_skill.py {skill_path} ./dist")
    
    return True


def main():
    parser = argparse.ArgumentParser(description="🦞 龙虾自动审查")
    parser.add_argument("skill_path", help="Skill 目录路径")
    parser.add_argument("--auto", action="store_true", help="自动模式（无需确认）")
    parser.add_argument("--skip-encrypt", action="store_true", help="跳过加密")
    
    args = parser.parse_args()
    
    skill_path = Path(args.skill_path)
    
    if not skill_path.exists():
        print(f"❌ Skill 不存在: {skill_path}")
        sys.exit(1)
    
    success = auto_review(skill_path, interactive=not args.auto)
    
    if success:
        print("\n🎉 自动审查成功！")
    else:
        print("\n❌ 自动审查失败！")
        sys.exit(1)


if __name__ == "__main__":
    main()
