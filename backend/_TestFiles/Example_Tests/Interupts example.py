# import time
# import RPi.GPIO as GPIO


# BUTTON_GPIO = 27
# BUTTON_GPIO = 17


# if __name__ == '__main__':
#     GPIO.setwarnings(False)
#     GPIO.setmode(GPIO.BCM)
#     GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#     GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#     while True:
#         # button is pressed when pin is LOW
#         if not GPIO.input(17):
#             print("Button pressed 17!")
#             pressed = True
#         if not GPIO.input(27):
#             print("Button pressed 27!")
#             pressed = True
#         # button not pressed (or released)

#         time.sleep(0.1)

import signal
import sys
import RPi.GPIO as GPIO
okruhy = {}
okruhy["garaz"] = [17, 5]
okruhy["patro"] = [27, 13]


def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)


def button_pressed_callback(d):
    print("Button pressed " + str(d))


if __name__ == '__main__':

    GPIO.setmode(GPIO.BCM)
    for i in okruhy.get("patro"):
        GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    for i in okruhy.get("patro"):
        GPIO.add_event_detect(i, GPIO.FALLING,
                              callback=button_pressed_callback, bouncetime=100)

    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()
