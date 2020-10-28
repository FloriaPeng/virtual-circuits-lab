from flask_restful import Resource
from flask import request

CIRCUIT_RECEIVED = "{} received"


class Simulate(Resource):

    @classmethod
    def post(cls, name: str):
        circuit_json = request.get_json()  # circuit elements
        circuit_json["name"] = name  # the item name is not in the request body, instead, it is in the url

        # return {"message": CIRCUIT_RECEIVED.format(name)}, 201
        return circuit_json, 201
