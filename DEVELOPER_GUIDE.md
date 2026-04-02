# 🦞 龙虾 Skill 认证系统 - 开发者使用手册

> **核心理念**: 龙虾负责评估和签名，加密决策权交给开发者

---

## 📖 系统原理

### 什么是龙虾 Skill 认证系统？

这是一个为 OpenClaw AgentSkills 提供**评估、签名和溯源**的系统。由 🦞 虾米酱（龙虾）作为"守护者"，为每个 skill 提供：

1. **四维评估** - 商业价值、独特性、风险、意愿
2. **数字签名** - 龙虾印记 + 时间戳 + 哈希
3. **区块链记录** - 不可篡改的认证链
4. **可选加密** - AES-256 真实加密（开发者决定）

### 设计哲学

```
龙虾 ≠ 独裁者
龙虾 = 顾问 + 守护者

龙虾给出专业评分和建议
最终决策权在开发者手中
```

---

## 🚀 快速开始

### 安装

```bash
# 将 skill-creator 放入你的 skills 目录
cp -r skill-creator ~/.openclaw/skills/

# 安装依赖
pip install cryptography
```

### 三步使用

```bash
# 1. 创建 skill（会自动触发龙虾评估）
python scripts/init_skill.py my-skill --path ./skills

# 2. 查看龙虾建议
python scripts/lobster_advisor.py ./skills/my-skill

# 3. 根据建议决定是否加密和签名
```

---

## 🦞 龙虾评估体系

### 四维评分

| 维度 | 权重 | 说明 | 评估标准 |
|-----|------|------|---------|
| **商业价值** | 30% | 是否解决实际问题 | 企业级(80)/自动化(70)/工具(60)/通用(40) |
| **独特性** | 25% | 是否有创新点 | 自定义脚本(75)/纯文档(50) |
| **被窃风险** | 25% | 是否容易被复制 | 加密相关(90)/高商业(80)/普通(50) |
| **作者意愿** | 20% | 是否希望保护 | 明确加密(100)/未表态(50) |

### 评分等级

```
90-100分: 🌟 极佳 - 强烈建议加密保护
70-89分:  🔒 优秀 - 建议加密
50-69分:  ⚠️  良好 - 可选加密
0-49分:   ✓ 一般 - 加密意义不大
```

### 龙虾建议解读

**🔒 强烈建议加密**
- 评分 ≥ 80
- 龙虾认为这个 skill 很有价值
- 被复制的风险较高
- 建议：加密 + 签名

**⚠️ 建议加密**
- 评分 50-79
- 龙虾认为有一定价值
- 如果包含敏感逻辑，建议保护
- 建议：根据内容决定

**✓ 可选加密**
- 评分 < 50
- 龙虾认为加密意义不大
- 可以只添加签名，不加密
- 建议：签名即可

---

## 📋 完整工作流程

### 场景 1: 只看评分，不加密

```bash
# 1. 创建 skill
python scripts/init_skill.py my-skill --path ./skills

# 2. 查看龙虾评分
python scripts/lobster_advisor.py ./skills/my-skill

# 输出示例:
# 📈 四维评分:
#    商业价值: 60/100
#    独特性: 75/100
#    被窃风险: 50/100
#    作者意愿: 50/100
#    综合评分: 58.5/100
#
# 🦞 龙虾的建议:
#    ⚠️  建议加密
#    💡 理由: 这个 skill 有一定价值...

# 3. 决定不加密，只签名
python scripts/evaluate_skill.py ./skills/my-skill --block-id 1 --apply

# 4. 打包
python scripts/package_skill.py ./skills/my-skill ./dist
```

### 场景 2: 评分后决定加密

```bash
# 1-2. 同上，创建并查看评分

# 3. 决定加密
python scripts/encrypt_skill.py encrypt ./skills/my-skill --password mypassword

# 4. 添加签名
python scripts/evaluate_skill.py ./skills/my-skill --block-id 1 --apply

# 5. 打包
python scripts/package_skill.py ./skills/my-skill ./dist

# 6. 添加到区块链
python scripts/add_to_chain.py --add ./skills/my-skill --name my-skill
```

### 场景 3: 一体化快速流程

```bash
# 创建 + 自动评估（不自动加密）
python scripts/init_skill.py my-skill --path ./skills
python scripts/lobster_advisor.py ./skills/my-skill

# 然后根据建议决定后续操作
```

---

## 🔐 加密说明

### 加密算法

- **算法**: AES-256-CBC
- **密钥派生**: PBKDF2-HMAC-SHA256 (100000 次迭代)
- **盐值**: 随机 16 字节
- **格式**: JSON 封装

### 加密 vs 不加密

| 特性 | 加密 | 不加密 |
|-----|------|--------|
| 安全性 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| 便捷性 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 龙虾签名 | ✅ 有 | ✅ 有 |
| 区块链记录 | ✅ 有 | ✅ 有 |
| 适用场景 | 高价值/敏感 | 通用/开源 |

### 加密命令

```bash
# 加密
python scripts/encrypt_skill.py encrypt ./skills/my-skill --password your_password

# 解密
python scripts/encrypt_skill.py decrypt ./skills/my-skill.encrypted --password your_password
```

---

## 🦞 龙虾签名格式

每个经过龙虾认证的 skill 都会包含以下签名：

```yaml
xia_mi_signature:
  emoji: "🦞"
  name: "虾米酱"
  timestamp: "2026-04-01T14:47:50+08:00"
  hash: "sha256:abc123..."           # 原始内容哈希
  encrypted_hash: "sha256:def456..."  # 加密后哈希（如加密）
  status: "certified"
  block_id: 1
  evaluation:
    commercial_value: 80
    uniqueness: 75
    theft_risk: 90
    author_wish: 50
    overall_score: 75.2
    encrypted: true                   # 是否加密
    encryption_type: "AES-256"        # 加密类型
```

---

## ⛓ 区块链系统

### 查看区块链

```bash
# 验证区块链完整性
python scripts/verify_chain.py --chain-dir ./chain

# 查看账本
python scripts/add_to_chain.py --list
```

### 区块链结构

```
区块 #0 (创世) ──→ 区块 #1 ──→ 区块 #2 ──→ ...
skill-creator      my-skill      another-skill
```

每个区块包含：
- 区块 ID
- 时间戳
- Skill 名称和路径
- 龙虾签名
- 评估分数
- 当前哈希
- 上一区块哈希（哈希链）

---

## 🛠 高级用法

### 自定义评估权重

编辑 `evaluate_skill.py` 第 45-48 行：

```python
weights = {
    "commercial_value": 0.30,  # 调整权重
    "uniqueness": 0.25,
    "theft_risk": 0.25,
    "author_wish": 0.20
}
```

### 批量处理

```bash
# 批量评估多个 skills
for skill in ./skills/*; do
    python scripts/lobster_advisor.py "$skill"
done
```

### 集成到 CI/CD

```yaml
# .github/workflows/lobster.yml
- name: Lobster Review
  run: |
    python scripts/lobster_advisor.py ./skills/my-skill
    python scripts/verify_chain.py --chain-dir ./chain
```

---

## ❓ 常见问题

### Q: 龙虾评分准确吗？
A: 龙虾基于规则自动评估，给出参考建议。最终决策权在开发者。

### Q: 不加密只签名有用吗？
A: 有用！签名提供溯源和可信度，适合开源或低敏感度 skill。

### Q: 加密后还能修改吗？
A: 可以。解密 → 修改 → 重新加密 → 新版本上链。

### Q: 密码忘了怎么办？
A: 无法恢复。建议妥善保管密码，或使用版本控制管理原始文件。

### Q: 可以撤销认证吗？
A: 可以标记为 `revoked`，但区块链记录不可删除（不可篡改特性）。

---

## 🤝 参与贡献

### 报告问题
- 在 GitHub Issues 提交
- 或联系 🦞 虾米酱

### 改进建议
- 调整评估规则
- 增加新功能
- 优化加密算法

---

## 📞 联系龙虾

🦞 **虾米酱** - 你的 Skill 守护者

- 负责评估和签名
- 给出专业建议
- 保护你的数字资产

---

**记住**: 龙虾是顾问，不是独裁者。最终决策权在你！🦞✨
