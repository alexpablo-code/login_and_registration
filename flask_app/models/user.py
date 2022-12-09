from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash, session
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.t_-]+@[a-zA_Z0-9._-]+\.[a-zA-Z]+$')

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


class User:
    DB = "login_and_registration"

    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def create_user(cls, user_data):
        data = {
            "first_name": user_data['first_name'],
            "last_name": user_data['last_name'],
            "email": user_data['email'],
            "password": bcrypt.generate_password_hash(user_data['password'])
        }
        query = """
                INSERT INTO users (first_name, last_name, email, password, created_at, updated_at)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());
                """
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def one_user(cls,data):
        query = """
                SELECT * FROM users
                WHERE users.id = %(id)s;
                """
        results = connectToMySQL(cls.DB).query_db(query, data)

        return cls(results[0])


    @classmethod
    def email_unique(cls,user):
        data ={
            "email": user['email']
        }

        query = """
                SELECT * FROM users
                WHERE email = %(email)s;
                """
        results = connectToMySQL(cls.DB).query_db(query, data)

        unique = True 
        if not results:
            unique = False

        return unique

    @classmethod
    def select_by_email(cls, user_data):
        data = {
            "email": user_data['email']
        }
        query = """
                SELECT * FROM users
                WHERE email = %(email)s;
                """

        results = connectToMySQL(cls.DB).query_db(query, data)

        if not results:
            return False

        return cls(results[0])


    @staticmethod
    def validate_user(user):
        is_valid = True


        if not user['first_name'].isalpha():
            flash("First name is required", "error")
            is_valid = False

        if not user['last_name'].isalpha():
            flash("Last name is required", "error")
            is_valid = False

        if not user['email']:
            flash("Email is required", "error")
            is_valid = False

        elif not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address", "error")
            is_valid = False

        elif User.email_unique(user):
            flash("Email already exists")
            is_valid = False

        if len(user['password']) <= 0 or len(user['confirm_password']) <= 0:
            flash("Password is required")
            is_valid = False

        elif len(user['password']) < 8 or len(user['confirm_password']) < 8:
            flash("Password is required")
            is_valid = False

        elif not user['password'] == user['confirm_password']:
            flash("passwords don't match")
            is_valid = False

        return is_valid


    @staticmethod
    def validate_login(user_data):
        is_valid = True
        user_db = User.select_by_email(user_data)

        if len(user_data['email']) <= 0 or len(user_data['password']) <= 0:
            flash("email/password required", "login error")
            is_valid = False
            return is_valid
        

        elif not user_db:
            flash("Invalid email/password", "login error")
            is_valid = False
            return is_valid

        if not bcrypt.check_password_hash(user_db.password, user_data['password']):
            flash("Invalid email/password", "login error")
            is_valid = False

        return is_valid
