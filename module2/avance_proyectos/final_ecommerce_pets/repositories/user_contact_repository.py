"""user_contact_repository.py

User contact repository for managing user contact records.
Handles CRUD operations for user contacts with relationship to users.
"""

import json
from flask import (request, jsonify)
from repositories.repository import Repository
from modules.jwt_manager import require_jwt
from modules.models import _models


class UserContactRepository(Repository):
    """
    Repository for managing user contact records.

    Handles user contacts with relationship to user profiles.

    Attributes:
        db_manager: Database manager instance.
        model_class: The UserContact model class.
    """

    def __init__(self, db_manager, *args, **kwargs):
        """
        Initialize the user contact repository.

        Args:
            db_manager: Database manager instance.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.db_manager = db_manager
        self.model_class = _models.get('user_contact')

    def _get(self, id=None):
        """
        Internal method to retrieve user contact records.

        Args:
            id (int, optional): Filter by contact ID.

        Returns:
            tuple: (JSON response with contact data, HTTP status code)
        """
        model_class = self.model_class
        relationship_list = [model_class.user]
        session = self.db_manager.sessionlocal()
        contacts = self.db_manager.get_query(session, model_class, id=id,
                                              relationships=relationship_list)

        # If querying by ID and no result found
        if id and not contacts:
            return jsonify({"error": "User contact not found"}), 404

        # Convert SQLAlchemy objects to dictionaries
        contact_list = []
        for contact in contacts:
            contact_data = {
                "id": contact.id,
                "user_id": contact.user_id,
                "created_at": str(contact.created_at) if contact.created_at else None,
                "updated_at": str(contact.updated_at) if contact.updated_at else None
            }
            # Include related user data if loaded
            if hasattr(contact, 'user') and contact.user:
                contact_data["user"] = {
                    "id": contact.user.id,
                    "user_name": f"{contact.user.first_name} {contact.user.last_name}"
                }
            contact_list.append(contact_data)

        # Return single object if querying by ID, otherwise return list
        if id and contact_list:
            return jsonify(contact_list[0]), 200

        return jsonify(contact_list), 200

    def _add(self, data):
        """
        Internal method to create a new user contact.

        Args:
            data (dict): Contact data with user_id.

        Returns:
            tuple: (JSON response with new contact data, HTTP status code)
        """
        session = self.db_manager.sessionlocal()
        model_class = self.model_class

        _contact = model_class(**data)
        contact = self.db_manager.insert(session, _contact)
        if contact is None:
            return jsonify({
                "error": "User contact already exists or violates database constraints",
                "message": "This contact may already be registered or the data conflicts with existing records"
            }), 409
        return jsonify({
            "id": contact.id,
            "user_id": contact.user_id,
            "created_at": str(contact.created_at)
        }), 201

    def _update(self, id, new_data):
        """
        Internal method to update a user contact.

        Args:
            id (int): Contact ID to update.
            new_data (dict): Fields to update.

        Returns:
            tuple: (JSON response, HTTP status code)
        """
        if not new_data:
            return jsonify({"error": "No fields to update"}), 400

        if not id:
            return jsonify({"error": "User contact ID is required"}), 400

        try:
            model_class = self.model_class
            session = self.db_manager.sessionlocal()
            contacts = self.db_manager.get_query(session, model_class, id=id)
            contact = contacts[0]
            if not contact:
                return jsonify({"error": f"User contact ID {id} has not been found"}), 404

            for column in contact.__table__.columns:
                field_name = column.name

                # Skip fields that shouldn't be updated
                if field_name in ('id', 'created_at', 'updated_at'):
                    continue

                # Check if field is in new_data
                if field_name in new_data:
                    old_value = getattr(contact, field_name)
                    new_value = new_data[field_name]

                    # Compare values (handle type conversions)
                    if str(old_value) != str(new_value):
                        setattr(contact, field_name, new_value)

            if not contact:
                return jsonify({"error": "No fields to update"}), 400

            # Update contact
            updated_contact = self.db_manager.update(session, contact)
            if updated_contact:
                return jsonify({
                    "id": updated_contact.id,
                    "user_id": updated_contact.user_id,
                    "updated_at": str(updated_contact.updated_at)
                }), 200

        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    def _remove(self, id):
        """
        Internal method to delete a user contact.

        Args:
            id (int): Contact ID to delete.

        Returns:
            tuple: (JSON response with deletion message, HTTP status code)
        """
        if not id:
            return jsonify({"error": "User contact ID is required"}), 400
        try:
            model_class = self.model_class
            session = self.db_manager.sessionlocal()
            contacts = self.db_manager.get_query(session, model_class, id=id)
            contact = contacts[0]
            if not contact:
                raise ValueError(f"User contact ID {id} has not been found")
            self.db_manager.delete(session, contact)
            msg = f"User contact with ID {id} has been DELETED"
            return jsonify({"message": msg}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @require_jwt(["administrator", "client"])
    def get(self, id=None):
        """
        Get user contact records.

        Args:
            id: Optional ID from URL path parameter
        """
        records, http_code = self._get(id=id)
        return records, http_code

    @require_jwt("administrator")
    def post(self):
        """
        Create a new user contact.

        Requires administrator role.

        Returns:
            tuple: (JSON response with new contact data, HTTP status code)
        """
        data = request.get_json()
        new_record, http_code = self._add(data)
        return new_record, http_code

    @require_jwt("administrator")
    def put(self, id):
        """
        Update user contact information.
        """
        data = request.get_json()
        updated_record, http_code = self._update(id, data)
        return updated_record, http_code

    @require_jwt("administrator")
    def delete(self, id):
        """
        Delete a user contact.

        Requires administrator role.

        Args:
            id (int): Contact ID to delete.

        Returns:
            tuple: (JSON response with deletion message, HTTP status code)
        """
        deleted_record, http_code = self._remove(id)
        return deleted_record, http_code
