# reward-hacking propagation

code and results for the paper: when one AI agent games a coding test, do the other agents copy it?

v11 run used for the findings: 198 runs, 26 follow-up cases, 728 follow-up calls.

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

set your API key and the path to the private experiment inputs:

```sh
# linux / macos
export OPENROUTER_API_KEY="your-key"
export RH_PRIVATE_MATERIAL="/path/to/private.json"
```

```powershell
# windows powershell
$env:OPENROUTER_API_KEY = "your-key"
$env:RH_PRIVATE_MATERIAL = "C:\path\to\private.json"
```

private prompts and example histories aren't in this repo. rerunning the original experiment needs them separately. the JSON needs:

- `patient_zero_private_history`, `honest_seed_private_history`: lists of `{"role": ..., "content": ...}` messages
- `patient_zero_trigger_directive`, `honest_trigger_directive`: the two original instruction strings

```sh
python -m jupyterlab experiments.ipynb
```

open from the repo folder, then run cells in order. calls cost money; no spending limit built in. generated code runs locally, so use a disposable environment. old model IDs may no longer work, and new runs can differ.

## what's here

- `experiments.ipynb`: main experiment + follow-up (RQ3)
- `config/`: exact model versions, dataset versions and task IDs
- `data/`: paper results; no API key needed to read these
- `src/`: code for spotting test-gaming behavior, building agent networks and estimating uncertainty
- `tests/`: checks for the detector and network code

```sh
python -m unittest discover -s tests -v
```

notes: `sycophancy` means how much an agent is told to defer to peers. SWE-bench checks look at behavior only; repository tests weren't run. history hashes are references, not checked by the loader. zero cost fields in new logs are placeholders.
