import query
import time
from cryptography.fernet import Fernet
from typing import List
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/home/jaffator/Home_Security/Flask_Server/Main_App/backend')))
from classes import temperature

def read_temp_thread():
    def init_temp_read():
        with open('backend/modules/cipher.txt', 'r', encoding='utf-8') as file:
            cipher = Fernet(file.read())
        try:
            type_temp = ['Tuya', 'DHT22']
            temp_sensors = []

            # create list of all temp sensors from database
            for type in type_temp:
                temp_sensors.extend(query.get_sensor_by_type(type))

            # read tuya access data from database
            access_id = cipher.decrypt(query.get_Setting('TuyaAccess_id')[0]['Value'].encode("utf-8")).decode()
            access_key = cipher.decrypt(query.get_Setting('TuyaAccess_key')[0]['Value'].encode("utf-8")).decode()
            # set tuya ids's to class atributes
            temperature.TuyaSensor.initialize(access_id, access_key)

            # type hint for list -> list contain instances of temperaturesensor class
            ListTempSensorsObj: List[temperature.TemperatureSensor] = []

            # creating instances of temperaturesensor class
            for sensor in temp_sensors:
                if sensor['Type'] == 'Tuya':
                    tuyaTemp = temperature.TuyaSensor(sensor['DeviceID'], sensor['Name'], sensor['SensorID'])
                    ListTempSensorsObj.append(tuyaTemp)
                if sensor['Type'] == 'DHT22':
                    dhtTemp = temperature.DHT22Sensor(sensor['DigitalPin'], sensor['Name'], sensor['SensorID'])
                    ListTempSensorsObj.append(dhtTemp)
            return ListTempSensorsObj
        
        except Exception as e:
            print(f'error init temp sensor {e}')
    
    tempsensors = init_temp_read()
    def send_temp():
        # send temp via websocket to frontend
        None
    def store_temp_db(sensorID, temp):
        query.write_temp(sensorID, temp)

    def read_temps():
        print()
        tempdata = []
        for sensor in tempsensors:
            try:
                print(f'---{sensor.sensor_name}')
                tempactual = sensor.read_temperature()
                tempdict = {
                    "temp_id": sensor.id,
                    "temp": tempactual,
                    "status": True
                }
                tempdata.append(tempdict)
                print(f'     actual: {tempactual}')
                try:
                    templast = query.get_last_temp(sensor.id)['Temperature']
                except Exception as e:
                    if e.args[0] == 'list index out of range':
                        store_temp_db(sensor.id, tempactual)
                    continue
                print(f'     last: {templast} id: {sensor.id}')

                if abs(tempactual - templast) > 0.2:
                    store_temp_db(sensor.id, tempactual)

            except Exception as e:
                print(e)
                tempdict = {
                    "temp_id": sensor.id,
                    "temp": None,
                    "status": False
                }
                tempdata.append(tempdict)
        return tempdata
    
    while True:
        read_temps()
        time.sleep(10)

read_temp_thread()
    
