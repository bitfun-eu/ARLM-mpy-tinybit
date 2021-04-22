from microbit import i2c, pin1, pin12, pin13, pin14, pin15, pin16
from machine import time_pulse_us

import neopixel as np

import music
from utime import sleep_us as usleep

i2c.init()
led = np.NeoPixel(pin12, 2)
pin13.set_pull(pin13.NO_PULL)
pin14.set_pull(pin14.NO_PULL)

ADDR = 0x01

CMD_RGB = 0x01
CMD_MOTOR = 0x02

def light(index, red, green, blue):
    assert index in (0,1)
    assert 0 <= red <= 255
    assert 0 <= green <= 255
    assert 0 <= blue <= 255
    if index == 0:
        i2c.write(ADDR, bytes((CMD_RGB, red, green, blue)))
    elif index == 1:
        led[0] = (red, green, blue)
        led[1] = (red, green, blue)
        led.show()

def run(left, right):
    assert -255 <= left <= 255
    assert -255 <= right <= 255
    if left >= 0:
        b0 = left
        b1 = 0
    else:
        b0 = 0
        b1 = -left
    if right >= 0:
        b2 = right
        b3 = 0
    else:
        b2 = 0
        b3 = -right
    i2c.write(ADDR, bytes((CMD_MOTOR, b0,b1,b2,b3)))

def sing():
    music.play(music.NYAN)

def line(left=pin13, right=pin14):
    return (left.read_digital(), right.read_digital())

def sound(p=pin1):
    return pin1.read_analog()

def measure(echo=pin15, trigger=pin16, loops=1):
    echo.read_digital()
    r = []
    for i in range(loops):
        trigger.write_digital(0)
        usleep(2)
        trigger.write_digital(1)
        usleep(15)
        trigger.write_digital(0)
        micros = time_pulse_us(echo, 1)
        if micros == -2:
            raise Exception("waiting pin to be value 1 timeout")
        elif micros == -1:
            raise Exception("waiting pin to be value 0 timeout")
        elif micros < 0:
            raise Exception("unknown error")
        else:
            t_echo = micros / 1000000
            dist_cm = (t_echo / 2) * 34300
            r.append(dist_cm)

    return sum(r)/loops

# EOF
