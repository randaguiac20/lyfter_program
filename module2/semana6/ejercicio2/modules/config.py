from sqlalchemy import (Column, MetaData, Integer,
                        ForeignKey, String, Table)
import os

DB_NAME = "lyfter_6_week"
DB_USERNAME = "randall_aguilar"
DB_PASSWORD = "lyfter_password"
DB_HOST = "localhost"
DB_PORT = "5450"
SQL_FILE = "database/schema.sql"
SCHEMA = "lyfter_week_6"

# DB Tables

user_table = Table(
    "address",
    MetaData(),
    Column("id", Integer, primary_key=True),
    Column("first_name", nullable=False),
    Column("last_name", String, nullable=False),
    Column("email", String, nullable=False),
)

address_table = Table(
    "address",
    MetaData(),
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("users.id"), nullable=False),
    Column("street", String, nullable=False),
    Column("city", String, nullable=False),
    Column("state", String),
    Column("postal_code", String),
    Column("country", String, nullable=False),
)

car_table = Table(
    "address",
    MetaData(),
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("users.id"), nullable=False),
    Column("brand", String, nullable=False),
    Column("model", String, nullable=False),
    Column("status", String, nullable=False),
    Column("email_address", String, nullable=False),
)
