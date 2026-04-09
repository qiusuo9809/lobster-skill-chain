#!/usr/bin/env python3
"""
🦞 龙虾 Skill 加密脚本
提供真实的 AES 加密保护，默认使用密码保险箱
"""

import argparse
import base64
import getpass
import hashlib
import json
import os
import sys
from pathlib import Path

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


# 保险箱路径
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
    os.chmod(VAULT_FILE, 0o600)


def get_stored_password(skill_name: str) -> str:
    """从保险箱获取密码"""
    vault = get_vault()
    return vault.get(skill_name)


def store_password(skill_name: str, password: str):
    """存储密码到保险箱"""
    vault = get_vault()
    vault[skill_name] = password
    save_vault(vault)


def generate_key(password: str, salt: bytes = None) -> tuple:
    """从密码生成加密密钥"""
    if salt is None:
        salt = os.urandom(16)
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key, salt


def encrypt_skill(skill_path: Path, password: str = None, output_path: Path = None, 
                  use_vault: bool = True, skill_name: str = None):
    """加密整个 skill 目录，默认使用保险箱"""
    
    if skill_name is None:
        skill_name = skill_path.name
    
    if output_path is None:
        output_path = skill_path.parent / f"{skill_name}.encrypted"
    
    print(f"🔒 正在加密: {skill_name}")
    
    # 获取密码
    if password is None:
        stored = get_stored_password(skill_name) if use_vault else None
        
        if stored:
            print(f"🔐 使用保险箱中的密码")
            password = stored
        else:
            password = getpass.getpass(f"设置加密密码: ")
            confirm = getpass.getpass("确认密码: ")
            if password != confirm:
                print("❌ 密码不一致")
                return None
            
            # 询问是否保存到保险箱
            if use_vault:
                print(f"💾 是否保存密码到保险箱? (y/n) [默认y]: ", end="")
                response = input().strip().lower()
                if response in ('', 'y', 'yes'):
                    store_password(skill_name, password)
                    print(f"✅ 密码已存入保险箱")
    
    # 生成密钥
    key, salt = generate_key(password)
    f = Fernet(key)
    
    # 收集所有文件（安全检查：解析符号链接，确保不越界）
    files_data = {}
    skill_path_resolved = skill_path.resolve()
    
    for file_path in skill_path.rglob("*"):
        if file_path.is_file():
            # 安全检查：解析符号链接，确保目标在 skill 目录内
            try:
                file_resolved = file_path.resolve()
                # 确保解析后的路径仍在 skill 目录内
                if not str(file_resolved).startswith(str(skill_path_resolved)):
                    print(f"⚠️  跳过越界文件: {file_path} -> {file_resolved}")
                    continue
                
                rel_path = str(file_path.relative_to(skill_path))
                files_data[rel_path] = file_path.read_bytes()
            except (OSError, ValueError) as e:
                print(f"⚠️  跳过可疑文件: {file_path} ({e})")
                continue
    
    # 打包并加密
    package = {
        "skill_name": skill_name,
        "salt": base64.b64encode(salt).decode(),
        "files": {}
    }
    
    for rel_path, content in files_data.items():
        encrypted = f.encrypt(content)
        package["files"][rel_path] = base64.b64encode(encrypted).decode()
    
    # 保存加密文件
    with open(output_path, 'w') as f_out:
        json.dump(package, f_out, indent=2)
    
    # 计算加密后的哈希
    hasher = hashlib.sha256()
    hasher.update(open(output_path, 'rb').read())
    encrypted_hash = hasher.hexdigest()[:16]
    
    print(f"✅ 加密完成: {output_path}")
    print(f"📦 文件数: {len(files_data)}")
    print(f"🔐 加密哈希: {encrypted_hash}")
    print(f"🦞 龙虾签名: 🦞{encrypted_hash}")
    
    if use_vault and get_stored_password(skill_name):
        print(f"💡 密码已保存在保险箱，下次解密自动使用")
    
    return output_path, encrypted_hash


def decrypt_skill(encrypted_path: Path, password: str = None, 
                  output_path: Path = None, use_vault: bool = True):
    """解密 skill，默认使用保险箱"""
    
    # 从文件名获取 skill_name
    skill_name = encrypted_path.name.replace('.encrypted', '')
    
    print(f"🔓 正在解密: {skill_name}")
    
    # 读取加密文件
    with open(encrypted_path, 'r') as f_in:
        package = json.load(f_in)
    
    # 获取密码
    if password is None:
        stored = get_stored_password(skill_name) if use_vault else None
        
        if stored:
            print(f"🔐 使用保险箱中的密码")
            password = stored
        else:
            password = getpass.getpass(f"输入解密密码: ")
    
    # 还原密钥
    try:
        salt = base64.b64decode(package["salt"])
        key, _ = generate_key(password, salt)
        f = Fernet(key)
    except Exception as e:
        print(f"❌ 密码错误: {e}")
        return None
    
    # 解密并恢复文件
    if output_path is None:
        output_path = encrypted_path.parent / skill_name
    
    output_path.mkdir(parents=True, exist_ok=True)
    
    try:
        for rel_path, encrypted_b64 in package["files"].items():
            encrypted = base64.b64decode(encrypted_b64)
            content = f.decrypt(encrypted)
            
            file_path = output_path / rel_path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_bytes(content)
    except Exception as e:
        print(f"❌ 解密失败，密码可能错误: {e}")
        return None
    
    print(f"✅ 解密完成: {output_path}")
    print(f"📦 恢复文件数: {len(package['files'])}")
    
    return output_path


def main():
    parser = argparse.ArgumentParser(description="🦞 龙虾 Skill 加密工具（默认使用保险箱）")
    parser.add_argument("action", choices=["encrypt", "decrypt"], help="操作类型")
    parser.add_argument("path", help="文件路径")
    parser.add_argument("--password", help="密码（可选，默认从保险箱读取）")
    parser.add_argument("--output", help="输出路径")
    parser.add_argument("--no-vault", action="store_true", help="不使用保险箱")
    
    args = parser.parse_args()
    
    path = Path(args.path)
    output = Path(args.output) if args.output else None
    use_vault = not args.no_vault
    
    if args.action == "encrypt":
        result = encrypt_skill(path, args.password, output, use_vault)
        if result is None:
            sys.exit(1)
    else:
        result = decrypt_skill(path, args.password, output, use_vault)
        if result is None:
            sys.exit(1)


if __name__ == "__main__":
    main()
