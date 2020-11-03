import PySpice.Logging.Logging as Logging
from PySpice.Doc.ExampleTools import find_libraries
from PySpice.Probe.Plot import plot
from PySpice.Spice.Library import SpiceLibrary
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

logger = Logging.setup_logging()

libraries_path = find_libraries()
spice_library = SpiceLibrary(libraries_path)

circuit = Circuit('Transistor')

circuit.V('power', 5, circuit.gnd, 15 @ u_V)
source = circuit.SinusoidalVoltageSource('in', 'in', circuit.gnd, amplitude=.5 @ u_V, frequency=1 @ u_kHz)
circuit.C(1, 'in', 2, 10 @ u_uF)
circuit.R(1, 5, 2, 100 @ u_kΩ)
circuit.R(2, 2, 0, 20 @ u_kΩ)
circuit.R('C', 5, 4, 10 @ u_kΩ)
circuit.BJT(1, 4, 2, 3, model='bjt')  # Q is mapped to BJT !
circuit.model('bjt', 'npn', bf=80, cjc=pico(5), rb=100)
circuit.R('E', 3, 0, 2 @ u_kΩ)
circuit.C(2, 4, 'out', 10 @ u_uF)
circuit.R('Load', 'out', 0, 1 @ u_MΩ)

# .ac dec 5 10m 1G

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.transient(step_time=source.period / 200, end_time=source.period * 2)
