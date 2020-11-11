import PySpice.Logging.Logging as Logging
from PySpice.Spice.Netlist import Circuit
from PySpice.Spice.NgSpice.Shared import NgSpiceCommandError
from PySpice.Unit import *


def calculate_voltage(circuit, node1, node2):
    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    try:
        analysis = simulator.operating_point()
        pos = 0 if node1 == "gnd" else float(analysis[node1])
        neg = 0 if node2 == "gnd" else float(analysis[node2])
        return pos - neg, 201

    except NgSpiceCommandError as e:
        return {"message": "Invalid circuit simulation, " + str(e)}, 400


def calculate_amp(circuit, ammeter):
    am_name = "v" + str(ammeter["name"])
    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    try:
        analysis = simulator.operating_point()
        return float(analysis[am_name]), 201

    except NgSpiceCommandError as e:
        return {"message": "Invalid circuit simulation, " + str(e)}, 400


class Simulator:

    def __init__(self, circuit):
        self.circuit = circuit  # json format of the circuit
        self.spice = None  # PySpice circuit

    def get_circuit(self):
        return self.circuit

    def get_spice(self):
        return self.spice

    def define_circuit(self):
        logger = Logging.setup_logging()
        circuit_lab = self.circuit
        circuit = Circuit(circuit_lab["name"])

        # add all elements to the PySpice circuit
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

            elif element == "AM":
                for ammeter in circuit_lab["AM"]:
                    circuit.V(ammeter["name"],
                              circuit.gnd if ammeter["node1"] == "gnd" else ammeter["node1"],
                              circuit.gnd if ammeter["node2"] == "gnd" else ammeter["node2"],
                              ammeter["value"] @ u_V)

        self.spice = circuit

    def circuit_op(self):
        circuit_lab = self.circuit
        circuit = self.spice
        volt_output = []
        amp_output = []
        message = {}

        # get measurements
        for element in circuit_lab:
            if element == "AM":
                for ammeter in circuit_lab["AM"]:
                    measurement, code = calculate_amp(circuit, ammeter)
                    if code == 400:
                        return measurement, code
                    amp_output.append({ammeter["name"]: measurement})
                message["AM"] = amp_output

            elif element == "VM":
                for voltmeter in circuit_lab["VM"]:
                    measurement, code = calculate_voltage(circuit, voltmeter["node1"], voltmeter["node2"])
                    if code == 400:
                        return measurement, code
                    volt_output.append({voltmeter["name"]: measurement})
                message["VM"] = volt_output

        print(message)
        return message, 201

    def circuit_runtime(self):
        pass
