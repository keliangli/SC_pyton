#!/usr/bin/env python3
"""
Publish daily GitHub agent news to SC_pyton repository.
"""

import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Hardcoded parameters for 2026-04-22
TRACK = "agent"
DATE = "2026-04-22"
SLUG = "multi-framework-opus-support-security-hardening"
TITLE = "GitHub 智能体日报（2026-04-22）- 多框架Opus 4.7适配与安全加固潮"
SOURCE = "/home/li/.openclaw/workspace/reports/github_agent_news_2026-04-22.md"

def run_cmd(cmd, cwd=None):
    """Run a shell command and return output."""
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running: {cmd}")
        print(f"stderr: {result.stderr}")
        return None
    return result.stdout.strip()

def main():
    # Parse date
    date_obj = datetime.strptime(DATE, "%Y-%m-%d")
    year_month = date_obj.strftime("%Y-%m")
    
    # Setup paths
    repo_root = Path("/home/li/.openclaw/workspace/SC_pyton")
    target_dir = repo_root / "openclaw_reports" / "daily_github_news" / TRACK / year_month
    target_filename = f"{DATE}-{TRACK}-{SLUG}.md"
    target_path = target_dir / target_filename
    
    # Ensure directory exists
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy source file to target
    source_path = Path(SOURCE)
    if not source_path.exists():
        print(f"Error: Source file {SOURCE} does not exist")
        sys.exit(1)
    
    shutil.copy2(source_path, target_path)
    print(f"Copied {source_path} -> {target_path}")
    
    # Configure git
    run_cmd('git config user.email "openclaw@local"', cwd=repo_root)
    run_cmd('git config user.name "OpenClaw Agent"', cwd=repo_root)
    
    # Add file
    rel_path = target_path.relative_to(repo_root)
    run_cmd(f'git add "{rel_path}"', cwd=repo_root)
    
    # Commit
    commit_msg = f"[{DATE}] {TITLE}\n\nTrack: {TRACK}\nSlug: {SLUG}"
    commit_result = run_cmd(f'git commit -m "{commit_msg}"', cwd=repo_root)
    if commit_result:
        print(f"Committed: {commit_result}")
        
        # Get commit hash
        commit_hash = run_cmd("git rev-parse --short HEAD", cwd=repo_root)
        print(f"Commit hash: {commit_hash}")
        
        # Save commit hash to file for later retrieval
        with open(repo_root / ".last_commit_hash", "w") as f:
            f.write(commit_hash if commit_hash else "")
    
    print(f"\nDone! File published to: {target_path}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
