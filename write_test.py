import os
import sys
import psycopg2
import time
import random
import getopt
import threading
import math
from statistics import mean



ip_list = ['24.98.255.22'] #,  '24.98.255.22', '52.201.253.38' , '54.209.168.101', '54.221.17.161'
connections_list = ["ec2-54-226-57-144.compute-1.amazonaws.com", "ec2-50-17-30-28.compute-1.amazonaws.com", "ec2-54-91-97-231.compute-1.amazonaws.com"]
proxy_connection = psycopg2.connect(user = "postgres",
                                    password = "realSmooth",
                                    host = '127.0.0.1',
                                    port = "6432",
                                    database = "ChaCha")

def init_conn(ip_list) :
    conn = []

    for i in range(len(ip_list)) :
        connection = psycopg2.connect(user = "postgres",
                                      password = "realSmooth",
                                      host = ip_list[i],
                                      port = "5432",
                                      database = "ChaCha")
        conn.append(connection)
    return conn


def bulk_insert(queries, idx):
    time.sleep(1)
    query = "".join(queries)
    start_time = time.time()
    connection = psycopg2.connect(user = "postgres",
                                    password = "realSmooth",
                                    host = '127.0.0.1',
                                    port = "6432",
                                    database = "ChaCha")
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    connection.close()
    commit_time = time.time() - start_time
    print("Thread ", idx, " insert time: ", commit_time)
    return commit_time


def insert_query(conn, bulk, num_queries, num_writers):
    global proxy_connection
    query = []
    for i in range(num_queries) :
        query.append(f"INSERT INTO pgbench_history (tid, bid, aid, delta, mtime, filler) VALUES ({random.randrange(1, 10000, 1)}, {random.randrange(1, 1000, 1)}, {i + 1}, {random.randrange(-1000, 1000, 1)}, now(), '');")

    start_time = time.time()
    commit_time = 0.0
    for i in range(num_writers):
        proxy_connection = psycopg2.connect(user = "postgres",
                                        password = "realSmooth",
                                        host = connections_list[i],
                                        port = "5432",
                                        database = "ChaCha")
        cursor = proxy_connection.cursor()
        truncate = "TRUNCATE pgbench_history;"
        cursor.execute(truncate)
        proxy_connection.commit()
        proxy_connection.close()

    if bulk == 0 :
        for i in range(num_queries) :
            start_time = time.time()
            connection = psycopg2.connect(user = "postgres",
                                    password = "realSmooth",
                                    host = '127.0.0.1',
                                    port = "6432",
                                    database = "ChaCha")
            cursor = connection.cursor()
            cursor.execute(query[i])
            connection.commit()            
            connection.close()
            commit_time += time.time() - start_time
        print("IP: proxy ", " insert ", num_queries, " queries time: ", commit_time)
        cursor.close ()
    else :
        threads = []
        for i in range(num_writers):
            start_idx = i * math.floor(len(query)/num_writers)
            end_idx = (i+1) * math.floor(len(query)/num_writers)

            sub_queries = query[start_idx: end_idx]
            t = threading.Thread(target=bulk_insert, args=(sub_queries, i))
            threads.append(t)
            t.start()
        tot_commit_time = 0.0
        for t in threads:
            t.join()
        print("All Threads Done")
        print("Average insert time = ", tot_commit_time/num_writers)
    commit_time = time.time() - start_time
    


def check_sub(conn, num_queries) :

    done_flag = [False for i in range(len(conn))]
    start_time = time.time()
    total_time = [0.0 for i in range(len(conn))]
    while True :
        for i in range(len(conn)) :

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
                    print("IP: ", ip_list[i], " time: ", total_time[i])
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
        opts, args = getopt.getopt(argv, "ub:n:w:")
    except getopt.GetoptError: 
        print ("For Usage: run_test.py -u")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-u' :
            print ("Usage: run_test.py -b <bulk 1/0> -n <number of queries>")
            print("-b 1 -> For bulk testing")
            print("-b 0 -> For single testing")
            print("-n <int> -> Number of Inserts to be done")
            print("-w <int> -> Number of Writers")
            sys.exit(2)

        elif opt == '-b' :
            bulk = int(arg)
            if bulk != 0 and bulk != 1:
                print ("For Usage: run_test.py -u")
                sys.exit(2)

        elif opt == '-n' :
            num_queries = int(arg)
        elif opt == '-w' :
            num_writers = int(arg)

    if '-b' not in argv or '-n' not in argv :
        print ("For Usage: run_test.py -u")
        sys.exit(2)

    print(num_queries)
    print(num_writers)

    conn = init_conn(ip_list)
    insert_query(conn, bulk, num_queries, num_writers)
    
    if check_sub(conn, num_queries) == True :
        for i in range (len(conn)) : conn[i].close()
        print("gg wp")



if __name__ == '__main__':
    main(sys.argv[1:])