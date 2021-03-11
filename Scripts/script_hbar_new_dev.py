"""
add docstring
"""
import sys

import numpy as np
import source.data as D
import source.qt as qt

import modules.traces as traces

NUM_GATES = 6

QDAC_ENABLED = False

FILENAME = 'VA_485_Ebase_G'
INTRASWEEP_DELAY = 0.1
INTERSWEEP_DELAY = 1
THRESHOLD = 200000
COMPLIANCE = 5e-3
RAMP_RATE = 1e-2

R_SENSE = 992

START1 = -2
END1 = 2
XSTEP1 = 0.04
REV = False

lockins = []
meters = []
for name in qt.instruments.get_instrument_names():
    instrument = qt.instruments.get(name)
    if instrument.get_type() in ['SR830', 'SR860']:
        lockins.append(instrument)
    elif instrument.get_type() in ['Keithley_2400', 'Yokogawa_GS610']:
        meters.append(instrument)

if QDAC_ENABLED:
    qdac1 = qt.instruments.get('qdac1')

class Script():
    """
    add docstring
    """

    def __init__(self):
        self._generator = D.IncrementalGenerator(qt.config['datadir'] + '\\'
                                                 + FILENAME)

    def create_data(self, x_vector, x_coordinate, x_parameter, y_vector,
                    y_coordinate, y_parameter, z_vector, z_coordinate,
                    z_parameter):
        """
        Generates the data file, spyview file, and copies the python script.

        Input:

        Output:

        """
        qt.Data.set_filename_generator(self._generator)
        data = qt.Data(name=FILENAME)
        data.add_coordinate(x_parameter + ' (' + x_coordinate + ')',
                            size=len(x_vector), start=x_vector[0],
                            end=x_vector[-1])
        data.add_coordinate(y_parameter + ' (' + y_coordinate + ')',
                            size=len(y_vector), start=y_vector[0],
                            end=y_vector[-1])
        data.add_coordinate(z_parameter + ' (' + z_coordinate + ')',
                            size=len(z_vector), start=z_vector[0],
                            end=z_vector[-1])

        for i in range(NUM_GATES):
            data.add_value('Gate {} V meas'.format(i))
            data.add_value('Gate {} leak'.format(i))

        for i, _ in enumerate(lockins):
            data.add_value('Lockin {} X raw'.format(i))
            data.add_value('Lockin {} X pros'.format(i))
            data.add_value('Lockin {} Y raw'.format(i))

        data.create_file()
        traces.copy_script(
            sys._getframe().f_code.co_filename, data.get_dir(),
            FILENAME + '_' + str(self._generator._counter - 1))

        return data

    def volt_sweep(self, lockin, xname, xstart, xend, xstep, rev, threshold):
        qt.mstart()

        # create sweep vectors
        x_vector = np.arange(xstart, xend, xstep)
        y_vector = [0]
        z_vector = [0]

        x1_vector = []

        data_fwd = self.create_data(x_vector, xname, 'Lockin Voltage',
                                    y_vector, 'none', 'y_parameter', z_vector,
                                    'none', 'z_parameter')

        for x in x_vector:
            if lockin.get_type() == 'SR830':
                lockin.set_amplitude(x)
            elif lockin.get_type() == 'SR860':
                lockin.set_sine_out_amplitude(x)

            qt.msleep(0.2)
            data_values = take_data(x)
            data_fwd.add_data_point(x, 0, 0, data_values[0], data_values[1])

            if data_values[0] > threshold:
                break

            x1_vector.append(x)

        data_fwd._write_settings_file()
        data_fwd.close_file()
        qt.msleep(INTERSWEEP_DELAY)

        if rev:
            x1_vector = np.flip(x1_vector)
            data_bck = self.create_data(x1_vector, xname, 'Lockin Voltage',
                                        y_vector, 'none', 'y_parameter',
                                        z_vector, 'none', 'z_parameter')

            for x1 in x1_vector:
                if lockin.get_type() == 'SR830':
                    lockin.set_amplitude(x1)
                elif lockin.get_type() == 'SR860':
                    lockin.set_sine_out_amplitude(x1)

                qt.msleep(0.2)
                data_values = take_data(x1)
                data_bck.add_data_point(x1, 0, 0, data_values[0],
                                        data_values[1])

            data_bck._write_settings_file()
            data_bck.close_file()

        qt.mend()
        return 1

    def qdac_1gate(self, channel, xname, xstart, xend, xstep, rev, threshold, compliance):
        qt.mstart()

        if ((xstart - xend) / xstep) % 2 == 0:
            xnum = np.int(np.ceil(np.abs(xstart - xend) / xstep) + 1)
        else:
            xnum = np.int(np.ceil(np.abs((xstart - xend) / xstep)))

        x_vector = np.linspace(xstart, xend, xnum)
        y_vector = [0]
        z_vector = [0]

        x1_vector = []
        data_fwd = self.create_data(x_vector, xname, 'x_parameter', y_vector,
                                    'none', 'y_parameter', z_vector, 'none', 'z_parameter')

        for x in x_vector:
            if x == x_vector[1]:
                print("Scan has started.")

            # Do we have multiple multimeters ever? And do we use the QDAC and other multimeter at the same time? Currently assuming 1 meter.
            # for _, meter in enumerate(meters):
                if meters[0].get_type() == 'Keithley_2400':
                    xcurrent = meters[0].get_voltage()
                elif meters[0].get_type() == 'Yokogawa_GS610':
                    meters[0].set_sense_function(0)
                    xcurrent = meters[0].read()
                elif QDAC_ENABLED:
                    xcurrent = qdac1.getDCVoltage(channel)

            ramp_steps = np.int(
                np.ceil(np.abs((xcurrent - x) / RAMP_RATE) + 1))
            temp_ramp = np.linspace(xcurrent, x, ramp_steps)

            for i in temp_ramp[1:]:
                mask = (i > x) ^ (xcurrent > x)
                if meters[0].get_type() == 'Keithley_2400':
                    a.keithley_gateset(1, x if mask else i)
                elif meters[0].get_type() == 'Yokogawa_GS610':
                    a.yoko_gateset(x if mask else i)
                elif QDAC_ENABLED:
                    qdac1.rampDCVoltage(channel, x if mask else i)

            if meters[0].get_type() == 'Keithley_2400':
                a.keithley_gateset(1, x)
            elif meters[0].get_type() == 'Yokogawa_GS610':
                a.yoko_gateset(x)
            elif QDAC_ENABLED:
                qdac1.rampDCVoltage(channel, x)

            qt.msleep(INTRASWEEP_DELAY)
            data_values = take_data(x) # x does not affect take_data?

            data_fwd.add_data_point(x, 0, 0, data_values[0:14])

            if threshold is not None:
                if data_values[13] > threshold:
                    break
            if data_values[2 * channel - 1] > compliance:
                break
            x1_vector.append(x)

        data_fwd._write_settings_file()
        data_fwd.close_file()
        qt.mend()
        qt.msleep(INTERSWEEP_DELAY)

        if rev:
            x1_vector = np.flip(x1_vector)
            data_bck = self.create_data(x1_vector, xname, 'Lockin Voltage',
                                        y_vector, 'none', 'y_parameter', z_vector, 'none', 'z_parameter')
            print("Reverse scan started.")
            for x1 in x1_vector:
                x1current = qdac1.getDCVoltage(channel)
                ramp_steps1 = np.int(
                    np.ceil(np.abs((x1current - x1) / RAMP_RATE) + 1))
                temp_ramp1 = np.linspace(x1current, x1, ramp_steps1)

                for i in temp_ramp1[1:]:
                    if (i > x1) ^ (x1current > x1):
                        qdac1.setDCVoltage(channel, x1)
                    else:
                        qdac1.setDCVoltage(channel, i)
                qt.msleep(0.05)
                qdac1.setDCVoltage(channel, x1)
                qt.msleep(INTRASWEEP_DELAY)
                data_values = take_data(x1)

                data_bck.add_data_point(x, 0, 0, data_values[0:14])

            data_bck._write_settings_file()
            data_bck.close_file()

        qt.mend()
        return 1

    def qdac_2gate(self, channel, channel2, xname1, xstart1, xend1, xstep1, xname2, xstart2, xend2, xstep2, threshold, compliance):
        qt.mstart()

        if ((xstart1 - xend1) / xstep1) % 2 == 0:
            xnum1 = np.int(np.ceil(np.abs((xstart1 - xend1) / xstep1) + 1))
        else:
            xnum1 = np.int(np.ceil(np.abs((xstart1 - xend1) / xstep1)))

        x_vector1 = np.linspace(xstart1, xend1, xnum1)

        #y_vector1 = [0]
        z_vector = [0]

        if ((xstart2 - xend2) / xstep2) % 2 == 0:
            xnum2 = np.int(np.ceil(np.abs((xstart2 - xend2) / xstep2) + 1))
        else:
            xnum2 = np.int(np.ceil(np.abs((xstart2 - xend2) / xstep2)))

        x_vector2 = np.linspace(xstart2, xend2, xnum2)

        #yvector2 = [0]

        xq1_vector = []
        xq2_vector = []
        data_fwd = self.create_data(x_vector1, 'gate_1', 'x_parameter',
                                    x_vector2, 'gate_2', 'y_parameter',
                                    z_vector, 'none', 'z_parameter')

        for x1 in x_vector1:
            xcurrent1 = qdac1.getDCVoltage(channel)

            ramp_steps1 = np.int(
                np.ceil(np.abs((xcurrent1 - x1) / RAMP_RATE) + 1))
            temp_ramp1 = np.linspace(xcurrent1, x1, ramp_steps1)

            for i in temp_ramp1[1:]:
                if (i > x1) ^ (xcurrent1 > x1):
                    qdac1.setDCVoltage(channel, x1)
                else:
                    qdac1.setDCVoltage(channel, i)
                qt.msleep(0.05)

            for x2 in x_vector2:
                xcurrent2 = qdac1.getDCVoltage(channel2)

                ramp_steps2 = np.int(
                    np.ceil(np.abs((xcurrent2 - x2) / RAMP_RATE) + 1))
                temp_ramp2 = np.linspace(xcurrent2, x2, ramp_steps2)

                for i in temp_ramp2[1:]:
                    if (i > x2) ^ (xcurrent2 > x2):
                        qdac1.setDCVoltage(channel2, x2)
                    else:
                        qdac1.setDCVoltage(channel2, i)
                    qt.msleep(0.05)

                qdac1.setDCVoltage(channel2, x2)
                qt.msleep(INTERSWEEP_DELAY)
                data_values = take_data(x1)

                if data_values[1] > compliance or data_values[3] > compliance:
                    print("I am broken.")
                    break

                if data_values[5] > threshold:
                    data_fwd.add_data_point(x1, x2, 0, data_values[0:11],
                                            np.nan, data_values[13:14])

                    print("I shall continue.")
                    continue
                else:
                    data_fwd.add_data_point(x1, x2, 0, data_values[0],
                                            data_values[1], data_values[2],
                                            data_values[3], data_values[4],
                                            data_values[5], data_values[6],
                                            data_values[7], data_values[8],
                                            data_values[9], data_values[10],
                                            data_values[11], data_values[12],
                                            data_values[13], data_values[14])
                    print("I am awesome.")

                xq2_vector.append(x2)

            print("end X2")
            qdac1.setDCVoltage(channel, x1)
            qt.msleep(INTERSWEEP_DELAY)

            xq1_vector.append(x1)

        print("end X1")
        data_fwd._write_settings_file()
        data_fwd.close_file()
        qt.msleep(INTRASWEEP_DELAY)

    def qdac_gateset(self, channel, xend):
        xcurrent = qdac1.getDCVoltage(channel)

        ramp_steps = np.int(np.ceil(np.abs((xcurrent - xend) / RAMP_RATE) + 1))
        temp_ramp = np.linspace(xcurrent, xend, ramp_steps)

        for i in temp_ramp[1:]:
            if (i > xend) ^ (xcurrent > xend):
                qdac1.setDCVoltage(channel, xend)
            else:
                qdac1.setDCVoltage(channel, i)
            qt.msleep(0.05)

        qdac1.setDCVoltage(channel, xend)
        qt.msleep(INTERSWEEP_DELAY)

    # assumes only one keithley!
    def keithley_gateset(self, num, xend):
        keithley = qt.instruments.get_instruments_by_type('Keithley_2400')
        xcurrent = keithley.get_voltage()

        ramp_steps = np.int(
            np.ceil(np.abs((xcurrent - xend) / RAMP_RATE) + 1))
        temp_ramp = np.linspace(xcurrent, xend, ramp_steps)

        for i in temp_ramp[1:]:
            keithley.set_voltage(xend if (i > xend) ^ (xcurrent > xend) else i)
            qt.msleep(0.01)

        keithley.set_voltage(xend)
        qt.msleep(INTRASWEEP_DELAY)

    # assumes only one yoko!
    def yoko_gateset(self, xend):
        yoko = qt.instruments.get_instruments_by_type('Yokogawa_GS610')
        yoko.set_source_function(0)
        yoko.set_source_voltage_range(xend)
        yoko.set_source_protection_linkage(1)
        yoko.set_source_current_protection_upper_limit(COMPLIANCE)

        yoko.set_source_protection(1)

        yoko.set_sense(1)
        yoko.set_sense_function(1)

        yoko.set_trigger_source(0)
        yoko.set_trigger_timer(INTRASWEEP_DELAY)
        yoko.set_source_delay(yoko.get_source_delay_minimum())
        yoko.set_sense_delay(yoko.get_sense_delay_minimum())

        yoko.set_output(1)

        xcurrent = yoko.get_source_voltage_level()

        ramp_steps = np.int(np.ceil(np.abs((xcurrent - xend) / RAMP_RATE) + 1))
        temp_ramp = np.linspace(xcurrent, xend, ramp_steps)

        for i in temp_ramp[1:]:
            yoko.set_source_voltage_level(
                xend if (i > xend) ^ (xcurrent > xend) else i)
            qt.msleep(0.01)
            print(str(yoko.get_source_voltage_level()) + ' V, '
                  + str(yoko.read()) + ' A')

        yoko.set_source_voltage_level(xend)
        qt.msleep(INTRASWEEP_DELAY)


def take_data(x):
    """
    add docstring
    """
    qt.msleep(INTRASWEEP_DELAY)

    X = []
    X_pros = []
    Y = []
    for i, lockin in enumerate(lockins):
        if lockin.get_type() == 'SR830':
            X.append(lockin.get_X())
            X_pros.append((V_in - X[i]) / (1e-9 if X[i] == 0.0 else X[i])
                          * R_SENSE)
            Y.append(lockin.get_Y())
        elif lockin.get_type() == 'SR860':
            X.append(lockin.get_data_param(0))
            X_pros.append((V_in - X[i]) / (1e-9 if X[i] == 0.0 else X[i])
                          * R_SENSE)
            Y.append(lockin.get_data_param(1))

    gates = [999] * NUM_GATES
    leaks = [999] * NUM_GATES
    for i, meter in enumerate(meters):
        if meter.get_type() == 'Keithley_2400':
            gates[i] = meter.get_voltage()
            leaks[i] = meter.get_current()
        elif meter.get_type() == 'Yokogawa_GS610':
            meter.set_sense_function(0)
            gates[i] = meter.read()

            meter.set_sense_function(1)
            leaks[i] = meter.read()

    if QDAC_ENABLED:
        for i in range(len(meters), NUM_GATES):
            gates[i] = qdac1.getDCVoltage(i)
            leaks[i] = qdac1.getCurrentReading(i)

    return [i for j in zip(gates, leaks) for i in j] \
        + [i for j in zip(X, X_pros, Y) for i in j]


a = Script()
V_in = 100e-6
# lockin1.set_amplitude(0.1)
# a.yoko_gateset(1)
# a.yoko_gateset(1)

#a.qdac_1gate(1, 'Gate', start1, end1, xstep1, rev, threshold, compliance)
