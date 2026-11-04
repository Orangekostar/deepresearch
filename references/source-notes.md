# Scholarly and engineering sources / provenance

Version anchors used to produce the **research-method interpretation**. Consult the original article when quoting exact results, mathematical objectives, axes and model settings; links are scholarly sources, not evidence of user experiment execution.

| Reference | Role |
|---|---|
| [OGPO: Sample Efficient Full-Finetuning of Generative Control Policies, arXiv 2605.03065v4](https://arxiv.org/abs/2605.03065v4) | Primary worked example: off-policy critic, generative policy optimization, critic overexploitation, modal/component controls |
| [Diffusion Policy Policy Optimization (DPPO), 2409.00588v3](https://arxiv.org/abs/2409.00588v3) | Representation and optimizer comparison |
| [Much Ado About Noising, 2512.01809v3](https://arxiv.org/abs/2512.01809v3) | Confounder control and subtractive research design |
| [Cal-QL, 2303.05479v4](https://arxiv.org/abs/2303.05479v4) | Offline→online diagnostic and calibrated interfaces |
| [V-GPS, 2410.13816](https://arxiv.org/abs/2410.13816) | Adaptation at candidate-selection locus |
| [DSRL, 2506.15799](https://arxiv.org/abs/2506.15799) | Adaptation at generative input-noise locus |
| [karpathy/autoresearch](https://github.com/karpathy/autoresearch/tree/228791fb499afffb54b46200aca536f79142f117) | Fixed evaluation, baseline-first iterative experiment workflow; no source code copied |

### Nearest-prior-work checking entry points

- Flow-GRPO: <https://arxiv.org/abs/2505.05470>
- FQL: <https://arxiv.org/abs/2502.02538>
- QAM: <https://arxiv.org/abs/2601.14234>
- Persistent Robot World Models: <https://arxiv.org/abs/2603.25685>
- DRILL: <https://arxiv.org/abs/2610.30814>

**Scope / science limitations**

1. This package distills transferable *methodological moves*; it neither attributes private thought processes to authors nor reproduces cited experiments.
2. OGPO works on generative **control policies**. Equating them with a predictive **world model** is incorrect without explicitly identifying state and time dynamics.
3. Source figures include different selection and metric conventions. For example, OGPO Fig.4 reports trajectory length conditional on success; Fig.16 is not a gradient-norm plot; Fig.15 text/caption require careful audit before asserting an orthogonal-variance interpretation.
4. The earlier figure study identified frequent monospace bold fonts and low-opacity ribbons in selected vector panels, not a uniform author-provided Origin theme.
5. New suggestions (independent confirmation, mandatory source ledger, style recipes, scripts) are **our design recommendations**, not claimed author procedures.
6. An earlier private skill version may contain additional unexposed files. This self-contained GitHub package is a **reconstructed distributable implementation** of the documented workflow, not a verified byte-identical export of that personal skill.
