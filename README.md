# README

- [Version Control \& Git Tools](#version-control--git-tools)
  - [Repository Management](#repository-management)
    - [`git-wtf`](#git-wtf)
    - [`git-show-merges`](#git-show-merges)
    - [`git-show-large-objects`](#git-show-large-objects)
    - [`git-rank-contributors`](#git-rank-contributors)
    - [`git-create-fixups`](#git-create-fixups)
    - [`git-apply-fixups`](#git-apply-fixups)
  - [AI-Assisted Git Tools](#ai-assisted-git-tools)
    - [`git-ai-squash-messages`](#git-ai-squash-messages)
- [git-ai-commit-with-message](#git-ai-commit-with-message)
    - [`git-ai-reword-message`](#git-ai-reword-message)
    - [`git-ai-squash-commit-messages`](#git-ai-squash-commit-messages)
    - [`git-ai-release-notes`](#git-ai-release-notes)
- [Media \& File Processing](#media--file-processing)
  - [Audio/Video Processing](#audiovideo-processing)
    - [`audiocat`](#audiocat)
    - [`describe-image`](#describe-image)
    - [`frames-to-video`](#frames-to-video)
    - [`imgcat`](#imgcat)
    - [`srt-dedup-lines`](#srt-dedup-lines)
    - [`trim-silence`](#trim-silence)
  - [File Management](#file-management)
    - [`fix-file-dates`](#fix-file-dates)
    - [`localize_cloud_files.sh`](#localize_cloud_filessh)
- [Development Tools](#development-tools)
  - [File Watching](#file-watching)
    - [`rerun`](#rerun)
  - [Build Tools](#build-tools)
    - [`clean-builds`](#clean-builds)
  - [Python Environment Management](#python-environment-management)
    - [`find-installed-python-environments`](#find-installed-python-environments)
    - [`list-python-environments`](#list-python-environments)
  - [Development Environment Tools](#development-environment-tools)
    - [`docker-machine-rename`](#docker-machine-rename)
    - [`jupyter-agent`](#jupyter-agent)
    - [`pboard-sync`](#pboard-sync)
    - [`run-manim`](#run-manim)
    - [`sync_gists.py`](#sync_gistspy)
- [System Administration](#system-administration)
  - [Network \& Security](#network--security)
    - [`disable-wsdl`](#disable-wsdl)
    - [`uninstall-juniper-connect`](#uninstall-juniper-connect)
    - [`whitelist_rabbitmq`](#whitelist_rabbitmq)
  - [Application Management](#application-management)
    - [`check-for-electron-apps.sh`](#check-for-electron-appssh)
    - [`dropbox-pause-unpause.sh`](#dropbox-pause-unpausesh)
    - [`list-electron-apps.sh`](#list-electron-appssh)
    - [`remove-mackups`](#remove-mackups)
    - [`uninstall-arq`](#uninstall-arq)
- [Browser \& Data Tools](#browser--data-tools)
  - [Browser Management](#browser-management)
    - [`chrome-tabs-to-md.sh`](#chrome-tabs-to-mdsh)
    - [`list-browser-urls.sh`](#list-browser-urlssh)
  - [Data Analysis \& Processing](#data-analysis--processing)
    - [`analyze-apple-healthkit-export.py`](#analyze-apple-healthkit-exportpy)
    - [`google_to_hugo.py`](#google_to_hugopy)
    - [`vote-counter.py`](#vote-counterpy)

This repository contains various utility scripts, primarily in Bash and Python, to assist with system management, development, and miscellaneous automation tasks.

## Version Control & Git Tools

### Repository Management

These script names begin with `git-`, so that they can be used as git
subcoommands, e.g. `git ai-commit` as an alternative to `git-ai-commit`.

#### `git-wtf`
Displays a readable summary of a repository's state, including branch relationships to remote repositories and other branches. Useful for working with multiple branches in complex repositories.

Copyright 2008--2009 William Morgan.

```bash
git-wtf
```

#### `git-show-merges`
Lists branches that have been merged into the current branch and those that have not. Useful for tracking the status of branches and their relationships within a repository.

```bash
git-show-merges [BRANCHES...] # Shows merge status of specified or all branches
```

#### `git-show-large-objects`
Displays the largest objects in a Git repository's pack files, helpful for identifying and potentially cleaning up large files in a repository.

```bash
git-show-large-objects
```

Written by Antony Stubbs, as `show-large-git-objects`.

#### `git-rank-contributors`
Ranks contributors based on the size of diffs they've made in the repository. This script can be valuable for creating contributor credit lists, although manual adjustments may be needed if contributors commit from multiple email addresses.

```bash
git-rank-contributors [-v] [-o] [-h] # -v for verbose, -o to obfuscate emails
```

#### `git-create-fixups`
Creates separate commits for each modified file, with commit messages that reference their previous commits. Part of a workflow with `git-apply-fixups` for efficiently managing related changes across multiple files.

Usage:
```bash
git-create-fixups [-n|--dry-run]
```

#### `git-apply-fixups`
Automatically reorders and optionally squashes fixup commits created by `git-create-fixups`. This provides an automated alternative to manually reordering commits in an interactive rebase.

**Workflow**:
1. Make changes to multiple files
2. Run `git-create-fixups` to create separate commits for each file
3. Run `git-apply-fixups` to automatically reorder (and optionally squash) the commits

**Usage**:
```bash
# Show proposed reordering without executing
git-apply-fixups --dry-run

# Reorder and mark fixups for squashing
git-apply-fixups --squash

# Only process recent commits
git-apply-fixups --since="2 days ago"
git-apply-fixups -n 10
```

**Options**:
- `--dry-run, -n`: Show proposed reordering without executing
- `--squash, -s`: Use 'squash' instead of 'pick' for fixup commits
- `--max-count, -n N`: Limit to processing the last N commits
- `--since DATE`: Process commits more recent than DATE (e.g. "2 days ago")

### AI-Assisted Git Tools

#### `git-ai-squash-messages`
Generates commit messages based on changes using AI assistance. Designed to streamline commit message creation and ensure consistent descriptions.

```bash
git-ai-squash-messages # Analyzes messages and proposes a combined commit message
```

## git-ai-commit-with-message
Generate and commit changes using AI messages.

```bash
git-ai-commit # Analyzes current changes and suggests commit message
```

#### `git-ai-reword-message`
Generates a new commit message for a specified commit based on analyzing its changes. Uses LLM to create a descriptive and accurate commit message that reflects the actual changes in the commit.

```bash
# Rewrite message for the most recent commit
git-ai-reword-message

# Rewrite message for a specific commit
git-ai-reword-message <commit-hash>

# Preview the new message without applying it
git-ai-reword-message -n

# Use a specific LLM model
git-ai-reword-message --model gpt-4

# Modify the message according to specific instructions
git-ai-reword-message --prompt "Make the message more concise"
```

#### `git-ai-squash-commit-messages`
Uses an AI language model to combine multiple git commit messages into a single, comprehensive message. Useful when squashing commits or preparing pull request descriptions.

```bash
# Combine the last 3 commit messages
git-ai-squash-commit-messages HEAD~3..HEAD

# Combine messages between specific commits
git-ai-squash-commit-messages abc123..def456

# Use a specific model
git-ai-squash-commit-messages -m gpt-4 HEAD~3..HEAD
```
#### `git-ai-release-notes`
Generates a blog post announcing a new version based on git commits. Uses a LLM
to create a well-structured announcement that categorizes and highlights the
most important changes.

```bash
# Generate a post from all commits
git-ai-release-notes

# Generate a post from the last 5 commits
git-ai-release-notes HEAD~5..HEAD

# Generate a post from commits between two tags
git-ai-release-notes v1.0..v1.1

# Generate a post from commits in the last day
git-ai-release-notes --since="1 day ago"

# Save the output to a file
git-ai-release-notes -o announcement.md

# Output raw markdown without rich formatting
git-ai-release-notes --raw

# Use a different tone/style
git-ai-release-notes --tone=technical    # More technical details
git-ai-release-notes --tone=casual       # Conversational style
git-ai-release-notes --tone=enthusiastic # Excited and energetic
git-ai-release-notes --tone=minimal      # Just the facts
git-ai-release-notes --tone=pirate       # Arr, matey! Pirate speak
git-ai-release-notes --tone=nerd         # For the technically obsessed
git-ai-release-notes --tone=apologetic   # Sorry for the update...
```

The script automatically determines the project name from any project files, or
failing that the remote repository name or the local directory name, but you can
also specify it with the `--project-name` option.

## Media & File Processing

### Audio/Video Processing

#### `audiocat`
Transcodes and concatenates audio files into a single output file. This script is helpful for batch processing or merging audio files for production.

```bash
audiocat [-o output.m4a] [FILES...] # Specify output file and input files
audiocat # Process all audio files in current directory
```

#### `describe-image`
Uses the OpenAI API to analyze images.

```bash
describe-image

```

#### `frames-to-video`
Converts a sequence of numbered image frames into a video file using ffmpeg. Automatically detects frame numbering format and supports customizable output settings.

```bash
frames-to-video [options] <input_dir> [output.mp4]

Options:
    -f, --fps N        Set framerate (default: 60)
    -r, --resolution WxH   Set output resolution (default: 1920x1080)
    -q, --quality N    Set quality (0-51, lower is better, default: 25)
```

#### `imgcat`
Displays images directly in the terminal, with support for `tmux`. This is useful for quick image previews or terminal-based visualization.

```bash
imgcat filename... # Display specified images
cat image.png | imgcat # Display image from stdin
```

#### `srt-dedup-lines`
Removes duplicate subtitle entries from SRT files by merging overlapping segments with identical text. Creates a backup of the original file and renumbers remaining segments.

```bash
srt-dedup-lines <srt_file>  # Processes file in place, creates .bak backup
```

#### `trim-silence`
Remove silence from the beginning and end of audio files. Supports various audio formats and quality settings.

```bash
# Basic usage (creates input_trimmed.m4a from input.m4a)
audiotrim input.m4a

# Convert to OGG with quality setting
audiotrim --format ogg --quality 3 input.m4a

# Convert to MP3 with specific bitrate
audiotrim --format mp3 --bitrate 192k input.m4a

# Adjust silence detection threshold (higher number = more aggressive)
audiotrim --threshold -30 input.m4a

# Show debug information
audiotrim --debug input.m4a

# Suppress output (except errors)
audiotrim --quiet input.m4a

# Isolate voice before processing
audiotrim --isolate input.m4a  # Uses Eleven Labs API if ELEVENLABS_API_KEY is set, otherwise uses Demucs locally

# Example output:
Isolating voice using Eleven Labs API...
✓ Voice isolation complete
✓ Successfully processed audio:
  • Original duration: 1:09:21.79
  • New duration: 1:09:19.18
  • Removed from start: 0:00.25
  • Removed from end: 0:02.36
  • Total silence removed: 0:02.61
  • Original size: 32.9MB
  • New size: 31.2MB
  • Size change: 1.7MB (-5.2%)

Dependencies:
- Required: pydub, typer, rich
- Optional:
  - For local voice isolation: demucs
  - For cloud voice isolation: requests (and ELEVENLABS_API_KEY environment variable)

Format-specific settings:
- **OGG**: Quality -1 (lowest) to 10 (highest), default ~3
- **MP3**: Quality 0 (best) to 9 (worst), default 4
- **M4A**: Quality 0 (worst) to 100 (best), default 80

Common bitrates:
- MP3: 32k-320k (common: 128k, 192k, 256k, 320k)
- AAC/M4A: 32k-400k (common: 128k, 256k)
- OGG: 45k-500k (common: 128k, 192k, 256k)

The script will append " trimmed" to filenames that contain spaces, and "_trimmed" to filenames without spaces.

#### `srt2paragraphs`
Converts SRT subtitle files into paragraphed text, using timing information and punctuation to intelligently break paragraphs. Removes `<b></b>` tags and joins related lines.

```bash
# Print processed text to stdout
srt2paragraphs input.srt

# Write to output file
srt2paragraphs input.srt -o output.txt

# Preview output without writing
srt2paragraphs input.srt --dry-run
```

### File Management

#### `fix-file-dates`
Standardizes or adjusts file dates and supports a dry-run option to preview changes. Useful for fixing inconsistent file timestamps, often in file management or archiving tasks.

```bash
fix-file-dates [-n|--dry-run] [-h|--help] FILES... # Preview or perform date fixes
```

#### `localize_cloud_files.sh`
Forces a local cache of all files in a directory by reading all bytes from the cloud storage. This can be useful for ensuring all files are downloaded locally, potentially improving performance for subsequent accesses.

```bash
localize_cloud_files.sh [DIR]  # Defaults to current directory if not specified
```

## Development Tools

### File Watching

#### `rerun`
Runs a given command every time filesystem changes are detected. This is useful for running commands to regenerate visual output every time you hit [save] in your editor.

```bash
rerun [OPTIONS] COMMAND
```

Source: https://gist.github.com/rubencaro/633cd90065d399d5fe1b56e46440d2bb

### Build Tools

#### `clean-builds`
A utility script that helps clean up build artifacts and cache directories in development projects. It recursively finds project directories (containing .git, package.json, etc.) and cleans their build and cache directories.

```bash
clean-builds [OPTIONS] [DIRECTORIES...]

Options:
    --dry-run    Preview what would be deleted
    --show-size  Show sizes of directories being removed
```

### Python Environment Management

#### `find-installed-python-environments`
Searches for installed Python environments and checks if they are in use. Useful for system administrators managing multiple Python versions and virtual environments.

```bash
find-installed-python-environments # Lists all Python installations with status
```

#### `list-python-environments`
Lists available Python installations, including virtual environments and Homebrew installations. Helps in identifying Python versions across different environments on a system.

```bash
list-python-environments
```

### Development Environment Tools

#### `docker-machine-rename`
Renames Docker machine instances, allowing for better organization of Docker environments.

```bash
docker-machine-rename OLD_NAME NEW_NAME
```

Adapted from https://gist.github.com/alexproca/2324c60c86380b59001f w/ comments from eurythmia

#### `jupyter-agent`
Launches Jupyter Notebook from a specified directory. Useful for setting up a consistent working environment for Jupyter Notebooks in a designated directory.

```bash
jupyter-agent
```

#### `pboard-sync`
Uses `rshell` to sync files to a pyboard device. This script facilitates transferring code or data to hardware running on a microcontroller.

This just wraps the `rshell` command, since I keep forgetting the syntax.

```bash
pboard-sync [DIR]  # Defaults to current directory if not specified
```

#### `run-manim`
Runs the Manim (Mathematical Animation Engine) through Docker. This script simplifies running Manim without needing local installations or configurations.

```bash
run-manim source.py [options] # Renders animation from source file
```

#### `sync_gists.py`
Synchronizes local script files with GitHub Gists. Supports interactive mode, dry-run, and diff viewing. Uses `.gists.toml` for mapping local files to gist IDs.

```bash
sync_gists.py [OPTIONS] [FILES...]

Options:
    --dry-run      Preview changes without making them
    --interactive  Prompt for each file without a gist mapping
    --show-diffs   Show diffs between local files and gists
```

## System Administration

### Network & Security

#### `disable-wsdl`
Disables `awdl0` on macOS to troubleshoot network issues. This is useful for resolving specific network conflicts related to Apple Wireless Direct Link (AWDL).

```bash
disable-wsdl
```

#### `uninstall-juniper-connect`
Uninstalls the Juniper Network Connect software, removing related files and configurations from the system.

```bash
uninstall-juniper-connect
```

#### `whitelist_rabbitmq`
Whitelists RabbitMQ in the macOS firewall by adding it to the Application Firewall settings. Essential for configuring firewall rules to allow RabbitMQ traffic.

```bash
whitelist_rabbitmq
```

### Application Management

#### `check-for-electron-apps.sh`
A companion script to `list-electron-apps.sh` that checks for the presence of Electron-based applications in common installation directories.

```bash
check-for-electron-apps.sh
```

#### `dropbox-pause-unpause.sh`
Pauses or resumes Dropbox using signals on macOS. Particularly useful for users looking to control Dropbox activity without closing the application.


```bash
dropbox-pause-unpause.sh # Show current status
dropbox-pause-unpause.sh --pause # Pause Dropbox
dropbox-pause-unpause.sh --resume # Resume Dropbox
```

By Timothy J. Luoma.

#### `list-electron-apps.sh`
Lists applications built on the Electron framework. Looks in common locations for Electron apps.

```bash
list-electron-apps.sh
```

#### `remove-mackups`
Removes symlinks created by the Mackup utility in the Preferences directory. This script aids in clearing out unwanted or outdated backup links.

```bash
remove-mackups
```

#### `uninstall-arq`
Uninstalls Arq backup software, removing all related files and configurations from the system.

```bash
uninstall-arq
```

## Browser & Data Tools

### Browser Management

#### `chrome-tabs-to-md.sh`
Exports currently open Chrome tabs as Markdown links. This script is useful for quickly saving session data in a shareable format.

```bash
chrome-tabs-to-md.sh  # Outputs markdown-formatted links for all open tabs
```

#### `list-browser-urls.sh`
Uses AppleScript to retrieve URLs and titles of open Chrome tabs. Particularly useful for quick snapshots of browsing sessions or documentation of open resources.

```bash
list-browser-urls.sh
```

### Data Analysis & Processing

#### `analyze-apple-healthkit-export.py`
Parses and processes data from an Apple Health XML export file. This script can be customized for specific data analysis tasks related to health metrics.

```bash
analyze-apple-healthkit-export.py
```

#### `google_to_hugo.py`
Converts Google data (potentially Google Docs or Sheets) to a Hugo-compatible format for website generation. Helpful for automating content migration to Hugo sites.

```bash
google_to_hugo.py
```
#### `vote-counter.py`
Interacts with Google Sheets to retrieve and count votes from a spreadsheet. It can be useful for basic polling or tabulation tasks in a Google Sheets-based workflow.

```bash
vote-counter.py
```
