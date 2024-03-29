import sqlite3 as sql
import os 
import sys
from init import * 

class Database:
    def __init__(self, database, check_same_thread: bool = False):
        self.db_connection = sql.connect(database, check_same_thread)
        self.cursor = self.db_connection.cursor()

    def execute(self, statement, __parameters = ()):
        self.cursor.execute(statement, __parameters)
    
    def commit(self):
        self.db_connection.commit()
    
    def close(self):
        self.cursor.close()
    
    def cursor_close(self):
        self.db_connection.close()
        
    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()
            

class Tools:
    def regen_world():
        os.remove(Files.world_database)
        db = Database(Files.world_database)
        db.execute(SQLDatabase.World.query)
        db.commit()
        db.close()