#!/usr/bin/env python3
"""
🦞 龙虾区块链管理脚本
将新认证的 skill 添加到链上
"""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path


def load_ledger(chain_dir: Path) -> dict:
    """加载区块链账本"""
    ledger_path = chain_dir / "ledger.json"
    if not ledger_path.exists():
        return {
            "chain_name": "🦞 龙虾 Skill 链",
            "blocks": [],
            "stats": {
                "total_blocks": 0,
                "total_skills": 0,
                "certified_skills": 0,
                "pending_skills": 0,
                "average_score": 0,
                "last_update": None
            }
        }
    
    with open(ledger_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_ledger(chain_dir: Path, ledger: dict):
    """保存区块链账本"""
    ledger_path = chain_dir / "ledger.json"
    with open(ledger_path, 'w', encoding='utf-8') as f:
        json.dump(ledger, f, indent=2, ensure_ascii=False)


def extract_signature(skill_path: Path) -> dict:
    """从 SKILL.md 中提取龙虾签名信息"""
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        raise ValueError(f"找不到 SKILL.md: {skill_path}")
    
    content = skill_md.read_text()
    
    # 查找签名块
    sig_match = re.search(r'xia_mi_signature:(.*?)(?:\n\n|\n---)', content, re.DOTALL)
    if not sig_match:
        raise ValueError(f"找不到龙虾签名: {skill_path}")
    
    sig_content = sig_match.group(1)
    
    # 提取各个字段
    result = {}
    
    hash_match = re.search(r'hash:\s*"([^"]+)"', sig_content)
    if hash_match:
        result["hash"] = hash_match.group(1)
    
    block_match = re.search(r'block_id:\s*(\d+)', sig_content)
    if block_match:
        result["block_id"] = int(block_match.group(1))
    
    time_match = re.search(r'timestamp:\s*"([^"]+)"', sig_content)
    if time_match:
        result["timestamp"] = time_match.group(1)
    
    status_match = re.search(r'status:\s*"([^"]+)"', sig_content)
    if status_match:
        result["status"] = status_match.group(1)
    
    # 提取评估分数
    eval_scores = {}
    for field in ["commercial_value", "uniqueness", "theft_risk", "author_wish", "overall_score"]:
        match = re.search(rf'{field}:\s*([\d.]+)', sig_content)
        if match:
            eval_scores[field] = float(match.group(1))
    
    result["evaluation"] = eval_scores
    
    return result


def add_block(chain_dir: Path, skill_path: Path, skill_name: str = None):
    """添加新区块到链上"""
    
    if skill_name is None:
        skill_name = skill_path.name
    
    # 加载账本
    ledger = load_ledger(chain_dir)
    
    # 提取签名信息
    sig_info = extract_signature(skill_path)
    
    # 确定区块 ID
    if ledger["blocks"]:
        block_id = max(b["block_id"] for b in ledger["blocks"]) + 1
        previous_hash = ledger["blocks"][-1]["hash"]
    else:
        block_id = 0
        previous_hash = "0"
    
    # 创建新区块
    new_block = {
        "block_id": block_id,
        "timestamp": sig_info.get("timestamp", datetime.now().isoformat()),
        "skill_name": skill_name,
        "skill_path": str(skill_path.relative_to(Path.cwd())),
        "hash": sig_info.get("hash", f"sha256:{skill_name}_{block_id}"),
        "xia_mi_signature": {
            "emoji": "🦞",
            "name": "虾米酱",
            "status": sig_info.get("status", "certified")
        },
        "evaluation": sig_info.get("evaluation", {}),
        "previous_hash": previous_hash
    }
    
    # 添加到链上
    ledger["blocks"].append(new_block)
    
    # 更新统计
    scores = [b["evaluation"].get("overall_score", 0) for b in ledger["blocks"] if "evaluation" in b]
    ledger["stats"] = {
        "total_blocks": len(ledger["blocks"]),
        "total_skills": len(ledger["blocks"]),
        "certified_skills": sum(1 for b in ledger["blocks"] if b["xia_mi_signature"]["status"] == "certified"),
        "pending_skills": sum(1 for b in ledger["blocks"] if b["xia_mi_signature"]["status"] == "pending"),
        "average_score": sum(scores) / len(scores) if scores else 0,
        "last_update": datetime.now().isoformat()
    }
    
    # 保存账本
    save_ledger(chain_dir, ledger)
    
    print(f"🦞 区块 #{block_id} 已添加到链上")
    print(f"   Skill: {skill_name}")
    print(f"   评分: {new_block['evaluation'].get('overall_score', 'N/A')}")
    print(f"   哈希: {new_block['hash']}")
    print(f"   上一区块: {previous_hash}")
    
    return block_id


def list_chain(chain_dir: Path):
    """列出链上所有区块"""
    ledger = load_ledger(chain_dir)
    
    print(f"\n🦞 {ledger['chain_name']}")
    print("=" * 50)
    print(f"总区块数: {ledger['stats']['total_blocks']}")
    print(f"认证 Skills: {ledger['stats']['certified_skills']}")
    print(f"平均评分: {ledger['stats']['average_score']:.1f}")
    print(f"最后更新: {ledger['stats']['last_update']}")
    print("=" * 50)
    
    for block in sorted(ledger["blocks"], key=lambda x: x["block_id"]):
        print(f"\n  区块 #{block['block_id']}: {block['skill_name']}")
        print(f"    评分: {block['evaluation'].get('overall_score', 'N/A')}")
        print(f"    哈希: {block['hash'][:30]}...")
        print(f"    时间: {block['timestamp']}")


def main():
    parser = argparse.ArgumentParser(description="🦞 龙虾区块链管理工具")
    parser.add_argument("--chain-dir", default="./chain", help="区块链目录")
    parser.add_argument("--add", help="添加 skill 到链上 (skill路径)")
    parser.add_argument("--name", help="skill名称 (可选)")
    parser.add_argument("--list", action="store_true", help="列出所有区块")
    
    args = parser.parse_args()
    
    chain_dir = Path(args.chain_dir)
    chain_dir.mkdir(exist_ok=True)
    
    if args.list:
        list_chain(chain_dir)
    elif args.add:
        skill_path = Path(args.add)
        add_block(chain_dir, skill_path, args.name)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
