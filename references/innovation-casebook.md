# Casebook — six related examples, seven distinct invention moves

These are **analytical interpretations** of published work, not accounts of authors' private reasoning or the literal chronological discovery process. All transfer prescriptions are ours.

| Case | Primary observed construction (consult source version) | Transferable invention move | What can falsify a new candidate |
|---|---|---|---|
| **OGPO** (`2605.03065v4`) | Off-policy reusable critic + critic-derived terminal signal through multi-step policy generation with adapted PPO; critic over-exploitation studied and repaired | Separate expensive interactions from internal optimization; carry a compatible mature optimizer into a newly exposed update interface | Direct off-policy updates or extra samples achieve same benefit; critic error predicts no failure; compute erases sample advantage |
| **DPPO** (`2409.00588v3`) | Diffusion-policy fine-tuning using RL and a generative-process representation | Re-represent a generative process so a mature optimization tool applies | New representation invalid or gains actually from parameterization/backbone |
| **MIP** (`2512.01809v3`) | Examine common explanations for generative BC success; construct simplified controls to test components | Strongly controlled, **subtractive** causal reasoning | Putative essential component is not removed or other confounds change |
| **Cal-QL** (`2303.05479v4`) | Diagnose offline→online transitions and value calibration | Stage-boundary mismatch as research problem | No transition-specific issue; final metric-only effect due to different total updates |
| **V-GPS** (`2410.13816v2`) | Value-guided selection/steering of proposals from a base generative policy | Move adaptation to inference selection rather than retraining all policy parameters | Base policy's candidate coverage inadequate; inference cost overwhelms gains |
| **DSRL** (`2506.15799v2`) | Adapt latent noise distribution for pretrained generative policy to support RL | Move learning to input/latent distribution | Noise-space controllability too weak; matching full policy update dominates fairly |

### Reasonable nearest-neighbor entry points

- Flow-GRPO: <https://arxiv.org/abs/2505.05470>
- Flow Q-Learning: <https://arxiv.org/abs/2502.02538>
- QAM: <https://arxiv.org/abs/2601.14234>
- Persistent Robot World Models: <https://arxiv.org/abs/2603.25685>
- DRILL: <https://arxiv.org/abs/2610.30814>

These links are **search entry points**, not an exhaustive novelty audit; verify titles, mechanisms and versions against actual papers before claiming an exact overlap.
