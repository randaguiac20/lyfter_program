import os
from sqlalchemy.orm import (declarative_base)
from sqlalchemy import MetaData


# DB options
DB_NAME = "lyfter_7_week"
DB_USERNAME = "randall_aguilar"
DB_PASSWORD = "lyfter_password"
DB_HOST = "localhost"
DB_PORT = "5451"
SQL_FILE = "database/schema.sql"
SCHEMA = "lyfter_week_7"

# SCHEMA and ORM Base
_metadata = MetaData(schema=SCHEMA)
Base = declarative_base(metadata=_metadata)
