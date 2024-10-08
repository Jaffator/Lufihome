from modules import query, Notification
import time
from copy import copy, deepcopy
import RPi.GPIO as GPIO
import dht11
from werkzeug.security import generate_password_hash, check_password_hash

# query.set_Alert_Log(17)

# res = query.get_default(
#     "SELECT * FROM AlarmEventLog ORDER BY AlarmEventID DESC LIMIT 1")[0]["AlarmEventID"]
# print(res)

# res1 = query.get_allUsers()
# for user in res1:
#     print(user['UserName'])
# query.set_unreadMsg("j", "alarm", 12)
# dates = query.get_unreadMsg_dates("j", "alarm")
# dateslist = []
# for date in dates:
#     print(date["TimeStamp"])
#     dateslist.append(date["TimeStamp"])

# oldest = min(dateslist)
# latest = max(dateslist)
# print(f"oldest{oldest} latest {latest}")

# print(query.get_AlarmLog())
# def trydb():
#     try:
#         query.set_newUser('ahoj', 'jasda', 'jasda', 'a',
#                           'yes', 'user')
#     except Exception as e:
#         print(e)
#         return 'error'
#     return 'ok'


# print(trydb())

# print(query.get_Outputs('gate')[0]['DigitalPin'])


# GPIO.setmode(GPIO.BCM)
# GPIO.cleanup()
# sensor1 = dht11.DHT11(18)


# while True:

#     temp1 = sensor1.read()
#     time.sleep(5)
#     if temp1.is_valid():
#         print("Temperature 2: %-3.1f C" % temp1.temperature)
#         print(temp1.humidity)
#     else:
#         print("Error 2: %d" % temp1.error_code)
import Adafruit_DHT

# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
sensor = Adafruit_DHT.DHT22


pin = '18'

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)


if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
else:
    print('Failed to get reading. Try again!')

# from werkzeug.security import generate_password_hash, check_password_hash

# areas = query.get_Areas()
# areadef = query.get_AreaDefiniton()
# sensors = query.get_AllSensor()
# resultAreaDef = {'areadef1': {'SensorID': 10, 'list': [
#     'ahoj', 'cau']}, 'areadef2': {'SensorID': 5, 'list': ['ds', 'fdfd']}}
# for item in sensors:
#     item.pop("Type")
#     item.pop("DigitalPin")
#     item["use"] = False

# for a in areas:
#     resultAreaDef[] = {}
#     resultAreaDef['AreaID'] = a["AreaID"]

# a["AreaID"]
# for a in areas:
#     for sen in sensors:
#         sen['use'] = False
#     for area in areadef:
#         if area['AreaID'] == a['AreaID']:
#             for sensor in sensors:
#                 if sensor['SensorID'] == area['SensorID']:
#                     sensor['use'] = True
#     resultAreaDef[a['AreaID']] = deepcopy(sensors)

# query.update_test('777', '145')
# query.delete_AreaDef(5)
