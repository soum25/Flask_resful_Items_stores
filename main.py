from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity
from user import UserRegister

app = Flask(__name__)
app.secret_key = "eee451b7ffefce1016d942a5555e4493"
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

items = []


class Items(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True,
                        help="this field should be fill in")

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {"item": item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {"message": f"this item, {name}, already exists"}, 400
        request_data = Items.parser.parse_args()
        item = {"name": name, "price": request_data['price']}
        items.append(item)
        return item, 201

    def put(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        request_data = Items.parser.parse_args()
        if item is None:
            item = {"name": name, "price": request_data['price']}
            items.append(item)
        else:
            item.update(request_data)
        return item

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': f"this following item called {name} has been deleted"}


class Itemlist(Resource):
    def get(self):
        return items


api.add_resource(Items, '/item/<string:name>')
api.add_resource(Itemlist, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(debug=True)
