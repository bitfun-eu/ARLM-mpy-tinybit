# Add your Python code here. E.g.
from microbit import *
from tinybit import *
import radio

radio.on()
radio.config(power=7, channel=0, address=0, group=0, data_rate=radio.RATE_250KBIT)

def sonar_run(speed=60, delta=0):
    left = speed - delta
    right = speed + delta
    d = measure()
    if d < 30:
        run(-left, -right)
    elif d > 50:
        run(left, right)
    else:
        run(0, 0)

def line_follow(speed=60, delta=20):
    left, right = line()
    speed_map = {
        00: (speed, speed),
        01: (speed+delta, speed),
        10: (speed, speed+delta),
        11: (speed, speed),
    }
    key = left*10 + right
    left_speed, right_speed = speed_map[key]
    run(left_speed, right_speed)

def cap_speed(n):
    if n < -255: return -255
    elif n > 255: return 255
    else: return n

def radio_run():
    try:
        data = radio.receive()
        left, right = data.split()
    except:
        display.set_pixel(0, 0, 5)
        return
    display.set_pixel(0, 0, 0)
    left = int(left)
    right = int(right)
    left = cap_speed(left)
    right = cap_speed(right)
    run(left, right)

def super_bit():
    mode = 0
    func_list = [
        sonar_run,
        line_follow,
        radio_run,
    ]
    while True:
        run(0, 0)
        display.show(str(mode))
        sleep(1000)
        func = func_list[mode]
        while True:
            if button_a.is_pressed() or button_b.is_pressed():
                break
            func()
        mode = (mode + 1) % len(func_list)

super_bit()
