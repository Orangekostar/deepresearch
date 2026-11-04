# Mechanism-first experimental design protocol

## Every experiment starts with a scientific question

```text
Experiment ID / linked claim ID:
Competing hypotheses and their opposed predictions:
Intervention; all co-changing factors:
Fixed inputs/model/backbone/samples/compute/evaluator:
Actual training, development, confirmation and test permissions:
Metric formula, unit, aggregation, denominator, direction:
Independent analytical unit and paired/repeated sampling plan:
Expected range, practical minimum improvement, uncertainty plan:
Run commands, seed, source/commit, environment, artifact output:
Budget: trials/time/GPU/interactions/API; stop and failure rules:
Result A → decision; B → decision; inconclusive → decision:
Intended Figure ID and strongest allowable manuscript sentence:
```

## Seven evidence questions

| Question | Design pattern | What it cannot establish by itself |
|---|---|---|
| Does the system help? | Competitive baselines with clear cost/sample disclosure | Why it helps |
| What caused the gain? | Controlled backbone/data/compute replacement | Generalization beyond tested settings |
| What mechanism changed? | Intervene on intermediate signal, test diagnostic **and** task outcome | Causality if unmeasured confounding remains |
| Which component is needed? | Minimum implementation, ablation, and key interaction factorial cells | Universally necessary design |
| Where does it fail? | Strong-initialization, easy tasks, scarce data, long-horizon or other meaningful challenges | All deployments |
| What does it cost? | Quality at equal observed samples, training walltime/compute, deployment latency measured separately | Overall efficiency from only one axis |
| Is it reliable? | Independent runs or groups, pre-specified paired comparison, uncertainty | Significance from a single seed |

## Crossed diagnostics

To distinguish two failing subsystems A/B, use 2×2: A-reference/B-reference, A-new/B-reference, A-reference/B-new, A-new/B-new. Disclose interactions and compute; a four-point picture alone does not show statistical significance.

For proxy estimators compare internal score against external outcome on a declared joint dataset. In a model-based planner: holding proposed actions fixed, examine coverage vs ranking; change the model *only* in a separate comparison. For a critic: measure Q relative to realized returns using the same sampling protocol where feasible.

## Critical validity boundaries

- A trajectory sampled during evaluation is not an independent trained model. Slices from one person are not independent people. A single scene can contain dependent views/objects.
- A failed run is a missing/invalid measurement; a successful run with measured 0 success rate **is zero**.
- A success-conditioned trajectory length measures only successful episodes; it does not directly measure all attempted costs.
- An uncertainty alpha of 0.12 is **visual transparency**, not a confidence level.
- An embedding projection cannot prove a high-dimensional geometric mechanism. Use original-space statistics and interventions.
- A figure of *loss* does not establish claims about gradients if gradient norms were not measured.
- Distinguish exploration and frozen independent confirmation. If confirmation data are used to choose a new variant, subsequent tests must be independent again.

## Priority and budget

Reserve budget for initial baseline, invalid runs, independent confirmation, mechanistic contrasts and limits. Do the cheapest experiment that can trigger **continue / narrow / redesign / stop** before scaling. Report negative results and non-replicated effects; never reconstruct optimistic values from planned targets.
