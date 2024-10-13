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

# install network manager to create wifi hotspot
sudo apt purge -y openresolv dhcpcd5 ifupdown
sudo apt install -y network-manager
sudo nmcli con add con-name hotspot ifname wlan0 type wifi ssid "sb101a"
sudo nmcli con modify hotspot wifi-sec.key-mgmt wpa-psk
sudo nmcli con modify hotspot wifi-sec.psk '321gameon'
sudo nmcli con up hotspot

# run pulse audio as root
sudo systemctl --system enable pulseaudio.service
sudo systemctl --system start pulseaudio.service
sudo systemctl --system status pulseaudio.service

