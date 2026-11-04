# Experiment → Figure Atlas (OGPO-inspired)

The prior analysis counted **25 numbered figures and 8 tables** in OGPO v4. This file provides **traceable, known examples and a general figure-card framework**, not a claim that every panel was independently remeasured here. Re-open source v4 when assigning exact subplot titles, legends, axes or statistics.

## Individually grounded experiment-to-figure examples

| Source element | What scientific question it helps answer | Key comparison or diagnostic | Reuse recipe | Important reading boundary |
|---|---|---|---|---|
| **Fig. 2** | How are expensive environmental interaction and internal generative updates reorganized? | Flow/data/update diagram | R0 | Method schematic, not empirical evidence |
| **Fig. 4** | Does stronger optimization exploit an imperfect critic; what stabilization matters? | Task outcome + failure/length diagnostics | R3 | Length conditional on **successful** trajectories only |
| **Fig. 5** | Which subsystem (actor or critic input modality) accounts for a failure? | Crossed 2×2 modality swaps | R2 | Avoid one-factor claim if other inputs changed |
| **Fig. 6** | Do success replay and inference-time Best-of-N contribute independently? | Ablations / combination factors | R2 | Separate computational search gain from core update |
| **Fig. 7** | Are learned Q estimates calibrated against realized return? | Q vs Monte Carlo returns | R4 | Rollouts are not independent training repetitions |
| **Figs. 9–12** | Does performance change across challenge conditions? | Per-task learning curves and conditions | R1 | Match budgets; avoid overclaim across tasks |
| **Figs. 13–15** | What behavior/exploration geometry changes? | Trajectory, action, projection diagnostics | R5/R6 | Original-space tests needed; Fig.15 caption/body orthogonal-variance wording needs audit |
| **Fig. 16** | How do different objectives vary with training? | Losses, Q, success | R3 | Figure does not directly measure gradient norms |
| **Table 2 / Fig. 17** | How much does the extraction objective matter under fixed framework? | Shared-interface alternatives | R2 | Same framework controls key confounders |

For unlisted numbered figures/tables, make a new source-verified card before using its exact content. An unidentified panel must be marked **NOT_YET_VERIFIED**, never guessed from a theme.

## Reusable recipe taxonomy

| Recipe | Question | Data contract | Visual language |
|---|---|---|---|
| R0 / schematic | Why modify this interface? | labelled components, direction, train/inference states | restrained blocks and arrows; no invented numbers |
| R1 / learning curves | Does quality improve with experience? | panel, method, replicate, checkpoint, outcome | method-ID colors; mean line; declared interval; shared legends |
| R2 / factorial | Which factor matters? | condition, factorA, factorB, independent unit, score | grouped/paired points and interaction bars; truthful missing cells |
| R3 / diagnostics | Does an internal quantity track outcome? | run, checkpoint, metric, value, unit | aligned X; separate Y scales for different quantities |
| R4 / calibration | Does estimate match external truth? | id, estimate, reference, phase | XY scatter; matched scale; y=x line; residual check |
| R5 / trajectories | What behavior changed? | scene, rollout, time, x, y, phase | equal spatial aspect; one time colormap shared across panels |
| R6 / embedding/vectors | Does geometry suggest a mechanism? | projection ID, x0, y0, x1, y1, provenance | scatter plus vectors; label projection and scale |
| R7 / costs | What does performance cost? | budget unit, observed cost, quality, status | Pareto/frontier; mark unfinished/threshold-not-met |
| R8 / protocol/table | What is controlled and claimed? | method, train/test data, compute, status | consistent table annotations with units and provenance |

## Per-figure evidence card

```text
Figure ID / source:                 (paper figure or new Figure F#)
Decision the viewer should make:
Alternatives ruled out / remaining:
Data file and exact columns:
Axes, units, denominator, selected subset:
Independent unit, sample count, interval definition:
Visual color/line/facet assignments:
What is observed; what is interpretation:
What opposite result would look like:
Paper claim ID; caption; source/analysis version:
```

The purpose is not to imitate a signature palette at the expense of correctness. Use the actual figure's scientific role to choose a proper graphic.
