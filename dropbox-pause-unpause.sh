#!/bin/zsh
# Dropbox Pause/Unpause Utility
# Version: 1.1.0
#
# Pause or continue the Dropbox.app on Mac OS X using `kill -STOP` and `kill -CONT`
#
# Usage: dropbox-pause-unpause.sh [--pause|--resume|--kill|--start|--toggle]
#
# Examples:
#   dropbox-pause-unpause.sh          # Show status
#   dropbox-pause-unpause.sh --pause  # Pause Dropbox
#   dropbox-pause-unpause.sh --resume # Resume Dropbox
#   dropbox-pause-unpause.sh --toggle # Toggle between pause/resume
#
# Changes from original:
# - Added --toggle command to switch between pause/resume states
# - Improved msg function to try osascript first, fall back to echo
# - Added timeout to prevent infinite loops
# - Added error handling with die function
#
# Original author: Timothy J. Luoma <luomat at gmail dot com>
# Date:	2013-07-08
# Modified: 2024-10-23

# Add safety flags
set -eu

NAME="$0:t:r"
LONG_NAME="$0:t"

die() {
    msg "ERROR: $*"
    exit 1
}

msg() {
		echo "$*"
    if command -v osascript >/dev/null 2>&1; then
        osascript -e "display notification \"$*\" with title \"Dropbox\"" 2>/dev/null || echo "$*"
    fi
}

show_usage () {
    cat <<EOF
'$LONG_NAME' can be used to either stop (pause) or resume (unpause) the Dropbox client on Mac OS X. There are three ways to invoke $0:

1. With no arguments, $0 will show Dropbox's current status
2. '$LONG_NAME --pause' will tell Dropbox to pause
3. '$LONG_NAME --resume' will tell Dropbox to resume (unpause)

If '$LONG_NAME --resume' is called when Dropbox.app is not running, Dropbox.app will be launched.
If '$LONG_NAME --pause' is called when Dropbox.app is not running, Dropbox.app will NOT be launched.

Hopefully someday Dropbox, Inc. will give Mac users the proper tools to pause/unpause Dropbox via automation, but until then, this will work.

Note that when Dropbox.app is paused, the menu bar app will not update, nor will it respond to mouseover or clicks. This can lead to the mistaken belief that Dropbox.app is up-to-date, when in fact it is simply 'frozen in time.'

Unless someone can figure out a reliable way to trigger Dropbox pause/unpause, I don't see any way around it.
EOF
    exit 0
}

PLIST="$HOME/Library/LaunchAgents/com.tjluoma.is-dropbox-paused.plist"

unload_plist () {
    if [ -e "$PLIST" ]; then
        launchctl unload "$PLIST"
    fi
    return 0
}

load_plist () {
    if [ -e "$PLIST" ]; then
        launchctl load "$PLIST"
    fi
    return 0
}

get_db_info () {
    DB_INFO=($(ps cx | awk -F' ' '/ Dropbox$/{print $1"\t"$3}'))
    DB_PID="$DB_INFO[1]"
    DB_STATUS="$DB_INFO[2]"

    # Add timeout to prevent infinite loop
    local timeout=30
    local count=0
    while [ "$DB_STATUS" = "U" ]; do
        if [ $count -ge $timeout ]; then
            die "Timeout waiting for Dropbox status to change from uninterruptible"
        fi
        sleep 1
        ((count++))
        DB_STATUS=$(ps cx | awk -F' ' '/ Dropbox$/{print $3}')
        msg "DB_STATUS = U (please wait)"
    done
}

report_db_status () {
    get_db_info
    if [ "$DB_PID" = "" ]; then
        msg "Dropbox is not running"
    else
        # Dropbox IS running, is it paused ?
        case "$DB_STATUS" in
            S|R)
                msg "Dropbox Status: NORMAL [$DB_PID/$DB_STATUS]"
                ;;
            T)
                msg "Dropbox Status: PAUSED [$DB_PID]"
                ;;
            *)
                msg "Dropbox Status: UNKNOWN ($DB_STATUS) [$DB_PID]"
                ;;
        esac
    fi
}

ACTION="REPORT"

for ARG in "$@"
do
	case "$ARG" in
		-p|--pause|-s|--stop)
				ACTION="PAUSE"
				shift
		;;

		-u|--unpause|-c|--continue|-r|--resume)
				ACTION="CONTINUE"
				shift
		;;

		-t|--toggle)
				ACTION="TOGGLE"
				shift
		;;

		-s|--start|--l|--launch)
				ACTION="START"
				shift
		;;

		-k|--kill)
				ACTION="KILL"
				shift
		;;

		-*)
				show_usage
		;;

	esac
done

case "$ACTION" in
	REPORT)
				report_db_status
	;;

	PAUSE)
				get_db_info

				if [ "$DB_PID" = "" ]
				then
						msg "Dropbox is not running, so cannot be paused"
				else
						# Dropbox IS running, is it paused ?
						if [ "$DB_STATUS" = "T" ]
						then
								msg "Dropbox is already PAUSED [$DB_PID]"
						else
								kill -STOP "$DB_PID" && load_plist || die "Attempt to kill -STOP $DB_PID failed"
								report_db_status
						fi
				fi
	;;

	KILL)
				get_db_info

				if [ "$DB_PID" = "" ]
				then
						msg "Dropbox is not running, so cannot be killed"
				else
						kill "$DB_PID" && load_plist || die "Attempt to kill -STOP $DB_PID failed"
				fi
	;;

	START)
				get_db_info

				if [ "$DB_PID" != "" ]
				then
						msg "Dropbox is already running"
				else
						open -a Dropbox.app || die "Attempt to launch Dropbox.app failed"
				fi
	;;

	CONTINUE)
				get_db_info

				if [ "$DB_PID" = "" ]
				then
						msg "Dropbox is not running, launching"
						open -g -a Dropbox
				else
						if [ "$DB_STATUS" = "S" ]
						then
								msg "Dropbox is not paused (Status: $DB_STATUS)"
						else
								kill -CONT "$DB_PID" && unload_plist || die "Attempt to kill -CONT $DB_PID failed"
								report_db_status
						fi
				fi
	;;

	TOGGLE)
				get_db_info
				if [ "$DB_PID" = "" ]; then
					msg "Dropbox is not running, launching"
					open -g -a Dropbox
				else
					case "$DB_STATUS" in
						T)  # If paused, resume
							kill -CONT "$DB_PID" && unload_plist || die "Attempt to kill -CONT $DB_PID failed"
							;;
						S|R)  # If running, pause
							kill -STOP "$DB_PID" && load_plist || die "Attempt to kill -STOP $DB_PID failed"
							;;
						*)
							msg "Unknown Dropbox status: $DB_STATUS"
							;;
					esac
					report_db_status
				fi
	;;

esac


exit
