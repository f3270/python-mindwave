#coding: latin-1
#
# STEM - Blinking Counter

# Este programa es un ejemplo de utilizacion de python para implementar un simple
# contador de penstaneos basados en una senal de EMG/EMG/EOG.
#
# Frecuencia de sampleo Fs = 128
import csv
import numpy as np

from scipy import sparse
from scipy.sparse.linalg import spsolve

import peakutils

def baseline_als(y, lam, p, niter=10):
  L = len(y)
  D = sparse.diags([1,-2,1],[0,-1,-2], shape=(L,L-2))
  w = np.ones(L)
  for i in range(niter):
    W = sparse.spdiags(w, 0, L, L)
    Z = W + lam * D.dot(D.transpose())
    z = spsolve(Z, w*y)
    w = p * (y > z) + (1-p) * (y < z)
  return z


results = []

print 'Este programa tiene que ejecutarse con python 2.7!'

# Esta primera linea, abre el archivo 'blinking.dat' que se grabó
# al establecerse la conexión con el servidor.
with open('blinking.dat') as inputfile:
    for row in csv.reader(inputfile):
        rows = row[0].split(' ')
        results.append(rows[1:])

print 'Longitud del archivo:'+str(len(results))

# Convert the file into numpy array of ints.
results = np.asarray(results)
results = results.astype(int)

# Strip from the signal anything you want


# La primer columna corresponde a el largo del archivo a considerar
# en relación a las muestras (1:100 serian las muestras) representante
# del tiempo.
# La segunda columna, corresponde a: eeg, attention y meditation.
eeg = results[1:,0]

print eeg

eeg = np.ones((64))

eeg = np.arange(64)

print eeg.shape

eeg[32] = 120

eeg[43] = -130

eeg = eeg - baseline_als(eeg,10000,0.5)


import matplotlib.pyplot as plt
fig = plt.figure()
ax1 = fig.add_subplot(111)

ax1.plot(eeg,'r', label='EEG')
plt.legend(loc='upper left');
plt.show()




# El threshold corresponde al limite en amplitud a considerar para discriminar
# que es un pestañeo de qué no lo es.
signalthreshold = 140

def crest_factor(x):
    return np.max(np.abs(x))/np.sqrt(np.mean(np.square(x)))

ptp = abs(np.max(eeg)) + abs(np.min(eeg))
rms = np.sqrt(np.mean(eeg**2))
cf = crest_factor(eeg)

print ptp
print rms
print cf

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
