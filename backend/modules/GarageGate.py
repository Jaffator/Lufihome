import RPi.GPIO as GPIO
import time
from modules import query
from web import SocketIO_events


def apply_gate_switch():
    pin = query.get_Outputs('gate')[0]['DigitalPin']
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(1)
    GPIO.output(pin, GPIO.HIGH)


def gateCheckStatus(channel):
    channelID = int(query.get_sensorID_by_pin(channel)['SensorID'])
    gateUpID = int(query.get_Setting('GateSensorUp')[0]['Value'])
    gateDownID = int(query.get_Setting('GateSensorDown')[0]['Value'])
    if channelID == gateUpID:
        if GPIO.input(channel) == True:  # magnet is moved away from upper sensor
            gateState = 'Closing'
        if GPIO.input(channel) == False:  # magnet is on upper sensor
            gateState = 'Open'
        query.set_Setting('GateState', gateState)
        SocketIO_events.broadcast_gateState(gateState)
    if channelID == gateDownID:
        if GPIO.input(channel) == True:  # magnet is moved away from down sensor
            gateState = 'Opening'
        if GPIO.input(channel) == False:  # magnet is on down sensor
            gateState = 'Close'
        query.set_Setting('GateState', gateState)
        SocketIO_events.broadcast_gateState(gateState)
