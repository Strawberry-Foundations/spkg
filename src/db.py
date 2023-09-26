import sqlite3 as sql
import os 
import sys
from init import * 


class DB:
    def __init__(self):
        pass

class Tools:
    def regen_world():
        os.remove(Files.world_database)
        tmp_db  = sql.connect(Files.world_database, check_same_thread=False)
        tmp_cur = tmp_db.cursor()
        tmp_cur.execute(SQLDatabase.World.query)
        tmp_db.commit()
        tmp_cur.close()
        tmp_db.close()
        print(StringLoader("RebuiltWorldDatabase"))