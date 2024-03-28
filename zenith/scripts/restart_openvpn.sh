#!/bin/bash

RANDOM_CONFIG_PATH=$(find /etc/openvpn/configs/ -type f -regex ".*\.ovpn$" | shuf -n 1)
echo "$RANDOM_CONFIG_PATH"
nohup openvpn --config "$RANDOM_CONFIG_PATH" --auth-user-pass /etc/openvpn/login.conf &
echo $! >/tmp/openvpn_pid.txt
