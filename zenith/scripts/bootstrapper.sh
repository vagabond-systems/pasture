#!/bin/bash

cp /etc/openvpn/resolv.conf /etc/resolv.conf
. /app/scripts/restart_openvpn.sh
sleep infinity
