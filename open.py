import time
import board
import digitalio

button = digitalio.DigitalInOut(board.D20)
button.direction = digitalio.Direction.OUTPUT

time.sleep(5)

button.value = True
time.sleep(0.1)
button.value = False

