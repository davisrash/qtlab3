import qt


awg = qt.instruments.get('awg')

AWG_clock = 1e9

number_waveform = 2
waveform_prefix = 'test_'
burst_short = 1e-6	#shortest burst
burst_long = 2e-6		#longest burst
burst_amplitude = 1

pulse_length = 2e-3

if pulse_length < burst_long:
    print "The burst is longer than the pulse"


pulse_length_pts = round(pulse_length*AWG_clock)
burst_short_pts = round(burst_short*AWG_clock)
burst_long_pts = round(burst_long*AWG_clock)
burst_increment_pts = round(AWG_clock*(burst_long - burst_short)/(number_waveform-1))

marker = zeros(pulse_length_pts)

for k in arange(0,number_waveform,1):
    print 'Creating waveform number %i' %k
    waveform = zeros(pulse_length_pts)
    indexstart = round(pulse_length_pts/2 - (burst_short_pts+(k)*burst_increment_pts)/2)
    indexstop = round(pulse_length_pts/2 + (burst_short_pts+k*burst_increment_pts)/2)
    waveform[indexstart:indexstop] = burst_amplitude
    filename = '%s%i.wfm' %(waveform_prefix,k)
    awg.send_waveform(waveform,marker,marker,filename,AWG_clock)

sequence_opts = zeros((number_waveform,4))
sequence_opts[:,3] = -1
awg.create_sequence_file('burst_',arange(0,number_waveform,1),'',[],sequence_opts,'burst.seq')