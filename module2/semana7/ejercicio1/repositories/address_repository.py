import json
from flask import (Flask, request, jsonify)
from datetime import date
from repositories.repository import Repository
from modules.jwt_manager import require_jwt
from modules.models import _models



class AddressRepository(Repository):
    def __init__(self, db_manager, *args, **kwargs):
        # Ensure MethodView init runs and accept extra args if Flask passes any
        super().__init__(*args, **kwargs)
        self.db_manager = db_manager
        self.model_class = _models.get('address')

    def _get(self, id=None):
        model_class = self.model_class
        relationship_list = [model_class.users]
        session = self.db_manager.sessionlocal()
        addresses = self.db_manager.get_query(session, model_class, id=id,
                                              relationships=relationship_list)

        # If querying by ID and no result found
        if id and not addresses:
            return jsonify({"error": "Address not found"}), 404
        # Convert SQLAlchemy objects to dictionaries
        address_list = []
        for address in addresses:
            address_data = {
                "id": address.id,
                "postal_code": address.postal_code,
                "country": address.country,
                "state": address.state,
                "city": address.city,
                "street": address.street,
                "created_at": str(address.created_at) if address.created_at else None,
                "updated_at": str(address.updated_at) if address.updated_at else None
            }
            
            # Include related user data if loaded
            if hasattr(address, 'users') and address.users:
                users_list = []
                for user in address.users:
                    user_data = {
                        "id": user.id,
                        "user_name": f"{user.first_name} {user.last_name}"
                    }
                    users_list.append(user_data)
                address_data['users'] = users_list
            
            address_list.append(address_data)       
        # Return single object if querying by ID, otherwise return list
        if id and address_list:
            return jsonify(address_list[0]), 200
        
        return jsonify(address_list), 200

    def _add(self, data):
        session = self.db_manager.sessionlocal()
        model_class = self.model_class

        _address = model_class(**data)
        address = self.db_manager.insert(session, _address)
        if address is None:
            return jsonify({
                "error": "Address already exists or violates database constraints",
                "message": "This postal code may already be registered or the data conflicts with existing records"
            }), 409
        return jsonify({
            "id": address.id,
            "postal_code": address.postal_code,
            "country": address.country,
            "state": address.state,
            "created_at": str(address.created_at)
        }), 200

    def _update(self, id, new_data):
        if not new_data:
            return jsonify({"error": "No fields to update"}), 400
        
        if not id:
            return jsonify({"error": "Registration ID is required"}), 400
        
        try:
            model_class = self.model_class
            session = self.db_manager.sessionlocal()
            addresses = self.db_manager.get_query(session, model_class, id=id)
            address = addresses[0]
            if not address:
                return jsonify({"error": f"User ID {id} has not been found"}), 404
            
            for column in address.__table__.columns:
                field_name = column.name
                
                # Skip fields that shouldn't be updated
                if field_name in ('id', 'created_at', 'updated_at'):
                    continue
                
                # Check if field is in new_data
                if field_name in new_data:
                    old_value = getattr(address, field_name)
                    new_value = new_data[field_name]
                    
                    # Compare values (handle type conversions)
                    if str(old_value) != str(new_value):
                        setattr(address, field_name, new_value)
            
            if not address:
                return jsonify({"error": "No fields to update"}), 400

            # Update address
            updated_address = self.db_manager.update(session, address)
            if updated_address:
                msg = f"Address with ID {updated_address.id} has been UPDATED"
                return jsonify({"message": msg}), 200
            
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    def _remove(self, id):
        if not id:
            return jsonify({"error": "Address ID is required"}), 400
        try:
            model_class = self.model_class
            session = self.db_manager.sessionlocal()
            addresses = self.db_manager.get_query(session, model_class, id=id)
            address = addresses[0]
            if not address:
                raise ValueError(f"Address ID {id} has not been found")
            self.db_manager.delete(session, address)
            msg = f"Address with ID {id} has been DELETED"
            return jsonify({"message": msg}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @require_jwt("administrator")
    def get(self, id=None):
        """
        Get address records.
        
        Args:
            id: Optional ID from URL path parameter
            with_relationships: Whether to load related user data
        """
        records, http_code = self._get(id=id)
        return records, http_code

    @require_jwt("administrator")
    def post(self):
        data = request.get_json()
        new_record, http_code = self._add(data)
        return new_record, http_code
    
    @require_jwt("administrator")
    def put(self, id):
        """
        Update Address information (e.g., change street or city).
        """
        data = request.get_json()
        updated_record, http_code = self._update(id, data)
        return updated_record, http_code

    @require_jwt("administrator")
    def delete(self, id):
        deleted_record, http_code = self._remove(id)
        return deleted_record, http_code
