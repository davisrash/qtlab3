"""
TODO add docstring
"""

import logging
from time import time, sleep

import visa
import numpy as np
import source.qt as qt
from source.instrument import Instrument


def bool_to_str(val):
    '''
    Function to convert boolean to 'ON' or 'OFF'
    '''
    if val:
        return "ON"

    return "OFF"


class Keithley_2400(Instrument):
    '''
    This is the driver for the Keithley 2400

    Usage:
    Initialize with
    <name> = instruments.create('<name>', 'Keithley_2400',
        address='<GBIP address>',
        reset=<bool>,
        change_display=<bool>,
        change_autozero=<bool>)
    '''

    def __init__(self, name, address, reset=False, change_display=True,
                 change_autozero=True):
        '''
        Initializes the Keithley_2000, and communicates with the wrapper.

        Input:
            name (string)           : name of the instrument
            address (string)        : GPIB address
            reset (bool)            : resets to default values
            change_display (bool)   : If True (default), automatically turn off
                                        display during measurements.
            change_autozero (bool)  : If True (default), automatically turn off
                                        autozero during measurements.
        Output:
            None
        '''
        # Initialize wrapper functions
        logging.info('Initializing instrument Keithley_2000')
        Instrument.__init__(self, name, tags=['physical'])

        # Add some global constants
        self._address = address
        self.name = name
        #self._visainstrument = visa.instrument(self._address)
        rm = visa.ResourceManager()
        self._visainstrument = rm.get_instrument(self._address)

        self.modes = ['VOLT:AC', 'VOLT:DC', 'CURR:AC', 'CURR:DC', 'RES',
                      'FRES', 'TEMP', 'FREQ']
        self.change_display = change_display
        self.change_autozero = change_autozero
        self.averaging_types = ['MOV', 'REP']
        self.trigger_sent = False

        self.add_function('enable_source')
        self.add_function('disable_source')
        self.add_function('measure_resistance')
        self.add_function('measure_voltage')
        self.add_function('measure_current')
        self.add_function('auto_range_source')
        self.add_function('beep')
        self.add_function('triad')
        self.add_function('check_errors')

        self.add_function('set_current')
        self.add_function('set_current_source')
        self.add_function('set_current_comp')

        self.add_function('set_voltage')
        self.add_function('set_voltage_source')
        self.add_function('set_voltage_comp')

        self.add_function('set_res_range')

        self.add_function('reset')
        self.add_function('ramp_to_current')
        self.add_function('ramp_to_voltage')
        self.add_function('trigger')
        self.add_function('trigger_immediately')
        self.add_function('trigger_on_bus')
        self.add_function('set_trigger_counts')
        self.add_function('disable_buffer')
        self.add_function('sample_continuously')
        self.add_function('set_timed_arm')
        self.add_function('trigger_on_external')
        self.add_function('output_trigger_on_external')
        self.add_function('disable_output_trigger')

        self.add_function('get_resistance')
        self.add_function('get_current')
        self.add_function('get_voltage')

        self.add_function('set_mode')
        self.add_function('read_val')

        if reset:
            self.reset()

    def enable_source(self):
        """ Enables the source of current or voltage depending on the
        configuration of the instrument. """
        self._visainstrument.write("OUTPUT ON")

    def disable_source(self):
        """ Disables the source of current or voltage depending on the
        configuration of the instrument. """
        self._visainstrument.write("OUTPUT OFF")

    def measure_resistance(self, nplc=1, resistance=2.1e5, auto_range=True):
        """ Configures the measurement of resistance.

        :param nplc: Number of power line cycles (NPLC) from 0.01 to 10
        :param resistance: Upper limit of resistance in Ohms, from -210 MOhms to 210 MOhms
        :param auto_range: Enables auto_range if True, else uses the set resistance
        """

        logging.debug("%s is measuring resistance." % self.name)
        self._visainstrument.write(":SENS:FUNC 'RES';")
        self._visainstrument.write(":SENS:RES:MODE MAN;")
        self._visainstrument.write(":SENS:RES:NPLC %f;:FORM:ELEM RES;" % nplc)

        if auto_range:
            self._visainstrument.write(":SENS:RES:RANG:AUTO 1;")
        else:
            self.set_res_range(resistance)
        self.check_errors()

    def measure_voltage(self, nplc=1, voltage=21.0, auto_range=True):
        """ Configures the measurement of voltage.

        :param nplc: Number of power line cycles (NPLC) from 0.01 to 10
        :param voltage: Upper limit of voltage in Volts, from -210 V to 210 V
        :param auto_range: Enables auto_range if True, else uses the set voltage
        """
        logging.debug("%s is measuring voltage." % self.name)

        self._visainstrument.write(":SENS:FUNC 'VOLT';")
        self._visainstrument.write(
            ":SENS:VOLT:NPLC %f;:FORM:ELEM VOLT;" % nplc)

        if auto_range:
            self._visainstrument.write(":SENS:VOLT:RANG:AUTO 1;")
        else:
            # self._visainstrument.write(":SENS:VOLT:RANG?")
            self._visainstrument.write(
                ":SENS:VOLT:RANG:AUTO 0;:SENS:VOLT:RANG %g" % voltage)
        self.check_errors()

    def measure_current(self, nplc=1, current=1.05e-4, auto_range=True):
        """ Configures the measurement of current.

        :param nplc: Number of power line cycles (NPLC) from 0.01 to 10
        :param current: Upper limit of current in Amps, from -1.05 A to 1.05 A
        :param auto_range: Enables auto_range if True, else uses the set current
        """
        logging.debug("%s is measuring current." % self.name)

        self._visainstrument.write(":SENS:FUNC 'CURR';")
        self._visainstrument.write(
            ":SENS:CURR:NPLC %f;:FORM:ELEM CURR;" % nplc)

        if auto_range:
            self._visainstrument.write(":SENS:CURR:RANG:AUTO 1;")
        else:
            self._visainstrument.write(":SENS:CURR:RANG?")
            self._visainstrument.write(
                ":SENS:CURR:RANG:AUTO 0;:SENS:CURR:RANG %g" % current)

        self.check_errors()

    def set_current_source(self, range):
        # range of current in Amps
        # maximum range [-1.05, 1.05]

        self._visainstrument.write(":SOUR:FUNC CURR")
        self._visainstrument.write(":SOUR:CURR:RANG %g" % range)

    def set_current_comp(self, max):
        # range of current in Amps
        # Measure range ---- Max compliance value (+/-)
        # 1 uA --- 1.05 uA
        # 10 uA --- 10.5 uA
        # 100 uA --- 105 uA
        # 1 mA --- 1.05 mA
        # 10 mA --- 10.5 mA
        # 100 mA --- 105 mA
        # 1 A --- 1.05 A

        self._visainstrument.write(":SENS:FUNC 'CURR';")
        self._visainstrument.write(":SENS:CURR:PROT %g" % max)
        #self._visainstrument.write(":SENS:CURR:RANG:AUTO 0;:SENS:CURR:RANG %g" % range)

    def set_voltage_source(self, range):
        # range of voltage in Volts
        # maximum range [-210, 210]

        self._visainstrument.write(":SOUR:FUNC VOLT")
        self._visainstrument.write(":SOUR:VOLT:RANG %g" % range)
        #self._visainstrument.write(":SENS:VOLT:RANG %g" % range)

    def set_voltage_comp(self, max):
        # range of voltage in Volts
        # Measure range ---- Max compliance value (+/-)
        # 200 mV --- 210mV
        # 2V --- 2.1V
        # 20V --- 21 V
        # 200V --- 210 V

        self._visainstrument.write(":SENS:FUNC 'VOLT';")
        self._visainstrument.write(":SENS:VOLT:PROT %g" % max)
        #self._visainstrument.write(":SENS:CURR:RANG:AUTO 0;:SENS:CURR:RANG %g" % range)

    def set_res_range(self, range):
        self._visainstrument.write(":SENS:RES:RANG %g" % range)

    def auto_range_source(self):
        """ Configures the source to use an automatic range.
        """
        # if self.source_mode == 'current':
        #    self._visainstrument.write(":SOUR:CURR:RANG:AUTO 1")
        # else:
        #    self._visainstrument.write(":SOUR:VOLT:RANG:AUTO 1")

    def set_current(self, target_current):
        #target_current in Amps
        logging.debug("%s is sourcing current." % self.name)

        #self._visainstrument.write(":SOUR:FUNC CURR")
        self._visainstrument.write(":SOUR:CURR:LEV %g" % target_current)

        self.check_errors()

    def set_voltage(self, target_voltage):
        #target_current in Amps
        logging.debug("%s is sourcing voltage." % self.name)

        #self._visainstrument.write(":SOUR:FUNC VOLT")
        self._visainstrument.write(":SOUR:VOLT:LEV %g" % target_voltage)

        self.check_errors()

    def beep(self, frequency, duration):
        """ Sounds a system beep.

        :param frequency: A frequency in Hz between 65 Hz and 2 MHz
        :param duration: A time in seconds between 0 and 7.9 seconds
        """
        self._visainstrument.write(":SYST:BEEP %g, %g" % (frequency, duration))

    def triad(self, base_frequency, duration):
        """ Sounds a musical triad using the system beep.

        :param base_frequency: A frequency in Hz between 65 Hz and 1.3 MHz
        :param duration: A time in seconds between 0 and 7.9 seconds
        """
        self.beep(base_frequency, duration)
        sleep(duration)
        self.beep(base_frequency * 5.0 / 4.0, duration)
        sleep(duration)
        self.beep(base_frequency * 6.0 / 4.0, duration)

    @property
    def error(self):
        """ Returns a tuple of an error code and message from a 
        single error. """
        #err = self.values(":system:error?")
        err = self._visainstrument.query(":system:error?")

        if len(err) < 2:
            err = self._visainstrument.read()  # Try reading again

        s = err.split(',')

        code = int(s[0])
        message = s[1].replace('"', '')

        return (code, message)

    def check_errors(self):
        """ Logs any system errors reported by the instrument.
        """
        code, message = self.error

        while code != 0:
            t = time()
            #logging.warning("Keithley 2400 reported error: %d, %s" % (code, message))
            print("Keithley 2400 reported error: %d, %s" % (code, message))
            code, message = self.error
            if (time() - t) > 10:
                logging.warning("Timed out for Keithley 2400 error retrieval.")

    def reset(self):
        """ Resets the instrument and clears the queue.  """
        self._visainstrument.write("status:queue:clear;*RST;:stat:pres;:*CLS;")

    '''
    def ramp_to_current(self, target_current, steps=30, pause=20e-3):
        """ Ramps to a target current from the set current value over 
        a certain number of linear steps, each separated by a pause duration.

        :param target_current: A current in Amps
        :param steps: An integer number of steps
        :param pause: A pause duration in seconds to wait between steps
        """
        currents = np.linspace(
            self.source_current,
            target_current,
            steps
        )
        for current in currents:
            self.source_current = current
            time.sleep(pause)
    '''

    def ramp_to_current(self, target_current, current_step):
        delay0 = .005

        startI = self.get_current()

        len = np.int(np.ceil(np.abs(target_current-startI)/current_step)+1)
        iList = np.linspace(startI, target_current, len)

        for _ in iList:
            self.set_current(target_current)
            qt.msleep(delay0)

    def ramp_to_voltage(self, stop, step, channel=None):
        """
        Ramps the source voltage from the current level to the desired
        level in linear steps.

        Parameters
        ----------
        stop : float
            The voltage to be reach by the end of the sweep in volts.

        step : float
            The ramp step size in volts.

        channel : int
            Selects the channel to ramp. Included for compatibility
            with meters with channels, as the 2400 Series uses only
            one.
        """
        # for compatibility with meters with channels
        assert channel is None

        start = float(self._visainstrument.query(':SOUR:VOLT:LEV?'))

        # source settings
        self._visainstrument.write(':SOUR:FUNC VOLT')
        self._visainstrument.write(':SOUR:VOLT:RANG {}'.format(
            max(start, stop)))

        # output ON
        self._visainstrument.write(':OUTP ON')

        # step voltage from start to stop
        ramp = np.linspace(start, stop,
                           int(np.ceil(np.abs((stop - start) / step)) + 1))
        for i in ramp[1:]:
            self._visainstrument.write(':SOUR:VOLT:LEV {}'.format(i))
            qt.msleep(0.001)

        # output OFF
        self._visainstrument.write(':OUTP OFF')

    def get_resistance(self):
        self.measure_resistance()
        return self.read_val()

    def get_current(self):
        self.measure_current()
        return self.read_val()

    def get_voltage(self):
        self.measure_voltage()
        return self.read_val()

    def trigger(self):
        """ Executes a bus trigger, which can be used when 
        :meth:`~.trigger_on_bus` is configured. 
        """
        return self._visainstrument.write("*TRG")

    def trigger_immediately(self):
        """ Configures measurements to be taken with the internal
        trigger at the maximum sampling rate.
        """
        self._visainstrument.write(":ARM:SOUR IMM;:TRIG:SOUR IMM;")

    def trigger_on_bus(self):
        """ Configures the trigger to detect events based on the bus
        trigger, which can be activated by :code:`GET` or :code:`*TRG`.
        """
        self._visainstrument.write(":ARM:COUN 1;:ARM:SOUR BUS;:TRIG:SOUR BUS;")

    def set_trigger_counts(self, arm, trigger):
        """ Sets the number of counts for both the sweeps (arm) and the
        points in those sweeps (trigger), where the total number of
        points can not exceed 2500
        """
        if arm * trigger > 2500 or arm * trigger < 0:
            raise Exception(
                "Keithley 2400 has a combined maximum of 2500 counts")
        if arm < trigger:
            self._visainstrument.write(
                ":ARM:COUN %d;:TRIG:COUN %d" % (arm, trigger))
        else:
            self._visainstrument.write(
                ":TRIG:COUN %d;:ARM:COUN %d" % (trigger, arm))

    def disable_buffer(self):
        """ Disables the connection between measurements and the
        buffer, but does not abort the measurement process.
        """
        self._visainstrument.write(":TRAC:FEED:CONT NEV")

    def sample_continuously(self):
        """ Causes the instrument to continuously read samples
        and turns off any buffer or output triggering
        """
        self.disable_buffer()
        self.disable_output_trigger()
        self.trigger_immediately()

    def set_timed_arm(self, interval):
        """ Sets up the measurement to be taken with the internal
        trigger at a variable sampling rate defined by the interval
        in seconds between sampling points
        """
        if interval > 99999.99 or interval < 0.001:
            raise Exception(
                "Keithley 2400 can only be time triggered between 1 ms and 1 Ms")
        self._visainstrument.write(":ARM:SOUR TIM;:ARM:TIM %.3f" % interval)

    def trigger_on_external(self, line=1):
        """ Configures the measurement trigger to be taken from a 
        specific line of an external trigger

        :param line: A trigger line from 1 to 4
        """
        cmd = ":ARM:SOUR TLIN;:TRIG:SOUR TLIN;"
        cmd += ":ARM:ILIN %d;:TRIG:ILIN %d;" % (line, line)
        self._visainstrument.write(cmd)

    def output_trigger_on_external(self, line=1, after='DEL'):
        """ Configures the output trigger on the specified trigger link
        line number, with the option of supplying the part of the
        measurement after which the trigger should be generated
        (default to delay, which is right before the measurement)

        :param line: A trigger line from 1 to 4
        :param after: An event string that determines when to trigger
        """
        self._visainstrument.write(
            ":TRIG:OUTP %s;:TRIG:OLIN %d;" % (after, line))

    def disable_output_trigger(self):
        """ Disables the output trigger for the Trigger layer
        """
        self._visainstrument.write(":TRIG:OUTP NONE")

    def status(self):
        return self._visainstrument.query("status:queue?;")

    '''
    def RvsI(self, startI, stopI, stepI, compliance, delay=10.0e-3, backward=False):
        num = int(float(stopI-startI)/float(stepI)) + 1
        currRange = 1.2*max(abs(stopI),abs(startI))
        # self.write(":SOUR:CURR 0.0")
        self.write(":SENS:VOLT:PROT %g" % compliance)
        self.write(":SOUR:DEL %g" % delay)
        self.write(":SOUR:CURR:RANG %g" % currRange )
        self.write(":SOUR:SWE:RANG FIX")
        self.write(":SOUR:CURR:MODE SWE")
        self.write(":SOUR:SWE:SPAC LIN")
        self.write(":SOUR:CURR:STAR %g" % startI)
        self.write(":SOUR:CURR:STOP %g" % stopI)
        self.write(":SOUR:CURR:STEP %g" % stepI)
        self.write(":TRIG:COUN %d" % num)
        if backward:
            currents = np.linspace(stopI, startI, num)
            self.write(":SOUR:SWE:DIR DOWN")
        else:
            currents = np.linspace(startI, stopI, num)
            self.write(":SOUR:SWE:DIR UP")
        self.connection.timeout = 30.0
        self.enable_source()
        data = self.values(":READ?") 

        self.check_errors()
        return zip(currents,data)

    def RvsIaboutZero(self, minI, maxI, stepI, compliance, delay=10.0e-3):
        data = []
        data.extend(self.RvsI(minI, maxI, stepI, compliance=compliance, delay=delay))
        data.extend(self.RvsI(minI, maxI, stepI, compliance=compliance, delay=delay, backward=True))
        self.disable_source()    
        data.extend(self.RvsI(-minI, -maxI, -stepI, compliance=compliance, delay=delay))
        data.extend(self.RvsI(-minI, -maxI, -stepI, compliance=compliance, delay=delay, backward=True))
        self.disable_source()
        return data 
    '''

    def use_rear_terminals(self):
        """ Enables the rear terminals for measurement, and 
        disables the front terminals. """
        self._visainstrument.write(":ROUT:TERM REAR")

    def use_front_terminals(self):
        """ Enables the front terminals for measurement, and 
        disables the rear terminals. """
        self._visainstrument.write(":ROUT:TERM FRON")

    '''
    def shutdown(self):
        """ Ensures that the current or voltage is turned to zero
        and disables the output. """
        log.info("Shutting down %s." % self.name)
        if self.source_mode == 'current':
            self.ramp_to_current(0.0)
        else:
            self.ramp_to_voltage(0.0)
        self.stop_buffer()
        self.disable_source()
    '''

    def set_mode(self, mode):
        '''
        #Set the mode to the specified value

        Input:
            mode (string) : mode to be set. Choose from self._modes

        Output:
            None
        '''

        logging.debug('Set mode to %s', mode)
        if mode in self.modes:
            string = 'SENS:FUNC "%s"' % mode
            self._visainstrument.write(string)

            '''
            if mode.startswith('VOLT'):
                self._change_units('V')
            elif mode.startswith('CURR'):
                self._change_units('A')
            elif mode.startswith('RES'):
                self._change_units('Ohm')
            elif mode.startswith('FREQ'):
                self._change_units('Hz')
            '''

        else:
            logging.error('invalid mode %s' % mode)

        # self.get_all()
            # Get all values again because some paramaters depend on mode

    def read_val(self, ignore_error=False):
        '''
        Aborts current trigger and sends a new trigger
        to the device and reads float value.
        Do not use when trigger mode is 'CONT'
        Instead use readlastval

        Input:
            ignore_error (boolean): Ignore trigger errors, default is 'False'

        Output:
            value(float) : currrent value on input
        '''

        '''
        trigger_status = self.get_trigger_continuous(query=False)
        if trigger_status:
            if ignore_error:
                logging.debug('Trigger=continuous, can\'t trigger, return 0')
            else:
                logging.error('Trigger=continuous, can\'t trigger, return 0')
            text = '0'
            return float(text[0:15])
        elif not trigger_status:
            logging.debug('Read current value')
            #text = self._visainstrument.ask('READ?')
            text = self._visainstrument.query('READ?')
            self._trigger_sent = False
            return float(text[0:15])
        else:
            logging.error('Error in retrieving triggering status, no trigger sent.')
            
        '''

        logging.debug('Read current value')
        #text = self._visainstrument.ask('READ?')
        self._visainstrument.write(":OUTP ON")
        text = self._visainstrument.query('READ?')
        self._trigger_sent = False

        self.check_errors()

        return float(text[0:15])
        # else:
        #    logging.error('Error in retrieving triggering status, no trigger sent.')
