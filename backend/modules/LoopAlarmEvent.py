import RPi.GPIO as GPIO
from modules import query, AlarmFunctions, Notification, GarageGate
from web import SocketIO_events
import time
from queue import Queue
from datetime import datetime

GPIO.setwarnings(False)


def event_alarm_thread():

    def start_securing_all_house():
        # check if house is alread secured
        allsecured = bool
        areas = query.get_Areas()
        for item in areas:
            if item['Status'] == 'secured':
                allsecured = True
            else:
                allsecured = False
        if allsecured == False:
            print('----- Remote pressed: Start arming  -----')
            AlarmFunctions.broadcast_arming_alarm_from_remote()
            AlarmFunctions.arming = True
        else:
            print('----- Already secured  -----')
            AlarmFunctions.arming = False
            AlarmFunctions.confirmBeep('armed')

    def __alert(sensorPin, areaID):
        AlarmFunctions.alert = True
        areaName = query.get_AreaName_byID(areaID)[0]['AreaName']
        sensorName = query.get_sensor_name_by_pin(sensorPin)
        Notification.send_notification(
            'all', Notification.alert, f'Area: {areaName} \nSensor: {sensorName} \n{time.ctime()}')
        query.set_Actual_areaStatus(areaID, 'alert')
        query.set_Alert_Log(sensorPin)
        AlarmFunctions.set_unread_msg('alarm', True)
        SocketIO_events.broadcast_updatedAlarmEvent()
        SocketIO_events.broadcast_updatedAreas()

    def sensor_event_callback(channel):
        GarageGate.gateCheckStatus(channel)
        # ----------------- read and broadcast sensors state -----------------
        date = datetime.now().strftime(" % H: % M: % S")
        print(f"----------{channel,date}----------")
        sensors = AlarmFunctions.sensorsGlobal
        for sensor in sensors:
            if sensor['DigitalPin'] == channel:
                if sensor['Type'] == 'pir' or 'remote alarm ON' or 'remote alarm OFF':
                    sensor['sensorData'] = not GPIO.input(channel)
                if sensor['Type'] == 'magnet':
                    sensor['sensorData'] = GPIO.input(channel)
        AlarmFunctions.sensorsGlobal = sensors
        SocketIO_events.broadcast_sensorState(sensors)

        # ---------------------------------- check if it's alarm event ----------------------------------
        # ----------------- check MAGNET sensors -----------------
        if (GPIO.input(channel) == True) and (query.get_sensor_type_by_pin(channel) == 'magnet'):
            sensorID = query.get_sensorID_by_pin(channel)['SensorID']
            # check if it's alarm sensor
            for areaDef in query.get_AreaDefiniton():
                if areaDef['SensorID'] == sensorID:
                    # if area with event sensor secured that raise ALARM
                    if query.get_AreaStatus_byID(areaDef['AreaID'])[0][0] == 'secured':
                        # trigger alarm
                        __alert(channel, areaDef['AreaID'])
                        break

        # ----------------- check PIR sensors -----------------
        if (GPIO.input(channel) == False) and (query.get_sensor_type_by_pin(channel) == 'pir' or 'remote alarm ON' or 'remote alarm OFF'):
            sensorID = query.get_sensorID_by_pin(channel)['SensorID']
            # check if it's remote alarm control button
            if query.get_sensor_type_by_pin(channel) == 'remote alarm ON':
                start_securing_all_house()
            if query.get_sensor_type_by_pin(channel) == 'remote alarm OFF':
                AlarmFunctions.unsecure_all_house()
            # check if it's alarm sensor
            for areaDef in query.get_AreaDefiniton():
                if areaDef['SensorID'] == sensorID:
                    # if area with event sensor secured that raise ALARM
                    if query.get_AreaStatus_byID(areaDef['AreaID'])[0][0] == 'secured':
                        # trigger alarm
                        __alert(channel, areaDef['AreaID'])
                        break

    def init_Alarm():
        AlarmFunctions.get_sensors_state()
        AlarmFunctions.alert = False
        AlarmFunctions.arming = False
        print('---------- Initializing Alarm ----------')
        GPIO.cleanup()
        GPIOpins_sensors = query.get_AllSensorsGPIOpin()
        GPIO.setmode(GPIO.BCM)
        print(GPIOpins_sensors)
        for sensor in GPIOpins_sensors:
            GPIO.setup(sensor['DigitalPin'], GPIO.IN,
                       pull_up_down=GPIO.PUD_UP)
        for sensor in GPIOpins_sensors:
            GPIO.add_event_detect(
                sensor['DigitalPin'], GPIO.BOTH, callback=sensor_event_callback, bouncetime=200)
        print('---------- Alarm successfully initialized ----------')

    init_Alarm()

    while True:
        message = AlarmFunctions.queue.get()
        if message == 'reinit_alarm':
            init_Alarm()
