#coding: latin-1
# Run me with frameworkpython inside a virtual environment.

# This program connect to ThinkGear and receives via TCP/IP all the
# raw streaming from NeuroSky MindWave Mobile (the black headset)
# It also plot the signal using matplotlib.

import socket, select
import json

import matplotlib.pyplot as plt

import time, datetime, sys

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


ip = '127.0.0.1'
port = 13854

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (ip,port)
sock.connect(server_address)

# Send to ThinkGear the command to start receiving packages.
msg = "{\"enableRawOutput\": true, \"format\": \"JSON\"}"
sent = sock.sendto(msg, server_address)


# Make the socket to be crlf aware.
myfile = sock.makefile()
data = myfile.readline()

plotter = Plotter(500,-500,500)

attention = 0
meditation = 0
eeg = 0

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')
f = open('eeg.'+st+'.dat', 'w')

conn_list = []
serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('0.0.0.0', 13855)
serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
print >> sys.stderr, 'Starting up on %s port %s', server_address
serversock.bind(server_address)
serversock.listen(10)

conn_list.append( serversock )

#print >>sys.stderr, 'waiting for a connection'
#connection, client_address = serversock.accept()
#print >>sys.stderr, 'Connection established!'

try:
    while (True):
        data = myfile.readline()

        print data

        obj = json.loads(data)

        if "rawEeg" in obj:
            eeg = obj["rawEeg"]

        if "eSense" in obj:
            attention = obj["eSense"]["attention"]
            meditation = obj["eSense"]["meditation"]

        f.write( str(eeg) + ' ' + str(attention) + ' ' + str(meditation) + '\n')
        #sent = connection.send(data)
        plotter.plotdata( [eeg, attention, meditation])

        read_sockets,write_sockets,error_sockets = select.select(conn_list, [],[])

        for connsock in read_sockets:
            if connsock == serversock:
                sockfd, addr = serversock.accept()
                conn_list.append( sockfd )
                print "Client (%s, %s) connected " % addr

            else:
                try:
                    sent = connsock.send(str(eeg) + ' ' + str(attention) + ' ' + str(meditation) + '\n')

                except:
                    print  "Client (%s, %s) is offline " % addr
                    connsock.close()
                    conn_list.remove(connsock)
                    continue

finally:
    sock.close()
    f.close()
    #connection.close()
    serversock.close()
