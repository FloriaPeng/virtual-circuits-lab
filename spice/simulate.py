import PySpice.Logging.Logging as Logging
from PySpice.Spice.Netlist import Circuit
from PySpice.Spice.NgSpice.Shared import NgSpiceCommandError
from PySpice.Unit import *


def calculate_voltage(circuit, node1, node2):
    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    try:
        analysis = simulator.operating_point()
        if node2 == "gnd":
            return float(analysis[node1]), 201
        return float(analysis[node1]) - float(analysis[node2]), 201

    except NgSpiceCommandError as e:
        return {"message": "Invalid circuit simulation, " + str(e)}, 400


class Simulator:

    def __init__(self, circuit):
        self.circuit = circuit

    def simulate_circuit(self):
        logger = Logging.setup_logging()
        circuit_lab = self.circuit
        circuit = Circuit(circuit_lab["name"])
        output = []
        message = {}

        for element in circuit_lab:
            if element == "V":
                for dc_voltage_source in circuit_lab["V"]:
                    circuit.V(dc_voltage_source["name"],
                              circuit.gnd if dc_voltage_source["node1"] == "gnd" else dc_voltage_source["node1"],
                              circuit.gnd if dc_voltage_source["node2"] == "gnd" else dc_voltage_source["node2"],
                              dc_voltage_source["value"] @ u_V)

            elif element == "I":
                for dc_current_source in circuit_lab["I"]:
                    circuit.I(dc_current_source["name"],
                              circuit.gnd if dc_current_source["node1"] == "gnd" else dc_current_source["node1"],
                              circuit.gnd if dc_current_source["node2"] == "gnd" else dc_current_source["node2"],
                              dc_current_source["value"] @ u_A)

            elif element == "R":
                for resistor in circuit_lab["R"]:
                    circuit.R(resistor["name"],
                              circuit.gnd if resistor["node1"] == "gnd" else resistor["node1"],
                              circuit.gnd if resistor["node2"] == "gnd" else resistor["node2"],
                              resistor["value"] @ u_Ω)

            elif element == "L":
                for inductor in circuit_lab["L"]:
                    circuit.L(inductor["name"],
                              circuit.gnd if inductor["node1"] == "gnd" else inductor["node1"],
                              circuit.gnd if inductor["node2"] == "gnd" else inductor["node2"],
                              inductor["value"] @ u_H)

            elif element == "C":
                for capacitor in circuit_lab["C"]:
                    circuit.C(capacitor["name"],
                              circuit.gnd if capacitor["node1"] == "gnd" else capacitor["node1"],
                              circuit.gnd if capacitor["node2"] == "gnd" else capacitor["node2"],
                              capacitor["value"] @ u_F)

            elif element == "VM":
                for voltmeter in circuit_lab["VM"]:
                    measurement, code = calculate_voltage(circuit, voltmeter["node1"], voltmeter["node2"])
                    if code == 400:
                        return measurement, code
                    output.append(measurement)
                message["VM"] = output

        return message, 201
