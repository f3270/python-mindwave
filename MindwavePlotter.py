#coding: latin-1

# Run me with frameworkpython

import numpy as np

import mindwave, time
import matplotlib.pyplot as plt


headset = mindwave.Headset('/dev/tty.MindWaveMobile-DevA','ef47')

time.sleep(2)


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




class mymindwave:
    def __init__(self):
        self.raw = 0
        self.plotter = Plotter(500,-1000,1000)

    def on_raw(self, headset, rawvalue):
        self.raw = rawvalue
        print "Raw %d" % (self.raw)
        self.plotter.plotdata( [rawvalue, 0, 0])

#def on_raw(headset, rawvalue):
#    plotter.plotdata( [rawvalue, 0, 0])
my = mymindwave()
headset.raw_value_handlers.append( my.on_raw )

try:
    while (True):
        print "Attention: %s, Meditation: %s" % (headset.attention, headset.meditation)
except KeyboardInterrupt as e:
    print e.message
finally:
    print "Disconnecting..."
    headset.disconnect()
