import PySpice.Logging.Logging as Logging
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

logger = Logging.setup_logging()
circuit = Circuit('Amp Meter')

circuit.V('input', 'in', circuit.gnd, 10@u_V)
circuit.V('meter1', 1, 'in', 0@u_V)
circuit.R(1, 1, 'out', 9@u_kΩ)
circuit.R(2, 'out', circuit.gnd, 1@u_kΩ)

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.operating_point()

print(float(analysis["vmeter1"]))
