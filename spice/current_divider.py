import PySpice.Logging.Logging as Logging
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

logger = Logging.setup_logging()
circuit = Circuit('Current Divider')

circuit.I('input', 1, circuit.gnd, 1@u_A)  # Fixme: current value
circuit.R(1, 1, circuit.gnd, 2@u_kΩ)
circuit.R(2, 1, circuit.gnd, 1@u_kΩ)

for resistance in (circuit.R1, circuit.R2):
    resistance.minus.add_current_probe(circuit)  # to get positive value

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.operating_point()

# Fixme: current over resistor
for node in analysis.branches.values():
    print('Node {}: {:5.2f} A'.format(str(node), float(node)))  # Fixme: format value + unit
