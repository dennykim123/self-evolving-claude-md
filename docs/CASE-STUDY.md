# Case study: v1.0 → v1.8 in 24 hours

This is the real, lightly-anonymized history of the first deployment. Every version row cites the verbatim human correction that caused it (translated from Korean where needed). Client projects are anonymized as "Site A" (a bilingual B2B corporate site) and "Site B" (a nonprofit association site).

## Day 0: mining the baseline

We mined 4,041 short user messages from months of real Claude Code transcripts:

- 498 corrections, 1,124 approvals → baseline ratio **1 : 2.3**
- Top correction cluster: **"it's still not fixed / still not live"** — 106 occurrences. Completion had been claimed on code state, not on the deployed page.
- Second cluster: reference-skipping in design work ("why didn't you look at the top design firms?")
- The distilled **approval formula**: *clone a proven reference → execute the full sweep autonomously → verify on the live URL yourself → report the outcome first, briefly.*

## The version log (real)

| Ver | What changed | Verbatim evidence (translated) |
|---|---|---|
| v1.0 | Initial harness: 7-step loop, 12 rules | the mining report above |
| v1.1 | Banned mid-flight approval gates; banned asking the user for references; deploys ship immediately after verification (this fixed a bug in our own stop-conditions); bounded-claim reporting | A/B comparison showed the mid-tier model saying "I'll show you two variants and code the one you pick" while the frontier model finished one best option |
| v1.2 | Register/politeness codified; banned "shall I proceed?" closings; re-verify remembered facts before quoting | the small model mixed up two clients' page counts in one answer |
| v1.3 | Evolution protocol itself (Path A live promotion + Path B weekly mining via launchd) | "it would be better if you designed this to evolve" |
| v1.4 | **Promoted automatically by the weekly run**: completion = opening the live URL and checking every element renders with the right content in the right slot | "why can't I see the image here?", "the photos are all broken", "the wrong clinic's photo is in this slot" |
| v1.5 | **Promoted automatically by the weekly run**: render checks aren't enough — execute interactive flows (signup, comments, email) end-to-end like a real user; a provided screenshot IS the target, reproduce don't reinterpret | "can you test the signup?", "the test email went to the actual recipient?!", "you should have cloned the screenshot exactly... don't rebuild it" |
| v1.6 | Codex history added as a mining source (corrections given in Codex sessions were a blind spot) | "how does this port to Codex?" |
| v1.7 | FUSION layer: task-type routing table (mechanical→cheapest, production→mid, judgment→never down), escalation, delegation ledger read by the weekly run | Cognition's Devin Fusion data + "turns out what I wanted to build was Fusion" |
| v1.8 | No-recency-bias rule (Path A promotion: the same correction had arrived twice, months apart) | "why are you obsessed with [Site A]?" — matching an April correction "why are you obsessed with [topic X]?" |

## The production test

A real task — full live audit and repair of Site A (28 bilingual pages) — was handed to a mid-tier model with **only the task, no harness rules in the prompt** (the harness loads globally; that was the test).

Result: it audited 30 pages (found 2 legacy strays beyond the asked 28), fixed five real defect classes (dead footer links causing five 404s, untranslated strings, a stale cache-busting version), deployed via FTP, re-verified every fix on the live URL, kept a pre-deploy backup, correctly STOPPED on the one destructive decision (deleting legacy files) and escalated it to the human — and wrote its results into project memory unprompted. Zero corrections needed. An independent orchestrator re-checked every claim against the live site: all true.

## The tier-boundary demo

The cheapest tier was handed a pure measurement task (28 URLs × HTTP status × asset version). Measurements: 28/28 correct. But its summary line *interpreted* — it counted "asset not referenced on this page" as "wrong version on 24 pages". The orchestrator caught it against ground truth.

That is the routing table's core claim, observed live: **the cheapest tier measures perfectly and interprets poorly. Judgment never routes down.**

## Honest limits

- The harness reduces procedural failures. It does not transplant taste. The quality gap narrows; it does not close.
- Single-run probes are noisy; we stopped tuning on them and only promote from repeated real corrections.
- One rule ('no casual verb X in Korean') has been violated repeatedly despite maximally explicit wording — a standing reminder that written rules are not compliance. Probes exist because drift is real.
