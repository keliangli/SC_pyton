#!/usr/bin/env python3
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

TRACK_LABELS = {
    'inference': '大模型推理',
    'agent': '智能体',
}

SLUG_RE = re.compile(r'^[a-z]+(?:-[a-z]+){2,7}$')


def run(cmd, cwd=None, check=True):
    proc = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if check and proc.returncode != 0:
        raise RuntimeError(
            f"command failed: {' '.join(cmd)}\nstdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
        )
    return proc


def yaml_escape(text: str) -> str:
    return text.replace('\\', '\\\\').replace('"', '\\"')


def main():
    parser = argparse.ArgumentParser(description='Publish a daily GitHub news report into SC_pyton.')
    parser.add_argument('--track', required=True)
    parser.add_argument('--date', required=True)
    parser.add_argument('--slug', required=True)
    parser.add_argument('--title', required=True)
    parser.add_argument('--source', required=True)
    parser.add_argument('--commit', action='store_true')
    parser.add_argument('--push', action='store_true')
    args = parser.parse_args()

    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', args.date):
        raise SystemExit('--date must be YYYY-MM-DD')
    if not SLUG_RE.fullmatch(args.slug):
        raise SystemExit('--slug must be 3-8 lowercase words joined by hyphens')

    source_path = Path(args.source).expanduser().resolve()
    if not source_path.is_file():
        raise SystemExit(f'source report not found: {source_path}')

    repo_root = Path(run(['git', 'rev-parse', '--show-toplevel']).stdout.strip())
    year_month = args.date[:7]
    rel_repo_path = Path('openclaw_reports') / 'daily_github_news' / args.track / year_month / f'{args.date}-{args.track}-{args.slug}.md'
    target_path = repo_root / rel_repo_path
    target_path.parent.mkdir(parents=True, exist_ok=True)

    source_text = source_path.read_text(encoding='utf-8').rstrip() + '\n'
    track_label = TRACK_LABELS.get(args.track, args.track)

    frontmatter = (
        '---\n'
        f'title: "{yaml_escape(args.title)}"\n'
        f'date: {args.date}\n'
        f'track: {track_label}\n'
        f'slug: {args.slug}\n'
        f'source_report: {source_path}\n'
        f'repo_path: {rel_repo_path.as_posix()}\n'
        'generated_by: openclaw\n'
        '---\n\n'
    )

    target_path.write_text(frontmatter + source_text, encoding='utf-8')

    commit_sha = ''
    if args.commit:
        paths_to_add = [str(rel_repo_path)]
        script_rel = Path('scripts/publish_daily_news_to_scpyton.py')
        if (repo_root / script_rel).exists():
            paths_to_add.append(str(script_rel))
        run(['git', 'add', *paths_to_add], cwd=repo_root)

        diff_cached = run(['git', 'diff', '--cached', '--name-only'], cwd=repo_root).stdout.strip()
        if diff_cached:
            msg = f'Add daily {args.track} GitHub news for {args.date}: {args.slug}'
            run(['git', 'commit', '-m', msg], cwd=repo_root)
            commit_sha = run(['git', 'rev-parse', 'HEAD'], cwd=repo_root).stdout.strip()
        else:
            commit_sha = run(['git', 'rev-parse', 'HEAD'], cwd=repo_root).stdout.strip()

    if args.push:
        run(['git', 'push', 'origin', run(['git', 'branch', '--show-current'], cwd=repo_root).stdout.strip()], cwd=repo_root)
        if not commit_sha:
            commit_sha = run(['git', 'rev-parse', 'HEAD'], cwd=repo_root).stdout.strip()

    print(f'TARGET_PATH={target_path}')
    print(f'REPO_PATH={rel_repo_path.as_posix()}')
    print(f'COMMIT_SHA={commit_sha}')


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        raise
