from microbit import *
from tinybit import *
import radio
from random import randint

FIND_LINE = False
#radio.config(power=7, channel=0, address=0, group=0, data_rate=radio.RATE_250KBIT)
radio.on()

def cap_speed(n):
    if n < -255: return -255
    elif n > 255: return 255
    else: return n

def sleep_run():
    global FIND_LINE
    FIND_LINE = False
    music.stop()
    run(0, 0)
    light(0, 0, 0, 0)
    light(1, 0, 0, 0)

def sonar_run(speed=80):
    d = measure()
    light(0, 0, 0, 0)
    light(1, 0, 0, 0)
    if d < 30:
        light(1, 100, 0, 0)
        run(-speed, -speed)
    elif d > 50:
        light(0, 50, 50, 50)
        run(speed, speed)
    else:
        light(0, 100, 0, 0)
        run(0, 0)

def line_run(speed=60, delta=60):
    global FIND_LINE
    left, right = line()
    if FIND_LINE == True:
        light(0, 30, 30, 30)
        light(1, 0, 0, 0)
        if left == 1 and right == 1:
           light(0, 30, 0, 0)
           run(speed,-speed)
        elif left == 1 and right == 0:
            light(0, 0, 30, 0)
            run(speed-delta,speed)
        elif left == 0 and right == 1:
            light(0, 0, 0, 30)
            run(speed,speed-delta)
        elif left == 0 and right == 0:
            a = randint(0, 50)
            b = randint(0, 50)
            c = randint(0, 50)
            light(1, a, b, c)
            light(0, c, a, b)
            run(speed, speed)
    else:
        light(0, 50, 0, 0) # searching for line
        run(speed, speed)
        if left == 1 or right == 1:
            FIND_LINE = True

V = 0
def radio_run():
    global V
    try:
        data = radio.receive()
        left, right = data.split()
    except:
        return
    display.set_pixel(4, 4, V)
    if V: V = 0
    else: V = 9
    left = int(left)
    right = int(right)
    left = cap_speed(left)
    right = cap_speed(right)
    run(left, right)

def check():
    d = measure()
    if d < 30:
        run(0, 0)
        music.stop()
        sleep(1000)

def party_run():
    max_num = 50
    check()
    music.play(music.PYTHON, wait=False)
    r = randint(0, max_num)
    g = randint(0, max_num)
    b = randint(0, max_num)
    light(0, r, g, b)
    r = randint(0, max_num)
    g = randint(0, max_num)
    b = randint(0, max_num)
    light(1, r, g, b)

    left = randint(-255, 255)
    right = randint(-255, 255)
    run(left,right)
    sleep(1000)

def remote_loop(xpin=pin1, ypin=pin2, period=100):
    v = 9
    while True:
        x = xpin.read_analog()
        y = ypin.read_analog()
        speed = (y - 512) >> 1 # [0, 1024] -> [-512, 512] -> [-255, 255]
        delta = (x - 512) >> 2 # [0, 1024] -> [-512, 512] -> [-128, 128]
        left = cap_speed(speed + delta)
        right = cap_speed(speed - delta)
        s = str(left) + ' ' + str(right)
        radio.send(s)
        print(s)
        display.set_pixel(4, 4, v)
        if v: v = 0
        else: v = 9
        sleep(period)

# button_a: next mode, button_b: sleep mode
def super_run():
    # dual mode
    try:
        run(0,0)
    except OSError: # I2C error ...
        display.show(Image.HEART)
        remote_loop()
        display.show(Image.SAD)
        return
    run_list = [sleep_run, sonar_run, line_run, radio_run, party_run]
    mode = 0
    while True:
        display.show(mode)
        sleep_run()
        func = run_list[mode]
        while True:
            func()
            if button_a.is_pressed():# or (pin1.read_analog() > 200):
                mode = mode + 1
                mode = mode % len(run_list)
                sleep(500)
                break # exit the current loop: inner loop --> return to outer loop
            if button_b.is_pressed():
                mode = 0
                break

super_run()
