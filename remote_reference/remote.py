from microbit import *
import radio

radio.on()
radio.config(power=7, channel=0, address=0, group=0, data_rate=radio.RATE_250KBIT)

while True:
    if button_a.is_pressed() and button_b.is_pressed():
        display.show("T")
        radio.send("-100 100")
    elif button_a.is_pressed():
        display.show("F")
        radio.send("100 100")
    elif button_b.is_pressed():
        display.show("B")
        radio.send("-100 -100")
    else:
        display.show("S")
        radio.send("0 0")
    sleep(10)
