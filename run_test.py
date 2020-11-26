import os
import sys
import psycopg2


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
    

def insert(conn) :
    insert_query = "INSERT INTO pgbench_tellers (tid, bid, tbalance, filler) VALUES (999, 999, 999, '');"
    for i in range(len(conn)) :
        cursor = conn[i].cursor()
        cursor.execute(insert_query)
        conn[i].commit ()
        cursor.close ()
                    

def check_sub(conn) :

    done_flag = [False for i in range(len(conn))]

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
                    done_flag[i] = True

        if False in done_flag :
            continue
        else :
            return True
            

def main(argv):

    ip_list = ['52.201.253.38', '54.209.168.101', '54.221.17.161']
    
    conn = init_conn(ip_list)

    #insert_query(conn)
    
    if check_sub(conn) == True :
        for i in range (len(conn)) : conn[i].close()
        print("gg wp")



if __name__ == '__main__':
    main(sys.argv[1:])
