# 🦞 Lobster Skill Certification - HEARTBEAT.md

## Automatic Skill Evaluation

Add this to your OpenClaw HEARTBEAT.md to enable automatic skill discovery and evaluation:

```markdown
## 🦞 Lobster Skill Auto-Evaluation (every 30 minutes)

If 30 minutes since last Lobster check:
1. Run `python scripts/auto_evaluate_heartbeat.py`
2. If new skills found, notify user with evaluation report
3. Update lastLobsterCheck timestamp in memory
```

## Manual Commands

```bash
# Auto-evaluate all skills
python scripts/auto_evaluate_heartbeat.py

# Verify specific skill signature
python scripts/runtime_verifier.py my-skill

# Verify all skills
python scripts/runtime_verifier.py --all

# Check hash chain integrity
python scripts/verify_chain.py --chain-dir ./chain
```

## Integration with OpenClaw

Add to your OpenClaw `HEARTBEAT.md`:

```markdown
## Skill Certification Check (every 30 min)
- Check for new skills in ~/.openclaw/skills
- Auto-evaluate and report to user
- Remind about encryption/signing if needed
```
