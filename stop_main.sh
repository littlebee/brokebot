#!/bin/bash

# don't stop on error - let other subs exit if any sub fails to exit
# set -e

# user=`echo $USER`
# if [ "$user" != "root" ]; then
#   echo "Script must be run as root.  Try 'sudo ./stop.sh'"
#   exit 1
# fi

echo "stopping brokebot via stop_main" >> brokebot.log

pid_file="./brokebot.pid"

set -x

if [ -f "$pid_file" ]; then
  sudo kill -1 `cat $pid_file`
  rm -f $pid_file
else
  echo "$pid_file does not exist. skipping"
fi
