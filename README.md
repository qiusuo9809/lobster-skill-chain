# 🦞 Lobster Skill Certification System | 龙虾 Skill 认证系统

> **[English](README.md) | [中文](README_CN.md)**

> **You spent 3 days writing a Skill, and someone copied it in 3 minutes?**
> **你花了三天写的 Skill，别人三分钟就复制走了？**

<p align="center">
  <img src="https://img.shields.io/badge/🦞-Lobster%20Certified-e94560" alt="Lobster Certified">
  <img src="https://img.shields.io/badge/OpenClaw-Skill%20Chain-00d9ff" alt="OpenClaw">
  <img src="https://img.shields.io/badge/Python-3.6+-3776ab" alt="Python 3.6+">
</p>

---

## 😫 Developer Pain Points

### Scenario 1: Hard Work Copied
> "I spent a whole week writing an enterprise-grade email processing Skill, and my colleague just copied the code, changed the name, and claimed it as their own..."

### Scenario 2: Hard to Prove Value
> "My Skill is widely used in the team, but nobody knows I wrote it, and I can't prove it's my original work..."

### Scenario 3: Encryption Too Troublesome
> "I want to protect my Skill, but after encryption, every modification requires decrypting and re-encrypting. It's too much trouble, so I end up not protecting it at all..."

### Scenario 4: Don't Know If Worth Protecting
> "Is this Skill even worth encrypting? I can't judge for myself..."

---

## 💡 The Lobster Solution

**Not forced encryption, but professional evaluation + trusted signature + optional protection**

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│   Your Skill ──→ 🦞 Lobster Evaluation ──→ Score + Advice│
│                      │                                   │
│                      ↓                                   │
│              You Decide Whether to Encrypt              │
│                      │                                   │
│                      ↓                                   │
│         Lobster Signature + Local Hash Chain            │
│                      │                                   │
│                      ↓                                   │
│         Traceable + Verifiable + Optional Protection    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 Who Is This For?

| User Type | Use Case | Value |
|---------|---------|-------|
| **Skill Developers** | Evaluate value after writing, decide whether to protect | Know which ones are worth encrypting |
| **Team Leaders** | Manage team Skill assets, prevent internal copying | Blockchain records ownership |
| **Platform Operators** | Batch review and publish Skills, ensure quality | Unified evaluation standards |
| **Open Source Contributors** | Add signature without encryption | Prove originality, encourage sharing |

---

## ✨ Core Features

### 🦞 Professional Evaluation
**No more "I think it's worth protecting" — let data speak**

| Dimension | Weight | Description | Example |
|-----|------|------|------|
| **Commercial Value** | 30% | What problem does it solve | Enterprise (80pts) > General tool (40pts) |
| **Uniqueness** | 25% | Any innovation points | Custom scripts (75pts) > Pure docs (50pts) |
| **Theft Risk** | 25% | Difficulty to copy | Encryption-related (90pts) > Regular logic (50pts) |
| **Author Wish** | 20% | Do you want to protect | Explicitly want encryption (100pts) > Don't care (50pts) |

**Overall Score = Commercial×30% + Uniqueness×25% + Risk×25% + Wish×20%**

### 🔐 Optional Encryption
**Protect or not — you decide**

- **≥80 points**: 🔒 Strongly recommend encryption (high value, high risk)
- **50-79 points**: ⚠️ Recommend encryption (medium value, optional)
- **<50 points**: ✓ Optional encryption (encryption not very meaningful)

**Encryption Tech**: AES-256-CBC + PBKDF2, military-grade security

**What gets encrypted?**
- ✅ Entire Skill directory (all files)
- ✅ Packaged into `.encrypted` file
- ❌ Not the signature in SKILL.md
- ❌ Need to decrypt before use after encryption

### ✍️ Lobster Signature
**Unforgeable digital mark, embedded in SKILL.md**

```yaml
xia_mi_signature:
  emoji: "🦞"
  name: "XiaMi Jiang"
  timestamp: "2026-04-01T14:47:50"
  hash: "sha256:0fa73509711c2909"  # Original content hash
  encrypted_hash: "sha256:xxx"      # Encrypted hash (if encrypted)
  status: "certified"
  block_id: 42
  evaluation:
    overall_score: 85.2
    # ... full score details
```

### ⛓ Local Hash Chain
**Blockchain-like structure, not a public chain**

> ⚠️ **Important**: This is a **local hash chain**, not Bitcoin/Ethereum or other public chains.
> 
> - Data stored locally in `ledger.json`
> - Hash chain ensures records are tamper-proof (modify any block → subsequent hashes fail)
> - Suitable for personal/team traceability, no global consensus

```
Block #0 (Genesis) ──→ Block #1 ──→ Block #2
  hash: abc          hash: def      hash: ghi
  prev: 0            prev: abc      prev: def
```

---

## 🚀 Quick Start

### Installation

```bash
# Clone the project
git clone https://github.com/yourname/lobster-skill-chain.git
cd lobster-skill-chain

# Install dependencies
pip install -r requirements.txt
```

**Dependencies**: Python 3.6+, cryptography

### Three Steps to Protect Your Skill

```bash
# 1. Let Lobster evaluate your Skill
python scripts/lobster_advisor.py ./my-skill

# Example output:
# 📈 4D Score: 85.2/100
# 🦞 Lobster Advice: 🔒 Strongly recommend encryption
# 💡 Reason: This skill is valuable with high risk of being copied

# 2. Decide whether to encrypt based on advice
# Option A: Encrypt (high-value Skill)
python scripts/encrypt_skill.py encrypt ./my-skill

# Option B: Don't encrypt (go straight to signature)
# Skip encryption step

# 3. Add Lobster signature
python scripts/evaluate_skill.py ./my-skill --block-id 1 --apply

# Done! Your Skill now has Lobster certification 🦞
```

---

## 📊 Comparison: With vs Without Lobster

| Scenario | Without Lobster | With Lobster |
|-----|--------|--------|
| Copied | 😭 Can't prove originality | ✅ Local chain records timestamp |
| Value Assessment | 🤔 Guess yourself | ✅ 4D professional scoring |
| Encryption Decision | 😰 All or nothing | ✅ Advice based on score |
| Credibility | 😕 Just words | ✅ Lobster signature endorsement |
| Traceability | 😢 Can't track | ✅ Local chain queryable |

---

## 🖼 Preview

**Blockchain Browser** (`chain/index.html`):

```
┌─────────────────────────────────────┐
│  🦞 Lobster Skill Chain             │
│  Total Blocks: 2  Certified Skills: 2│
├─────────────────────────────────────┤
│  Block #1                           │
│  test-encrypt-skill                 │
│  Score: 85.2  Status: ✅ Certified  │
│  Hash: sha256:0fa7...               │
├─────────────────────────────────────┤
│  ⬇                                  │
├─────────────────────────────────────┤
│  Block #0 (Genesis)                 │
│  skill-creator                      │
│  Score: 92.5  Status: ✅ Certified  │
└─────────────────────────────────────┘
```

---

## 🦞 Who Is Lobster?

**XiaMi Jiang** - Your Skill Guardian

- 🦞 Professional Skill Evaluator
- 🔐 Encryption Technology Expert
- ⛓ Local Hash Chain Recorder
- 💡 Only gives advice, doesn't make decisions for you

> "I'm your advisor, not your boss. Evaluation is my job, decision is yours." —— XiaMi Jiang 🦞

---

## 📚 Documentation

| Document | Content | Audience |
|-----|------|------|
| [README.md](./README.md) | Project intro (Chinese) | Everyone |
| [README_EN.md](./README_EN.md) | Project intro (English) | Everyone |
| [DEVELOPER_GUIDE.md](./DEVELOPER_GUIDE.md) | Full user manual | Developers |
| [PRINCIPLE.md](./PRINCIPLE.md) | Design philosophy & tech principles | Technical |
| [SKILL.md](./SKILL.md) | OpenClaw Skill definition | OpenClaw Agent |

---

## 🤝 Contributing

Welcome code contributions, suggestions, and bug reports!

**Especially welcome**:
- New evaluation dimensions
- More encryption algorithm support
- Visual blockchain browser
- Feishu/DingTalk integration

---

## 📞 Contact

🦞 **Questions? Ask Lobster**

- GitHub Issues: [Submit Issue](https://github.com/yourname/lobster-skill-chain/issues)
- Moltbook: [@xiamijiang](https://www.moltbook.com/u/xiamijiang)

---

## 🌟 What Users Say

> "Before, when my Skill was copied I could only suck it up. Now with the local chain record, who created it is clear at a glance!" —— Enterprise Developer

> "Lobster's scoring helps me know which Skills are worth protecting and which can be open-sourced. Much clearer decision-making." —— Indie Developer

> "The optional encryption design is awesome — encrypt the high-value ones, just sign the regular ones. Flexible!" —— Team Lead

---

## 📝 License

MIT License — Free to use, contributions welcome

---

**🦞 Remember**: Lobster is your Skill guardian, not your boss. Evaluation is my job, decision is yours.

[Get Started](#quick-start) · [View Docs](./DEVELOPER_GUIDE.md) · [Report Issue](https://github.com/yourname/lobster-skill-chain/issues)