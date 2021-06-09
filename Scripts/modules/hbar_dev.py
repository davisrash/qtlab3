"""
docstring
"""

import sys
from shutil import copyfile
from time import time

import numpy as np
import source.qt as qt
from source.data import Data, IncrementalGenerator


current_time = time()

class HallBar():
    """
    add docstring
    """


def create_data(filename, instruments, circuit, sweeps):
    """
    add docstring
    """

    # incrementally number file names in the given data directory
    generator = IncrementalGenerator(qt.config['datadir'] + '\\' + filename)
    Data.set_filename_generator(generator)

    # create data object
    data = Data(name=filename)

    if isinstance(sweeps, dict):
        sweeps = [sweeps, {'name': 'empty', 'vector': [0]}]

    # create coordinates
    for i, dim in enumerate(['x', 'y']):
        data.add_coordinate(dim + ' (' + sweeps[i]['name'] + ')',
                            size=len(sweeps[i]['vector']),
                            start=sweeps[i]['vector'][0],
                            end=sweeps[i]['vector'][-1])

    # put instruments into lists if necessary for looping
    for instrument_type in instruments:
        if not isinstance(instruments[instrument_type], (list, tuple)):
            instruments[instrument_type] = [instruments[instrument_type]]

    # create lockin data
    for lockin in instruments['lockins']:
        for dim in ['x', 'y']:
            data.add_value(dim + ' raw', instrument=lockin.get_name(),
                           units='V')
            data.add_value(dim + ' pros', instrument=lockin.get_name(),
                           units='V')

    # add data for each gate
    for i in range(circuit['num_gates']):
        data.add_value('gate {} V meas'.format(i + 1),
                       #instrument=meter,
                       units='A')
        data.add_value('gate {} leak'.format(i + 1),
                       #instrument=meter,
                       units='A')

    # add magnet data
    if 'magnets' in instruments \
            and instruments['magnets'] not in [None, [None]]:
        for magnet in instruments['magnets']:
            data.add_value('magnet z',
                           instrument=magnet.get_name(),
                           #units='T',
                           )

    # add time data
    data.add_value('time', units='s')

    # create data file
    data.create_file()
    copyfile(sys._getframe().f_code.co_filename,
             data.get_dir() + '\\' + filename + '_'
                 + str(generator.counter - 1) + '.py')

    return data

def take_data(instruments, circuit, channels=None):
    """
    add docstring
    """
    # TODO standardize parameter measuring, i.e. get_X()
    # and get_data_param0()

    # define lists for data
    x, y, z = [], [], []
    gates, leaks = [], []

    # put instruments into lists if necessary for looping
    for instrument_type in instruments:
        if not isinstance(instruments[instrument_type], (list, tuple)):
            instruments[instrument_type] = [instruments[instrument_type]]

    # measure X and Y channels on lockins
    for lockin in instruments['lockins']:
        if lockin.get_type() == 'SR830':
            x.append(lockin.get_X())
            y.append(lockin.get_Y())

        elif lockin.get_type() == 'SR860':
            x.append(lockin.get_data_param0())
            y.append(lockin.get_data_param1())

    # calculate x_pros and y_pros
    x_pros = [(circuit['input_voltage'] - x[i]) * circuit['sense_resistance'] /
              (1e-9 if x[i] == 0.0 else x[i]) for i in range(len(x))]
    y_pros = [(circuit['input_voltage'] - y[i]) * circuit['sense_resistance'] /
              (1e-9 if y[i] == 0.0 else y[i]) for i in range(len(y))]

    # measure gate voltage and leakage current for meters
    for meter in instruments['meters']:
        if meter.get_type() == 'Keithley_2400':
            gates.append(meter.get_voltage())
            leaks.append(meter.get_current())

        elif meter.get_type() == 'GS610':
            meter.set_sense_function('voltage')
            gates.append(meter.read())

            meter.set_sense_function('current')
            leaks.append(meter.read())

        elif meter.get_type() == 'QDevilQdac':
            for channel in channels:
                gates.append(meter.getDCVoltage(channel))
                leaks.append(meter.getCurrentReading(channel))

    # set all other gate voltages and leakage currents to 999
    for _ in range(circuit['num_gates'] - len(gates)):
        gates.append(999)
        leaks.append(999)

    # get magnetic field
    if 'magnets' in instruments \
            and instruments['magnets'] not in [None, [None]]:
        for magnet in instruments['magnets']:
            z.append(magnet.get_fieldZ())

    # get time
    t = time() - current_time

    return [i for j in zip(x, x_pros, y, y_pros) for i in j] \
            + [i for j in zip(gates, leaks) for i in j] + z + [t]

'''
def gate_sweep(filename, instruments, circuit, sweeps, channels):
    """
    add docstring
    """

    qt.mstart()

    # put instruments into lists if necessary for looping
    for instrument_type in instruments:
        if not isinstance(instruments[instrument_type], (list, tuple)):
            instruments[instrument_type] = [instruments[instrument_type]]

    if len(sweeps) == 1:
        sweeps.append({'name': 'None', 'start': 0.0, 'stop': 0.0, 'step': 0.1})
        dims = 1
    else:
        dims = 2

    for sweep in sweeps:
        sweep['vector'].append(np.linspace(
            sweep['start'], sweep['stop'],
            int(np.ceil(np.abs(
                (sweep['stop'] - sweep['start']) / sweep['step']
            )) + 1)
        ))

    if dims == 1:
        data = create_data(filename, instruments, circuit, sweeps)

        qt.msleep(sweeps[0]['intersweep_delay'])

        for x in sweeps[0]['vector'][0][0:]:
            instruments['meters'][0].ramp_to_voltage(x, sweeps[0]['ramp_rate'],
                                                     channel=channels[0])

            qt.msleep(sweeps[0]['intrasweep_delay'])
            data_vals = take_data(instruments, circuit, channels)

            data.add_data_point([x, 0] + data_vals)

    elif dims == 2:
        data = create_data(filename, instruments, circuit, sweeps)

        qt.msleep(sweeps[0]['intersweep_delay'])

        for x in sweeps[1]['vector'][0][0:]:
            instruments['meters'][0].ramp_to_voltage(x, sweeps[1]['ramp_rate'],
                                                     channel=channels[0])

            qt.msleep(sweeps[1]['intrasweep_delay'])
            for y in sweeps[1]['vector'][1][0:]:
                instruments['meters'][1].ramp_to_voltage(y, ramp_rate,
                                                         channel=channels[1])

                qt.msleep(intrasweep_delay)
                data_vals = take_data(instruments, circuit, channels)

                data.add_data_point([x, y] + data_vals)

    data._write_settings_file()
    data.close_file()

    qt.mend()
'''

def magnet_sweep(filename, instruments, circuit, sweeps, channels=None):
    """
    add docstring
    """
    # TODO says `sweeps` but assumes only one, potentially OK but then need to
    # force one sweep and one magnet and then work around mandatory 2D data in
    # create/take_data

    qt.mstart()

    # put instruments into lists if necessary for looping
    for instrument_type in instruments:
        if not isinstance(instruments[instrument_type], (list, tuple)):
            instruments[instrument_type] = [instruments[instrument_type]]

    # TODO what meter to use? fix channels
    instruments['meters'][0].ramp_to_voltage(
        sweeps['v_gate'], sweeps['ramp_rate'], channel=channels
    )

    # TODO conform to standard instrument looping, fix start and step
    for magnet in instruments['magnets']:
        sweeps['start'] = magnet.get_fieldZ()
        sweeps['step'] = int(np.abs((sweeps['stop'] - sweeps['start'])) \
            / sweeps['ramp_rate'] * 60 / sweeps['intrasweep_delay']) + 5

        sweeps['vector'] = np.linspace(sweeps['start'], sweeps['stop'],
                                       sweeps['step'])

    data = create_data(filename, instruments, circuit, sweeps)

    # TODO conform to standard instrument looping
    for magnet in instruments['magnets']:
        data_values = take_data(instruments, circuit)
        data.add_data_point([sweeps['vector'][0], 0] + data_values)

        magnet.rampToZ(sweeps['stop'])

        is_ramping = True
        counter = 1

        print('Start Bnow is {} and Bend is {}'.format(
            sweeps['start'], sweeps['stop']
        ))

        while is_ramping:
            # TODO take data quickly (?)
            data_values = take_data(instruments, circuit)
            data.add_data_point([sweeps['vector'][counter], 0] + data_values)

            counter = counter + 1

            qt.msleep(sweeps['intersweep_delay'])

            if magnet.get_rampStateZ() == 2 or magnet.get_rampStateZ() == 3:
                is_ramping = False

        data_values = take_data(instruments, circuit)
        data.add_data_point([sweeps['stop'], 0] + data_values)

        print('ramp ended')
        data._write_settings_file()
        data.close_file()

        qt.mend()

def record(filename, instruments, circuit, sweeps, time0, timestep):
    """
    add docstring
    """

    qt.mstart()

    sweeps['vector'] = np.arange(0, time0, timestep)

    data = create_data(filename, instruments, circuit, sweeps)

    data_vals = take_data(instruments, circuit)

    # what meter to use?
    instruments['meters'][0].ramp_to_voltage(
        sweeps['v_gate'], sweeps['ramp_rate'], channel=None
    )

    qt.msleep(sweeps['intersweep_delay'])

    t = 0
    while t < time0:
        # TODO take data quickly (?)
        data_vals = take_data(instruments, circuit)
        data.add_data_point([t, 0] + data_vals)

        qt.msleep(timestep)
        t = t + timestep

    data._write_settings_file()
    data.close_file()

    qt.mend()
