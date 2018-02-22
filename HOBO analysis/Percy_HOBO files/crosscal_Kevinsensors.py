'''
PAL 5/21/2012
read field calibration data between new HOBOs and Kevin's sensors
#
HLM 10/15/2012
changed path for variable calnew and paths in filesK and filesnew, minor modifications to plotting for legibility
'''

import numpy as np
from matplotlib.pyplot import plot,scatter,savefig,figure,colorbar,suptitle,close,show,subplot,rgrids,subplots_adjust
from matplotlib.mlab import csv2rec
import matplotlib as mpl
import datetime
from matplotlib.dates import DateFormatter
from time import mktime
from scipy.interpolate import interp1d

# file with calibration relationships for new sensors
#calnew = '/Users/percy/Documents/Research/Data/Rivendell/Micromet/HOBO calibration/linregressions.csv'
calnew = './linregressions.csv'

# list of Feb-May files - for new sensors and for Kevin's sensors
filesK = {'795':'./Data/ShuttleReadout05_07_12_02_07_41_PM_GMT-07_00/2373795_0.csv', \
	'796':'./Data/ShuttleReadout05_07_12_04_56_23_PM_GMT-07_00/2373796.csv', \
	'797':'./Data/ShuttleReadout05_07_12_04_56_23_PM_GMT-07_00/2373797.csv', \
	'798':'./Data/ShuttleReadout05_07_12_02_07_41_PM_GMT-07_00/2373798_0.csv', \
	'799':'./Data/ShuttleReadout05_07_12_04_22_10_PM_GMT-07_00/2373799.csv', \
	'800':'./Data/ShuttleReadout05_07_12_02_07_41_PM_GMT-07_00/2373800_0.csv', \
	'803':'./Data/ShuttleReadout05_07_12_04_22_10_PM_GMT-07_00/2373803.csv', \
	'804':'./Data/ShuttleReadout05_07_12_04_56_23_PM_GMT-07_00/2373804.csv', \
	'807':'./Data/ShuttleReadout05_07_12_02_07_41_PM_GMT-07_00/2373807_0.csv', \
	'808':'./Data/ShuttleReadout05_07_12_04_22_10_PM_GMT-07_00/2373808.csv', \
	'809':'./Data/ShuttleReadout05_07_12_04_22_10_PM_GMT-07_00/2373809.csv', \
	'810':'./Data/ShuttleReadout05_07_12_04_56_23_PM_GMT-07_00/2373810.csv' }
sensorsK = filesK.keys()
sensorsK.sort()

filesnew = {'34':'./Data/ShuttleReadout05_07_12_04_56_23_PM_GMT-07_00/HydroWatch_10042534.csv', \
	'37':'./Data/ShuttleReadout05_07_12_04_56_23_PM_GMT-07_00/HydroWatch_10042537.csv', \
	'48':'./Data/ShuttleReadout05_07_12_04_56_23_PM_GMT-07_00/HydroWatch_10042548.csv', \
	'50':'./Data/ShuttleReadout05_07_12_04_56_23_PM_GMT-07_00/HydroWatch_10042550.csv', \
	'51':'./Data/ShuttleReadout05_07_12_04_22_10_PM_GMT-07_00/HydroWatch_10042551.csv', \
	'54':'./Data/ShuttleReadout05_07_12_02_07_41_PM_GMT-07_00/HydroWatch_10042554_0.csv', \
	'58':'./Data/ShuttleReadout05_07_12_02_07_41_PM_GMT-07_00/HydroWatch_10042558_0.csv', \
	'59':'./Data/ShuttleReadout05_07_12_02_07_41_PM_GMT-07_00/HydroWatch_10042559_0.csv', \
	'60':'./Data/ShuttleReadout05_07_12_04_22_10_PM_GMT-07_00/HydroWatch_10042560.csv', \
	'61':'./Data/ShuttleReadout05_07_12_04_22_10_PM_GMT-07_00/HydroWatch_10042561.csv', \
	'62':'./Data/ShuttleReadout05_07_12_02_07_41_PM_GMT-07_00/HydroWatch_10042562_0.csv', \
	'66':'./Data/ShuttleReadout05_07_12_04_22_10_PM_GMT-07_00/HydroWatch_10042566.csv' }
sensorsnew = filesnew.keys()
sensorsnew.sort()
	
crosslist = {'795':'58', \
	'796':'48', \
	'797':'37', \
	'798':'54', \
	'799':'66', \
	'800':'59', \
	'803':'61', \
	'804':'34', \
	'807':'62', \
	'808':'51', \
	'809':'60', \
	'810':'50' }

# read in new sensors calibration relationships
calnewparams = csv2rec(calnew)

# adjust Feb-May data for new sensors
dtnew = dict()
Tnew = dict()
RHnew = dict()

for ss in sensorsnew:
	print(ss)
	
	filein = filesnew[ss]
	
	mt = calnewparams.mt[calnewparams.sensor==ss]
	bt = calnewparams.bt[calnewparams.sensor==ss]
	mrh = calnewparams.mrh[calnewparams.sensor==ss]
	brh = calnewparams.brh[calnewparams.sensor==ss]
	
	data = csv2rec(filein,skiprows=1,comments='!')
	mask = (data.coupler_detached=='') & (data.coupler_attached=='') & (data.stopped=='') & (data.end_of_file=='')
	dttmp = data.date_time_gmt0800[mask]
	Ttmp = data['temp_\xa1c'][mask]
	RHtmp = data.rh_[mask]
	
	Ttmp = Ttmp*mt+bt
	RHtmp = RHtmp*mrh+brh
	
	dtnew[ss] = dttmp
	Tnew[ss] = Ttmp
	RHnew[ss] = RHtmp

# interpolate Kevin's sensors to same time as comparison new sensor
mT = np.zeros(len(sensorsK))+np.nan
bT = np.zeros(len(sensorsK))+np.nan
mRH = np.zeros(len(sensorsK))+np.nan
bRH = np.zeros(len(sensorsK))+np.nan

f = figure(figsize=(18,8))

fid = open('calibrations_Kevinsensors.csv','w')
header = 'sensor,mT,bT,mRH,bRH'
fid.write(header+'\n')

for ii,sk in enumerate(sensorsK):
	print(sk)
	sn = crosslist[sk]
	filein = filesK[sk]
	data = csv2rec(filein,skiprows=1,comments='!')
	mask = (data.coupler_detached=='') & (data.coupler_attached=='') & (data.stopped=='') & (data.end_of_file=='')
	dttmp = data.date_time_gmt0700[mask]
	dttmp = dttmp-datetime.timedelta(seconds=3600) # Kevin's sensors are on daylight savings time - subtract an hour
	Ttmp = data['temp_\xa1c'][mask]
	RHtmp = data.rh_[mask]
	
	# convert datetime arrays to datenum (seconds)
	dnumN = [mktime(dtnew[sn][n].timetuple()) for n in xrange(len(dtnew[sn]))]
	dnumK = [mktime(dttmp[n].timetuple()) for n in xrange(len(dttmp))]
	
	# interpolate T & RH from K to new sensor
	fn = interp1d(dnumK,Ttmp,bounds_error=False)
	Tinterp = fn(dnumN)
	maskT = (np.isfinite(Tinterp)) & (np.isfinite(Tnew[sn]))
	fn = interp1d(dnumK,RHtmp,bounds_error=False)
	RHinterp = fn(dnumN)
	maskRH = (np.isfinite(RHinterp)) & (np.isfinite(RHnew[sn]))
	
	# plot comparisons & regress
	xT = Tinterp[maskT]; yT = Tnew[sn][maskT]
	xRH = RHinterp[maskRH]; yRH = RHnew[sn][maskRH]
	xRH[xRH>100.] = 100.; yRH[yRH>100.] = 100.  # round any RH values over 100 down to 100
	
	AT = np.vstack([xT, np.ones(len(xT))]).T
	ARH = np.vstack([xRH, np.ones(len(xRH))]).T
	
	mT[ii], bT[ii] = np.linalg.lstsq(AT, yT)[0]
	mRH[ii], bRH[ii] = np.linalg.lstsq(ARH, yRH)[0]

	ax = f.add_subplot(1,2,1)
	ax.plot(xT,yT,'.')
	linepts = np.array([np.min(xT),np.max(xT)])
	ax.plot(linepts,mT[ii]*linepts+bT[ii],color='gray')
	ax.set_title('temperature, m='+str(round(mT[ii],2))+', b='+str(round(bT[ii],2)))
	ax.set_xlabel('T, sensor '+str(sk))
	ax.set_ylabel('T, sensor '+str(sn)+', adjusted')
	
	ax = f.add_subplot(1,2,2)
	ax.plot(xRH,yRH,'.')
	linepts = np.array([np.min(xRH),np.max(xRH)])
	ax.plot(linepts,mRH[ii]*linepts+bRH[ii],color='gray')
	ax.set_title('rel hum, m='+str(round(mRH[ii],2))+', b='+str(round(bRH[ii],2)))
	ax.set_xlabel('RH, sensor '+str(sk))
	ax.set_ylabel('RH, sensor '+str(sn)+', adjusted')
	
	f.suptitle('sensor '+str(sk))

	subplots_adjust(wspace=0.3)
	f.savefig('regression_'+str(sk)+'.pdf',format='pdf')
	f.clf()

	# write parameters to csv file
	line = str(sk)+','+str(mT[ii])+','+str(bT[ii])+','+str(mRH[ii])+','+str(bRH[ii])
	fid.write(line+'\n')

fid.close()
