#!/bin/bash

# builds on top of

# echo on
set -x

# audio
sudo apt install -y espeak
sudo apt install -y mpg123

# for display, mplayer is run in a loop playing `/media/brokebot display.mp4`
# see also start_display.sh
sudo apt install -y mplayer

# head tilt and pan
sudo pip3 install adafruit-circuitpython-servokit

if [ ! -f /etc/xdg/lxsession/LXDE-pi/autostart.orig ]; then
  sudo mv /etc/xdg/lxsession/LXDE-pi/autostart /etc/xdg/lxsession/LXDE-pi/autostart.orig
fi
# lxsession autostart is used to start_display.sh after the X windows desktop is loaded
# I also tweeked it for running as a kiosk similar to love-frame.
sudo ln -sf /home/bee/brokebot/setup/files/etc/xdg/lxsession/LXDE-pi/autostart /etc/xdg/lxsession/LXDE-pi/autostart

# rc.local calls start_main.sh
sudo cp setup/files/etc/rc.local /etc/
sudo chmod +x setup/files/etc/rc.local

# install network manager to create wifi hotspot
sudo apt purge -y openresolv dhcpcd5 ifupdown
sudo apt install -y network-manager
sudo nmcli con add con-name hotspot ifname wlan0 type wifi ssid "sb101a"
sudo nmcli con modify hotspot wifi-sec.key-mgmt wpa-psk
sudo nmcli con modify hotspot wifi-sec.psk '2broken4u'
sudo nmcli con up hotspot


# change to /boot/config to rotate hdmi screen 90°
sudo cp setup/files/boot/config.txt /boot/

# for audio espeak needs pulse audio global to run as root background because
# src/main is started from /etc/rc.local and `sudo -u bee` did not fix
# the "pulse server not found" issue. `aplay` and `espeak` both didn't
# work unless src/main.py was started from a bash terminal.  I also
# unsuccessfully tried starting src/main.py from rclocal using
# `sudo -u bee bash -c /home/bee/start_main.sh`
sudo adduser root pulse-access
sudo cp setup/files/etc/systemd/system/pulseaudio.service /etc/systemd/system/
sudo cp setup/files/etc/pulse/client.conf /etc/pulse/

# run pulse audio as root
sudo systemctl --system enable pulseaudio.service
sudo systemctl --system start pulseaudio.service
sudo systemctl --system status pulseaudio.service

