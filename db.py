import psycopg2, os
from dotenv import load_dotenv

def create_database(database_name):
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_IP = os.getenv("DB_IP")
    DB_PORT = os.getenv("DB_PORT")

    #establishing the connection
    conn = psycopg2.connect(
    database="postgres", user=DB_USER, password=DB_PASSWORD, host=DB_IP, port= DB_PORT
    )
    conn.autocommit = True

    cur = conn.cursor()

    cur.execute("SELECT datname FROM pg_database;")

    list_database = cur.fetchall()

    if (database_name,) in list_database:
        print("'{}' Database already exist".format(database_name))
    else:
        print("'{}' Database not exist.".format(database_name))
        sql = 'CREATE database {}'.format(database_name)
        #Creating a database
        cur.execute(sql)
        #Closing the connection
        print('Done')
    #Preparing query to create a database