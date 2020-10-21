import PySpice.Logging.Logging as Logging
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

logger = Logging.setup_logging()

thevenin_circuit = Circuit('Thévenin Representation')

thevenin_circuit.V('input', 1, thevenin_circuit.gnd, 10@u_V)
thevenin_circuit.R('generator', 1, 'load', 10@u_Ω)
thevenin_circuit.R('load', 'load', thevenin_circuit.gnd, 1@u_kΩ)

simulator = thevenin_circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.operating_point()

load_node = analysis.load
print('Node {}: {:5.2f} V'.format(str(load_node), float(load_node)))
