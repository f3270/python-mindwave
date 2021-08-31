#coding: latin-1
#
# This program uses Mindawave object to connect using bluetooth to Mindwave
# and get the raw eeg signals from there.
# 
# It also plot the signal using matplotlib.
#
# The data is also dumped into a file, but keep in mind that the capture of data
# from python can be slower than the driver and the effictive sampling frequency
# could be lower.
#
# Fs = 128 (nominally it should be 512 but never managed to work at that sampling freq)

import socket,select

import time, datetime, sys

import matplotlib.pyplot as plt

import sys

lamdalength = 10
Fs=128
show=False

# Please provide the number of sample points to take
if (len(sys.argv) > 1):
    samplepoints = int(sys.argv[1])
else:
    samplepoints = Fs*lamdalength

print('Please remove the VGA connection that sometimes interfere with Mindwave')


import mindwave, time

headset = mindwave.Headset('/dev/tty.MindWaveMobile-DevA','ef47')

time.sleep(2)

from Plotter import Plotter
plotter = Plotter(500,-500,500)

attention = 0
meditation = 0
eeg = 0


ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')
filename = './data/eeg.'+st+'.dat'
f = open(filename, 'w')

try:
    while (headset.poor_signal > 5):
        print("Headset signal noisy %d. Adjust the headset and the earclip." % (headset.poor_signal))

    print("Writing %d seconds output to %s" % (lamdalength,filename))
    for i in range(0,samplepoints):
        time.sleep(.01)
        (count,eeg, attention, meditation, blink) = (headset.count, headset.raw_value, headset.attention, headset.meditation, headset.blink)

        plotter.plotdata( [eeg, attention, meditation, blink])
        ts = time.time()
        f.write( str(ts) + ' ' + str(count) + ' ' + str(eeg) + ' ' + str(attention) + ' ' + str(meditation) + ' ' + str(blink) + '\n')


finally:
    headset.stop()
    f.close()
