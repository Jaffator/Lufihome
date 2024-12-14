
from gevent import monkey  # nopep8
monkey.patch_all()  # nopep8
from backend.modules import LoopAlarmEvent, LoopAlarmSireneSound
from web import create_app, SocketIO_events
import time
import RPi.GPIO as GPIO
from flask_restful import Api, Resource
from flask_cors import CORS
from threading import Thread
from flask import jsonify
from backend.modules import LoopAlarmArmBeep

# @werkzeug.serving.run_with_reloader
# def runServer():
#     ws = WSGIServer(("192.168.0.107", 5000), app)
#     ws.serve_forever()
# runServer()


def start_thread3():
    t3 = Thread(target=LoopAlarmSireneSound.alert_beep_thread)
    t3.daemon = True
    t3.start()


def start_thread2():
    t2 = Thread(target=LoopAlarmArmBeep.arming_beep_thread)
    t2.daemon = True
    t2.start()


def start_thread1():
    t1 = Thread(target=LoopAlarmEvent.event_alarm_thread)
    t1.daemon = True
    t1.start()


# if __name__ == '__main__':
app = create_app()


start_thread1()
start_thread2()
start_thread3()
