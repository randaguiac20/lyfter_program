from modules.config import BACKUP_DIR
from datetime import datetime
import psycopg2
import os, csv



class HealthDBChecker:
    def __init__(self):
        self.conn = None
        self.tables = ["lyfter_car_rental.users", "lyfter_car_rental.cars",
                       "lyfter_car_rental.rentcar_users"]
        self.db_info = {
            "dbname": "lyfter",
            "user": "randall_aguilar",
            "password": "lyfter_password",
            "host": "localhost",
            "port": "5450"
        }

    def check_db_health(self):
        try:
            print("Connecting to the DB....")
            self.conn = psycopg2.connect(**self.db_info)
            self.cursor = self.conn.cursor()
            print("Connected to the DB....")
        except psycopg2.Error as e:
            print(f"DB Connection error: {e}")
        print("Starting health validation....\n")
        for table in self.tables:
            self.cursor.execute(f"SELECT * FROM {table};")
            if self.cursor.description:
                print(f"{table}: exist.\n")
                if table == "lyfter_car_rental.cars":
                    data = self.cursor.fetchall()
                    if not data:
                        print("DB error. No cars available\n")
            else:
                print(f"{table}: does NOT exist.\n")
    
    def close_connection(self):
        if self.conn:
            self.cursor.close()
            self.conn.close()

if __name__ == "__main__":
    db_backup = HealthDBChecker()
    db_backup.check_db_health()
    db_backup.close_connection()
