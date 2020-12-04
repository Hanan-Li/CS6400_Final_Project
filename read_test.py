import os
import sys
import getopt

def setupHaproxy(num_servers):
    server_cfg = "server_" + str(num_servers) + ".cfg"
    command = 'sudo haproxy -f {0} -p /var/run/haproxy.pid -sf $(cat /var/run/haproxy.pid)'.format(server_cfg)
    stream = os.popen(command)
    output = stream.read()
    print(output)


def run_pgbench(num_clients, num_transactions, num_threads, read_only):
    command = ""
    if read_only:
        command = 'pgbench -n -S -c {0} -t {1} -j {2} -C -h 127.0.0.1 -p 6432 -U postgres ChaCha'.format(num_clients, num_transactions, num_threads)
    else:
        command = 'pgbench -n -c {0} -t {1} -j {2} -C -h 127.0.0.1 -p 6432 -U postgres ChaCha'.format(num_clients, num_transactions, num_threads)
    print(command)
    stream = os.popen(command)
    output = stream.read()
    print(output)


def main(argv):
    num_servers = 2
    num_clients = 80
    num_transactions = 1000
    num_threads = 1
    read_only = False
    try:
        opts, args = getopt.getopt(argv,"hs:c:t:j:r",["servers=","clients=","transactions=", "jobs="])
    except getopt.GetoptError:
        print("Shit")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("Shit")
            sys.exit()
        elif opt in ("-s", "--servers"):
            num_servers = int(arg)
        elif opt in ("-c", "--clients"):
            num_clients = int(arg)
        elif opt in ("-t", "--transactions"):
            num_transactions = int(arg)
        elif opt in ("-j", "--jobs"):
            num_threads = int(arg)
        elif opt == '-r':
            read_only = True
    print(num_servers)
    # setupHaproxy(num_servers)
    run_pgbench(num_clients, num_transactions, num_threads, read_only)

if __name__ == '__main__':
    main(sys.argv[1:]) 