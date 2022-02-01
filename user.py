import sqlite3



class User():
    def __init__(self, id_, username, password):
        self.id = id_
        self.username = username
        self.password = password

    @classmethod
    def find_username(cls,username):
        connection  = sqlite3.connect('data.db')
        cursor =  connection.cursor()
        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,)) #single tuple (username,)
        row = result.fetchone()

        if row:
            user = cls(*row)
        else:
            None

        connection.close()
        return user

    @classmethod
    def find_id(cls,id_):
        connection  = sqlite3.connect('data.db')
        cursor =  connection.cursor()
        query = "SELECT * FROM users WHERE id_=?"
        result = cursor.execute(query, (id_,))
        row = result.fetchone()

        if row:
            user = cls(*row)
        else:
            None

        connection.close()
        return user


        