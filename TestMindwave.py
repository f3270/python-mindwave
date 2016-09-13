import mindwave, time

headset = mindwave.Headset('/dev/tty.MindWaveMobile-DevA','ef47')

time.sleep(2)

# headset.connect()
# print "Connecting..."
#
# while headset.status != 'connected':
#     time.sleep(0.5)
#     if headset.status == 'standby':
#         headset.connect()
#         print "Retrying connect..."
# print "Connected."

myraw = 0

class mymindwave:
    def __init__(self):
        self.raw = 0

    def on_raw(self, headset, rawvalue):
        self.raw = rawvalue
        print "Raw %d" % (self.raw)

my = mymindwave()
headset.raw_value_handlers.append( my.on_raw )

print headset.poor_signal

try:
    while (True):
        print "Attention: %s, Meditation: %s" % (headset.attention, headset.meditation)
finally:
    headset.disconnect()


headset.disconnect()
