import matplotlib.pyplot as plt
import numpy as np
import PySpice.Logging.Logging as Logging
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

logger = Logging.setup_logging()
circuit = Circuit('Voltage Divider')

# https://pyspice.fabrice-salvaire.fr/releases/v1.3/api/PySpice/Spice/Netlist.html#PySpice.Spice.Netlist.Netlist
source = circuit.SinusoidalVoltageSource('input', 'in', circuit.gnd, amplitude=10@u_V, frequency=50@u_Hz, offset=10@u_V)
# source = circuit.SinusoidalCurrentSource('input', 'in', circuit.gnd, amplitude=10@u_A, frequency=50@u_Hz)
circuit.R('load', 'in', 'out', 100@u_Ω)
circuit.C('1', 'out', circuit.gnd, 1@u_mF)
# circuit.L('1', 'out', circuit.gnd, 1@u_mH)

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
# analysis = simulator.transient(step_time=source.period/200, end_time=source.period*20)
analysis = simulator.transient(step_time=5e-6, end_time=0.4)

# circuit.V('input', 'in', circuit.gnd, 10@u_V)
# circuit.R(1, 'in', 'out', 1@u_kΩ)
# circuit.C(2, 'out', circuit.gnd, 1@u_uF)
#
# simulator = circuit.simulator(temperature=25, nominal_temperature=25)
# analysis = simulator.transient(step_time=1e-5, end_time=30e-3)

print(np.asarray(analysis['out']))
out_arr = np.asarray(analysis['out'])
print(np.max(out_arr))
plt.plot(analysis['in'])
# plt.plot(analysis['out'])
plt.show()
