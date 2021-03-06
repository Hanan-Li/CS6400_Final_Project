# CS6400_Final_Project

Final Project for Gatech CS6400 Database system course. Detailed instructions on how to setup the project can be seen in instructions.md

## Directory Structure
* haproxy_cfg/
  * Contains all the haproxy configs used for the project, and a bash script with the command used to start different haproxy setups
* stats_graph/
  * Contains all the graphs generated for the project
* instructions.md
  * Contains instructions on our experiment setup
* raf_test.py
  * Custom python script used to test read-after-write latency.
* read_test.py
  * Custom python script used to test distributed reads. This files calls the pgbench command to do testing
* write_test.py
  * Custom python script used to test distributed writes. Threadified to send work synchronously to load balancer.
