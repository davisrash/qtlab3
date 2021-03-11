import source.qt as qt

## Lock-in amplifiers
qt.instruments.create('sr830_1', 'SR830', address='GPIB::9')
print("Created new SR830 instrument on GPIB::9.")
qt.instruments.create('sr860_1', 'SR860', address='GPIB::4')
print("Created new SR860 instrument on GPIB::4.")

##QDevil Qdac
#print('Setting up QDevil Qdac...')
#qdac1 = qt.instruments.create('qdac1', 'QDevilQdac', port='COM3', verbose=False)

##K2400
print('Setting up K2400...')
qt.instruments.create('keithley1', 'Keithley_2400', address='GPIB::24',
                      change_display=False)

## Yokogawa
print("Setting up Yokogawa GS610...")
yoko = qt.instruments.create('yoko', 'Yokogawa_GS610', address='GPIB::1')

print('All instruments set up and good to go!')

#b = qdac1.getSerialNumber()
#a = keithley1.readlast()
#print(a)
#print(b)