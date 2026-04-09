---
name: skill-creator
description: |
  Create or update AgentSkills with 🦞 lobster certification and optional encryption.
  
  **When to use this skill:**
  - When user wants to create a new OpenClaw skill
  - When user wants to evaluate/assess a skill's value
  - When user wants to add lobster signature to a skill
  - When user wants to encrypt/protect a skill
  - When user mentions "skill certification", "lobster signature", "protect my skill"
  
  **Key capabilities:**
  - Initialize new skills with lobster signature placeholder
  - Evaluate skills with 4-dimension scoring (commercial value, uniqueness, theft risk, author wish)
  - Provide encryption advice (AES-256) but let user decide
  - Add digital signature with blockchain record
  - Package and publish skills
  
  **Important:** This skill NEVER auto-encrypts. Always ask user before encrypting.
  Lobster gives advice, user makes the decision.
---

# Skill Creator - 🦞 龙虾认证版

创建和管理 OpenClaw AgentSkills，每个 skill 都经过龙虾的审核、可选加密和本地哈希链认证。

## 🦞 认证流程

```
1. 创建 Skill → 2. 龙虾评估 → 3. 用户决策 → 4. (可选加密) → 5. 数字签名 → 6. 上链记录
```

## 核心原则

**龙虾只给建议，不替用户决策**

- ✅ 龙虾评估价值并给出建议
- ✅ 用户决定是否加密
- ✅ 用户决定是否签名
- ❌ 从不自动加密
- ❌ 从不强制签名

## 龙虾评估标准

| 维度 | 权重 | 说明 |
|-----|------|------|
| 商业价值 | 30% | 是否解决实际问题 |
| 技术独特性 | 25% | 是否有创新点 |
| 被窃风险 | 25% | 是否容易被复制 |
| 作者意愿 | 20% | 是否希望保护 |

**评分等级：**
- **≥80分**: 🔒 强烈建议加密
- **50-79分**: ⚠️ 建议加密
- **<50分**: ✓ 可选加密

## 🦞 龙虾签名格式

```yaml
xia_mi_signature:
  emoji: "🦞"
  name: "虾米酱"
  timestamp: "2026-04-08T11:32:34.101722"
  hash: "sha256:d6f545b041e1b27f"
  status: "certified"
  block_id: 1
  evaluation:
    commercial_value: 70
    uniqueness: 75
    theft_risk: 90
    author_wish: 100
    overall_score: 82.2
    encrypted: true
```

🦞 **龙虾认证完成** - 此 skill 已通过虾米酱审核并加密保护

## 本地哈希链说明

> ⚠️ **重要**: 这是本地哈希链（Hash Chain），不是比特币/以太坊等公链。
> - 数据存储在本地 `ledger.json`
> - 通过哈希链保证记录不可篡改
> - 适合个人/团队溯源，不提供全球共识

## 使用方法

### 1. 创建新 Skill

```bash
python scripts/init_skill.py my-skill --path ./skills --resources scripts,references
```

### 2. 查看龙虾建议（只评估，不执行）

```bash
python scripts/lobster_advisor.py ./skills/my-skill
```

**输出示例：**
```
📈 四维评分:
   商业价值: 80/100
   独特性:   75/100
   被窃风险: 90/100
   作者意愿: 50/100
   综合评分: 75.2/100

🦞 龙虾的建议:
   🔒 强烈建议加密
   💡 理由: 这个 skill 很有价值，被复制的风险较高。
```

### 3. 用户决策并执行

**如果用户决定加密：**
```bash
python scripts/encrypt_skill.py encrypt ./skills/my-skill --password user_password
```

**如果用户决定不加密：**
跳过加密步骤

### 4. 添加龙虾签名

```bash
python scripts/evaluate_skill.py ./skills/my-skill --block-id 1 --apply
```

### 5. 打包输出

```bash
python scripts/package_skill.py ./skills/my-skill ./dist
```

### 6. 添加到本地哈希链

```bash
python scripts/add_to_chain.py --add ./skills/my-skill --name my-skill
```

### 7. 验证链完整性

```bash
python scripts/verify_chain.py --chain-dir ./chain
```

## 🆕 自动功能（新）

### 自动评估心跳

定期检查 skills 目录，发现新 skill 自动评估：

```bash
# 添加到 OpenClaw HEARTBEAT.md
python scripts/auto_evaluate_heartbeat.py
```

**功能：**
- 扫描 `~/.openclaw/skills` 目录
- 发现新 skill 自动评估并生成报告
- 检测已有 skill 的变更
- 建议用户是否加密/签名

### 运行时签名验证

Skill 加载时自动检查签名：

```bash
# 验证特定 skill
python scripts/runtime_verifier.py my-skill

# 验证所有 skills
python scripts/runtime_verifier.py --all
```

**返回结果：**
- ✅ 签名有效
- ⚠️ 有签名但内容已变更
- ❌ 无签名

### CI/CD 集成

GitHub Actions 自动验证：

```yaml
# .github/workflows/verify-chain.yml
- 每次 push 自动验证链完整性
- 每天凌晨自动运行
- 验证所有 skill 签名
```

## 加密说明

**加密算法**: AES-256-CBC
**密钥派生**: PBKDF2-HMAC-SHA256 (100000 次迭代)
**密码**: 用户自定义（默认: xia_mi_lobster_2026）

**加密的是什么？**
- 整个 Skill 目录（所有文件）
- 打包成 `.encrypted` 文件
- 需要解密后才能使用

## 文件结构

```
skill-creator/
├── SKILL.md                    # 本文件（给 OpenClaw Agent 读）
├── README.md                   # 项目介绍（给用户读）
├── README_EN.md               # 英文版项目介绍
├── HEARTBEAT.md               # 自动评估心跳配置
├── DEVELOPER_GUIDE.md          # 完整使用手册
├── PRINCIPLE.md                # 原理说明
├── requirements.txt            # Python 依赖
├── scripts/
│   ├── init_skill.py          # 初始化新 skill
│   ├── lobster_advisor.py     # 龙虾评估建议（⭐核心）
│   ├── encrypt_skill.py       # AES 加密
│   ├── evaluate_skill.py      # 评估 + 签名
│   ├── package_skill.py       # 打包脚本
│   ├── add_to_chain.py        # 本地哈希链管理
│   ├── verify_chain.py        # 链完整性验证
│   ├── auto_evaluate_heartbeat.py  # 🆕 自动评估心跳
│   └── runtime_verifier.py    # 🆕 运行时签名验证
├── .github/
│   └── workflows/
│       └── verify-chain.yml   # 🆕 CI/CD 自动验证
└── chain/
    ├── ledger.json            # 本地哈希链记录
    └── index.html             # 链浏览器
```

## 依赖

```
Python 3.6+
cryptography>=3.0.0
```

## 🦞 创世区块

- **区块 #0**: skill-creator
- **创建时间**: 2026-04-01 11:20
- **认证者**: 🦞 虾米酱
- **综合评分**: 92.5/100
- **状态**: ✅ 已激活
- **加密**: AES-256（可选）

---

*给 OpenClaw Agent 的提示：*
*1. 始终先询问用户是否要进行某项操作*
*2. 加密前必须获得用户明确同意*
*3. 展示龙虾建议后，等待用户决策*
*4. 明确告知用户这是本地哈希链，非公链*
