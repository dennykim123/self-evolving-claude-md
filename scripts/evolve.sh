#!/bin/zsh
# HARNESS evolution runner: mine -> promotion session -> (if rules changed) regression probes.
# Usage: ./evolve.sh [days, default 7]
set -eu
DAYS="${1:-7}"
OFFICE="$HOME/.claude/office"
REPORT=$(python3 "$OFFICE/mine.py" --days "$DAYS")
echo "$REPORT"
echo "----- promotion session -----"
claude -p --model opus "You are the evolution steward of the HARNESS. Evolve it based on the mining report below.

Procedure:
1. Read $OFFICE/HARNESS.md (the SSOT).
2. Promote to rule candidates ONLY correction themes that repeat 2+ times AND are not covered by existing rules. If a rule exists but was violated, STRENGTHEN its wording instead of adding a new rule. If the rule is already maximally explicit, it is a compliance failure, not a rule defect — change nothing.
3. Apply changes consistently to all loaders: the SSOT, ~/.claude/CLAUDE.md, and the HARNESS marker block inside ~/.codex/AGENTS.md (NEVER touch anything outside the markers).
4. Add one row to the SSOT version log: date | version | what changed and why | verbatim correction quotes as evidence.
5. If nothing qualifies, modify NO documents — report 'no promotion' and why. Do not overfit to one-off corrections.
6. If the correction:approval ratio is worse than the baseline noted in the SSOT, say so in your first line.
7. FUSION routing learning: if $OFFICE/fusion-ledger.jsonl exists with 5+ entries, read it; a task_type failing verify twice at a tier gets routed one tier up in the SSOT routing table (immediately); a task_type passing 5+ straight at a tier earns a route-DOWN experiment proposal in the version log (proposal only).

Mining report:
$REPORT"
echo "----- regression -----"
echo "If rules changed, run: $OFFICE/probes.sh <model>"
