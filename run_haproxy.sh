#!/bin/bash

sudo haproxy -f two_servers.cfg -p /var/run/haproxy.pid -sf $(cat /var/run/haproxy.pid)

