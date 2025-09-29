from modules.config import BACKUP_DIR
from datetime import datetime
import psycopg2
import os, csv



class db_backup_manager:
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
        self.backup_dir = BACKUP_DIR
        self.create_backup_dir = os.makedirs(self.backup_dir, exist_ok=True)

    def export_table_to_csv(self, table):
        current_time = datetime.now().strftime('%Y-%m-%d')
        filename = f"backup_{table}_{current_time}.csv"
        self.filepath = os.path.join(self.backup_dir, filename)
        self.cursor.execute(f"SELECT * FROM {table};")
        rows = self.cursor.fetchall()
        column_names = [colum[0] for colum in self.cursor.description]
        with open(self.filepath, 'w', newline='', encoding='utf-8') as csv_data:
            csv_writer = csv.writer(csv_data)
            csv_writer.writerow(column_names)
            csv_writer.writerows(rows)
        print(f"{table} was exported and backed up under {self.filepath}\n")

    def backup_data(self):
        try:
            print("Connecting to the DB....")
            self.conn = psycopg2.connect(**self.db_info)
            self.cursor = self.conn.cursor()
            print("Connected to the DB....")
        except psycopg2.Error as e:
            print(f"DB Connection error: {e}")
        print("Starting backup....")
        for table in self.tables:
            try:
                self.export_table_to_csv(table)
                print("Backup successfully done.")
            except Exception as e:
                print(f"\nTable export error: {e}")
        if self.conn:
            self.cursor.close()
            self.conn.close()

if __name__ == "__main__":
    db_backup = db_backup_manager()
    db_backup.backup_data()
