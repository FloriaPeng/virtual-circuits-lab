import PySpice.Logging.Logging as Logging
from PySpice.Spice.Netlist import Circuit
from PySpice.Spice.Netlist import SubCircuit
from PySpice.Spice.NgSpice.Shared import NgSpiceCommandError
from PySpice.Doc.ExampleTools import find_libraries
from PySpice.Spice.Library import SpiceLibrary
from PySpice.Unit import *
import os
import sys
from PySpice.Tools.Path import parent_directory_of
import numpy as np


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
    am_name = "v" + str(ammeter["id"])
    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    try:
        analysis = simulator.operating_point()
        return float(analysis[am_name]), 201

    except NgSpiceCommandError as e:
        return {"message": "Invalid circuit simulation, " + str(e)}, 400


def display_voltage(circuit, node1, node2, time_interval, step_size):
    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    try:
        analysis = simulator.transient(step_time=step_size, end_time=time_interval)
        pos = 0 if node1 == "gnd" else np.asarray(analysis[node1])
        neg = 0 if node2 == "gnd" else np.asarray(analysis[node2])
        return pos - neg, 201

    except NgSpiceCommandError as e:
        return {"message": "Invalid circuit simulation, " + str(e)}, 400


def display_amp(circuit, ammeter, time_interval, step_size):
    am_name = "v" + str(ammeter["id"])
    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    try:
        analysis = simulator.transient(step_time=step_size, end_time=time_interval)
        return np.asarray(analysis[am_name]), 201

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

    # This definition is to create a subcircuit when we run a circuit
    def define_subcircuit(self, my_subcircuit):
        logger = Logging.setup_logging()
        circuit_lab = my_subcircuit
        subcircuit = SubCircuit(circuit_lab["name"])

        python_file = os.path.abspath(sys.argv[0])
        examples_root = parent_directory_of(python_file)
        libraries_path = os.path.join(examples_root, 'libraries')

        spice_library = SpiceLibrary(libraries_path)
        message = ""

        # add all elements to the PySpice circuit
        for element in circuit_lab:
            if element == "R":
                for resistor in circuit_lab["R"]:
                    subcircuit.R(resistor["id"],
                              subcircuit.gnd if resistor["node1"] == "gnd" else resistor["node1"],
                              subcircuit.gnd if resistor["node2"] == "gnd" else resistor["node2"],
                              resistor["value"] @ u_Ω)

            elif element == "L":
                for inductor in circuit_lab["L"]:
                    subcircuit.L(inductor["id"],
                              subcircuit.gnd if inductor["node1"] == "gnd" else inductor["node1"],
                              subcircuit.gnd if inductor["node2"] == "gnd" else inductor["node2"],
                              inductor["value"] @ u_H)

            elif element == "C":
                for capacitor in circuit_lab["C"]:
                    subcircuit.C(capacitor["id"],
                              subcircuit.gnd if capacitor["node1"] == "gnd" else capacitor["node1"],
                              subcircuit.gnd if capacitor["node2"] == "gnd" else capacitor["node2"],
                              capacitor["value"] @ u_F)

            elif element == "D":
                for diode in circuit_lab["D"]:
                    try:
                        subcircuit.include(spice_library[diode["modelType"]])
                        subcircuit.X(diode["id"],
                                  diode["modelType"],
                                  subcircuit.gnd if diode["node1"] == "gnd" else diode["node1"],
                                  subcircuit.gnd if diode["node2"] == "gnd" else diode["node2"])
                    except KeyError as e:
                        message += " " + str(e)

        if not message:
            self.spice = subcircuit
            return message
        return "Undefined model type:" + message

    # TODO
    # https://pyspice.fabrice-salvaire.fr/releases/v1.4/api/PySpice/Spice/Netlist.html
    def define_circuit(self):
        logger = Logging.setup_logging()
        circuit_lab = self.circuit
        circuit = Circuit(circuit_lab["name"])  # Circuit is imported from PySpcie (it is a Netlist)
        # There's a method SubCircuitElement that is from class Pyspice.spice.Netlist.Netlist
        # libraries_path = find_libraries()

        python_file = os.path.abspath(sys.argv[0])
        examples_root = parent_directory_of(python_file)
        libraries_path = os.path.join(examples_root, 'libraries')

        spice_library = SpiceLibrary(libraries_path)
        message = ""

        # add all elements to the PySpice circuit
        for element in circuit_lab:
            if element == "V":
                for dc_voltage_source in circuit_lab["V"]:
                    circuit.V(dc_voltage_source["id"],
                              circuit.gnd if dc_voltage_source["node1"] == "gnd" else dc_voltage_source["node1"],
                              circuit.gnd if dc_voltage_source["node2"] == "gnd" else dc_voltage_source["node2"],
                              dc_voltage_source["value"] @ u_V)

            elif element == "VA":
                for ac_voltage_source in circuit_lab["VA"]:
                    circuit.SinusoidalVoltageSource(ac_voltage_source["id"],
                                                    circuit.gnd if ac_voltage_source["node1"] == "gnd" else
                                                    ac_voltage_source["node1"],
                                                    circuit.gnd if ac_voltage_source["node2"] == "gnd" else
                                                    ac_voltage_source["node2"],
                                                    amplitude=ac_voltage_source["amplitude"] @ u_V,
                                                    frequency=ac_voltage_source["frequency"] @ u_Hz,
                                                    offset=ac_voltage_source["offset"] @ u_V)

            elif element == "I":
                for dc_current_source in circuit_lab["I"]:
                    circuit.I(dc_current_source["id"],
                              circuit.gnd if dc_current_source["node1"] == "gnd" else dc_current_source["node1"],
                              circuit.gnd if dc_current_source["node2"] == "gnd" else dc_current_source["node2"],
                              dc_current_source["value"] @ u_A)

            elif element == "IA":
                for ac_current_source in circuit_lab["IA"]:
                    circuit.SinusoidalCurrentSource(ac_current_source["id"],
                                                    circuit.gnd if ac_current_source["node1"] == "gnd" else
                                                    ac_current_source["node1"],
                                                    circuit.gnd if ac_current_source["node2"] == "gnd" else
                                                    ac_current_source["node2"],
                                                    amplitude=ac_current_source["amplitude"] @ u_A,
                                                    frequency=ac_current_source["frequency"] @ u_Hz,
                                                    offset=ac_current_source["offset"] @ u_A)

            elif element == "R":
                for resistor in circuit_lab["R"]:
                    circuit.R(resistor["id"],
                              circuit.gnd if resistor["node1"] == "gnd" else resistor["node1"],
                              circuit.gnd if resistor["node2"] == "gnd" else resistor["node2"],
                              resistor["value"] @ u_Ω)

            elif element == "L":
                for inductor in circuit_lab["L"]:
                    circuit.L(inductor["id"],
                              circuit.gnd if inductor["node1"] == "gnd" else inductor["node1"],
                              circuit.gnd if inductor["node2"] == "gnd" else inductor["node2"],
                              inductor["value"] @ u_H)

            elif element == "C":
                for capacitor in circuit_lab["C"]:
                    circuit.C(capacitor["id"],
                              circuit.gnd if capacitor["node1"] == "gnd" else capacitor["node1"],
                              circuit.gnd if capacitor["node2"] == "gnd" else capacitor["node2"],
                              capacitor["value"] @ u_F)

            elif element == "D":
                for diode in circuit_lab["D"]:
                    try:
                        circuit.include(spice_library[diode["modelType"]])
                        circuit.X(diode["id"],
                                  diode["modelType"],
                                  circuit.gnd if diode["node1"] == "gnd" else diode["node1"],
                                  circuit.gnd if diode["node2"] == "gnd" else diode["node2"])
                    except KeyError as e:
                        message += " " + str(e)

            elif element == "nBJT":
                for nBJT in circuit_lab["nBJT"]:
                    try:
                        circuit.include(spice_library[nBJT["modelType"]])
                        circuit.BJT(nBJT["id"],
                                    circuit.gnd if nBJT["node1"] == "gnd" else nBJT["node1"],
                                    circuit.gnd if nBJT["node2"] == "gnd" else nBJT["node2"],
                                    circuit.gnd if nBJT["node3"] == "gnd" else nBJT["node3"],
                                    model=nBJT["modelType"])
                    except KeyError as e:
                        message += " " + str(e)

            elif element == "pBJT":
                for pBJT in circuit_lab["pBJT"]:
                    try:
                        circuit.include(spice_library[pBJT["modelType"]])
                        circuit.BJT(pBJT["id"],
                                    circuit.gnd if pBJT["node3"] == "gnd" else pBJT["node3"],
                                    circuit.gnd if pBJT["node2"] == "gnd" else pBJT["node2"],
                                    circuit.gnd if pBJT["node1"] == "gnd" else pBJT["node1"],
                                    model=pBJT["modelType"])
                    except KeyError as e:
                        message += " " + str(e)

            elif element == "AM":
                for ammeter in circuit_lab["AM"]:
                    circuit.V(ammeter["id"],
                              circuit.gnd if ammeter["node1"] == "gnd" else ammeter["node1"],
                              circuit.gnd if ammeter["node2"] == "gnd" else ammeter["node2"],
                              ammeter["value"] @ u_V)

            elif element == "X":
                my_subcircuit = myGlobalArray.get(ID)
                define_subcircuit(my_subcircuit)

        if not message:
            self.spice = circuit
            return message
        return "Undefined model type:" + message

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

    def circuit_runtime(self, time_interval, step_size):
        circuit_lab = self.circuit
        circuit = self.spice
        volt_output = []
        amp_output = []
        message = {}

        # get measurements
        for element in circuit_lab:
            if element == "AM":
                for ammeter in circuit_lab["AM"]:
                    measurement, code = display_amp(circuit, ammeter, time_interval, step_size)
                    if code == 400:
                        return measurement, code
                    amp_output.append({ammeter["name"]: measurement.tolist()})
                message["AM"] = amp_output

            elif element == "VM":
                for voltmeter in circuit_lab["VM"]:
                    measurement, code = display_voltage(circuit, voltmeter["node1"], voltmeter["node2"],
                                                        time_interval, step_size)
                    if code == 400:
                        return measurement, code
                    volt_output.append({voltmeter["name"]: measurement.tolist()})
                message["VM"] = volt_output

        print(message)
        return message, 201
