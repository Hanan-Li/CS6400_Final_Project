#!/bin/bash

sudo haproxy -f servers_1.cfg -p /var/run/haproxy.pid -sf $(cat /var/run/haproxy.pid)

