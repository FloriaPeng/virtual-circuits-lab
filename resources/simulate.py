from flask_restful import Resource
from flask import request

CIRCUIT_RECEIVED = "{} received"


class Simulate(Resource):

    circuit_json = {}

    @classmethod
    def get(cls, name: str):
        return cls.circuit_json, 200

    @classmethod
    def post(cls, name: str):
        cls.circuit_json = request.get_json()  # circuit elements
        cls.circuit_json["name"] = name  # the item name is not in the request body, instead, it is in the url

        # return {"message": CIRCUIT_RECEIVED.format(name)}, 201
        return cls.circuit_json, 201
