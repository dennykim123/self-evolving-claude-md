# Judgment modules

Rules (the harness) keep any model on your quality floor. **Judgment modules go one step further: they turn a recurring judgment you make — "is this worth money?", "how do I structure this?", "what do we quote?" — into a skill with a fixed input → criteria → output contract.**

The pattern that makes them work:

1. **Fixed output contract.** Numbered sections, never skipped, never reordered. This is what makes the module's output composable and its drift detectable.
2. **A personal registry, isolated.** The judgment axis "does this connect to MY assets?" is only as good as the asset list injected into it. The registry is *instance data* — edit `_registry.md`, never the module itself.
3. **NO is a first-class verdict.** A screener that can't reject is a cheerleader. Chain orchestrators must stop on NO.
4. **Judgment never routes down.** Run these on your top model tier (see the FUSION section of the harness).

Ship order that worked in the field: screener → structurer → closer (idea → one-page structure → paying document), chained by an orchestrator that stops on NO.

| Template | Judgment it modularizes |
|---|---|
| `money-screener.md` | "Can this make money, for me specifically?" |
| `one-page-structurer.md` | "Can a human see the money flow at a glance?" |
| `proposal-closer.md` | "Would the customer pay for this document?" |
| `chain-orchestrator.md` | input → screen → (NO? stop) → structure → proposal |
| `_registry.md` | YOUR assets/context — the only file you must edit |

Install: copy a module to `~/.claude/skills/<name>/SKILL.md`, fill `_registry.md`, replace `{{...}}` placeholders. Your corrections to a module's output feed the same evolution loop as everything else — modules get sharper the way rules do.
