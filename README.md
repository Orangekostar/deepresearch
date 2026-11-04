# DeepResearch — OGPO-style Research Method Skill

A reusable research agent skill for **innovation discovery → evidence-driven experimental design → bounded autoresearch → Origin-style data figures → defensible research writing**.

> 中文说明：这是基于 OGPO、相关作者工作与 karpathy/autoresearch 的研究方法归纳，并非 OGPO 官方技能、算法复现或原作者对本项目的认可。

## Quick start

Point your coding/research agent to the repository's [`SKILL.md`](SKILL.md) and ask:

```text
请按 deepresearch/SKILL.md 执行“创新发现 + 最小辨识实验”模式。
研究问题：……
现有仓库路径：……
已有实测结果：……
预算：最多 8 次实验，累计训练/评价命令不超过 2 小时；预留独立确认。
请先审计最近工作和学习对象，再给创新候选、归因实验、Origin 图表计划、论文主张。
只有真实可运行代码和明确授权时才执行实验；不得编造结果。
```

## Architecture

```text
REAL PROBLEM / MEASURED FAILURE
     ↓
Innovation discovery: transfer eligibility + closest prior art + falsifier
     ↓
Research contract: learning object + expensive/cheap interfaces + budget
     ↓
Identification experiments: baseline + direct transfer + minimal adaptation
     ↓
Bounded autoresearch: log each actual run, failure, version and cost
     ↓
Independent confirmation + mechanism & scope tests
     ↓
Origin-style plot contract and reproducible data transforms
     ↓
Claim ↔ Evidence ↔ Figure ↔ Manuscript
```

## Included modules

| Path | Purpose |
|---|---|
| [`SKILL.md`](SKILL.md) | Main skill instructions, mode routing, decision gates |
| [`references/innovation-discovery.md`](references/innovation-discovery.md) | Seven innovation moves, cross-domain transplant contract, novelty delta |
| [`references/innovation-casebook.md`](references/innovation-casebook.md) | OGPO, DPPO, MIP, Cal-QL, V-GPS, DSRL case studies |
| [`references/experiment-design.md`](references/experiment-design.md) | Strong baselines, causal contrasts, uncertainty, costs, failures |
| [`references/experiment-figure-atlas.md`](references/experiment-figure-atlas.md) | Figure-to-scientific-question cards and plot recipes; verification boundaries |
| [`references/origin-style.md`](references/origin-style.md) | Origin data columns, themes/templates, stable style mappings, export checks |
| [`references/autoresearch-protocol.md`](references/autoresearch-protocol.md) | Protocol freezing, evaluation adapter, search vs confirmation, stop/recover |
| [`references/writing-blueprint.md`](references/writing-blueprint.md) | Evidence-led paper structure, figure-caption and claim constraints |
| [`references/source-notes.md`](references/source-notes.md) | Primary and secondary scholarly/project sources |
| [`assets/`](assets/) | Project instructions, briefs, evidence ledger, JSON configs and CPU demo |
| [`scripts/autoresearch_loop.py`](scripts/autoresearch_loop.py) | Bounded trial runner (one experiment per explicit invocation) |
| [`scripts/audit_evidence.py`](scripts/audit_evidence.py) | Structural integrity audit of claims and evidence |
| [`scripts/prepare_origin_data.py`](scripts/prepare_origin_data.py) | Long-form replicate CSV → Origin-friendly mean and interval CSV |
| [`scripts/render_origin_style.py`](scripts/render_origin_style.py) | Matplotlib vector preview using semantic style profiles |

## Demo: real CPU evaluation, not OGPO reproduction

Python 3.10+ is required. The core runner, evidence audit, and data preparation need only Python's standard library; optional preview requires `matplotlib`.

```bash
cd deepresearch-skill
mkdir -p work/demo
cp assets/demo/{evaluate.py,train_config.json,autoresearch.json} work/demo/
python3 scripts/autoresearch_loop.py init --config work/demo/autoresearch.json --state work/run-state
python3 scripts/autoresearch_loop.py run --state work/run-state --role baseline --hypothesis H0 --seed 7
# Edit *only* work/demo/train_config.json, then run a candidate:
python3 scripts/autoresearch_loop.py run --state work/run-state --role candidate --hypothesis H1 --seed 7
python3 scripts/autoresearch_loop.py status --state work/run-state
```

**Important:** `--role confirmation` does not restore or switch models for you. Restore the corresponding baseline/candidate snapshot before each paired run, and check saved file hashes. Never compare search and confirmation metrics as if from the same evaluation protocol.

Plotting preparation:

```bash
python3 scripts/prepare_origin_data.py examples/learning-curves.csv \
    --output work/origin-summary.csv --interval sd --independent-unit seed
python3 scripts/render_origin_style.py work/origin-summary.csv \
    --styles assets/style_profiles.json --profile origin_publication \
    --output work/learning-curves.pdf
```

The example dataset is synthetic, not paper data.

## Compatibility and boundaries

- Skill format: Markdown frontmatter in `SKILL.md` + progressive-disclosure references. Usable by file-reading research or coding agents. Native auto-discovery varies by client.
- Runner: single explicit command, no LLM API, daemon, or background job scheduler. Python 3.10+ on POSIX Linux/macOS. It does not sandbox arbitrary evaluation code.
- Runner budget: trials, per-run seconds, cumulative command-run seconds and consecutive failures. GPU-hours, environment interactions and API spending need separate project-level enforcement.
- `source_faithful` and `origin_publication` are **adapted style recipes**, not exact recovered plotting source or native `.oth/.otp/.otpu` files.
- Figures and metrics must be computed from real experiments; failed executions produce missing data, while measured zero success is preserved as zero.
- The evidence auditor checks file/ID/state consistency, not the truth of results, statistical validity, or novelty.

## Upload to GitHub

This directory may be committed as the **root** of an existing empty `Orangekostar/deepresearch` repository (or inside `skills/ogpo-research-to-paper/` if the repository already contains other files). Do not force-push or overwrite unrelated contents.

```bash
git clone https://github.com/Orangekostar/deepresearch.git
cd deepresearch
# Copy the *contents* of this directory here, inspect conflicts before replacing.
python3 -m unittest discover -s tests -v
git add . && git diff --cached --stat
git commit -m 'Add OGPO-style deep research skill with autoresearch and Origin plotting'
git push origin HEAD
```

A repository URL that returns 404 must first be created or made accessible to the account/token performing the push. This package is not evidence that a remote push succeeded.

## Credits / intellectual provenance

See [`references/source-notes.md`](references/source-notes.md). Original skill text and utility scripts are provided under [MIT](LICENSE); OGPO and cited upstream projects keep their respective rights. The approach is adapted, not a copy of their source code.
