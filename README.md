# reward-hacking propagation

v11 experiments used in the paper: 198 stage-1 runs, 26 RQ3 cases, 728 calls.

## setup

python 3.11+

```sh
git clone https://github.com/Isct123/reward-hacking-propagation.git
cd reward-hacking-propagation
python -m venv .venv
```

activate the environment:

```sh
# linux / macos
source .venv/bin/activate

# windows powershell
.\.venv\Scripts\Activate.ps1
```

```sh
python -m pip install -r requirements.txt
python setup_benchmark.py
```

set these before opening jupyter:

- `OPENROUTER_API_KEY`: your API key
- `RH_PRIVATE_MATERIAL`: path to the private material JSON

private JSON fields:

- `patient_zero_private_history`, `honest_seed_private_history`: ordered lists of `{"role": ..., "content": ...}` messages
- `patient_zero_trigger_directive`, `honest_trigger_directive`: original directive strings

private prompts and histories aren't included, so an exact live rerun needs them separately. published hashes identify the original histories; the loader doesn't verify their serialization.

```sh
python -m jupyterlab experiments.ipynb
```

run cells in order, from the repo root. paid API calls + local execution of generated code; use a disposable environment. no spending cap in this version. cost placeholders in new logs aren't measurements. historical model IDs may no longer be available; fresh runs can differ.

## files

- `experiments.ipynb`: stage 1 + RQ3
- `config/`: model/dataset pins, task IDs, history hashes
- `data/`: final tables and sanitized results; usable without API access
- `src/`: detectors, topologies, bootstrap
- `tests/`: detector and topology checks

```sh
python -m unittest discover -s tests -v
```

`sycophancy` = low/medium/high peer-deference condition. SWE-bench results are a behavioral audit, without repository test execution.
