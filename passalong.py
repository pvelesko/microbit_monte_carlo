from microbit import *
import radio

uart.init(baudrate=115200)
display.show(Image.HAPPY)
sleep(2000)
radio.on()

while True:
    message = radio.receive_full()

    if message != None:
        display.show(Image.HEART)
        display.show(Image.HAPPY)
        print(message[0])