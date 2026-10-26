"""download the experiment version of ImpossibleBench"""
import io
import json
import sys
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
commit = json.loads((ROOT / 'config/run_plan.json').read_text())['impossiblebench_repo_commit']
target = ROOT / 'vendor' / 'impossiblebench'
if target.exists():
    raise SystemExit(f'{target} already exists. Reuse it, or move it aside before setup.')
url = f'https://codeload.github.com/safety-research/impossiblebench/zip/{commit}'
request = urllib.request.Request(url, headers={'User-Agent': 'reward-hacking-propagation'})
with urllib.request.urlopen(request, timeout=120) as response:
    payload = response.read()
with zipfile.ZipFile(io.BytesIO(payload)) as archive:
    prefix = f'impossiblebench-{commit}/'
    for item in archive.infolist():
        if item.is_dir():
            continue
        if not item.filename.startswith(prefix):
            raise ValueError('Unexpected archive root')
        destination = (target / item.filename[len(prefix):]).resolve()
        if not destination.is_relative_to(target.resolve()):
            raise ValueError('Unexpected archive path')
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(archive.read(item))
package = target / 'src' / 'impossiblebench'
mini = package / 'livecodebench_agent_mini.py'
mini.write_text(mini.read_text(encoding='utf-8').replace('from livecodebench_scorers import find_code', 'from .livecodebench_scorers import find_code'), encoding='utf-8')
(package / '__init__.py').write_text(
    'from .livecodebench_tasks import impossible_livecodebench, record_to_sample\n'
    'from .livecodebench_agent_mini import agentic_humaneval_solver, minimal_humaneval_solver\n'
    'from .livecodebench_scorers import humaneval_scorer, agentic_humaneval_scorer, find_code\n',
    encoding='utf-8',
)
# notebook handles the import path
print(f'Prepared ImpossibleBench {commit} at {target}')
