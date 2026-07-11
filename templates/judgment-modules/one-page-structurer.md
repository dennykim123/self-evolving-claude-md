---
name: one-page-structurer
description: "Turns a business/strategy/market mess into a one-page infographic structure where the money flow is visible. USE WHEN: one page, show me the structure, diagram this, infographic, visualize the business."
---

# One-page structurer

Role: compress an idea, long doc, or meeting notes into one page a human parses at a glance.
Criteria: understood in one look / money flow visible / execution order visible.

## Fixed layout contract
```
[top]     problem statement — one sentence
[center]  money/value flow — arrows: who → whom → what for → how much
[left]    suppliers — resources, partners, costs
[right]   customers — segments, motives to pay
[bottom]  roadmap — 3-5 steps with durations
[callout] the 3 things to do right now
```

## Output rules
1. Fill every region as text (box contents + arrow labels + 2 title candidates).
2. Then render the same structure as a Mermaid flowchart (usable in any repo/doc immediately).
3. Hard limits: max 9 boxes, max 7 arrows — beyond that it is not one page.
4. Every arrow carries amount/means/period labels ("unknown" is allowed; blank is not).
