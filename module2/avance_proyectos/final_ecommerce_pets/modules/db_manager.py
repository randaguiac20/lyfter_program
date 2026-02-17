"""db_manager.py

Database manager module for handling all database operations using SQLAlchemy ORM.
Provides session management, CRUD operations, and query building functionality.
"""

from sqlalchemy import (create_engine, text)
from sqlalchemy.exc import IntegrityError
from modules.config import (DB_HOST, DB_USERNAME, DB_PORT,
                            DB_PASSWORD, DB_NAME, SCHEMA,
                            Base)
from sqlalchemy.orm import (sessionmaker, scoped_session, joinedload)
from modules.models import _models



class DBManager:
    """
    Database Manager class for PostgreSQL operations using SQLAlchemy.
    
    Handles database connections, session management, and CRUD operations
    for all models in the application.
    
    Attributes:
        db_uri (str): PostgreSQL connection URI.
        engine: SQLAlchemy engine instance.
        schema (str): Database schema name.
        sessionlocal: Session factory for creating new sessions.
        _session: Scoped session for thread-safe operations.
        _models (dict): Dictionary mapping model names to model classes.
    """
    
    def __init__(self, model_name=None, db_uri=None):
        """
        Initialize the database manager.

        Args:
            model_name (str, optional): Name of the default model to use.
            db_uri (str, optional): Database URI. Defaults to PostgreSQL from .env.
        """
        if db_uri:
            self.db_uri = db_uri
        else:
            self.db_uri = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
        self.engine = create_engine(self.db_uri, echo=False)
        self.schema = SCHEMA
        self.base = Base
        self.sessionlocal = sessionmaker(bind=self.engine)
        self.session = self.sessionlocal()
        self._session = scoped_session(self.sessionlocal)
        self._models = _models
        self._model_name = model_name
        if self.engine.dialect.name == 'postgresql':
            self._ensure_schema()

    def _get_model_name(self, model_name):
        """
        Set and retrieve the model class by name.
        
        Args:
            model_name (str): Name of the model to retrieve.
            
        Returns:
            DBManager: Self reference for method chaining.
        """
        self.model_name = self._model_name if self._model_name else model_name
        self.model_class = self._models.get(self.model_name)
        return self

    def _get_model(self):
        """
        Get the currently set model class.
        
        Returns:
            class: The SQLAlchemy model class, or error message if not found.
        """
        if not self.model_class:
            return f"Model '{self.model_name}' not found or provided"
        return self.model_class
    
    def get_session(self):
        """
        Get a new scoped session instance.
        
        Returns:
            Session: SQLAlchemy scoped session.
        """
        return self._session()
    
    def remove_session(self):
        """
        Remove the current scoped session.
        
        Cleans up the session after request completion.
        """
        self._session.remove()
 
    def _ensure_schema(self):
        """
        Ensure the database schema exists.
        
        Creates the schema if it doesn't already exist.
        """
        with self.engine.begin() as conn:
            conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{self.schema}"'))

    def create_tables(self):
        """
        Create all database tables defined in the models.
        
        Uses SQLAlchemy's metadata to create tables that don't exist.
        """
        self.base.metadata.create_all(self.engine)

    def drop_tables(self):
        """
        Drop all database tables defined in the models.
        
        WARNING: This will delete all data in the tables.
        """
        self.base.metadata.drop_all(self.engine)

    def get_query(self, session, model_class, id=None, name=None,
                  email=None, relationships=[]):
        """
        Build and execute a query with optional filters and relationships.
        
        Args:
            session: SQLAlchemy session instance.
            model_class: The model class to query.
            id (int, optional): Filter by ID.
            name (str, optional): Filter by name.
            email (str, optional): Filter by email.
            relationships (list, optional): List of relationships to eager load.
            
        Returns:
            list: List of matching records.
            
        Raises:
            ValueError: If ID format is invalid.
            Exception: If query execution fails.
        """
        try:
            query= None
            _query = session.query(model_class)
            if relationships:
                for relationship in relationships:
                    query = _query.options(joinedload(relationship))
            if not query:
                query = _query
                print("No relationship found for this query")
            if id:
                try:
                    id = int(id)
                except ValueError:
                    raise ValueError(f"Invalid ID format: {id}")
                query = query.filter_by(id=id)
            elif name:
                query = query.filter_by(name=name)
            elif email:
                query = query.filter_by(email=email)
                      
            return self.get(query)
        except IntegrityError as e:
            session.rollback()
            return None
        except ValueError:
            raise  # Re-raise ValueError as-is
        except Exception as e:
            raise Exception("Failed to fetch records") from e

    def get(self, query):
        """
        Execute a query and return all results.
        
        Args:
            query: SQLAlchemy query object.
            
        Returns:
            list: All records matching the query.
            
        Raises:
            Exception: If query execution fails.
        """
        try:
            return query.all()
        except Exception as e:
            raise Exception("Failed to fetch records") from e
        
    def get_by_id(self, session, id):
        """
        Get a record by its ID.
        
        Args:
            session: SQLAlchemy session instance.
            id: The record ID to search for.
            
        Returns:
            list: List containing the matching record, or None if not found.
        """
        try:
            query = session.query(self.model_class).filter_by(id=id)
            return self.get(query)
        except IntegrityError as e:
            session.rollback()
            return None
        except Exception as e:
            raise Exception("Failed to fetch records") from e
        
    def get_by_name(self, session, name):
        """
        Get records by name.
        
        Args:
            session: SQLAlchemy session instance.
            name (str): The name to search for.
            
        Returns:
            list: List of matching records.
        """
        try:
            query = session.query(self.model_class).filter_by(name=name)
            return self.get(query)
        except IntegrityError as e:
            session.rollback()
            return None
        except Exception as e:
            raise Exception("Failed to fetch records") from e
        
    def get_by_email(self, session, email):
        """
        Get records by email address.
        
        Args:
            session: SQLAlchemy session instance.
            email (str): The email address to search for.
            
        Returns:
            list: List of matching records.
        """
        try:
            query = session.query(self.model_class).filter_by(email=email)
            return self.get(query)
        except IntegrityError as e:
            session.rollback()
            return None
        except Exception as e:
            raise Exception("Failed to fetch records") from e

    def insert(self, session, new_record):
        """
        Insert a new record into the database.
        
        Args:
            session: SQLAlchemy session instance.
            new_record: The model instance to insert.
            
        Returns:
            object: The inserted record with updated fields, or None if failed.
            
        Raises:
            Exception: If insertion fails due to non-integrity errors.
        """
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
        """
        Update an existing record in the database.
        
        Args:
            session: SQLAlchemy session instance.
            new_record: The model instance with updated fields.
            
        Returns:
            object: The updated record, or None if failed.
            
        Raises:
            Exception: If update fails due to non-integrity errors.
        """
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
        """
        Delete a record from the database.
        
        Args:
            session: SQLAlchemy session instance.
            record: The model instance to delete.
            
        Raises:
            Exception: If deletion fails due to non-integrity errors.
        """
        try:
            session.delete(record)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            return None
        except Exception as e:
            raise Exception("Failed to delete record") from e
