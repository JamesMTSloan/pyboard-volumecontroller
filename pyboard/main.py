import pyb

vcp = pyb.USB_VCP()
sw = pyb.Switch()
led_1 = pyb.LED(1)
acc = pyb.Accel()

vcp.setinterrupt(-1)

DELAY = 100

led_1.toggle()
pyb.delay(int(DELAY))
led_1.toggle()


def calcDegree(x_val):
    if x_val >= 0:
        sign = 1
    else:
        sign = -1
    degree = abs(x_val) // 9
    sign *= -1  # flip x-axis
    return sign * degree


button_flag = False

while True:
    if sw():
        c = "BUT"
        button_flag = True
    else:
        x = acc.x()
        c = calcDegree(x)

    buf = str(c).encode("utf-8")
    vcp.write(buf + b"\n")
    pyb.delay(DELAY)

    if button_flag:
        # extend delay until next iteration
        # to prevent debounce effect
        pyb.delay(DELAY * 2)
        button_flag = False
