from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import datetime, timedelta
import re



EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX=re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$')


class User:
    
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.language = data['language']
        self.birth_date = data['birth_date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def create_user(cls, form):
        query = 'INSERT INTO users (first_name, last_name, email, password, language, birth_date) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(language)s, %(birth_date)s)'
        result = connectToMySQL('login').query_db(query,form)
        return result

    @classmethod
    def user_by_email(cls, form):
        query = 'SELECT * FROM users WHERE email = %(email)s'
        result = connectToMySQL('login').query_db(query, form)
        if len(result)<1:
            return False
        else:
            user=cls(result[0])
            return user
        
    @classmethod
    def user_by_id(cls, form):
        query = 'SELECT * FROM users WHERE id= %(id)s'
        result = connectToMySQL('login').query_db(query,form)
        user = cls(result[0])
        return user
    
    @staticmethod
    def validation(form):
        is_valid=True
        if len(form['first_name'])<2:
            flash('First name at least 2 characters', 'register')
            is_valid = False
        if len(form['last_name'])<2:
            flash('Last name at least 2 characeters', 'register')
            is_valid=False
        if not EMAIL_REGEX.match(form['email']):
            flash('Use a valid email address', 'register')
            is_valid=False
        query = 'SELECT * FROM users WHERE email=%(email)s'
        results = connectToMySQL('login').query_db(query, form)
        if len(results)>=1:
            flash('Email already exists', 'register')
            is_valid=False
        #que se les requiera tener al menos 10 años de edad para poder registrarse
        date_1=datetime.strptime((form['birth_date']),'%Y-%m-%d')
        date_2=datetime.today()
        yeardate_1 = int(date_1.strftime("%Y"))
        years=(date_2-date_1)/timedelta(days=365)
        if round(years,0)<10:
            flash('You are too young','register')
            is_valid=False
        if (not form['birth_date']) or (yeardate_1<1900) or (yeardate_1>2022):
            flash('Date invalid', 'register')
            is_valid=False
        if not PASSWORD_REGEX.match(form['password']):
            flash('Password should be a combination of upper and lowercase letters, numbers, and special symbols.', 'register')
            is_valid=False
        if form['password']!=form['c_password']:
            flash('Passwords dont match', 'register')
            is_valid=False
        return is_valid