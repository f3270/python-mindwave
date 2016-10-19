#coding: latin-1
# Run me with frameworkpython inside a virtual environment.

# This program connect to ThinkGear and receives via TCP/IP all the
# raw streaming from NeuroSky MindWave Mobile (the black headset)
# It also plot the signal using matplotlib.

import cv2
import socket
import json

import thread

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

def film():
    import cv2

    cap = cv2.VideoCapture(0)

    cap.set(3,640)
    cap.set(4,480)

    w = cap.get(cv2.CAP_PROP_FRAME_WIDTH);
    h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT);
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    out = cv2.VideoWriter('output.avi',fourcc, 15.0, (int(w),int(h)))

    while (True):
        ret, frame = cap.read()

        out.write(frame)
        #cv2.imshow('Video Stream', frame)

        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord('q'):
            break

    cap.release()
    out.release()


thread.start_new_thread( film, () )

# def on_raw( headset, rawvalue):
#     time.sleep(.01)
#     print "Count %d :Raw value: %s, Attention: %s, Meditation: %s" % (headset.count, headset.raw_value, headset.attention, headset.meditation)
#     (eeg, attention, meditation) = (headset.raw_value, headset.count, headset.meditation)
#     plotter.plotdata( [eeg, attention, meditation])
#
# headset.raw_value_handlers.append( on_raw )

try:
    while (headset.poor_signal > 5):
        print "Headset signal is too bad %d. Adjust the headset to fit your head." % (headset.poor_signal)

        time.sleep(.01)
        (eeg, attention, meditation) = (headset.raw_value, headset.count, headset.meditation)
        #plotter.plotdata( [eeg, attention, meditation])
        plotter.plotdata( [eeg, 0, 0])
finally:
    headset.disconnect()
    headset.serial_close()
    cv2.destroyAllWindows()
