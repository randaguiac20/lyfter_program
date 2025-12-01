from sqlalchemy import (create_engine, MetaData, text)
from modules.config import (DB_HOST, DB_USERNAME, DB_PORT,
                    DB_PASSWORD, DB_NAME, SCHEMA)
from sqlalchemy.orm import (declarative_base, sessionmaker)


_metadata = MetaData(schema=SCHEMA)
Base = declarative_base(metadata=_metadata)

class DBManager:
    def __init__(self):
        self.db_uri = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
        self.engine = create_engine(self.db_uri, echo=True)
        self.schema = SCHEMA
        self.base = Base
        self.sessionlocal = sessionmaker(bind=self.engine)
        self._ensure_schema()

    def _ensure_schema(self):
          with self.engine.begin() as conn:
            conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{self.schema}"'))

    def create_tables(self):
        self.base.metadata.create_all(self.engine)

    def get(self):
        pass

    def insert(self):
        pass

    def delete(self):
        pass

    def commit(self):
        pass