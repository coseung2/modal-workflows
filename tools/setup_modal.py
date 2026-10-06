"""Plan or apply setup in the caller's Modal workspace, never the maintainer's."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def plan(target):
    commands = []
    if target in {'h3', 'image'}:
        commands.append(['run', 'modal/check_environment.py'])
    commands.append(['run', 'modal/bootstrap.py', '--target', target])
    commands.append(['deploy', {'h3': 'modal/workflow_h3.py', 'image': 'modal/workflow_image.py',
                                'music': 'modal/workflow_music.py'}[target]])
    return commands


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('target', choices=['h3', 'image', 'music'])
    parser.add_argument('--apply', action='store_true', help='Execute CPU build/download/deploy; can incur charges')
    args = parser.parse_args()
    models = json.loads((ROOT / 'easygen_runtime/models.json').read_text())
    print(json.dumps({'target': args.target, 'model_GiB': round(sum(x['bytes'] for x in models.get(args.target, []))/2**30, 2),
                      'commands': plan(args.target), 'GPU_generation': False}, indent=2))
    if not args.apply:
        return
    subprocess.run([sys.executable, '-m', 'modal', 'app', 'list', '--json'], cwd=ROOT, check=True)
    for command in plan(args.target):
        subprocess.run([sys.executable, '-m', 'modal', *command], cwd=ROOT, check=True)
    print(json.dumps({
        'setup_completed': args.target,
        'next_example': 'examples/README.md',
        'agent_next_step': '환경 준비가 끝났습니다. 도자기 컵 상업 광고 영상을 무드보드부터 내레이션·영상 생성·자막·최종 편집까지 완성해볼까요?',
        'before_execution': 'Confirm remaining runtimes, TTS access, local editing tools, commercial-use suitability and approved cost scope. Do not re-ask H3 license status or approvals already given.',
        'GPU_generation': False,
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
