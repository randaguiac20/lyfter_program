"""user_repository.py

User repository for managing user profile records.
Handles CRUD operations for user personal information including name,
telephone, and relationships to addresses and shopping carts.
"""

import json
import redis
from flask import (Flask, request, jsonify)
from datetime import date
from repositories.repository import Repository
from modules.models import _models
from modules.jwt_manager import require_jwt
from modules.cache_manager import CacheManager



class UserRepository(Repository):
    """
    Repository for managing user profiles.
    
    Handles user personal data with relationships to addresses,
    contacts, and shopping carts.
    
    Attributes:
        db_manager: Database manager instance.
        model_class: The User model class.
    """
    
    def __init__(self, db_manager, *args, **kwargs):
        """
        Initialize the user repository.
        
        Args:
            db_manager: Database manager instance.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        # Ensure MethodView init runs and accept extra args if Flask passes any
        super().__init__(*args, **kwargs)
        self.db_manager = db_manager
        self.model_class = _models.get('user')
        self.cache_manager = CacheManager()

    def _get(self, id=None, name=None):
        """
        Internal method to retrieve user records with relationships.
        
        Args:
            id (int, optional): Filter by user ID.
            name (str, optional): Filter by name.
            
        Returns:
            tuple: (JSON response with user data, HTTP status code)
        """
        # Cache layer with Redis
        cache_key = f"users:{id}" if id else "users:all"
        try:
            cached_data = self.cache_manager.get_data(cache_key)
        except redis.RedisError:
            cached_data = None
        if cached_data:
            print("Pull from Redis")
            return jsonify(json.loads(cached_data)), 200

        model_class = self.model_class
        relationship_list = [model_class.contacts, model_class.address, model_class.carts]
        session = self.db_manager.sessionlocal()
        users = self.db_manager.get_query(session, model_class, id=id, name=name,
                                          relationships=relationship_list)

        # If querying by ID and no result found
        if id and not users:
            return jsonify({"error": "User not found"}), 404
        
        # Convert SQLAlchemy objects to dictionaries
        user_list = []
        for user in users:
            user_data = {
                "id": user.id,
                "registration_id": user.registration_id,
                "user_name": f"{user.first_name} {user.last_name}",
                "created_at": str(user.created_at) if user.created_at else None,
                "updated_at": str(user.updated_at) if user.updated_at else None
            }
            # Include related address data if loaded
            if hasattr(user, 'address') and user.address:
                user_data["address"] = {
                    "id": user.address.id,
                    "street": user.address.street,
                    "city": user.address.city,
                    "state": user.address.state,
                    "postal_code": user.address.postal_code,
                    "country": user.address.country
                }
            # Include related contact data if loaded
            if hasattr(user, 'contacts') and user.contacts:
                contact_list = []
                for contact in user.contacts:
                    contact_data = {
                        "contact_id": contact.id,
                        "user_name": f"{user.first_name} {user.last_name}"
                    }
                    contact_list.append(contact_data)
                user_data["contacts"] = contact_list
            
            # Include related cart data if loaded
            if hasattr(user, 'carts') and user.carts:
                cart_list = []
                for cart in user.carts:
                    cart_data = {
                        "cart_id": cart.id,
                        "status": cart.status,
                        "purchase_date": cart.purchase_date
                    }
                    cart_list.append(cart_data)
                user_data['carts'] = cart_list
            
            user_list.append(user_data)

        self.cache_manager.store_data(cache_key, json.dumps(user_list), ttl=180)

        # Return single object if querying by ID, otherwise return list
        if id and user_list:
            return jsonify(user_list[0]), 200
        
        return jsonify(user_list), 200

    def _add(self, data):
        """
        Internal method to create a new user profile.
        
        Args:
            data (dict): User data with registration_id, first_name,
                        last_name, telephone, and address_id.
            
        Returns:
            tuple: (JSON response with new user data, HTTP status code)
        """
        session = self.db_manager.sessionlocal()
        model_class = self.model_class

        _user = model_class(**data)
        user = self.db_manager.insert(session, _user)
        
        if user is None:
            return jsonify({
            "error": "User already exists or violates database constraints",
            "message": "This user may already be registered or the data conflicts with existing records"
        }), 409

        try:
            self.cache_manager.delete_pattern("users:*")
        except redis.RedisError as e:
            print(f"Redis Error: {e}")

        return jsonify({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "created_at": str(user.created_at)
        }), 200

    def _update(self, id, new_data):
        """
        Internal method to update a user profile.
        
        Args:
            id (int): User ID to update.
            new_data (dict): Fields to update.
            
        Returns:
            tuple: (JSON response, HTTP status code)
        """
        if not new_data:
            return jsonify({"error": "No fields to update"}), 400
        
        if not id:
            return jsonify({"error": "User ID is required"}), 400
        
        try:
            model_class = self.model_class
            session = self.db_manager.sessionlocal()
            users = self.db_manager.get_query(session, model_class, id=id)
            user = users[0]
            if not user:
                return jsonify({"error": f"User ID {id} has not been found"}), 404
            
            for column in user.__table__.columns:
                field_name = column.name
                
                # Skip fields that shouldn't be updated
                if field_name in ('id', 'created_at', 'updated_at'):
                    continue
                
                # Check if field is in new_data
                if field_name in new_data:
                    old_value = getattr(user, field_name)
                    new_value = new_data[field_name]
                    
                    # Compare values (handle type conversions)
                    if str(old_value) != str(new_value):
                        setattr(user, field_name, new_value)
            
            if not user:
                return jsonify({"error": "No fields to update"}), 400

            # Update user
            updated_user = self.db_manager.update(session, user)

            try:
                self.cache_manager.delete_pattern("users:*")
            except redis.RedisError as e:
                print(f"Redis Error: {e}")

            if updated_user:
                return jsonify({
                    "id": updated_user.id,
                    "user_name": f"{updated_user.first_name} {updated_user.last_name}",
                    "updated_at": str(updated_user.updated_at)
                }), 200
            
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    def _remove(self, id):
        """
        Internal method to delete a user profile.
        
        Args:
            id (int): User ID to delete.
            
        Returns:
            tuple: (JSON response with deletion message, HTTP status code)
        """
        if not id:
            return jsonify({"error": "User ID is required"}), 400
        try:
            model_class = self.model_class
            session = self.db_manager.sessionlocal()
            users = self.db_manager.get_query(session, model_class, id=id)
            user = users[0]
            if not user:
                raise ValueError(f"User ID {id} has not been found")
            self.db_manager.delete(session, user)

            try:
                self.cache_manager.delete_pattern("users:*")
            except redis.RedisError as e:
                print(f"Redis Error: {e}")

            msg = f"User with ID {id} has been DELETED"
            return jsonify({"message": msg}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @require_jwt("administrator")
    def get(self, id=None):
        """
        Get user records.
        
        Args:
            id: Optional ID from URL path parameter
            with_relationships: Whether to load related user data
        """
        records, http_code = self._get(id=id)
        return records, http_code

    @require_jwt("administrator")
    def post(self):
        """
        Create a new user profile.
        
        Requires administrator role.
        
        Returns:
            tuple: (JSON response with new user data, HTTP status code)
        """
        data = request.get_json()
        new_record, http_code = self._add(data)
        return new_record, http_code
    
    @require_jwt("administrator")
    def put(self, id):
        """
        Update User information (e.g., change role or password).
        """
        data = request.get_json()
        result = self._update(id, data)
        # Handle both tuple returns and single Response returns
        if isinstance(result, tuple):
            return result
        return result, 200
    
    @require_jwt("administrator")
    def delete(self, id):
        deleted_record, http_code = self._remove(id)
        return deleted_record, http_code
