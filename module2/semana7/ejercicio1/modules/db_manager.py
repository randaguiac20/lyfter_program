from sqlalchemy import (create_engine, MetaData, text)
from modules.config import (DB_HOST, DB_USERNAME, DB_PORT,
                            DB_PASSWORD, DB_NAME, SCHEMA,
                            Base)
from sqlalchemy.orm import (sessionmaker, scoped_session)



class DB_Manager:
    def __init__(self, drop_table=False):
        self.db_uri = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
        self.engine = create_engine(self.db_uri, echo=False)
        self.schema = SCHEMA
        self.base = Base
        self.sessionlocal = sessionmaker(bind=self.engine)
        self._session = scoped_session(self.sessionlocal)
        self._ensure_schema()
        if drop_table:
            self.drop_tables()
        self.create_tables()

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

    def get(self, query):
        try:
            results = query.all()
            return results
        except Exception as e:
            raise e

    def insert(self, new_record, session):
        try:
            session.add(new_record)
            session.commit()
            session.refresh(new_record)
            return new_record
        except Exception as e:
            session.rollback()
            raise e

    def update(self, session, model_class,
               filter, **kwargs):
        try:
            # Get the model class
            model_class = self.get_model(model_class)
            record = session.query(model_class).filter_by(id=filter).first()
            if not record:
                raise ValueError(f"{model_class} with filter {filter} not found")
            for key, value in kwargs.items():
                setattr(record, key, value)
            session.commit()
            session.refresh(record)
            return record
        except Exception as e:
            raise e

    def delete(self, session,  model_class, filter):
        try:
            # Get the model class
            model_class = self.get_model(model_class)
            record = session.query(model_class).filter_by(id=filter).first()
            if not record:
                raise ValueError(f"{model_class} with filter {filter} not found")
            session.delete(record)
            session.commit()
            msg = f"{record} has been DELETED"
            return msg
        except Exception as e:
            raise e
