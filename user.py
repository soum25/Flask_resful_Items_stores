from importlib.resources import Resource
from multiprocessing import connection
import sqlite3
from flask import jsonify
from flask_restful import Resource, reqparse


class User():
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))  # single tuple (username,)
        row = result.fetchone()

        if row:
            user = cls(*row)
        else:
            None

        connection.close()
        return user

    @classmethod
    def find_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()

        if row:
            user = cls(*row)
        else:
            None

        connection.close()
        return user


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", required=True, type=str,
                        help="this should not be empty")
    parser.add_argument("password", required=True, type=str,
                        help="this should not be empty")

    def post(self):
        data = UserRegister.parser.parse_args()

        if User.find_username(data['username']):
            return ("Message: User already exists"), 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        insert_data = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(insert_data, (data['username'], data['password'],))

        connection.commit()
        connection.close()

        return ("Message: User created successfully"), 201
