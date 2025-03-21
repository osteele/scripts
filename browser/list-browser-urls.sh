#!/bin/bash

osascript << EOF
# shows all url+titles of Chrome along with front window+tab url+title
 set titleString to ""
 tell application "Google Chrome"
         set window_list to every window # get the windows
         repeat with the_window in window_list # for every window
                 set tab_list to every tab in the_window # get the tabs
                 repeat with the_tab in tab_list # for every tab
                         set the_url to the URL of the_tab # grab the URL
                         set the_title to the title of the_tab # grab the title
                         set titleString to titleString & the_url & " - " & the_title & "\n" # concatenate
                 end repeat
         end repeat
         set the_url to the URL of active tab of front window # grab the URL
   set the_title to the URL of active tab of front window # grab the title
         set titleString to titleString & "Active: " & the_url & " - " & the_title & "\n" # concatenate
 end tell
EOF
