#!/usr/bin/env python3
"""
🦞 龙虾运行时签名验证器

Skill 加载时自动检查签名有效性
"""

import os
import sys
import re
import hashlib
import yaml
from pathlib import Path

def extract_signature(skill_md_path):
    """从 SKILL.md 中提取龙虾签名"""
    skill_md_path = Path(skill_md_path)
    if not skill_md_path.exists():
        return None
    
    content = skill_md_path.read_text(encoding='utf-8')
    
    # 查找签名块
    signature_pattern = r'xia_mi_signature:\s*\n((?:  .+\n?)*)'
    match = re.search(signature_pattern, content)
    
    if not match:
        return None
    
    # 解析 YAML
    try:
        signature_yaml = 'xia_mi_signature:\n' + match.group(1)
        # 移除 emoji 避免 YAML 解析错误
        signature_yaml = signature_yaml.replace('🦞', ':lobster:')
        data = yaml.safe_load(signature_yaml)
        return data.get('xia_mi_signature')
    except:
        return None

def calculate_hash(skill_dir):
    """计算 skill 目录的当前哈希"""
    skill_dir = Path(skill_dir)
    hasher = hashlib.sha256()
    
    for file in sorted(skill_dir.rglob('*')):
        if file.is_file():
            try:
                hasher.update(file.read_bytes())
            except:
                pass
    
    return hasher.hexdigest()

def verify_signature(skill_path):
    """
    验证 skill 签名
    
    返回: {
        'valid': bool,
        'signed': bool,  # 是否有签名
        'hash_match': bool,  # 哈希是否匹配
        'message': str
    }
    """
    skill_path = Path(skill_path)
    skill_md = skill_path / 'SKILL.md'
    
    if not skill_md.exists():
        return {
            'valid': False,
            'signed': False,
            'hash_match': False,
            'message': '❌ SKILL.md not found'
        }
    
    # 提取签名
    signature = extract_signature(skill_md)
    
    if not signature:
        return {
            'valid': False,
            'signed': False,
            'hash_match': False,
            'message': '⚠️ No Lobster signature found'
        }
    
    # 检查必要字段
    if 'hash' not in signature:
        return {
            'valid': False,
            'signed': True,
            'hash_match': False,
            'message': '❌ Signature incomplete: missing hash'
        }
    
    # 计算当前哈希
    current_hash = calculate_hash(skill_path)
    
    # 对比哈希
    stored_hash = signature.get('hash', '').replace('sha256:', '')
    hash_match = stored_hash[:16] == current_hash[:16]
    
    if hash_match:
        return {
            'valid': True,
            'signed': True,
            'hash_match': True,
            'message': f'✅ Valid Lobster signature (Block #{signature.get("block_id", "?")})',
            'signature': signature
        }
    else:
        return {
            'valid': False,
            'signed': True,
            'hash_match': False,
            'message': '⚠️ Signature found but content has changed!',
            'signature': signature
        }

def verify_all_skills(skills_dir):
    """验证所有 skills"""
    skills_dir = Path(skills_dir)
    if not skills_dir.exists():
        print(f"❌ Skills directory not found: {skills_dir}")
        return
    
    results = []
    
    for item in skills_dir.iterdir():
        if item.is_dir() and (item / 'SKILL.md').exists():
            result = verify_signature(item)
            results.append({
                'name': item.name,
                **result
            })
    
    # 打印报告
    print("🦞 Lobster Signature Verification Report")
    print("=" * 50)
    
    valid_count = sum(1 for r in results if r['valid'])
    signed_count = sum(1 for r in results if r['signed'])
    total = len(results)
    
    for r in results:
        print(f"\n{r['name']}:")
        print(f"  {r['message']}")
    
    print("\n" + "=" * 50)
    print(f"Summary: {valid_count}/{total} valid, {signed_count}/{total} signed")
    
    return results

def auto_verify(skill_name=None):
    """
    自动验证（用于集成到 OpenClaw）
    
    如果指定 skill_name，只验证该 skill
    否则验证所有 skills
    """
    skills_dir = Path(os.path.expanduser('~/.openclaw/skills'))
    
    if skill_name:
        skill_path = skills_dir / skill_name
        if skill_path.exists():
            result = verify_signature(skill_path)
            return result
        else:
            return {'valid': False, 'message': f'Skill not found: {skill_name}'}
    else:
        return verify_all_skills(skills_dir)

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='🦞 Lobster Runtime Signature Verifier')
    parser.add_argument('skill', nargs='?', help='Specific skill to verify')
    parser.add_argument('--all', action='store_true', help='Verify all skills')
    
    args = parser.parse_args()
    
    if args.all or not args.skill:
        verify_all_skills(os.path.expanduser('~/.openclaw/skills'))
    else:
        result = verify_signature(args.skill)
        print(result['message'])
        sys.exit(0 if result['valid'] else 1)
