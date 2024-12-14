from modules import query
from classes import TemperatureSensor
from typing import List

type_temp = ['Tuya', 'DHT22']
temp_sensors = []
for type in type_temp:
    temp_sensors.extend(query.get_sensor_by_type(type))

print(temp_sensors)
