import os
from sqlalchemy.orm import (declarative_base)
from sqlalchemy import MetaData


# DB options
DB_NAME = "lyfter_7_week_guiado"
DB_USERNAME = "randall_aguilar"
DB_PASSWORD = "lyfter_password"
DB_HOST = "localhost"
DB_PORT = "5451"
SQL_FILE = "database/schema.sql"
SCHEMA = "lyfter_week_7_guiado"

# SCHEMA and ORM Base
_metadata = MetaData(schema=SCHEMA)
Base = declarative_base(metadata=_metadata)
