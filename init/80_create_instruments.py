import source.qt as qt

#example1 = qt.instruments.create('example1', 'example', address='GPIB::1', reset=True)
#dsgen = qt.instruments.create('dsgen', 'dummy_signal_generator')
#pos = qt.instruments.create('pos', 'dummy_positioner')
#combined = qt.instruments.create('combined', 'virtual_composite')
#combined.add_variable_scaled('magnet', example1, 'chA_output', 0.02, -0.13, units='mT')
#combined.add_variable_combined('waveoffset', [{
#    'instrument': dmm1,
#    'parameter': 'ch2_output',
#    'scale': 1,
#    'offset': 0}, {
#    'instrument': dsgen,
#    'parameter': 'wave',
#    'scale': 0.5,
#    'offset': 0
#    }], format='%.04f')

## Keithleys
#print('Setting up Keithley 1...')
#keithley1 = qt.instruments.create('keithley1', 'Keithley_2000', address='GPIB::1', change_display=False)
#keithley1 = qt.instruments.get('keithley1')

#print('Setting up Keithley 2...')
#keithley2 = qt.instruments.create('keithley2', 'Keithley_2000', address='GPIB::2', change_display=False)
#keithley2 = qt.instruments.get('keithley2')

## Lock-in amplifiers
print('Setting up lockin1...')
lockin1 = qt.instruments.create('lockin1', 'SR830', address='GPIB::9')

##QDevil Qdac
#print('Setting up QDevil Qdac...')
#qdac1 = qt.instruments.create('qdac1', 'QDevilQdac', port='COM3', verbose=False)

##K2400
print('Setting up K2400...')
keithley1 = qt.instruments.create('keithley1', 'Keithley_2400', address='GPIB::24', change_display=False)

## Yokogawa
print("Setting up Yokogawa GS610...")
yoko = qt.instruments.create('yoko', 'Yokogawa_GS610', address='GPIB::1')

# SR860
print("Setting up SR860...")
sr860 = qt.instruments.create('sr860', 'SR860', address='GPIB::4')

print('All instruments set up and good to go!')

#b = qdac1.getSerialNumber()
#a = keithley1.readlast()
#print(a)
#print(b)