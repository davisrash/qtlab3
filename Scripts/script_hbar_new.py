from numpy import arange, flip

import source.qt as qt
import sys

import numpy as np
import source.data as d
import modules.traces as traces

filename = 'test'
intrasweep_delay = 0.1
intersweep_delay = 1
threshhold = 200000
compliance = 5e-3
ramp_rate = 1e-2

keithley1 = qt.instruments.get('keithley1')
lockin1 = qt.instruments.get('lockin1')
qdac1 = qt.instruments.get('qdac1')
yoko = qt.instruments.get('yoko')

# device = 0 is keithley1
# device = 1 is qdac1
# device = 2 is yoko
device = 2

V_in = 100e-6
lockin1.set_amplitude(0.1)
R_sense = 992

start1 = -2
end1 = 2
xstep1 = 0.04
rev = False

class Script():
	def __init__(self):
		self.filename = filename
		self.generator = d.IncrementalGenerator(qt.config['datadir'] + '\\' + self.filename, 1)

	def create_data(self, x_vector, x_coordinate, x_parameter, y_vector, y_coordinate, y_parameter, z_vector, z_coordinate, z_parameter):
		"""
		Generates the data file, spyview file, and copies the python script.

		Input:

		Output:

		"""
		qt.Data.set_filename_generator(self.generator)
		data = qt.Data(name=self.filename)
		data.add_coordinate(x_parameter + ' (' + x_coordinate + ')', size=len(x_vector), start=x_vector[0], end=x_vector[-1])
		data.add_coordinate(y_parameter + ' (' + y_coordinate + ')', size=len(y_vector), start=y_vector[0], end=y_vector[-1])
		data.add_coordinate(z_parameter + ' (' + z_coordinate + ')', size=len(z_vector), start=z_vector[0], end=z_vector[-1])

		# Gate 1
		data.add_value('Gate 1 V meas')
		data.add_value('Gate 1 leak')

		# Gate 2
		data.add_value('Gate 2 V meas')
		data.add_value('Gate 2 leak')

		# Gate 3
		data.add_value('Gate 3 V meas')
		data.add_value('Gate 3 leak')

		# Gate 4
		data.add_value('Gate 4 V meas')
		data.add_value('Gate 4 leak')

		# Gate 5
		data.add_value('Gate 5 V meas')
		data.add_value('Gate 5 leak')

		# Gate 6
		data.add_value('Gate 6 V meas')
		data.add_value('Gate 6 leak')

		# Lockin 1
		data.add_value('Lockin 1 X raw')
		data.add_value('Lockin 1 X pros')
		data.add_value('Lockin 1 Y raw')

		data.create_file()
		traces.copy_script(sys._getframe().f_code.co_filename, data._dir, self.filename + '_' + str(self.generator._counter - 1))
		return data

	def take_data(self, x):
		"""
		"""
		qt.msleep(intrasweep_delay)
		L1_X = lockin1.get_X()
		L1_X_pro = (V_in - L1_X) / (1e-9 if L1_X == 0.0 else L1_X) * R_sense

		L1_Y = lockin1.get_Y()

		if device == 0:
			# keithley selected
			gate_1 = keithley1.get_voltage()
			gate_2 = 999
			gate_3 = 999
			gate_4 = 999
			gate_5 = 999
			gate_6 = 999

			leak_1 = keithley1.get_current()
			leak_2 = 999
			leak_3 = 999
			leak_4 = 999
			leak_5 = 999
			leak_6 = 999
		elif device == 1:
			# qdac selected
			gate_1 = qdac1.getDCVoltage(1)
			gate_2 = qdac1.getDCVoltage(2)
			gate_3 = qdac1.getDCVoltage(3)
			gate_4 = qdac1.getDCVoltage(4)
			gate_5 = qdac1.getDCVoltage(5)
			gate_6 = qdac1.getDCVoltage(6)

			leak_1 = qdac1.getCurrentReading(1)
			leak_2 = qdac1.getCurrentReading(2)
			leak_3 = qdac1.getCurrentReading(3)
			leak_4 = qdac1.getCurrentReading(4)
			leak_5 = qdac1.getCurrentReading(5)
			leak_6 = qdac1.getCurrentReading(6)
		elif device == 2:
			# yokogawa selected
			yoko.set_sense_function(0)
			gate_1 = yoko.read()
			gate_2 = 0
			gate_3 = 0
			gate_4 = 0
			gate_5 = 0
			gate_6 = 0

			yoko.set_sense_function(1)
			leak_1 = yoko.read()
			leak_2 = 0
			leak_3 = 0
			leak_4 = 0
			leak_5 = 0
			leak_6 = 0

		return [gate_1, leak_1, gate_2, leak_2, gate_3, leak_3, gate_4, leak_4, gate_5, leak_5, gate_6, leak_6, L1_X, L1_X_pro, L1_Y]

	def volt_sweep(self, xname, xstart, xend, xstep, rev, threshhold):
		qt.mstart()

		# create sweep vectors
		x_vector = arange(xstart, xend, xstep)
		y_vector = [0]
		z_vector = [0]

		x1_vector = []

		data_fwd = self.create_data(x_vector, xname, 'Lockin Voltage', y_vector, 'none', 'y_parameter', z_vector, 'none', 'z_parameter')

		for x in x_vector:
			lockin1.set_amplitude(x)
			qt.msleep(0.2)
			data_values = self.take_data(x)
			data_fwd.add_data_point(x, 0, 0, data_values[0], data_values[1])

			if data_values[0] > threshhold:
				break

			x1_vector.append(x)

		data_fwd._write_settings_file()
		data_fwd.close_file()
		qt.msleep(intersweep_delay)

		if rev:
			x1_vector = flip(x1_vector)
			data_bck = self.create_data(x1_vector, xname, 'Lockin Voltage', y_vector, 'none', 'y_parameter', z_vector, 'none', 'z_parameter')

			for x1 in x1_vector:
				lockin1.set_amplitude(x1)
				qt.msleep(0.2)
				data_values = self.take_data(x1)
				data_bck.add_data_point(x1, 0, 0, data_values[0], data_values[1])

			data_bck._write_settings_file()
			data_bck.close_file()

		qt.mend()
		return 1

	def qdac_1gate(self, channel, xname, xstart, xend, xstep, rev, threshhold, compliance):
		qt.mstart()

		if ((xstart - xend) / xstep) % 2 == 0:
			xnum = np.int(np.ceil(np.abs(xstart - xend) / xstep) + 1)
		else:
			xnum = np.int(np.ceil(np.abs((xstart - xend) / xstep)))

		x_vector = np.linspace(xstart, xend, xnum)
		y_vector = [0]
		z_vector = [0]

		x1_vector = []
		data_fwd = self.create_data(x_vector, xname, 'x_parameter', y_vector, 'none', 'y_parameter', z_vector, 'none', 'z_parameter')

		for x in x_vector:
			if x == x_vector[1]:
				print("Scan has started.")

			if device == 0:
				xcurrent = keithley1.get_voltage()
			elif device == 1:
				xcurrent = qdac1.getDCVoltage(channel)
			elif device == 2:
				yoko.set_sense_function(0)
				xcurrent = yoko.read()

			ramp_steps = np.int(np.ceil(np.abs((xcurrent - x) / ramp_rate) + 1))
			temp_ramp = np.linspace(xcurrent, x, ramp_steps)

			for i in temp_ramp[1:]:
				if (i > x) ^ (xcurrent > x):
					if device == 0:
						a.keithley_gateset(1, x)
					elif device == 1:
						qdac1.rampDCVoltage(channel, x)
					elif device == 2:
						a.yoko_gateset(x)
				else:
					if device == 0:
						a.keithley_gateset(1, i)
					elif device == 1:
						qdac1.rampDCVoltage(channel, i)
					elif device == 2:
						a.yoko_gateset(i)

			if device == 0:
				a.keithley_gateset(1, x)
			elif device == 1:
				qdac1.rampDCVoltage(channel, x)
			elif device == 2:
				a.yoko_gateset(x)

			qt.msleep(intrasweep_delay)
			data_values = self.take_data(x)

			data_fwd.add_data_point(x, 0, 0, data_values[0], data_values[1], data_values[2], data_values[3], data_values[4], data_values[5], data_values[6], data_values[7], data_values[8], data_values[9], data_values[10], data_values[11], data_values[12], data_values[13], data_values[14])

			if threshhold is not None:
				if data_values[13] > threshhold:
					break
			if data_values[2 * channel - 1] > compliance:
				break
			x1_vector.append(x)

		data_fwd._write_settings_file()
		data_fwd.close_file()
		qt.mend()
		qt.msleep(intersweep_delay)

		if rev:
			x1_vector = flip(x1_vector)
			data_bck = self.create_data(x1_vector, xname, 'Lockin Voltage', y_vector, 'none', 'y_parameter', z_vector, 'none', 'z_parameter')
			print("Reverse scan started.")
			for x1 in x1_vector:
				x1current = qdac1.getDCVoltage(channel)
				ramp_steps1 = np.int(np.ceil(np.abs((x1current - x1) / ramp_rate) + 1))
				temp_ramp1 = np.linspace(x1current, x1, ramp_steps1)

				for i in temp_ramp1[1:]:
					if (i > x1) ^ (x1current > x1):
						qdac1.setDCVoltage(channel, x1)
					else:
						qdac1.setDCVoltage(channel, i)
				qt.msleep(0.05)
				qdac1.setDCVoltage(channel, x1)
				qt.msleep(intrasweep_delay)
				data_values = self.take_data(x1)

				data_bck.add_data_point(x, 0, 0, data_values[0], data_values[1], data_values[2], data_values[3], data_values[4], data_values[5], data_values[6], data_values[7], data_values[8], data_values[9], data_values[9], data_values[10], data_values[11], data_values[12], data_values[13], data_values[14])

			data_bck._write_settings_file()
			data_bck.close_file()

		qt.mend()
		return 1

	def qdac_2gate(self, channel, channel2, xname1, xstart1, xend1, xstep1, xname2, xstart2, xend2, xstep2, threshhold, compliance):
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
		data_fwd = self.create_data(x_vector1, 'gate_1', 'x_parameter', x_vector2, 'gate_2', 'y_parameter', z_vector, 'none', 'z_parameter')

		for x1 in x_vector1:
			xcurrent1 = qdac1.getDCVoltage(channel)

			ramp_steps1 = np.int(np.ceil(np.abs((xcurrent1 - x1) / ramp_rate) + 1))
			temp_ramp1 = np.linspace(xcurrent1, x1, ramp_steps1)

			for i in temp_ramp1[1:]:
				if (i > x1) ^ (xcurrent1 > x1):
					qdac1.setDCVoltage(channel, x1)
				else:
					qdac1.setDCVoltage(channel, i)
				qt.msleep(0.05)

			for x2 in x_vector2:
				xcurrent2 = qdac1.getDCVoltage(channel2)

				ramp_steps2 = np.int(np.ceil(np.abs((xcurrent2 - x2) / ramp_rate) + 1))
				temp_ramp2 = np.linspace(xcurrent2, x2, ramp_steps2)

				for i in temp_ramp2[1:]:
					if (i > x2) ^ (xcurrent2 > x2):
						qdac1.setDCVoltage(channel2, x2)
					else:
						qdac1.setDCVoltage(channel2, i)
					qt.msleep(0.05)

				qdac1.setDCVoltage(channel2, x2)
				qt.msleep(intersweep_delay)
				data_values = self.take_data(x1)

				if data_values[1] > compliance or data_values[3] > compliance:
					print("I am broken.")
					break

				if data_values[5] > threshhold:
					data_fwd.add_data_point(x1, x2, 0, data_values[0], data_values[1], data_values[2], data_values[3], data_values[4], data_values[5], data_values[6], data_values[7], data_values[8], data_values[9], data_values[10], data_values[11], np.nan, data_values[13], data_values[14])

					print("I shall continue.")
					continue
				else:
					data_fwd.add_data_point(x1, x2, 0, data_values[0], data_values[1], data_values[2], data_values[3], data_values[4], data_values[5], data_values[6], data_values[7], data_values[8], data_values[9], data_values[10], data_values[11], data_values[12], data_values[13], data_values[14])

					print("I am awesome.")

				xq2_vector.append(x2)

			print("end X2")
			qdac1.setDCVoltage(channel, x1)
			qt.msleep(intersweep_delay)

			xq1_vector.append(x1)

		print("end X1")
		data_fwd._write_settings_file()
		data_fwd.close_file()
		qt.msleep(intrasweep_delay)

	def qdac_gateset(self, channel, xend):
		xcurrent = qdac1.getDCVoltage(channel)

		ramp_steps = np.int(np.ceil(np.abs((xcurrent - xend) / ramp_rate) + 1))
		temp_ramp = np.linspace(xcurrent, xend, ramp_steps)

		for i in temp_ramp[1:]:
			if (i > xend) ^ (xcurrent > xend):
				qdac1.setDCVoltage(channel, xend)
			else:
				qdac1.setDCVoltage(channel, i)
			qt.msleep(0.05)

		qdac1.setDCVoltage(channel, xend)
		qt.msleep(intersweep_delay)

	def keithley_gateset(self, num, xend):
		if num == 1:
			xcurrent = keithley1.get_voltage()

			ramp_steps = np.int(np.ceil(np.abs((xcurrent - xend) / ramp_rate) + 1))
			temp_ramp = np.linspace(xcurrent, xend, ramp_steps)

			for i in temp_ramp[1:]:
				if (i > xend) ^ (xcurrent > xend):
					keithley1.set_voltage(xend)
				else:
					keithley1.set_voltage(i)
				qt.msleep(0.01)

			keithley1.set_voltage(xend)
		qt.msleep(intrasweep_delay)

	def yoko_gateset(self, xend):
		yoko.set_source_function(0)
		yoko.set_source_voltage_range(xend)
		yoko.set_source_protection_linkage(1)
		yoko.set_source_current_protection_upper_limit(compliance)

		yoko.set_source_protection(1)

		yoko.set_sense(1)
		yoko.set_sense_function(1)

		yoko.set_trigger_source(0)
		yoko.set_trigger_timer(intrasweep_delay)
		yoko.set_source_delay(yoko.get_source_delay_minimum())
		yoko.set_sense_delay(yoko.get_sense_delay_minimum())

		yoko.set_output(1)

		xcurrent = yoko.get_source_voltage_level()

		ramp_steps = np.int(np.ceil(np.abs((xcurrent - xend) / ramp_rate) + 1))
		temp_ramp = np.linspace(xcurrent, xend, ramp_steps)

		for i in temp_ramp[1:]:
			if (i > xend) ^ (xcurrent > xend):
				yoko.set_source_voltage_level(xend)
			else:
				yoko.set_source_voltage_level(i)
			qt.msleep(0.01)
			print((str)(yoko.get_source_voltage_level()) + ' V, ' + (str)(yoko.read()) + ' A')

			yoko.set_source_voltage_level(xend)
		qt.msleep(intrasweep_delay)

a = Script()
a.yoko_gateset(0.5)
a.yoko_gateset(1)

a.qdac_1gate(1, 'Midgate', start1, end1, xstep1, rev, threshhold, compliance)
