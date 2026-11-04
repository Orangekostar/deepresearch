# Autoresearch protocol (bounded, reproducible and evidence-sensitive)

The external research agent chooses one scientific modification at a time. `autoresearch_loop.py` runs **one** user-authorized experiment per CLI call and records results; it is not a reasoning engine or persistent daemon.

## Lock the experiment contract before search

- Define actual learning object, hypothesis, competing explanations, baseline state, primary metric/direction, minimum *practical* gain (not p-value).
- Distinguish fixed benchmark/evaluator/splits from editable model code/config. For a non-Git demo, copied project files are checked by declared-file hashes; this is not a sandbox. For scientific projects, use isolated Git worktrees and preserve full commit/environment/data hashes.
- Set finite `max_trials`, `per_trial_seconds`, `max_total_seconds`, `max_consecutive_failures`. This runner does not enforce GPU-hour, purchased API cost or environment interactions; implement external bounds for those.
- Reserve separate time/trials for baseline, failures and independent confirmation. Plan actual independent units.
- Record the actual evaluation command. A JSON file containing a hand-written score is **not** a valid research evaluator.

## Config example

See `assets/autoresearch-config.example.json` and `assets/demo` for a working contract.

The evaluation command receives:

- `OGPO_PHASE` = `search` or `confirm` (confirmation data must be separate)
- `OGPO_SEED` = integer provided on CLI and actually used by evaluation
- `OGPO_RESULT_PATH` = fresh absolute path to metrics JSON
- `OGPO_TRIAL_ID` = unique trial identifier

Return 0 only after writing e.g. `{"metrics":{"mse":0.0123},"details":{"split":"dev","independent_unit":"seed"}}`. The number is a **schema example**, not an observed result. The chosen metric must be finite and numeric. Evaluator must validate dataset count and permission separately.

## Execute search and confirmation

```bash
python3 scripts/autoresearch_loop.py init --config PROJECT/autoresearch.json --state PROJECT_STATE
python3 scripts/autoresearch_loop.py run --state PROJECT_STATE --role baseline --hypothesis H0 --seed 7
# agent changes authorized files, saves source and rationale
python3 scripts/autoresearch_loop.py run --state PROJECT_STATE --role candidate --hypothesis H1 --seed 7
python3 scripts/autoresearch_loop.py status --state PROJECT_STATE
# After freezing a candidate and restoring correct baseline or candidate files each time:
python3 scripts/autoresearch_loop.py run --state PROJECT_STATE --role confirmation --hypothesis H1 --seed 101 --label baseline-confirm-101
python3 scripts/autoresearch_loop.py run --state PROJECT_STATE --role confirmation --hypothesis H1 --seed 101 --label candidate-confirm-101
python3 scripts/autoresearch_loop.py finish --state PROJECT_STATE --reason 'Verification completed'
```

Labels do **not** change model files. The user/agent must restore the actual corresponding snapshot between paired runs and check source hashes. Confirmation results do not promote search incumbents automatically. Invalid output, nonzero exit, timeout or evaluator/protected file drift all count as failures, never score 0.

## Interpretation boundary

`candidate_keep` means the fixed *development metric* exceeded a declared threshold. The independent confirmation might disagree; the mechanism can still be unsupported; a different budget or dataset can reverse the result. Generate a manuscript claim only after reading raw artifacts, correct independent units and all relevant negative experiments.

A runner that allows arbitrary evaluation commands is not a security sandbox. Do not execute untrusted repositories or expand authorization to data export, paid services or publishing. On damaged state history, retain original files and reconstruct after inspection instead of deleting logs. If an external process is detached from its process group, POSIX group termination is not guaranteed to stop it.
