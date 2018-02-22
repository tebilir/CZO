'''
PAL 5/1/2012
get calibration relationships between HOBO loggers, and against Rivendell weather stations.
HLM 10/15/2012
changed path for outfile linregressions.csv, minor modifications to plotting to legibility
'''

import numpy as np
from matplotlib.pyplot import plot,scatter,savefig,figure,colorbar,suptitle,close,show,subplot,rgrids
from matplotlib.mlab import csv2rec
import matplotlib as mpl
import datetime
from matplotlib.dates import DateFormatter

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 6}

import matplotlib
matplotlib.rc('font', **font)

sensors = np.arange(32,67)
sensors = sensors[sensors!=55]
mindt = datetime.datetime(2012,1,10,18,0,0)
maxdt = datetime.datetime(2012,2,3,20,0,0)
nsec = (maxdt-mindt).days*86400+(maxdt-mindt).seconds
dtarr = np.array([mindt+datetime.timedelta(seconds=x) for x in range(0,nsec,900)])

# load calibration datasets
T = np.zeros((len(dtarr),len(sensors)))+np.nan
RH = np.zeros((len(dtarr),len(sensors)))+np.nan
for ii,ss in enumerate(sensors):
	print(ss)
	data = csv2rec('HydroWatch_100425'+str(ss)+'.csv',skiprows=1,comments='!')
	dttmp = data.date_time_gmt0800
	Ttmp = data['temp_\xa1c']
	RHtmp = data.rh_
	for jj,dd in enumerate(dtarr):
		mask = dttmp==dd
		T[jj,ii] = Ttmp[mask]
		RH[jj,ii] = RHtmp[mask]
		
meanT = np.mean(T,axis=1)
meanT = np.transpose(np.tile(meanT,(len(sensors),1)))
anomT = T-meanT

f = figure()
f.subplots_adjust(hspace=0.3,wspace=0.3)
count = 1
for ii,ss in enumerate(sensors):
	ax=f.add_subplot(3,3,(ss-min(sensors))%9+1)
	ax.plot(dtarr,anomT[:,ii])
	ax.set_title('sensor '+str(ss))
	ax.grid()
	ax.set_ylim(-1.5,1.5)
	ax.xaxis.set_major_formatter( DateFormatter('%d') )
	if ((ss-np.min(sensors)+1)%9==0) | (ss==np.max(sensors)):
		f.savefig('Tanomplots'+str(count)+'.pdf',format='pdf')
		f.clf()
		f.subplots_adjust(hspace=0.3,wspace=0.3)
		count = count+1

meanRH = np.mean(RH,axis=1)
meanRH = np.transpose(np.tile(meanRH,(len(sensors),1)))
anomRH = RH-meanRH

f.subplots_adjust(hspace=0.3,wspace=0.3)
count = 1
for ii,ss in enumerate(sensors):
	ax=f.add_subplot(3,3,(ss-min(sensors))%9+1)
	ax.plot(dtarr,anomRH[:,ii])
	ax.set_title('sensor '+str(ss))
	ax.grid()
	#ax.set_ylim(-1.5,1.5)
	ax.xaxis.set_major_formatter( DateFormatter('%d') )
	if ((ss-np.min(sensors)+1)%9==0) | (ss==np.max(sensors)):
		f.savefig('RHanomplots'+str(count)+'.pdf',format='pdf')
		f.clf()
		f.subplots_adjust(hspace=0.3,wspace=0.3)
		count = count+1

# linearly regress each sensor against sensor 51 (middle of the pack)
yT = T[:,sensors==51]
yRH = RH[:,sensors==51]
mT = np.zeros(len(sensors))+np.nan
bT = np.zeros(len(sensors))+np.nan
mRH = np.zeros(len(sensors))+np.nan
bRH = np.zeros(len(sensors))+np.nan
for ii,ss in enumerate(sensors):
	xT = T[:,ii]
	xRH = RH[:,ii]
	AT = np.vstack([xT, np.ones(len(xT))]).T
	ARH = np.vstack([xRH, np.ones(len(xRH))]).T
	mT[ii], bT[ii] = np.linalg.lstsq(AT, yT)[0]
	mRH[ii], bRH[ii] = np.linalg.lstsq(ARH, yRH)[0]
	
	ax = f.add_subplot(1,2,1)
	ax.plot(xT,yT,'.')
	linepts = np.array([np.min(xT),np.max(xT)])
	ax.plot(linepts,mT[ii]*linepts+bT[ii],color='gray')
	ax.set_title('temperature, m='+str(round(mT[ii],2))+', b='+str(round(bT[ii],2)))
	ax.set_xlabel('T, sensor '+str(ss))
	ax.set_ylabel('T, sensor 51')
	
	ax = f.add_subplot(1,2,2)
	ax.plot(xRH,yRH,'.')
	linepts = np.array([np.min(xRH),np.max(xRH)])
	ax.plot(linepts,mRH[ii]*linepts+bRH[ii],color='gray')
	ax.set_title('rel hum, m='+str(round(mRH[ii],2))+', b='+str(round(bRH[ii],2)))
	ax.set_xlabel('RH, sensor '+str(ss))
	ax.set_ylabel('RH, sensor 51')
	
	f.suptitle('sensor '+str(ss))

	f.savefig('regression_'+str(ss)+'.pdf',format='pdf')
	f.clf()
	
# output regression equations
fid = open('../linregressions.csv','w')
header = 'sensor,mT,bT,mRH,bRH'
fid.write(header+'\n')
for ii,ss in enumerate(sensors):
	line = str(ss)+','+str(mT[ii])+','+str(bT[ii])+','+str(mRH[ii])+','+str(bRH[ii])
	fid.write(line+'\n')
fid.close()
