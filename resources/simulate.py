from flask_restful import Resource
from flask import request
from spice.simulate import Simulator
from resources.circuit_element import Circuit_element

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

        data_sent = request.get_json()  # JSON with {"raw_data" : ..., "processed_data": ...}
        # Extract raw_data
        raw_circuit = data_sent["raw_data"]
        circuit_element = Circuit_element(raw_circuit) # Make circuit_element object instance where raw_circuit is stored in a list of Part and Line objects
    
        # Form dictionary to send to Simulator class for processesing. --> Adjustment to fit pre-exisitng code in file.
        circuit_json = data_sent["processed_data"]
        circuit_json["name"] = name  # the item name is not in the request body, instead, it is in the url
        print(f"\nCircuit DICT sent to Simulator: {circuit_json}")
        
        simulator = Simulator(circuit_json)
        output = simulator.define_circuit()
        if output:
            return {"message": output}, 500
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
