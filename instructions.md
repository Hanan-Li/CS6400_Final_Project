# Setup Instructions

## Setting up Postgresql 13.1 Logical Replication Servers
1. Acquire 3 AWS ec2 linux instances with 4GB of RAM
1. If you are able to set up port forwarding on your local router and your computer has ~10gb free disk space, we will use your own computer as another server. If not, set up another AWS ec2 instance with 4GB of RAM
1. Install Postgres 13 on each server/local computer with these commands, detailed instructions available on: https://www.postgresql.org/download/linux/ubuntu/:
    1. sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
    1. wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
    1. sudo apt-get update
    1. sudo apt-get -y install postgresql