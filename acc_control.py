from microbit import accelerometer as acc
from microbit import display, Image, button_a, button_b
from tinybit import run
import radio
radio.on()

def send():
    display.show(Image.HEART)
    speed = acc.get_y()
    speed = -speed
    speed = speed // 4
    s = str(speed)
    b = bytes(s, 'utf-8')
    radio.send(b)

def receive():
    display.show(Image.SMILE)
    try:
        b = radio.receive()
        s = str(b, 'utf-8')
        n = int(s)
    except:
        run(0, 0)
        return
    run(n, n)

MODE = 0 # 0: send, 1: receive

while True:
    if button_a.was_pressed():
        MODE = 0
    if button_b.was_pressed():
        MODE = 1
    if MODE == 0:
        send()
    else:
        receive()
