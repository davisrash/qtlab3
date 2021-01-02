from source.instrument import Instrument
import visa

#################################
# To Do:
#  - Fix the preset commands
#     - frequency_preset,
#     - sine_out_amplitude_preset, and
#     - sine_out_dc_level_preset,
#    to work with multiple arguments.
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
        self.add_parameter('assign_param_to_channel', type=(int, int),
                           flags=Instrument.FLAG_GETSET,
                           minval=(0, 0), maxval=(3, 16))

        # auto functions
        self.add_function('auto_phase')
        self.add_function('auto_range')
        self.add_function('auto_scale')

        # display functions
        self.add_function('screenshot')

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
