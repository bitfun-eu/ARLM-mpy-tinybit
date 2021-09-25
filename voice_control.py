# Add your Python code here. E.g.
from microbit import pin1, sleep
from tinybit import run

def listen(level=100, duration_ms=1000, speed=70, wait=300):
    noise = pin1.read_analog()
    if noise > level:
        run(speed, speed)
        sleep(duration_ms)
    run(0, 0)
    sleep(wait)

while True:
    listen()

# Questions
# 1. Why do we sleep(wait) at line 11? what could happen if we don't do that?
# 2. Can we use two microphone, such that tinybit can run towards the voice source?
# e.g. if voice comes from left, then it turns left, if voice comes from right, it turns right?
# There is a mic sensor in the hardware pack, please use microbit v1 if your tinybit is not fixed for v2.

# Below is another version which is more sensitive, think about why this is the case?
from microbit import pin1, sleep
from tinybit import run

def listen(level=100, duration_ms=1000, speed=70, wait=300):
    while True:
        noise = pin1.read_analog()
        if noise < level:
            continue
        else:
            run(speed, speed)
            sleep(duration_ms)
        run(0, 0)
        sleep(wait)

listen()
