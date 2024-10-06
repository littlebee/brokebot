#!/bin/bash


LOG_FILE=/home/bee/brokebot/video_player.log

# /usr/bin/vlc --repeat --fullscreen --no-osd /home/bee/brokebot\ display.mp4

# -loop 0 must be after the file name to avoid screen blanking on each loop
/usr/bin/mplayer -fs -vf scale -zoom /home/bee/brokebot/media/brokebot\ display.mp4 -loop 0


# echo "Starting video player at $(date)" >> $LOG_FILE
# python3 src/video_player.py >> $LOG_FILE

