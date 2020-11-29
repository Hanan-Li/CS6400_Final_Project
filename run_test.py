import os
import sys
import psycopg2
import time
import random


ip_list = ['24.98.255.22', '52.201.253.38', '54.209.168.101', '54.221.17.161']

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
    

def insert_query(conn) :
    
    num_queries = 100
    query = []
    for i in range(num_queries) :
        query.append(f"INSERT INTO pgbench_history (tid, bid, aid, delta, mtime, filler) VALUES ({random.randrange(1, 10000, 1)}, {random.randrange(1, 1000, 1)}, {i + 1}, {random.randrange(-1000, 1000, 1)}, now(), '');")

    
    #query = "INSERT INTO pgbench_history (tid, bid, aid, delta, mtime, filler) VALUES (999, 999, 999, 999, now(), '');"
    #print(query)

    start_time = time.time()
    #commit_time = 0.0
    cursor = conn[0].cursor()
    for i in range(num_queries) :

        cursor.execute(query[i])
        conn[0].commit ()

    commit_time = time.time() - start_time
    print("IP: ", ip_list[0], " insert ", num_queries, " queries time: ", commit_time)
    cursor.close ()


def check_sub(conn) :

    done_flag = [False for i in range(len(conn))]
    start_time = time.time()
    total_time = [0.0 for i in range(len(conn))]

    while True :
        for i in range(len(conn)) :

            if done_flag[i] == False :
            
                cursor = conn[i].cursor()
                cursor.execute("SELECT * FROM pg_subscription_rel;")
                record = cursor.fetchall()
                cursor.close ()
                
                state = [record[j][2] for j in range(len(record))]
                if 'd' in state:
                    continue
                else :
                    total_time[i] = time.time() - start_time
                    print("IP: ", ip_list[i], " time: ", total_time[i])
                    done_flag[i] = True

        if False in done_flag :
            continue
        else :
            return True
            

def main(argv):

    
    conn = init_conn(ip_list)

    insert_query(conn)
    
    if check_sub(conn) == True :
        for i in range (len(conn)) : conn[i].close()
        print("gg wp")



if __name__ == '__main__':
    main(sys.argv[1:])
