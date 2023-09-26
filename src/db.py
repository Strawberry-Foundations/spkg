import sqlite3 as sql
import os 
import sys
from init import * 


class StbWrapper():
    class DB:
        def __init__(self, file):
            self.db_connection = sql.connect(file, check_same_thread=False)
            self.cursor = self.db_connection.cursor()

        def execute(self, statement):
            self.db_connection.execute(statement)
        
        def commit(self):
            self.db_connection.commit()
        
        def close(self):
            self.db_connection.close()
            self.cursor.close()
            

class Tools:
    def regen_world():
        os.remove(Files.world_database)
        db = StbWrapper.DB(Files.world_database)
        db.execute(SQLDatabase.World.query)
        db.commit()
        db.close()
        print(StringLoader("RebuiltWorldDatabase"))