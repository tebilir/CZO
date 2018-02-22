'''
PAL 5/21/2012 mod 9/18/2012
compile and calibrate field data
exclude non-field times for new sensors
#
Modified by H. Maness on 15 Oct 2012:
Changed calnew and calK paths
'''

import numpy as np
from matplotlib.pyplot import plot,scatter,savefig,figure,colorbar,suptitle,close,show,subplot,rgrids
from matplotlib.mlab import csv2rec
import matplotlib as mpl
import datetime
from matplotlib.dates import DateFormatter
from time import mktime
from scipy.interpolate import interp1d
import cPickle

# calibration relationships
calnew = csv2rec('./linregressions.csv')
calK = csv2rec('./calibrations_Kevinsensors.csv')

# datafiles
files = dict()
# 795 = 1-3
files['795'] = ['25 August 2010/station1-3.csv','ShuttleReadout12_10_10_10_02_57_AM_PST/2373795.csv',\
	'ShuttleReadout09_07_11_05_38_23_PM_PDT/2373795_0.csv','6 Feb 2012/2373795.csv','ShuttleReadout03_16_12_12_04_52_PM_GMT-07_00/2373795.csv',\
	'ShuttleReadout05_07_12_02_07_41_PM_GMT-07_00/2373795_0.csv','ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/2373795.csv']
# 796 = 2-4
files['796'] = ['25 August 2010/station2-4.csv','ShuttleReadout10_22_10_08_47_13_AM_PDT/2373796_0.csv',\
	'ShuttleReadout09_07_11_05_38_23_PM_PDT/2373796_1.csv','ShuttleReadout09_07_11_05_38_23_PM_PDT/2373796_2.csv',\
	'6 Feb 2012/2373796.csv','ShuttleReadout03_16_12_12_04_52_PM_GMT-07_00/2373796.csv','ShuttleReadout05_07_12_04_56_23_PM_GMT-07_00/2373796.csv',\
	'ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/2373796.csv','ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/2373796_0.csv']
# 797 = 2-1
files['797'] = ['25 August 2010/station2-1.csv','ShuttleReadout10_22_10_08_47_13_AM_PDT/2373797_0.csv',\
	'ShuttleReadout09_07_11_05_38_23_PM_PDT/2373797_1.csv','6 Feb 2012/2373797.csv',\
	'ShuttleReadout05_07_12_02_07_41_PM_GMT-07_00/2373797.csv','ShuttleReadout05_07_12_04_56_23_PM_GMT-07_00/2373797.csv',\
	'ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/2373797.csv']
# 798 = 1-1
files['798'] = ['25 August 2010/station1-1.csv','ShuttleReadout12_10_10_10_02_57_AM_PST/2373798.csv',\
	'ShuttleReadout09_07_11_05_38_23_PM_PDT/2373798_0.csv','6 Feb 2012/2373798.csv',\
	'ShuttleReadout03_16_12_12_04_52_PM_GMT-07_00/2373798.csv','ShuttleReadout05_07_12_02_07_41_PM_GMT-07_00/2373798_0.csv',\
	'ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/2373798.csv']
# 799 = S-1
files['799'] = ['25 August 2010/station3-1.csv','ShuttleReadout10_22_10_08_47_13_AM_PDT/2373799_0.csv',\
	'ShuttleReadout09_07_11_05_38_23_PM_PDT/2373799_1.csv','6 Feb 2012/2373799.csv',\
	'ShuttleReadout03_16_12_12_04_52_PM_GMT-07_00/2373799.csv','ShuttleReadout05_07_12_04_22_10_PM_GMT-07_00/2373799.csv',\
	'ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/2373799.csv']
# 800 = 1-4
files['800'] = ['25 August 2010/station1-4.csv','ShuttleReadout12_10_10_10_02_57_AM_PST/2373800.csv',\
	'ShuttleReadout09_07_11_05_38_23_PM_PDT/2373800_0.csv','6 Feb 2012/2373800.csv',\
	'ShuttleReadout03_16_12_12_04_52_PM_GMT-07_00/2373800.csv','ShuttleReadout05_07_12_02_07_41_PM_GMT-07_00/2373800_0.csv',\
	'ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/2373800.csv']
# 803 = S-3
files['803'] = ['25 August 2010/station3-3.csv','ShuttleReadout10_22_10_08_47_13_AM_PDT/2373803_0.csv',\
	'ShuttleReadout09_07_11_05_38_23_PM_PDT/2373803_1.csv','6 Feb 2012/2373803.csv',\
	'ShuttleReadout03_16_12_12_04_52_PM_GMT-07_00/2373803.csv','ShuttleReadout05_07_12_04_22_10_PM_GMT-07_00/2373803.csv',\
	'ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/2373803.csv']
# 804 = 2-3
files['804'] = ['25 August 2010/station2-3.csv','ShuttleReadout10_22_10_08_47_13_AM_PDT/2373804_0.csv',\
	'ShuttleReadout09_07_11_05_38_23_PM_PDT/2373804_1.csv','ShuttleReadout09_07_11_05_38_23_PM_PDT/2373804_2.csv',\
	'6 Feb 2012/2373804.csv','ShuttleReadout03_16_12_12_04_52_PM_GMT-07_00/2373804.csv',\
	'ShuttleReadout05_07_12_04_56_23_PM_GMT-07_00/2373804.csv','ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/2373804.csv']
# 807 = 1-2
files['807'] = ['25 August 2010/station1-2.csv','ShuttleReadout12_10_10_10_02_57_AM_PST/2373807.csv',\
	'ShuttleReadout09_07_11_05_38_23_PM_PDT/2373807_0.csv','6 Feb 2012/2373807.csv',\
	'ShuttleReadout03_16_12_12_04_52_PM_GMT-07_00/2373807.csv','ShuttleReadout05_07_12_02_07_41_PM_GMT-07_00/2373807_0.csv',\
	'ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/2373807.csv']
# 808 = S-2
files['808'] = ['25 August 2010/station3-2.csv','ShuttleReadout10_22_10_08_47_13_AM_PDT/2373808_0.csv',\
	'ShuttleReadout09_07_11_05_38_23_PM_PDT/2373808_1.csv','6 Feb 2012/2373808.csv',\
	'ShuttleReadout03_16_12_12_04_52_PM_GMT-07_00/2373808.csv','ShuttleReadout05_07_12_04_22_10_PM_GMT-07_00/2373808.csv',\
	'ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/2373808.csv']
# 809 = S-4
files['809'] = ['6 May 2010/Station3-4.csv','25 August 2010/station3-4.csv',\
	'ShuttleReadout10_22_10_08_47_13_AM_PDT/2373809_0.csv','ShuttleReadout09_07_11_05_38_23_PM_PDT/2373809_1.csv',\
	'6 Feb 2012/2373809.csv','ShuttleReadout03_16_12_12_04_52_PM_GMT-07_00/2373809.csv',\
	'ShuttleReadout05_07_12_04_22_10_PM_GMT-07_00/2373809.csv','ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/2373809.csv']
# 810 = 2-2
files['810'] = ['25 August 2010/station2-2.csv','ShuttleReadout10_22_10_08_47_13_AM_PDT/2373810_0.csv',\
	'ShuttleReadout09_07_11_05_38_23_PM_PDT/2373810_1.csv','ShuttleReadout09_07_11_05_38_23_PM_PDT/2373810_2.csv',\
	'6 Feb 2012/2373810.csv','ShuttleReadout03_16_12_12_04_52_PM_GMT-07_00/2373810.csv',\
	'ShuttleReadout05_07_12_04_56_23_PM_GMT-07_00/2373810.csv','ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/2373810.csv']
# 40 = ILean 30m
files['40'] = ['ShuttleReadout05_07_12_03_45_25_PM_GMT-07_00/HydroWatch_10042540_0_mod.csv',\
	'ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/HydroWatch_10042540.csv']
# 52 = ILean 25m
files['52'] = ['ShuttleReadout05_07_12_03_45_25_PM_GMT-07_00/HydroWatch_10042552_0.csv',\
	'ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/HydroWatch_10042552.csv']
# 44 = ILean 20m
files['44'] = ['ShuttleReadout05_07_12_03_45_25_PM_GMT-07_00/HydroWatch_10042544_0.csv',\
	'ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/HydroWatch_10042544.csv']
# 45 = ILean 15m
files['45'] = ['ShuttleReadout05_07_12_03_45_25_PM_GMT-07_00/HydroWatch_10042545_0.csv',\
	'ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/HydroWatch_10042545.csv']
# 43 = ILean 10m
files['43'] = ['ShuttleReadout05_07_12_03_45_25_PM_GMT-07_00/HydroWatch_10042543_0.csv',\
	'ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/HydroWatch_10042543.csv']
# 36 = ILean 5m
files['36'] = ['ShuttleReadout05_07_12_03_45_25_PM_GMT-07_00/HydroWatch_10042536_0.csv',\
	'ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/HydroWatch_10042536.csv']
# 47 = FT 28m
files['47'] = ['ShuttleReadout05_07_12_03_45_25_PM_GMT-07_00/HydroWatch_10042547.csv',\
	'ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/HydroWatch_10042547.csv']
# 56 = FT 22m
files['56'] = ['ShuttleReadout05_07_12_03_45_25_PM_GMT-07_00/HydroWatch_10042556.csv',\
	'ShuttleReadout05_07_12_03_45_25_PM_GMT-07_00/HydroWatch_10042556_0.csv',\
	'ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/HydroWatch_10042556.csv']
# 35 = FT 17m
files['35'] = ['ShuttleReadout05_07_12_03_45_25_PM_GMT-07_00/HydroWatch_10042535.csv',\
	'ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/HydroWatch_10042535.csv']
# 41 = FT 12m
files['41'] = ['ShuttleReadout05_07_12_03_45_25_PM_GMT-07_00/HydroWatch_10042541.csv',\
	'ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/HydroWatch_10042541.csv']
# 33 = FT 7m
files['33'] = ['ShuttleReadout05_07_12_03_45_25_PM_GMT-07_00/HydroWatch_10042533.csv',\
	'ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/HydroWatch_10042533.csv']
# 49 = FT 2m
files['49'] = ['ShuttleReadout05_07_12_03_45_25_PM_GMT-07_00/HydroWatch_10042549.csv',\
	'ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/HydroWatch_10042549.csv']
# 62 = Ursula 25 m
files['62'] = ['ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/HydroWatch_10042562.csv']
# 58 = Ursula 20 m
files['58'] = ['ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/HydroWatch_10042558.csv']
# 54 = Ursula 15 m
files['54'] = ['ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/HydroWatch_10042554.csv']
# 61 = Ursula 10 m
files['61'] = ['ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/HydroWatch_10042561.csv']
# 42 = Ursula 5 m
files['42'] = ['ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/HydroWatch_10042542.csv']
# 59 = SMM 17.5 m
files['59'] = ['ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/HydroWatch_10042559.csv']
# 32 = SMM 15 m
files['32'] = ['ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/HydroWatch_10042532.csv']
# 60 = SMM 10 m
files['60'] = ['ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/HydroWatch_10042560.csv']
# 48 = SMM 5 m
files['48'] = ['ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/HydroWatch_10042548.csv']
# 34 = SMM 2.5 m
files['34'] = ['ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/HydroWatch_10042534.csv']
# 63 = SMU 17.5 m
files['63'] = ['ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/HydroWatch_10042563.csv']
# 37 = SMU 15 m
files['37'] = ['ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/HydroWatch_10042537.csv']
# 66 = SMU 10 m
files['66'] = ['ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/HydroWatch_10042566.csv']
# 65 = SMU 7.5 m
files['65'] = ['ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/HydroWatch_10042565.csv']
# 64 = SMU 5 m
files['64'] = ['ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/HydroWatch_10042564.csv']
# 50 = Freddie 30 m
files['50'] = ['ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/HydroWatch_10042550.csv']
# 51 = Freddie 24 m
files['51'] = ['ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/HydroWatch_10042551.csv']
# 53 = Freddie 18 m
files['53'] = ['ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/HydroWatch_10042553.csv']
# 39 = Freddie 12 m
files['39'] = ['ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/HydroWatch_10042539.csv']
# 46 = Freddie 6 m
files['46'] = ['ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/HydroWatch_10042546.csv']
# 38 = road between well 6 and well 5
files['38'] = ['ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/HydroWatch_10042538.csv']
# 57 = near well 15, top of ridge
files['57'] = ['ShuttleReadout09_16_12_01_13_41_AM_GMT-07_00/HydroWatch_10042557.csv']

# list of sensors placed in the field on May 7 2012
latesensors = ['62','58','54','61','42','59','32','60','48','34','63','37','66','65','64','50','51','53','39','46']

# loop through sensors
sensors = files.keys()
sensors.sort()

dt = dict()
T = dict()
RH = dict()
for ss in sensors:

	print(ss)
	
	dttmp = np.array([])
	Ttmp = np.array([])
	RHtmp = np.array([])
	# loop through files
	for ff in files[ss]:
		
		# read file
		data = csv2rec('./Data/'+ff,skiprows=1,comments='!')
		fields = data.dtype.names
		mask = (data.end_of_file=='')
		if 'coupler_detached' in fields:
			mask = mask & (data.coupler_detached=='')
		if 'coupler_attached' in fields:
			mask = mask & (data.coupler_attached=='')
		if 'stopped' in fields:
			mask = mask & (data.stopped=='')
		Ttmp = np.append(Ttmp,data['temp_\xa1c'][mask])
		RHtmp = np.append(RHtmp,data.rh_[mask])
		
		# adjust time
		if len(ss)==3:
			dttmp = np.append(dttmp,(data.date_time_gmt0700[mask]-datetime.timedelta(seconds=3600))) # Kevin's sensors are on daylight savings time - subtract an hour
		elif len(ss)==2:
			dttmp = np.append(dttmp,data.date_time_gmt0800[mask])
			
	# exclude non-field data for sensors placed in field on May 7 2012
	if ss in latesensors:
		mask = dttmp>=datetime.datetime(2012,5,7,17,0,0)
		dttmp = dttmp[mask]
		Ttmp = Ttmp[mask]
		RHtmp = RHtmp[mask]
		
	# calibrate
	if len(ss)==3:
		mt = calK.mt[calK.sensor==ss]
		bt = calK.bt[calK.sensor==ss]
		mrh = calK.mrh[calK.sensor==ss]
		brh = calK.brh[calK.sensor==ss]
	elif len(ss)==2:
		mt = calnew.mt[calnew.sensor==ss]
		bt = calnew.bt[calnew.sensor==ss]
		mrh = calnew.mrh[calnew.sensor==ss]
		brh = calnew.brh[calnew.sensor==ss]			
		
	Ttmp = mt*Ttmp+bt
	RHtmp = mrh*RHtmp+brh
	
	# adjust rel hum
	RHtmp[RHtmp>100.] = 100.

	if ss=='803':
		RHtmp = RHtmp+np.nan  # replace bad RH sensor data with nans
		
	# save date, temp, rel hum
	dt[ss] = dttmp
	T[ss] = Ttmp
	RH[ss] = RHtmp

data = dict()
data['dt'] = dt
data['T'] = T
data['RH'] = RH
cPickle.dump(data,open('HOBOdata.p','wb'))
