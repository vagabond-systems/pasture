#!/bin/bash

cp /etc/openvpn/resolv.conf /etc/resolv.conf
sudo systemctl restart squid
. /app/scripts/restart_openvpn.sh
sleep infinity
