# Evidence-to-paper writing blueprint

First write a **claim/evidence/figure matrix**; then select one appropriate narrative:

- Method paper: actual failure → new optimization/representation boundary → minimum method and necessary stability → primary benefit → mechanism evidence → limits.
- Mechanism paper: observed phenomenon → competing explanations → controlled substitutions/interventions → minimum sufficient implementation → counterexamples and scope.
- Diagnostic paper: failure symptom → measured internal quantity → precise operational definition → targeted repair → task-level benefit and cost.

These are rational **argument structures**, not the literal sequence of discoveries by OGPO authors.

## Section responsibilities

**Abstract:** problem, specific unmet need, mechanism, real verified main result with scope, caveat. If no results exist, write a proposal abstract or placeholder—not fabricated performance.

**Introduction:** engineering/decision objective, real loss, families of existing attempts and exact missing evidence, core mechanism, evidence scope. Avoid “lack of resources” unless documented; standardized area/time budgets are evaluation constraints, not necessarily engineering problems.

**Method:** what is learned; input/supervision/target; math of smallest method; critical stability modifications versus optional inference compute; assumptions that make borrowed methods applicable.

**Experiments:** each subsection answers one falsifiable question. State comparison and controls, data/protocol/independent unit, actual measurements and uncertainty, rival explanations weakened or unresolved, and implications for next decision.

**Related work:** group by changed mathematical interface and target setting, not keyword lists. Nearest prior art needs substantive differences and compatible baseline conditions.

**Conclusion:** verified benefit, conditions, actual cost, important failures and unresolved questions. No new untested result.

## Figure captions as compact validity statements

Caption = what was compared; input conditions and what was held constant; axes and budget; independent unit and `n`; statistics and interval definition; what observation supports; scope and omitted explanations. Strong titles are only allowed after real outcomes are available.

## Strength of words

- **Significantly** needs appropriate inferential analysis and independent units.
- **Causes/why** needs intervention capable of separating competitors; correlation or UMAP is a clue.
- **Efficient** needs exact resource axis: environment interactions, GPU compute, walltime, inference latency, etc.
- **Generalizes** needs relevant independent held-out domains/people/scenes/times.
- **No expert demonstrations** must say *which phase*; a pretrained BC policy may have used demonstrations.
- **First/novel** needs a scoped contemporary literature comparison, not missing hits in a quick search.

Never transform planned numbers, source paper results or example synthetic charts into project results. Attach each strong manuscript sentence to completed evidence and raw result paths. A genuine refutation is useful scientific information and must not be hidden to preserve a narrative.
