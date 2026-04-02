#!/usr/bin/env python3
"""
🦞 龙虾 Skill 打包脚本
打包 skill 并生成 .skill 文件，包含龙虾认证信息
"""

import argparse
import json
import os
import re
import shutil
import sys
import zipfile
from datetime import datetime
from pathlib import Path


from typing import Tuple, List

def validate_skill(skill_path: Path) -> Tuple[bool, List]:
    """验证 skill 结构"""
    errors = []
    
    if not skill_path.exists():
        errors.append(f"Skill 目录不存在: {skill_path}")
        return False, errors
    
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        errors.append("缺少 SKILL.md 文件")
        return False, errors
    
    content = skill_md.read_text()
    
    # 检查 YAML frontmatter
    if not content.startswith("---"):
        errors.append("SKILL.md 缺少 YAML frontmatter")
    
    # 检查 name 和 description
    if "name:" not in content:
        errors.append("缺少 name 字段")
    if "description:" not in content:
        errors.append("缺少 description 字段")
    
    # 检查龙虾签名（如果已认证）
    if "xia_mi_signature:" in content:
        if "status: \"certified\"" not in content:
            errors.append("龙虾签名未完成认证")
    
    return len(errors) == 0, errors


def check_symlinks(skill_path: Path) -> list:
    """检查是否存在符号链接"""
    symlinks = []
    for item in skill_path.rglob("*"):
        if item.is_symlink():
            symlinks.append(item)
    return symlinks


def package_skill(skill_path: Path, output_dir: Path = None) -> Path:
    """打包 skill 为 .skill 文件"""
    
    skill_name = skill_path.name
    
    if output_dir is None:
        output_dir = skill_path.parent
    
    output_path = output_dir / f"{skill_name}.skill"
    
    # 创建 zip 文件
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file_path in skill_path.rglob("*"):
            if file_path.is_file():
                arcname = file_path.relative_to(skill_path)
                zf.write(file_path, arcname)
    
    return output_path


def extract_certification_info(skill_path: Path) -> dict:
    """提取龙虾认证信息"""
    
    skill_md = skill_path / "SKILL.md"
    content = skill_md.read_text()
    
    info = {
        "certified": False,
        "timestamp": None,
        "hash": None,
        "block_id": None,
        "score": None
    }
    
    # 查找签名块
    match = re.search(r'xia_mi_signature:.*?```', content, re.DOTALL)
    if match:
        sig_content = match.group(0)
        
        if "status: \"certified\"" in sig_content:
            info["certified"] = True
        
        hash_match = re.search(r'hash: "([^"]+)"', sig_content)
        if hash_match:
            info["hash"] = hash_match.group(1)
        
        block_match = re.search(r'block_id: (\d+)', sig_content)
        if block_match:
            info["block_id"] = int(block_match.group(1))
        
        score_match = re.search(r'overall_score: ([\d.]+)', sig_content)
        if score_match:
            info["score"] = float(score_match.group(1))
    
    return info


def main():
    parser = argparse.ArgumentParser(description="🦞 龙虾 Skill 打包工具")
    parser.add_argument("skill_path", help="Skill 目录路径")
    parser.add_argument("output", nargs="?", help="输出目录（可选）")
    parser.add_argument("--no-validate", action="store_true", help="跳过验证")
    
    args = parser.parse_args()
    
    skill_path = Path(args.skill_path)
    
    print(f"🦞 龙虾正在打包: {skill_path.name}")
    print("-" * 40)
    
    # 验证
    if not args.no_validate:
        valid, errors = validate_skill(skill_path)
        if not valid:
            print("❌ 验证失败:")
            for error in errors:
                print(f"   • {error}")
            sys.exit(1)
        print("✅ 验证通过")
    
    # 检查符号链接
    symlinks = check_symlinks(skill_path)
    if symlinks:
        print("❌ 发现符号链接（安全限制）:")
        for link in symlinks:
            print(f"   • {link}")
        sys.exit(1)
    
    # 提取认证信息
    cert_info = extract_certification_info(skill_path)
    if cert_info["certified"]:
        print(f"🦞 已认证 | 区块 #{cert_info['block_id']} | 评分 {cert_info['score']:.1f}")
    else:
        print("⚠️ 未经过龙虾认证")
    
    # 打包
    output_dir = Path(args.output) if args.output else None
    output_path = package_skill(skill_path, output_dir)
    
    # 计算文件大小
    size = output_path.stat().st_size
    size_kb = size / 1024
    
    print("-" * 40)
    print(f"✅ 打包完成: {output_path}")
    print(f"📦 大小: {size_kb:.1f} KB")
    
    # 生成区块链记录
    record = {
        "skill_name": skill_path.name,
        "timestamp": datetime.now().isoformat(),
        "certification": cert_info,
        "package_size": size,
        "package_path": str(output_path)
    }
    
    print(f"\n🔗 区块链记录:")
    print(json.dumps(record, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
