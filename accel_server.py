import serial
import time

from alsaaudio import Mixer


name_0 = '/dev/ttyACM0'
BAUD_RATE = 115200

mix = Mixer()


def checkPort(port):
    try:
        ser = serial.Serial(port, BAUD_RATE, timeout=1)
        print("Connected!")
        return True
    except OSError:
        return False


def checkBuffer(b):
    return not (b and (b[-1] == '\n'))


def changeVolume(m, degree):
    if degree:
        current_volume = m.getvolume()[0]
        new_volume = current_volume + degree
        if new_volume < 0:
            new_volume = 0
        elif new_volume > 100:
            new_volume = 100
        m.setvolume(new_volume)
        print("Volume set to {}%".format(new_volume))


def mute_unmute(m):
    is_muted = bool(m.getmute()[0])
    m.setmute(not is_muted)
    if not is_muted:
        print("Muted")
    else:
        print("Unmuted")


# attempt to connect once per second until success
while not checkPort(name_0):
    time.sleep(1)

ser = serial.Serial(name_0, BAUD_RATE, timeout=1)

buf = []

while True:
    while checkBuffer(buf):
        received = ser.read(size=1).decode("utf-8")
        buf.append(received)

    c = ''.join(buf[:-1])

    try:
        accel_data = int(c)
        # print("Received accel data: {}".format(accel_data))
        changeVolume(mix, accel_data)

    except ValueError:
        if c == "BUT":
            mute_unmute(mix)

    buf = []
