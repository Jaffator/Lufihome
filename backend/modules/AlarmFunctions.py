import RPi.GPIO as GPIO
from modules import query
import time
from web import SocketIO_events
from queue import Queue
# global variables
arming = False
alert = False
beep_request_app = False
sensorsGlobal = []
queue = Queue()

# --------------------------------------------- Global functions ---------------------------------------------


def reinit_alarm():
    queue.put('reinit_alarm')


def get_sensors_state():
    GPIO.setmode(GPIO.BCM)
    sensors = query.get_AllSensor()
    for sensor in sensors:
        GPIO.setup(sensor['DigitalPin'], GPIO.IN,pull_up_down=GPIO.PUD_UP)
    for sensor in sensors:
        if GPIO.input(sensor['DigitalPin']) == 1:
            state = False
        else:
            state = True
        sensor['sensorData'] = state
    global sensorsGlobal
    sensorsGlobal = sensors
    return sensors


def start_armin_beeping_from_app(play):
    global arming
    global beep_request_app
    arming = play  # start arming beeping sound
    beep_request_app = play  # flag that request came from app


def broadcast_arming_alarm_from_remote():
    query.set_Setting('AllHouse', True)
    query.set_Setting('AlarmState', 'arming')
    SocketIO_events.broadcast_setting(query.get_allSetting())
    SocketIO_events.broadcast_houseall(True)
    SocketIO_events.broadcast_updatedAreas()


def get_logID(type):
    if type == "alarm":
        lastAlarmID = query.get_default(
            "SELECT * FROM AlarmEventLog ORDER BY AlarmEventID DESC LIMIT 1")[0]["AlarmEventID"]
        return lastAlarmID
    if type == "event":
        lastEventID = query.get_default(
            "SELECT * FROM SensorLog ORDER BY SensorLogID DESC LIMIT 1")[0]["SensorLogID"]
        return lastEventID


def set_unread_msg(logType, alluser=bool):
    users = query.get_allUsers()
    if alluser:
        for user in users:
            query.set_unreadMsg(user['UserName'], logType, get_logID(logType))
    else:
        for user in users:
            if user['AccountType'] == 'admin':
                adminName = user['UserName']
            break
        query.set_unreadMsg(adminName, logType, get_logID(logType))


def secure_all_house():
    areas = query.get_Areas()
    for item in areas:
        query.update_Areas(
            item['AreaID'], item['AreaName'], True, 'secured')
    query.set_Setting('AllHouse', True)
    query.set_Setting('AlarmState', 'armed')
    SocketIO_events.broadcast_setting(query.get_allSetting())
    SocketIO_events.broadcast_houseall(True)
    SocketIO_events.broadcast_updatedAreas()
    print('----- Armed  -----')


def unsecure_all_house():
    global arming
    global alert
    global beep_request_app
    arming = False
    alert = False
    beep_request_app = False
    print('----- remote unsecure all house -----')
    areas = query.get_Areas()
    for item in areas:
        query.update_Areas(
            item['AreaID'], item['AreaName'], False, 'unsecured')
    query.set_Setting('AllHouse', False)
    query.set_Setting('AlarmState', 'disarm')
    SocketIO_events.broadcast_setting(query.get_allSetting())
    SocketIO_events.broadcast_houseall(False)
    SocketIO_events.broadcast_updatedAreas()
    confirmBeep('disarmed')
    print('----- Disarmed  -----')


def confirmBeep(type):  # type = 'armed' or 'disarmer
    sirenPin = sireneOutput()
    GPIO.setup(sirenPin, GPIO.OUT)
    if type == 'armed':
        confirmBeepTime = 1.5
    if type == 'disarmed':
        confirmBeepTime = 1
    while confirmBeepTime > 0:
        GPIO.output(sirenPin, GPIO.LOW)
        time.sleep(0.035)
        GPIO.output(sirenPin, GPIO.HIGH)
        time.sleep(0.2)
        confirmBeepTime -= 0.535


def sireneOutput():
    sirene = query.get_alarm_outputs()
    for item in sirene:
        if item['Name'] == 'siren':
            sirenPin = item['DigitalPin']
            break
    return int(sirenPin)
