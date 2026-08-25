# Context Limits

## File Size Limits

Every artifact is re-read by the orchestrator on each planning turn and by every worker and the
Verifier by section; size is paid on every read. The cap is a tripwire — the instrument is the
structural rule in [specify.md](specify.md) § *Size by scope* and [design.md](design.md) § *Size
by scope*: a line that is neither an AC nor a decision does not belong in the spec.

| File      | Small / Medium | Large / Complex          | Warning At (Large) |
| --------- | -------------- | ------------------------ | ------------------ |
| spec.md   | ≤ ~8 kB (~2k tokens) | 5,000 tokens (~20 kB) | 4,000 tokens |
| design.md | ≤ ~8 kB (Medium; skipped for Small) | 8,000 tokens (~32 kB) | 6,400 tokens |
| tasks.md  | inline plan or ≤ ~8 kB | 10,000 tokens (~40 kB) | 8,000 tokens |
| spike.md  | evidence annex, any size — read by Design and the Verifier only, never by workers or on every planning turn | same | — |

Measured in the origin project: a Medium feature carried a 20 kB spec + 16 kB
design + 8 kB tasks, re-read by the orchestrator each planning turn and by every worker.

## Context Zones

🟢 **Healthy** (<40k total): Silent
🟡 **Moderate** (40-60k): Discrete footer note
🔴 **Critical** (>60k): Active warning, suggest optimization

## Monitoring

Display context status in footer when >40k:

```
📊 Context: 52k tokens (moderate)
  - tasks.md: 11k (ok)
  - design.md: 6k (ok)
  - Total: 52k / 200k (26%)
```

## Principles

**Target:** <40k tokens loaded (20% of window)
**Reserve:** 160k+ tokens for work, reasoning, outputs
