# Innovation discovery: from a failure to a defensible technical delta

## Rule 0: name the object, don't copy a buzzword

Is the target a generative *policy* π(a|o), a *world model* p(s′|s,a), a Q/critic, a planner, a retriever, or a downstream estimator? A group of responses conditioned on a prompt and multiple action proposals conditioned on an observation are structurally comparable **only if** the conditioning, sampling, score and update interfaces line up. An internal denoising trajectory is not automatically an environment rollout.

## Seven invention moves distilled from related research

1. **Re-representation (DPPO-type).** Identify which mathematical interface a mature optimizer expects; reformulate the target process without silently changing the objective. Verify probability, Markov assumptions, conditioning, and valid gradients. Test whether representation rather than optimizer drives the gain.
2. **Optimization boundary (OGPO-type).** Separate expensive environment/measurement interactions from cheap-ish replay, candidate generation and optimization. Measure the *actual* marginal cost on each side, then move a learning/update boundary. Test cheaper direct alternatives.
3. **Selective mechanism transfer (GRPO-like comparisons in OGPO).** Port the mechanism that fits (same-condition candidates and relative scores); re-derive assumptions about score normalization, stochasticity, rewards, policy likelihoods, importance weights and compute. Avoid “LLM post-training + world model” as a novelty claim.
4. **Turn failed transfers into mechanisms (OGPO-type).** A stronger extractor may exploit an imperfect critic. Measure proxy-vs-real divergence, state-distribution shift and error, then test a constrained repair. Check *both* diagnosis and task score.
5. **Subtractive explanation (MIP-type).** Remove a supposedly essential complexity under controlled architecture/data/training conditions. If a minimal substitute preserves performance, revise the supposed source of improvement.
6. **Stage-interface mismatch (Cal-QL-type).** Look at pretrain→finetune, offline→online, simulator→real, detector→planner transitions. A useful previous-stage estimate may be miscalibrated for the next stage. Evaluate startup drop, recovery time and cumulative cost, not only endpoints.
7. **Move adaptation locus (V-GPS/DSRL-type).** Compare modifying candidate selection, input noise, an intermediate evaluator, or model parameters. Identify reachability limits and whether computation shifts to deployment.

## Transfer eligibility card (mandatory before implementation)

| Question | Required evidence |
|---|---|
| Source mechanism | Exact input, output, objective, assumptions, source version |
| Target interface | Which object corresponds to condition, candidate, scorer, generator, update? |
| Mismatches | Deterministic vs stochastic, differentiability, credit assignment, offline vs on-policy, cost |
| Naive transfer | What happens if the original mature technique is used *without* the proposed modification? |
| Minimum adaptation | What is the smallest new operation needed and why? |
| Simple rival | Could calibration, ranking, weighted regression, extra samples or a smaller backbone suffice? |
| Falsifier | Under what result does the claimed novel mechanism fail? |
| Verification | Which experiment and raw artifact resolve this question? |

## Nearest-prior-art delta (required)

Use current literature search when asserting novelty. Historical paper interpretation and current invention priority are different tasks: record date, versions, exact implementation claims. Search *direct* adjacent ideas, e.g. Flow-GRPO, FQL, QAM for generated-policy RL; for world models inspect multi-future comparison and decision-relevant training before proposing those as novel.

| Closest prior art | Already achieves | Remaining measurable gap | Our exact delta | Why not the trivial extension | Decisive test |
|---|---|---|---|---|---|

Do not write “first,” “novel,” or “no prior work” solely because a limited search found no match. Under uncertainty use “proposed candidate pending further literature verification.”

## Selection and stop gates

Pick 2–4 structurally different candidates (objective, representation, optimization boundary, adaptation locus). Prioritize by: reality/importance of bottleneck; eligibility of mechanism; actual novelty delta; testability; computation/data cost; informative negative result. First run the smallest *decision-changing* test. Stop if a strong simple baseline matches performance, the direct transfer already solves the issue, a critical assumption fails, or the intended benefit is not real. Preserve negative evidence; redesign or narrow the claim.

## World-model example (hypothetical)

Observed: low one-step prediction error but weak model-based planning. Diagnose separately: horizon drift, poor candidate coverage, wrong selection among available candidates. If available, fix a shared set of candidate actions and obtain actual downstream returns; compare oracle best vs learned evaluator choice. This separates coverage from ranking. Candidate innovations could modify long-horizon training distribution, evaluate calibration under a fixed planner, or optimize for decision relevance. Check close precedents **before** calling reward-conditioned futures or group-rank world-model training novel. No real-world-model evidence is implied by this example.
