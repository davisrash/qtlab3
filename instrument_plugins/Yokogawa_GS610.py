from source.instrument import Instrument
import visa

#################################
# To Do:
#  - add a python version of polymorphic functions to ease function calls to allow for calls like yoko.set_output('ON')
#     - fixes yoko.set_sense_integration_time('PLC')
#     - adds ability for yoko.get_source_delay('MIN') = yoko.get_source_delay_minimum(), etc.
#  - fix sweep file management parameters/functions
#  - make save/recall parameters back into functions
#################################

class Yokogawa_GS610(Instrument):
	"""
	This is the python driver for the GS610 Source Measure Unit from Yokogawa.
	
	Usage:
	Initialize with
	<name> = qt.instruments.create('<name>', 'Yokogawa_GS610', address='<GBIP address>', reset=<bool>)
	"""
	def __init__(self, name, address, reset=False):
		"""
		Initializes the Yokogawa_GS610.
		
		Input:
			name (str)    : name of the instrument
			address (str) : GPIB address
			reset (bool)  : resets to default values
		
		Output:
			None
		"""
		Instrument.__init__(self, name, tags=['physical'])
		self._visainstrument = visa.ResourceManager().get_instrument(address)
		
		# output parameters
		self.add_parameter('output', type=int, flags=Instrument.FLAG_GETSET, minval=0, maxval=2, format_map={0: '0', 1: '1', 2: 'ZERO'})
		self.add_parameter('output_program', type=int, flags=Instrument.FLAG_GETSET, minval=0, maxval=2, format_map={0: '0', 1: '1', 2: 'PULS'})
		
		# source parameters
		self.add_parameter('source_function', type=int, flags=Instrument.FLAG_GETSET, minval=0, maxval=1, format_map={0: 'VOLT', 1: 'CURR'})
		self.add_parameter('source_shape', type=int, flags=Instrument.FLAG_GETSET, minval=0, maxval=1, format_map={0: 'DC', 1: 'PULS'})
		self.add_parameter('source_mode', type=int, flags=Instrument.FLAG_GETSET, minval=0, maxval=2, format_map={0: 'FIX', 1: 'SWE', 2: 'LIST'})
		self.add_parameter('source_delay_minimum', type=float, flags=Instrument.FLAG_GET, units='s')
		self.add_parameter('source_delay_maximum', type=float, flags=Instrument.FLAG_GET, units='s')
		self.add_parameter('source_delay', type=float, flags=Instrument.FLAG_GETSET, minval=1e-6, maxval=3600, units='s')
		self.add_parameter('source_pulse_width_minimum', type=float, flags=Instrument.FLAG_GET, units='s')
		self.add_parameter('source_pulse_width_maximum', type=float, flags=Instrument.FLAG_GET, units='s')
		self.add_parameter('source_pulse_width', type=float, flags=Instrument.FLAG_GETSET, minval=1e-4, maxval=3600, units='s')
		self.add_parameter('source_list_select', type=str, flags=Instrument.FLAG_GETSET)
		self.add_parameter('source_list_catalog', type=list, flags=Instrument.FLAG_GET)
		self.add_parameter('source_voltage_range_minimum', type=float, flags=Instrument.FLAG_GET, units='V')
		self.add_parameter('source_voltage_range_maximum', type=float, flags=Instrument.FLAG_GET, units='V')
		self.add_parameter('source_voltage_range', type=float, flags=Instrument.FLAG_GETSET, minval=(float)(self.do_get_source_voltage_range_minimum()), maxval=(float)(self.do_get_source_voltage_range_maximum()), units='V')
		self.add_parameter('source_voltage_level_minimum', type=float, flags=Instrument.FLAG_GET, units='V')
		self.add_parameter('source_voltage_level_maximum', type=float, flags=Instrument.FLAG_GET, units='V')
		self.add_parameter('source_voltage_level', type=float, flags=Instrument.FLAG_GETSET, minval=(float)(self.do_get_source_voltage_level_minimum()), maxval=(float)(self.do_get_source_voltage_level_maximum()), units='V')
		self.add_parameter('source_voltage_pulse_base_minimum', type=float, flags=Instrument.FLAG_GET, units='V')
		self.add_parameter('source_voltage_pulse_base_maximum', type=float, flags=Instrument.FLAG_GET, units='V')
		self.add_parameter('source_voltage_pulse_base', type=float, flags=Instrument.FLAG_GETSET, minval=(float)(self.do_get_source_voltage_pulse_base_minimum()), maxval=(float)(self.do_get_source_voltage_pulse_base_maximum()), units='V')
		self.add_parameter('source_voltage_protection_upper_limit_minimum', type=float, flags=Instrument.FLAG_GET, units='V')
		self.add_parameter('source_voltage_protection_upper_limit_maximum', type=float, flags=Instrument.FLAG_GET, units='V')
		self.add_parameter('source_voltage_protection_upper_limit', type=float, flags=Instrument.FLAG_GETSET, minval=(float)(self.do_get_source_voltage_protection_upper_limit_minimum()), maxval=(float)(self.do_get_source_voltage_protection_upper_limit_maximum()), units='V')
		self.add_parameter('source_voltage_protection_lower_limit_minimum', type=float, flags=Instrument.FLAG_GET, units='V')
		self.add_parameter('source_voltage_protection_lower_limit_maximum', type=float, flags=Instrument.FLAG_GET, units='V')
		self.add_parameter('source_voltage_protection_lower_limit', type=float, flags=Instrument.FLAG_GETSET, minval=(float)(self.do_get_source_voltage_protection_lower_limit_minimum()), maxval=(float)(self.do_get_source_voltage_protection_lower_limit_maximum()), units='V')
		self.add_parameter('source_voltage_sweep_start_minimum', type=float, flags=Instrument.FLAG_GET, units='V')
		self.add_parameter('source_voltage_sweep_start_maximum', type=float, flags=Instrument.FLAG_GET, units='V')
		self.add_parameter('source_voltage_sweep_start', type=float, flags=Instrument.FLAG_GETSET, minval=(float)(self.do_get_source_voltage_sweep_start_minimum()), maxval=(float)(self.do_get_source_voltage_sweep_start_maximum()), units='V')
		self.add_parameter('source_voltage_sweep_stop_minimum', type=float, flags=Instrument.FLAG_GET, units='V')
		self.add_parameter('source_voltage_sweep_stop_maximum', type=float, flags=Instrument.FLAG_GET, units='V')
		self.add_parameter('source_voltage_sweep_stop', type=float, flags=Instrument.FLAG_GETSET, minval=(float)(self.do_get_source_voltage_sweep_stop_minimum()), maxval=(float)(self.do_get_source_voltage_sweep_stop_maximum()), units='V')
		self.add_parameter('source_voltage_sweep_step_minimum', type=float, flags=Instrument.FLAG_GET, units='V')
		self.add_parameter('source_voltage_sweep_step_maximum', type=float, flags=Instrument.FLAG_GET, units='V')
		self.add_parameter('source_voltage_sweep_step', type=float, flags=Instrument.FLAG_GETSET, minval=(float)(self.do_get_source_voltage_sweep_step_minimum()), maxval=(float)(self.do_get_source_voltage_sweep_step_maximum()), units='V')
		self.add_parameter('source_voltage_sweep_points_minimum', type=int, flags=Instrument.FLAG_GET)
		self.add_parameter('source_voltage_sweep_points_maximum', type=int, flags=Instrument.FLAG_GET)
		self.add_parameter('source_voltage_sweep_points', type=int, flags=Instrument.FLAG_GET, minval=(int)(self.do_get_source_voltage_sweep_points_minimum()), maxval=(int)(self.do_get_source_voltage_sweep_points_maximum()))
		self.add_parameter('source_voltage_zero_impedance', type=int, flags=Instrument.FLAG_GETSET, minval=0, maxval=1, format_map={0: 'LOW', 1: 'HIGH'})
		self.add_parameter('source_voltage_zero_offset', type=float, flags=Instrument.FLAG_GETSET, minval=(float)(self.do_get_source_voltage_range_minimum()), maxval=(float)(self.do_get_source_voltage_range_maximum()), units='V')
		self.add_parameter('source_current_range_minimum', type=float, flags=Instrument.FLAG_GET, units='V')
		self.add_parameter('source_current_range_maximum', type=float, flags=Instrument.FLAG_GET, units='V')
		self.add_parameter('source_current_range', type=float, flags=Instrument.FLAG_GETSET, minval=(float)(self.do_get_source_current_range_minimum()), maxval=(float)(self.do_get_source_current_range_maximum()), units='V')
		self.add_parameter('source_current_level_minimum', type=float, flags=Instrument.FLAG_GET, units='V')
		self.add_parameter('source_current_level_maximum', type=float, flags=Instrument.FLAG_GET, units='V')
		self.add_parameter('source_current_level', type=float, flags=Instrument.FLAG_GETSET, minval=(float)(self.do_get_source_current_level_minimum()), maxval=(float)(self.do_get_source_current_level_maximum()), units='V')
		self.add_parameter('source_current_pulse_base_minimum', type=float, flags=Instrument.FLAG_GET, units='V')
		self.add_parameter('source_current_pulse_base_maximum', type=float, flags=Instrument.FLAG_GET, units='V')
		self.add_parameter('source_current_pulse_base', type=float, flags=Instrument.FLAG_GETSET, minval=(float)(self.do_get_source_current_pulse_base_minimum()), maxval=(float)(self.do_get_source_current_pulse_base_maximum()), units='V')
		self.add_parameter('source_current_protection_upper_limit_minimum', type=float, flags=Instrument.FLAG_GET, units='V')
		self.add_parameter('source_current_protection_upper_limit_maximum', type=float, flags=Instrument.FLAG_GET, units='V')
		self.add_parameter('source_current_protection_upper_limit', type=float, flags=Instrument.FLAG_GETSET, minval=(float)(self.do_get_source_current_protection_upper_limit_minimum()), maxval=(float)(self.do_get_source_current_protection_upper_limit_maximum()), units='V')
		self.add_parameter('source_current_protection_lower_limit_minimum', type=float, flags=Instrument.FLAG_GET, units='V')
		self.add_parameter('source_current_protection_lower_limit_maximum', type=float, flags=Instrument.FLAG_GET, units='V')
		self.add_parameter('source_current_protection_lower_limit', type=float, flags=Instrument.FLAG_GETSET, minval=(float)(self.do_get_source_current_protection_lower_limit_minimum()), maxval=(float)(self.do_get_source_current_protection_lower_limit_maximum()), units='V')
		self.add_parameter('source_current_sweep_start_minimum', type=float, flags=Instrument.FLAG_GET, units='V')
		self.add_parameter('source_current_sweep_start_maximum', type=float, flags=Instrument.FLAG_GET, units='V')
		self.add_parameter('source_current_sweep_start', type=float, flags=Instrument.FLAG_GETSET, minval=(float)(self.do_get_source_current_sweep_start_minimum()), maxval=(float)(self.do_get_source_current_sweep_start_maximum()), units='V')
		self.add_parameter('source_current_sweep_stop_minimum', type=float, flags=Instrument.FLAG_GET, units='V')
		self.add_parameter('source_current_sweep_stop_maximum', type=float, flags=Instrument.FLAG_GET, units='V')
		self.add_parameter('source_current_sweep_stop', type=float, flags=Instrument.FLAG_GETSET, minval=(float)(self.do_get_source_current_sweep_stop_minimum()), maxval=(float)(self.do_get_source_current_sweep_stop_maximum()), units='V')
		self.add_parameter('source_current_sweep_step_minimum', type=float, flags=Instrument.FLAG_GET, units='V')
		self.add_parameter('source_current_sweep_step_maximum', type=float, flags=Instrument.FLAG_GET, units='V')
		self.add_parameter('source_current_sweep_step', type=float, flags=Instrument.FLAG_GETSET, minval=(float)(self.do_get_source_current_sweep_step_minimum()), maxval=(float)(self.do_get_source_current_sweep_step_maximum()), units='V')
		self.add_parameter('source_current_sweep_points_minimum', type=int, flags=Instrument.FLAG_GET)
		self.add_parameter('source_current_sweep_points_maximum', type=int, flags=Instrument.FLAG_GET)
		self.add_parameter('source_current_sweep_points', type=int, flags=Instrument.FLAG_GET, minval=(int)(self.do_get_source_current_sweep_points_minimum()), maxval=(int)(self.do_get_source_current_sweep_points_maximum()))
		self.add_parameter('source_current_zero_impedance', type=int, flags=Instrument.FLAG_GETSET, minval=0, maxval=1, format_map={0: 'LOW', 1: 'HIGH'})
		self.add_parameter('source_current_zero_offset', type=float, flags=Instrument.FLAG_GETSET, minval=(float)(self.do_get_source_current_range_minimum()), maxval=(float)(self.do_get_source_current_range_maximum()), units='V')
		self.add_parameter('source_range_auto', type=int, flags=Instrument.FLAG_GETSET, minval=0, maxval=1)
		self.add_parameter('source_protection', type=int, flags=Instrument.FLAG_GETSET, minval=0, maxval=1)
		self.add_parameter('source_protection_linkage', type=int, flags=Instrument.FLAG_GETSET, minval=0, maxval=1)
		self.add_parameter('source_sweep_spacing', type=int, flags=Instrument.FLAG_GETSET, minval=0, maxval=1, format_map={0: 'LIN', 1: 'LOG'})
		
		# sweep parameters
		self.add_parameter('sweep_count_minimum', type=int, flags=Instrument.FLAG_GET)
		self.add_parameter('sweep_count_maximum', type=int, flags=Instrument.FLAG_GET)
		self.add_parameter('sweep_count', type=int, flags=Instrument.FLAG_GETSET, minval=(int)(self.do_get_sweep_count_minimum()), maxval=(int)(self.do_get_sweep_count_maximum()))
		self.add_parameter('sweep_last', type=int, flags=Instrument.FLAG_GETSET, minval=0, maxval=1, format_map={0: 'KEEP', 1: 'RET'})
		
		# measurement parameters
		self.add_parameter('sense', type=int, flags=Instrument.FLAG_GETSET, minval=0, maxval=1)
		self.add_parameter('sense_function', type=int, flags=Instrument.FLAG_GETSET, minval=0, maxval=2, format_map={0: 'VOLT', 1: 'CURR', 2: 'RES'})
		self.add_parameter('sense_range_auto', type=int, flags=Instrument.FLAG_GETSET, minval=0, maxval=1)
		self.add_parameter('sense_integration_time_minimum', type=float, flags=Instrument.FLAG_GET, units='s')
		self.add_parameter('sense_integration_time_maximum', type=float, flags=Instrument.FLAG_GET, units='s')
		self.add_parameter('sense_integration_time', type=float, flags=Instrument.FLAG_GETSET, minval=(float)(self.do_get_sense_integration_time_minimum()), maxval=(float)(self.do_get_sense_integration_time_maximum()), units='s')
		self.add_parameter('sense_delay_minimum', type=float, flags=Instrument.FLAG_GET, units='s')
		self.add_parameter('sense_delay_maximum', type=float, flags=Instrument.FLAG_GET, units='s')
		self.add_parameter('sense_delay', type=float, flags=Instrument.FLAG_GETSET, minval=(float)(self.do_get_sense_delay_minimum()), maxval=(float)(self.do_get_sense_delay_maximum()), units='s')
		self.add_parameter('sense_auto_zero', type=int, flags=Instrument.FLAG_GETSET, minval=0, maxval=1)
		self.add_parameter('sense_average', type=int, flags=Instrument.FLAG_GETSET, minval=0, maxval=1)
		self.add_parameter('sense_average_mode', type=int, flags=Instrument.FLAG_GETSET, minval=0, maxval=1, format_map={0: 'BLOC', 1: 'MOV'})
		self.add_parameter('sense_average_count_minimum', type=int, flags=Instrument.FLAG_GET)
		self.add_parameter('sense_average_count_maximum', type=int, flags=Instrument.FLAG_GET)
		self.add_parameter('sense_average_count', type=int, flags=Instrument.FLAG_GETSET, minval=(int)(self.do_get_sense_average_count_minimum()), maxval=(int)(self.do_get_sense_average_count_maximum()))
		self.add_parameter('sense_auto_change', type=int, flags=Instrument.FLAG_GETSET, minval=0, maxval=1)
		self.add_parameter('sense_remote_sense', type=int, flags=Instrument.FLAG_GETSET, minval=0, maxval=1)
		
		# trigger parameters
		self.add_parameter('trigger_source', type=int, flags=Instrument.FLAG_GETSET, minval=0, maxval=2, format_map={0: 'TIM', 1: 'EXT', 2: 'IMM'})
		self.add_parameter('trigger_timer_minimum', type=float, flags=Instrument.FLAG_GET, units='s')
		self.add_parameter('trigger_timer_maximum', type=float, flags=Instrument.FLAG_GET, units='s')
		self.add_parameter('trigger_timer', type=float, flags=Instrument.FLAG_GETSET, minval=(float)(self.do_get_trigger_timer_minimum()), maxval=(float)(self.do_get_trigger_timer_maximum()), units='s')
		
		# computation parameters
		self.add_parameter('calculate_null', type=int, flags=Instrument.FLAG_GETSET, minval=0, maxval=1)
		self.add_parameter('calculate_null_offset', type=float, flags=Instrument.FLAG_GETSET, minval=-9.99999e24, maxval=9.99999e24)
		self.add_parameter('calculate_math', type=int, flags=Instrument.FLAG_GETSET, minval=0, maxval=1)
		self.add_parameter('calculate_math_select', type=str, flags=Instrument.FLAG_GETSET)
		self.add_parameter('calculate_math_catalog', type=list, flags=Instrument.FLAG_GET)
		self.add_parameter('calculate_math_parameter_a', type=float, flags=Instrument.FLAG_GETSET, minval=-9.99999e24, maxval=9.99999e24)
		self.add_parameter('calculate_math_parameter_b', type=float, flags=Instrument.FLAG_GETSET, minval=-9.99999e24, maxval=9.99999e24)
		self.add_parameter('calculate_math_parameter_c', type=float, flags=Instrument.FLAG_GETSET, minval=-9.99999e24, maxval=9.99999e24)
		self.add_parameter('calculate_limit', type=int, flags=Instrument.FLAG_GETSET, minval=0, maxval=1)
		self.add_parameter('calculate_limit_upper_minimum', type=float, flags=Instrument.FLAG_GET)
		self.add_parameter('calculate_limit_upper_maximum', type=float, flags=Instrument.FLAG_GET)
		self.add_parameter('calculate_limit_upper', type=float, flags=Instrument.FLAG_GETSET, minval=(float)(self.do_get_calculate_limit_upper_minimum()), maxval=(float)(self.do_get_calculate_limit_upper_maximum()))
		self.add_parameter('calculate_limit_lower_minimum', type=float, flags=Instrument.FLAG_GET)
		self.add_parameter('calculate_limit_lower_maximum', type=float, flags=Instrument.FLAG_GET)
		self.add_parameter('calculate_limit_lower', type=float, flags=Instrument.FLAG_GETSET, minval=(float)(self.do_get_calculate_limit_lower_minimum()), maxval=(float)(self.do_get_calculate_limit_lower_maximum()))
		
		# store/recall parameters
		# test the data types of the returns
		#self.add_parameter('trace', type=int, flags=Instrument.FLAG_GETSET, minval=0, maxval=1)
		#self.add_parameter('trace_auto', type=int, flags=Instrument.FLAG_GETSET, minval=0, maxval=1)
		#self.add_parameter('trace_points_minimum', type=int, flags=Instrument.FLAG_GET)
		#self.add_parameter('trace_points_maximum', type=int, flags=Instrument.FLAG_GET)
		#self.add_parameter('trace_points', type=int, flags=Instrument.FLAG_GETSET, minval=(int)(self.do_get_trace_points_minimum()), maxval=(int)(self.do_get_trace_points_maximum()))
		#self.add_parameter('trace_actual', type=int, flags=Instrument.FLAG_GET, minval=(int)(self.do_get_trace_points_minimum()), maxval=(int)(self.do_get_trace_points_maximum()))
		#self.add_parameter('trace_calculate_minimum', type=float, flags=Instrument.FLAG_GET)
		#self.add_parameter('trace_calculate_maximum', type=float, flags=Instrument.FLAG_GET)
		#self.add_parameter('trace_calculate_average', type=float, flags=Instrument.FLAG_GET)
		#self.add_parameter('trace_calculate_standard_deviation', type=float, flags=Instrument.FLAG_GET)
		#self.add_parameter('trace_data_number_minimum', type=int, flags=Instrument.FLAG_GET)
		#self.add_parameter('trace_data_number_maximum', type=int, flags=Instrument.FLAG_GET)
		#self.add_parameter('trace_data_number', type=int, flags=Instrument.FLAG_GETSET, minval=(int)(self.do_get_trace_data_number_minimum()), maxval=(int)(self.do_get_trace_data_number_maximum()))
		#self.add_parameter('trace_data_time', type=str, flags=Instrument.FLAG_GET)
		#self.add_parameter('trace_data_source', type=float, flags=Instrument.FLAG_GET, units='V' if self.do_get_source_function() == 1 else 'A')
		#self.add_parameter('trace_data', flags=Instrument.FLAG_GET)
		#self.add_parameter('trace_data_setup', flags=Instrument.FLAG_GET)
		#self.add_parameter('trace_measurement_only')
		
		# external input/output parameters
		#self.add_parameter('route_BNC_input_select')
		#self.add_parameter('route_BNC_input_control')
		#self.add_parameter('route_BNC_output_select')
		#self.add_parameter('route_BNC_output_trigger')
		#self.add_parameter('route_BNC_output_sweep')
		#self.add_parameter('route_BNC_output_control')
		#self.add_parameter('route_DIO_5')
		#self.add_parameter('route_DIO_6')
		#self.add_parameter('route_DIO_7')
		#self.add_parameter('route_DIO_8')
		
		# system parameters
		#self.add_parameter('system_display')
		#self.add_parameter('system_display_brightness')
		#self.add_parameter('system_clock_date')
		#self.add_parameter('system_clock_time')
		#self.add_parameter('system_clock_timezone')
		#self.add_parameter('system_setup_catalog', flags=Instrument.FLAG_GET)
		#self.add_parameter('system_setup_power_on')
		#self.add_parameter('system_error', flags=Instrument.FLAG_GET)
		#self.add_parameter('system_lock')
		#self.add_parameter('system_beeper')
		#self.add_parameter('system_LF_frequency')
		#self.add_parameter('system_communicate_GPIB_address')
		#self.add_parameter('system_communicate_RS232_baud_rate')
		#self.add_parameter('system_communicate_RS232_data_length')
		#self.add_parameter('system_communicate_RS232_parity')
		#self.add_parameter('system_communicate_RS232_stop_bits')
		#self.add_parameter('system_communicate_RS232_pace')
		#self.add_parameter('system_communicate_RS232_terminator')
		#self.add_parameter('system_communicate_ethernet_MAC', flags=Instrument.FLAG_GET)
		#self.add_parameter('system_communicate_ethernet_port', flags=Instrument.FLAG_GET)
		#self.add_parameter('system_communicate_ethernet_DHCP')
		#self.add_parameter('system_communicate_ethernet_IP')
		#self.add_parameter('system_communicate_ethernet_mask')
		#self.add_parameter('system_communicate_ethernet_default_gateway')
		#self.add_parameter('system_communicate_ehternet_terminator', flags=Instrument.FLAG_GET)
		
		# status parameters
		#self.add_parameter('status_source_condition', flags=Instrument.FLAG_GET)
		#self.add_parameter('status_source_event', flags=Instrument.FLAG_GET)
		#self.add_parameter('status_source_enable')
		#self.add_parameter('status_sense_condition', flags=Instrument.FLAG_GET)
		#self.add_parameter('status_sense_event', flags=Instrument.FLAG_GET)
		#self.add_parameter('status_sense_enable')
		
		# common parameters
		self.add_parameter('save', type=int, flags=Instrument.FLAG_SET, minval=1, maxval=4)
		self.add_parameter('recall', type=int, flags=Instrument.FLAG_SET, minval=1, maxval=4)
		self.add_parameter('service_request_enable_register', type=int, flags=Instrument.FLAG_GETSET, minval=0, maxval=255)
		self.add_parameter('standard_event_enable_register', type=int, flags=Instrument.FLAG_GETSET, minval=0, maxval=255)
		
		# source functions
		#self.add_function('source_list_delete')
		#self.add_function('source_list_define')
		self.add_function('source_voltage_range_increment')
		self.add_function('source_voltage_range_decrement')
		self.add_function('source_current_range_increment')
		self.add_function('source_current_range_decrement')
		
		# sweep functions
		self.add_function('sweep_trigger')
		
		# measurement functions
		self.add_function('sense_auto_zero_execute')
		self.add_function('sense_integration_time_plc')
		self.add_function('sense_integration_time_increment')
		self.add_function('sense_integration_time_decrement')
		
		# computation functions
		self.add_function('calculate_math_delete')
		self.add_function('calculate_math_define')
		
		# store/recall functions
		#self.add_function('trace_data_number_increment')
		#self.add_function('trace_data_number_decrement')
		
		# system functions
		#self.add_function('system_setup_save')
		#self.add_function('system_setup_load')
		#self.add_function('system_setup_delete')
		#self.add_function('system_remote')
		#self.add_function('system_local')
		self.add_function('system_wait')
		
		# measured value read functions
		self.add_function('initiate')
		self.add_function('fetch')
		self.add_function('read')
		
		# common functions
		self.add_function('identify')
		self.add_function('options')
		self.add_function('trigger')
		self.add_function('calibrate')
		self.add_function('test')
		self.add_function('reset')
		self.add_function('clear')
		self.add_function('status_byte')
		self.add_function('standard_event_register')
		self.add_function('generate_operation_complete')
		self.add_function('test_operation_complete')
		self.add_function('wait')
		
		if reset:
			self.reset()
	
	def do_get_output(self):
		"""
		Queries the current output state (ON, OFF, or zero).
		
		Input:
			None
		
		Output:
			state (int) : output state
		"""
		map = self.get_parameters()['output']['format_map']
		return list(map.keys())[list(map.values()).index(self._visainstrument.query(':OUTP?').replace('\n', ''))]
	
	def do_set_output(self, state):
		"""
		Sets the output state (ON, OFF, or zero).
		
		Input:
			state (int) : output state
		
		Output:
			None
		"""
		self._visainstrument.write(':OUTP %s' % self.get_parameters()['output']['format_map'][state])
		
	def do_get_output_program(self):
		"""
		Queries the programmable output state (ON or OFF).
		
		Input:
			None
		
		Output:
			state (int) : programmable output state
		"""
		map = self.get_parameters()['output_program']['format_map']
		return list(map.keys())[list(map.values()).index(self._visainstrument.query(':OUTP:PROG?').replace('\n', ''))]
	
	def do_set_output_program(self, state):
		"""
		Sets the programmable output state (ON or OFF) or carries out pulse generation.
		
		Input:
			state (int) : programmable output state
		
		Output:
			None
		"""
		self._visainstrument.write(':OUTP:PROG %s' % self.get_parameters()['output_program']['format_map'][state])
	
	def do_get_source_function(self):
		"""
		Queries the current source function (voltage or current).
		
		Input:
			None
		
		Output:
			function (int) : source function
		"""
		map = self.get_parameters()['source_function']['format_map']
		return list(map.keys())[list(map.values()).index(self._visainstrument.query(':SOUR:FUNC?').replace('\n', ''))]
	
	def do_set_source_function(self, function):
		"""
		Sets the source function (voltage or current).
		
		Input:
			function (int) : source function
		
		Output:
			None
		"""
		self._visainstrument.write(':SOUR:FUNC %s' % self.get_parameters()['source_function']['format_map'][function])
	
	
	def do_get_source_shape(self):
		"""
		Queries the current source mode (DC or pulse).
		
		Input:
			None
		
		Output:
			shape (int) : source mode
		"""
		map = self.get_parameters()['source_shape']['format_map']
		return list(map.keys())[list(map.values()).index(self._visainstrument.query(':SOUR:SHAP?').replace('\n', ''))]
	
	def do_set_source_shape(self, shape):
		"""
		Sets the source mode (DC or pulse).
		
		Input:
			shape (int) : source mode
		
		Output:
			None
		"""
		self._visainstrument.write(':SOUR:SHAP %s' % self.get_parameters()['source_shape']['format_map'][shape])
	
	def do_get_source_mode(self):
		"""
		Queries the current source pattern (fixed level, sweep, or program sweep).
		
		Input:
			None
		
		Output:
			mode (int) : source pattern
		"""
		map = self.get_parameters()['source_mode']['format_map']
		return list(map.keys())[list(map.values()).index(self._visainstrument.query(':SOUR:MODE?').replace('\n', ''))]
		
	def do_set_source_mode(self, mode):
		"""
		Sets the source pattern (fixed level, sweep, or program sweep).
		
		Input:
			mode (int) : source pattern
		
		Output:
			None
		"""
		self._visainstrument.write(':SOUR:MODE %s' % self.get_parameters()['source_mode']['format_map'][mode])
	
	
	def do_get_source_delay_minimum(self):
		"""
		Queries the minimum source delay.
		
		Input:
			None
		
		Output:
			delay (float) : minimum source delay in seconds
		"""
		return self._visainstrument.query(':SOUR:DEL? MIN').replace('\n', '')
		
	def do_get_source_delay_maximum(self):
		"""
		Queries the maximum source delay.
		
		Input:
			None
		
		Output:
			delay (float) : maximum source delay in seconds
		"""
		return self._visainstrument.query(':SOUR:DEL? MAX').replace('\n', '')
		
	def do_get_source_delay(self):
		"""
		Queries the current source delay.
		
		Input:
			None
		
		Output:
			delay (float) : source delay in seconds
		"""
		return self._visainstrument.query(':SOUR:DEL?').replace('\n', '')
	
	def do_set_source_delay(self, delay):
		"""
		Sets the source delay.
		
		Input:
			delay (float) : source delay in seconds
		
		Output:
			None
		"""
		self._visainstrument.write(':SOUR:DEL %e' % delay)
	
	
	def do_get_source_pulse_width_minimum(self):
		"""
		Queries the minimum source pulse width.
		
		Input:
			None
		
		Output:
			width (float) : minimum source pulse width in seconds
		"""
		return self._visainstrument.query(':SOUR:PULS:WIDT? MIN').replace('\n', '')
	
	def do_get_source_pulse_width_maximum(self):
		"""
		Queries the maximum source pulse width.
		
		Input:
			None
		
		Output:
			width (float) : maximum source pulse width in seconds
		"""
		return self._visainstrument.query(':SOUR:PULS:WIDT? MAX').replace('\n', '')
	
	def do_get_source_pulse_width(self):
		"""
		Queries the current source pulse width.
		
		Input:
			None
		
		Output:
			width (float) : source pulse width in seconds
		"""
		return self._visainstrument.query(':SOUR:PULS:WIDT?').replace('\n', '')
	
	def do_set_source_pulse_width(self, width):
		"""
		Sets the source pulse width.
		
		Input:
			width (float) : source pulse width in seconds
		
		Output:
			None
		"""
		self._visainstrument.write(':SOUR:PULS:WIDT %e' % width)
	
	def do_get_source_list_select(self):
		"""
		Queries the current program sweep pattern file.
		
		Input:
			None
		
		Output:
			file (str) : pattern file name
		"""
		return self._visainstrument.query(':SOUR:LIST:SEL?').replace('\n', '')
	
	def do_set_source_list_select(self, file):
		"""
		Sets the program sweep pattern file.
		
		Input:
			file (str) : pattern file name
		
		Output:
			None
		"""
		self._visainstrument.write(':SOUR:LIST:SEL %s' % file)
	
	# probably doesn't work
	def do_get_source_list_catalog(self):
		"""
		Queries the list of program sweep pattern files.
		
		Input:
			None
		
		Output:
			files (list) : pattern file names
		"""
		return self._visainstrument.query(':SOUR:LIST:CAT?')
	
	def do_get_source_voltage_range_minimum(self):
		"""
		Queries the minimum voltage source range.
		
		Input:
			None
		
		Output:
			voltage_range (float) : minimum voltage source range in volts
		"""
		return self._visainstrument.query(':SOUR:VOLT:RANG? MIN').replace('\n', '')
	
	def do_get_source_voltage_range_maximum(self):
		"""
		Queries the maximum voltage source range.
		
		Input:
			None
		
		Output:
			voltage_range (float) : maximum voltage source range in volts
		"""
		return self._visainstrument.query(':SOUR:VOLT:RANG? MAX').replace('\n', '')
	
	def do_get_source_voltage_range(self):
		"""
		Queries the current voltage source range (200 mV, 2 V, 12 V, 20 V, 30 V, 60 V, or 110 V).
		
		Input:
			None
		
		Output:
			voltage_range (float) : voltage source range in volts
		"""
		return self._visainstrument.query(':SOUR:VOLT:RANG?').replace('\n', '')
	
	def do_set_source_voltage_range(self, voltage_range):
		"""
		Sets the voltage source range to the smallest range that includes the argument (200 mV, 2 V, 12 V, 20 V, 30 V, 60 V, or 110 V).
		
		Input:
			voltage_range (float) : voltage source range in volts
		
		Output:
			None
		"""
		self._visainstrument.write(':SOUR:VOLT:RANG %e' % voltage_range)
	
	def do_get_source_voltage_level_minimum(self):
		"""
		Queries the minimum voltage source level.
		
		Input:
			None
		
		Output:
			level (float) : minimum voltage source level in volts
		"""
		return self._visainstrument.query(':SOUR:VOLT:LEV? MIN').replace('\n', '')
	
	def do_get_source_voltage_level_maximum(self):
		"""
		Queries the maximum voltage source level.
		
		Input:
			None
		
		Output:
			level (float) : maximum voltage source level in volts
		"""
		return self._visainstrument.query(':SOUR:VOLT:LEV? MAX').replace('\n', '')
	
	def do_get_source_voltage_level(self):
		"""
		Queries the current voltage source level.
		
		Input:
			None
		
		Output:
			level (float) : voltage source level in volts
		"""
		return self._visainstrument.query(':SOUR:VOLT:LEV?').replace('\n', '')
	
	def do_set_source_voltage_level(self, level):
		"""
		Sets the voltage source level.
		
		Input:
			level (float) : voltage source level in volts
		
		Output:
			None
		"""
		self._visainstrument.write(':SOUR:VOLT:LEV %e' % level)
	
	def do_get_source_voltage_pulse_base_minimum(self):
		"""
		Queries the minimum voltage source pulse base value.
		
		Input:
			None
		
		Output:
			pulse_base (float) : minimum voltage source pulse base in volts
		"""
		return self._visainstrument.query(':SOUR:VOLT:PBAS? MIN').replace('\n', '')
	
	def do_get_source_voltage_pulse_base_maximum(self):
		"""
		Queries the maximum voltage source pulse base value.
		
		Input:
			None
		
		Output:
			pulse_base (float) : maximum voltage source pulse base in volts
		"""
		return self._visainstrument.query(':SOUR:VOLT:PBAS? MAX').replace('\n', '')
	
	def do_get_source_voltage_pulse_base(self):
		"""
		Queries the current voltage source pulse base value.
		
		Input:
			None
		
		Output:
			pulse_base (float) : voltage source pulse base in volts
		"""
		return self._visainstrument.query(':SOUR:VOLT:PBAS?').replace('\n', '')
	
	def do_set_source_voltage_pulse_base(self, pulse_base):
		"""
		Sets the voltage source pulse base value.
		
		Input:
			pulse_base (float) : voltage source pulse base in volts
		
		Output:
			None
		"""
		self._visainstrument.write(':SOUR:VOLT:PBAS %e' % pulse_base)
	
	def do_get_source_voltage_protection_upper_limit_minimum(self):
		"""
		Queries the minimum source upper voltage limiter value.
		
		Input:
			None
		
		Output:
			limit (float) : minimum source upper voltage limiter value
		"""
		return self._visainstrument.query(':SOUR:VOLT:PROT:ULIM? MIN').replace('\n', '')
	
	def do_get_source_voltage_protection_upper_limit_maximum(self):
		"""
		Queries the maximum source upper voltage limiter value.
		
		Input:
			None
		
		Output:
			limit (float) : maximum source upper voltage limiter value
		"""
		return self._visainstrument.query(':SOUR:VOLT:PROT:ULIM? MAX').replace('\n', '')
	
	def do_get_source_voltage_protection_upper_limit(self):
		"""
		Queries the current source upper voltage limiter value.
		
		Input:
			None
		
		Output:
			limit (float) : source upper voltage limiter value
		"""
		return self._visainstrument.query(':SOUR:VOLT:PROT:ULIM?').replace('\n', '')
	
	def do_set_source_voltage_protection_upper_limit(self, limit):
		"""
		Sets the source upper voltage limiter value.
		
		Input:
			limit (float) : source upper voltage limiter value
		
		Output:
			None
		"""
		self._visainstrument.write(':SOUR:VOLT:PROT:ULIM %e' % limit)
	
	def do_get_source_voltage_protection_lower_limit_minimum(self):
		"""
		Queries the minimum source lower voltage limiter value.
		
		Input:
			None
		
		Output:
			limit (float) : minimum source lower voltage limiter value
		"""
		return self._visainstrument.query(':SOUR:VOLT:PROT:LLIM? MIN').replace('\n', '')
	
	def do_get_source_voltage_protection_lower_limit_maximum(self):
		"""
		Queries the maximum source lower voltage limiter value.
		
		Input:
			None
		
		Output:
			limit (float) : minimum source lower voltage limiter value
		"""
		return self._visainstrument.query(':SOUR:VOLT:PROT:LLIM? MAX').replace('\n', '')
	
	def do_get_source_voltage_protection_lower_limit(self):
		"""
		Queries the current source lower voltage limiter value.
		
		Input:
			None
		
		Output:
			limit (float) : source lower voltage limiter value
		"""
		return self._visainstrument.query(':SOUR:VOLT:PROT:LLIM?').replace('\n', '')
	
	def do_set_source_voltage_protection_lower_limit(self, limit):
		"""
		Sets the source lower voltage limiter value.
		
		Input:
			limit (float) : source lower voltage limiter value
		
		Output:
			None
		"""
		self._visainstrument.write(':SOUR:VOLT:PROT:LLIM %e' % limit)
	
	def do_get_source_voltage_sweep_start_minimum(self):
		"""
		Queries the minimum start value of the voltage sweep.
		
		Input:
			None
		
		Output:
			start (float) : minimum start value of the voltage sweep
		"""
		return self._visainstrument.query(':SOUR:VOLT:SWE:STAR? MIN').replace('\n', '')
	
	def do_get_source_voltage_sweep_start_maximum(self):
		"""
		Queries the maximum start value of the voltage sweep.
		
		Input:
			None
		
		Output:
			start (float) : maximum start value of the voltage sweep
		"""
		return self._visainstrument.query(':SOUR:VOLT:SWE:STAR? MAX').replace('\n', '')
	
	def do_get_source_voltage_sweep_start(self):
		"""
		Queries the current start value of the voltage sweep.
		
		Input:
			None
		
		Output:
			start (float) : start value of voltage sweep
		"""
		return self._visainstrument.query(':SOUR:VOLT:SWE:STAR?').replace('\n', '')
	
	def do_set_source_voltage_sweep_start(self, start):
		"""
		Sets the start value of the voltage sweep.
		
		Input:
			start (float) : start value of the voltage sweep
		
		Output:
			None
		"""
		self._visainstrument.write(':SOUR:VOLT:SWE:STAR %e' % start)
	
	def do_get_source_voltage_sweep_stop_minimum(self):
		"""
		Queries the minimum stop value of the voltage sweep.
		
		Input:
			None
		
		Output:
			stop (float) : minimum stop value of voltage sweep
		"""
		return self._visainstrument.query(':SOUR:VOLT:SWE:STOP? MIN').replace('\n', '')
	
	def do_get_source_voltage_sweep_stop_maximum(self):
		"""
		Queries the maximum stop value of the voltage sweep.
		
		Input:
			None
		
		Output:
			stop (float) : maximum stop value of voltage sweep
		"""
		return self._visainstrument.query(':SOUR:VOLT:SWE:STOP? MAX').replace('\n', '')
	
	def do_get_source_voltage_sweep_stop(self):
		"""
		Queries the current stop value of the voltage sweep.
		
		Input:
			None
		
		Output:
			stop (float) : stop value of voltage sweep
		"""
		return self._visainstrument.query(':SOUR:VOLT:SWE:STOP?').replace('\n', '')
	
	def do_set_source_voltage_sweep_stop(self, stop):
		"""
		Sets the stop value of the voltage sweep.
		
		Input:
			stop (float) : stop value of voltage sweep
		
		Output:
			None
		"""
		self._visainstrument.write(':SOUR:VOLT:SWE:STOP %e' % stop)
	
	def do_get_source_voltage_sweep_step_minimum(self):
		"""
		Queries the minimum step value of the linear voltage sweep.
		
		Input:
			None
		
		Output:
			step (float) : minimum step value of linear voltage sweep
		"""
		return self._visainstrument.query(':SOUR:VOLT:SWE:STEP? MIN').replace('\n', '')
	
	def do_get_source_voltage_sweep_step_maximum(self):
		"""
		Queries the maximum step value of the linear voltage sweep.
		
		Input:
			None
		
		Output:
			step (float) : maximum step value of linear voltage sweep
		"""
		return self._visainstrument.query(':SOUR:VOLT:SWE:STEP? MAX').replace('\n', '')
	
	def do_get_source_voltage_sweep_step(self):
		"""
		Queries the current step value of the linear voltage sweep.
		
		Input:
			None
		
		Output:
			step (float) : step value of the linear voltage sweep
		"""
		return self._visainstrument.query(':SOUR:VOLT:SWE:STEP?').replace('\n', '')
	
	def do_set_source_voltage_sweep_step(self, step):
		"""
		Sets the step value of the linear voltage sweep.
		
		Input:
			step (float) : step value of the linear voltage sweep
		
		Output:
			None
		"""
		self._visainstrument.write(':SOUR:VOLT:SWE:STEP %e' % step)
	
	def do_get_source_voltage_sweep_points_minimum(self):
		"""
		Queries the minimum step count of the logarithmic voltage sweep.
		
		Input:
			None
		
		Output:
			points (int) : minimum step count of logarithmic voltage sweep
		"""
		return self._visainstrument.query(':SOUR:VOLT:SWE:POIN? MIN').replace('\n', '')
	
	def do_get_source_voltage_sweep_points_maximum(self):
		"""
		Queries the maximum step count of the logarithmic voltage sweep.
		
		Input:
			None
		
		Output:
			points (int) : maximum step count of logarithmic voltage sweep
		"""
		return self._visainstrument.query(':SOUR:VOLT:SWE:POIN? MAX').replace('\n', '')
	
	def do_get_source_voltage_sweep_points(self):
		"""
		Queries the current step count of the logarithmic voltage sweep.
		
		Input:
			None
		
		Output:
			points (int) : step count of logarithmic voltage sweep
		"""
		return self._visainstrument.query(':SOUR:VOLT:SWE:POIN?').replace('\n', '')
	
	def do_set_source_voltage_sweep_points(self, points):
		"""
		Sets the step count of the logarithmic voltage sweep.
		
		Input:
			points (int) : step count of logarithmic voltage sweep
		
		Output:
			None
		"""
		self._visainstrument.write(':SOUR:VOLT:SWE:POIN %i' % points)
	
	def do_get_source_voltage_zero_impedance(self):
		"""
		Queries the current zero source impedance for generating voltage (LOW or HIGH).
		
		Input:
			None
		
		Output:
			impedance (int) : zero source impedance for generating voltage
		"""
		map = self.get_parameters()['source_voltage_zero_impedance']['format_map']
		return list(map.keys())[list(map.values()).index(self._visainstrument.query(':SOUR:VOLT:ZERO:IMP?').replace('\n', ''))]
	
	def do_set_source_voltage_zero_impedance(self, impedance):
		"""
		Sets the zero source impedance for generating voltage (LOW or HIGH).
		
		Input:
			impedance (int) : zero source impedance for generating voltage
		
		Output:
			None
		"""
		self._visainstrument.write(':SOUR:VOLT:ZERO:IMP %s' % self.get_parameters()['output']['format_map'][impedance])
	
	def do_get_source_voltage_zero_offset(self):
		"""
		Queries the current zero source offset for generating voltage.
		
		Input:
			None
		
		Output:
			offset (float) : zero source offset for generating voltage
		"""
		return self._visainstrument.query(':SOUR:VOLT:ZERO:OFFS?').replace('\n', '')
	
	def do_set_source_voltage_zero_offset(self, offset):
		"""
		Sets the zero source offset for generating voltage.
		
		Input:
			offset (float) : zero source offset for generating voltage
		
		Output:
			None
		"""
		self._visainstrument.write(':SOUR:VOLT:ZERO:OFFS %e' % offset)
	
	def do_get_source_current_range_minimum(self):
		"""
		Queries the minimum current source range.
		
		Input:
			None
		
		Output:
			current_range (float) : minimum current source range in amperes
		"""
		return self._visainstrument.query(':SOUR:CURR:RANG? MIN').replace('\n', '')
	
	def do_get_source_current_range_maximum(self):
		"""
		Queries the maximum current source range.
		
		Input:
			None
		
		Output:
			current_range (float) : maximum current source range in amperes
		"""
		return self._visainstrument.query(':SOUR:CURR:RANG? MAX').replace('\n', '')
	
	def do_get_source_current_range(self):
		"""
		Queries the current current source range (20 μA, 200 μA, 2 mA, 20 mA, 200 mA, 0.5 A, 1 A, 2 A, or 3 A).
		
		Input:
			None
		
		Output:
			current_range (float) : current source range in amperes
		"""
		return self._visainstrument.query(':SOUR:CURR:RANG?').replace('\n', '')
	
	def do_set_source_current_range(self, current_range):
		"""
		Sets the current source range to the smallest range that includes the argument (20 μA, 200 μA, 2 mA, 20 mA, 200 mA, 0.5 A, 1 A, 2 A, or 3 A).
		
		Input:
			current_range (float) : current source range in amperes
		
		Output:
			None
		"""
		self._visainstrument.write(':SOUR:CURR:RANG %e' % current_range)
	
	def do_get_source_current_level_minimum(self):
		"""
		Queries the minimum current source level.
		
		Input:
			None
		
		Output:
			level (float) : minimum current source level in amperes
		"""
		return self._visainstrument.query(':SOUR:CURR:LEV? MIN').replace('\n', '')
	
	def do_get_source_current_level_maximum(self):
		"""
		Queries the maximum current source level.
		
		Input:
			None
		
		Output:
			level (float) : maximum current source level in amperes
		"""
		return self._visainstrument.query(':SOUR:CURR:LEV? MAX').replace('\n', '')
	
	def do_get_source_current_level(self):
		"""
		Queries the current current source level.
		
		Input:
			None
		
		Output:
			level (float) : current source level in amperes
		"""
		return self._visainstrument.query(':SOUR:CURR:LEV?').replace('\n', '')
	
	def do_set_source_current_level(self, level):
		"""
		Sets the current source level.
		
		Input:
			level (float) : current source level in amperes
		
		Output:
			None
		"""
		self._visainstrument.write(':SOUR:CURR:LEV %e' % level)
	
	def do_get_source_current_pulse_base_minimum(self):
		"""
		Queries the minimum current source pulse base value.
		
		Input:
			None
		
		Output:
			pulse_base (float) : minimum current source pulse base in amperes
		"""
		return self._visainstrument.query(':SOUR:CURR:PBAS? MIN').replace('\n', '')
	
	def do_get_source_current_pulse_base_maximum(self):
		"""
		Queries the maximum current source pulse base value.
		
		Input:
			None
		
		Output:
			pulse_base (float) : maximum current source pulse base in amperes
		"""
		return self._visainstrument.query(':SOUR:CURR:PBAS? MAX').replace('\n', '')
	
	def do_get_source_current_pulse_base(self):
		"""
		Queries the current current source pulse base value.
		
		Input:
			None
		
		Output:
			pulse_base (float) : current source pulse base in amperes
		"""
		return self._visainstrument.query(':SOUR:CURR:PBAS?').replace('\n', '')
	
	def do_set_source_current_pulse_base(self, pulse_base):
		"""
		Sets the current source pulse base value.
		
		Input:
			pulse_base (float) : current source pulse base in amperes
		
		Output:
			None
		"""
		self._visainstrument.write(':SOUR:CURR:PBAS %e' % pulse_base)
	
	def do_get_source_current_protection_upper_limit_minimum(self):
		"""
		Queries the minimum source upper current limiter value.
		
		Input:
			None
		
		Output:
			limit (float) : minimum source upper current limiter value
		"""
		return self._visainstrument.query(':SOUR:CURR:PROT:ULIM? MIN').replace('\n', '')
	
	def do_get_source_current_protection_upper_limit_maximum(self):
		"""
		Queries the maximum source upper current limiter value.
		
		Input:
			None
		
		Output:
			limit (float) : maximum source upper current limiter value
		"""
		return self._visainstrument.query(':SOUR:CURR:PROT:ULIM? MAX').replace('\n', '')
	
	def do_get_source_current_protection_upper_limit(self):
		"""
		Queries the current source upper current limiter value.
		
		Input:
			None
		
		Output:
			limit (float) : source upper current limiter value
		"""
		return self._visainstrument.query(':SOUR:CURR:PROT:ULIM?').replace('\n', '')
	
	def do_set_source_current_protection_upper_limit(self, limit):
		"""
		Sets the source upper current limiter value.
		
		Input:
			limit (float) : source upper current limiter value
		
		Output:
			None
		"""
		self._visainstrument.write(':SOUR:CURR:PROT:ULIM %e' % limit)
	
	def do_get_source_current_protection_lower_limit_minimum(self):
		"""
		Queries the minimum source lower current limiter value.
		
		Input:
			None
		
		Output:
			limit (float) : minimum source lower current limiter value
		"""
		return self._visainstrument.query(':SOUR:CURR:PROT:LLIM? MIN').replace('\n', '')
	
	def do_get_source_current_protection_lower_limit_maximum(self):
		"""
		Queries the maximum source lower current limiter value.
		
		Input:
			None
		
		Output:
			limit (float) : minimum source lower current limiter value
		"""
		return self._visainstrument.query(':SOUR:CURR:PROT:LLIM? MAX').replace('\n', '')
	
	def do_get_source_current_protection_lower_limit(self):
		"""
		Queries the current source lower current limiter value.
		
		Input:
			None
		
		Output:
			limit (float) : source lower current limiter value
		"""
		return self._visainstrument.query(':SOUR:CURR:PROT:LLIM?').replace('\n', '')
	
	def do_set_source_current_protection_lower_limit(self, limit):
		"""
		Sets the source lower current limiter value.
		
		Input:
			limit (float) : source lower current limiter value
		
		Output:
			None
		"""
		self._visainstrument.write(':SOUR:CURR:PROT:LLIM %e' % limit)
	
	def do_get_source_current_sweep_start_minimum(self):
		"""
		Queries the minimum start value of the current sweep.
		
		Input:
			None
		
		Output:
			start (float) : minimum start value of the current sweep
		"""
		return self._visainstrument.query(':SOUR:CURR:SWE:STAR? MIN').replace('\n', '')
	
	def do_get_source_current_sweep_start_maximum(self):
		"""
		Queries the maximum start value of the current sweep.
		
		Input:
			None
		
		Output:
			start (float) : maximum start value of the current sweep
		"""
		return self._visainstrument.query(':SOUR:CURR:SWE:STAR? MAX').replace('\n', '')
	
	def do_get_source_current_sweep_start(self):
		"""
		Queries the current start value of the current sweep.
		
		Input:
			None
		
		Output:
			start (float) : start value of current sweep
		"""
		return self._visainstrument.query(':SOUR:CURR:SWE:STAR?').replace('\n', '')
	
	def do_set_source_current_sweep_start(self, start):
		"""
		Sets the start value of the current sweep.
		
		Input:
			start (float) : start value of the current sweep
		
		Output:
			None
		"""
		self._visainstrument.write(':SOUR:CURR:SWE:STAR %e' % start)
	
	def do_get_source_current_sweep_stop_minimum(self):
		"""
		Queries the minimum stop value of the current sweep.
		
		Input:
			None
		
		Output:
			stop (float) : minimum stop value of current sweep
		"""
		return self._visainstrument.query(':SOUR:CURR:SWE:STOP? MIN').replace('\n', '')
	
	def do_get_source_current_sweep_stop_maximum(self):
		"""
		Queries the maximum stop value of the current sweep.
		
		Input:
			None
		
		Output:
			stop (float) : maximum stop value of current sweep
		"""
		return self._visainstrument.query(':SOUR:CURR:SWE:STOP? MAX').replace('\n', '')
	
	def do_get_source_current_sweep_stop(self):
		"""
		Queries the current stop value of the current sweep.
		
		Input:
			None
		
		Output:
			stop (float) : stop value of current sweep
		"""
		return self._visainstrument.query(':SOUR:CURR:SWE:STOP?').replace('\n', '')
	
	def do_set_source_current_sweep_stop(self, stop):
		"""
		Sets the stop value of the current sweep.
		
		Input:
			stop (float) : stop value of current sweep
		
		Output:
			None
		"""
		self._visainstrument.write(':SOUR:CURR:SWE:STOP %e' % stop)
	
	def do_get_source_current_sweep_step_minimum(self):
		"""
		Queries the minimum step value of the linear current sweep.
		
		Input:
			None
		
		Output:
			step (float) : minimum step value of linear current sweep
		"""
		return self._visainstrument.query(':SOUR:CURR:SWE:STEP? MIN').replace('\n', '')
	
	def do_get_source_current_sweep_step_maximum(self):
		"""
		Queries the maximum step value of the linear current sweep.
		
		Input:
			None
		
		Output:
			step (float) : maximum step value of linear current sweep
		"""
		return self._visainstrument.query(':SOUR:CURR:SWE:STEP? MAX').replace('\n', '')
	
	def do_get_source_current_sweep_step(self):
		"""
		Queries the current step value of the linear current sweep.
		
		Input:
			None
		
		Output:
			step (float) : step value of the linear current sweep
		"""
		return self._visainstrument.query(':SOUR:CURR:SWE:STEP?').replace('\n', '')
	
	def do_set_source_current_sweep_step(self, step):
		"""
		Sets the step value of the linear current sweep.
		
		Input:
			step (float) : step value of the linear current sweep
		
		Output:
			None
		"""
		self._visainstrument.write(':SOUR:CURR:SWE:STEP %e' % step)
	
	def do_get_source_current_sweep_points_minimum(self):
		"""
		Queries the minimum step count of the logarithmic current sweep.
		
		Input:
			None
		
		Output:
			points (int) : minimum step count of logarithmic current sweep
		"""
		return self._visainstrument.query(':SOUR:CURR:SWE:POIN? MIN').replace('\n', '')
	
	def do_get_source_current_sweep_points_maximum(self):
		"""
		Queries the maximum step count of the logarithmic current sweep.
		
		Input:
			None
		
		Output:
			points (int) : maximum step count of logarithmic current sweep
		"""
		return self._visainstrument.query(':SOUR:CURR:SWE:POIN? MAX').replace('\n', '')
	
	def do_get_source_current_sweep_points(self):
		"""
		Queries the current step count of the logarithmic current sweep.
		
		Input:
			None
		
		Output:
			points (int) : step count of logarithmic current sweep
		"""
		return self._visainstrument.query(':SOUR:CURR:SWE:POIN?').replace('\n', '')
	
	def do_set_source_current_sweep_points(self, points):
		"""
		Sets the step count of the logarithmic current sweep.
		
		Input:
			points (int) : step count of logarithmic current sweep
		
		Output:
			None
		"""
		self._visainstrument.write(':SOUR:CURR:SWE:POIN %i' % points)
	
	def do_get_source_current_zero_impedance(self):
		"""
		Queries the current zero source impedance for generating current (LOW or HIGH).
		
		Input:
			None
		
		Output:
			impedance (int) : zero source impedance for generating current
		"""
		map = self.get_parameters()['source_current_zero_impedance']['format_map']
		return list(map.keys())[list(map.values()).index(self._visainstrument.query(':SOUR:CURR:ZERO:IMP?').replace('\n', ''))]
	
	def do_set_source_current_zero_impedance(self, impedance):
		"""
		Sets the zero source impedance for generating current (LOW or HIGH).
		
		Input:
			impedance (int) : zero source impedance for generating current
		
		Output:
			None
		"""
		self._visainstrument.write(':SOUR:CURR:ZERO:IMP %s' % self.get_parameters()['output']['format_map'][impedance])
	
	def do_get_source_current_zero_offset(self):
		"""
		Queries the current zero source offset for generating current.
		
		Input:
			None
		
		Output:
			offset (float) : zero source offset for generating current
		"""
		return self._visainstrument.query(':SOUR:CURR:ZERO:OFFS?').replace('\n', '')
	
	def do_set_source_current_zero_offset(self, offset):
		"""
		Sets the zero source offset for generating current.
		
		Input:
			offset (float) : zero source offset for generating current
		
		Output:
			None
		"""
		self._visainstrument.write(':SOUR:CURR:ZERO:OFFS %e' % offset)
	
	def do_get_source_range_auto(self):
		"""
		Queries the current source autorange setting.
		
		Input:
			None
		
		Output:
			auto (int) : source autorange
		"""
		return self._visainstrument.query(':SOUR:VOLT:RANG:AUTO?').replace('\n', '')
	
	def do_set_source_range_auto(self, auto):
		"""
		Sets the source autorange setting.
		
		Intput:
			auto (int) : source autorange
		
		Output:
			None
		"""
		self._visainstrument.write(':SOUR:VOLT:RANG:AUTO %i' % auto)
	
	def do_get_source_protection(self):
		"""
		Queries the current source limiter state (ON or OFF).
		
		Input:
			None
		
		Output:
			state (int) : source limiter state
		"""
		return self._visainstrument.query(':SOUR:VOLT:PROT?').replace('\n', '')
	
	def do_set_source_protection(self, state):
		"""
		Sets the source limiter state (ON or OFF).
		
		Input:
			state (int) : source limiter state
		
		Output:
			None
		"""
		self._visainstrument.write(':SOUR:VOLT:PROT %i' % state)
	
	def do_get_source_protection_linkage(self):
		"""
		Queries the current source limiter tracking state (ON or OFF).
		
		Input:
			None
		
		Output:
			state (int) : source limiter tracking state
		"""
		return self._visainstrument.query(':SOUR:VOLT:PROT:LINK?').replace('\n', '')
	
	def do_set_source_protection_linkage(self, state):
		"""
		Sets the source limiter tracking state (ON or OFF).
		
		Input:
			state (int) : source limiter tracking state
		
		Output:
			None
		"""
		self._visainstrument.write(':SOUR:VOLT:PROT:LINK %i' % state)
	
	def do_get_source_sweep_spacing(self):
		"""
		Queries the current sweep mode (linear or log).
		
		Input:
			None
		
		Output:
			spacing (int) : sweep mode
		"""
		map = self.get_parameters()['source_sweep_spacing']['format_map']
		return list(map.keys())[list(map.values()).index(self._visainstrument.query(':SOUR:VOLT:SWE:SPAC?').replace('\n', ''))]
	
	def do_set_source_sweep_spacing(self, spacing):
		"""
		Sets the sweep mode (linear or log).
		
		Input:
			spacing (int) : sweep mode
		
		Output:
			None
		"""
		self._visainstrument.write(':SOUR:VOLT:SWE:SPAC %s' % self.get_parameters()['source_sweep_spacing']['format_map'][spacing])
	
	def do_get_sweep_count_minimum(self):
		"""
		Queries the minimum sweep repeat count.
		
		Input:
			None
		
		Output:
			count (int) : minimum sweep repeat count
		"""
		return self._visainstrument.query(':SWE:COUN? MIN').replace('\n', '')
	
	def do_get_sweep_count_maximum(self):
		"""
		Queries the maximum sweep repeat count.
		
		Input:
			None
		
		Output:
			count (int) : maximum sweep repeat count
		"""
		return self._visainstrument.query(':SWE:COUN? MAX').replace('\n', '')
	
	def do_get_sweep_count(self):
		"""
		Queries the current sweep repeat count (a count of 0 corresponds to infinity).
		
		Input:
			None
		
		Output:
			count (int) : sweep repeat count
		"""
		count = self._visainstrument.query(':SWE:COUN?').replace('\n', '')
		return count if count != 'INF' else 0
	
	def do_set_sweep_count(self, count):
		"""
		Sets the sweep repeat count (a count of 0 corresponds to infinity).
		
		Input:
			count (int) : sweep repeat count
		
		Output:
			None
		"""
		if count != 0:
			self._visainstrument.write(':SWE:COUN %i' % count)
		else:
			self._visainstrument.write(':SWE:COUN INF')
	
	def do_get_sweep_last(self):
		"""
		Queries the current sweep termination mode (keep level or return to initial level).
		
		Input:
			None
		
		Output:
			level (int) : sweep termination mode
		"""
		map = self.get_parameters()['sweep_last']['format_map']
		return list(map.keys())[list(map.values()).index(self._visainstrument.query(':SWE:LAST?').replace('\n', ''))]
	
	def do_set_sweep_last(self, level):
		"""
		Sets the sweep termination mode (keep level or return to initial level).
		
		Input:
			level (int) : sweep termination mode
		
		Output:
			None
		"""
		self._visainstrument.write(':SWE:LAST %s' % self.get_parameters()['sweep_last']['format_map'][level])
	
	def do_get_sense(self):
		"""
		Queries the current measurement state (ON or OFF).
		
		Input:
			None
		
		Output:
			state (int) : measurement state
		"""
		return self._visainstrument.query(':SENS:STAT?').replace('\n', '')
	
	def do_set_sense(self, state):
		"""
		Sets the measurement state (ON or OFF).
		
		Input:
			state (int) : measurement state
		
		Output:
			None
		"""
		self._visainstrument.write(':SENS %s' % state)
	
	def do_get_sense_function(self):
		"""
		Queries the current measurement function (voltage, current, or resistance).
		
		Input:
			None
		
		Output:
			function (int) : measurement function
		"""
		map = self.get_parameters()['sense_function']['format_map']
		return list(map.keys())[list(map.values()).index(self._visainstrument.query(':SENS:FUNC?').replace('\n', ''))]
	
	def do_set_sense_function(self, function):
		"""
		Setst the measurement function (voltage, current, or resistance).
		
		Input:
			function (int) : measurement function
		
		Output:
			None
		"""
		self._visainstrument.write(':SENS:FUNC %s' % self.get_parameters()['sense_function']['format_map'][function])
	
	def do_get_sense_range_auto(self):
		"""
		Queries the current measurement autorange state (ON or OFF).
		
		Input:
			None
		
		Output:
			auto (int) : measurement autorange state
		"""
		return self._visainstrument.query(':SENS:RANG:AUTO?').replace('\n', '')
	
	def do_set_sense_range_auto(self, auto):
		"""
		Sets the measurement autorange state (ON or OFF).
		
		Input:
			auto (int) : measurement autorange state
		
		Output:
			None
		"""
		self._visainstrument.write(':SENS:RANG:AUTO %s' % auto)
	
	def do_get_sense_integration_time_minimum(self):
		"""
		Queries the minimum integration time in seconds.
		
		Input:
			None
		
		Output:
			time (float) : minimum integration time in seconds
		"""
		return self._visainstrument.query(':SENS:ITIM? MIN').replace('\n', '')
	
	def do_get_sense_integration_time_maximum(self):
		"""
		Queries the maximum integration time in seconds.
		
		Input:
			None
		
		Output:
			time (float) : maximum integration time in seconds
		"""
		return self._visainstrument.query(':SENS:ITIM? MAX').replace('\n', '')
	
	def do_get_sense_integration_time(self):
		"""
		Queries the current integration time (250 μs, 1 ms, 4 ms, 16.6 ms or 20 ms, 100 ms, or 200 ms).
		
		Input:
			None
		
		Output:
			time (float) : integration time in seconds
		"""
		return self._visainstrument.query(':SENS:ITIM?').replace('\n', '')
	
	def do_set_sense_integration_time(self, time):
		"""
		Sets the integration time to the smallest setting that includes the parameter (250 μs, 1 ms, 4 ms, 16.6 ms or 20 ms, 100 ms, or 200 ms).
		
		Input:
			time (float) : integration time in seconds
		
		Output:
			None
		"""
		self._visainstrument.write(':SENS:ITIM %e' % time)
	
	def do_get_sense_delay_minimum(self):
		"""
		Queries the minimum measurement delay in seconds.
		
		Input:
			None
		
		Output:
			delay (float) : minimum measurement delay in seconds
		"""
		return self._visainstrument.query(':SENS:DEL? MIN').replace('\n', '')
	
	def do_get_sense_delay_maximum(self):
		"""
		Queries the maximum measurement delay in seconds.
		
		Input:
			None
		
		Output:
			delay (float) : maximum measurement delay in seconds
		"""
		return self._visainstrument.query(':SENS:DEL? MAX').replace('\n', '')
	
	def do_get_sense_delay(self):
		"""
		Queries the current measurement delay in seconds.
		
		Input:
			None
		
		Output:
			delay (float) : measurement delay in seconds
		"""
		return self._visainstrument.query(':SENS:DEL?').replace('\n', '')
	
	def do_set_sense_delay(self, delay):
		"""
		Sets the measurement delay in seconds.
		
		Input:
			delay (float) : measurement delay in seconds
		
		Output:
			None
		"""
		return self._visainstrument.write(':SENS:DEL %e' % delay)
	
	def do_get_sense_auto_zero(self):
		"""
		Queries the current autozero state (ON or OFF).
		
		Input:
			None
		
		Output:
			state (int) : autozero state
		"""
		return self._visainstrument.query(':SENS:AZER?').replace('\n', '')
	
	def do_set_sense_auto_zero(self, state):
		"""
		Sets the autozero state (ON or OFF).
		
		Input:
			state (int) : autozero state
		
		Output:
			None
		"""
		self._visainstrument.write(':SENS:AZER %s' % state)
	
	def do_get_sense_average(self):
		"""
		Queries the current average state (ON or OFF).
		
		Input:
			None
		
		Output:
			state (int) : average state
		"""
		return self._visainstrument.query(':SENS:AVER?').replace('\n', '')
	
	def do_set_sense_average(self, state):
		"""
		Sets the average state (ON or OFF).
		
		Input:
			state (int) : average state
		
		Output:
			None
		"""
		self._visainstrument.write(':SENS:AVER %s' % state)
	
	def do_get_sense_average_mode(self):
		"""
		Queries the current average mode (block or moving average).
		
		Input:
			None
		
		Output:
			mode (int) : average mode (block or moving average)
		"""
		map = self.get_parameters()['sense_average_mode']['format_map']
		return list(map.keys())[list(map.values()).index(self._visainstrument.query(':SENS:AVER:MODE?').replace('\n', ''))]
	
	def do_set_sense_average_mode(self, mode):
		"""
		Sets the average mode (block or moving average).
		
		Input:
			mode (int) : average mode (block or moving average)
		
		Output:
			None
		"""
		self._visainstrument.write(':SENS:AVER:MODE %s' % self.get_parameters()['sense_average_mode']['format_map'][mode])
	
	def do_get_sense_average_count_minimum(self):
		"""
		Queries the minimum average count.
		
		Input:
			None
		
		Output:
			count (int) : minimum average count
		"""
		return self._visainstrument.query(':SENS:AVER:COUN? MIN').replace('\n', '')
	
	def do_get_sense_average_count_maximum(self):
		"""
		Queries the maximum average count.
		
		Input:
			None
		
		Output:
			count (int) : maximum average count
		"""
		return self._visainstrument.query(':SENS:AVER:COUN? MAX').replace('\n', '')
	
	def do_get_sense_average_count(self):
		"""
		Queries the current average count.
		
		Input:
			None
		
		Output:
			count (int) : average count
		"""
		return self._visainstrument.query(':SENS:AVER:COUN?').replace('\n', '')
	
	def do_set_sense_average_count(self, count):
		"""
		Sets the average count.
		
		Input:
			count (int) : average count
		
		Output:
			None
		"""
		self._visainstrument.write(':SENS:AVER:COUN %i' % count)
	
	def do_get_sense_auto_change(self):
		"""
		Queries the current auto-V/I mode (ON or OFF).
		
		Input:
			None
		
		Output:
			mode (int) : auto-V/I mode
		"""
		return self._visainstrument.query(':SENS:ACH?').replace('\n', '')
	
	def do_set_sense_auto_change(self, mode):
		"""
		Sets the auto-V/I mode (ON or OFF).
		
		Input:
			mode (int) : auto-V/I mode
		
		Output:
			None
		"""
		self._visainstrument.write(':SENS:ACH %s' % mode)
	
	def do_get_sense_remote_sense(self):
		"""
		Queries the current four-wire measurement (remote sense) setting (ON or OFF).
		
		Input:
			None
		
		Output:
			sense (int) : four-wire measurement setting
		"""
		return self._visainstrument.query(':SENS:RSEN?').replace('\n', '')
	
	def do_set_sense_remote_sense(self, sense):
		"""
		Sets the four-wire measurement (remote sense) setting (ON or OFF).
		
		Input:
			sense (int) : four-wire measurement setting
		
		Output:
			None
		"""
		self._visainstrument.write(':SENS:RSEN %s' % sense)
	
	def do_get_trigger_source(self):
		"""
		Queries the current trigger source (constant period timer, external trigger, or no trigger wait).
		
		Input:
			None
		
		Output:
			state (int) : trigger source
		"""
		map = self.get_parameters()['trigger_source']['format_map']
		return list(map.keys())[list(map.values()).index(self._visainstrument.query(':TRIG:SOUR?').replace('\n', ''))]
	
	def do_set_trigger_source(self, state):
		"""
		Sets the trigger source (constant period timer, external trigger, or no trigger wait).
		
		Input:
			state (int) : trigger source
		
		Output:
			None
		"""
		self._visainstrument.write(':TRIG:SOUR %s' % self.get_parameters()['trigger_source']['format_map'][state])
	
	def do_get_trigger_timer_minimum(self):
		"""
		Queries the minimum period of the constant trigger timer in seconds.
		
		Input:
			None
		
		Output:
			time (float) : minimum period of the constant trigger timer in seconds
		"""
		return self._visainstrument.query(':TRIG:TIM? MIN').replace('\n', '')
	
	def do_get_trigger_timer_maximum(self):
		"""
		Queries the maximum period of the constant trigger timer in seconds.
		
		Input:
			None
		
		Output:
			time (float) : maximum period of the constant trigger timer in seconds
		"""
		return self._visainstrument.query(':TRIG:TIM? MAX').replace('\n', '')
	
	def do_get_trigger_timer(self):
		"""
		Queries the current period of the constant trigger timer in seconds.
		
		Input:
			None
		
		Output:
			time (float) : period of the constant trigger timer in seconds
		"""
		return self._visainstrument.query(':TRIG:TIM?').replace('\n', '')
	
	def do_set_trigger_timer(self, time):
		"""
		Sets the period of the constant trigger timer in seconds.
		
		Input:
			time (float) : period of the constant trigger timer in seconds
		
		Output:
			None
		"""
		self._visainstrument.write(':TRIG:TIM %e' % time)
	
	def do_get_calculate_null(self):
		"""
		Queries the current NULL computation state (ON or OFF).
		
		Input:
			None
		
		Output:
			state (int) : NULL computation state
		"""
		return self._visainstrument.query(':CALC:NULL?').replace('\n', '')
	
	def do_set_calculate_null(self, state):
		"""
		Sets the NULL computation state (ON or OFF).
		
		Input:
			state (int) : NULL computation state
		"""
		self._visainstrument.write(':CALC:NULL %s' % state)
	
	def do_get_calculate_null_offset(self):
		"""
		Queries the current NULL computation offset.
		
		Input:
			None
		
		Output:
			offset (float) : NULL computation offset
		"""
		return self._visainstrument.query(':CALC:NULL:OFFS?').replace('\n', '')
	
	def do_set_calculate_null_offset(self, offset):
		"""
		Sets the NULL computation offset.
		
		Input:
			offset (float) : NULL computation offset
		
		Output:
			None
		"""
		self._visainstrument.write(':CALC:NULL:OFFS %e' % offset)
	
	def do_get_calculate_math(self):
		"""
		Queries the current state of the computation using equations (ON or OFF).
		
		Input:
			None
		
		Output:
			state (int) : state of the computation using equations
		"""
		return self._visainstrument.query(':CALC:MATH?').replace('\n', '')
	
	def do_set_calculate_math(self, state):
		"""
		Sets the state of the computation using equations (ON or OFF).
		
		Input:
			state (int) : state of the computation using equations
		
		Output:
			None
		"""
		self._visainstrument.write(':CALC:MATH %s' % state)
	
	def do_get_calculate_math_select(self):
		"""
		Queries the current definition file of the computation using equations.
		
		Input:
			None
		
		Output:
			file (str) : definition file of the computation using equations
		"""
		return self._visainstrument.query(':CALC:MATH:SEL?').replace('\n', '')
	
	def do_set_calculate_math_select(self, file):
		"""
		Sets the definition file of the computation using equations.
		
		Input:
			file (str) : definition file of the computation using equations
		
		Output:
			None
		"""
		self._visainstrument.write(':CALC:MATH:SEL %s' % file)
	
	# probably doesn't work
	def do_get_calculate_math_catalog(self):
		"""
		Queries the current list of definition files of the computation using equations.
		
		Input:
			None
		
		Output:
			files (list) : list of definition files of the computation using equations.
		"""
		return self._visainstrument.query(':CALC:MATH:CAT?').replace('\n', '')
	
	def do_get_calculate_math_parameter_a(self):
		"""
		Queries the current equation parameter A.
		
		Input:
			None
		
		Output:
			a (float) : equation parameter A
		"""
		return self._visainstrument.query(':CALC:MATH:PAR:A?').replace('\n', '')
	
	def do_set_calculate_math_parameter_a(self, a):
		"""
		Sets the equation parameter A.
		
		Input:
			a (float) : equation parameter A
		
		Output:
			None
		"""
		self._visainstrument.write(':CALC:MATH:PAR:A %e' % a)
	
	def do_get_calculate_math_parameter_b(self):
		"""
		Queries the current equation parameter B.
		
		Input:
			None
		
		Output:
			b (float) : equation parameter B
		"""
		return self._visainstrument.query(':CALC:MATH:PAR:B?').replace('\n', '')
	
	def do_set_calculate_math_parameter_b(self, b):
		"""
		Sets the equation parameter B.
		
		Input:
			b (float) : equation parameter B
		
		Output:
			None
		"""
		self._visainstrument.write(':CALC:MATH:PAR:B %e' % b)
	
	def do_get_calculate_math_parameter_c(self):
		"""
		Queries the current equation parameter C.
		
		Input:
			None
		
		Output:
			c (float) : equation parameter C
		"""
		return self._visainstrument.query(':CALC:MATH:PAR:C?').replace('\n', '')
	
	def do_set_calculate_math_parameter_c(self, c):
		"""
		Sets the equation parameter C.
		
		Input:
			c (float) : equation parameter C
		
		Output:
			None
		"""
		self._visainstrument.write(':CALC:MATH:PAR:C %e' % c)
	
	def do_get_calculate_limit(self):
		"""
		Queries the state of the comparison operation (ON or OFF).
		
		Input:
			None
		
		Output:
			state (int) : state of the computation operation
		"""
		return self._visainstrument.query(':CALC:LIM?').replace('\n', '')
	
	def do_set_calculate_limit(self, state):
		"""
		Sets the state of the comparison operation (ON or OFF).
		
		Input:
			state (int) : state of the comparison operation
		
		Output:
			None
		"""
		self._visainstrument.write(':CALC:LIM %s' % state)
	
	def do_get_calculate_limit_upper_minimum(self):
		"""
		Queries the minimum upper limit of the comparison operation.
		
		Input:
			None
		
		Output:
			limit (float) : minimum upper limit of the comparison operation
		"""
		return self._visainstrument.query(':CALC:LIM:UPP? MIN').replace('\n', '')
	
	def do_get_calculate_limit_upper_maximum(self):
		"""
		Queries the maximum upper limit of the comparison operation.
		
		Input:
			None
		
		Output:
			limit (float) : maximum upper limit of the comparison operation
		"""
		return self._visainstrument.query(':CALC:LIM:UPP? MAX').replace('\n', '')
	
	def do_get_calculate_limit_upper(self):
		"""
		Queries the current upper limit of the comparison operation.
		
		Input:
			None
		
		Output:
			limit (float) : upper limit of the comparison operation
		"""
		return self._visainstrument.query(':CALC:LIM:UPP?').replace('\n', '')
	
	def do_set_calculate_limit_upper(self, limit):
		"""
		Sets the upper limit of the comparison operation.
		
		Input:
			limit (float) : upper limit of the comparison operation
		
		Output:
			None
		"""
		self._visainstrument.write(':CALC:LIM:UPP %e' % limit)
	
	def do_get_calculate_limit_lower_minimum(self):
		"""
		Queries the minimum lower limit of the comparison operation.
		
		Input:
			None
		
		Output:
			limit (float) : minimum lower limit of the comparison operation
		"""
		return self._visainstrument.query(':CALC:LIM:LOW? MIN').replace('\n', '')
	
	def do_get_calculate_limit_lower_maximum(self):
		"""
		Queries the maximum lower limit of the comparison operation.
		
		Input:
			None
		
		Output:
			limit (float) : maximum lower limit of the comparison operation
		"""
		return self._visainstrument.query(':CALC:LIM:LOW? MAX').replace('\n', '')
	
	def do_get_calculate_limit_lower(self):
		"""
		Queries the current lower limit of the comparison operation.
		
		Input:
			None
		
		Output:
			limit (float) : lower limit of the comparison operation
		"""
		return self._visainstrument.query(':CALC:LIM:LOW?').replace('\n', '')
	
	def do_set_calculate_limit_lower(self, limit):
		"""
		Sets the lower limit of the comparison operation.
		
		Input:
			limit (float) : lower limit of the comparison operation
		
		Output:
			None
		"""
		self._visainstrument.write(':CALC:LIM:LOW %e' % limit)
	
	#################################################
	
	def do_set_save(self, file):
		"""
		Saves the settings as Setup 1, 2, 3, or 4.
		
		Input:
			file (int) : setup file number
		
		Output:
			None
		"""
		self._visainstrument.write(':*SAV %i' % file)
	
	def do_set_recall(self, file):
		"""
		Loads the saved settings from Setup 1, 2, 3, or 4.
		
		Input:
			file (int) : setup file number
		
		Output:
			None
		"""
		self._visainstrument.write(':*RCL %i' % file)
	
	def do_get_service_request_enable_register(self):
		"""
		Queries the current service request enable register.
		
		Input:
			None
		
		Output:
			register (int) : service request enable register
		"""
		return self._visainstrument.query(':*SRE?').replace('\n', '')
	
	def do_set_service_request_enable_register(self, register):
		"""
		Sets the service request enable register.
		
		Input:
			register (int) : service request enable register
		
		Output:
			None
		"""
		self._visainstrument.write(':*SRE %i' % register)
	
	def do_get_standard_event_enable_register(self):
		"""
		Queries the current standard event enable register.
		
		Input:
			None
		
		Output:
			register (int) : standard event enable register
		"""
		return self._visainstrument.query(':*ESR?').replace('\n', '')
	
	def do_set_standard_event_enable_register(self, register):
		"""
		Sets the standard event enable register.
		
		Input:
			register (int) : standard event enable register
		
		Output:
			None
		"""
		self._visainstrument.write(':*ESR %i' % register)
	
	#def source_list_delete(self, file):
	#    """
	#    Deletes the program sweep pattern file.
	#    
	#    Input:
	#        file (str) : pattern file name
	#    
	#    Output:
	#        None
	#    """
	#    self._visainstrument.write(':SOUR:LIST:DEL %s' % file)
	
	#def source_list_define(self, file, contents):
	#    """
	#    Creates a program sweep pattern file.
	#    
	#    Input:
	#        file (str)     : pattern file name
	#        contents (str) : contents to be written to file
	#    
	#    Output:
	#        None
	#    """
	#    self._visainstrument.write(':SOUR:LIST:DEF "test.csv", "1.0\r\n2.0\r\n')
	#    #self._visainstrument.write(':SOUR:LIST:DEF %s, %s' % (file, contents))
	
	def source_voltage_range_increment(self):
		"""
		Increases the source voltage range by 1 setting.
		
		Input:
			None
		
		Output:
			None
		"""
		self._visainstrument.write(':SOUR:VOLT:RANG UP')
	
	def source_voltage_range_decrement(self):
		"""
		Decreases the source voltage range by 1 setting.
		
		Input:
			None
		
		Output:
			None
		"""
		self._visainstrument.write(':SOUR:VOLT:RANG DOWN')
	
	def source_current_range_increment(self):
		"""
		Increases the source current range by 1 setting.
		
		Input:
			None
		
		Output:
			None
		"""
		self._visainstrument.write(':SOUR:CURR:RANG UP')
	
	def source_current_range_decrement(self):
		"""
		Decreases the source current range by 1 setting.
		
		Input:
			None
		
		Output:
			None
		"""
		self._visainstrument.write(':SOUR:CURR:RANG DOWN')
	
	def sweep_trigger(self):
		"""
		Starts the sweep operation.
		
		Input:
			None
		
		Output:
			None
		"""
		self._visainstrument.write(':SWE:TRIG')
		
	def sense_auto_zero_execute(self):
		"""
		Executes auto-zero.
		
		Input:
			None
		
		Output:
			None
		"""
		self._visainstrument.write(':SENS:AZER:EXEC')
	
	def sense_integration_time_plc(self):
		"""
		Sets the integration time to 1 cycle of the power frequency.
		
		Input:
			None
		
		Output:
			None
		"""
		self._visainstrument.write(':SENS:ITIM PLC')
	
	def sense_integration_time_increment(self):
		"""
		Increases the integration time by 1 setting.
		
		Input:
			None
		
		Output:
			None
		"""
		self._visainstrument.write(':SENS:ITIM UP')
	
	def sense_integration_time_decrement(self):
		"""
		Decreases the integration time by 1 setting.
		
		Input:
			None
		
		Output:
			None
		"""
		self._visainstrument.write(':SENS:ITIM DOWN')
	
	def calculate_math_delete(self, file):
		"""
		Deletes the definition file of the computation using equations.
		
		Input:
			file (str) : file name
		
		Output:
			None
		"""
		self._visainstrument.write(':CALC:MATH:DEL %s' % file)
	
	def calculate_math_define(self, file, contents):
		"""
		Creates a definition file of the computation using equations.
		
		Input:
			file (str)     : file name
			contents (str) : contents to be written to file
		
		Output:
			None
		"""
		self._visainstrument.write(':CALC:MATH:DEF %s, %s' % (file, contents))
	
	def system_wait(self, time):
		"""
		Holds the GS610 for the specified wait time in seconds.

		Input:
			time (float) : wait time in seconds

		Output:
			None
		"""
		self._visainstrument.write(':SYST:WAIT %e' % time)

	def initiate(self):
		"""
		Starts a new measurement.
		
		Input:
			None
		
		Output:
			None
		"""
		self._visainstrument.write(':INIT')
	
	def fetch(self):
		"""
		Queries the measured results.
		
		Input:
			None
		
		Output:
			value (str) : measured results
		"""
		return self._visainstrument.query(':FETC?').replace('\n', '')
	
	def read(self):
		"""
		Starts a new measurement and queries the measured results.
		
		Input:
			None
		
		Output:
			value (str) : measured results
		"""
		return (float)(self._visainstrument.query(':READ?').replace('\n', ''))
	
	def identify(self):
		"""
		Queries the instrument model.
		
		Input:
			None
		
		Output:
			model (str) : instrument model
		"""
		return self._visainstrument.query(':*IDN?').replace('\n', '')
	
	def options(self):
		"""
		Queries the options (None or ethernet option)
		
		Input:
			None
		
		Output:
			options (str) : options
		"""
		return self._visainstrument.query(':*OPT?').replace('\n', '')
	
	def trigger(self):
		"""
		Generates a trigger.
		
		Input:
			None
		
		Output:
			None
		"""
		self._visainstrument.write(':*TRG').replace('\n', '')
	
	def calibrate(self):
		"""
		Performs a calibration and queries the result (successful if 0, unsuccessful otherwise).
		
		Input:
			None
		
		Output:
			result (int) : calibration result
		"""
		return self._visainstrument.query(':*CAL?').replace('\n', '')
	
	def test(self):
		"""
		Performs a self-test and queries the result (normal if 0, error otherwise).
		
		Input:
			None
		
		Output:
			result (int) : self-test result
		"""
		return self._visainstrument.query(':*TST?').replace('\n', '')
	
	def reset(self):
		"""
		Resets the instrument to default values.
		
		Input:
			None
		
		Output:
			None
		"""
		self._visainstrument.write(':*RST')
	
	def clear(self):
		"""
		Clears the event register and error queue.
		
		Input:
			None
		
		Output:
			None
		"""
		self._visainstrument.write(':*CLS')
	
	def status_byte(self):
		"""
		Queries the status byte and clears the SRQ.
		
		Input:
			None
		
		Output:
			status (int) : status byte
		"""
		return self._visainstrument.query(':*STB').replace('\n', '')
	
	def standard_event_register(self):
		"""
		Queries the standard event register and clears the register.
		
		Input:
			None
		
		Output:
			status (int) : standard event register
		"""
		return self._visainstrument.query(':*ESR?').replace('\n', '')
	
	def generate_operation_complete(self):
		"""
		Generates a standard event OPC when the execution of all previous commands is completed.
		
		Input:
			None
		
		Output:
			None
		"""
		self._visainstrument.write(':*OPC')
	
	def test_operation_complete(self):
		"""
		Queries the completion of the execution of all previous commands (1 if complete).
		
		Input:
			None
		
		Output:
			complete (int) : completion status
		"""
		return self._visainstrument.query(':*OPC?').replace('\n', '')
	
	def wait(self):
		"""
		Waits for the completion of the overlap command.
		
		Input:
			None
		
		Output:
			None
		"""
		self._visainstrument.write(':*WAI')
