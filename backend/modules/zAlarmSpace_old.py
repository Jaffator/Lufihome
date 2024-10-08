import RPi.GPIO as GPIO
from modules import query
import time
from web import SocketIO_events
from threading import Thread
import random
from queue import Queue

# global variables
arming = False
alert = False
beep_request_app = False
GPIO.setwarnings(False)

# def init_Alarm():
#     t1 = Thread(target=event_alarm_thread)
#     t2 = Thread(target=arming_beep_thread)
#     t3 = Thread(target=alert_beep_thread)
#     t1.start()
#     t2.start()
#     t3.start()

# --------------------------------------------- Global functions ---------------------------------------------


def start_armin_beeping_from_app(play):
    global arming
    global beep_request_app
    arming = play  # start arming beeping sound
    beep_request_app = play  # flag that request came from app


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
    arming = False
    print('----- remote unsecure all house -----')
    confirmBeep('disarmed')
    areas = query.get_Areas()
    for item in areas:
        query.update_Areas(
            item['AreaID'], item['AreaName'], False, 'unsecured')
    query.set_Setting('AllHouse', False)
    query.set_Setting('AlarmState', 'disarm')
    SocketIO_events.broadcast_setting(query.get_allSetting())
    SocketIO_events.broadcast_houseall(False)
    SocketIO_events.broadcast_updatedAreas()
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

# --------------------------------------------- Threads ---------------------------------------------


def alert_beep_thread():
    None
    # global alert

    # def alert_sirene():  # Full sirene sound - alarm Alert
    #     global arming
    #     sirenPin = sireneOutput()
    #     armtime = int(query.get_Setting('ArmTime')[0]['Value'])
    #     GPIO.setup(sirenPin, GPIO.OUT)
    #     while armtime > 0:
    #         if arming:
    #             armingStop = False
    #             GPIO.output(sirenPin, GPIO.LOW)
    #             time.sleep(0.035)
    #             GPIO.output(sirenPin, GPIO.HIGH)
    #             time.sleep(1.5)
    #             print(f'arming...{armtime}')
    #             armtime -= 1.535
    #         else:
    #             armingStop = True
    #             break
    #     arming = False
    #     if armingStop == False:
    #         secure_all_house()

    # while True:
    #     if alert:
    #         alert_sirene()


def arming_beep_thread():
    global arming
    global beep_request_app

    def armin_beeping():  # short beep sound that indicates arming
        global arming
        sirenPin = sireneOutput()
        armtime = int(query.get_Setting('ArmTime')[0]['Value'])
        GPIO.setup(sirenPin, GPIO.OUT)
        while armtime > 0:
            if arming:
                armingStop = False
                GPIO.output(sirenPin, GPIO.LOW)
                time.sleep(0.035)
                GPIO.output(sirenPin, GPIO.HIGH)
                time.sleep(1.5)
                print(f'arming...{armtime}')
                armtime -= 1.535
            else:
                armingStop = True
                break
        arming = False
        if armingStop == False:
            if beep_request_app == False:
                # secure all house becouse request came from remote key
                secure_all_house()
            else:
                # do nothing beacouse request came from app
                beep_request_app == False

    while True:
        if arming:
            armin_beeping()


def event_alarm_thread():
    global arming

    def alert():
        sirenPin = sireneOutput()
        GPIO.setup(sirenPin, GPIO.OUT)
        GPIO.output(sirenPin, GPIO.LOW)
        siren_countdown = query.get_Setting('Siren countdown')[0]['Value']
        while siren_countdown > 0:
            time.sleep(0.5)
            siren_countdown -= 0.5
            print('--- sirene on ---', siren_countdown)

    def start_securing_all_house():
        global arming
        print('----- Remote pressed: Start arming  -----')
        # check if house is alread secured
        allsecured = bool
        areas = query.get_Areas()
        for item in areas:
            if item['Status'] == 'secured':
                allsecured = True
            else:
                allsecured = False
        if allsecured == False:
            arming = True
        else:
            arming = False
            confirmBeep('armed')

    def sensor_event_callback(channel):
        if GPIO.input(channel) == False:
            sensorID = query.get_sensorID_by_pin(channel)['SensorID']
            # check if it's remote alarm control button
            if query.get_sensor_type_by_pin(channel) == 'remote alarm ON':
                start_securing_all_house()
            if query.get_sensor_type_by_pin(channel) == 'remote alarm OFF':
                unsecure_all_house()
            # check if it's alarm sensor
            for areaDef in query.get_AreaDefiniton():
                if areaDef['SensorID'] == sensorID:
                    if query.get_AreaStatus_byID(areaDef['AreaID'])[0][0] == 'secured':
                        query.set_Actual_areaStatus(areaDef['AreaID'], 'alert')
                        SocketIO_events.broadcast_updatedAreas()
                        alert()
                        break

    #  Initializing Alarm
    print('---------- Initializing Alarm ----------')
    GPIO.cleanup()
    GPIOpins_sensors = query.get_AllSensorsGPIOpin()
    GPIO.setmode(GPIO.BCM)
    for sensor in GPIOpins_sensors:
        GPIO.setup(sensor['DigitalPin'], GPIO.IN,
                   pull_up_down=GPIO.PUD_UP)
    for sensor in GPIOpins_sensors:
        GPIO.add_event_detect(
            sensor['DigitalPin'], GPIO.BOTH, callback=sensor_event_callback, bouncetime=200)
    print('---------- Alarm successfully initialized ----------')
