#!/usr/bin/bash

set -x

cd /home/bee/brokebot

logfile="./brokebot.log"

if [ -f "$logfile" ]; then
  mv -f "$logfile" "$logfile".1
fi

echo "starting brokebot at $(date)" >> "$logfile"
espeak "starting behavior module"

python3 src/main.py > $logfile 2>&1 &

echo $! > ./brokebot.pid
