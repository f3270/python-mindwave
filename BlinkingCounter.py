import csv
import numpy as np

results = []
with open('eeg.2016-09-13-17-44-27.dat') as inputfile:
    for row in csv.reader(inputfile):
        rows = row[0].split(' ')
        results.append(rows)

print len(results)

print results[0]


results = np.asarray(results)
results = results.astype(int)

# Strip from the signal anything you want
eeg = results[1:2948,0]

print eeg

import matplotlib.pyplot as plt
fig = plt.figure()
ax1 = fig.add_subplot(111)

ax1.plot(eeg,'r', label='EEG')
plt.legend(loc='upper left');
plt.show()

signalthreshold = 60


boolpeaks = np.where( eeg < -signalthreshold  )
print boolpeaks
dpeaks = np.diff( eeg )
print dpeaks
pdpeaks = np.where( dpeaks > 0)
print pdpeaks
print (pdpeaks != 0)
a = np.in1d(pdpeaks,boolpeaks)
print a
blinkings = a.sum()

print "Blinkings: %d" % blinkings
