#!/usr/bin/env python3
"""
🦞 龙虾自动评估心跳

定期检查 skills 目录，发现新 skill 自动评估并通知用户
"""

import os
import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent))

def get_skill_hash(skill_path):
    """计算 skill 目录的哈希"""
    hasher = hashlib.sha256()
    skill_path = Path(skill_path)
    
    for file in sorted(skill_path.rglob('*')):
        if file.is_file():
            hasher.update(file.read_bytes())
    
    return hasher.hexdigest()[:16]

def scan_skills(skills_dir):
    """扫描 skills 目录，返回所有 skill"""
    skills_dir = Path(skills_dir)
    if not skills_dir.exists():
        return []
    
    skills = []
    for item in skills_dir.iterdir():
        if item.is_dir() and (item / 'SKILL.md').exists():
            skills.append({
                'name': item.name,
                'path': str(item),
                'hash': get_skill_hash(item),
                'modified': item.stat().st_mtime
            })
    
    return skills

def load_state(state_file):
    """加载状态文件"""
    if os.path.exists(state_file):
        with open(state_file, 'r') as f:
            return json.load(f)
    return {'known_skills': {}, 'last_check': None}

def save_state(state, state_file):
    """保存状态文件"""
    with open(state_file, 'w') as f:
        json.dump(state, f, indent=2)

def evaluate_skill(skill_path):
    """评估 skill（简化版，调用完整评估）"""
    import subprocess
    result = subprocess.run(
        ['python3', 'scripts/lobster_advisor.py', skill_path],
        capture_output=True,
        text=True,
        cwd=str(Path(__file__).parent.parent)
    )
    
    # 解析评分
    score = None
    recommendation = None
    for line in result.stdout.split('\n'):
        if '综合评分' in line or 'Overall Score' in line:
            try:
                score = float(line.split(':')[1].strip().split('/')[0])
            except:
                pass
        if '龙虾建议' in line or 'Lobster Advice' in line:
            recommendation = line.split(':')[1].strip() if ':' in line else line
    
    return score, recommendation, result.stdout

def generate_report(new_skills, changed_skills, state_file):
    """生成评估报告"""
    report = []
    report.append("🦞 龙虾 Skill 自动评估报告")
    report.append(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    if new_skills:
        report.append(f"📦 发现 {len(new_skills)} 个新 Skill:")
        for skill in new_skills:
            report.append(f"  • {skill['name']}")
            score, rec, detail = evaluate_skill(skill['path'])
            report.append(f"    评分: {score}/100" if score else "    评分: 未获取")
            report.append(f"    建议: {rec}" if rec else "    建议: 请查看详细评估")
            report.append("")
    
    if changed_skills:
        report.append(f"📝 发现 {len(changed_skills)} 个 Skill 有变更:")
        for skill in changed_skills:
            report.append(f"  • {skill['name']} (内容已变更，建议重新评估)")
        report.append("")
    
    if not new_skills and not changed_skills:
        report.append("✅ 没有新发现，所有 Skill 都已评估过")
    
    report.append("")
    report.append("💡 提示: 运行 `python scripts/lobster_advisor.py <skill-path>` 查看详细评估")
    report.append("🔒 如需加密/签名，请运行相应脚本")
    
    return '\n'.join(report)

def main():
    """主函数"""
    # 配置
    skills_dir = os.path.expanduser('~/.openclaw/skills')
    state_file = os.path.expanduser('~/.openclaw/skill-creator/heartbeat_state.json')
    
    # 确保目录存在
    os.makedirs(os.path.dirname(state_file), exist_ok=True)
    
    # 加载状态
    state = load_state(state_file)
    
    # 扫描当前 skills
    current_skills = {s['name']: s for s in scan_skills(skills_dir)}
    known_skills = state.get('known_skills', {})
    
    # 发现新 skill 和变更的 skill
    new_skills = []
    changed_skills = []
    
    for name, skill in current_skills.items():
        if name not in known_skills:
            new_skills.append(skill)
            known_skills[name] = skill
        elif known_skills[name]['hash'] != skill['hash']:
            changed_skills.append(skill)
            known_skills[name] = skill
    
    # 生成报告
    report = generate_report(new_skills, changed_skills, state_file)
    
    # 更新状态
    state['known_skills'] = known_skills
    state['last_check'] = datetime.now().isoformat()
    save_state(state, state_file)
    
    # 输出报告
    print(report)
    
    # 如果有新 skill，返回非零码以便调用者知道需要通知用户
    return 1 if new_skills else 0

if __name__ == '__main__':
    sys.exit(main())
