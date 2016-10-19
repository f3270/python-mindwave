#coding: latin-1
# Run me with frameworkpython inside a virtual environment.

# This program connect to ThinkGear and receives via TCP/IP all the
# raw streaming from NeuroSky MindWave Mobile (the black headset)
# It also plot the signal using matplotlib.

import socket
import json

import time, datetime, sys

import matplotlib.pyplot as plt

class Plotter:

    def __init__(self,rangeval,minval,maxval):
        # You probably won't need this if you're embedding things in a tkinter plot...
        import matplotlib.pyplot as plt
        plt.ion()

        self.x = []
        self.y = []
        self.z = []

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)

        self.line1, = self.ax.plot(self.x,'r', label='X') # Returns a tuple of line objects, thus the comma
        self.line2, = self.ax.plot(self.y,'g', label='Y')
        self.line3, = self.ax.plot(self.z,'b', label='Z')

        self.rangeval = rangeval
        self.ax.axis([0, rangeval, minval, maxval])
        self.plcounter = 0
        self.plotx = []

    def plotdata(self,new_values):
        # is  a valid message struct
        #print new_values

        self.x.append( float(new_values[0]))
        self.y.append( float(new_values[1]))
        self.z.append( float(new_values[2]))

        self.plotx.append( self.plcounter )

        self.line1.set_ydata(self.x)
        self.line2.set_ydata(self.y)
        self.line3.set_ydata(self.z)

        self.line1.set_xdata(self.plotx)
        self.line2.set_xdata(self.plotx)
        self.line3.set_xdata(self.plotx)

        self.fig.canvas.draw()
        plt.pause(0.0001)

        self.plcounter = self.plcounter+1

        if self.plcounter > self.rangeval:
          self.plcounter = 0
          self.plotx[:] = []
          self.x[:] = []
          self.y[:] = []
          self.z[:] = []


import mindwave, time

headset = mindwave.Headset('/dev/tty.MindWaveMobile-DevA','ef47')

time.sleep(2)

plotter = Plotter(500,-500,500)

attention = 0
meditation = 0
eeg = 0

# def on_raw( headset, rawvalue):
#     time.sleep(.01)
#     print "Count %d :Raw value: %s, Attention: %s, Meditation: %s" % (headset.count, headset.raw_value, headset.attention, headset.meditation)
#     (eeg, attention, meditation) = (headset.raw_value, headset.count, headset.meditation)
#     plotter.plotdata( [eeg, attention, meditation])
#
# headset.raw_value_handlers.append( on_raw )

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')
f = open('./data/eeg.'+st+'.dat', 'w')

try:
    while (headset.poor_signal > 5):
        print "Headset signal noisy %d. Adjust the headset to adjust better to your forehead." % (headset.poor_signal)

    while (True):
        time.sleep(.01)
        (eeg, attention, meditation) = (headset.raw_value, headset.count, headset.meditation)
        #plotter.plotdata( [eeg, attention, meditation])
        plotter.plotdata( [eeg, 0, 0])
        f.write( str(eeg) + ' ' + str(attention) + ' ' + str(meditation) + '\n')
finally:
    headset.disconnect()
    headset.serial_close()
    f.close()
