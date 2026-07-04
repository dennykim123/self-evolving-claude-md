# self-evolving-claude-md

**Your corrections become rules. Automatically.**

A self-evolving `CLAUDE.md` system for [Claude Code](https://claude.com/claude-code) and [Codex CLI](https://github.com/openai/codex): it mines your own session transcripts for the corrections you keep giving your AI, promotes repeated corrections into permanent rules, verifies the rules with behavioral probes, and routes work across model tiers (FUSION-style) so cheap models do the mechanical work without dropping quality.

Stop re-teaching your AI the same thing every session.

```
              ┌────────────────────────────────────────────┐
              │              HARNESS  (SSOT)               │
              │  7-step work loop + invariant rules        │
              │  loaded by CLAUDE.md (Claude Code)         │
              │  and AGENTS.md marker block (Codex)        │
              └───────▲────────────────────────┬───────────┘
                      │ promotes rules         │ routes work
  ┌───────────────────┴───────────┐   ┌────────▼──────────────────┐
  │        EVOLUTION LOOP         │   │      FUSION ROUTING       │
  │ Path A: correction repeated   │   │ mechanical → cheap model  │
  │   twice → becomes a rule now  │   │ production → mid model    │
  │ Path B: weekly transcript     │   │ judgment   → top model    │
  │   mining (launchd) → promote  │   │ (never route judgment     │
  │   clusters, version-log it    │   │  down) + escalation +     │
  │ regression probes verify      │   │  delegation ledger        │
  └───────────────────────────────┘   └───────────────────────────┘
```

## Why

1. **Frontier-model discipline is mostly procedure, not IQ.** If you write the procedure down (intent decomposition → evidence gathering → self-QA → evidence-first reporting), cheaper models follow most of it. We measured this with behavioral probes across model tiers.
2. **Your transcript history is training data for your rules.** Every correction you typed ("why didn't you test this before showing me?", "why did you redesign instead of copying the reference?") is a rule waiting to be written. This repo ships the miner.
3. **Routing needs a quality floor first.** [Cognition's Devin Fusion](https://cognition.com/blog/devin-fusion) showed mechanical work can be delegated down at big savings (-62% on test-running) while *judgment* work degrades when delegated. This repo implements that routing table for Claude Code agents — plus a delegation ledger so your weekly evolution run tunes the routing from your own outcomes.

## What happened when we ran it (24-hour case study)

- Mined **4,041 user messages** from real transcripts → 498 corrections, 1,124 approvals (baseline ratio 1:2.3).
- The dominant correction cluster: **"it's still not fixed"** (106×) — completion claimed without live verification. That became the strictest rule in the harness.
- Harness went **v1.0 → v1.8 in one day**, every version logged with the verbatim correction that caused it. Two of those versions were promoted *by the automated weekly run itself*, not by hand.
- A real production task (full live audit + fix + deploy of a 28-page bilingual site) ran on a mid-tier model with **zero corrections needed**, 7/7 harness compliance, independently verified.
- A bottom-tier sidekick measured 28 URLs perfectly but botched one summary line by *interpreting* — live proof of the "never route judgment down" rule.

Full story: [docs/CASE-STUDY.md](docs/CASE-STUDY.md)

## Quick start

```bash
git clone https://github.com/dennykim123/self-evolving-claude-md
cd self-evolving-claude-md
./scripts/install.sh          # backs up your existing files, never overwrites blindly
```

Then:

1. Edit `~/.claude/office/HARNESS.md` — replace the placeholder rules with yours (or keep the defaults and let evolution rewrite them).
2. Mine your own history: `python3 ~/.claude/office/mine.py --days 30` — read the report, write your own "approval formula".
3. Let it evolve: the installer registers a weekly `launchd` job (macOS) that mines → promotes → regression-probes. Or run `~/.claude/office/evolve.sh 7` manually.

## The pieces

| File | What it is |
|---|---|
| `templates/HARNESS.md` | The SSOT: 7-step loop, invariant rules, FUSION routing table, evolution protocol, version log |
| `templates/CLAUDE.md` | Global loader for Claude Code — inlines the minimum contract so it works even if the SSOT isn't read |
| `templates/AGENTS-block.md` | Marker-bounded block appended to `~/.codex/AGENTS.md` — same contract for Codex, safe to coexist with other AGENTS.md managers |
| `scripts/mine.py` | Transcript miner: extracts your corrections/approvals from Claude Code *and* Codex history, buckets them by theme, tracks your correction:approval ratio against baseline |
| `scripts/evolve.sh` | The weekly evolution run: mine → LLM promotion session (strict rules: only promote corrections seen 2+, never overfit to one-offs) → sync 3 docs → version log |
| `scripts/probes.sh` | Behavioral regression suite: 5 trap prompts (design task, bug report, false-completion trap, sloppy-check trap) + automated grading |
| `scripts/install.sh` | Copies templates (with backup), appends the Codex block, registers the launchd job |

## Design rules that survived contact with reality

- **A rule without a verbatim correction as evidence doesn't get added.** Every version log row cites the human sentence that caused it.
- **One-off corrections never promote** — that's noise. Twice is a rule defect.
- **The promotion session may strengthen an existing rule instead of adding one.** Rule count inflation is how CLAUDE.md files die.
- **Compliance failures are not rule defects.** If the rule is already maximally explicit and still violated, wording won't fix it — don't touch it.
- **Never let the builder self-verify.** Completion claims get independently re-checked before they reach the human.
- **Judgment never routes down.** Mechanical measurement to the cheapest tier, interpretation stays at the top.

## What this won't do (honest limits)

- It reduces *procedural* failures (unverified "done", skipped references, guess-patches). It does **not** give a small model a frontier model's taste. The gap narrows; it doesn't close.
- Rules in files are not 100% compliance. We ship probes precisely because models drift in long sessions.
- The launchd automation is macOS-only (cron/systemd equivalents are a few lines — PRs welcome).

## 한국어

이 리포는 "교정이 자동으로 규칙이 되는 CLAUDE.md" 시스템입니다. 세션 트랜스크립트에서 반복 교정을 채굴해 규칙으로 승격하고(2회 반복 시에만 — 과적합 방지), 행동 프로브로 회귀를 검증하며, 작업 유형별 3티어 라우팅(기계적=하위 모델, 생산=중위, 판단=상위 고정)과 위임 원장으로 Devin Fusion형 멀티모델 운영을 Claude Code 위에 구현합니다. 실제 24시간 운영에서 v1.0에서 v1.8까지 진화했고, 그중 두 번은 사람 개입 없이 주간 자동 실행이 스스로 승격했습니다.

## License

MIT
