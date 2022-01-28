from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = "eee451b7ffefce1016d942a5555e4493"
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

items = []


class Items(Resource):
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {"item": item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {"message": f"this item, {name}, already exists"}, 400

        request_data = request.get_json()  # json payload
        item = {"name": name, "price": request_data['price']}
        items.append(item)
        return item, 201

    def put(self, name):
        return {'items': name}

    def delete(self, name):
        return {'items': name}


class Itemlist(Resource):
    def get(self):
        return items


api.add_resource(Items, '/item/<string:name>')
api.add_resource(Itemlist, '/items')

if __name__ == '__main__':
    app.run(debug=True)
