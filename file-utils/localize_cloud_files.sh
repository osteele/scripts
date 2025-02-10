#!/bin/bash

set -euo pipefail

show_help() {
    cat << EOF
Usage: $(basename "$0") [OPTIONS] [DIRECTORY]

Forces download of cloud-synced files by reading all bytes from files in the specified directory.
Useful for ensuring files are fully downloaded from cloud storage services like Dropbox, OneDrive, etc.

Options:
    -h, --help                      Show this help message and exit
    --include-hidden true|false     Include hidden files and directories (default: true)

Arguments:
    DIRECTORY       Target directory to process (default: current directory)

Examples:
    $(basename "$0")                         # Process current directory, including hidden files
    $(basename "$0") --include-hidden false  # Skip hidden files and directories
    $(basename "$0") ~/Documents             # Process Documents directory
EOF
    exit 0
}

INCLUDE_HIDDEN=true
DEBUG=false

# Parse command line arguments
while [ $# -gt 0 ]; do
    case "$1" in
        -h|--help)
            show_help
            ;;
        --debug)
            DEBUG=true
            shift
            ;;
        --include-hidden)
            shift
            if [ "$1" != "true" ] && [ "$1" != "false" ]; then
                echo "Error: --include-hidden requires 'true' or 'false'" >&2
                exit 1
            fi
            INCLUDE_HIDDEN="$1"
            shift
            ;;
        *)
            TARGET_DIR="$1"
            break
            ;;
    esac
    shift
done

start_time=$(date +%s)

# Default to current directory if no argument provided
TARGET_DIR="${1:-.}"

# Normalize path to absolute path and resolve symlinks
TARGET_DIR=$(cd -P "$TARGET_DIR" 2>/dev/null && pwd) || {
    echo "Error: Cannot access directory '$1'" >&2
    exit 1
}

# Add informative message if it was a symlink
if [ -L "${1:-.}" ]; then
    echo "Note: Following symlink to target: $TARGET_DIR"
fi

echo "Starting to process directory: $TARGET_DIR"
echo "This will force download of all files from cloud storage..."
echo "Counting files and calculating total size..."

# Counter variables
total_files=0
total_bytes=0
processed_files=0

FIND_OPTS=()
if [ "$INCLUDE_HIDDEN" = "false" ]; then
    FIND_OPTS+=(-not -path '*/\.*')
fi

if [ "$DEBUG" = "true" ]; then
    echo "CMD: find \"$TARGET_DIR\" -type f ! -type l ${FIND_OPTS[*]:-}"
fi

# First, count total files and bytes with progress
while IFS= read -r -d '' file; do
    if [ -f "$file" ] && [ ! -L "$file" ]; then
        ((total_files++))
        file_size=$(stat -f %z "$file" 2>/dev/null || stat -c %s "$file")
        total_bytes=$((total_bytes + file_size))
        echo -ne "\rCounted $total_files files ($(numfmt --to=iec-i --suffix=B $total_bytes))...\033[K"
    fi
done < <(find "$TARGET_DIR" -type f ! -type l ${FIND_OPTS[*]:-} -print0 2>/dev/null)

echo -e "\nFound $total_files files totaling $(numfmt --to=iec-i --suffix=B $total_bytes)"

# Process files
while IFS= read -r -d '' file; do
    if [ -f "$file" ] && [ ! -L "$file" ]; then
        ((processed_files++))
        file_size=$(stat -f %z "$file" 2>/dev/null || stat -c %s "$file")

        # Show progress
        echo -ne "\rProcessing file $processed_files/$total_files: $(basename "$file")...\033[K"

        # Read entire file using dd and discard output
        dd if="$file" of=/dev/null bs=1M status=none 2>/dev/null || {
            echo -e "\nWarning: Could not read '$file'" >&2
            continue
        }
    fi
done < <(find "$TARGET_DIR" -type f ! -type l ${FIND_OPTS[*]:-} -print0 2>/dev/null)

end_time=$(date +%s)
elapsed=$((end_time - start_time))
# Convert seconds to hours, minutes, seconds
hours=$((elapsed / 3600))
minutes=$(((elapsed % 3600) / 60))
seconds=$((elapsed % 60))

echo -e "\nCompleted processing $processed_files files"
echo "All files should now be downloaded locally"
echo "Total time: ${hours}h ${minutes}m ${seconds}s"
