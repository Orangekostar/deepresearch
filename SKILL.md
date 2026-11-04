---
name: ogpo-research-to-paper
description: "用于生成机器学习与机器人交叉领域的真正可证伪研究创新，借鉴 OGPO/DPPO/MIP/Cal-QL 等研究策略与 autoresearch 自动实验循环，设计受控实验、逐图论证、Origin 风格数据图和证据一致的论文。适用于论文选题、仓库实验、机制与消融、图表及写作，不用于无数据的虚构 Results。"
---

# OGPO Style Deep Research Method

**Goal:** Convert a measurable scientific failure into a falsifiable and novel method, run bounded real experiments where authorized, then produce evidence-matched figures and manuscript claims.

Never assume that similarity to popular LLM post-training (PPO/GRPO, best-of-N, critic) proves a world-model or control-policy innovation. Separate **policy** (observation→action), **world model** (action/state→predicted future), **critic**, **search/planner**. Determine the actual learned object and algorithmic interface before transferring any technique.

## Route by requested stage

| User's materials | Read next | Deliver |
|---|---|---|
| A new research idea or paper | `references/innovation-discovery.md`, `references/innovation-casebook.md` | bottleneck, nearest prior art, 2–4 structurally distinct candidates, minimal decisive test |
| Experiment design or existing results | `references/experiment-design.md`, `references/experiment-figure-atlas.md` | question-to-control-to-falsifier table, independent-unit protocol, decision rules |
| Repo + executable evaluation + budget | `references/autoresearch-protocol.md`, `assets/program.md` | verified baseline, bounded trial ledger, provisional incumbent, independent confirmation |
| Origin graph or graph style | `references/origin-style.md`, `assets/style_profiles.json` | data contract, uncertainty definition, recipe, preview and native Origin steps |
| Writing or manuscript critique | `references/writing-blueprint.md`, `assets/evidence-ledger.json` | evidence-to-claim-to-figure mapping; complete requested prose with correct limits |

Read `references/source-notes.md` on first citation-heavy use. Never claim to have reviewed user code unless actually opened it.

## Research pipeline / hard gates

### Gate 1 — reality and learning object

Record: task and decision; measurable failure and baseline; input/information available at deployment; learnable variables; supervision/reward; output and downstream effect; actual engineering goal versus standardized evaluation constraints. Separate VERIFIED FACT / USER-REPORTED / HYPOTHESIS / RECOMMENDATION.

### Gate 2 — innovation discovery, not just stacking models

For each candidate: (i) closest prior work and version, (ii) transferable structural interface (condition, candidate, scorer, sampler, mathematical update), (iii) what fails on naive transfer, (iv) exact adapted mechanism, (v) minimum distinguishing experiment, and (vi) stop or narrow criteria. Do **not** claim novelty solely because two buzzwords are combined. Prefer a smaller explicit problem over an unsupported grand narrative.

Use the seven moves in innovation-discovery: re-representation; optimization-boundary shift; conditional mechanism transfer; failed-transfer diagnosis; subtractive counterexample; stage-transition mismatch; and moving the adaptation interface.

### Gate 3 — experiment design

First choose an experiment that can change a research decision, not a number of tables to fill. State competing explanations and their opposed predictions. Compare a strong baseline, direct-transfer baseline, minimal adaptation, simple alternative, core removal, and cost/scope tests **as needed**. Freeze all factors outside the scientific intervention; report unavoidable differences.

Every experiment card must include claim ID, independent sample unit, train/development/confirmation split, editable and fixed factors, data/model versions, primary and diagnostic metrics, budget, stop rule, outputs, and how the result would alter the claim.

### Gate 4 — bounded autoresearch

An agent may change only authorized project files. Freeze evaluation code/splits/metric, run a real baseline, alter one interpretable factor, run a candidate, retain all failures and hashes, and respect both search and confirmation budgets. `candidate_keep` is a **provisional development-metric** decision, not a science result. For confirmation, freeze the candidate first; use paired seeds or correct independent units, never repeatedly tune on the confirmation holdout. An unauthorized repository, unreachable data or absent evaluator yields an actionable plan, not invented run logs.

Scripts: `scripts/autoresearch_loop.py` and `scripts/audit_evidence.py`. The runner is not an unattended research agent or a safety sandbox.

### Gate 5 — figures as scientific arguments

Choose recipes R0–R8 in `references/experiment-figure-atlas.md`. Determine if each visual encodes a method, phase, time, independent unit or confidence interval. Keep sample size, statistic, band definition, axis unit and conditions explicit. Plot successful trials with valid zero values as zero; failed runs as NA with recorded cause. Do not interpolate missing checkpoints or imply significance through alpha transparency.

For Origin, use `references/origin-style.md`: tidy CSV → explicit aggregation → Origin columns (center/low/high or offsets) → theme/template with semantic style map → final physical export check. This repository supplies **matplotlib previews and Origin configuration guidance**, not native Origin assets.

### Gate 6 — evidence controls the manuscript

For every sentence of contribution, find its claim ID → completed experiment → raw artifact → relevant figure → scope and uncertainty. Missing result means planned or explicit placeholder, never fabricated results. Differentiate evidence for performance, mechanism, efficiency, generalization and causality. A visually persuasive UMAP or internal Q score does not establish task-level correctness.

Use method, mechanism, or diagnostic narrative based on the actual contribution. Keep counterexamples, weak tasks, budget differences and negative results. When evidence refutes the preferred story, revise the story.

## Deliverable quality check

- **Novelty**: nearest prior art and substantive delta are explicit, no premature priority claim.
- **Validity**: learning object, comparison unit, constraints and actual measurement are clear.
- **Reproducibility**: versions, snapshot, seeds, commands, outputs and failures traceable.
- **Figures**: data contract, intervals, colors/line types, exact axis meaning and caption scope.
- **Writing**: strongest claim supported; no universalization from local evidence.

Answer only the relevant parts; do not force all stages when user requests a narrower task.
