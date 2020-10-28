import PySpice.Logging.Logging as Logging
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *


class Simulator:

    def __init__(self, circuit):
        self.circuit = circuit

    def simulate_circuit(self):
        logger = Logging.setup_logging()
        circuit = Circuit('Voltage Divider')

        circuit_lab = self.circuit
        voltage_source = circuit_lab["Voltage Source"]
        circuit.V(voltage_source["name"],
                  circuit.gnd if voltage_source["node1"] == "gnd" else voltage_source["node1"],
                  circuit.gnd if voltage_source["node2"] == "gnd" else voltage_source["node2"],
                  voltage_source["value"] @ u_V)
        for R in circuit_lab["R"]:
            resistor = R["R"]
            circuit.R(resistor["name"],
                      circuit.gnd if resistor["node1"] == "gnd" else resistor["node1"],
                      circuit.gnd if resistor["node2"] == "gnd" else resistor["node2"],
                      resistor["value"] @ u_Ω)

        simulator = circuit.simulator(temperature=25, nominal_temperature=25)

        analysis = simulator.operating_point()
        for node in (analysis['in'], analysis.out):  # .in is invalid !
            print('Node {}: {} V'.format(str(node), float(node)))

        return float(analysis.out)
