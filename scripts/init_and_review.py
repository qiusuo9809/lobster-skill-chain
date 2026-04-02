#!/usr/bin/env python3
"""
🦞 龙虾创建+审查一体化脚本
创建 skill 后自动进入审查流程
"""

import argparse
import subprocess
import sys
from pathlib import Path


def init_and_review(name: str, output_dir: str, resources: list, auto: bool = False):
    """
    创建 skill 并自动审查
    """
    
    script_dir = Path(__file__).parent
    
    # 1. 创建 skill
    print(f"🦞 ========== 创建 Skill ==========")
    cmd = [
        "python", str(script_dir / "init_skill.py"),
        name,
        "--path", output_dir
    ]
    
    if resources:
        cmd.extend(["--resources", ",".join(resources)])
    
    print(f"运行: {' '.join(cmd)}")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    
    if result.returncode != 0:
        print(f"❌ 创建失败:\n{result.stderr}")
        return False
    
    print(result.stdout)
    
    # 2. 自动审查
    skill_path = Path(output_dir) / name
    print(f"\n🦞 ========== 自动审查 ==========")
    
    cmd = [
        "python", str(script_dir / "auto_review.py"),
        str(skill_path)
    ]
    
    if auto:
        cmd.append("--auto")
    
    print(f"运行: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description="🦞 龙虾创建+审查一体化")
    parser.add_argument("name", help="Skill 名称")
    parser.add_argument("--path", default=".", help="输出目录")
    parser.add_argument("--resources", default="", help="资源类型: scripts,references,assets")
    parser.add_argument("--auto", action="store_true", help="自动模式（无需确认）")
    
    args = parser.parse_args()
    
    resources = [r.strip() for r in args.resources.split(",") if r.strip()]
    
    success = init_and_review(args.name, args.path, resources, args.auto)
    
    if success:
        print("\n🎉 创建+审查完成！")
    else:
        print("\n❌ 流程失败！")
        sys.exit(1)


if __name__ == "__main__":
    main()
