import mindwave, time
from pprint import pprint

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

while True:
    time.sleep(.5)
    print "Raw value: %s, Attention: %s, Meditation: %s" % (headset.raw_value, headset.attention, headset.meditation)
    pprint(headset.waves)
