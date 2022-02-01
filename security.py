from user import User

def authenticate(username, password):
    user = User.find_username(username)
    if user and user.password == password:
        return user


def identity(payload):
    user_id = payload['identity']
    return User.find_id(user_id)
