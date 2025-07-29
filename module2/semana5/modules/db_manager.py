import psycopg2
import os
from config import (DB_USER,DB_PASSWORD,DB_HOST,DB_PORT,SQL_FILE)


class db_manager:
    def __init__(self, dbname=None):
        self.dbname="postgres" if None else dbname
        self.sql_file=SQL_FILE
        self.user=DB_USER
        self.password=DB_PASSWORD
        self.host=DB_HOST
        self.port=DB_PORT
        self.connection = self.create_connection()
        if self.connection:
            print("Connected to database!")
            self.cursor = self.connection.cursor()
        
    def create_connection(self):
        try:
            return psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            ) 
        except Exception as error:
            print("Error connecting to the database:", error)
            return None

    def execute_query(self, query, *args):
        self.cursor.execute(query, args)
        self.connection.commit()
        if self.cursor.description:
            results = self.cursor.fetchall()
            return results

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Connection closed")
    
    def create_database_if_not_exists(self):
        self.connection.autocommit = True
        with self.connection.cursor() as cur:
            cur.execute(f"SELECT 1 FROM pg_database WHERE datname = %s", (self.dbname,))
            exists = cur.fetchone()
            if not exists:
                print(f"Creating database: {self.dbname}")
                cur.execute(f"CREATE DATABASE {self.dbname} OWNER {self.user}")
            else:
                print(f"Database {self.dbname} already exists.")

    def initialize_schema(self):
        with self.connection.cursor() as cur:
            with open(self.sql_file, 'r') as f:
                sql_script = f.read()
                cur.execute(sql_script)
            print("Schema initialized successfully.")

# Run setup
if __name__ == "__main__":
    db_manager=db_manager()
    db_manager.create_database_if_not_exists()
    db_manager.initialize_schema()

