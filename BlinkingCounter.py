#coding: latin-1

import csv
import numpy as np

results = []

print 'Este programa tiene que ejecutarse con python 2.7!'

# Esta primera linea, abre el archivo 'blinking.dat' que se grabó
# al establecerse la conexión con el servidor.
with open('blinking.dat') as inputfile:
    for row in csv.reader(inputfile):
        rows = row[0].split(' ')
        results.append(rows[0:])

print 'Longitud del archivo:'+str(len(results))

# Convert the file into numpy array of ints.
results = np.asarray(results)
results = results.astype(int)

# Strip from the signal anything you want


# La primer columna corresponde a el largo del archivo a considerar
# en relación a las muestras (1:100 serian las muestras) representante
# del tiempo.
# La segunda columna, corresponde a: eeg, attention y meditation.
eeg = results[1:100,0]

print eeg

import matplotlib.pyplot as plt
fig = plt.figure()
ax1 = fig.add_subplot(111)

ax1.plot(eeg,'r', label='EEG')
plt.legend(loc='upper left');
plt.show()


# El threshold corresponde al limite en amplitud a considerar para discriminar
# que es un pestañeo de qué no lo es.
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
