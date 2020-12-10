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

        # signal commands
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

        # reference functions
        self.add_function('auto_phase_shift')

    def do_get_timebase_mode(self):
        """
        Queries the current external 10 MHz timebase mode (auto (0) or internal (1)).

        Input:
                None

        Output:
                mode (int) : timebase mode
        """
        return self._visainstrument.query(':TBMODE?').replace('\n', '')

    def do_set_timebase_mode(self, mode):
        """
        Sets the external 10 MHz timebase mode (auto (0) or internal (1)).

        Input:
                mode (int) : timebase mode

        Output:
                None
        """
        self._visainstrument.write(':TBMODE {}'.format(mode))

    def do_get_timebase_source(self):
        """
        Queries the current 10 MHz timebase source (external (0) or internal (1)).

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
        return self._visainstrument.query(':HARMDUAL?').replace('\n', '')

    def do_set_external_frequency_harmonic_detect_dual_reference(self, harmonic):
        self._visainstrument.write(':HARMDUAL {}'.format(harmonic))

    def do_get_external_SR540_chopper_blade_slots(self):
        return self._visainstrument.query(':BLADESLOTS?').replace('\n', '')

    def do_set_external_SR540_chopper_blade_slots(self, slots):
        self._visainstrument.write(':BLADESLOTS {}'.format(slots))

    def do_get_external_SR540_chopper_phase(self):
        return self._visainstrument.query(':BLADEPHASE?').replace('\n', '')

    def do_set_external_SR540_chopper_phase(self, phase):
        self._visainstrument.write(':BLADEPHASE {}'.format(phase))

    def do_get_sine_out_amplitude(self):
        return self._visainstrument.query(':SLVL?').replace('\n', '')

    def do_set_sine_out_amplitude(self, amplitude):
        self._visainstrument.write(':SLVL {}'.format(amplitude))

    def do_get_sine_out_dc_level(self):
        return self._visainstrument.query(':SOFF?').replace('\n', '')

    def do_set_sine_out_dc_level(self, level):
        self._visainstrument.write(':SOFF {}'.format(level))

    def do_get_sine_out_dc_mode(self):
        return self._visainstrument.query(':REFM?').replace('\n', '')

    def do_set_sine_out_dc_mode(self, mode):
        self._visainstrument.write(':REFM {}'.format(mode))

    def do_get_reference_source(self):
        return self._visainstrument.query(':RSRC?').replace('\n', '')

    def do_set_reference_source(self, source):
        self._visainstrument.write(':RSRC {}'.format(source))

    def do_get_external_reference_trigger_mode(self):
        return self._visainstrument.query(':RTRG?').replace('\n', '')

    def do_set_external_reference_trigger_mode(self, mode):
        self._visainstrument.write(':RTRG {}'.format(mode))

    def do_get_external_reference_trigger_input(self):
        return self._visainstrument.query(':REFZ?').replace('\n', '')

    def do_set_external_reference_trigger_input(self, resistance):
        self._visainstrument.write(':REFZ {}'.format(resistance))

    def do_get_frequency_preset(self):
        return self._visainstrument.query(':PSTF? 0').replace('\n', '')

    def do_set_frequency_preset(self, frequency):
        self._visainstrument.write(':PSTF 0, {}'.format(frequency))

    def do_get_sine_out_amplitude_preset(self):
        return self._visainstrument.query(':PSTA? 0').replace('\n', '')

    def do_set_sine_out_amplitude_preset(self, amplitude):
        self._visainstrument.write(':PSTA 0, {}'.format(amplitude))

    def do_get_sine_out_dc_level_preset(self):
        return self._visainstrument.query(':PSTL? 0').replace('\n', '')

    def do_set_sine_out_dc_level_preset(self, level):
        self._visainstrument.write(':PSTL 0, {}'.format(level))

    def do_get_signal_input(self):
        return self._visainstrument.query(':IVMD?').replace('\n', '')

    def do_set_signal_input(self, input):
        self._visainstrument.write(':IVMD {}'.format(input))

    def do_get_voltage_input_mode(self):
        return self._visainstrument.query(':ISRC?').replace('\n', '')

    def do_set_voltage_input_mode(self, mode):
        self._visainstrument.write(':ISRC {}'.format(mode))

    def do_get_voltage_input_coupling(self):
        return self._visainstrument.query(':ICPL?').replace('\n', '')

    def do_set_voltage_input_coupling(self, coupling):
        self._visainstrument.write(':ICPL {}'.format(coupling))

    def do_get_voltage_input_shields(self):
        return self._visainstrument.query(':IGND?').replace('\n', '')

    def do_set_voltage_input_shields(self, shields):
        self._visainstrument.write(':IGND {}'.format(shields))

    def do_get_voltage_input_range(self):
        return self._visainstrument.query(':IRNG?').replace('\n', '')

    def do_set_voltage_input_range(self, range):
        self._visainstrument.write(':IRNG {}'.format(range))

    ############

    def auto_phase_shift(self):
        """
        Performs the Auto Phase function. This command is the same as pressing the [Auto Phase] key. The outputs will take many time constants to reach their new values. Do not send the command again without waiting the appropriate amount of time.

        Input:
                None

        Output:
                None
        """
        self._visainstrument.write(':APHS')
