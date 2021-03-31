"""
add docstring
"""

import visa
from source.instrument import Instrument

import logging

###############################################################################
# To Do:
#  - add logging
#  - add doc options
#  - find minval and maxval for
#     - blade_phase
#     - equivalent_noise_bandwidth
#  - consider flags=Instrument.FLAG_GETSET | Instrument.FLAG_GET_AFTER_SET
###############################################################################


class SR860(Instrument):
    """
    Creates a new Instrument to interact with the SR860.

    Usage:
    Initialize with
    <name> = qt.instruments.create('<name>', 'SR860', address='<GPIB address>',
                                   reset=<bool>)
    """

    def __init__(self, name: str, address: str, reset: bool = False):
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
        self.add_parameter('timebase_mode', type=str,
                           flags=Instrument.FLAG_GETSET,
                           doc="The TBMODE i command sets the external 10 MHz"
                               "timebase mode to auto (i = 0) or internal (i ="
                               "1).",
                           format_map={0: 'auto', 1: 'internal'})
        self.add_parameter('timebase_source', type=str,
                           flags=Instrument.FLAG_GET,
                           doc="The TBSTAT? query returns the current 10 MHz"
                               "timebase source, either external (0) or"
                               "internal (1).",
                           format_map={0: 'external', 1: 'internal'})
        self.add_parameter('phase_shift', type=tuple,
                           flags=Instrument.FLAG_GETSET,
                           minval=-360000, maxval=360000,  # units='DEG',
                           format='%.7f',
                           doc="The PHAS p command sets the reference phase"
                               "shift to p degrees. The value of p is set with"
                               "a resolution of ~0.0000001°. The phase may be"
                               "programmed from -360000° ≤ p ≤ 360000° and"
                               "will be wrapped around at ±180°. For example,"
                               "the PHAS 541.0 command will set the phase to"
                               "-179.00° (541 - 360 = 181; 181 - 360 = -179)."
                               "Phase may be specified in degrees (default),"
                               "or millidegrees, microdegrees, radians,"
                               "milliradians, or microradians.")
        self.add_parameter('frequency', type=float,
                           flags=Instrument.FLAG_GETSET,
                           minval=1e-3, maxval=500e6, units='HZ',
                           doc="")
        self.add_parameter('internal_frequency', type=float,
                           flags=Instrument.FLAG_GETSET,
                           minval=1e-3, maxval=500e6, units='Hz',
                           doc="")
        self.add_parameter('external_frequency', type=float,
                           flags=Instrument.FLAG_GET,
                           minval=1e-3, maxval=500e6, units='Hz',
                           doc="")
        self.add_parameter('detection_frequency', type=float,
                           flags=Instrument.FLAG_GET,
                           minval=1e-3, maxval=500e6, units='Hz',
                           doc="")
        self.add_parameter('harmonic_detect', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=1, maxval=99,
                           doc="")
        self.add_parameter('harmonic_detect_dual_reference', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=1, maxval=99,
                           doc="")
        self.add_parameter('blade_slots', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=1,
                           doc="",
                           format_map={0: '6-slot', 1: '30-slot'})
        self.add_parameter('blade_phase', type=float,
                           flags=Instrument.FLAG_GETSET,
                           # minval=?, maxval=?,
                           units='deg',
                           doc="")
        self.add_parameter('sine_out_amplitude', type=float,
                           flags=Instrument.FLAG_GETSET,
                           minval=1e-9, maxval=2.0, units='V',
                           doc="")
        self.add_parameter('sine_out_dc_level', type=float,
                           flags=Instrument.FLAG_GETSET,
                           minval=-5.0, maxval=5.0, units='V',
                           doc="")
        self.add_parameter('sine_out_dc_mode', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=1,
                           doc="",
                           format_map={0: 'common', 1: 'difference'})
        self.add_parameter('reference_source', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=3,
                           doc="",
                           format_map={0: 'internal',
                                       1: 'external',
                                       2: 'dual',
                                       3: 'chop'})
        self.add_parameter('external_reference_trigger_mode', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=2,
                           doc="",
                           format_map={0: 'sine',
                                       1: 'positive TTL',
                                       2: 'negative TTL'})
        self.add_parameter('external_reference_trigger_input', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=1, units='Ω',
                           doc="",
                           format_map={0: '50 Ω', 1: '1 MΩ'})
        self.add_parameter('frequency_preset', type=float,
                           flags=Instrument.FLAG_GETSET,
                           minval=1e-3, maxval=500e6, units='Hz',
                           doc="")
        self.add_parameter('sine_out_amplitude_preset', type=float,
                           flags=Instrument.FLAG_GETSET,
                           minval=1e-9, maxval=2.0, units='V',
                           doc="")
        self.add_parameter('sine_out_dc_level_preset', type=float,
                           flags=Instrument.FLAG_GETSET,
                           minval=-5.0, maxval=5.0, units='V',
                           doc="")

        # signal parameters
        self.add_parameter('signal_input', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=1,
                           doc="",
                           format_map={0: 'voltage', 1: 'current'})
        self.add_parameter('voltage_input_mode', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=1,
                           doc="",
                           format_map={0: 'A', 1: 'A-B'})
        self.add_parameter('voltage_input_coupling', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=1,
                           doc="",
                           format_map={0: 'AC', 1: 'DC'})
        self.add_parameter('voltage_input_shields', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=1,
                           doc="",
                           format_map={0: 'float', 1: 'ground'})
        self.add_parameter('voltage_input_range', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=4,
                           doc="",
                           format_map={0: '1 V',
                                       1: '300 mV',
                                       2: '100 mV',
                                       3: '30 mV',
                                       4: '10 mV'})
        self.add_parameter('current_input_gain', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=1,
                           doc="",
                           format_map={0: '1 MΩ (1 μA)', 1: '100 MΩ (10 nA)'})
        self.add_parameter('signal_strength', type=int,
                           flags=Instrument.FLAG_GET,
                           minval=0, maxval=4,
                           doc="",
                           format_map={0: 'lowest',
                                       1: 'low',
                                       2: 'medium',
                                       3: 'high',
                                       4: 'overload'})
        self.add_parameter('sensitivity', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=27,
                           doc="",
                           format_map={0: '1 V [μA]',
                                       1: '500 mV [nA]',
                                       2: '200 mV [nA]',
                                       3: '100 mV [nA]',
                                       4: '50 mV [nA]',
                                       5: '20 mV [nA]',
                                       6: '10 mV [nA]',
                                       7: '5 mV [nA]',
                                       8: '2 mV [nA]',
                                       9: '1 mV [nA]',
                                       10: '500 μV [pA]',
                                       11: '200 μV [pA]',
                                       12: '100 μV [pA]',
                                       13: '50 μV [pA]',
                                       14: '20 μV [pA]',
                                       15: '10 μV [pA]',
                                       16: '5 μV [pA]',
                                       17: '2 μV [pA]',
                                       18: '1 μV [pA]',
                                       19: '500 nV [fA]',
                                       20: '200 nV [fA]',
                                       21: '100 nV [fA]',
                                       22: '50 nV [fA]',
                                       23: '20 nV [fA]',
                                       24: '10 nV [fA]',
                                       25: '5 nV [fA]',
                                       26: '2 nV [fA]',
                                       27: '1 nV [fA]'})
        self.add_parameter('time_constant', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=21,
                           doc="",
                           format_map={0: '1 μs',
                                       1: '3 μs',
                                       2: '10 μs',
                                       3: '30 μs',
                                       4: '100 μs',
                                       5: '300 μs',
                                       6: '1 ms',
                                       7: '3 ms',
                                       8: '10 ms',
                                       9: '30 ms',
                                       10: '100 ms',
                                       11: '300 ms',
                                       12: '1 s',
                                       13: '3 s',
                                       14: '10 s',
                                       15: '30 s',
                                       16: '100 s',
                                       17: '300 s',
                                       18: '1 ks',
                                       19: '3 ks',
                                       20: '10 ks',
                                       21: '30 ks'})
        self.add_parameter('filter_slope', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=3,
                           doc="",
                           format_map={0: '6 dB/oct',
                                       1: '12 dB/oct',
                                       2: '18 dB/oct',
                                       3: '24 dB/oct'})
        self.add_parameter('synchronous_filter', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=1,
                           doc="",
                           format_map={0: 'off', 1: 'on'})
        self.add_parameter('advanced_filter', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=1,
                           doc="",
                           format_map={0: 'off', 1: 'on'})
        self.add_parameter('equivalent_noise_bandwidth', type=float,
                           flags=Instrument.FLAG_GET,
                           # minval=?, maxval=?
                           units='Hz',
                           doc="")

        # ch1/ch2 output parameters
        self.add_parameter('output_channel', type=int,
                           flags=Instrument.FLAG_GETSET,
                           channels=(0, 1),
                           minval=0, maxval=1,
                           doc="",
                           format_map={0: 'XY', 1: 'Rθ'})
        self.add_parameter('output_expand', type=int,
                           flags=Instrument.FLAG_GETSET,
                           channels=(0, 2),
                           minval=0, maxval=2,
                           doc="",
                           format_map={0: 'off', 1: 'x10', 2: 'x100'})
        self.add_parameter('output_offset', type=int,
                           flags=Instrument.FLAG_GETSET,
                           channels=(0, 2),
                           minval=0, maxval=1,
                           doc="",
                           format_map={0: 'off', 1: 'on'})
        self.add_parameter('output_offset_percentage', type=float,
                           flags=Instrument.FLAG_GETSET,
                           channels=(0, 2),
                           minval=-999.99, maxval=999.99,
                           doc="")
        self.add_parameter('ratio_function', type=int,
                           flags=Instrument.FLAG_GETSET,
                           channels=(0, 2),
                           minval=0, maxval=1,
                           doc="",
                           format_map={0: 'off',
                                       1: 'on'})

        # aux input and output commands
        self.add_parameter('aux_input_voltage', type=int,
                           flags=Instrument.FLAG_GET,
                           minval=0, maxval=3,
                           doc="")
        self.add_parameter('aux_output_voltage', type=float,
                           flags=Instrument.FLAG_GETSET,
                           channels=(0, 3),
                           minval=-10.5, maxval=10.5, units='V',
                           doc="")

        # display parameters
        self.add_parameter('front_panel_blanking', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=1,
                           doc="",
                           format_map={0: 'off',
                                       1: 'on'})
        self.add_parameter('screen_layout', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=5,
                           doc="",
                           format_map={0: 'trend',
                                       1: 'full strip chart history',
                                       2: 'half strip chart history',
                                       3: 'full FFT',
                                       4: 'half FFT',
                                       5: 'big numerical'})
        self.add_parameter('channel_param', type=int,
                           flags=Instrument.FLAG_GETSET,
                           channels=(0, 3),
                           minval=0, maxval=16,
                           doc="",
                           format_map={0: 'X output',
                                       1: 'Y output',
                                       2: 'R output',
                                       3: 'θ output',
                                       4: 'Aux In1',
                                       5: 'Aux In2',
                                       6: 'Aux In3',
                                       7: 'Aux In4',
                                       8: 'Xnoise',
                                       9: 'Ynoise',
                                       10: 'Aux Out1',
                                       11: 'Aux Out2',
                                       12: 'reference phase',
                                       13: 'sine out amplitude',
                                       14: 'DC level',
                                       15: 'internal reference frequency',
                                       16: 'external reference frequency'})
        self.add_parameter('channel_strip_chart_graph',
                           #type=(int, int),
                           flags=Instrument.FLAG_GETSET,
                           # minval=(0, 0), maxval=(3, 1)
                           )

        # strip chart parameters
        self.add_parameter('horizontal_time_scale', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=16)
        self.add_parameter('channel_vertical_scale',
                           #type=(int, float),
                           flags=Instrument.FLAG_GETSET,
                           # minval=(0, 0+), maxval=(3, x)  unknown max
                           )
        self.add_parameter('channel_vertical_offset',
                           #type=(int, float),
                           flags=Instrument.FLAG_GETSET,
                           # minval=(0, -x), maxval=(3, x)  unknown range
                           )
        self.add_parameter('channel_graph',
                           #type=(int, int),
                           flags=Instrument.FLAG_GETSET,
                           # minval=(0, 0), maxval=(3, 1)
                           )
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
        self.add_parameter('channel_strip_chart_cursor_value',
                           #type=(int, float),
                           flags=Instrument.FLAG_GET,
                           # minval=(0, -x), maxval=(4, x)  unknown range
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
                           # minval=?, maxval=?  unknown range
                           )
        self.add_parameter('FFT_max_span', type=float,
                           flags=Instrument.FLAG_GET)
        self.add_parameter('FFT_span', type=float,
                           flags=Instrument.FLAG_GETSET,
                           # minval=?,  unknown min
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
                           # type=float,  unknown if float or int
                           flags=Instrument.FLAG_GET,
                           # minval=?, maxval=?,  unknown range
                           units='HZ')
        self.add_parameter('FFT_cursor_amp',
                           # type=float,  unknown if float or int
                           flags=Instrument.FLAG_GET,
                           # minval=0, maxval=0  unknown range
                           # units='DB'  valid unit? necessary?
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
                           # minval=0,  minval unknown
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
        self.add_parameter('scan_freq',
                           #type=(int, float),
                           flags=Instrument.FLAG_GETSET,
                           # minval=(0, 1e-3), maxval=(1, 500e3),
                           units='HZ')
        self.add_parameter('scan_amp',
                           #type=(int, float),
                           flags=Instrument.FLAG_GETSET,
                           # minval=(0, 1e-9), maxval=(1, 2),
                           units='V')
        self.add_parameter('scan_ref_dc_level',
                           #type=(int, float),
                           flags=Instrument.FLAG_GETSET,
                           # minval=(0, -5), maxval=(1, 5),
                           units='V')
        self.add_parameter('scan_aux_out_1_level',
                           #type=(int, float),
                           flags=Instrument.FLAG_GETSET,
                           # minval=(0, -10.5), maxval=(1, 10.5),
                           units='V')
        self.add_parameter('scan_aux_out_2_level',
                           #type=(int, float),
                           flags=Instrument.FLAG_GETSET,
                           # minval=(0, -10.5), maxval=(1, 10.5),
                           units='V')

        # data transfer parameters
        self.add_parameter('data_channel_val', type=float,
                           flags=Instrument.FLAG_GET,
                           channels=(0, 3),
                           doc="The OUTR? j query returns the value of data"
                               "channel j.\n\n"
                               "The value of j (0–3) corresponds to the DAT1"
                               "(green), DAT2 (blue), DAT3 (yellow), and DAT4"
                               "(orange) data channels.")
        self.add_parameter('data_param', type=float,
                           flags=Instrument.FLAG_GET,
                           channels=(0, 16),
                           doc="The OUTP? j query returns the value of a"
                               "single lock-in parameter. The argument j"
                               "selects the parameter according to the dict"
                               "below. The enumeration strings may be used"
                               "instead of the integer value j.\n\n"
                               "The parameter list is\n"
                               "j   enumeration parameter\n"
                               "0   X           X output\n"
                               "1   Y           Y output\n"
                               "2   R           R output\n"
                               "3   THeta       θ output\n"
                               "4   IN1         Aux In1\n"
                               "5   IN2         Aux In2\n"
                               "6   IN3         Aux In3\n"
                               "7   IN4         Aux In4\n"
                               "8   XNOise      Xnoise\n"
                               "9   YNOise      Ynoise\n"
                               "10  OUT1        Aux Out1\n"
                               "11  OUT2        Aux Out2\n"
                               "12  PHAse       Reference Phase\n"
                               "13  SAMp        Sine Out Amplitude\n"
                               "14  LEVel       DC Level\n"
                               "15  FInt        Int. Ref. Frequency\n"
                               "16  FExt        Ext. Ref. Frequency\n")
        # self.add_parameter('multi_data_param')
        # self.add_parameter('multi_data_channel')

        # data capture commands
        self.add_parameter('capture_length', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=1, maxval=4096)
        self.add_parameter('capture_config', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=3)
        self.add_parameter('capture_rate_max', type=int,
                           flags=Instrument.FLAG_GET)
        self.add_parameter('capture_rate', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=20)
        self.add_parameter('capture_state', type=int,
                           flags=Instrument.FLAG_GET)
        self.add_parameter('num_bytes_captured', type=int,
                           flags=Instrument.FLAG_GET)
        self.add_parameter('num_kbytes_written', type=float,
                           flags=Instrument.FLAG_GET)
        self.add_parameter('capture_buffer_ascii', type=int,
                           flags=Instrument.FLAG_GET)
        self.add_parameter('capture_buffer_bin',
                           #type=(int, int),
                           flags=Instrument.FLAG_GET)

        # data streaming parameters
        self.add_parameter('stream_config', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=3)
        self.add_parameter('stream_rate_max', type=int,
                           flags=Instrument.FLAG_GET)
        self.add_parameter('stream_rate', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=20)
        self.add_parameter('stream_format', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=1)
        self.add_parameter('stream_packet_size', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=1)
        self.add_parameter('stream_port', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=1)
        self.add_parameter('stream_option', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=1)
        self.add_parameter('stream_enabled', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=1)

        # system parameters
        self.add_parameter('time',
                           #type=(int, int),
                           flags=Instrument.FLAG_GETSET,
                           # minval=(0, 0), maxval=(1, 59) | (2, 23)
                           )
        self.add_parameter('date',
                           #type=(int, int),
                           flags=Instrument.FLAG_GETSET,
                           # minval=(0, 0), maxval=(0, 31) | (1, 12) | (2, 99)
                           )
        # self.add_parameter('') tbmode move from earlier
        # self.add_parameter('') tbstat
        self.add_parameter('BlazeX_output', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=2)
        self.add_parameter('sounds', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=1)
        self.add_parameter('screenshot_mode', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=2)
        self.add_parameter('data_file_format', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=1)
        self.add_parameter('filename_prefix', type=str,
                           flags=Instrument.FLAG_GETSET)
        self.add_parameter('filename_suffix', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0)
        self.add_parameter('next_filename', type=str,
                           flags=Instrument.FLAG_GET)

        # interface parameters
        self.add_parameter('identification', type=str,
                           flags=Instrument.FLAG_GET)
        self.add_parameter('op_complete_bit', type=int,
                           flags=Instrument.FLAG_GETSET)
        self.add_parameter('local_remote', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=2)
        self.add_parameter('GPIB_override_remote', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=1)

        # status reporting parameters
        self.add_parameter('standard_event_enable_register',
                           #type=(int, int),
                           flags=Instrument.FLAG_GETSET,
                           # minval=(0, 0), maxval=(1, 7)
                           )
        self.add_parameter('standard_event_status_byte', type=int,
                           flags=Instrument.FLAG_GET,
                           minval=0, maxval=255)
        self.add_parameter('serial_poll_enable_register',
                           #type=(int, int),
                           flags=Instrument.FLAG_GETSET,
                           # minval=(0, 0), maxval=(1, 7)
                           )
        self.add_parameter('serial_poll_status_byte', type=int,
                           flags=Instrument.FLAG_GET,
                           minval=0, maxval=255)
        self.add_parameter('power_on_status_clear_bit', type=int,
                           flags=Instrument.FLAG_GETSET,
                           minval=0, maxval=1)
        self.add_parameter('error_status_enable_register',
                           #type=(int, int),
                           flags=Instrument.FLAG_GETSET,
                           # minval=(0, 0), maxval=(1, 7)
                           )
        self.add_parameter('error_status_byte',
                           # type=(int, int), # different types
                           flags=Instrument.FLAG_GET,
                           # minval=(0, 0), maxval=(1, 7)
                           )
        self.add_parameter('LIA_status_enable_register',
                           #type=(int, int),
                           flags=Instrument.FLAG_GETSET,
                           # minval=(0, 0), maxval=(1, 11)
                           )
        self.add_parameter('LIA_status_word',
                           # type=int,
                           flags=Instrument.FLAG_GET,
                           # minval=0, maxval=1
                           )
        self.add_parameter('overload_states', type=int,
                           flags=Instrument.FLAG_GET,
                           minval=0, maxval=4095)

        # auto functions
        self.add_function('auto_offset')
        self.add_function('auto_phase')
        self.add_function('auto_range')
        self.add_function('auto_scale')

        # display functions
        self.add_function('screenshot')
        # self.add_function('get_screen')

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

        # data transfer functions
        self.add_function('get_multi_params')
        self.add_function('get_data_params')

        # data capture functions
        self.add_function('start_capture')
        self.add_function('stop_capture')

        # system functions
        # self.add_function('screenshot')
        self.add_function('save_data')

        # interface functions
        self.add_function('reset')
        self.add_function('test')

        # status reporting functions
        self.add_function('clear')

        if reset:
            self.reset()

    def do_get_timebase_mode(self):
        """
        Queries the current external 10 MHz timebase mode. Returns either
        'auto' (0) or 'internal' (1).

        Input:
                None

        Output:
                mode (str) : timebase mode
        """
        return self.get_parameters()['timebase_mode']['format_map']\
            [int(self._visainstrument.query('TBMODE?').replace('\n', ''))]

    def do_set_timebase_mode(self, mode: str):
        """
        Sets the external 10 MHz timebase mode to either 'auto' (0) or
        'internal' (1).

        Input:
                mode (str) : timebase mode

        Output:
                None
        """
        self._visainstrument.write('TBMODE {}'.format(mode))

    def do_get_timebase_source(self):
        """
        Queries the current 10 MHz timebase source. Returns either 'external'
        (0) or 'internal' (1).

        Input:
                None

        Output:
                source (str) : timebase source
        """
        return self.get_parameters()['timebase_source']['format_map']\
            [int(self._visainstrument.query('TBSTAT?').replace('\n', ''))]

    def do_get_phase_shift(self):
        """
        Queries the current reference phase shift. The phase shift has a
        resolution of ~0.0000001° and is wrapped around at ±180°.

        Input:
                None

        Output:
                phase (float) : reference phase shift in degrees
        """
        return self._visainstrument.query('PHAS?')  # .replace('\n', '')

    def do_set_phase_shift(self, phase: float, units: str = 'DEG'):
        """
        Sets the reference phase shift. The phase shift has a resolution of
        ~0.0000001° and is wrapped around at ±180°.

        Input:
                phase (float) : reference phase shift
                units (str)   : units of reference phase shift

        Output:
                None
        """
        if units not in ['UDEG', 'MDEG', 'DEG', 'URAD', 'MRAD', 'RAD']:
            #logging.warning(
            #    'Unsupported unit \'{}\'. Allowed units are {}'.#format(units, 'unit list'))
            raise ValueError()

        self._visainstrument.write('PHAS {} {}'.format(phase, units))

    def do_get_frequency(self):
        """
        Queries the current internal reference frequency whenever the reference
        mode is one of Internal, Dual, or Chop. Otherwise, in External mode,
        the query returns the external reference frequency. This behavior
        mirrors the value displayed in the info bar at the top of the display.

        Input:
                None

        Output:
                frequency (float) : internal or external reference frequency in
                hertz
        """
        return self._visainstrument.query(':FREQ?')

    def do_set_frequency(self, frequency):
        """
        Sets the internal reference frequency. The frequency will be rounded to
        6 digits or 0.1 mHz, whichever is greater.

        Input:
                frequency (float) : internal frequency in hertz
        Output:
                None
        """
        self._visainstrument.write(':FREQ {}'.format(frequency))

    def do_get_internal_frequency(self):
        """
        Queries the current internal reference frequency.

        Input:
                None

        Output:
                frequency (float) : internal frequency in hertz
        """
        return self._visainstrument.query(':FREQINT?')

    def do_set_internal_frequency(self, frequency):
        """
        Sets the internal reference frequency. The frequency will be rounded to
        6 digits or 0.1 mHz, whichever is greater.

        Input:
                frequency (float) : internal frequency in hertz

        Output:
                None
        """
        self._visainstrument.write(':FREQINT {}'.format(frequency))

    def do_get_external_frequency(self):
        """
        Queries the current external reference frequency.

        Input:
                None

        Output:
                frequency (float) : external reference frequency in hertz
        """
        return self._visainstrument.query(':FREQEXT?')

    def do_get_detection_frequency(self):
        """
        Queries the current detection frequency. This is helpful in dual
        reference mode or harmonic detection. Otherwise, the detection
        frequency is either the internal or external reference frequency.

        Input:
                None

        Output:
                frequency (float) : detection frequency in hertz
        """
        return self._visainstrument.query(':FREQDET?')

    def do_get_harmonic_detect(self):
        """
        Queries the harmonic number of the reference frequency.

        Input:
                None

        Output:
                harmonic (int) : harmonic number of the reference frequency
        """
        return self._visainstrument.query(':HARM?')

    def do_set_harmonic_detect(self, harmonic):
        """
        Sets the lock-in to detect at the given harmonic of the reference
        frequency.

        Input:
                harmonic (int) : harmonic number of the reference frequency

        Output:
                None
        """
        self._visainstrument.write(':HARM {}'.format(harmonic))

    def do_get_harmonic_detect_dual_reference(self):
        """
        Queries the harmonic number of the external frequency in dual reference
        mode.

        Input:
                None

        Output:
                harmonic (int) : harmonic number of the external reference
                frequency in dual reference mode
        """
        return self._visainstrument.query(':HARMDUAL?')

    def do_set_harmonic_detect_dual_reference(self, harmonic):
        """
        Sets the lock-in to detect at the given harmonic of the external
        frequency in dual reference mode.

        Input:
                harmonic (int) : harmonic number of the external reference
                frequency in dual reference mode

        Output:
                None
        """
        self._visainstrument.write(':HARMDUAL {}'.format(harmonic))

    def do_get_blade_slots(self):
        """
        Queries the blade slots setting for operation with an external SR540
        chopper. Returns either 6-slot (0) or 30-slot (1).

        Input:
                None

        Output:
                slots (int) : blade slot setting
        """
        return self._visainstrument.query(':BLADESLOTS?')

    def do_set_blade_slots(self, slots):
        """
        Configures the SR860 for either 6-slot (0) or 30-slot (1) operation
        with an external SR540 chopper.

        Input:
                slots (int) : blade slot setting

        Output:
                None
        """
        self._visainstrument.write(':BLADESLOTS {}'.format(slots))

    def do_get_blade_phase(self):
        """
        Queries the current phase of an external SR540 chopper blade, or, with
        multiple choppers, the relative phase of the choppers.

        Input:
                None

        Output:
                phase (float) : blade phase in degrees
        """
        return self._visainstrument.query(':BLADEPHASE?')

    def do_set_blade_phase(self, phase):
        """
        Sets the phase of an external SR540 chopper blade. When operating a
        single chopper, this has little effect since the SR860 will follow the
        chopper, but it can modify the relative phase of multiple choppers in a
        single experiment.

        Input:
                phase (float) : blade phase in degrees

        Output:
                None
        """
        self._visainstrument.write(':BLADEPHASE {}'.format(phase))

    def do_get_sine_out_amplitude(self):
        """
        Queries the current sine out amplitude. The amplitude will be rounded
        to 3 digits or 1 nV, whichever is greater.

        Input:
                None

        Output:
                amplitude (float) : sine out amplitude in volts
        """
        return self._visainstrument.query(':SLVL?')

    def do_set_sine_out_amplitude(self, amplitude):
        """
        Sets the sine out amplitude. The amplitude will be rounded to 3 digits
        or 1 nV, whichever is greater.

        Input:
                amplitude (float) : sine out amplitude in volts

        Output:
                None
        """
        self._visainstrument.write(':SLVL {}'.format(amplitude))

    def do_get_sine_out_dc_level(self):
        """
        Queries the current sine out DC level. The DC level will be rounded to
        3 digits or 0.1 mV, whichever is greater.

        Input:
                None

        Output:
                level (float) : sine out DC level in volts
        """
        return self._visainstrument.query(':SOFF?')

    def do_set_sine_out_dc_level(self, level):
        """
        Sets the sine out DC level. The DC level will be rounded to 3 digits or
        0.1 mV, whichever is greater.

        Input:
                level (float) : sine out DC level in volts

        Output:
                None
        """
        self._visainstrument.write(':SOFF {}'.format(level))

    def do_get_sine_out_dc_mode(self):
        """
        Queries the current sine out DC mode. Returns either common (0) or
        difference (1).

        Input:
                None

        Output:
                mode (int) : sine out DC mode
        """
        return self._visainstrument.query(':REFM?')

    def do_set_sine_out_dc_mode(self, mode):
        """
        Sets the sine out DC mode to either common (0) or difference (1).

        Input:
                mode (int) : sine out DC mode

        Output:
                None
        """
        self._visainstrument.write(':REFM {}'.format(mode))

    def do_get_reference_source(self):
        """
        Queries the current reference source. Returns one of internal (0),
        external (1), dual (2), and chop (3).

        Input:
                None

        Output:
                source (int) : reference source
        """
        return self._visainstrument.query(':RSRC?')

    def do_set_reference_source(self, source):
        """
        Sets the reference source to one of internal (0), external (1), dual
        (2), and chop (3).

        Input:
                source (int) : reference source

        Output:
                None
        """
        self._visainstrument.write(':RSRC {}'.format(source))

    def do_get_external_reference_trigger_mode(self):
        """
        Queries the current external reference trigger mode. Returns one of
        sine (0), positive TTL (1), and negative TTL (2).

        Input:
                None

        Output:
                mode (int) : external reference trigger mode
        """
        return self._visainstrument.query(':RTRG?')

    def do_set_external_reference_trigger_mode(self, mode):
        """
        Sets the external reference trigger mode to one of sine (0), positive
        TTL (1), and negative TTL (2).

        Input:
                mode (int) : external reference trigger mode

        Output:
                None
        """
        self._visainstrument.write(':RTRG {}'.format(mode))

    def do_get_external_reference_trigger_input(self):
        """
        Queries the current external reference trigger input. Returns either
        50 Ω (0) or 1 MΩ (1).

        Input:
                None

        Output:
                setting (int) : external reference trigger input
        """
        return self._visainstrument.query(':REFZ?')

    def do_set_external_reference_trigger_input(self, setting):
        """
        Sets the external reference trigger input to either 50 Ω (0) or 1 MΩ
        (1).

        Input:
                setting (int) : external reference trigger input

        Output:
                None
        """
        self._visainstrument.write(':REFZ {}'.format(setting))

    def do_get_frequency_preset(self, preset):
        """
        Queries one of the current frequency presets F1 (0), F2 (1), F3 (2), or
        F4 (3). The frequency will be rounded to 6 digits or 0.1 mHz, whichever
        is greater.

        Input:
                preset (int) : frequency preset selection

        Output:
                frequency (float) : frequency preset in hertz
        """
        return self._visainstrument.query(':PSTF? {}'.format(preset))

    def do_set_frequency_preset(self, frequency, preset):
        """
        Sets one of the frequency presets F1 (0), F2 (1), F3 (2), or F3 (3).
        The frequency will be rounded to 6 digits or 0.1 mHz, whichever is
        greater.

        Input:
                frequency (float) : frequency preset in hretz
                preset (int)      : frequency preset selection

        Output:
                None
        """
        self._visainstrument.write(':PSTF {}, {}'.format(preset, frequency))

    def do_get_sine_out_amplitude_preset(self, preset):
        """
        Queries one of the current sine out amplitude presets A1 (0), A2 (1),
        A3 (2), or A4 (3). The amplitude will be rounded to 3 digits or 1 nV,
        whichever is greater.

        Input:
                preset (int) : sine out amplitude preset selection

        Output:
                amplitude (float) : sine out amplitude preset in volts
        """
        return self._visainstrument.query(':PSTA? {}'.format(preset))

    def do_set_sine_out_amplitude_preset(self, amplitude, preset):
        """
        Sets one of the sine out amplitude presets A1 (0), A2 (1), A3 (2), or
        A4 (3). The amplitude will be rounded to 3 digits or 1 nV, whichever is
        greater.

        Input:
                amplitude (float) : sine out amplitude preset in volts
                preset (int)      : sine out amplitude preset selection

        Output:
                None
        """
        self._visainstrument.write(':PSTA {}, {}'.format(preset, amplitude))

    def do_get_sine_out_dc_level_preset(self, preset):
        """
        Queries one of the current sine out DC level presets L1 (0), L2 (1), L3
        (2), or L4 (3). The DC level will be rounded to 3 digits or 0.1 mV,
        whichever is greater.

        Input:
                preset (int) : sine out DC level preset selection

        Output:
                level (float) : sine out DC level preset in volts
        """
        return self._visainstrument.query(':PSTL? {}'.format(preset))

    def do_set_sine_out_dc_level_preset(self, level, preset):
        """
        Sets one of the sine out DC level presets L1 (0), L2 (1), L3 (2), or L4
        (3). The DC level will be rounded to 3 digits or 0.1 mV, whichever is
        greater.

        Input:
                level (float) : sine out DC level preset in volts
                preset (int)  : sine out DC level preset selection

        Output:
                None
        """
        self._visainstrument.write(':PSTL {}, {}'.format(preset, level))

    def do_get_signal_input(self):
        """
        add docstring
        """
        return self._visainstrument.query(':IVMD?')

    def do_set_signal_input(self, signal):
        """
        add docstring
        """
        self._visainstrument.write(':IVMD {}'.format(signal))

    def do_get_voltage_input_mode(self):
        """
        add docstring
        """
        return self._visainstrument.query(':ISRC?')

    def do_set_voltage_input_mode(self, mode):
        """
        add docstring
        """
        self._visainstrument.write(':ISRC {}'.format(mode))

    def do_get_voltage_input_coupling(self):
        """
        add docstring
        """
        return self._visainstrument.query(':ICPL?')

    def do_set_voltage_input_coupling(self, coupling):
        """
        add docstring
        """
        self._visainstrument.write(':ICPL {}'.format(coupling))

    def do_get_voltage_input_shields(self):
        """
        add docstring
        """
        return self._visainstrument.query(':IGND?')

    def do_set_voltage_input_shields(self, shields):
        """
        add docstring
        """
        self._visainstrument.write(':IGND {}'.format(shields))

    def do_get_voltage_input_range(self):
        """
        add docstring
        """
        return self._visainstrument.query(':IRNG?')

    def do_set_voltage_input_range(self, input_range):
        """
        add docstring
        """
        self._visainstrument.write(':IRNG {}'.format(input_range))

    def do_get_current_input_gain(self):
        """
        Queries the current current input gain. Returns either 0 for 1 MΩ
        (1 μA) or 1 for 100 MΩ (10 nA).

        Input:
                None

        Output:
                gain (int) : current input gain setting
        """
        return self._visainstrument.query(':ICUR?')

    def do_set_current_input_gain(self, gain):
        """
        Sets the current input gain to 1 MΩ (1 μA) for gain == 0 or 100 MΩ
        (10 nA) for gain == 1.

        Input:
                gain (int) : current input gain setting

        Output:
                None
        """
        self._visainstrument.write(':ICUR {}'.format(gain))

    def do_get_signal_strength(self):
        """
        Queries the signal strength indicator. Returns an int between 0 for
        lowest and 4 for overload, inclusive.

        Input:
                None

        Output:
                strength (int) : signal strength indicator
        """
        return self._visainstrument.query(':ILVL?')

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
        return self._visainstrument.query(':SCAL?')

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
        return self._visainstrument.query(':OFLT?')

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
        return self._visainstrument.query(':OFSL?')

    def do_set_filter_slope(self, slope):
        """
        Sets the filter slope to 6 dB/oct for slope == 0, 12 dB/oct for
        slope == 1, 18 dB/oct for slope == 2, or 24 dB/oct for slope == 3.

        Input:
                slope (int) : filter slope setting

        Output:
                None
        """
        self._visainstrument.write(':OFSL {}'.format(slope))

    def do_get_synchronous_filter(self):
        """
        """
        return self._visainstrument.query(':SYNC?')

    def do_set_synchronous_filter(self, setting):
        """
        """
        self._visainstrument.write(':SYNC {}'.format(setting))

    def do_get_advanced_filter(self):
        """
        """
        return self._visainstrument.query(':ADVFILT?')

    def do_set_advanced_filter(self, setting):
        """
        """
        self._visainstrument.write(':ADVFILT {}'.format(setting))

    def do_get_equivalent_noise_bandwidth(self):
        """
        """
        return self._visainstrument.query(':ENBW?')

    def do_get_output_channel(self, channel):
        """
        """
        return self._visainstrument.query(':COUT? {}'.format(channel))

    def do_set_output_channel(self, output, channel):
        """
        Sets either the Channel 1 for channel == 1 or the Channel 2 for
        channel == 2 output mode to either rectangular (XY) for output == 0 or
        polar (Rθ) for output == 1.
        """
        self._visainstrument.write(':COUT {}, {}'.format(channel, output))

    def do_get_output_expand(self, axis):
        """
        """
        return self._visainstrument.query(':CEXP? {}'.format(axis))

    def do_set_output_expand(self, axis, mode):
        """
        """
        self._visainstrument.write(':CEXP {}, {}'.format(axis, mode))

    def do_get_output_offset(self, axis):
        """
        """
        return self._visainstrument.query(':COFA? {}'.format(axis))

    def do_set_output_offset(self, axis, offset):
        """
        """
        self._visainstrument.write(':COFA {}, {}'.format(axis, offset))

    def do_get_output_offset_percentage(self, axis):
        """
        """
        return self._visainstrument.query(':COFP? {}'.format(axis))

    def do_set_output_offset_percentage(self, axis, percentage):
        """
        """
        self._visainstrument.write(':COFP {}, {}'.format(axis, percentage))

    def do_get_ratio_function(self, axis):
        """
        """
        return self._visainstrument.query(':CRAT? {}'.format(axis))

    def do_set_ratio_function(self, axis, mode):
        """
        """
        self._visainstrument.write(':CRAT {}, {}'.format(axis, mode))

    def do_get_aux_input_voltage(self):
        """
        """
        return self._visainstrument.query(':OAUX?')

    def do_get_aux_output_voltage(self, output):
        """
        """
        return self._visainstrument.query(':AUXV? {}'.format(output))

    def do_set_aux_output_voltage(self, output, level):
        """
        """
        self._visainstrument.write(':AUXV {}, {}'.format(output, level))

    def do_get_front_panel_blanking(self):
        """
        """
        return self._visainstrument.query(':DBLK?')

    def do_set_front_panel_blanking(self, setting):
        """
        """
        self._visainstrument.write(':DBLK {}'.format(setting))

    def do_get_screen_layout(self):
        """
        """
        return self._visainstrument.query(':DLAY?')

    def do_set_screen_layout(self, layout):
        """
        """
        self._visainstrument.write(':DLAY {}'.format(layout))

    def do_get_channel_param(self, channel):
        """
        """
        return self._visainstrument.query(':CDSP? {}'.format(channel))

    def do_set_channel_param(self, channel, param):
        """
        """
        self._visainstrument.write(':CDSP {}, {}'.format(channel, param))

    def do_get_channel_strip_chart_graph(self, channel):
        """
        """
        return self._visainstrument.query(':CGRF? {}'.format(channel))

    def do_set_channel_strip_chart_graph(self, channel, setting):
        """
        """
        self._visainstrument.write(':CGRF {}, {}'.format(channel, setting))

    def do_get_horizontal_time_scale(self):
        """
        """
        return self._visainstrument.query(':GSPD?')

    def do_set_horizontal_time_scale(self, scale):
        """
        """
        self._visainstrument.write(':GSPD {}'.format(scale))

    def do_get_channel_vertical_scale(self, channel):
        """
        """
        return self._visainstrument.query(':GSCL? {}'.format(channel))

    def do_set_channel_vertical_scale(self, channel, scale):
        """
        """
        self._visainstrument.write(':GSCL {}, {}'.format(channel, scale))

    def do_get_channel_vertical_offset(self, channel):
        """
        """
        return self._visainstrument.query(':GOFF? {}'.format(channel))

    def do_set_channel_vertical_offset(self, channel, offset):
        """
        """
        self._visainstrument.write(':GOFF {}, {}'.format(channel, offset))

    def do_get_channel_graph(self, channel):
        """
        """
        return self._visainstrument.query(':CGRF? {}'.format(channel))

    def do_set_channel_graph(self, channel, setting):
        """
        """
        self._visainstrument.write(':CGRF {}, {}'.format(channel, setting))

    def do_get_strip_chart(self):
        """
        """
        return self._visainstrument.query(':GLIV?')

    def do_set_strip_chart(self, setting):
        """
        """
        self._visainstrument.write(':GLIV {}'.format(setting))

    def do_get_strip_chart_cursor_pos(self):
        """
        """
        return self._visainstrument.query(':PCUR?')

    def do_set_strip_chart_cursor_pos(self, pos):
        """
        """
        self._visainstrument.write(':PCUR {}'.format(pos))

    def do_get_strip_chart_cursor_mode(self):
        """
        """
        return self._visainstrument.query(':CURREL?')

    def do_set_strip_chart_cursor_mode(self, mode):
        """
        """
        self._visainstrument.write(':CURREL {}'.format(mode))

    def do_get_strip_chart_cursor_display_mode(self):
        """
        """
        return self._visainstrument.query(':CURDISP?')

    def do_set_strip_chart_cursor_display_mode(self, mode):
        """
        """
        self._visainstrument.write(':CURDISP {}'.format(mode))

    def do_get_strip_chart_cursor_readout_mode(self):
        """
        """
        return self._visainstrument.query(':CURBUG?')

    def do_set_strip_chart_cursor_readout_mode(self, mode):
        """
        """
        self._visainstrument.write(':CURBUG {}'.format(mode))

    def do_get_strip_chart_cursor_width(self):
        """
        """
        return self._visainstrument.query(':FCRW?')

    def do_set_strip_chart_cursor_width(self, width):
        """
        """
        self._visainstrument.write(':FCRW {}'.format(width))

    def do_get_channel_strip_chart_cursor_value(self, channel):
        """
        """
        return self._visainstrument.query(':SCRY? {}'.format(channel))

    def do_get_strip_chart_cursor_horizontal_time(self):
        """
        """
        return self._visainstrument.query(':CURDATTIM?')

    def do_get_strip_chart_cursor_horizontal_pos(self):
        """
        """
        return self._visainstrument.query(':CURINTERVAL?')

    def do_get_FFT_source(self):
        """
        """
        return self._visainstrument.query(':FFTR?')

    def do_set_FFT_source(self, source):
        """
        """
        self._visainstrument.write(':FFTR {}'.format(source))

    def do_get_FFT_vertical_scale(self):
        """
        """
        return self._visainstrument.query(':FFTS?')

    def do_set_FFT_vertical_scale(self, scale):
        """
        """
        self._visainstrument.write(':FFTS {}'.format(scale))

    def do_get_FFT_vertical_offset(self):
        """
        """
        return self._visainstrument.query(':FFTO?')

    def do_set_FFT_vertical_offset(self, offset):
        """
        """
        self._visainstrument.write(':FFTO {}'.format(offset))

    def do_get_FFT_max_span(self):
        """
        """
        return self._visainstrument.query(':FFTMAXSPAN?')

    def do_get_FFT_span(self):
        """
        """
        return self._visainstrument.query(':FFTSPAN?')

    def do_set_FFT_span(self, span):
        """
        """
        self._visainstrument.write(':FFTSPAN {}'.format(span))

    def do_get_FFT_averaging(self):
        """
        """
        return self._visainstrument.query(':FFTA?')

    def do_set_FFT_averaging(self, averaging):
        """
        """
        self._visainstrument.write(':FFTA {}'.format(averaging))

    def do_get_FFT_graph(self):
        """
        """
        return self._visainstrument.query(':FFTL?')

    def do_set_FFT_graph(self, paused):
        """
        """
        self._visainstrument.write(':FFTL {}'.format(paused))

    def do_get_FFT_cursor_width(self):
        """
        """
        return self._visainstrument.query(':FCRW?')

    def do_set_FFT_cursor_width(self, width):
        """
        """
        self._visainstrument.write(':FCRW {}'.format(width))

    def do_get_FFT_cursor_frequency(self):
        """
        """
        return self._visainstrument.query(':FCRX?')

    def do_set_FFT_cursor_frequency(self, frequency):
        """
        """
        self._visainstrument.write(':FCRX {}'.format(frequency))

    def do_get_FFT_cursor_amp(self):
        """
        """
        return self._visainstrument.query(':FCRY?')

    def do_get_scan_param(self):
        """
        """
        return self._visainstrument.query(':SCNPAR?')

    def do_set_scan_param(self, param):
        """
        """
        self._visainstrument.write(':SCNPAR {}'.format(param))

    def do_get_scan_type(self):
        """
        """
        return self._visainstrument.query(':SCNLOG?')

    def do_set_scan_type(self, setting):
        """
        """
        self._visainstrument.write(':SCNLOG {}'.format(setting))

    def do_get_scan_end_mode(self):
        """
        """
        return self._visainstrument.query(':SCNEND?')

    def do_set_scan_end_mode(self, mode):
        """
        """
        self._visainstrument.write(':SCNEND {}'.format(mode))

    def do_get_scan_time(self):
        """
        """
        return self._visainstrument.query(':SCNSEC?')

    def do_set_scan_time(self, time):
        """
        """
        self._visainstrument.write(':SCNSEC {}'.format(time))

    def do_get_scan_out_attenuator_op_mode_sine_out_amp(self):
        """
        """
        return self._visainstrument.query(':SCNAMPATTN?')

    def do_set_scan_out_attenuator_op_mode_sine_out_amp(self, mode):
        """
        """
        self._visainstrument.write(':SCNAMPATTN {}'.format(mode))

    def do_get_scan_out_attenuator_op_mode_dc_level(self):
        """
        """
        return self._visainstrument.query(':SCNDCATTN?')

    def do_set_scan_out_attenuator_op_mode_dc_level(self, mode):
        """
        """
        self._visainstrument.query(':SCNDCATTN {}'.format(mode))

    def do_get_scan_param_update_interval(self):
        """
        """
        return self._visainstrument.query(':SCNINRVL?')

    def do_set_scan_param_update_interval(self, interval):
        """
        """
        self._visainstrument.write(':SCNINRVL {}'.format(interval))

    def do_get_scan_enabled(self):
        """
        """
        return self._visainstrument.query(':SCNENBL?')

    def do_set_scan_enabled(self, enabled):
        """
        """
        self._visainstrument.write(':SCNENBL {}'.format(enabled))

    def do_get_scan_state(self):
        """
        """
        return self._visainstrument.query(':SCNSTATE?')

    def do_get_scan_freq(self):
        """
        """
        return self._visainstrument.query(':SCNFREQ?')

    def do_set_scan_freq(self, freq):
        """
        """
        self._visainstrument.write(':SCNFREQ {}'.format(freq))

    def do_get_scan_amp(self):
        """
        """
        return self._visainstrument.query(':SCNAMP?')

    def do_set_scan_amp(self, amp):
        """
        """
        self._visainstrument.write(':SCNAMP {}'.format(amp))

    def do_get_scan_ref_dc_level(self):
        """
        """
        return self._visainstrument.query(':SCNDC?')

    def do_set_scan_ref_dc_level(self, level):
        """
        """
        self._visainstrument.write(':SCNDC {}'.format(level))

    def do_get_scan_aux_out_1_level(self):
        """
        """
        return self._visainstrument.query(':SCNAUX1?')

    def do_set_scan_aux_out_1_level(self, level):
        """
        """
        self._visainstrument.write(':SCNAUX1 {}'.format(level))

    def do_get_scan_aux_out_2_level(self):
        """
        """
        return self._visainstrument.query(':SCNAUX2?')

    def do_set_scan_aux_out_2_level(self, level):
        """
        """
        self._visainstrument.write(':SCNAUX2 {}'.format(level))

    def do_get_data_channel_val(self, channel):
        """
        Queries the current value of data channel DAT(channel + 1).

        Input:
                channel (int) : data channel index

        Output:
                val (float)   : value of data channel DAT(channel + 1)
        """
        return float(self._visainstrument.query(
            'OUTR? DAT{}'.format(channel + 1)).replace('\n', ''))

    def do_get_data_param(self, channel):
        """
        Queries the current value of the given data parameter.

        Input:
                channel (int) : data parameter index

        Output:
                val (float)   : value of data parameter
        """
        return float(self._visainstrument.query('OUTP? {}'.format(channel)))

    def do_get_capture_length(self):
        """
        """
        return self._visainstrument.query(':CAPTURELEN?')

    def do_set_capture_length(self, length):
        """
        """
        self._visainstrument.write(':CAPTURELEN {}'.format(length))

    def do_get_capture_config(self):
        """
        """
        return self._visainstrument.query(':CAPTURECFG?')

    def do_set_capture_config(self, config):
        """
        """
        self._visainstrument.write(':CAPTURECFG {}'.format(config))

    def do_get_capture_rate_max(self):
        """
        """
        return self._visainstrument.query(':CAPTURERATEMAX?')

    def do_get_capture_rate(self):
        """
        """
        return self._visainstrument.query(':CAPTURERATE?')

    def do_set_capture_rate(self, rate):
        """
        """
        self._visainstrument.write(':CAPTURERATE {}'.format(rate))

    def do_get_capture_state(self):
        """
        """
        return self._visainstrument.query(':CAPTURESTAT?')

    def do_get_num_bytes_captured(self):
        """
        """
        return self._visainstrument.query(':CAPTUREBYTES?')

    def do_get_num_kbytes_written(self):
        """
        """
        return self._visainstrument.query(':CAPTUREPROG?')

    def do_get_capture_buffer_ascii(self, pos):
        """
        """
        return self._visainstrument.query(':CAPTUREVAL? {}'.format(pos))

    def do_get_capture_buffer_bin(self, offset, length):
        """
        """
        return self._visainstrument.query(':CAPTUREGET? {}, {}'.format(offset, length))

    def do_get_stream_config(self):
        """
        """
        return self._visainstrument.query(':STREAMCH?')

    def do_set_stream_config(self, config):
        """
        """
        self._visainstrument.write(':STREAMCH {}'.format(config))

    def do_get_stream_rate_max(self):
        """
        """
        return self._visainstrument.query(':STREAMRATEMAX?')

    def do_get_stream_rate(self):
        """
        """
        return self._visainstrument.query(':STREAMRATE?')

    def do_set_stream_rate(self, rate):
        """
        """
        self._visainstrument.write(':STREAMRATE {}'.format(rate))

    def do_get_stream_format(self):
        """
        """
        return self._visainstrument.query(':STREAMFMT?')

    def do_set_stream_format(self, fmt):
        """
        """
        self._visainstrument.write(':STREAMFMT {}'.format(fmt))

    def do_get_stream_packet_size(self):
        """
        """
        return self._visainstrument.query(':STREAMPCKT?')

    def do_set_stream_packet_size(self, size):
        """
        """
        self._visainstrument.write(':STREAMPCKT {}'.format(size))

    def do_get_stream_port(self):
        """
        """
        return self._visainstrument.query(':STREAMPORT?')

    def do_set_stream_port(self, port):
        """
        """
        self._visainstrument.write(':STREAMPORT {}'.format(port))

    def do_get_stream_option(self):
        """
        """
        return self._visainstrument.query(':STREAMOPTION?')

    def do_set_stream_option(self, option):
        """
        """
        self._visainstrument.write(':STREAMOPTION {}'.format(option))

    def do_get_stream_enabled(self):
        """
        """
        return self._visainstrument.query(':STREAM?')

    def do_set_stream_enabled(self, enabled):
        """
        """
        self._visainstrument.write(':STREAM {}'.format(enabled))

    def do_get_time(self):
        """
        """
        return self._visainstrument.query(':TIME?')

    def do_set_time(self, setting, time):
        """
        """
        self._visainstrument.write(':TIME {}, {}'.format(setting, time))

    def do_get_date(self):
        """
        """
        return self._visainstrument.query(':DATE?')

    def do_set_date(self, setting, time):
        """
        """
        self._visainstrument.write(':DATE {}, {}'.format(setting, time))

    # def do_get_timebase_mode
    # def do_set_timebase_mode
    # def do_get_timebase_source

    def do_get_BlazeX_output(self):
        """
        """
        return self._visainstrument.query(':BLAZEX?')

    def do_set_BlazeX_output(self, setting):
        """
        """
        self._visainstrument.write(':BLAZEX {}'.format(setting))

    def do_get_sounds(self):
        """
        """
        return self._visainstrument.query(':KEYC?')

    def do_set_sounds(self, setting):
        """
        """
        self._visainstrument.write(':KEYC {}'.format(setting))

    def do_get_screenshot_mode(self):
        """
        """
        return self._visainstrument.query(':PRMD?')

    def do_set_screenshot_mode(self, mode):
        """
        """
        self._visainstrument.write(':PRMD {}'.format(mode))

    def do_get_data_file_format(self):
        """
        """
        return self._visainstrument.query(':SDFM?')

    def do_set_data_file_format(self, fmt):
        """
        """
        self._visainstrument.write(':SDFM {}'.format(fmt))

    def do_get_filename_prefix(self):
        """
        """
        return self._visainstrument.query(':FBAS?')

    def do_set_filename_prefix(self, prefix):
        """
        """
        self._visainstrument.write(':FBAS {}'.format(prefix))

    def do_get_filename_suffix(self):
        """
        """
        return self._visainstrument.query(':FNUM?')

    def do_set_filename_suffix(self, suffix):
        """
        """
        self._visainstrument.write(':FNUM {}'.format(suffix))

    def do_get_next_filename(self):
        """
        """
        return self._visainstrument.query(':FNXT?')

    def do_get_identification(self):
        """
        """
        return self._visainstrument.query(':*IDN?')

    def do_get_op_complete_bit(self):
        """
        """
        return self._visainstrument.query(':*OPC?')

    def do_set_op_complete_bit(self, bit):
        """
        """
        self._visainstrument.write(':*OPC {}'.format(bit))

    def do_get_local_remote(self):
        """
        """
        return self._visainstrument.query(':LOCL?')

    def do_set_local_remote(self, mode):
        """
        """
        self._visainstrument.write(':LOCL {}'.format(mode))

    def do_get_GPIB_override_remote(self):
        """
        """
        return self._visainstrument.query(':OVRM?')

    def do_set_GPIB_override_remote(self, override):
        """
        """
        self._visainstrument.write(':OVRM {}'.format(override))

    def do_get_standard_event_enable_register(self, bit=None):
        """
        """
        return self._visainstrument.query(':*ESE? {}'.format(bit)) if bit is not None else self._visainstrument.query(':*ESE?')

    def do_set_standard_event_enable_register(self, value, bit=None):
        """
        """
        self._visainstrument.write(':*ESE {}, {}'.format(value, bit)
                                   ) if bit is not None else self._visainstrument.write(':*ESE {}'.format(value))

    def do_get_standard_event_status_byte(self, bit=None):
        """
        """
        return self._visainstrument.query(':*ESR? {}'.format(bit)) if bit is not None else self._visainstrument.query(':*ESR?')

    def do_get_serial_poll_enable_register(self, bit=None):
        """
        """
        return self._visainstrument.query(':*SRE? {}'.format(bit)) if bit is not None else self._visainstrument.query(':*SRE?')

    def do_set_serial_poll_enable_register(self, value, bit=None):
        """
        """
        self._visainstrument.write(':*SRE {}, {}'.format(bit, value)
                                   ) if bit is not None else self._visainstrument.write(':*SRE {}'.format(value))

    def do_get_serial_poll_status_byte(self, bit=None):
        """
        """
        return self._visainstrument.query(':*STB? {}'.format(bit)) if bit is not None else self._visainstrument.query(':*STB?')

    def do_get_power_on_status_clear_bit(self):
        """
        """
        return self._visainstrument.query(':*PSC?')

    def do_set_power_on_status_clear_bit(self, bit):
        """
        """
        self._visainstrument.write(':*PSC {}'.format(bit))

    def do_get_error_status_enable_register(self, bit=None):
        """
        """
        return self._visainstrument.query(':ERRE? {}'.format(bit)) if bit is not None else self._visainstrument.query(':ERRE?')

    def do_set_error_status_enable_register(self, value, bit=None):
        """
        """
        self._visainstrument.write(':ERRE {}, {}'.format(
            bit, value)) if bit is not None else self._visainstrument.write(':ERRE {}'.format(value))

    def do_get_error_status_byte(self, bit=None):
        """
        """
        return self._visainstrument.query(':ERRS? {}'.format(bit)) if bit is not None else self._visainstrument.query(':ERRS?')

    def do_get_LIA_status_enable_register(self, bit=None):
        """
        """
        return self._visainstrument.query(':LIAE? {}'.format(bit)) if bit is not None else self._visainstrument.query(':LIAE?')

    def do_set_LIA_status_enable_register(self, value, bit=None):
        """
        """
        self._visainstrument.write(':LIAE {}, {}'.format(
            bit, value)) if bit is not None else self._visainstrument.write(':LIAE {}'.format(value))

    def do_get_LIA_status_word(self, bit=None):
        """
        """
        return self._visainstrument.query(':LIAS? {}'.format(bit)) if bit is not None else self._visainstrument.query(':LIAS?')

    def do_get_overload_states(self):
        """
        """
        return self._visainstrument.query(':CUROVLDSTAT?')

    def auto_offset(self):
        """
        Offsets X, Y, or R. This is the same as Auto Offset in the offset keypad display.

        Input:
                channel (int) : X, Y, or R channel

        Output:
                None
        """
        self._visainstrument.write(':OAUT {}'.format(None))

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

    # def get_screen(self):
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

    def get_multi_params(self, param1, param2, param3=None):
        """
        """
        return self._visainstrument.query(':SNAP? {}, {}, {}'.format(param1, param2, param3))

    def get_data_params(self):
        """
        """
        return self._visainstrument.query(':SNAPD?')

    def start_capture(self, acquisition, start):
        """
        """
        self._visainstrument.write(
            ':CAPTURESTART {}, {}'.format(acquisition, start))

    def stop_capture(self):
        """
        """
        self._visainstrument.write(':CAPTURESTOP')

    # def screenshot(self):

    def save_data(self):
        """
        """
        self._visainstrument.write(':SVDT')

    def reset(self):
        """
        """
        self._visainstrument.write(':*RST')

    def test(self):
        """
        """
        return self._visainstrument.query(':*TST?')

    def clear(self):
        """
        """
        self._visainstrument.write(':*CLS')
