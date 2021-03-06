from flask_restful import Resource
from flask import request
from spice.simulate import Simulator

# This is the array of subcircuits. This will store the JSON objects.
# When a user right-clicks and selects "Create Subcircuit"
# then we just want to add it to the global array in the backend,
# nothing to create just yet.
global_array_of_subcircuits = {}

class Subciruit(Resource):

    @classmethod
    def post(cls, name: str):
        subcircuit_json = request.get_json()  # subcircuit elements
        global_array_of_subcircuits.update(subcircuit_json["name"], subcircuit_json)


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
        output = simulator.define_circuit()
        if output:
            return {"message": output}, 400
        output = simulator.circuit_runtime(circuit_json["time_interval"], circuit_json["step_size"])

        return output[0], output[1]
