#!/bin/bash
# Adapted from https://cameronnokes.com/blog/how-to-know-if-a-desktop-app-uses-electron/

check() {
  stat "$1/Contents/Frameworks/Electron Framework.framework" &> /dev/null
  if [[ $? = 0 ]]; then
    basename "$1"
  fi
}

export -f check

check_directory() {
  local dir="${1/#\~/$HOME}"  # Expand ~ to $HOME
  if [ -d "$dir" ]; then
    local apps=$(find "$dir" -maxdepth 2 -type d -name "*.app" -exec bash -c 'check "{}"' \; | sort -f)
    if [ ! -z "$apps" ]; then
      local count=$(echo "$apps" | wc -l | tr -d ' ')
      echo "📂 $dir ($count applications)"
      echo "$apps" | sed 's/^/    /'
      echo
      echo "$count" >> "$TEMP_COUNT"
    fi
  fi
}

# Set up temp file and cleanup
TEMP_COUNT=$(mktemp -t electron_app_count.XXXXXX)
export TEMP_COUNT

cleanup() {
    rm -f "$TEMP_COUNT"
}
trap cleanup EXIT

# Check each directory
check_directory "/Applications"
check_directory "/Applications/Setapp"
check_directory "/Applications/Utilities"
check_directory "~/Applications"
check_directory "~/Applications/Chrome Apps"
check_directory "~/Applications/Edge Apps"
check_directory "/System/Applications"
check_directory "/Network/Applications"

# Show total if we found apps in more than one directory
dir_count=$(grep -c . "$TEMP_COUNT")
if [ $dir_count -gt 1 ]; then
  total=$(awk '{sum += $1} END {print sum}' "$TEMP_COUNT")
  echo "Total: $total Electron applications"
fi
