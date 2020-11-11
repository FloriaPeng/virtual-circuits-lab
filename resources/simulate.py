from flask_restful import Resource
from flask import request
from spice.simulate import Simulator


class DCSimulate(Resource):

    @classmethod
    def post(cls, name: str):
        circuit_json = request.get_json()  # circuit elements
        circuit_json["name"] = name  # the item name is not in the request body, instead, it is in the url

        print(circuit_json)
        simulator = Simulator(circuit_json)
        simulator.define_circuit()
        output = simulator.circuit_op()

        return output[0], output[1]


class ACSimulate(Resource):

    @classmethod
    def post(cls, name: str):
        circuit_json = request.get_json()  # circuit elements
        circuit_json["name"] = name  # the item name is not in the request body, instead, it is in the url

        print(circuit_json)
        simulator = Simulator(circuit_json)
        simulator.define_circuit()
        output = simulator.circuit_runtime()

        return output[0], output[1]
