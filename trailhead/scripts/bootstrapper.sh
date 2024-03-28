#!/bin/bash

echo "http_port $INGRESS_PORT" >> /etc/squid/squid.conf
sudo systemctl restart squid
sleep infinity
