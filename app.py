from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError
from flask_cors import CORS
from ma import ma
from db import db
from blacklist import BLACKLIST
from resources.user import UserRegister, UserLogin, User, TokenRefresh, UserLogout
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.simulate import StaticSimulator, DynamicSimulator

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_BLACKLIST_ENABLED"] = True  # enable blacklist feature
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = [
    "access",
    "refresh",
]  # allow blacklisting for access and refresh tokens
app.secret_key = "jose"  # could do app.config['JWT_SECRET_KEY'] if we prefer
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


# set app level error handlers
@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):  # except ValidationError as err
    return jsonify(err.messages), 400


jwt = JWTManager(app)


# This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
#@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")
api.add_resource(StaticSimulator, "/static_simulator/<string:name>")
api.add_resource(DynamicSimulator, "/dynamic_simulator/<string:name>")
# api.add_resource(StaticSimulator, "/subcircuit")  #endpoint to create subcircuit. TODO Name of subcircuit is in the url

if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app) # tell that marshmallow object what app it should be talking to
    app.run(port=5000, debug=True)
