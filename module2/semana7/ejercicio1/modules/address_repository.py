import json
from flask import (Flask, request, jsonify)
from datetime import date
from modules.repository import Repository
from modules.models import _models
from sqlalchemy.orm import joinedload
from modules.jwt_manager import require_jwt



class AddressRepository(Repository):
    def __init__(self, db_manager, *args, **kwargs):
        # Ensure MethodView init runs and accept extra args if Flask passes any
        super().__init__(*args, **kwargs)
        self.manager = db_manager
        self.model_name = 'address'
        self.model_class = _models.get(self.model_name)

    def _get_model(self):
        if not self.model_class:
            raise ValueError(f"Model '{self.model_name}' not found")
        return self.model_class

    @require_jwt("administrator")
    def get(self, id=None, with_relationships=True):
        """
        Get address records.
        
        Args:
            id: Optional ID from URL path parameter
            with_relationships: Whether to load related user data
        """
        model_class = self._get_model()
        session = self.manager.sessionlocal()
        
        # If id is provided, try to get by ID
        if id:
            try:
                record_id = int(id)
                _query = session.query(model_class).filter_by(id=record_id)
            except ValueError:
                return jsonify({"error": "Invalid ID format"}), 400
        else:
            _query = session.query(model_class)
        
        if with_relationships:
            _query = _query.options(joinedload(model_class.user))
        
        addresses = self.manager.get(_query)
        
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
            if with_relationships and hasattr(address, 'user') and address.user:
                import ipdb; ipdb.set_trace()
                address_data["user"] = {
                    "id": address.user.id,
                    "user name": f"{address.user.first_name} {address.user.last_name}",
                    "email": address.user.email
                }
            
            address_list.append(address_data)
        
        # Return single object if querying by ID, otherwise return list
        if id and address_list:
            return jsonify(address_list[0])
        
        return jsonify(address_list)

    @require_jwt("administrator")
    def post(self):
        session = self.manager.sessionlocal()
        model_class = self._get_model()
        data = request.get_json()
        new_record = model_class(**data)
        record = self.manager.insert(session, new_record)
        if record is None:
            return jsonify({
            "error": "Address already exists or violates database constraints",
            "message": "This postal code may already be registered or the data conflicts with existing records"
        }), 409
        return jsonify({
            "postal_code": record.postal_code,
            "country": record.country,
            "state": record.state,
            "created_at": str(record.created_at)
        })
    
    @require_jwt("administrator")
    def put(self, id):
        """
        Update Address information (e.g., change street or city).
        """
        data = request.get_json()
        if not data:
            return jsonify({"error": "No fields to update"}), 400
        model_class = self._get_model()
        new_record = model_class(**data)
        if not id:
            return jsonify({"error": "Registration ID is required"}), 400
        try:
            session = self.manager.sessionlocal()
            _query = session.query(model_class).filter_by(id=id)
            records = self.manager.get(_query)
            current_record = records[0]
            import ipdb; ipdb.set_trace()
            # Get fields to update (exclude id)
            update_data = {k: v for k, v in request.json.items() if k != 'id'}
            
            if not update_data:
                return jsonify({"error": "No fields to update"}), 400
            
            # Update registration
            updated_reg = self.manager.update(session, new_record)
            
            return jsonify({
                "id": updated_reg.id,
                "email": updated_reg.email,
                "role": updated_reg.role,
                "updated_at": str(updated_reg.updated_at)
            })
            
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    
    @require_jwt("administrator")
    def delete(self, id):
        if not id:
            return jsonify({"error": "Address ID is required"}), 400
        try:
            model_class = self._get_model()
            session = self.manager.sessionlocal()
            message = self.manager.delete(session, model_class, id)
            return jsonify({"message": message}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 400
