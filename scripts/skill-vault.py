#!/usr/bin/env python3
"""
🦞 龙虾 Skill 保险箱
密码管理工具，让加密解密更方便
"""

import argparse
import getpass
import json
import os
import sys
from pathlib import Path


VAULT_FILE = Path.home() / ".lobster_vault.json"


def get_vault():
    """获取密码保险箱"""
    if VAULT_FILE.exists():
        with open(VAULT_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_vault(vault):
    """保存密码保险箱"""
    VAULT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(VAULT_FILE, 'w') as f:
        json.dump(vault, f, indent=2)
    os.chmod(VAULT_FILE, 0o600)  # 仅自己可读写


def store_password(skill_name: str, password: str):
    """存储密码到保险箱"""
    vault = get_vault()
    vault[skill_name] = password
    save_vault(vault)
    print(f"🔐 密码已存入保险箱: {skill_name}")


def get_password(skill_name: str) -> str:
    """从保险箱获取密码"""
    vault = get_vault()
    if skill_name in vault:
        return vault[skill_name]
    return None


def list_stored():
    """列出已存储的密码"""
    vault = get_vault()
    if not vault:
        print("🦞 保险箱是空的")
        return
    
    print("🦞 已存储的 Skill 密码:")
    for name in vault.keys():
        print(f"   • {name}")


def remove_password(skill_name: str):
    """删除存储的密码"""
    vault = get_vault()
    if skill_name in vault:
        del vault[skill_name]
        save_vault(vault)
        print(f"🗑️ 已删除: {skill_name}")
    else:
        print(f"❌ 未找到: {skill_name}")


def encrypt_with_vault(skill_path: Path, skill_name: str = None):
    """使用保险箱密码加密"""
    if skill_name is None:
        skill_name = skill_path.name
    
    # 检查是否已有密码
    password = get_password(skill_name)
    
    if password:
        print(f"🔐 使用保险箱中的密码")
    else:
        # 交互式输入
        password = getpass.getpass(f"设置密码 for {skill_name}: ")
        confirm = getpass.getpass("确认密码: ")
        if password != confirm:
            print("❌ 密码不一致")
            return False
        
        # 询问是否保存到保险箱
        print(f"\n💾 是否保存密码到保险箱? (y/n): ", end="")
        response = input().strip().lower()
        if response == 'y':
            store_password(skill_name, password)
    
    # 调用加密
    from encrypt_skill import encrypt_skill
    encrypt_skill(skill_path, password)
    return True


def decrypt_with_vault(encrypted_path: Path, skill_name: str = None):
    """使用保险箱密码解密"""
    if skill_name is None:
        skill_name = encrypted_path.name.replace('.encrypted', '')
    
    # 检查是否已有密码
    password = get_password(skill_name)
    
    if password:
        print(f"🔐 使用保险箱中的密码")
    else:
        # 交互式输入
        password = getpass.getpass(f"输入密码 for {skill_name}: ")
    
    # 调用解密
    from encrypt_skill import decrypt_skill
    output_path = encrypted_path.parent / skill_name
    decrypt_skill(encrypted_path, password, output_path)
    return True


def main():
    parser = argparse.ArgumentParser(description="🦞 龙虾 Skill 保险箱")
    parser.add_argument("action", choices=[
        "store", "get", "list", "remove",
        "encrypt", "decrypt"
    ], help="操作")
    parser.add_argument("skill_name", nargs="?", help="Skill 名称")
    parser.add_argument("--path", help="Skill 路径")
    
    args = parser.parse_args()
    
    if args.action == "store":
        if not args.skill_name:
            print("❌ 请提供 skill 名称")
            sys.exit(1)
        password = getpass.getpass("设置密码: ")
        store_password(args.skill_name, password)
    
    elif args.action == "get":
        if not args.skill_name:
            print("❌ 请提供 skill 名称")
            sys.exit(1)
        password = get_password(args.skill_name)
        if password:
            print(f"密码: {password}")
        else:
            print("❌ 未找到密码")
    
    elif args.action == "list":
        list_stored()
    
    elif args.action == "remove":
        if not args.skill_name:
            print("❌ 请提供 skill 名称")
            sys.exit(1)
        remove_password(args.skill_name)
    
    elif args.action == "encrypt":
        if not args.path:
            print("❌ 请提供 --path")
            sys.exit(1)
        skill_path = Path(args.path)
        encrypt_with_vault(skill_path, args.skill_name)
    
    elif args.action == "decrypt":
        if not args.path:
            print("❌ 请提供 --path")
            sys.exit(1)
        encrypted_path = Path(args.path)
        decrypt_with_vault(encrypted_path, args.skill_name)


if __name__ == "__main__":
    main()
