"""
TODO add docstring
"""

# import logging

import numpy as np
import visa
from source.instrument import Instrument

########################################################################
# TODO:
#  - add doc parameters and docstrings
#     - include references to :FUNCTIONS: for now, but remove later
#  - add logging
#  - add tags to relevant parameters
#  - add 0/1/False/True options to `off`/`on` parameters
#  - simplify parameter names
#  - make better!
########################################################################


class GS610(Instrument):
    """
    add docstring
    """

    def __init__(self, name, address, reset=False):
        """
        add docstring
        """
        Instrument.__init__(self, name, tags=['physical'])
        self._visainstrument = visa.ResourceManager().get_instrument(address)

        # output commands (output group)
        # TODO add 1/0 options
        self.add_parameter('output_state', type=str,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the output state (ON, OFF, or zero) or "
                               "queries the current setting.",
                           option_list=('on', 'off', 'zero'))
        # TODO add 1/0 options
        self.add_parameter('output_program', type=str,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the programmable output state (ON or "
                               "OFF) or queries the current setting or "
                               "carries out pulse generation.",
                           option_list=('on', 'off', 'pulse'))

        # source commands (source group)
        self.add_parameter('source_function', type=str,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the source function (voltage or current) "
                               "or queries the current setting.",
                           option_list=('voltage', 'current'))
        self.add_parameter('source_shape', type=str,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the source mode (DC or pulse) or queries "
                               "the current setting.",
                           option_list=('DC', 'pulse'))
        self.add_parameter('source_mode', type=str,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the source pattern (fixed level, sweep, "
                               "or program sweep) or queries the current "
                               "setting.",
                           option_list=('fixed', 'sweep', 'list'))
        # TODO fix min/max options for bound and type checking
        self.add_parameter('source_delay_value', type=float,
                           flags=Instrument.FLAG_GETSET,
                           minval=self._do_get_source_delay_minimum(),
                           maxval=self._do_get_source_delay_maximum(),
                           doc="Sets the source delay or queries the current "
                               "setting.")
        self.add_parameter('source_delay_minimum', type=float,
                           flags=Instrument.FLAG_GET,
                           doc="Queries the minimum source delay.")
        self.add_parameter('source_delay_maximum', type=float,
                           flags=Instrument.FLAG_GET,
                           doc="Queries the maximum source delay.")
        self.add_parameter('source_delay_bound', type=float,
                           flags=Instrument.FLAG_SET,
                           doc="Sets the source delay to the minimum or to "
                               "the maximum value.",
                           option_list=('min', 'max'))
        self.add_function('get_source_delay')
        self.add_function('set_source_delay')
        # TODO add min/max options
        self.add_parameter('source_pulse_width', type=float,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the pulse width for pulse generation or "
                               "queries the current setting.")
        self.add_parameter('source_list_select', type=str,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the program sweep pattern file or "
                               "queries the current setting.")
        self.add_parameter('source_list_catalog', type=list,
                           flags=Instrument.FLAG_GET,
                           doc="Queries the list of program sweep pattern "
                               "files.")
        self.add_function('source_list_delete')
        self.add_function('source_list_define')
        # ------------
        # TODO add min/max/up/down options, discretize input
        self.add_parameter('source_voltage_range', type=float,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the voltage source range setting "
                               "(200 mV, 2 V, 12 V, 20 V, 30 V, 60 V, or "
                               "110 V) or queries the current setting.")
        # TODO add min/max options
        self.add_parameter('source_voltage_level', type=float,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the voltage source level value or "
                               "queries the current setting.")
        # TODO add min/max options
        self.add_parameter('source_voltage_pulse_base', type=float,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the pulse base value for voltage pulse "
                               "generation or queries the current setting.")
        # TODO add min/max options
        self.add_parameter('source_voltage_protection_upper_limit', type=float,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the upper voltage limiter value (for "
                               "generating current) or queries the current "
                               "setting.")
        # TODO add min/max options
        self.add_parameter('source_voltage_protection_lower_limit', type=float,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the lower voltage limiter value (for "
                               "generating current) or queries the current "
                               "setting.")
        # TODO add min/max options
        self.add_parameter('source_voltage_sweep_start', type=float,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the start value of the voltage sweep or "
                               "queries the current setting.")
        # TODO add min/max options
        self.add_parameter('source_voltage_sweep_stop', type=float,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the stop value of the voltage sweep or "
                               "queries the current setting.")
        # TODO add min/max options
        self.add_parameter('source_voltage_sweep_step', type=float,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the step value of the voltage sweep "
                               "(linear sweep) or queries the current "
                               "setting.")
        # TODO add min/max options
        self.add_parameter('source_voltage_sweep_points', type=int,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the step count of the voltage sweep (log "
                               "sweep) or queries the current setting.")
        self.add_parameter('source_voltage_zero_impedance', type=str,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the zero source impedance (high or low) "
                               "for generating voltage or queries the current "
                               "setting.",
                           option_list=('high', 'low'))
        # TODO add min/max options (unspecified)
        self.add_parameter('source_voltage_zero_offset', type=float,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the zero source offset value for "
                               "generating voltage or queries the current "
                               "setting.")
        # TODO add min/max/up/down options, discretize input
        self.add_parameter('source_current_range', type=float,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the current source range setting (20 μA, "
                               "200 μA, 2 mA, 20 mA, 200 mA, 0.5 A, 1 A, 2 A, "
                               "or 3 A) or queries the current setting.")
        # TODO add min/max options
        self.add_parameter('source_current_level', type=float,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the current source level value or "
                               "queries the current setting.")
        # TODO add min/max options
        self.add_parameter('source_current_pulse_base', type=float,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the pulse base value for current pulse "
                               "generation or queries the current setting.")
        # TODO add min/max options
        self.add_parameter('source_current_protection_upper_limit', type=float,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the upper current limiter value (for "
                               "generating voltage) or queries the current "
                               "setting.")
        # TODO add min/max options
        self.add_parameter('source_current_protection_lower_limit', type=float,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the lower current limiter value (for "
                               "generating voltage) or queries the current "
                               "setting.")
        # TODO add min/max options
        self.add_parameter('source_current_sweep_start', type=float,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the start value of the current sweep or "
                               "queries the current setting.")
        # TODO add min/max options
        self.add_parameter('source_current_sweep_stop', type=float,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the stop value of the current sweep or "
                               "queries the current setting.")
        # TODO add min/max options
        self.add_parameter('source_current_sweep_step', type=float,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the step value of the current sweep "
                               "(linear sweep) or queries the current "
                               "setting.")
        # TODO add min/max options
        self.add_parameter('source_current_sweep_points', type=int,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the step count of the current sweep (log "
                               "sweep) or queries the current setting.")
        self.add_parameter('source_current_zero_impedance', type=str,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the zero source impedance (high or low) "
                               "for generating current or queries the current "
                               "setting.",
                           option_list=('high', 'low'))
        # TODO add min/max options (unspecified)
        self.add_parameter('source_current_zero_offset', type=float,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the zero source offset value for "
                               "generating current or queries the current "
                               "setting.")
        self.add_parameter('source_range_auto', type=str,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the source auto range (ON or OFF) or "
                               "queries the current setting.",
                           option_list=('on', 'off'))
        self.add_parameter('source_protection_state', type=str,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the limiter state (ON or OFF) or queries "
                               "the current setting.",
                           option_list=('on', 'off'))
        self.add_parameter('source_protection_linkage', type=str,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the limiter tracking state (ON or OFF) "
                               "or queries the current setting.",
                           option_list=('on', 'off'))
        self.add_parameter('source_sweep_spacing', type=str,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the sweep mode (linear or log) or "
                               "queries the current setting.",
                           option_list=('linear', 'log'))

        # sweep commands (sweep group)
        self.add_function('sweep_trigger', doc="Starts the sweep operation.")
        # TODO add inf/min/max options
        self.add_parameter('sweep_count', type=int,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the sweep repeat count or queries the "
                               "current setting.")
        self.add_parameter('sweep_last', type=str,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the sweep termination mode (keep level "
                               "or return to initial level) or queries the "
                               "current setting.",
                           option_list=('keep', 'return'))

        # measurement commands (sense group)
        self.add_parameter('sense_state', type=str,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the measurement state (ON or OFF) or "
                               "queries the current setting.",
                           option_list=('on', 'off'))
        self.add_parameter('sense_function', type=str,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the measurement function (voltage, "
                               "current, or resistance) or queries the "
                               "current setting.",
                           option_list=('voltage', 'current', 'resistance'))
        self.add_parameter('sense_range_auto', type=str,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the measurement auto range (ON or OFF) "
                               "or queries the current setting.",
                           option_list=('on', 'off'))
        # TODO add plc/min/max/up/down options
        self.add_parameter('sense_integration_time', type=float,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the integration time or queries the "
                               "current setting.")
        # TODO add min/max options
        self.add_parameter('sense_delay', type=float,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the measurement delay or queries the "
                               "current setting.")
        self.add_parameter('sense_auto_zero_state', type=str,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the auto zero state (ON or OFF) or "
                               "queries the current setting.",
                           option_list=('on', 'off'))
        self.add_function('sense_auto_zero_execute',
                          doc="Executes auto zero.")
        self.add_parameter('sense_average_state', type=str,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the average state (ON or OFF) or queries "
                               "the current setting.",
                           option_list=('on', 'off'))
        self.add_parameter('sense_average_mode', type=str,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the average mode (block or moving "
                               "average) or queries the current setting.",
                           option_list=('block', 'moving'))
        # TODO add min/max options
        self.add_parameter('sense_average_count', type=int,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the average count or queries the current "
                               "setting.")
        self.add_parameter('sense_auto_change', type=str,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the auto V/I mode (ON or OFF) or queries "
                               "the current setting.",
                           option_list=('on', 'off'))
        self.add_parameter('sense_remote_sense', type=str,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the four-wire measurement (remote sense) "
                               "(ON or OFF) or queries the current setting.",
                           option_list=('on', 'off'))

        # trigger commands (trigger group)
        # ...

        # computation commands (calculate group)
        # ...

        # store/recall commands (trace group)
        # ...

        # external input/output commands (route group)
        # ...

        # system commands (system group)
        # ...

        # measured value read commands (initiate, fetch, and read group)
        self.add_function('initiate', doc="Starts a new measurement.")
        self.add_function('fetch', doc="Queries the measured results.")
        self.add_function('read',
                          doc="Starts a new measurement and queries the "
                              "measured results.")

        # status commands (status group)
        # ...

        # common command group
        # TODO implement other commands
        # self.add_function('identify')
        # self.add_function('options')
        # self.add_function('trigger')
        # self.add_function('calibrate')
        # self.add_function('self_test')
        self.add_function('reset',
                          doc="Resets the GS610 to factory default settings.")
        # self.add_function('save')
        # self.add_function('recall')
        # self.add_function('clear_status')
        # self.add_function('read_status_byte')
        # self.add_function('service_request_enable')
        # self.add_function('standard_event_status_register')
        # self.add_function('standard_event_status_enable')
        # self.add_function('operation_complete')
        # self.add_function('is_operation_complete')
        # self.add_function('wait_to_continue')

        if reset:
            self.reset()


    # output commands (output group)
    def _do_get_output_state(self):
        """
        Queries and returns the current output state (ON, OFF, or
        zero).

        ON and OFF indicates ON and OFF of the output relay. ZERO
        indicates the zero state. The zero state is defined using the
        :SOUR:VOLT:ZERO or :SOUR:CURR:ZERO command.

        Returns
        -------
        out : str
            If `on`, currently ON. If `off`, currently OFF. If `zero`,
            currently zero.
        """
        format_map = {'0': 'off', '1': 'on', 'ZERO': 'zero'}
        state = self._visainstrument.query(':OUTP:STAT?').replace('\n', '')
        return format_map[state]

    def _do_set_output_state(self, state):
        """
        Sets the output state (ON, OFF, or zero).

        ON and OFF indicates ON and OFF of the output relay. ZERO
        indicates the zero state. The zero state is defined using the
        :SOUR:VOLT:ZERO or :SOUR:CURR:ZERO command.

        Parameters
        ----------
        state : str
            If `on`, turns the output ON. If `off`, turns the output
            OFF. If `zero`, turns the output to zero.
        """
        self._visainstrument.write(':OUTP:STAT {}'.format(state))

    def _do_get_output_program(self):
        """
        Queries and returns the current programmable output state (ON
        or OFF).

        The program output used here indicates pin 9 of the external
        input/output connector. If the BNC output is set to
        programmable output using the :ROUT:BOUT:SEL CONT;CONT PROG
        command, the same signal is output to the BNC output.

        Returns
        -------
        out : str
            If `on`, currently ON (low). If `off`, currently OFF
            (high).
        """
        format_map = {'0': 'off', '1': 'on'}
        state = self._visainstrument.query(':OUTP:PROG?').replace('\n', '')
        return format_map[state]

    def _do_set_output_program(self, state):
        """
        Sets the programmable output state (ON or OFF) or carries out
        pulse generation.

        The program output used here indicates pin 9 of the external
        input/output connector. If the BNC output is set to programmable
        output using the :ROUT:BOUT:SEL CONT;CONT PROG command, the same
        signal is output to the BNC output.

        Parameters
        ----------
        state : str
            If `on`, turns the output ON (low). If `off`, turns the
            output OFF (high). If `pulse`, generates a 10-μs pulse.
        """
        self._visainstrument.write(':OUTP:PROG {}'.format(state))


    # source commands (source group)

    def _do_get_source_function(self):
        """
        Queries and returns the current source function (voltage or
        current).

        When the source function is changed, the output (:OUTP:STAT) is
        automatically turned OFF.

        Returns
        -------
        out : str
            If `voltage`, currently set to voltage. If `current`,
            currently set to current.
        """
        format_map = {'VOLT': 'voltage', 'CURR': 'current'}
        function = self._visainstrument.query(':SOUR:FUNC?').replace('\n', '')
        return format_map[function]

    def _do_set_source_function(self, function):
        """
        Sets the source function (voltage or current).

        When the source function is changed, the output (:OUTP:STAT) is
        automatically turned OFF.

        Parameters
        ----------
        function : str
            If `voltage`, sets the source function to voltage. If
            `current`, sets the source function to current.
        """
        self._visainstrument.write(':SOUR:FUNC {}'.format(function))

    def _do_get_source_shape(self):
        """
        Queries and returns the current source mode (DC or pulse).

        This function corresponds to MODE on the front panel.

        Returns
        -------
        out : str
            If `DC`, currently set to DC. If `puls`, currently set to
            pulse.
        """
        format_map = {'DC': 'DC', 'PULS': 'pulse'}
        shape = self._visainstrument.query(':SOUR:SHAP?').replace('\n', '')
        return format_map[shape]

    def _do_set_source_shape(self, shape):
        """
        Sets the source mode (DC or pulse).

        This function corresponds to MODE on the front panel.

        Parameters
        ----------
        shape : str
            If `DC`, sets the source mode to DC. If `pulse`, sets the
            source mode to pulse.
        """
        self._visainstrument.write(':SOUR:SHAP {}'.format(shape))

    def _do_get_source_mode(self):
        """
        Queries and returns the current source pattern (fixed level,
        sweep, or program sweep).

        This function corresponds to SWEEP on the front panel. Specify
        the linear or log setting of the sweep mode using the
        :SOUR:VOLT:SWE:SPAC or :SOUR:CURR:SWE:SPAC command.

        Returns
        -------
        out : str
            If `fixed`, currently set to constant level (sweep OFF). If
            `sweep`, currently set to sweep (linear or log sweep). If
            `list`, currently set to program sweep.
        """
        format_map = {'FIX': 'fixed', 'SWE': 'sweep', 'LIST': 'list'}
        mode = self._visainstrument.query(':SOUR:MODE?').replace('\n', '')
        return format_map[mode]

    def _do_set_source_mode(self, mode):
        """
        Sets the source pattern (fixed level, sweep, or program sweep).

        This function corresponds to SWEEP on the front panel. Specify
        the linear or log setting of the sweep mode using the
        :SOUR:VOLT:SWE:SPAC or :SOUR:CURR:SWE:SPAC command.

        Parameters
        ----------
        mode : str
            If `fixed`, sets the source pattern to constant level
            (sweep OFF). If `sweep`, sets the source pattern to sweep
            (linear or log sweep). If `list`, sets the source pattern
            to program sweep.
        """
        self._visainstrument.write(':SOUR:MODE {}'.format(mode))

    def _do_get_source_delay_value(self):
        """
        Queries and returns the current source delay in seconds.

        Returns
        -------
        out : float
            The current source delay in seconds.
        """
        return self._visainstrument.query(':SOUR:DEL?')

    def _do_set_source_delay_value(self, delay):
        """
        Sets the source delay in seconds.

        Parameters
        ----------
        delay : float
            Sets the source delay to the specified value in seconds.
        """
        self._visainstrument.write(':SOUR:DEL {}'.format(delay))

    def _do_get_source_delay_minimum(self):
        """
        Queries and returns the minimum source delay value in seconds.

        Returns
        -------
        out : float
            The minimum value in seconds.
        """
        return self._visainstrument.query(':SOUR:DEL? MIN')

    def _do_get_source_delay_maximum(self):
        """
        Queries and returns the maximum source delay value in seconds.

        Returns
        -------
        out : float
            The maximum value in seconds.
        """
        return self._visainstrument.query(':SOUR:DEL? MAX')

    def _do_set_source_delay_bound(self, bound):
        """
        Sets the source delay to the minimum or to the maximum value in
        seconds.

        Paramaters
        ----------
        bound : str
            If `min`, sets the source delay to the minimum value. If
            `max`, sets the source delay to the maximum value.
        """
        self._visainstrument.write(':SOUR:DEL {}'.format(bound))

    def get_source_delay(self, bound=None):
        """
        Queries and returns the current source delay in seconds.

        TODO improve type checking and assert

        Parameters
        ----------
        bound : str
            If None, queries the current value in seconds. If `min`,
            queries the minimum value in seconds. If `max`, queries the
            maximum value in seconds.

        Returns
        -------
        out : float
            The source delay in seconds. If bound is given, either the
            minimum or maximum source delay in seconds.
        """
        if bound is not None:
            assert bound in ['min', 'max']

            if bound == 'min':
                delay = self._do_get_source_delay_minimum().replace('\n', '')
                return float(delay)

            if bound == 'max':
                delay = self._do_get_source_delay_maximum().replace('\n', '')
                return float(delay)

        return float(self._do_get_source_delay_value().replace('\n', ''))

    def set_source_delay(self, delay):
        """
        Sets the source delay in seconds.

        FIXME does not keep delay between min and max values
        TODO improve type checking and TypeError

        Parameters
        ----------
        delay : int, float, or str
            If a number, sets the source delay to the specified value.
            If a str (must be either `min` or `max`), sets the source
            delay to the minimum or to the maximum value.
        """
        if isinstance(delay, (int, float)):
            self._do_set_source_delay_value(delay)
        elif isinstance(delay, str):
            self._do_set_source_delay_bound(delay)
        else:
            raise TypeError()

    def _do_get_source_pulse_width(self):
        """
        Queries and returns the current pulse width for pulse
        generation in seconds.

        Returns
        -------
        out : float
            The current pulse width in seconds.
        """
        return self._visainstrument.query(':SOUR:PULS:WIDT?')

    def _do_set_source_pulse_width(self, width):
        """
        Sets the pulse width in seconds for pulse generation.

        Parameters
        ----------
        width : float
            Sets the pulse width to the specified value in seconds.
        """
        self._visainstrument.write(':SOUR:PULS:WIDT {}'.format(width))

    def _do_get_source_list_select(self):
        """
        Queries and returns the current program sweep pattern file
        name.

        Select a file in the PROGRAM directory on the GS610ROM disk. An
        error occurs if a file name that does not exist is specified.
        The file name is not case sensitive.

        Returns
        -------
        out : str
            The current program sweep pattern file name.
        """
        return self._visainstrument.query(':SOUR:LIST:SEL?').replace('\n', '')

    def _do_set_source_list_select(self, filename):
        """
        Sets the program sweep pattern file name.

        Select a file in the PROGRAM directory on the GS610ROM disk. An
        error occurs if a file name that does not exist is specified.
        The file name is not case sensitive.

        Parameters
        ----------
        filename : str
            Sets the program sweep pattern file to the file with the
            specified file name.
        """
        self._visainstrument.write(':SOUR:LIST:SEL \"{}\"'.format(filename))

    def _do_get_source_list_catalog(self):
        """
        Queries and returns a list of program sweep pattern file names.

        Pattern files are files in the PROGRAM directory of the
        GS610ROM disk.

        Returns
        -------
        out : list[str]
        """
        catalog = self._visainstrument.query(':SOUR:LIST:CAT?')
        catalog = catalog.replace('\n', '')
        return catalog.replace('\"', '').split(',')

    def source_list_delete(self, filename):
        """
        Deletes the program sweep pattern file.

        Select a file in the PROGRAM directory on the GS610ROM disk. An
        error occurs if a file name that does not exist is specified.
        The file name is not case sensitive.

        Parameters
        ----------
        filename : str
            Deletes the program sweep pattern file with the specified
            file name.
        """
        self._visainstrument.write(':SOUR:LIST:DEL \"{}\"'.format(filename))

    def source_list_define(self, filename, contents):
        """
        Creates a program sweep pattern file.

        The file is created in the PROGRAM directory of the GS610ROM
        disk. If an existing file name is specified, the file is
        overwritten.

        Parameters
        ----------
        filename : str
            Creates a program sweep pattern file with the specified
            file name.
        contents : list[float]
            The contents to be written to the new program sweep pattern
            file.
        """
        self._visainstrument.write(':SOUR:LIST:DEF \"{}\", \"{}\n\r\"'.format(
            filename, '\n\r'.join(map(str, contents))))

    # -----------

    def _do_get_source_voltage_range(self):
        """
        Queries the current voltage source range (200 mV, 2 V, 12 V,
        20 V, 30 V, 60 V, or 110 V).

        Input:
            None

        Output:
            voltage_range (float) : voltage source range in volts
        """
        return self._visainstrument.query(':SOUR:VOLT:RANG?').replace('\n', '')

    def _do_set_source_voltage_range(self, voltage_range):
        """
        Sets the voltage source range to the smallest range that
        includes the argument (200 mV, 2 V, 12 V, 20 V, 30 V, 60 V, or
        110 V).

        Input:
            voltage_range (float) : voltage source range in volts

        Output:
            None
        """
        self._visainstrument.write(':SOUR:VOLT:RANG %e' % voltage_range)

    def _do_get_source_voltage_level(self):
        """
        Queries the current voltage source level.

        Input:
            None

        Output:
            level (float) : voltage source level in volts
        """
        return self._visainstrument.query(':SOUR:VOLT:LEV?').replace('\n', '')

    def _do_set_source_voltage_level(self, level):
        """
        Sets the voltage source level.

        Input:
            level (float) : voltage source level in volts

        Output:
            None
        """
        self._visainstrument.write(':SOUR:VOLT:LEV %e' % level)

    def _do_get_source_voltage_pulse_base(self):
        """
        Queries the current voltage source pulse base value.

        Input:
            None

        Output:
            pulse_base (float) : voltage source pulse base in volts
        """
        return self._visainstrument.query(':SOUR:VOLT:PBAS?').replace('\n', '')

    def _do_set_source_voltage_pulse_base(self, pulse_base):
        """
        Sets the voltage source pulse base value.

        Input:
            pulse_base (float) : voltage source pulse base in volts

        Output:
            None
        """
        self._visainstrument.write(':SOUR:VOLT:PBAS %e' % pulse_base)

    def _do_get_source_voltage_protection_upper_limit(self):
        """
        Queries the current source upper voltage limiter value.

        Input:
            None

        Output:
            limit (float) : source upper voltage limiter value
        """
        return self._visainstrument.query(
            ':SOUR:VOLT:PROT:ULIM?').replace('\n', '')

    def _do_set_source_voltage_protection_upper_limit(self, limit):
        """
        Sets the source upper voltage limiter value.

        Input:
            limit (float) : source upper voltage limiter value

        Output:
            None
        """
        self._visainstrument.write(':SOUR:VOLT:PROT:ULIM %e' % limit)

    def _do_get_source_voltage_protection_lower_limit(self):
        """
        Queries the current source lower voltage limiter value.

        Input:
            None

        Output:
            limit (float) : source lower voltage limiter value
        """
        return self._visainstrument.query(
            ':SOUR:VOLT:PROT:LLIM?').replace('\n', '')

    def _do_set_source_voltage_protection_lower_limit(self, limit):
        """
        Sets the source lower voltage limiter value.

        Input:
            limit (float) : source lower voltage limiter value

        Output:
            None
        """
        self._visainstrument.write(':SOUR:VOLT:PROT:LLIM %e' % limit)

    def _do_get_source_voltage_sweep_start(self):
        """
        Queries the current start value of the voltage sweep.

        Input:
            None

        Output:
            start (float) : start value of voltage sweep
        """
        return self._visainstrument.query(
            ':SOUR:VOLT:SWE:STAR?').replace('\n', '')

    def _do_set_source_voltage_sweep_start(self, start):
        """
        Sets the start value of the voltage sweep.

        Input:
            start (float) : start value of the voltage sweep

        Output:
            None
        """
        self._visainstrument.write(':SOUR:VOLT:SWE:STAR %e' % start)

    def _do_get_source_voltage_sweep_stop(self):
        """
        Queries the current stop value of the voltage sweep.

        Input:
            None

        Output:
            stop (float) : stop value of voltage sweep
        """
        return self._visainstrument.query(
            ':SOUR:VOLT:SWE:STOP?').replace('\n', '')

    def _do_set_source_voltage_sweep_stop(self, stop):
        """
        Sets the stop value of the voltage sweep.

        Input:
            stop (float) : stop value of voltage sweep

        Output:
            None
        """
        self._visainstrument.write(':SOUR:VOLT:SWE:STOP %e' % stop)

    def _do_get_source_voltage_sweep_step(self):
        """
        Queries the current step value of the linear voltage sweep.

        Input:
            None

        Output:
            step (float) : step value of the linear voltage sweep
        """
        return self._visainstrument.query(
            ':SOUR:VOLT:SWE:STEP?').replace('\n', '')

    def _do_set_source_voltage_sweep_step(self, step):
        """
        Sets the step value of the linear voltage sweep.

        Input:
            step (float) : step value of the linear voltage sweep

        Output:
            None
        """
        self._visainstrument.write(':SOUR:VOLT:SWE:STEP %e' % step)

    def _do_get_source_voltage_sweep_points(self):
        """
        Queries the current step count of the logarithmic voltage sweep.

        Input:
            None

        Output:
            points (int) : step count of logarithmic voltage sweep
        """
        return self._visainstrument.query(
            ':SOUR:VOLT:SWE:POIN?').replace('\n', '')

    def _do_set_source_voltage_sweep_points(self, points):
        """
        Sets the step count of the logarithmic voltage sweep.

        Input:
            points (int) : step count of logarithmic voltage sweep

        Output:
            None
        """
        self._visainstrument.write(':SOUR:VOLT:SWE:POIN %i' % points)

    def _do_get_source_voltage_zero_impedance(self):
        """
        Queries the current zero source impedance for generating
        voltage (LOW or HIGH).

        Input:
            None

        Output:
            impedance (int) : zero source impedance for generating
                              voltage
        """
        format_map = self.get_parameters()['source_voltage_zero_impedance']\
            ['format_map']
        return list(format_map.keys())[
            list(format_map.values()).index(
                self._visainstrument.query(
                    ':SOUR:VOLT:ZERO:IMP?').replace('\n', ''))]

    def _do_set_source_voltage_zero_impedance(self, impedance):
        """
        Sets the zero source impedance for generating voltage (LOW or
        HIGH).

        Input:
            impedance (int) : zero source impedance for generating
                              voltage

        Output:
            None
        """
        self._visainstrument.write(
            ':SOUR:VOLT:ZERO:IMP %s' % self.get_parameters()['output']\
                ['format_map'][impedance])

    def _do_get_source_voltage_zero_offset(self):
        """
        Queries the current zero source offset for generating voltage.

        Input:
            None

        Output:
            offset (float) : zero source offset for generating voltage
        """
        return self._visainstrument.query(
            ':SOUR:VOLT:ZERO:OFFS?').replace('\n', '')

    def _do_set_source_voltage_zero_offset(self, offset):
        """
        Sets the zero source offset for generating voltage.

        Input:
            offset (float) : zero source offset for generating voltage

        Output:
            None
        """
        self._visainstrument.write(':SOUR:VOLT:ZERO:OFFS %e' % offset)

    def _do_get_source_current_range(self):
        """
        Queries the current current source range (20 μA, 200 μA, 2 mA,
        20 mA, 200 mA, 0.5 A, 1 A, 2 A, or 3 A).

        Input:
            None

        Output:
            current_range (float) : current source range in amperes
        """
        return self._visainstrument.query(':SOUR:CURR:RANG?').replace('\n', '')

    def _do_set_source_current_range(self, current_range):
        """
        Sets the current source range to the smallest range that
        includes the argument (20 μA, 200 μA, 2 mA, 20 mA, 200 mA,
        0.5 A, 1 A, 2 A, or 3 A).

        Input:
            current_range (float) : current source range in amperes

        Output:
            None
        """
        self._visainstrument.write(':SOUR:CURR:RANG %e' % current_range)

    def _do_get_source_current_level(self):
        """
        Queries the current current source level.

        Input:
            None

        Output:
            level (float) : current source level in amperes
        """
        return self._visainstrument.query(':SOUR:CURR:LEV?').replace('\n', '')

    def _do_set_source_current_level(self, level):
        """
        Sets the current source level.

        Input:
            level (float) : current source level in amperes

        Output:
            None
        """
        self._visainstrument.write(':SOUR:CURR:LEV %e' % level)

    def _do_get_source_current_pulse_base(self):
        """
        Queries the current current source pulse base value.

        Input:
            None

        Output:
            pulse_base (float) : current source pulse base in amperes
        """
        return self._visainstrument.query(':SOUR:CURR:PBAS?').replace('\n', '')

    def _do_set_source_current_pulse_base(self, pulse_base):
        """
        Sets the current source pulse base value.

        Input:
            pulse_base (float) : current source pulse base in amperes

        Output:
            None
        """
        self._visainstrument.write(':SOUR:CURR:PBAS %e' % pulse_base)

    def _do_get_source_current_protection_upper_limit(self):
        """
        Queries the current source upper current limiter value.

        Input:
            None

        Output:
            limit (float) : source upper current limiter value
        """
        return self._visainstrument.query(
            ':SOUR:CURR:PROT:ULIM?').replace('\n', '')

    def _do_set_source_current_protection_upper_limit(self, limit):
        """
        Sets the source upper current limiter value.

        Input:
            limit (float) : source upper current limiter value

        Output:
            None
        """
        self._visainstrument.write(':SOUR:CURR:PROT:ULIM %e' % limit)

    def _do_get_source_current_protection_lower_limit(self):
        """
        Queries the current source lower current limiter value.

        Input:
            None

        Output:
            limit (float) : source lower current limiter value
        """
        return self._visainstrument.query(
            ':SOUR:CURR:PROT:LLIM?').replace('\n', '')

    def _do_set_source_current_protection_lower_limit(self, limit):
        """
        Sets the source lower current limiter value.

        Input:
            limit (float) : source lower current limiter value

        Output:
            None
        """
        self._visainstrument.write(':SOUR:CURR:PROT:LLIM %e' % limit)

    def _do_get_source_current_sweep_start(self):
        """
        Queries the current start value of the current sweep.

        Input:
            None

        Output:
            start (float) : start value of current sweep
        """
        return self._visainstrument.query(
            ':SOUR:CURR:SWE:STAR?').replace('\n', '')

    def _do_set_source_current_sweep_start(self, start):
        """
        Sets the start value of the current sweep.

        Input:
            start (float) : start value of the current sweep

        Output:
            None
        """
        self._visainstrument.write(':SOUR:CURR:SWE:STAR %e' % start)

    def _do_get_source_current_sweep_stop(self):
        """
        Queries the current stop value of the current sweep.

        Input:
            None

        Output:
            stop (float) : stop value of current sweep
        """
        return self._visainstrument.query(
            ':SOUR:CURR:SWE:STOP?').replace('\n', '')

    def _do_set_source_current_sweep_stop(self, stop):
        """
        Sets the stop value of the current sweep.

        Input:
            stop (float) : stop value of current sweep

        Output:
            None
        """
        self._visainstrument.write(':SOUR:CURR:SWE:STOP %e' % stop)

    def _do_get_source_current_sweep_step(self):
        """
        Queries the current step value of the linear current sweep.

        Input:
            None

        Output:
            step (float) : step value of the linear current sweep
        """
        return self._visainstrument.query(
            ':SOUR:CURR:SWE:STEP?').replace('\n', '')

    def _do_set_source_current_sweep_step(self, step):
        """
        Sets the step value of the linear current sweep.

        Input:
            step (float) : step value of the linear current sweep

        Output:
            None
        """
        self._visainstrument.write(':SOUR:CURR:SWE:STEP %e' % step)

    def _do_get_source_current_sweep_points(self):
        """
        Queries the current step count of the logarithmic current sweep.

        Input:
            None

        Output:
            points (int) : step count of logarithmic current sweep
        """
        return self._visainstrument.query(
            ':SOUR:CURR:SWE:POIN?').replace('\n', '')

    def _do_set_source_current_sweep_points(self, points):
        """
        Sets the step count of the logarithmic current sweep.

        Input:
            points (int) : step count of logarithmic current sweep

        Output:
            None
        """
        self._visainstrument.write(':SOUR:CURR:SWE:POIN %i' % points)

    def _do_get_source_current_zero_impedance(self):
        """
        Queries the current zero source impedance for generating
        current (LOW or HIGH).

        Input:
            None

        Output:
            impedance (int) : zero source impedance for generating
                              current
        """
        format_map = self.get_parameters()['source_current_zero_impedance']\
            ['format_map']
        return list(format_map.keys())[
            list(format_map.values()).index(
                self._visainstrument.query(
                    ':SOUR:CURR:ZERO:IMP?').replace('\n', ''))]

    def _do_set_source_current_zero_impedance(self, impedance):
        """
        Sets the zero source impedance for generating current (LOW or
        HIGH).

        Input:
            impedance (int) : zero source impedance for generating
                              current

        Output:
            None
        """
        self._visainstrument.write(
            ':SOUR:CURR:ZERO:IMP %s' % self.get_parameters()['output']\
                ['format_map'][impedance])

    def _do_get_source_current_zero_offset(self):
        """
        Queries the current zero source offset for generating current.

        Input:
            None

        Output:
            offset (float) : zero source offset for generating current
        """
        return self._visainstrument.query(
            ':SOUR:CURR:ZERO:OFFS?').replace('\n', '')

    def _do_set_source_current_zero_offset(self, offset):
        """
        Sets the zero source offset for generating current.

        Input:
            offset (float) : zero source offset for generating current

        Output:
            None
        """
        self._visainstrument.write(':SOUR:CURR:ZERO:OFFS %e' % offset)

    def _do_get_source_range_auto(self):
        """
        Queries the current source autorange setting.

        Input:
            None

        Output:
            auto (int) : source autorange
        """
        return self._visainstrument.query(
            ':SOUR:VOLT:RANG:AUTO?').replace('\n', '')

    def _do_set_source_range_auto(self, auto):
        """
        Sets the source autorange setting.

        Intput:
            auto (int) : source autorange

        Output:
            None
        """
        self._visainstrument.write(':SOUR:VOLT:RANG:AUTO %i' % auto)

    def _do_get_source_protection_state(self):
        """
        Queries the current source limiter state (ON or OFF).

        Input:
            None

        Output:
            state (int) : source limiter state
        """
        return self._visainstrument.query(':SOUR:VOLT:PROT?').replace('\n', '')

    def _do_set_source_protection_state(self, state):
        """
        Sets the source limiter state (ON or OFF).

        Input:
            state (int) : source limiter state

        Output:
            None
        """
        self._visainstrument.write(':SOUR:VOLT:PROT %i' % state)

    def _do_get_source_protection_linkage(self):
        """
        Queries the current source limiter tracking state (ON or OFF).

        Input:
            None

        Output:
            state (int) : source limiter tracking state
        """
        return self._visainstrument.query(
            ':SOUR:VOLT:PROT:LINK?').replace('\n', '')

    def _do_set_source_protection_linkage(self, state):
        """
        Sets the source limiter tracking state (ON or OFF).

        Input:
            state (int) : source limiter tracking state

        Output:
            None
        """
        self._visainstrument.write(':SOUR:VOLT:PROT:LINK %i' % state)

    def _do_get_source_sweep_spacing(self):
        """
        Queries the current sweep mode (linear or log).

        Input:
            None

        Output:
            spacing (int) : sweep mode
        """
        format_map = self.get_parameters()['source_sweep_spacing']\
            ['format_map']
        return list(format_map.keys())[
            list(format_map.values()).index(
                self._visainstrument.query(
                    ':SOUR:VOLT:SWE:SPAC?').replace('\n', ''))]

    def _do_set_source_sweep_spacing(self, spacing):
        """
        Sets the sweep mode (linear or log).

        Input:
            spacing (int) : sweep mode

        Output:
            None
        """
        self._visainstrument.write(
            ':SOUR:VOLT:SWE:SPAC %s' % self.get_parameters()\
                ['source_sweep_spacing']['format_map'][spacing])


    # sweep commands (sweep group)

    def sweep_trigger(self):
        """
        TODO implement me
        """

    def _do_get_sweep_count(self):
        """
        Queries the current sweep repeat count (a count of 0
        corresponds to infinity).

        Input:
            None

        Output:
            count (int) : sweep repeat count
        """
        count = self._visainstrument.query(':SWE:COUN?').replace('\n', '')
        return count if count != 'INF' else 0

    def _do_set_sweep_count(self, count):
        """
        Sets the sweep repeat count (a count of 0 corresponds to
        infinity).

        Input:
            count (int) : sweep repeat count

        Output:
            None
        """
        if count != 0:
            self._visainstrument.write(':SWE:COUN %i' % count)
        else:
            self._visainstrument.write(':SWE:COUN INF')

    def _do_get_sweep_last(self):
        """
        Queries the current sweep termination mode (keep level or
        return to initial level).

        Input:
            None

        Output:
            level (int) : sweep termination mode
        """
        format_map = self.get_parameters()['sweep_last']['format_map']
        return list(format_map.keys())[
            list(format_map.values()).index(
                self._visainstrument.query(':SWE:LAST?').replace('\n', ''))]

    def _do_set_sweep_last(self, level):
        """
        Sets the sweep termination mode (keep level or return to
        initial level).

        Input:
            level (int) : sweep termination mode

        Output:
            None
        """
        self._visainstrument.write(':SWE:LAST %s' % self.get_parameters()\
            ['sweep_last']['format_map'][level])


    # measurement commands (sense group)

    def _do_get_sense_state(self):
        """
        Queries the current measurement state (ON or OFF).

        Input:
            None

        Output:
            state (int) : measurement state
        """
        return self._visainstrument.query(':SENS:STAT?').replace('\n', '')

    def _do_set_sense_state(self, state):
        """
        Sets the measurement state (ON or OFF).

        Input:
            state (int) : measurement state

        Output:
            None
        """
        self._visainstrument.write(':SENS %s' % state)

    def _do_get_sense_function(self):
        """
        Queries the current measurement function (voltage, current, or
        resistance).

        Input:
            None

        Output:
            function (int) : measurement function
        """
        format_map = self.get_parameters()['sense_function']['format_map']
        return list(format_map.keys())[
            list(format_map.values()).index(
                self._visainstrument.query(':SENS:FUNC?').replace('\n', ''))]

    def _do_set_sense_function(self, function):
        """
        Setst the measurement function (voltage, current, or resistance).

        Input:
            function (int) : measurement function

        Output:
            None
        """
        self._visainstrument.write(':SENS:FUNC %s' % self.get_parameters()\
            ['sense_function']['format_map'][function])

    def _do_get_sense_range_auto(self):
        """
        Queries the current measurement autorange state (ON or OFF).

        Input:
            None

        Output:
            auto (int) : measurement autorange state
        """
        return self._visainstrument.query(':SENS:RANG:AUTO?').replace('\n', '')

    def _do_set_sense_range_auto(self, auto):
        """
        Sets the measurement autorange state (ON or OFF).

        Input:
            auto (int) : measurement autorange state

        Output:
            None
        """
        self._visainstrument.write(':SENS:RANG:AUTO %s' % auto)

    def _do_get_sense_integration_time(self):
        """
        Queries the current integration time (250 μs, 1 ms, 4 ms,
        16.6 ms or 20 ms, 100 ms, or 200 ms).

        Input:
            None

        Output:
            time (float) : integration time in seconds
        """
        return self._visainstrument.query(':SENS:ITIM?').replace('\n', '')

    def _do_set_sense_integration_time(self, time):
        """
        Sets the integration time to the smallest setting that includes
        the parameter (250 μs, 1 ms, 4 ms, 16.6 ms or 20 ms, 100 ms, or
        200 ms).

        Input:
            time (float) : integration time in seconds

        Output:
            None
        """
        self._visainstrument.write(':SENS:ITIM %e' % time)

    def _do_get_sense_delay(self):
        """
        Queries the current measurement delay in seconds.

        Input:
            None

        Output:
            delay (float) : measurement delay in seconds
        """
        return self._visainstrument.query(':SENS:DEL?').replace('\n', '')

    def _do_set_sense_delay(self, delay):
        """
        Sets the measurement delay in seconds.

        Input:
            delay (float) : measurement delay in seconds

        Output:
            None
        """
        return self._visainstrument.write(':SENS:DEL %e' % delay)

    def _do_get_sense_auto_zero_state(self):
        """
        Queries the current autozero state (ON or OFF).

        Input:
            None

        Output:
            state (int) : autozero state
        """
        return self._visainstrument.query(':SENS:AZER?').replace('\n', '')

    def _do_set_sense_auto_zero_state(self, state):
        """
        Sets the autozero state (ON or OFF).

        Input:
            state (int) : autozero state

        Output:
            None
        """
        self._visainstrument.write(':SENS:AZER %s' % state)

    def sense_auto_zero_execute(self):
        """
        TODO implement me
        """

    def _do_get_sense_average_state(self):
        """
        Queries the current average state (ON or OFF).

        Input:
            None

        Output:
            state (int) : average state
        """
        return self._visainstrument.query(':SENS:AVER?').replace('\n', '')

    def _do_set_sense_average_state(self, state):
        """
        Sets the average state (ON or OFF).

        Input:
            state (int) : average state

        Output:
            None
        """
        self._visainstrument.write(':SENS:AVER %s' % state)

    def _do_get_sense_average_mode(self):
        """
        Queries the current average mode (block or moving average).

        Input:
            None

        Output:
            mode (int) : average mode (block or moving average)
        """
        format_map = self.get_parameters()['sense_average_mode']['format_map']
        return list(format_map.keys())[list(format_map.values()).index(
            self._visainstrument.query(':SENS:AVER:MODE?').replace('\n', ''))]

    def _do_set_sense_average_mode(self, mode):
        """
        Sets the average mode (block or moving average).

        Input:
            mode (int) : average mode (block or moving average)

        Output:
            None
        """
        self._visainstrument.write(
            ':SENS:AVER:MODE %s' % self.get_parameters()['sense_average_mode']\
                ['format_map'][mode])

    def _do_get_sense_average_count(self):
        """
        Queries the current average count.

        Input:
            None

        Output:
            count (int) : average count
        """
        return self._visainstrument.query(':SENS:AVER:COUN?').replace('\n', '')

    def _do_set_sense_average_count(self, count):
        """
        Sets the average count.

        Input:
            count (int) : average count

        Output:
            None
        """
        self._visainstrument.write(':SENS:AVER:COUN %i' % count)

    def _do_get_sense_auto_change(self):
        """
        Queries the current auto-V/I mode (ON or OFF).

        Input:
            None

        Output:
            mode (int) : auto-V/I mode
        """
        return self._visainstrument.query(':SENS:ACH?').replace('\n', '')

    def _do_set_sense_auto_change(self, mode):
        """
        Sets the auto-V/I mode (ON or OFF).

        Input:
            mode (int) : auto-V/I mode

        Output:
            None
        """
        self._visainstrument.write(':SENS:ACH %s' % mode)

    def _do_get_sense_remote_sense(self):
        """
        Queries the current four-wire measurement (remote sense)
        setting (ON or OFF).

        Input:
            None

        Output:
            sense (int) : four-wire measurement setting
        """
        return self._visainstrument.query(':SENS:RSEN?').replace('\n', '')

    def _do_set_sense_remote_sense(self, sense):
        """
        Sets the four-wire measurement (remote sense) setting (ON or
        OFF).

        Input:
            sense (int) : four-wire measurement setting

        Output:
            None
        """
        self._visainstrument.write(':SENS:RSEN %s' % sense)


    # trigger commands (trigger group)
    # ...


    # computation commands (calculate group)
    # ...


    # store/recall commands (trace group)
    # ...


    # external input/output commands (route group)
    # ...


    # system commands (system group)
    # ...


    # measured value read commands (initiate, fetch, and read group)

    def initiate(self):
        """
        Starts a new measurement.
        """
        self._visainstrument.write(':INIT')

    def fetch(self):
        """
        Queries the measured results.

        Returns
        -------
        out : TODO what is the type? what should it be?
        """
        return self._visainstrument.query(':FETCH?').replace('\n', '')

    def read(self):
        """
        Starts a new measurement and queries the measured results.

        This command is equivalent to :INIT;:FETCH?.

        Returns
        -------
        out : TODO what is the type? what should it be?
        """
        return self._visainstrument.query(':READ?').replace('\n', '')


    # common command group

    def reset(self):
        """
        Resets the GS610 to factory default settings.

        This command is equivalent to setting the file name of the
        :SYST:SET:LOAD command to `Default.txt`.
        """
        self._visainstrument.write('*RST')


    def gateset(self, xend, intrasweep_delay, ramp_rate):
        """
        TODO add docstring
        """
        # self._do_set_source_voltage_range(xend)

        # self._do_set_sense(1)
        # self._do_set_sense_function(1)

        # self._do_set_trigger_source(0)
        # self._do_set_trigger_timer(intrasweep_delay)

        # self._do_set_output_state('on')

        # xcurrent = self._do_get_source_voltage_level()

        # ramp_steps = int(np.ceil(np.abs((xcurrent - xend) / ramp_rate) + 1))
        # temp_ramp = np.linspace(xcurrent, xend, ramp_steps)

        # for i in temp_ramp[1:]:
        #     self._do_set_source_voltage_level(
        #         xend if (i > xend) ^ (xcurrent > xend) else i)

        # self._do_set_source_voltage_level(xend)
