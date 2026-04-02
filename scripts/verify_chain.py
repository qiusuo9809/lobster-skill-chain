#!/usr/bin/env python3
"""
🦞 龙虾区块链验证脚本
验证区块链的完整性和一致性
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path


def calculate_block_hash(block: dict) -> str:
    """计算区块的哈希"""
    # 提取关键字段计算哈希
    data = {
        "block_id": block["block_id"],
        "timestamp": block["timestamp"],
        "skill_name": block["skill_name"],
        "skill_path": block["skill_path"],
        "previous_hash": block["previous_hash"],
        "evaluation": block.get("evaluation", {})
    }
    
    hasher = hashlib.sha256()
    hasher.update(json.dumps(data, sort_keys=True).encode())
    return hasher.hexdigest()[:16]


def verify_chain(chain_dir: Path) -> dict:
    """验证整个区块链"""
    
    ledger_path = chain_dir / "ledger.json"
    if not ledger_path.exists():
        return {"valid": False, "error": "找不到账本文件"}
    
    with open(ledger_path, 'r') as f:
        ledger = json.load(f)
    
    blocks = ledger.get("blocks", [])
    if not blocks:
        return {"valid": False, "error": "区块链为空"}
    
    errors = []
    warnings = []
    
    print(f"🦞 ========== 区块链验证 ==========")
    print(f"总区块数: {len(blocks)}")
    print(f"链名称: {ledger.get('chain_name', 'N/A')}")
    print("=" * 40)
    
    # 验证每个区块
    for i, block in enumerate(blocks):
        block_id = block.get("block_id", i)
        print(f"\n验证区块 #{block_id}...")
        
        # 1. 检查区块 ID 连续性
        if block_id != i:
            errors.append(f"区块 #{block_id}: ID 不连续 (期望 {i})")
        
        # 2. 验证哈希链
        if i == 0:
            # 创世区块
            if block.get("previous_hash") != "0":
                errors.append(f"区块 #{block_id}: 创世区块 previous_hash 应为 '0'")
        else:
            # 普通区块
            prev_block = blocks[i - 1]
            expected_hash = prev_block.get("hash", "")
            actual_hash = block.get("previous_hash", "")
            
            if expected_hash and actual_hash != expected_hash:
                errors.append(f"区块 #{block_id}: 哈希链断裂 (期望 {expected_hash[:16]}..., 实际 {actual_hash[:16]}...)")
        
        # 3. 验证签名状态
        sig = block.get("xia_mi_signature", {})
        if sig.get("status") != "certified":
            warnings.append(f"区块 #{block_id}: 未认证 (状态: {sig.get('status')})")
        
        # 4. 验证龙虾印记
        if sig.get("emoji") != "🦞" or sig.get("name") != "虾米酱":
            errors.append(f"区块 #{block_id}: 龙虾签名无效")
        
        # 5. 验证评分
        eval_data = block.get("evaluation", {})
        if "overall_score" not in eval_data:
            warnings.append(f"区块 #{block_id}: 缺少评分")
        
        if not errors or all(e.split(':')[0].strip() != f"区块 #{block_id}" for e in errors):
            print(f"   ✅ 区块 #{block_id} 验证通过")
    
    # 输出结果
    print(f"\n🦞 ========== 验证结果 ==========")
    
    if errors:
        print(f"❌ 发现 {len(errors)} 个错误:")
        for error in errors:
            print(f"   • {error}")
    
    if warnings:
        print(f"⚠️  发现 {len(warnings)} 个警告:")
        for warning in warnings:
            print(f"   • {warning}")
    
    if not errors and not warnings:
        print("✅ 区块链验证通过！所有区块完整且可信。")
        print(f"🦞 龙虾认证: {len(blocks)} 个 skill 已通过验证")
    elif not errors:
        print("✅ 区块链验证通过（有警告，但无错误）")
    else:
        print("❌ 区块链验证失败！")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "total_blocks": len(blocks),
        "certified_blocks": sum(1 for b in blocks if b.get("xia_mi_signature", {}).get("status") == "certified")
    }


def main():
    parser = argparse.ArgumentParser(description="🦞 龙虾区块链验证工具")
    parser.add_argument("--chain-dir", default="./chain", help="区块链目录")
    
    args = parser.parse_args()
    
    chain_dir = Path(args.chain_dir)
    result = verify_chain(chain_dir)
    
    if not result["valid"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
