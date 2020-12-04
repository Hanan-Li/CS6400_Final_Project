#!/bin/bash
# script for installing and running haproxy
sudo apt-get install haproxy
sudo haproxy -f servers_2.cfg -p /var/run/haproxy.pid -sf $(cat /var/run/haproxy.pid)

