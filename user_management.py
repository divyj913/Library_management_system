# library_management_system/user_management.py
import re

class UserManager:
    def __init__(self, database):
        self.db = database

    def validate_email(self, email):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None

    def add_user(self, user_data):
        # Validate user data
        required_fields = ['name', 'email', 'phone', 'address']
        for field in required_fields:
            if not user_data.get(field):
                raise ValueError(f"{field.capitalize()} is required")

        # Email validation
        if not self.validate_email(user_data['email']):
            raise ValueError("Invalid email format")

        # Phone number validation (simple check)
        if not user_data['phone'].isdigit():
            raise ValueError("Phone number must contain only digits")

        self.db.insert_user(user_data)
        return "User added successfully"

    def get_all_users(self):
        return self.db.fetch_all_users()