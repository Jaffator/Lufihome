
from gevent import monkey  # nopep8
monkey.patch_all()  # nopep8
from web import create_app, SocketIO_events
import time
import RPi.GPIO as GPIO
from flask_restful import Api, Resource
from flask_cors import CORS
import json
from threading import Thread
from flask import jsonify
import werkzeug.serving
from werkzeug.debug import DebuggedApplication
from gevent.pywsgi import WSGIServer
from modules import AlarmEvent, AlarmArminBeep, AlarmSireneSound
from flask_jwt_extended import jwt_required
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies
# @werkzeug.serving.run_with_reloader
# def runServer():
#     ws = WSGIServer(("192.168.0.107", 5000), app)
#     ws.serve_forever()
# runServer()


def start_thread3():
    t3 = Thread(target=AlarmSireneSound.alert_beep_thread)
    t3.daemon = True
    t3.start()


def start_thread2():
    t2 = Thread(target=AlarmArminBeep.arming_beep_thread)
    t2.daemon = True
    t2.start()


def start_thread1():
    t1 = Thread(target=AlarmEvent.event_alarm_thread)
    t1.daemon = True
    t1.start()


# if __name__ == '__main__':
app = create_app()


# @app.after_request
# def refresh_expiring_jwts(response):
#     try:
#         exp_timestamp = get_jwt()["exp"]
#         now = datetime.now(timezone.utc)
#         target_timestamp = datetime.timestamp(now + timedelta(seconds=10))
#         if target_timestamp > exp_timestamp:
#             access_token = create_access_token(identity=get_jwt_identity())
#             set_access_cookies(response, access_token)
#             print("--token refresh")
#         return response
#     except (RuntimeError, KeyError):
#         print("--token expire")
#         # Case where there is not a valid JWT. Just return the original response
#         return response


start_thread1()
start_thread2()
start_thread3()


# def my_callback(channel):
#     global prev_inp
#     global count

#     inp = GPIO.input(6)
#     if ((not prev_inp) and inp):
#         count = count + 1
#         print("Rising edge detected")
#     else:
#         print("Falling edge detected")
#     prev_inp = inp
#     time.sleep(0.6)


#     print(channel)
#     if GPIO.input(6):     # if port 25 == 1
#         print("Rising edge detected on 25")
#     else:                  # if port 25 != 1
#         print("Falling edge detected on 25")


#         print("true")
#         SocketIO_events.testSend(True)
#         time.sleep(2)
#         print("false")
#         SocketIO_events.testSend(False)
#     print("as")
#     cas = time.strftime("%H:%M:%S", t)
#     temperature_c = dhtDevice.temperature
#     temperature_f = temperature_c * (9 / 5) + 32
#     humidity = dhtDevice.humidity

#     temp = "Temp: {:.1f} C    Humidity: {}%  Time: {}".format(
#         temperature_c, humidity, cas)
#     print(temp)
# for x in AlarmSpace.alarm.get_PINS_to_secure():
#     if GPIO.event_detected(x):
#         if GPIO.input(x):
#             print(f"rise {x} and value {GPIO.input(x)}")


# def core3():
#     while True:
#         time.sleep(3)
# SocketIO_events.refresh_clients()
# print(f"Raise detect on pin {6}")
#  and GPIO.input(6) == GPIO.LOW
#   if len(pins):
#   try:
#         for item in pins:
#             if GPIO.event_detected(item) and GPIO.input(item) == GPIO.LOW:
#                 print(f"Raise detect on pin {item}")
#     except:
#         print("error")
# else:
#     time.sleep(1)
#     print("empty")

# test.share.getvalue()
# AlarmSpace.alarm.get_PINS_to_secure()
# else:
#     if var == key.SPACE:
#         test.share.setvalue()
# AlarmSpace.alarm.set_PINS_to_secure()
#     print(GPIO.input(digital_pin))
# try:
#     # Print the values to the serial
#     t = time.localtime()
# cas = time.strftime("%H:%M:%S", t)
# temperature_c = dhtDevice.temperature
# temperature_f = temperature_c * (9 / 5) + 32
# humidity = dhtDevice.humidity

# temp = "Temp: {:.1f} C    Humidity: {}%  Time: {}".format(
#     temperature_c, humidity, cas)
# print(temp)
#     with open('Temp.txt', 'a') as f:
#         f.write(temp + '\n')

# except RuntimeError as error:
#     # Errors happen fairly often, DHT's are hard to read, just keep going
#     # print(error.args[0])
#     time.sleep(10.0)
#     continue
# except Exception as error:
#     dhtDevice.exit()
#     raise error
# print(alarm.get_PINS_to_secure())


# -------------------------------- For later use with multiple loops--------------------------------
