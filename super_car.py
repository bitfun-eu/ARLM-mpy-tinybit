# Add your Python code here. E.g.
from microbit import *
from tinybit import *
from random import randint

def sleep_run():
    pass

def sonar_run(speed=80):
    d = measure()
    if d < 30:
        run(-speed, -speed)
    elif d > 50:
        run(speed, speed)
    else:
        run(0, 0)

def line_run(speed=90):
    pass

def radio_run():
    pass

def check():
    d = measure()
    if d < 30:
        run(0, 0)
        music.stop()
        sleep(1000)

def party_run():
    #display.scroll("Partymodus") # Aufgabe 1
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


# button_a: next mode, button_b: sleep mode
def super_run():
    run_list = [sleep_run, sonar_run, line_run, radio_run, party_run]
    mode = 0
    while True:
        display.show(mode)
        run(0, 0)
        music.stop()
        light(0, 0, 0, 0)
        light(1, 0, 0, 0)
        func = run_list[mode]
        while True:
            func()
            if button_a.is_pressed():
                mode = mode + 1
                mode = mode % len(run_list)
                sleep(1000)
                break # exit the current loop: inner loop --> return to outer loop
            if button_b.is_pressed():
                mode = 0
                break

super_run()
