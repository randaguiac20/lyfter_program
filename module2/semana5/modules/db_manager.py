import os
import psycopg2
from modules.config import (DB_NAME, DB_USERNAME, DB_PASSWORD,
                            DB_HOST, DB_PORT, SQL_FILE)


class db_manager:
    def __init__(self, dbname=None):
        # Target DB from arg, env, or config
        self.target_dbname = os.environ.get("DB_NAME", DB_NAME) or dbname
        self.user = DB_USERNAME
        self.password = DB_PASSWORD
        self.host = DB_HOST
        self.port = DB_PORT
        self.sql_file = SQL_FILE

        # Connect to 'postgres' for admin tasks
        self.connection = self.create_connection()
        self.cursor = self.connection.cursor() if self.connection else None
        if self.connection:
            print("Connected to Lyfter database!")

    def create_connection(self):
        dbname = self.target_dbname
        try:
            return psycopg2.connect(
                dbname=dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
            )
        except Exception as error:
            print(f"Error connecting to the database '{dbname}': {error}")
            return None

    def execute_query(self, query, params=None):
        if not self.connection or not self.cursor:
            raise RuntimeError("No active database connection")
        self.cursor.execute(query, params)
        self.connection.commit()
        if self.cursor.description:
            return self.cursor.fetchall()
        return None

    def close_connection(self):
        if getattr(self, "cursor", None):
            try:
                self.cursor.close()
            except Exception:
                pass
        if getattr(self, "connection", None):
            try:
                self.connection.close()
            except Exception:
                pass
        print("Connection closed")

    def create_database_if_not_exists(self):
        if not self.connection:
            print("Connection not established. Cannot create database.")
            return False
        self.connection.autocommit = True
        with self.connection.cursor() as cur:
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (self.target_dbname,))
            exists = cur.fetchone()
            if not exists:
                print(f"Creating database: {self.target_dbname}")
                cur.execute(f"CREATE DATABASE {self.target_dbname} OWNER {self.user}")
            else:
                print(f"Database {self.target_dbname} already exists.")

    def initialize_schema(self):
        if not self.connection:
            print("No connection to target database. Cannot initialize schema.")
            return
        if not os.path.isfile(self.sql_file):
            print(f"SQL file not found: {self.sql_file}")
            return
        with self.connection.cursor() as cur:
            with open(self.sql_file, "r", encoding="utf-8") as f:
                sql_script = f.read()
            # Execute statements one-by-one to avoid issues with multiple commands
            statements = [s.strip() for s in sql_script.split(";")]
            for stmt in statements:
                if not stmt:
                    continue
                cur.execute(stmt + ";")
        self.connection.commit()
        print("Schema initialized successfully.")




