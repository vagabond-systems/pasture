#!/bin/bash

RANDOM_CONFIG_PATH=$(find /etc/openvpn/configs/nord -type f -regex ".*\.ovpn$" | shuf -n 1)
echo "$RANDOM_CONFIG_PATH"

# set up auth
rm -f /etc/openvpn/login.conf
echo "$VPN_USERNAME" >> /etc/openvpn/login.conf
echo "$VPN_PASSWORD" >> /etc/openvpn/login.conf

openvpn --config "$RANDOM_CONFIG_PATH" --auth-user-pass /etc/openvpn/login.conf
