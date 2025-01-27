#!/usr/bin/env bash
# shows all url+titles of Chrome along with front window+tab url+title
# Source: https://gist.github.com/osteele/704d40f90e17d7bc059d06731056bbe7
# Forked from: https://gist.github.com/samyk/65c12468686707b388ec43710430a421
# Original author: https://gist.github.com/samyk

(osascript << EOF
set titleString to ""

tell application "Google Chrome"
  set windowList to every window # get the windows

  repeat with theWindow in windowList # for every window
    set tabList to every tab in theWindow # get the tabs

    repeat with theTab in tabList # for every tab
        set tabUrl to the URL of theTab # grab the URL
        set tabTitle to the title of theTab # grab the title
        set titleString to titleString & "- [" & tabTitle & "](" & tabUrl & ")\n"
    end repeat

    set titleString to titleString & "\n---\n\n"
  end repeat
end tell
EOF
) \
  | grep -v '](chrome:' \
  | sed 's/\(.*](\)chrome-extension:\/\/klbibkeccnjlkjkiokjodocebajanakg\/suspended.html#.*uri=\(.*\)/\1\2/'
