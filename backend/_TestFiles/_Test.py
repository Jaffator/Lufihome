
import time
import dht11

from cryptography.fernet import Fernet
from RPi import GPIO
from tuya_connector import (
    TuyaOpenAPI,
    TuyaOpenPulsar,
    TuyaCloudPulsarTopic,
)
# Generování šifrovacího klíče (uložte ho na bezpečné místo)
# key = Fernet.generate_key()
# cipher = Fernet('u7spEnQ4gwifMomLUFauAXs95mSIccU9DueNX1azKbc=')
# # print(key)
# # Šifrování dat
# # accessid = "yjvwmvtux9y9fkudcc5u"
# # accessid = cipher.encrypt(accessid.encode())
# # accesskey = "8d99f154e80a46129652843c448bbea7"
# # accesskey = cipher.encrypt(accesskey.encode())
# # print(accesskey)
# # query.set_Setting('TuyaAccess_id', accessid)
# # query.set_Setting('TuyaAccess_key', accesskey)

# id = query.get_Setting('TuyaAccess_id')[0]['Value']
# id = id.encode("utf-8")
# key = query.get_Setting('TuyaAccess_key')[0]['Value']
# key = key.encode("utf-8")

# decrypted_data_id = cipher.decrypt(id).decode()
# decrypted_data_key = cipher.decrypt(key).decode()

# print(decrypted_data_id)
# print(decrypted_data_key)


# # Dešifrování dat

# # from classes import TemperatureSensor

# dht22 = TemperatureSensor.DHT22Sensor(24)
# dht22.read_temperature
# tuya = TemperatureSensor.TuyaSensor(
#     "yjvwmvtux9y9fkudcc5u", "8d99f154e80a46129652843c448bbea7", "bf441813fba99f8d51uyts")
# try:
#     print(tuya.read_temperature()['temp'])
# except TemperatureSensor.SensorError as e:
#     print(e)


# set_Setting

# passw = generate_password_hash(request.json['NewPass'])
# 1. Zadej své API klíče a endpoint
# ACCESS_ID = "yjvwmvtux9y9fkudcc5u"
# ACCESS_KEY = "8d99f154e80a46129652843c448bbea7"
# API_ENDPOINT = "https://openapi.tuyaeu.com"  # Pro Evropu (změň dle regionu)


# # 2. Inicializace Tuya OpenAPI
# openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
# openapi.connect()

# # 4. Čtení stavu konkrétního zařízení
# DEVICE_ID = "bf441813fba99f8d51uyts"  # Nahraď ID zařízení ze seznamu
# response = openapi.get(f"/v1.0/devices/{DEVICE_ID}/status")
# temp = int(response["result"][0]["value"]) / 10
# print(temp)
# humi = int(response["result"][1]["value"]) / 10
# print(humi)

# from tuya_iot import TuyaOpenAPI


# ACCESS_ID = "yjvwmvtux9y9fkudcc5u"
# ACCESS_KEY = "8d99f154e80a46129652843c448bbea7"
# API_ENDPOINT = "https://openapi.tuyaeu.com"
# USERNAME = "jardalufi@gmail.com"
# PASSWORD = "Tanvald2664"

# openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
# response = openapi.connect(USERNAME, PASSWORD)
# print(response)  # Mělo by vrátit token

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.IN)  # set a port/pin as an input
sensor1 = dht11.DHT11(22 )  # obyvak
# # sensor2 = dht11.DHT11(23)  # jidelna
# # # sensor3 = dht11.DHT11(23)  # predsín
# # # sensor4 = dht11.DHT11(27)  # dilna
# # # # sensor5 = dht11.DHT11(26)  # chodba do garaze
# # # sensor6 = dht11.DHT11(22)  # garaz

while True:

    temp = sensor1.read()
    time.sleep(0.5)

    if temp.is_valid:
        print("Temp: %-3.1f C" % temp.temperature)
        print("Humi: %-3.1f C" % temp.humidity)
    else:
        print("Error 2: %d" % temp.error_code)

# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
# sensor = Adafruit_DHT.DHT22


# humidity, temperature = Adafruit_DHT.read_retry(sensor, 25)


# if humidity is not None and temperature is not None:
#     print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
# else:
#     print('Failed to get reading. Try again!')
