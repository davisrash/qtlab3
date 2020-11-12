from source.instrument import Instrument
import visa

#################################
# To Do:
#  - Add radians option to reference_phase_shift parameter.
#  - Find external_SR540_chopper_phase minval and maxval.
#  - Fix the preset commands
#     - frequency_preset,
#     - sine_out_amplitude_preset, and
#     - sine_out_dc_level_preset,
#    to work with multiple arguments.
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

	def do_get_timebase_mode(self):
		"""
		Queries the current external 10 MHz timebase mode (auto or internal).

		Input:
			None

		Output:
			mode (int) : timebase mode
		"""
		map = self.get_parameters()['timebase_mode']['format_map']
		return list(map.keys())[list(map.values()).index(self._visainstrument.query(':TBMODE?').replace('\n', ''))]
	
	def do_set_timebase_mode(self, mode):
		"""
		Sets the external 10 MHz timebase mode (auto or internal).

		Input:
			mode (int) : timebase mode

		Output:
			None
		"""
		self._visainstrument.write(':TBMODE {}'.format(self.get_parameters()['timebase_mode']['format_map'][mode]))
	
	def do_get_timebase_source(self):
		"""
		Queries the current 10 MHz timebase source (external (0) or internal (1)).

		Input:
			None
		
		Output:
			source (int) : timebase source
		"""
		self._visainstrument.query(':TBSTAT?').replace('\n', '')
	
	def do_get_reference_phase_shift(self):
		"""
		Queries the current reference phase shift.

		Input:
			None
		
		Output:
			phase_shift (float) : reference phase shift in degrees
		"""
		self._visainstrument.query(':PHAS?').replace('\n', '')
	
	def do_set_reference_phase_shift(self, phase_shift):
		"""
		Sets the reference phase shift.

		Input:
			phase_shift (float) : reference phase shift in degrees
		
		Output:
			None
		"""
		self._visainstrument.write(':PHAS {}'.format(phase_shift))
	
	def do_get_frequency(self):
		"""
		Queries the current internal frequency whenever the reference mode is one of Internal, Dual, or Chop. Otherwise, in External mode, the query returns the external frequency.
		
		Input:
			None
		
		Output:
			frequency (float) : internal or external frequency in hertz
		"""
		self._visainstrument.query(':FREQ?').replace('\n', '')
	
	def do_set_frequency(self, frequency):
		"""
		Sets the internal frequency.

		Input:
			frequency (float) : internal frequency in hertz
		Output:
			None
		"""
		self._visainstrument.write(':FREQ {}'.format(frequency))
	
	############

	def auto_phase_shift(self):
		"""
		Performs the Auto Phase function.

		Input:
			None
		
		Output:
			None
		"""
		self._visainstrument.write(':APHS')
