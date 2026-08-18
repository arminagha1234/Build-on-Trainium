# Autonomous overnight optimizer — Trainium

An agent-driven optimizer that runs on a Trainium instance and keeps improving
models overnight — no human in the loop. It cycles a seed model list forever,
promotes what it learns into a shared knowledge bank, and compounds those
lessons across subsequent models and cycles. Each cycle writes a leaderboard
and per-model trajectory charts.

Framework code lives in [`trainium-optimizer`](https://github.com/arminagha1234/trainium-optimizer).
This folder is a **snapshot** of one overnight run's output.

## Latest leaderboard (native-pytorch on trn2.48xlarge)

| Model      | Baseline (tok/s) | Best (tok/s) |   Speedup |
|------------|-----------------:|-------------:|----------:|
| Qwen3-0.6B |            3,196 |   **44,100** | **13.80×** |
| Qwen3-1.7B |            2,779 |   **30,704** | **11.05×** |
| Qwen3-4B   |            1,893 |   **20,423** | **10.79×** |
| Qwen3-8B   |            1,806 |   **15,454** |  **8.56×** |
| Qwen3-32B  |            1,004 |    **7,909** |  **7.88×** |

Measured on real hardware (torch 2.12.1 · torch\_neuronx 2.12.3 · neuronx\_cc 2.27
· nki 0.6.0 · driver 2.30.2.0). The dominant Stage-1 lever is
`torch.compile(backend="neuron")` — the search reliably finds it because
`compile_mode` is tried before every other axis and no soft stopping condition
fires until each axis has been explored.

## Two seeds still need adapters

| Model | Why it's not there yet |
|-------|------------------------|
| Gemma-4-31B  | heterogeneous per-layer head layout; needs a family adapter for `k_proj.view(...,-1,512)` under uniform sharding |
| Qwen3.8-27B  | 4 KV heads cap the simple GQA plan at TP=4 where 27B weights don't fit a 24 GB core; needs KV-head replication or vocab-parallel embed/lm_head to reach TP=8 |

A partial adapter (GQA→MHA expansion) has already landed on the box; a full
family-specific adapter is the next piece of work.

## Charts

The staircase is written every cycle by the framework. Each step is an
optimization *idea* (torch.compile, SDPA, TP=4, …), not an axis name. The final
red `Nx` is the accumulated speedup vs the eager baseline.

- Hero (new "highlights" style): [`charts/qwen3-0-6b-highlights.png`](./charts/qwen3-0-6b-highlights.png)
- Detail (every attempt, incl. discards): `charts/<model>-timeline.png`

## What made this run keep improving

Full technical notes in [`NIGHT_LEARNINGS.md`](./NIGHT_LEARNINGS.md). The short
version:

1. **The search must try `compile_mode` early.** With the old order + a 5-round
   no-improvement stop, small models never reached compile (they'd stop at
   1.06×). Compile-first + explore-every-axis-before-stopping raised Qwen3-0.6B
   from 1.06× to 13.80×.
2. **Cross-chip TP works on Trn2.** The Trn1 device-barrier failure does not
   reproduce; TP=8 all\_reduce + full forward verified.
3. **TP is bounded by the model, not the box.** The old `[1, 2, 4, 8]` cap was
   artificial — the proposer now sweeps up to the instance core count (64 on
   trn2.48xlarge). What actually bounds clean TP is `num_kv_heads`.
4. **DP replicas fill the rest of the instance.** For a 27B model capped at
   TP=4, that leaves 60 idle cores; the fill planner adds `dp = cores // tp`
   so every candidate uses the whole box.
5. **The bank compounds across cycles.** Auto-promotion moves a lesson from
   `provisional/` to `verified/` when it clears the explicit criteria (≥N
   models, ≥N families, correctness gate) — so seed N+1 starts from what seed
   N proved.

## How to read the chart

Blue dots on a staircase — every improvement is a step up. Grey dashed lines
divide **Stage 1 (config)** from **Stage 3 (borrow)** from **Stage 4 (invent)**
from **Stage 5 (graph rewrite)**. Where a giant red `Nx` sits at the top-right
of the last point, that's the total speedup vs the eager baseline.

## Where the framework lives

- Framework repo: [`trainium-optimizer`](https://github.com/arminagha1234/trainium-optimizer)
- Model ports (for warm-starts): [`Armin-Neuron`](https://github.com/arminagha1234/Armin-Neuron)
