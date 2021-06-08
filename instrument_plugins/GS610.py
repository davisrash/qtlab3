"""
TODO add docstring
"""

# import logging

import visa
import numpy as np
import source.qt as qt
from source.instrument import Instrument

#######################################################################
# TODO:
#  - continue implementing commented places
#  - add docstring
#  - add logging
#  - add tags to relevant parameters
#  - add 0/1/False/True options to `off`/`on` parameters
#  - review parameter/function/function parameter names
#  - improve instrument.py to work with list type with parameters
#######################################################################


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
        # TODO add min/max/up/down options
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
        # TODO add 1/0 options
        self.add_parameter('source_range_auto', type=str,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the source auto range (ON or OFF) or "
                               "queries the current setting.",
                           option_list=('on', 'off'))
        # TODO add 1/0 options
        self.add_parameter('source_protection_state', type=str,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the limiter state (ON or OFF) or queries "
                               "the current setting.",
                           option_list=('on', 'off'))
        # TODO add 1/0 options
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
        self.add_function('sense_auto_zero_execute')
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
        self.add_parameter('trigger_source', type=str,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the trigger source (constant period "
                               "timer, external trigger, or no trigger wait) "
                               "or queries the current setting.",
                           option_list=('timer', 'external', 'immediate'))
        self.add_parameter('trigger_timer', type=float,
                           flags=Instrument.FLAG_GETSET,
                           doc="Sets the period of the constant period timer "
                               "or queries the current setting.")

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
        self.add_function('clear_status')
        # self.add_function('read_status_byte')
        # self.add_function('service_request_enable')
        # self.add_function('standard_event_status_register')
        # self.add_function('standard_event_status_enable')
        # self.add_function('operation_complete')
        # self.add_function('is_operation_complete')
        # self.add_function('wait_to_continue')

        # hbar module commands
        self.add_function('ramp_to_voltage')

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
            A list of the program sweep pattern files.
        """
        catalog = self._visainstrument.query(':SOUR:LIST:CAT?').replace(
            '\n', '')
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

    def _do_get_source_voltage_range(self):
        """
        Queries and returns the current voltage source range setting
        (200 mV, 2 V, 12 V, 20 V, 30 V, 60 V, or 110 V).

        Returns
        -------
        out : float
            The current voltage source range setting.
        """
        return self._visainstrument.query(':SOUR:VOLT:RANG?')

    def _do_set_source_voltage_range(self, voltage_range):
        """
        Sets the voltage source range setting (200 mV, 2 V, 12 V, 20 V,
        30 V, 60 V, or 110 V).

        If the range setting is changed when auto range is ON by the
        SOUR:VOLT:RANG:AUTO ON command, auto range is automatically
        disabled.

        Parameters
        ----------
        voltage_range : float
            Sets the voltage source range to the smallest range setting
            that includes the specified value.
        """
        self._visainstrument.write(':SOUR:VOLT:RANG {}'.format(voltage_range))

    def _do_get_source_voltage_level(self):
        """
        Queries and returns the current voltage source level value in
        volts.

        Returns
        -------
        out : float
            The voltage level in volts.
        """
        return self._visainstrument.query(':SOUR:VOLT:LEV?')

    def _do_set_source_voltage_level(self, level):
        """
        Sets the voltage source level value in volts.

        Parameters
        ----------
        level : float
            Sets the voltage level to the specified value in volts.
        """
        self._visainstrument.write(':SOUR:VOLT:LEV {}'.format(level))

    def _do_get_source_voltage_pulse_base(self):
        """
        Queries and returns the current pulse base value for voltage
        pulse generation in volts.

        Returns
        -------
        out : float
            The pulse base value in volts.
        """
        return self._visainstrument.query(':SOUR:VOLT:PBAS?')

    def _do_set_source_voltage_pulse_base(self, pulse_base):
        """
        Sets the pulse base value for voltage generation in volts.

        Parameters
        ----------
        pulse_base : float
            Sets the pulse base value to the specified value in volts.
        """
        self._visainstrument.write(':SOUR:VOLT:PBAS {}'.format(pulse_base))

    def _do_get_source_voltage_protection_upper_limit(self):
        """
        Queries and returns the current upper voltage limiter value
        (for generating current) in volts.

        Note that the voltage limiter is activated when the source
        function is set to current (:SOUR:FUNC CURR).

        Returns
        -------
        out : float
            The limiter value.
        """
        return self._visainstrument.query(':SOUR:VOLT:PROT:ULIM?')

    def _do_set_source_voltage_protection_upper_limit(self, limit):
        """
        Sets the upper voltage limiter value (for generating current)
        in volts.

        Note that the voltage limiter is activated when the source
        function is set to current (:SOUR:FUNC CURR).

        Parameters
        ----------
        limit : float
            Sets the limiter value to the specified value.
        """
        self._visainstrument.write(':SOUR:VOLT:PROT:ULIM {}'.format(limit))

    def _do_get_source_voltage_protection_lower_limit(self):
        """
        TODO add docstring
        """
        return self._visainstrument.query(':SOUR:VOLT:PROT:LLIM?')

    def _do_set_source_voltage_protection_lower_limit(self, limit):
        """
        TODO add docstring
        """
        self._visainstrument.write(':SOUR:VOLT:PROT:LLIM {}'.format(limit))

    def _do_get_source_voltage_sweep_start(self):
        """
        TODO add docstring
        """
        return self._visainstrument.query(':SOUR:VOLT:SWE:STAR?')

    def _do_set_source_voltage_sweep_start(self, start):
        """
        TODO add docstring
        """
        self._visainstrument.write(':SOUR:VOLT:SWE:STAR {}'.format(start))

    def _do_get_source_voltage_sweep_stop(self):
        """
        TODO add docstring
        """
        return self._visainstrument.query(':SOUR:VOLT:SWE:STOP?')

    def _do_set_source_voltage_sweep_stop(self, stop):
        """
        TODO add docstring
        """
        self._visainstrument.write(':SOUR:VOLT:SWE:STOP {}'.format(stop))

    def _do_get_source_voltage_sweep_step(self):
        """
        TODO add docstring
        """
        return self._visainstrument.query(':SOUR:VOLT:SWE:STEP?')

    def _do_set_source_voltage_sweep_step(self, step):
        """
        TODO add docstring
        """
        self._visainstrument.write(':SOUR:VOLT:SWE:STEP {}'.format(step))

    def _do_get_source_voltage_sweep_points(self):
        """
        TODO add docstring
        """
        return self._visainstrument.query(':SOUR:VOLT:SWE:POIN?')

    def _do_set_source_voltage_sweep_points(self, points):
        """
        TODO add docstring
        """
        self._visainstrument.write(':SOUR:VOLT:SWE:POIN {}'.format(points))

    def _do_get_source_voltage_zero_impedance(self):
        """
        TODO add docstring
        """
        format_map = {'HIGH': 'high', 'LOW': 'low'}
        impedance = self._visainstrument.query(':SOUR:VOLT:ZERO:IMP?').replace(
            '\n', '')
        return format_map[impedance]

    def _do_set_source_voltage_zero_impedance(self, impedance):
        """
        TODO add docstring
        """
        self._visainstrument.write(':SOUR:VOLT:ZERO:IMP {}'.format(impedance))

    def _do_get_source_voltage_zero_offset(self):
        """
        TODO add docstring
        """
        return self._visainstrument.query(':SOUR:VOLT:ZERO:OFFS?')

    def _do_set_source_voltage_zero_offset(self, offset):
        """
        TODO add docstring
        """
        self._visainstrument.write(':SOUR:VOLT:ZERO:OFFS {}'.format(offset))

    def _do_get_source_current_range(self):
        """
        TODO add docstring
        """
        return self._visainstrument.query(':SOUR:CURR:RANG?')

    def _do_set_source_current_range(self, current_range):
        """
        TODO add docstring
        """
        self._visainstrument.write(':SOUR:CURR:RANG {}'.format(current_range))

    def _do_get_source_current_level(self):
        """
        TODO add docstring
        """
        return self._visainstrument.query(':SOUR:CURR:LEV?')

    def _do_set_source_current_level(self, level):
        """
        TODO add docstring
        """
        self._visainstrument.write(':SOUR:CURR:LEV {}'.format(level))

    def _do_get_source_current_pulse_base(self):
        """
        TODO add docstring
        """
        return self._visainstrument.query(':SOUR:CURR:PBAS?')

    def _do_set_source_current_pulse_base(self, pulse_base):
        """
        TODO add docstring
        """
        self._visainstrument.write(':SOUR:CURR:PBAS {}'.format(pulse_base))

    def _do_get_source_current_protection_upper_limit(self):
        """
        TODO add docstring
        """
        return self._visainstrument.query(':SOUR:CURR:PROT:ULIM?')

    def _do_set_source_current_protection_upper_limit(self, limit):
        """
        TODO add docstring
        """
        self._visainstrument.write(':SOUR:CURR:PROT:ULIM {}'.format(limit))

    def _do_get_source_current_protection_lower_limit(self):
        """
        TODO add docstring
        """
        return self._visainstrument.query(':SOUR:CURR:PROT:LLIM?')

    def _do_set_source_current_protection_lower_limit(self, limit):
        """
        TODO add docstring
        """
        self._visainstrument.write(':SOUR:CURR:PROT:LLIM {}'.format(limit))

    def _do_get_source_current_sweep_start(self):
        """
        TODO add docstring
        """
        return self._visainstrument.query(':SOUR:CURR:SWE:STAR?')

    def _do_set_source_current_sweep_start(self, start):
        """
        TODO add docstring
        """
        self._visainstrument.write(':SOUR:CURR:SWE:STAR {}'.format(start))

    def _do_get_source_current_sweep_stop(self):
        """
        TODO add docstring
        """
        return self._visainstrument.query(':SOUR:CURR:SWE:STOP?')

    def _do_set_source_current_sweep_stop(self, stop):
        """
        TODO add docstring
        """
        self._visainstrument.write(':SOUR:CURR:SWE:STOP {}'.format(stop))

    def _do_get_source_current_sweep_step(self):
        """
        TODO add docstring
        """
        return self._visainstrument.query(':SOUR:CURR:SWE:STEP?')

    def _do_set_source_current_sweep_step(self, step):
        """
        TODO add docstring
        """
        self._visainstrument.write(':SOUR:CURR:SWE:STEP {}'.format(step))

    def _do_get_source_current_sweep_points(self):
        """
        TODO add docstring
        """
        return self._visainstrument.query(':SOUR:CURR:SWE:POIN?')

    def _do_set_source_current_sweep_points(self, points):
        """
        TODO add docstring
        """
        self._visainstrument.write(':SOUR:CURR:SWE:POIN {}'.format(points))

    def _do_get_source_current_zero_impedance(self):
        """
        TODO add docstring
        """
        format_map = {'HIGH': 'high', 'LOW': 'low'}
        impedance = self._visainstrument.query(':SOUR:CURR:ZERO:IMP?').replace(
            '\n', '')
        return format_map[impedance]

    def _do_set_source_current_zero_impedance(self, impedance):
        """
        TODO add docstring
        """
        self._visainstrument.write(':SOUR:CURR:ZERO:IMP {}'.format(impedance))

    def _do_get_source_current_zero_offset(self):
        """
        TODO add docstring
        """
        return self._visainstrument.query(':SOUR:CURR:ZERO:OFFS?')
    def _do_set_source_current_zero_offset(self, offset):
        """
        TODO add docstring
        """
        self._visainstrument.write(':SOUR:CURR:ZERO:OFFS {}'.format(offset))

    def _do_get_source_range_auto(self):
        """
        Queries and returns the current source auto range setting (ON
        or OFF).

        Returns
        -------
        out : str
            If `on`, currently ON. If `off`, currently OFF.
        """
        format_map = {'0': 'off', '1': 'on'}
        auto = self._visainstrument.query(':SOUR:VOLT:RANG:AUTO?').replace(
            '\n', '')
        return format_map[auto]

    def _do_set_source_range_auto(self, auto):
        """
        Sets the source auto range setting (ON or OFF).

        Parameters
        ----------
        auto : str
            If `on`, turns auto range ON. If `off`, turns auto range
            OFF.
        """
        self._visainstrument.write(':SOUR:VOLT:RANG:AUTO {}'.format(auto))

    def _do_get_source_protection_state(self):
        """
        Queries and returns the current limiter state (ON or OFF).

        Returns
        -------
        out : str
            If `on`, currently ON. If `off`, currently OFF.
        """
        format_map = {'0': 'off', '1': 'on'}
        state = self._visainstrument.query(':SOUR:VOLT:PROT:STAT?').replace(
            '\n', '')
        return format_map[state]

    def _do_set_source_protection_state(self, state):
        """
        Sets the limiter state (ON or OFF).

        Parameters
        ----------
        state : str
            If `on`, turns the limiter ON. If `off`, turns the limiter
            OFF.
        """
        self._visainstrument.write(':SOUR:VOLT:PROT:STAT {}'.format(state))

    def _do_get_source_protection_linkage(self):
        """
        Queries and returns the current limiter tracking state (ON or
        OFF).

        Returns
        -------
        out : str
            If `on`, currently ON. If `off`, currently OFF.
        """
        format_map = {'0': 'off', '1': 'on'}
        state = self._visainstrument.query(':SOUR:VOLT:PROT:LINK?').replace(
            '\n', '')
        return format_map[state]

    def _do_set_source_protection_linkage(self, state):
        """
        Sets the limiter tracking state (ON or OFF).

        Parameters
        ----------
        state : str
            If `on`, turns limiter tracking ON. If `off`, turns limiter
            tracking OFF.
        """
        self._visainstrument.write(':SOUR:VOLT:PROT:LINK {}'.format(state))

    def _do_get_source_sweep_spacing(self):
        """
        Queries and returns the current sweep mode (linear or log).

        This setting is used when the source pattern is set to sweep
        (:SOUR:MODE SWE).

        Returns
        -------
        out : str
            If `linear`, currently set to linear. If `log`, currently
            set to logarithmic.
        """
        format_map = {'LIN': 'linear', 'LOG': 'log'}
        spacing = self._visainstrument.query(':SOUR:VOLT:SWE:SPAC?').replace(
            '\n', '')
        return format_map[spacing]

    def _do_set_source_sweep_spacing(self, spacing):
        """
        Sets the sweep mode (linear or log).

        This setting is used when the source pattern is set to sweep
        (:SOUR:MODE SWE).

        Parameters
        ----------
        spacing : str
            If `linear`, sets the sweep mode to linear. If `log`, sets
            the sweep mode to logarithmic.
        """
        self._visainstrument.write(':SOUR:VOLT:SWE:SPAC {}'.format(spacing))


    # sweep commands (sweep group)

    def sweep_trigger(self):
        """
        TODO add docstring
        """
        self._visainstrument.write(':SWE:TRIG')

    def _do_get_sweep_count(self):
        """
        TODO add docstring
        """
        return self._visainstrument.query(':SWE:COUN?')

    def _do_set_sweep_count(self, count):
        """
        TODO add docstring
        """
        self._visainstrument.write(':SWE:COUN {}'.format(count))

    def _do_get_sweep_last(self):
        """
        TODO add docstring
        """
        format_map = {'KEEP': 'keep', 'RET': 'return'}
        mode = self._visainstrument.query(':SWE:LAST?').replace('\n', '')
        return format_map[mode]

    def _do_set_sweep_last(self, mode):
        """
        TODO add docstring
        """
        self._visainstrument.write(':SWE:LAST {}'.format(mode))


    # measurement commands (sense group)

    def _do_get_sense_state(self):
        """
        TODO add docstring
        """
        format_map = {'0': 'off', '1': 'on'}
        state = self._visainstrument.query(':SENS:STAT?').replace('\n', '')
        return format_map[state]

    def _do_set_sense_state(self, state):
        """
        TODO add docstring
        """
        self._visainstrument.write(':SENS:STAT {}'.format(state))

    def _do_get_sense_function(self):
        """
        TODO add docstring
        """
        format_map = {'VOLT': 'voltage',
                      'CURR': 'current',
                      'RES': 'resistance'}
        function = self._visainstrument.query(':SENS:FUNC?').replace('\n', '')
        return format_map[function]

    def _do_set_sense_function(self, function):
        """
        TODO add docstring
        """
        self._visainstrument.write(':SENS:FUNC {}'.format(function))

    def _do_get_sense_range_auto(self):
        """
        TODO add docstring
        """
        format_map = {'0': 'off', '1': 'on'}
        auto = self._visainstrument.query(':SENS:RANG:AUTO?').replace('\n', '')
        return format_map[auto]

    def _do_set_sense_range_auto(self, auto):
        """
        TODO add docstring
        """
        self._visainstrument.write(':SENS:RANG:AUTO {}'.format(auto))

    def _do_get_sense_integration_time(self):
        """
        TODO add docstring
        """
        return self._visainstrument.query(':SENS:ITIM?')

    def _do_set_sense_integration_time(self, time):
        """
        TODO add docstring
        """
        self._visainstrument.write(':SENS:ITIM {}'.format(time))

    def _do_get_sense_delay(self):
        """
        TODO add docstring
        """
        return self._visainstrument.query(':SENS:DEL?')

    def _do_set_sense_delay(self, delay):
        """
        TODO add docstring
        """
        return self._visainstrument.write(':SENS:DEL {}'.format(delay))

    def _do_get_sense_auto_zero_state(self):
        """
        TODO add docstring
        """
        format_map = {'0': 'off', '1': 'on'}
        state = self._visainstrument.query(':SENS:AZER:STAT?').replace(
            '\n', '')
        return format_map[state]

    def _do_set_sense_auto_zero_state(self, state):
        """
        TODO add docstring
        """
        self._visainstrument.write(':SENS:AZER:STAT {}'.format(state))

    def sense_auto_zero_execute(self):
        """
        TODO add docstring
        """
        self._visainstrument.write(':SENS:AZER:EXEC')

    def _do_get_sense_average_state(self):
        """
        TODO add docstring
        """
        format_map = {'0': 'off', '1': 'on'}
        state = self._visainstrument.query(':SENS:AVER:STAT?').replace(
            '\n', '')
        return format_map[state]

    def _do_set_sense_average_state(self, state):
        """
        TODO add docstring
        """
        self._visainstrument.write(':SENS:AVER:STAT {}'.format(state))

    def _do_get_sense_average_mode(self):
        """
        TODO add docstring
        """
        format_map = {'BLOC': 'block', 'MOV': 'moving'}
        mode = self._visainstrument.query(':SENS:AVER:MODE?').replace('\n', '')
        return format_map[mode]

    def _do_set_sense_average_mode(self, mode):
        """
        TODO add docstring
        """
        self._visainstrument.write(':SENS:AVER:MODE {}'.format(mode))

    def _do_get_sense_average_count(self):
        """
        TODO add docstring
        """
        return self._visainstrument.query(':SENS:AVER:COUN?')

    def _do_set_sense_average_count(self, count):
        """
        TODO add docstring
        """
        self._visainstrument.write(':SENS:AVER:COUN {}'.format(count))

    def _do_get_sense_auto_change(self):
        """
        TODO add docstring
        """
        format_map = {'0': 'off', '1': 'on'}
        mode = self._visainstrument.query(':SENS:ACH?').replace('\n', '')
        return format_map[mode]

    def _do_set_sense_auto_change(self, mode):
        """
        TODO add docstring
        """
        self._visainstrument.write(':SENS:ACH {}'.format(mode))

    def _do_get_sense_remote_sense(self):
        """
        TODO add docstring
        """
        format_map = {'0': 'off', '1': 'on'}
        sense = self._visainstrument.query(':SENS:RSEN?').replace('\n', '')
        return format_map[sense]

    def _do_set_sense_remote_sense(self, sense):
        """
        TODO add docstring
        """
        self._visainstrument.write(':SENS:RSEN {}'.format(sense))


    # trigger commands (trigger group)

    def _do_get_trigger_source(self):
        """
        TODO add docstring
        """
        format_map = {'TIM': 'timer', 'EXT': 'external', 'IMM': 'immediate'}
        source = self._visainstrument.query(':TRIG:SOUR?').replace('\n', '')
        return format_map[source]

    def _do_set_trigger_source(self, source):
        """
        TODO add docstring
        """
        self._visainstrument.write(':TRIG:SOUR {}'.format(source))

    def _do_get_trigger_timer(self):
        """
        TODO add docstring
        """
        return self._visainstrument.query(':TRIG:TIM?')

    def _do_set_trigger_timer(self, period):
        """
        TODO add docstring
        """
        self._visainstrument.write(':TRIG:TIM {}'.format(period))


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
        out : float
            The result of the measurement.
        """
        return float(self._visainstrument.query(':READ?').replace('\n', ''))


    # common command group

    def reset(self):
        """
        Resets the GS610 to factory default settings.

        This command is equivalent to setting the file name of the
        :SYST:SET:LOAD command to `Default.txt`.
        """
        self._visainstrument.write('*RST')

    def clear_status(self):
        """
        Clears the event register and error queue.
        """
        self._visainstrument.write('*CLS')


    # hbar module commands
    def ramp_to_voltage(self, stop, step, channel=None):
        """
        Ramps the source voltage from the current level to the desired
        level in linear steps.

        Parameters
        ----------
        stop : float
            The voltage to be reached by the end of the sweep in volts.

        step : float
            The ramp step size in volts.

        channel : int
            Selects the channel to ramp. Included for compatibility
            with meters with channels, as the GS610 uses only one.
        """
        # for compatibility with meters with channels
        assert channel is None

        start = float(self._visainstrument.query(':SOUR:VOLT:LEV?'))

        # source settings
        self._visainstrument.write(':SOUR:FUNC VOLT')
        self._visainstrument.write(':SOUR:VOLT:RANG {}'.format(
            max(start, stop)))
        self._visainstrument.write(':SOUR:CURR:PROT:LINK ON')
        self._visainstrument.write(':SOUR:CURR:PROT:ULIM 0.5')
        self._visainstrument.write(':SOUR:CURR:PROT:STAT ON')

        # trigger settings
        self._visainstrument.write(':TRIG:SOUR TIM')
        # self._visainstrument.write(':TRIG:TIM 500E-6')
        self._visainstrument.write(':SOUR:DEL MIN')

        # step voltage from start to stop
        ramp = np.linspace(start, stop,
                           int(np.ceil(np.abs((stop - start) / step)) + 1))
        for i in ramp[1:]:
            self._visainstrument.write(':SOUR:VOLT:LEV {}'.format(i))
            qt.msleep(0.001)
