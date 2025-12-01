from sqlalchemy import (create_engine, MetaData, text)
from modules.config import (DB_HOST, DB_USERNAME, DB_PORT,
                            DB_PASSWORD, DB_NAME, SCHEMA,
                            Base)
from sqlalchemy.orm import (sessionmaker, joinedload)
from modules.models import _models


class DBManager:
    def __init__(self):
        self.db_uri = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
        self.engine = create_engine(self.db_uri, echo=False)
        self.schema = SCHEMA
        self.base = Base
        self.sessionlocal = sessionmaker(bind=self.engine)
        self.models = _models
        self._ensure_schema()
        self.drop_tables()
        self.create_tables()

    def _ensure_schema(self):
          with self.engine.begin() as conn:
            conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{self.schema}"'))

    def create_tables(self):
        self.base.metadata.create_all(self.engine)

    def drop_tables(self):
        self.base.metadata.drop_all(self.engine)

    def get_model(self, model_name):
        model_class = self.models.get(model_name.lower())
        if not model_class:
            raise ValueError(f"Model '{model_name}' not found")
        return model_class

    def get(self, model_name, with_relationships=True):
        session = self.sessionlocal()
        try:
            # Get the model class
            model_class = self.get_model(model_name)
            _query = session.query(model_class)
            
            if with_relationships:
                # Load relationships based on the model
                _model = model_name.lower() if isinstance(model_name, str) else model_name.__name__.lower()
                
                if _model == "user":
                    # Load address and car relationships for User
                    _query = _query.options(joinedload(model_class.address), joinedload(model_class.car))
                elif _model == "address":
                    # Load user relationship for Address
                    _query = _query.options(joinedload(model_class.user))
                elif _model == "car":
                    # Load user relationship for Car
                    _query = _query.options(joinedload(model_class.user))
            
            results = _query.all()
            return results
            
        except Exception as e:
            raise e
        finally:
            session.close()

    def insert(self, model_name, **kwargs):
        """
        Insert a new record into the database.
        
        Args:
            model_name: String name of the model (e.g., "User", "Address", "Car")
            **kwargs: Field values for the new record (e.g., first_name="John", email="john@example.com")
        
        Returns:
            The created object with its ID
        """
        session = self.sessionlocal()
        try:
            # Get the model class
            model_class = self.get_model(model_name)
            # Create new instance with provided data
            new_record = model_class(**kwargs)
            # Insert the data and commit
            session.add(new_record)
            session.commit()
            """
            NOTE: Skip this if
            - You don't need the ID or server-generated values
            - Performance is critical (it's an extra database query)
            - You're doing bulk inserts
            """
            session.refresh(new_record)
            
            return new_record
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def update(self, model_name, filter, **kwargs):
        session = self.sessionlocal()
        try:
            # Get the model class
            model_class = self.get_model(model_name)
            record = session.query(model_class).filter_by(id=filter).first()
            if not record:
                raise ValueError(f"{model_name} with filter {filter} not found")
            for key, value in kwargs.items():
                setattr(record, key, value)
            session.commit()
            session.refresh(record)
            return record
        except Exception as e:
            raise e

    def delete(self):
        pass

    def close(self):
        session = self.sessionlocal()
        session.close()

