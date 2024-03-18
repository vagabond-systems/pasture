#!/bin/bash
if [ -f /tmp/openvpn_pid.txt ]; then
    kill "$(cat /tmp/openvpn_pid.txt)"
fi
RANDOM_CONFIG_PATH=$(find /etc/openvpn/configs/ -type f | shuf -n 1)
echo "$RANDOM_CONFIG_PATH"
ORIGINAL_IP=$(curl icanhazip.com)
nohup openvpn --config "$RANDOM_CONFIG_PATH" --auth-user-pass /etc/openvpn/login.conf &
echo $! >/tmp/openvpn_pid.txt
sleep 5
NEW_IP=$(curl icanhazip.com)
echo "(*) initial ip:"
echo "$ORIGINAL_IP"
echo "(*) turned into:"
echo "$NEW_IP"
if [ "$NEW_IP" == "$ORIGINAL_IP" ]; then
    shutdown
fi
