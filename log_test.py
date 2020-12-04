import os
import sys
import psycopg2
import time
import random
import getopt
from statistics import mean



ip_list = ['24.98.255.22']#, 'ec2-50-17-30-28.compute-1.amazonaws.com']#, '54.209.168.101', '54.221.17.161']
conn_list = ["ec2-50-17-30-28.compute-1.amazonaws.com",
        "ec2-54-226-57-144.compute-1.amazonaws.com",
        "ec2-54-91-97-231.compute-1.amazonaws.com"]

def init_conn(ip_list) :
    conn = []
    for i in range(len(ip_list)) :
    
        connection = psycopg2.connect(user = "postgres",
                                      password = "realSmooth",
                                      host = ip_list[i],
                                      port = "5432",
                                      database = "ChaCha")
        conn.append(connection)
    for i in range(len(conn_list)) :
    
        connection = psycopg2.connect(user = "postgres",
                                      password = "realSmooth",
                                      host = conn_list[i],
                                      port = "5432",
                                      database = "ChaCha")
        conn.append(connection)
    return conn
    

def insert_query(conn, bulk, num_queries) :
    
    query = []
    for i in range(num_queries) :
        query.append(f"INSERT INTO pgbench_history (tid, bid, aid, delta, mtime, filler) VALUES ({random.randrange(1, 10000, 1)}, {random.randrange(1, 1000, 1)}, {i + 1}, {random.randrange(-1000, 1000, 1)}, now(), '');")

    start_time = time.time()
    cursor = conn[0].cursor()

    truncate = "TRUNCATE pgbench_history;"
    cursor.execute(truncate)
    conn[0].commit ()

    if bulk == 0 :

        for i in range(num_queries) :
            cursor.execute(query[i])
            conn[0].commit ()

    else :

        query = "".join(query)
        cursor.execute(query)
        conn[0].commit ()

    commit_time = time.time() - start_time
    print("IP: ", ip_list[0], " insert ", num_queries, " queries time: ", commit_time)
    cursor.close ()


def check_sub(conn, num_queries) :

    done_flag = [False for i in range(len(conn))]
    done_flag[0] = True
    start_time = time.time()
    total_time = [0.0 for i in range(len(conn))]

    while True :
        for i in range(1, len(conn)) :

            if done_flag[i] == False :
            
                cursor = conn[i].cursor()
                #cursor.execute("SELECT * FROM pg_subscription_rel;")
                #record = cursor.fetchall()
                cursor.execute("SELECT COUNT(*) FROM pgbench_history LIMIT 1;")
                record = cursor.fetchone()
                cursor.close ()


                
                #state = [record[j][2] for j in range(len(record))]
                if record[0] != num_queries:
                    continue
                else :
                    #print (temp[0])
                    total_time[i] = time.time() - start_time
                    print("IP: ", conn_list[i-1], " time: ", total_time[i])
                    done_flag[i] = True

        if False in done_flag :
            continue
        else :
            print("Avg raw latency :", mean(total_time))
            return True
            

def main(argv):

    if len(argv) == 0 :
        print ("For Usage: run_test.py -u")
        sys.exit(2)
    
    try :
        opts, args = getopt.getopt(argv, "ub:n:")
    except getopt.GetoptError: 
        print ("For Usage: run_test.py -u")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-u' :
            print ("Usage: run_test.py -b <bulk 1/0> -n <number of queries>")
            print("-b 1 -> For bulk testing")
            print("-b 0 -> For single testing")
            print("-n <int> -> Number of Inserts to be done")
            sys.exit(2)

        elif opt == '-b' :
            bulk = int(arg)
            if bulk != 0 and bulk != 1:
                print ("For Usage: run_test.py -u")
                sys.exit(2)

        elif opt == '-n' :
            num_queries = int(arg)

    if '-b' not in argv or '-n' not in argv :
        print ("For Usage: run_test.py -u")
        sys.exit(2)


    conn = init_conn(ip_list)

    insert_query(conn, bulk, num_queries)
    
    if check_sub(conn, num_queries) == True :
        for i in range (len(conn)) : conn[i].close()
        print("gg wp")



if __name__ == '__main__':
    main(sys.argv[1:])
