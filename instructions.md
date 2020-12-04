# Instructions for setup and execution
This document contains information on setting up servers for logical replication or log shipping, as well as execution information. We assume all machines/servers/clients will use a linux based operating system.
In particular, HAproxy load balancing does not support windows.
Logical Replication cannot be setup simultaneously with log shipping, so after finishing execution and tests on one setup, it has to be torn down and reconfigured from scratch.
## Server Acquisition and Installation of Postgresql 13.1
1. Acquire 3 AWS ec2 linux instances with 4GB of RAM
1. If you are able to set up port forwarding on your local router and your computer has ~10gb free disk space, we will use your own computer as another server. If not, set up another AWS ec2 instance with 4GB of RAM
1. Install Postgres 13 on each server/local computer with these commands, detailed instructions available on: https://www.postgresql.org/download/linux/ubuntu/:
    1. sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
    1. wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
    1. sudo apt-get update
    1. sudo apt-get -y install postgresql

## Setting up TPC-B database

## Setting up Logical Replication
### Distributed Read setup (1 primary server)
### Distributed Write setup (>1 primary servers)
## Setting up Log Shipping

## Setting up HAproxy load balancer on the client side
Note that we used HAproxy on the client side instead of putting it in another independent server, since we are cheapskates and this accomplishes our goal. To simulate a more realistic real life scenario, HAproxy would be hosted on a dedicated load balancing server.
1. If you use a DPKG based linux system:
    1. sudo apt update
    1. sudo apt-get install haproxy
1. If you use a RPM based linux system:
    1. yum install haproxy

To start HAproxy service:  
sudo haproxy -f <config name> -p /var/run/haproxy.pid -sf $(cat /var/run/haproxy.pid)  
Configs used for this project can be seen in haproxy_cfg directory. The ending number in the config files refers to number of servers to load balance connections to.



