from flask_restful import Resource
from flask import request
from spice.simulate import Simulator


class StaticSimulator(Resource):

    @classmethod
    def post(cls, name: str):
        circuit_json = request.get_json()  # circuit elements
        circuit_json["name"] = name  # the item name is not in the request body, instead, it is in the url

        print(circuit_json)
        simulator = Simulator(circuit_json)
        output = simulator.define_circuit()
        if output:
            return {"message": output}, 400
        output = simulator.circuit_op()

        return output[0], output[1]


class DynamicSimulator(Resource):

    @classmethod
    def post(cls, name: str):
        circuit_json = request.get_json()  # circuit elements
        circuit_json["name"] = name  # the item name is not in the request body, instead, it is in the url

        print(circuit_json)
        simulator = Simulator(circuit_json)
        simulator.define_circuit()
        output = simulator.circuit_runtime(circuit_json["time_interval"], circuit_json["step_size"])

        return output[0], output[1]
