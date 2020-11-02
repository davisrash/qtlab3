from source.instrument import Instrument
import visa

#################################
# To Do:
#  - add radians option to reference_phase_shift parameter
#  - find external_SR540_chopper_phase minval and maxval
#  - fix the following preset commands
#     - frequency_preset
#     - sine_out_amplitude_preset
#     - sine_out_dc_level_preset
#    to work with multiple arguments
#################################

class SR860(Instrument):
	"""
	This is the python driver for the SR860 500 kHz DSP Lock-in Amplifier from Stanford Research Systems.

	Usage:
	Initialize with
	<name> = qt.instruments.create('<name>', 'SR860', address='<GPIB address>', reset=<bool>)
	"""
	def __init__(self, name, address, reset=False):
		"""
		Initializes the SR860.

		Input:
			name (str)    : name of the instrument
			address (str) : GPIB address
			reset (bool)  : resets to default values

		Output:
			None
		"""
		Instrument.__init__(self, name, tags=['physical'])
		self._visainstrument = visa.ResourceManager().get_instrument(address)

		# reference parameters
		self.add_parameter('timebase_mode', type=int, flags=Instrument.FLAG_GETSET, minval=0, maxval=1, format_map={0: 'AUTO', 1: 'IN'})
		self.add_parameter('timebase_source', type=int, flags=Instrument.FLAG_GET, minval=0, maxval=1)
		self.add_parameter('reference_phase_shift', type=float, flags=Instrument.FLAG_GETSET, minval=-360000, maxval=360000, units='DEG')
		self.add_parameter('frequency', type=float, flags=Instrument.FLAG_GETSET, minval=1e-3, maxval=500e6, units='HZ')
		self.add_parameter('internal_reference_frequency', type=float, flags=Instrument.FLAG_GETSET, minval=1e-3, maxval=500e6, units='HZ')
		self.add_parameter('external_reference_frequency', type=float, flags=Instrument.FLAG_GET, minval=1e-3, maxval=500e6, units='HZ')
		self.add_parameter('detection_frequency', type=float, flags=Instrument.FLAG_GET, minval=1e-3, maxval=500e6, units='HZ')
		self.add_parameter('reference_frequency_harmonic_detect', type=int, flags=Instrument.FLAG_GETSET, minval=1, maxval=99)
		self.add_parameter('external_frequency_harmonic_detect_dual_reference', type=int, flags=Instrument.FLAG_GETSET, minval=1, maxval=99)
		self.add_parameter('external_SR540_chopper_blade_slots', type=int, flags=Instrument.FLAG_GETSET, minval=0, maxval=1, format_map={0: 'SLT6', 1: 'SLT30'})
		self.add_parameter('external_SR540_chopper_phase', type=float, flags=Instrument.FLAG_GETSET, units='DEG')
		self.add_parameter('sine_out_amplitude', type=float, flags=Instrument.FLAG_GETSET, minval=1e-9, maxval=2.0, units='V')
		self.add_parameter('sine_out_dc_level', type=float, flags=Instrument.FLAG_GETSET, minval=-5.0, maxval=5.0, units='V')
		self.add_parameter('sine_out_dc_mode', type=int, flags=Instrument.FLAG_GETSET, minval=0, maxval=1, format_map={0: 'COM', 1: 'DIF'})
		self.add_parameter('reference_source', type=int, flags=Instrument.FLAG_GETSET, minval=0, maxval=3, format_map={0: 'INT', 1: 'EXT', 2: 'DUAL', 3: 'CHOP'})
		self.add_parameter('external_reference_trigger_mode', type=int, flags=Instrument.FLAG_GETSET, minval=0, maxval=2, format_map={0: 'SIN', 1: 'POS', 2: 'NEG'})
		self.add_parameter('external_reference_trigger_input', type=int, flags=Instrument.FLAG_GETSET, minval=0, maxval=1, format_map={0: '50', 1: '1M'})
		self.add_parameter('frequency_preset', type=float, flags=Instrument.FLAG_GETSET, minval=1e-3, maxval=500e6, units='HZ')
		self.add_parameter('sine_out_amplitude_preset', type=float, flags=Instrument.FLAG_GETSET, minval=1e-9, maxval=2.0, units='V')
		self.add_parameter('sine_out_dc_level_preset', type=float, flags=Instrument.FLAG_GETSET, minval=-5.0, maxval=5.0, units='V')

		# signal commands
		self.add_parameter('signal_input', type=int, flags=Instrument.FLAG_GETSET, minval=0, maxval=1, format_map={0: 'VOLT', 1: 'CURR'})
		self.add_parameter('voltage_input_mode', type=int, flags=Instrument.FLAG_GETSET, minval=0, maxval=1, format_map={0: 'A', 1: 'A-B'})
		self.add_parameter('voltage_input_coupling', type=int, flags=Instrument.FLAG_GETSET, minval=0, maxval=1, format_map={0: 'AC', 1: 'DC'})
		self.add_parameter('voltage_input_shields', type=int, flags=Instrument.FLAG_GETSET, minval=0, maxval=1, format_map={0: 'FLO', 1: 'GRO'})
		self.add_parameter('voltage_input_range', type=int, flags=Instrument.FLAG_GETSET, minval=0, maxval=4, format_map={0: 1.0, 1: 0.3, 2: 0.1, 3: 0.03, 4: 0.01})
		self.add_parameter('')

		# reference functions
		self.add_function('auto_phase_shift')
