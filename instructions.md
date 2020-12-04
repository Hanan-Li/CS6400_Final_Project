# Instructions for setup and execution
This document contains information on setting up servers for logical replication or log shipping, as well as execution information. We assume all machines/servers/clients will use a linux based operating system.
In particular, HAproxy load balancing does not support windows.
Logical Replication cannot be setup simultaneously with log shipping, so after finishing execution and tests on one setup, it has to be torn down and reconfigured from scratch.
## Server Acquisition and Installation of Postgresql 13.1
1. Acquire 3 AWS ec2 linux instances with 4GB of RAM
1. If you are able to set up port forwarding on your local router and your computer has ~10gb free disk space, we will use your own computer as another server. If not, set up another AWS ec2 instance with 4GB of RAM
1. Install Postgres 13 on each server/local computer with these commands, detailed instructions available on: https://www.postgresql.org/download/linux/ubuntu/:
    1. `sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'`
    1. `wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -`
    1. `sudo apt-get update`
    1. `sudo apt-get -y install postgresql`

## Setting up TPC-B database

## Setting up Logical Replication
### Distributed Read setup (1 primary server)
### Distributed Write setup (>1 primary servers)
## Setting up Log Shipping

## Setting up HAproxy load balancer on the client side
Note that we used HAproxy on the client side instead of putting it in another independent server, since we are cheapskates and this accomplishes our goal. To simulate a more realistic real life scenario, HAproxy would be hosted on a dedicated load balancing server.
1. If you use a DPKG based linux system:
    1. `sudo apt update`
    1. `sudo apt-get install haproxy`
1. If you use a RPM based linux system:
    1. `yum install haproxy`

To start HAproxy service:  
`sudo haproxy -f <config name> -p /var/run/haproxy.pid -sf $(cat /var/run/haproxy.pid)`  
Configs used for this project can be seen in haproxy_cfg directory. The ending number in the config files refers to number of servers to load balance connections to. However, depending on your IP addresses, every single config file's 'listen' section has to change to reflect that.

## Setting up Python and required libraries
1. Install Python>=3.6, https://www.python.org/downloads/
1. Install psycopg2 library with pip:
    * `pip install psycopg2`

## Executing tests
Once everything is setup, tests can be executed on the clientside. One big note is to make sure to set up the configuration of the servers and load balancer correctly before each test run. To test different number of servers and how that affects latency, we turned off the subscription for some AWS instances. Details on usage of each script can be done by executing `python <script_name> -u`
* To run distributed read test on your configuration, use read_test.py. Make sure to change your haproxy to run with the correct config and have the postgresql servers set up in the proper configuration. For example. If we only want to test distributed reads on 3 servers, make sure to run haproxy with servers_3.cfg config.
* To run read after write test, use raf_test.py. However, the IP addresses are hardcoded into the file, so please change the `ip_list` variable to reflect your IP addresses for the servers. Make sure the first element in the list is the primary server used for writes. Read-after-write tests do not need a loadbalancer, but before running each test, make sure the servers are set up properly. For example, if you want to test read after write with a 3 server logical replication setup, make sure to turn off the subscription for one of the postgresql servers, and set up logical replication with 1 primary server and 2 secondary servers.
* If your setup is for logical replication distributed writes, use write_test.py. Distributed write setup must be setup in a specific way. That is, make sure to change the `connection_list` variable to reflect the IP addresses of your writing primary servers, and `ip_list` variable to only have the Ip address of your single read-only secondary server. Also make sure to change your haproxy to run with the correct config, load balancing to your primary writing servers before each test. Again, also make sure that the server configuration is correct.




