#!/usr/bin/env uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests",
#     "tomli",
#     "tomli-w",
# ]
# ///

import os
import sys
import argparse
from pathlib import Path
import requests
import tty
import termios
from typing import Dict
import difflib
from textwrap import indent
from datetime import datetime, timezone

try:
    import tomli
    import tomli_w
except ImportError:
    sys.exit("""
This script requires the tomli and tomli_w packages.
Install them with:
    pip install tomli tomli_w
""")

GIST_API_URL = 'https://api.github.com/gists'
CONFIG_FILE = Path('.gists.toml')
CONFIG_VERSION = 1

def parse_args():
    parser = argparse.ArgumentParser(
        description='Sync local files to GitHub Gists',
        epilog="""
Files listed in .gistignore will be excluded from new gist creation.
Each line in .gistignore is treated as a glob pattern, for example:
  *.tmp
  test_*.py
  *_test.sh

Examples:
  # Update existing gists in current directory
  ./sync_gists.py

  # Dry run to see what would be synced
  ./sync_gists.py --dry-run

  # Interactively add new files, offering to upload or ignore each
  ./sync_gists.py --create-new --interactive

  # Sync specific files, creating new gists if needed
  ./sync_gists.py --files script1.py script2.sh

  # Sync all scripts in a different directory
  ./sync_gists.py --folder ~/scripts --create-new
""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--folder', type=Path, default=Path.cwd(),
                       help='Folder path to sync (default: current directory)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Print actions without executing them')
    parser.add_argument('--create-new', action='store_true',
                       help='Create new gists for files not yet tracked (respects .gistignore)')
    parser.add_argument('--files', nargs='+', type=Path,
                       help='Specific files to sync')
    parser.add_argument('--interactive', action='store_true',
                       help='Interactively choose files to sync')
    parser.add_argument('--diff', action='store_true',
                       help='Show diff between local files and existing gists')
    return parser.parse_args()

def get_excluded_patterns():
    exclude_file = Path('.gistignore')
    if not exclude_file.exists():
        return set()
    return {pattern.strip() for pattern in exclude_file.read_text().splitlines() if pattern.strip()}

def get_existing_gists():
    response = requests.get(GIST_API_URL, headers=headers)
    response.raise_for_status()
    gists = response.json()
    return {
        next(iter(gist['files'])): gist['id']
        for gist in gists
        if gist['public'] is False
    }

def should_sync_file(file_path: Path, excluded_patterns: set) -> bool:
    return not any(file_path.match(pattern) for pattern in excluded_patterns)

def sync_to_gist(file_path: Path, gist_id: str = None, dry_run: bool = False):
    file_name = file_path.name
    content = file_path.read_text()

    if dry_run:
        action = "Would update" if gist_id else "Would create"
        print(f"{action} gist for {file_path}")
        return

    print(f"{'Updating' if gist_id else 'Creating'} gist for {file_path}... ", end='', flush=True)

    gist_data = {
        "description": f"Auto-synced gist for {file_name}",
        "public": False,
        "files": {
            file_name: {
                "content": content
            }
        }
    }

    if gist_id:
        # Update existing gist
        response = requests.patch(f"{GIST_API_URL}/{gist_id}", headers=headers, json=gist_data)
    else:
        # Create new gist
        response = requests.post(GIST_API_URL, headers=headers, json=gist_data)

    try:
        response.raise_for_status()
        result = response.json()
        print("done")
        print(f"  URL: {result['html_url']}")
        if not dry_run:
            save_gist_mapping(file_path, result['id'], result['html_url'])
    except requests.exceptions.HTTPError as e:
        print("failed")
        if e.response.status_code == 403:
            print("Error: GitHub token lacks required permissions.")
            print("\nFor fine-grained tokens:")
            print("1. Go to: GitHub Settings -> Developer Settings -> Fine-grained tokens")
            print("2. Ensure 'Gists: Read and write' is enabled under Account permissions")
            print("\nFor classic tokens:")
            print("1. Go to: GitHub Settings -> Developer Settings -> Tokens (classic)")
            print("2. Ensure the 'gist' scope is enabled")
            sys.exit(1)
        raise

def get_single_key() -> str:
    """Read a single keypress without requiring Enter."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def add_to_gistignore(pattern: str):
    """Add a pattern to .gistignore file."""
    with open('.gistignore', 'a') as f:
        f.write(f'{pattern}\n')

def interactive_sync(file_path: Path, dry_run: bool = False) -> bool:
    """
    Interactively handle a file that doesn't have a gist.
    Returns True to continue, False to quit.
    """
    while True:
        print(f"\nFile: {file_path}")
        print("[u]pload as gist, [x]clude (add to .gistignore), [s]kip (ask again next time), [q]uit? ", end='', flush=True)

        choice = get_single_key().lower()
        print(choice)  # Echo the choice

        if choice == 'q':
            return False
        elif choice == 's':
            print("Skipped. Will ask again next time.")
            return True
        elif choice == 'x':
            add_to_gistignore(file_path.name)
            print(f"Added {file_path.name} to .gistignore")
            return True
        elif choice == 'u':
            sync_to_gist(file_path, dry_run=dry_run)
            return True

def get_gist_content(gist_id: str) -> str:
    """Fetch the content of a gist from GitHub"""
    response = requests.get(f"{GIST_API_URL}/{gist_id}", headers=headers)
    response.raise_for_status()
    gist = response.json()
    # Get the content of the first (and should be only) file
    return next(iter(gist['files'].values()))['content']

def show_diff(file_path: Path, gist_id: str) -> bool:
    """
    Show diff between local file and gist.
    Returns True if there are differences, False if files are identical.
    """
    local_content = file_path.read_text().splitlines(keepends=True)
    try:
        response = requests.get(f"{GIST_API_URL}/{gist_id}", headers=headers)
        response.raise_for_status()
        gist = response.json()
        # Get the content and URL while we have the response
        gist_file = next(iter(gist['files'].values()))
        remote_content = gist_file['content'].splitlines(keepends=True)
        # Save the mapping even in diff mode
        save_gist_mapping(file_path, gist['id'], gist['html_url'])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching gist content: {e}")
        return True

    if local_content == remote_content:
        print(f"{file_path}: No changes")
        return False

    diff = difflib.unified_diff(
        remote_content, local_content,
        fromfile=f"{file_path} (gist)",
        tofile=f"{file_path} (local)",
        lineterm=''
    )
    diff_text = ''.join(diff)
    if diff_text:
        print(f"\nDiff for {file_path}:")
        print(indent(diff_text, '  '))
        return True
    return False

def sync_files_to_gists(files: list[Path], existing_gists: dict,
                       create_new: bool = False, dry_run: bool = False,
                       interactive: bool = False, show_diffs: bool = False):
    excluded_patterns = get_excluded_patterns() if create_new else set()

    for file_path in files:
        if not file_path.is_file():
            print(f"Warning: {file_path} is not a file, skipping")
            continue

        gist_id = existing_gists.get(file_path.name)
        if gist_id:
            if show_diffs:
                has_changes = show_diff(file_path, gist_id)
                if not has_changes:
                    continue
            sync_to_gist(file_path, gist_id, dry_run)
        elif create_new:
            if should_sync_file(file_path, excluded_patterns):
                if interactive:
                    if not interactive_sync(file_path, dry_run):
                        print("\nQuitting...")
                        break
                else:
                    sync_to_gist(file_path, dry_run=dry_run)
        else:
            print(f"Skipping {file_path} (no existing gist)")

def is_script(path: Path) -> bool:
    # Check file extension
    if path.suffix.lower() in {'.py', '.sh', '.rb'}:
        return True

    # Check if file is executable
    if os.access(path, os.X_OK):
        return True

    # Check for shebang
    try:
        with open(path, 'r') as f:
            first_line = f.readline().strip()
            return first_line.startswith('#!/usr/bin/env') or first_line.startswith('#!')
    except (UnicodeDecodeError, IOError):
        return False

def load_gist_mappings() -> Dict[str, str]:
    """Load gist mappings from .gists.toml"""
    try:
        with open(CONFIG_FILE, 'rb') as f:
            data = tomli.load(f)
            # Check version for future compatibility
            if data.get('version', 1) != CONFIG_VERSION:
                print(f"Warning: Config file version mismatch. Expected {CONFIG_VERSION}, got {data.get('version')}")
            return {
                filename: info['gist_id']
                for filename, info in data.get('files', {}).items()
            }
    except FileNotFoundError:
        return {}

def save_gist_mapping(file_path: Path, gist_id: str, gist_url: str):
    """Add or update a gist mapping in .gists.toml"""
    try:
        with open(CONFIG_FILE, 'rb') as f:
            data = tomli.load(f)
    except FileNotFoundError:
        data = {
            'version': CONFIG_VERSION,
            'metadata': {'last_sync': None},
            'files': {}
        }

    # Update metadata
    data['metadata']['last_sync'] = datetime.now(timezone.utc).isoformat()

    # Create the files table with all entries at the same level
    files = data.get('files', {})
    files[file_path.name] = {
        'gist_id': gist_id,
        'url': gist_url
    }

    # Reconstruct the full data structure
    new_data = {
        'version': data.get('version', CONFIG_VERSION),
        'metadata': data['metadata'],
        'files': files
    }

    with open(CONFIG_FILE, 'wb') as f:
        tomli_w.dump(new_data, f)

def main():
    args = parse_args()

    github_token = os.environ.get('GITHUB_TOKEN')
    if not github_token:
        sys.exit("Error: GITHUB_TOKEN environment variable not set")

    global headers  # Update the global headers with the token
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Load local tracking file
    tracked_gists = load_gist_mappings()

    # Fetch from API as fallback
    try:
        api_gists = get_existing_gists()
        # Merge API results with local tracking, preferring local tracking
        existing_gists = {**api_gists, **tracked_gists}
    except requests.exceptions.RequestException as e:
        print("Warning: Could not fetch gists from GitHub API, using local tracking only")
        existing_gists = tracked_gists

    if args.files:
        files = args.files
    else:
        files = [
            path for path in args.folder.iterdir()
            if path.is_file() and is_script(path)
        ]

    sync_files_to_gists(
        files,
        existing_gists,
        args.create_new,
        args.dry_run,
        args.interactive,
        args.diff
    )

    if not args.dry_run:
        print("Sync complete.")

if __name__ == '__main__':
    main()
