import threading
import time
from gstreamer import CCTV_VOD_THUMBNAIL
from thread import thread_camera
from db import run_query, select_query
import psycopg2
from datetime import datetime

thread_list = []

# cur.execute("DELETE FROM camera;")

while(True):
    list = select_query("SELECT * FROM camera;")
    for item in list:
        if (item[0] not in thread_list):
            query = "UPDATE camera SET online = 'NO' where id = {}".format(item[0])
            run_query(query)

            thread_list.append(item[0])
            threading.Thread(target=thread_camera, args=(item[0], item[2], item[6])).start()
    print(thread_list)
    time.sleep(60)