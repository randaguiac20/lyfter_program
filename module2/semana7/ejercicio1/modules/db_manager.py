from sqlalchemy import (create_engine, text)
from sqlalchemy.exc import IntegrityError
from modules.config import (DB_HOST, DB_USERNAME, DB_PORT,
                            DB_PASSWORD, DB_NAME, SCHEMA,
                            Base)
from sqlalchemy.orm import (sessionmaker, scoped_session)
from modules.models import _models



class DBManager:
    def __init__(self, model_name=None):
        self.db_uri = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
        self.engine = create_engine(self.db_uri, echo=False)
        self.schema = SCHEMA
        self.base = Base
        self.sessionlocal = sessionmaker(bind=self.engine)
        self.session = self.sessionlocal()
        self._session = scoped_session(self.sessionlocal)
        self._models = _models
        self._ensure_schema()

    def _get_model_name(self, model_name):
        self.model_name = model_name
        self.model_class = self._models.get(self.model_name)

    def _get_model(self):
        if not self.model_class:
            return f"Model '{self.model_name}' not found or provided"
        return self.model_class
    
    def get_session(self):
        return self._session()
    
    def remove_session(self):
        self._session.remove()
 
    def _ensure_schema(self):
          with self.engine.begin() as conn:
            conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{self.schema}"'))

    def create_tables(self):
        self.base.metadata.create_all(self.engine)

    def drop_tables(self):
        self.base.metadata.drop_all(self.engine)

    def get_query(self, session):
        try:
            query = session.query(self.model_class)
            return self.get(query)
        except Exception as e:
            raise Exception("Failed to fetch records") from e

    def get(self, query):
        try:
            return query.all()
        except Exception as e:
            raise Exception("Failed to fetch records") from e
        
    def get_by_id(self, session, id):
        try:
            query = session.query(self.model_class).filter_by(id=id)
            return self.get(query)
        except IntegrityError as e:
            session.rollback()
            return None
        except Exception as e:
            raise Exception("Failed to fetch records") from e
        
    def get_by_email(self, session, email):
        try:
            query = session.query(self.model_class).filter_by(email=email)
            return self.get(query)
        except IntegrityError as e:
            session.rollback()
            return None
        except Exception as e:
            raise Exception("Failed to fetch records") from e

    def insert(self, session, new_record):
        try:
            session.add(new_record)
            session.commit()
            session.refresh(new_record)
            return new_record
        except IntegrityError as e:
            session.rollback()
            return None
        except Exception as e:
            session.rollback()
            raise Exception("Failed to insert record") from e

    def update(self, session, new_record):
        try:
            session.commit()
            session.refresh(new_record)
            return new_record
        except IntegrityError as e:
            session.rollback()
            return None
        except Exception as e:
            raise Exception("Failed to update record") from e

    def delete(self, session,  record):
        try:
            session.delete(record)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            return None
        except Exception as e:
            raise Exception("Failed to delete record") from e
