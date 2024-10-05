#!/bin/bash

set -x

# audio
sudo apt install -y espeak
sudo apt install -y mpg123

# for display
sudo apt install -y mplayer

# head tilt and pan
sudo pip3 install adafruit-circuitpython-servokit

if [ ! -f /etc/xdg/lxsession/LXDE-pi/autostart.orig ]; then
  sudo mv /etc/xdg/lxsession/LXDE-pi/autostart /etc/xdg/lxsession/LXDE-pi/autostart.orig
fi

sudo ln -sf /home/bee/brokebot/setup/files/etc/xdg/lxsession/LXDE-pi/autostart /etc/xdg/lxsession/LXDE-pi/autostart

sudo cp setup/files/etc/rc.local /etc/
sudo chmod +x setup/files/etc/rc.local

# for audio espeak needs pulse audio global to run as background
sudo adduser root pulse-access
sudo cp setup/files/etc/systemd/system/pulseaudio.service /etc/systemd/system/
sudo cp setup/files/etc/pulse/client.conf /etc/pulse/

sudo systemctl --system enable pulseaudio.service
sudo systemctl --system start pulseaudio.service
sudo systemctl --system status pulseaudio.service

