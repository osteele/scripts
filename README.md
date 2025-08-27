# README

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
    - [`sync-gists`](#sync-gists)
- [Application Support](#application-support)
  - [Anki](#anki)
    - [`anki-simplify-hanzi`](#anki-simplify-hanzi)
  - [Chrome](#chrome)
    - [`chrome-tabs-to-md.sh`](#chrome-tabs-to-mdsh)
  - [Obsidian](#obsidian)
    - [`find-obsidian-duplicates`](#find-obsidian-duplicates)
    - [`move-tags-to-frontmatter`](#move-tags-to-frontmatter)
- [Media \& File Processing](#media--file-processing)
  - [Audio/Video Processing](#audiovideo-processing)
    - [`audiocat`](#audiocat)
    - [`describe-image`](#describe-image)
    - [`frames-to-video`](#frames-to-video)
    - [`imgcat`](#imgcat)
    - [`srt-dedup-lines`](#srt-dedup-lines)
    - [`audiotrim`](#audiotrim)
    - [`srt2paragraphs`](#srt2paragraphs)
  - [File Management](#file-management)
    - [`fix-file-dates`](#fix-file-dates)
    - [`localize-cloud-files`](#localize-cloud-files)
- [System Administration](#system-administration)
  - [Network \& Security](#network--security)
    - [`disable-wsdl`](#disable-wsdl)
    - [`uninstall-juniper-connect`](#uninstall-juniper-connect)
    - [`whitelist_rabbitmq`](#whitelist_rabbitmq)
  - [Application Management](#application-management)
    - [`dropbox-pause-unpause.sh`](#dropbox-pause-unpausesh)
    - [`remove-mackups`](#remove-mackups)
    - [`uninstall-arq`](#uninstall-arq)
    - [`check-for-electron-apps`](#check-for-electron-apps)
    - [`list-electron-apps`](#list-electron-apps)
- [Browser \& Data Tools](#browser--data-tools)
  - [Browser Management](#browser-management)
    - [`list-browser-urls`](#list-browser-urls)
  - [Data Analysis \& Processing](#data-analysis--processing)
    - [`analyze-healthkit-export`](#analyze-healthkit-export)
    - [`google-sites-to-hugo`](#google-sites-to-hugo)
    - [`vote-counter`](#vote-counter)

This repository contains various utility scripts, primarily in Bash and Python, to assist with system management, development, and miscellaneous automation tasks.

For more development tools and documentation, see: https://osteele.com/software/development-tools

## Development Tools

### Version Control Scripts

For Git and Jujutsu version control scripts, see:
- **Git Scripts**: https://github.com/osteele/git-scripts - AI-powered commit messages, repository management tools
- **Jujutsu Scripts**: https://github.com/osteele/jj-scripts - AI-powered Jujutsu tools and workflow enhancements

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

#### `sync-gists`
Synchronizes local script files with GitHub Gists. Supports interactive mode, dry-run, and diff viewing. Uses `.gists.toml` for mapping local files to gist IDs.

```bash
sync-gists [OPTIONS] [FILES...]

Options:
    --dry-run      Preview changes without making them
    --interactive  Prompt for each file without a gist mapping
    --show-diffs   Show diffs between local files and gists
```

## Application Support

### Anki

Also see [standalone Github repositories](https://github.com/osteele?tab=repositories&q=anki).

#### `anki-simplify-hanzi`

A script that uses the AnkiConnect add-on to convert traditional Chinese characters to simplified Chinese in Anki cards.

**Features:**
- Searches through specified fields (default: "Hanzi" and "Chinese") for traditional characters
- Converts them to simplified using hanziconv
- Provides a dry-run mode to preview changes
- Shows detailed statistics about changes

**Requirements:**
- Anki with AnkiConnect add-on installed
- uv for dependency management

**Usage:**
```bash
./anki/anki-simplify-hanzi "Your Deck Name"
./anki/anki-simplify-hanzi "Your Deck Name" --dry-run
./anki/anki-simplify-hanzi "Your Deck Name" --fields "Characters,Expression"
```

### Chrome

#### `chrome-tabs-to-md.sh`
Exports currently open Chrome tabs as Markdown links. This script is useful for quickly saving session data in a shareable format.

```bash
chrome-tabs-to-md.sh  # Outputs markdown-formatted links for all open tabs
```

### Obsidian

#### `find-obsidian-duplicates`
Finds duplicate markdown files in an Obsidian vault based on three possible criteria: (1) same filename and same content, (2) same filename only, or (3) same filename and similar content. Respects Obsidian's ignore patterns.

```bash
# Find files with same name and content
find-obsidian-duplicates /path/to/obsidian/vault

# Find files with same name only
find-obsidian-duplicates /path/to/obsidian/vault --mode name-only

# Find files with same name and similar content (fuzzy matching)
find-obsidian-duplicates /path/to/obsidian/vault --mode similar-content --similarity-threshold 0.8
```

#### `move-tags-to-frontmatter`

Processes Obsidian markdown files and moves file-level tags into the YAML frontmatter. Useful for standardizing tag locations in Obsidian vaults or migrating between different note-taking systems.

```bash
# Process all markdown files in an Obsidian vault
move-tags-to-frontmatter /path/to/obsidian/vault

# Preview changes without making them (dry run)
move-tags-to-frontmatter --dry-run /path/to/obsidian/vault

# Only process the first 10 files that would be modified
move-tags-to-frontmatter --limit 10 /path/to/obsidian/vault

# Combine options
move-tags-to-frontmatter --dry-run --limit 5 /path/to/obsidian/vault
```

The script:
- Recursively searches through all subdirectories of the vault
- Respects Obsidian's ignore patterns (hidden files and userIgnoreFilters)
- Identifies tag-only lines at the beginning of files or after existing frontmatter
- Moves tags to the frontmatter, creating it if needed
- De-duplicates tags and formats them as a YAML array
- Shows progress with a progress bar and summary of changes
- Can limit processing to a specific number of files (--limit option)

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

#### `audiotrim`
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
```

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

#### `localize-cloud-files`
Forces a local cache of all files in a directory by reading all bytes from the cloud storage. This can be useful for ensuring all files are downloaded locally, potentially improving performance for subsequent accesses.

```bash
localize-cloud-files [DIR]  # Defaults to current directory if not specified
```

||||||| e283f25
=======
#### `sync_gists.py`
Synchronizes local script files with GitHub Gists. Supports interactive mode, dry-run, and diff viewing. Uses `.gists.toml` for mapping local files to gist IDs.

```bash
sync_gists.py [OPTIONS] [FILES...]

Options:
    --dry-run      Preview changes without making them
    --interactive  Prompt for each file without a gist mapping
    --show-diffs   Show diffs between local files and gists
```

>>>>>>> origin/main
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

#### `dropbox-pause-unpause.sh`
Pauses or resumes Dropbox using signals on macOS. Particularly useful for users looking to control Dropbox activity without closing the application. origin/main

```bash
dropbox-pause-unpause.sh # Show current status
dropbox-pause-unpause.sh --pause # Pause Dropbox
dropbox-pause-unpause.sh --resume # Resume Dropbox
```

[Originally by Timothy J. Luoma.](https://github.com/tjluoma/dropbox-pause-unpause)
Minor modifications by O. Steele.

#### `remove-mackups`
Removes symlinks created by the Mackup utility in the Preferences directory. This script aids in clearing out unwanted or outdated backup links.

```bash
remove-mackups
```

#### `check-for-electron-apps`
A companion script to `list-electron-apps` that checks for the presence of Electron-based applications in common installation directories.

```bash
check-for-electron-apps
```

#### `list-electron-apps`
Lists applications built on the Electron framework. Looks in common locations for Electron apps.

```bash
list-electron-apps
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

#### `list-browser-urls`
Uses AppleScript to retrieve URLs and titles of open Chrome tabs. Particularly useful for quick snapshots of browsing sessions or documentation of open resources.

```bash
list-browser-urls
```

### Data Analysis & Processing

#### `analyze-healthkit-export`
Parses and processes data from an Apple Health XML export file. This script can be customized for specific data analysis tasks related to health metrics.

```bash
analyze-healthkit-export
```

#### `google-sites-to-hugo`
Converts Google Sites pages to a Hugo-compatible format for website generation. Helpful for automating content migration to Hugo sites.

```bash
google-sites-to-hugo
```

#### `vote-counter`
Interacts with Google Sheets to retrieve and count votes from a spreadsheet. It can be useful for basic polling or tabulation tasks in a Google Sheets-based workflow.

```bash
vote-counter
```
