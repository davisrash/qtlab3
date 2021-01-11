from source.instrument import Instrument
import visa

#################################
# To Do:
#  - SR860 Driver almost certainly will fail for functions with multiple arguments. Look into the channels parameter and others in the docstring.
#  - It may be the case that all do_get and do_set functions should really be _do_get and _do_set.
#
#  - Fix the preset commands
#     - frequency_preset,
#     - sine_out_amplitude_preset, and
#     - sine_out_dc_level_preset,
#    to work with multiple arguments.
#  - Change sensible 0/1 commands to True/False and add wrapper to convert.
#################################


class SR860(Instrument):
    """
    Creates a new Instrument to interact with the SR860.

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
        self.add_parameter('timebase_mode', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=1)
        self.add_parameter('timebase_source', type=int,
                           flags=Instrument.FLAG_GET,
                           minval=0, maxval=1)
        self.add_parameter('reference_phase_shift', type=float,
                           flags=Instrument.FLAG_GETSET,
                           minval=-360000, maxval=360000, units='DEG')
        self.add_parameter('reference_frequency', type=float,
                           flags=Instrument.FLAG_GETSET,
                           minval=1e-3, maxval=500e6, units='HZ')
        self.add_parameter('internal_reference_frequency', type=float,
                           flags=Instrument.FLAG_GETSET,
                           minval=1e-3, maxval=500e6, units='HZ')
        self.add_parameter('external_reference_frequency', type=float,
                           flags=Instrument.FLAG_GET,
                           minval=1e-3, maxval=500e6, units='HZ')
        self.add_parameter('detection_frequency', type=float,
                           flags=Instrument.FLAG_GET,
                           minval=1e-3, maxval=500e6, units='HZ')
        self.add_parameter('reference_frequency_harmonic_detect', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=1, maxval=99)
        self.add_parameter('external_frequency_harmonic_detect_dual_reference', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=1, maxval=99)
        self.add_parameter('external_SR540_chopper_blade_slots', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=1,
                           format_map={0: 'SLT6',
                                       1: 'SLT30'})
        self.add_parameter('external_SR540_chopper_phase', type=float,
                           flags=Instrument.FLAG_GETSET,
                           units='DEG')
        self.add_parameter('sine_out_amplitude', type=float,
                           flags=Instrument.FLAG_GETSET,
                           minval=1e-9, maxval=2.0, units='V')
        self.add_parameter('sine_out_dc_level', type=float,
                           flags=Instrument.FLAG_GETSET,
                           minval=-5.0, maxval=5.0, units='V')
        self.add_parameter('sine_out_dc_mode', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=1,
                           format_map={0: 'COM',
                                       1: 'DIF'})
        self.add_parameter('reference_source', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=3,
                           format_map={0: 'INT',
                                       1: 'EXT',
                                       2: 'DUAL',
                                       3: 'CHOP'})
        self.add_parameter('external_reference_trigger_mode', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=2,
                           format_map={0: 'SIN',
                                       1: 'POS',
                                       2: 'NEG'})
        self.add_parameter('external_reference_trigger_input', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=1,
                           format_map={0: '50',
                                       1: '1M'})
        self.add_parameter('frequency_preset', type=float,
                           flags=Instrument.FLAG_GETSET,
                           minval=1e-3, maxval=500e6, units='HZ')
        self.add_parameter('sine_out_amplitude_preset', type=float,
                           flags=Instrument.FLAG_GETSET,
                           minval=1e-9, maxval=2.0, units='V')
        self.add_parameter('sine_out_dc_level_preset', type=float,
                           flags=Instrument.FLAG_GETSET,
                           minval=-5.0, maxval=5.0, units='V')

        # signal parameters
        self.add_parameter('signal_input', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=1,
                           format_map={0: 'VOLT',
                                       1: 'CURR'})
        self.add_parameter('voltage_input_mode', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=1,
                           format_map={0: 'A',
                                       1: 'A-B'})
        self.add_parameter('voltage_input_coupling', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=1,
                           format_map={0: 'AC',
                                       1: 'DC'})
        self.add_parameter('voltage_input_shields', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=1,
                           format_map={0: 'FLO',
                                       1: 'GRO'})
        self.add_parameter('voltage_input_range', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=4,
                           format_map={0: 1.0,
                                       1: 0.3,
                                       2: 0.1,
                                       3: 0.03,
                                       4: 0.01})
        self.add_parameter('current_input_gain', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=1)
        self.add_parameter('signal_strength', type=int,
                           flags=Instrument.FLAG_GET,
                           minval=0, maxval=4)
        self.add_parameter('sensitivity', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=27)
        self.add_parameter('time_constant', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=21)
        self.add_parameter('filter_slope', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=3)
        self.add_parameter('synchronous_filter', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=1)
        self.add_parameter('advanced_filter', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=1)
        self.add_parameter('equivalent_noise_bandwidth', type=float,
                           flags=Instrument.FLAG_GET,
                           units='HZ')

        # ch1/ch2 output parameters
        self.add_parameter('channel_output', type=(int, int),
                           flags=Instrument.FLAG_GETSET,
                           minval=(0, 0), maxval=(1, 1))
        self.add_parameter('output_expand', type=(int, int),
                           flags=Instrument.FLAG_GETSET,
                           minval=(0, 0), maxval=(2, 2))
        self.add_parameter('output_offset', type=(int, int),
                           flags=Instrument.FLAG_GETSET,
                           minval=(0, 0), maxval=(2, 1))
        self.add_parameter('output_offset_percentage',
                           type=(int, float),
                           flags=Instrument.FLAG_GETSET,
                           minval=(0, -999.99), maxval=(2, 999.99))
        self.add_parameter('auto_offset', type=int,
                           flags=Instrument.FLAG_SET,
                           minval=0, maxval=2)
        self.add_parameter('ratio_function', type=(int, int),
                           flags=Instrument.FLAG_GETSET,
                           minval=(0, 0), maxval=(2, 1))

        # aux input and output commands
        self.add_parameter('aux_input_voltage', type=int,
                           flags=Instrument.FLAG_GET,
                           minval=0, maxval=3)
        self.add_parameter('aux_output_voltage', type=(int, float),
                           flags=Instrument.FLAG_GETSET,
                           minval=(0, -10.5), maxval=(3, 10.5),
                           units=('', 'V'))

        # display parameters
        self.add_parameter('front_panel_blanking', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=1)
        self.add_parameter('screen_layout', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=5)
        self.add_parameter('channel_param', type=(int, int),
                           flags=Instrument.FLAG_GETSET,
                           minval=(0, 0), maxval=(3, 16))
        self.add_parameter('channel_strip_chart_graph', type=(int, int),
                           flags=Instrument.FLAG_GETSET,
                           minval=(0, 0), maxval=(3, 1))
        
        # strip chart parameters
        self.add_parameter('horizontal_time_scale', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=16)
        self.add_parameter('channel_vertical_scale', type=(int, float),
                           flags=Instrument.FLAG_GETSET,
                           #minval=(0, 0+), maxval=(3, x)  unknown max
                           )
        self.add_parameter('channel_vertical_offset', type=(int, float),
                           flags=Instrument.FLAG_GETSET,
                           #minval=(0, -x), maxval=(3, x)  unknown range
                           )
        self.add_parameter('channel_graph', type=(int, int),
                           flags=Instrument.FLAG_GETSET,
                           minval=(0, 0), maxval=(3, 1))
        self.add_parameter('strip_chart', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=1)
        self.add_parameter('strip_chart_cursor_pos', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=639)
        self.add_parameter('strip_chart_cursor_mode', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=1)
        self.add_parameter('strip_chart_cursor_display_mode', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=1)
        self.add_parameter('strip_chart_cursor_readout_mode', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=2)
        self.add_parameter('strip_chart_cursor_width', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=2)
        self.add_parameter('channel_strip_chart_cursor_value', type=(int, float),
                           flags=Instrument.FLAG_GET,
                           #minval=(0, -x), maxval=(4, x)  unknown range
                           )
        self.add_parameter('strip_chart_cursor_horizontal_time', type=str,
                           flags=Instrument.FLAG_GET)
        self.add_parameter('strip_chart_cursor_horizontal_pos', type=str,
                           flags=Instrument.FLAG_GET)
        
        # FFT screen parameters
        self.add_parameter('FFT_source', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=2)
        self.add_parameter('FFT_vertical_scale', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=-20, maxval=20)
        self.add_parameter('FFT_vertical_offset', type=float,
                           flags=Instrument.FLAG_GETSET,
                           #minval=?, maxval=?  unknown range
                           )
        self.add_parameter('FFT_max_span', type=float,
                           flags=Instrument.FLAG_GET)
        self.add_parameter('FFT_span', type=float,
                           flags=Instrument.FLAG_GETSET,
                           #minval=?,  unknown min
                           maxval=float(self.do_get_FFT_max_span()))
        self.add_parameter('FFT_averaging', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=4)
        self.add_parameter('FFT_graph', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=1)
        self.add_parameter('FFT_cursor_width', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=2)
        self.add_parameter('FFT_cursor_frequency',
                           #type=float,  unknown if float or int
                           flags=Instrument.FLAG_GET,
                           #minval=?, maxval=?,  unknown range
                           units='HZ')
        self.add_parameter('FFT_cursor_amp',
                           #type=float,  unknown if float or int
                           flags=Instrument.FLAG_GET,
                           #minval=0, maxval=0  unknown range
                           #units='DB'  valid unit? necessary?
                           )
        
        # scan parameters
        self.add_parameter('scan_param', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=4)
        self.add_parameter('scan_type', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=1)
        self.add_parameter('scan_end_mode', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=2)
        self.add_parameter('scan_time', type=int,
                           flags=Instrument.FLAG_GETSET,
                           #minval=0,  minval unknown
                           maxval=1728000)
        self.add_parameter('scan_out_attenuator_op_mode_sine_out_amp',
                           type=int, flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=1)
        self.add_parameter('scan_out_attenuator_op_mode_dc_level',
                           type=int, flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=1)
        self.add_parameter('scan_param_update_interval', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=16)
        self.add_parameter('scan_enabled', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=1)
        self.add_parameter('scan_state', type=int,
                           flags=Instrument.FLAG_GET,
                           minval=0, maxval=4)
        self.add_parameter('scan_freq', type=(int, float),
                           flags=Instrument.FLAG_GETSET,
                           minval=(0, 1e-3), maxval=(1, 500e3),
                           units='HZ')
        self.add_parameter('scan_amp', type=(int, float),
                           flags=Instrument.FLAG_GETSET,
                           minval=(0, 1e-9), maxval=(1, 2),
                           units='V')
        self.add_parameter('scan_ref_dc_level', type=(int, float),
                           flags=Instrument.FLAG_GETSET,
                           minval=(0, -5), maxval=(1, 5),
                           units='V')
        self.add_parameter('scan_aux_out_1_level', type=(int, float),
                           flags=Instrument.FLAG_GETSET,
                           minval=(0, -10.5), maxval=(1, 10.5),
                           units='V')
        self.add_parameter('scan_aux_out_2_level', type=(int, float),
                           flags=Instrument.FLAG_GETSET,
                           minval=(0, -10.5), maxval=(1, 10.5),
                           units='V')

        # auto functions
        self.add_function('auto_phase')
        self.add_function('auto_range')
        self.add_function('auto_scale')

        # display functions
        self.add_function('screenshot')
        #self.add_function('get_screen')

        # strip chart functions
        self.add_function('channel_auto_scale')
        self.add_function('channel_auto_scale_zero_center')
        self.add_function('channel_auto_find')

        # FFT functions
        self.add_function('FFT_auto_scale')

        # scan functions
        self.add_function('start_scan')
        self.add_function('pause_scan')
        self.add_function('reset_scan')

    def do_get_timebase_mode(self):
        """
        Queries the current external timebase mode at 10 MHz. Returns either auto (0) or internal (1).

        Input:
                None

        Output:
                mode (int) : timebase mode
        """
        return self._visainstrument.query(':TBMODE?').replace('\n', '')

    def do_set_timebase_mode(self, mode):
        """
        Sets the external timebase mode at 10 MHz to either auto (0) or internal (1).

        Input:
                mode (int) : timebase mode

        Output:
                None
        """
        self._visainstrument.write(':TBMODE {}'.format(mode))

    def do_get_timebase_source(self):
        """
        Queries the current timebase source at 10 MHz. Returns either external (0) or internal (1).

        Input:
                None

        Output:
                source (int) : timebase source
        """
        return self._visainstrument.query(':TBSTAT?').replace('\n', '')

    def do_get_reference_phase_shift(self):
        """
        Queries the current reference phase shift. The phase shift has a resolution of ~0.0000001° and is wrapped around at ±180°.

        Input:
                None

        Output:
                phase_shift (float) : reference phase shift in degrees
        """
        return self._visainstrument.query(':PHAS?').replace('\n', '')

    def do_set_reference_phase_shift(self, phase_shift):
        """
        Sets the reference phase shift. The phase shift has a resolution of ~0.0000001° and is wrapped around at ±180°.

        Input:
                phase_shift (float) : reference phase shift in degrees

        Output:
                None
        """
        self._visainstrument.write(':PHAS {}'.format(phase_shift))

    def do_get_reference_frequency(self):
        """
        Queries the current internal reference frequency whenever the reference mode is one of Internal, Dual, or Chop. Otherwise, in External mode, the query returns the external reference frequency. This behavior mirrors the value displayed in the info bar at the top of the display.

        Input:
                None

        Output:
                frequency (float) : internal or external reference frequency in hertz
        """
        return self._visainstrument.query(':FREQ?').replace('\n', '')

    def do_set_reference_frequency(self, frequency):
        """
        Sets the internal reference frequency. The frequency will be rounded to 6 digits or 0.1 mHz, whichever is greater.

        Input:
                frequency (float) : internal frequency in hertz
        Output:
                None
        """
        self._visainstrument.write(':FREQ {}'.format(frequency))

    def do_get_internal_reference_frequency(self):
        """
        Queries the current internal reference frequency.

        Input:
                None

        Output:
                frequency (float) : internal frequency in hertz
        """
        return self._visainstrument.query(':FREQINT?').replace('\n', '')

    def do_set_internal_reference_frequency(self, frequency):
        """
        Sets the internal reference frequency. The frequency will be rounded to 6 digits or 0.1 mHz, whichever is greater.

        Input:
                frequency (float) : internal frequency in hertz

        Output:
                None
        """
        self._visainstrument.write(':FREQINT {}'.format(frequency))

    def do_get_external_reference_frequency(self):
        """
        Queries the current external reference frequency.

        Input:
                None

        Output:
                frequency (float) : external reference frequency in hertz
        """
        return self._visainstrument.query(':FREQEXT?').replace('\n', '')

    def do_get_detection_frequency(self):
        """
        Queries the current detection frequency. This is helpful in dual reference mode or harmonic detection. Otherwise, the detection frequency is either the internal or external reference frequency.

        Input:
                None

        Output:
                frequency (float) : detection frequency in hertz
        """
        return self._visainstrument.query(':FREQDET?').replace('\n', '')

    def do_get_reference_frequency_harmonic_detect(self):
        """
        Queries the harmonic number of the reference frequency.

        Input:
                None

        Output:
                harmonic (int) : harmonic number of the reference frequency
        """
        return self._visainstrument.query(':HARM?').replace('\n', '')

    def do_set_reference_frequency_harmonic_detect(self, harmonic):
        """
        Sets the lock-in to detect at the given harmonic of the reference frequency.

        Input:
                harmonic (int) : harmonic number of the reference frequency

        Output:
                None
        """
        self._visainstrument.write(':HARM {}'.format(harmonic))

    def do_get_external_frequency_harmonic_detect_dual_reference(self):
        """
        Queries the harmonic number of the external frequency in dual reference mode.

        Input:
                None

        Output:
                harmonic (int) : harmonic number of the external reference frequency in dual reference mode
        """
        return self._visainstrument.query(':HARMDUAL?').replace('\n', '')

    def do_set_external_frequency_harmonic_detect_dual_reference(self, harmonic):
        """
        Sets the lock-in to detect at the given harmonic of the external frequency in dual reference mode.

        Input:
                harmonic (int) : harmonic number of the external reference frequency in dual reference mode

        Output:
                None
        """
        self._visainstrument.write(':HARMDUAL {}'.format(harmonic))

    def do_get_external_SR540_chopper_blade_slots(self):
        """
        Queries the blade slots setting for operation with an external SR540 chopper. Returns either 6-slot (0) or 30-slot (1).

        Input:
                None

        Output:
                slots (int) : blade slot setting
        """
        return self._visainstrument.query(':BLADESLOTS?').replace('\n', '')

    def do_set_external_SR540_chopper_blade_slots(self, slots):
        """
        Configures the SR860 for either 6-slot (0) or 30-slot (1) operation with an external SR540 chopper.

        Input:
                slots (int) : blade slot setting

        Output:
                None
        """
        self._visainstrument.write(':BLADESLOTS {}'.format(slots))

    def do_get_external_SR540_chopper_phase(self):
        """
        """
        return self._visainstrument.query(':BLADEPHASE?').replace('\n', '')

    def do_set_external_SR540_chopper_phase(self, phase):
        """
        """
        self._visainstrument.write(':BLADEPHASE {}'.format(phase))

    def do_get_sine_out_amplitude(self):
        """
        """
        return self._visainstrument.query(':SLVL?').replace('\n', '')

    def do_set_sine_out_amplitude(self, amplitude):
        """
        """
        self._visainstrument.write(':SLVL {}'.format(amplitude))

    def do_get_sine_out_dc_level(self):
        """
        """
        return self._visainstrument.query(':SOFF?').replace('\n', '')

    def do_set_sine_out_dc_level(self, level):
        """
        """
        self._visainstrument.write(':SOFF {}'.format(level))

    def do_get_sine_out_dc_mode(self):
        """
        """
        return self._visainstrument.query(':REFM?').replace('\n', '')

    def do_set_sine_out_dc_mode(self, mode):
        """
        """
        self._visainstrument.write(':REFM {}'.format(mode))

    def do_get_reference_source(self):
        """
        """
        return self._visainstrument.query(':RSRC?').replace('\n', '')

    def do_set_reference_source(self, source):
        """
        """
        self._visainstrument.write(':RSRC {}'.format(source))

    def do_get_external_reference_trigger_mode(self):
        """
        """
        return self._visainstrument.query(':RTRG?').replace('\n', '')

    def do_set_external_reference_trigger_mode(self, mode):
        """
        """
        self._visainstrument.write(':RTRG {}'.format(mode))

    def do_get_external_reference_trigger_input(self):
        """
        """
        return self._visainstrument.query(':REFZ?').replace('\n', '')

    def do_set_external_reference_trigger_input(self, resistance):
        """
        """
        self._visainstrument.write(':REFZ {}'.format(resistance))

    def do_get_frequency_preset(self):
        """
        """
        return self._visainstrument.query(':PSTF? 0').replace('\n', '')

    def do_set_frequency_preset(self, frequency):
        """
        """
        self._visainstrument.write(':PSTF 0, {}'.format(frequency))

    def do_get_sine_out_amplitude_preset(self):
        """
        """
        return self._visainstrument.query(':PSTA? 0').replace('\n', '')

    def do_set_sine_out_amplitude_preset(self, amplitude):
        """
        """
        self._visainstrument.write(':PSTA 0, {}'.format(amplitude))

    def do_get_sine_out_dc_level_preset(self):
        """
        """
        return self._visainstrument.query(':PSTL? 0').replace('\n', '')

    def do_set_sine_out_dc_level_preset(self, level):
        """
        """
        self._visainstrument.write(':PSTL 0, {}'.format(level))

    def do_get_signal_input(self):
        """
        """
        return self._visainstrument.query(':IVMD?').replace('\n', '')

    def do_set_signal_input(self, signal):
        """
        """
        self._visainstrument.write(':IVMD {}'.format(signal))

    def do_get_voltage_input_mode(self):
        """
        """
        return self._visainstrument.query(':ISRC?').replace('\n', '')

    def do_set_voltage_input_mode(self, mode):
        """
        """
        self._visainstrument.write(':ISRC {}'.format(mode))

    def do_get_voltage_input_coupling(self):
        """
        """
        return self._visainstrument.query(':ICPL?').replace('\n', '')

    def do_set_voltage_input_coupling(self, coupling):
        """
        """
        self._visainstrument.write(':ICPL {}'.format(coupling))

    def do_get_voltage_input_shields(self):
        """
        """
        return self._visainstrument.query(':IGND?').replace('\n', '')

    def do_set_voltage_input_shields(self, shields):
        """
        """
        self._visainstrument.write(':IGND {}'.format(shields))

    def do_get_voltage_input_range(self):
        """
        """
        return self._visainstrument.query(':IRNG?').replace('\n', '')

    def do_set_voltage_input_range(self, input_range):
        """
        """
        self._visainstrument.write(':IRNG {}'.format(input_range))

    def do_get_current_input_gain(self):
        """
        Queries the current current input gain. Returns either 0 for 1 MΩ (1 μA) or 1 for 100 MΩ (10 nA).

        Input:
                None

        Output:
                gain (int) : current input gain setting
        """
        return self._visainstrument.query(':ICUR?').replace('\n', '')

    def do_set_current_input_gain(self, gain):
        """
        Sets the current input gain to 1 MΩ (1 μA) for gain == 0 or 100 MΩ (10 nA) for gain == 1.

        Input:
                gain (int) : current input gain setting

        Output:
                None
        """
        self._visainstrument.write(':ICUR {}'.format(gain))

    def do_get_signal_strength(self):
        """
        Queries the signal strength indicator. Returns an int between 0 for lowest and 4 for overload, inclusive.

        Input:
                None

        Output:
                strength (int) : signal strength indicator
        """
        return self._visainstrument.query(':ILVL?').replace('\n', '')

    def do_get_sensitivity(self):
        """
        Queries the sensitivity. Returns an int s according to the table below.

        s   sensitivity
        0   1 V [μA]
        1   500 mV [nA]
        2   200 mV [nA]
        3   100 mV [nA]
        4   50 mV [nA]
        5   20 mV [nA]
        6   10 mV [nA]
        7   5 mV [nA]
        8   2 mV [nA]
        9   1 mV [nA]
        10  500 μV [pA]
        11  200 μV [pA]
        12  100 μV [pA]
        13  50 μV [pA]
        14  20 μV [pA]
        15  10 μV [pA]
        16  5 μV [pA]
        17  2 μV [pA]
        18  1 μV [pA]
        19  500 nV [fA]
        20  200 nV [fA]
        21  100 nV [fA]
        22  50 nV [fA]
        23  20 nV [fA]
        24  10 nV [fA]
        25  5 nV [fA]
        26  2 nV [fA]
        27  1 nV [fA]

        Input:
                None

        Output:
                s (int) : sensitivity setting
        """
        return self._visainstrument.query(':SCAL?').replace('\n', '')

    def do_set_sensitivity(self, s):
        """
        Sets the sensitivity according to the table below.

        s   sensitivity
        0   1 V [μA]
        1   500 mV [nA]
        2   200 mV [nA]
        3   100 mV [nA]
        4   50 mV [nA]
        5   20 mV [nA]
        6   10 mV [nA]
        7   5 mV [nA]
        8   2 mV [nA]
        9   1 mV [nA]
        10  500 μV [pA]
        11  200 μV [pA]
        12  100 μV [pA]
        13  50 μV [pA]
        14  20 μV [pA]
        15  10 μV [pA]
        16  5 μV [pA]
        17  2 μV [pA]
        18  1 μV [pA]
        19  500 nV [fA]
        20  200 nV [fA]
        21  100 nV [fA]
        22  50 nV [fA]
        23  20 nV [fA]
        24  10 nV [fA]
        25  5 nV [fA]
        26  2 nV [fA]
        27  1 nV [fA]

        Input:
                s (int) : sensitivity setting

        Output:
                None
        """
        self._visainstrument.write(':SCAL {}'.format(s))

    def do_get_time_constant(self):
        """
        Queries the time constant. Returns an int t according to the table below.

        t   time constant
        0   1 μs
        1   3 μs
        2   10 μs
        3   30 μs
        4   100 μs
        5   300 μs
        6   1 ms
        7   3 ms
        8   10 ms
        9   30 ms
        10  100 ms
        11  300 ms
        12  1 s
        13  3 s
        14  10 s
        15  30 s
        16  100 s
        17  300 s
        18  1 ks
        19  3 ks
        20  10 ks
        21  30 ks

        Input:
                None

        Output:
                t (int) : time constant setting
        """
        return self._visainstrument.query(':OFLT?').replace('\n', '')

    def do_set_time_constant(self, t):
        """
        Sets the time constant according to the table below.

        t   time constant
        0   1 μs
        1   3 μs
        2   10 μs
        3   30 μs
        4   100 μs
        5   300 μs
        6   1 ms
        7   3 ms
        8   10 ms
        9   30 ms
        10  100 ms
        11  300 ms
        12  1 s
        13  3 s
        14  10 s
        15  30 s
        16  100 s
        17  300 s
        18  1 ks
        19  3 ks
        20  10 ks
        21  30 ks

        Input:
                t (int) : time constant setting

        Output:
                None
        """
        self._visainstrument.write(':OFLT {}'.format(t))

    def do_get_filter_slope(self):
        """
        """
        return self._visainstrument.query(':OFSL?').replace('\n', '')

    def do_set_filter_slope(self, slope):
        """
        Sets the filter slope to 6 dB/oct for slope == 0, 12 dB/oct for slope == 1, 18 dB/oct for slope == 2, or 24 dB/oct for slope == 3.

        Input:
                slope (int) : filter slope setting

        Output:
                None
        """
        self._visainstrument.write(':OFSL {}'.format(slope))

    def do_get_synchronous_filter(self):
        """
        """
        return self._visainstrument.query(':SYNC?').replace('\n', '')

    def do_set_synchronous_filter(self, setting):
        """
        """
        self._visainstrument.write(':SYNC {}'.format(setting))

    def do_get_advanced_filter(self):
        """
        """
        return self._visainstrument.query(':ADVFILT?').replace('\n', '')

    def do_set_advanced_filter(self, setting):
        """
        """
        self._visainstrument.write(':ADVFILT {}'.format(setting))

    def do_get_equivalent_noise_bandwidth(self):
        """
        """
        return self._visainstrument.query(':ENBW?').replace('\n', '')

    def do_get_channel_output(self, channel):
        """
        """
        return self._visainstrument.query(':COUT? {}'.format(channel)).replace('\n', '')

    def do_set_channel_output(self, channel, output):
        """
        Sets either the Channel 1 for channel == 1 or the Channel 2 for channel == 2 output mode to either rectangular (XY) for output == 0 or polar (Rθ) for output == 1. 
        """
        self._visainstrument.write(':COUT {}, {}'.format(channel, output))

    def do_get_output_expand(self, axis):
        """
        """
        return self._visainstrument.query(':CEXP? {}'.format(axis)).replace('\n', '')

    def do_set_output_expand(self, axis, mode):
        """
        """
        self._visainstrument.write(':CEXP {}, {}'.format(axis, mode))

    def do_get_output_offset(self, axis):
        """
        """
        return self._visainstrument.query(':COFA? {}'.format(axis)).replace('\n', '')

    def do_set_output_offset(self, axis, offset):
        """
        """
        self._visainstrument.write(':COFA {}, {}'.format(axis, offset))

    def do_get_output_offset_percentage(self, axis):
        """
        """
        return self._visainstrument.query(':COFP? {}'.format(axis)).replace('\n', '')

    def do_set_output_offset_percentage(self, axis, percentage):
        """
        """
        self._visainstrument.write(':COFP {}, {}'.format(axis, percentage))

    def do_get_auto_offset(self):
        """
        """
        return self._visainstrument.query(':OAUT?').replace('\n', '')

    def do_set_auto_offset(self, axis):
        """
        """
        self._visainstrument.write(':OAUT {}'.format(axis))

    def do_get_ratio_function(self, axis):
        """
        """
        return self._visainstrument.query(':CRAT? {}'.format(axis)).replace('\n', '')

    def do_set_ratio_function(self, axis, mode):
        """
        """
        self._visainstrument.write(':CRAT {}, {}'.format(axis, mode))

    def do_get_aux_input_voltage(self):
        """
        """
        return self._visainstrument.query(':OAUX?').replace('\n', '')
    
    def do_get_aux_output_voltage(self, output):
        """
        """
        return self._visainstrument.query(':AUXV? {}'.format(output)).replace('\n', '')
    
    def do_set_aux_output_voltage(self, output, level):
        """
        """
        self._visainstrument.write(':AUXV {}, {}'.format(output, level))
    
    def do_get_front_panel_blanking(self):
        """
        """
        return self._visainstrument.query(':DBLK?').replace('\n', '')
    
    def do_set_front_panel_blanking(self, setting):
        """
        """
        self._visainstrument.write(':DBLK {}'.format(setting))
    
    def do_get_screen_layout(self):
        """
        """
        return self._visainstrument.query(':DLAY?').replace('\n', '')
    
    def do_set_screen_layout(self, layout):
        """
        """
        self._visainstrument.write(':DLAY {}'.format(layout))
    
    def do_get_channel_param(self, channel):
        """
        """
        return self._visainstrument.query(':CDSP? {}'.format(channel)).replace('\n', '')
    
    def do_set_channel_param(self, channel, param):
        """
        """
        self._visainstrument.write(':CDSP {}, {}'.format(channel, param))
    
    def do_get_channel_strip_chart_graph(self, channel):
        """
        """
        return self._visainstrument.query(':CGRF? {}'.format(channel)).replace('\n', '')
    
    def do_set_channel_strip_chart_graph(self, channel, setting):
        """
        """
        self._visainstrument.write(':CGRF {}, {}'.format(channel, setting))
    
    def do_get_horizontal_time_scale(self):
        """
        """
        return self._visainstrument.query(':GSPD?').replace('\n', '')
    
    def do_set_horizontal_time_scale(self, scale):
        """
        """
        self._visainstrument.write(':GSPD {}'.format(scale))
    
    def do_get_channel_vertical_scale(self, channel):
        """
        """
        return self._visainstrument.query(':GSCL? {}'.format(channel)).replace('\n', '')

    def do_set_channel_vertical_scale(self, channel, scale):
        """
        """
        self._visainstrument.write(':GSCL {}, {}'.format(channel, scale))

    def do_get_channel_vertical_offset(self, channel):
        """
        """
        return self._visainstrument.query(':GOFF? {}'.format(channel)).replace('\n', '')
    
    def do_set_channel_vertical_offset(self, channel, offset):
        """
        """
        self._visainstrument.write(':GOFF {}, {}'.format(channel, offset))
    
    def do_get_channel_graph(self, channel):
        """
        """
        return self._visainstrument.query(':CGRF? {}'.format(channel)).replace('\n', '')
    
    def do_set_channel_graph(self, channel, setting):
        """
        """
        self._visainstrument.write(':CGRF {}, {}'.format(channel, setting))
    
    def do_get_strip_chart(self):
        """
        """
        return self._visainstrument.query(':GLIV?').replace('\n', '')
    
    def do_set_strip_chart(self, setting):
        """
        """
        self._visainstrument.write(':GLIV {}'.format(setting))
    
    def do_get_strip_chart_cursor_pos(self):
        """
        """
        return self._visainstrument.query(':PCUR?').replace('\n', '')
    
    def do_set_strip_chart_cursor_pos(self, pos):
        """
        """
        self._visainstrument.write(':PCUR {}'.format(pos))
    
    def do_get_strip_chart_cursor_mode(self):
        """
        """
        return self._visainstrument.query(':CURREL?').replace('\n', '')
    
    def do_set_strip_chart_cursor_mode(self, mode):
        """
        """
        self._visainstrument.write(':CURREL {}'.format(mode))
    
    def do_get_strip_chart_cursor_display_mode(self):
        """
        """
        return self._visainstrument.query(':CURDISP?').replace('\n', '')
    
    def do_set_strip_chart_cursor_display_mode(self, mode):
        """
        """
        self._visainstrument.write(':CURDISP {}'.format(mode))
    
    def do_get_strip_chart_cursor_readout_mode(self):
        """
        """
        return self._visainstrument.query(':CURBUG?').replace('\n', '')
    
    def do_set_strip_chart_cursor_readout_mode(self, mode):
        """
        """
        self._visainstrument.write(':CURBUG {}'.format(mode))
    
    def do_get_strip_chart_cursor_width(self):
        """
        """
        return self._visainstrument.query(':FCRW?').replace('\n', '')
    
    def do_set_strip_chart_cursor_width(self, width):
        """
        """
        self._visainstrument.write(':FCRW {}'.format(width))
    
    def do_get_channel_strip_chart_cursor_value(self, channel):
        """
        """
        return self._visainstrument.query(':SCRY? {}'.format(channel)).replace('\n', '')
    
    def do_get_strip_chart_cursor_horizontal_time(self):
        """
        """
        return self._visainstrument.query(':CURDATTIM?').replace('\n', '')
    
    def do_get_strip_chart_cursor_horizontal_pos(self):
        """
        """
        return self._visainstrument.query(':CURINTERVAL?').replace('\n', '')

    def do_get_FFT_source(self):
        """
        """
        return self._visainstrument.query(':FFTR?').replace('\n', '')

    def do_set_FFT_source(self, source):
        """
        """
        self._visainstrument.write(':FFTR {}'.format(source))
    
    def do_get_FFT_vertical_scale(self):
        """
        """
        return self._visainstrument.query(':FFTS?').replace('\n', '')
    
    def do_set_FFT_vertical_scale(self, scale):
        """
        """
        self._visainstrument.write(':FFTS {}'.format(scale))

    def do_get_FFT_vertical_offset(self):
        """
        """
        return self._visainstrument.query(':FFTO?').replace('\n', '')

    def do_set_FFT_vertical_offset(self, offset):
        """
        """
        self._visainstrument.write(':FFTO {}'.format(offset))
    
    def do_get_FFT_max_span(self):
        """
        """
        return self._visainstrument.query(':FFTMAXSPAN?').replace('\n', '')
    
    def do_get_FFT_span(self):
        """
        """
        return self._visainstrument.query(':FFTSPAN?').replace('\n', '')
    
    def do_set_FFT_span(self, span):
        """
        """
        self._visainstrument.write(':FFTSPAN {}'.format(span))
    
    def do_get_FFT_averaging(self):
        """
        """
        return self._visainstrument.query(':FFTA?').replace('\n', '')
    
    def do_set_FFT_averaging(self, averaging):
        """
        """
        self._visainstrument.write(':FFTA {}'.format(averaging))
    
    def do_get_FFT_graph(self):
        """
        """
        return self._visainstrument.query(':FFTL?').replace('\n', '')
    
    def do_set_FFT_graph(self, paused):
        """
        """
        self._visainstrument.write(':FFTL {}'.format(paused))
    
    def do_get_FFT_cursor_width(self):
        """
        """
        return self._visainstrument.query(':FCRW?').replace('\n', '')

    def do_set_FFT_cursor_width(self, width):
        """
        """
        self._visainstrument.write(':FCRW {}'.format(width))
    
    def do_get_FFT_cursor_frequency(self):
        """
        """
        return self._visainstrument.query(':FCRX?').replace('\n', '')
    
    def do_set_FFT_cursor_frequency(self, frequency):
        """
        """
        self._visainstrument.write(':FCRX {}'.format(frequency))
    
    def do_get_FFT_cursor_amp(self):
        """
        """
        return self._visainstrument.query(':FCRY?').replace('\n', '')

    def do_get_scan_param(self):
        """
        """
        return self._visainstrument.query(':SCNPAR?').replace('\n', '')
    
    def do_set_scan_param(self, param):
        """
        """
        self._visainstrument.write(':SCNPAR {}'.format(param))
    
    def do_get_scan_type(self):
        """
        """
        return self._visainstrument.query(':SCNLOG?').replace('\n', '')
    
    def do_set_scan_type(self, setting):
        """
        """
        self._visainstrument.write(':SCNLOG {}'.format(setting))
    
    def do_get_scan_end_mode(self):
        """
        """
        return self._visainstrument.query(':SCNEND?').replace('\n', '')
    
    def do_set_scan_end_mode(self, mode):
        """
        """
        self._visainstrument.write(':SCNEND {}'.format(mode))
    
    def do_get_scan_time(self):
        """
        """
        return self._visainstrument.query(':SCNSEC?').replace('\n', '')
    
    def do_set_scan_time(self, time):
        """
        """
        self._visainstrument.write(':SCNSEC {}'.format(time))
    
    def do_get_scan_out_attenuator_op_mode_sine_out_amp(self):
        """
        """
        return self._visainstrument.query(':SCNAMPATTN?').replace('\n', '')
    
    def do_set_scan_out_attenuator_op_mode_sine_out_amp(self, mode):
        """
        """
        self._visainstrument.write(':SCNAMPATTN {}'.format(mode))
    
    def do_get_scan_out_attenuator_op_mode_dc_level(self):
        """
        """
        return self._visainstrument.query(':SCNDCATTN?').replace('\n', '')
    
    def do_set_scan_out_attenuator_op_mode_dc_level(self, mode):
        """
        """
        self._visainstrument.query(':SCNDCATTN {}'.format(mode))
    
    def do_get_scan_param_update_interval(self):
        """
        """
        return self._visainstrument.query(':SCNINRVL?').replace('\n', '')
    
    def do_set_scan_param_update_interval(self, interval):
        """
        """
        self._visainstrument.write(':SCNINRVL {}'.format(interval))
    
    def do_get_scan_enabled(self):
        """
        """
        return self._visainstrument.query(':SCNENBL?').replace('\n', '')
    
    def do_set_scan_enabled(self, enabled):
        """
        """
        self._visainstrument.write(':SCNENBL {}'.format(enabled))
    
    def do_get_scan_state(self):
        """
        """
        return self._visainstrument.query(':SCNSTATE?').replace('\n', '')
    
    def do_get_scan_freq(self):
        """
        """
        return self._visainstrument.query(':SCNFREQ?').replace('\n', '')
    
    def do_set_scan_freq(self, freq):
        """
        """
        self._visainstrument.write(':SCNFREQ {}'.format(freq))
    
    def do_get_scan_amp(self):
        """
        """
        return self._visainstrument.query(':SCNAMP?').replace('\n', '')
    
    def do_set_scan_amp(self, amp):
        """
        """
        self._visainstrument.write(':SCNAMP {}'.format(amp))
    
    def do_get_scan_ref_dc_level(self):
        """
        """
        return self._visainstrument.query(':SCNDC?').replace('\n', '')
    
    def do_set_scan_ref_dc_level(self, level):
        """
        """
        self._visainstrument.write(':SCNDC {}'.format(level))
    
    def do_get_scan_aux_out_1_level(self):
        """
        """
        return self._visainstrument.query(':SCNAUX1?').replace('\n', '')
    
    def do_set_scan_aux_out_1_level(self, level):
        """
        """
        self._visainstrument.write(':SCNAUX1 {}'.format(level))
    
    def do_get_scan_aux_out_2_level(self):
        """
        """
        return self._visainstrument.query(':SCNAUX2?').replace('\n', '')
    
    def do_set_scan_aux_out_2_level(self, level):
        """
        """
        self._visainstrument.write(':SCNAUX2 {}'.format(level))

    def auto_phase(self):
        """
        Performs the Auto Phase function. This command is the same as pressing the [Auto Phase] key. The outputs may take many time constants to reach their new values. Do not send the command again without waiting the appropriate amount of time.

        Input:
                None

        Output:
                None
        """
        self._visainstrument.write(':APHS')

    def auto_range(self):
        """
        Performs the Auto Range function. This command is the same as pressing the [Auto Range] key. The outputs may take many time constants to return to their steady-state values.

        Input:
                None
        
        Output:
                None
        """
        self._visainstrument.write(':ARNG')
    
    def auto_scale(self):
        """
        Performs the Auto Scale function. This command is the same as pressing the [Auto Scale] key. This automatically sets the sensitivity. Measurements with the synchronous filter on or measurements of Xnoise or Ynoise may take many time constants to return to their steady-state values.

        Input:
                None
        
        Output:
                None
        """
        self._visainstrument.write(':ASCL')
    
    def screenshot(self):
        """
        """
        self._visainstrument.write(':DCAP')
    
    #def get_screen(self):
        """
        """
        # ...
    
    def channel_auto_scale(self, channel):
        """
        """
        self._visainstrument.write(':GAUT {}'.format(channel))
    
    def channel_auto_scale_zero_center(self, channel):
        """
        """
        self._visainstrument.write(':GACT {}'.format(channel))
    
    def channel_auto_find(self, channel):
        """
        """
        self._visainstrument.write(':GAUF {}'.format(channel))
    
    def FFT_auto_scale(self):
        """
        """
        self._visainstrument.write(':FAUT')
    
    def start_scan(self):
        """
        """
        self._visainstrument.write(':SCNRUN')
    
    def pause_scan(self):
        """
        """
        self._visainstrument.write(':SCNPAUSE')
    
    def reset_scan(self):
        """
        """
        self._visainstrument.write(':SCNRST')
