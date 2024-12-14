import time
from tuya_connector import (
    TuyaOpenAPI,
    TuyaOpenPulsar,
    TuyaCloudPulsarTopic,
)
import dht11
import RPi.GPIO as GPIO
from abc import ABC, abstractmethod

class SensorError(Exception):
    """Vlastní výjimka pro chyby při čtení ze senzoru."""

    def __init__(self, message, error_code=None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code  # Můžeš přidat kód chyby, pokud je potřeba

    def __str__(self):
        return f"{self.message} (Error code: {self.error_code})" if self.error_code else self.message

# Base Class


class TemperatureSensor(ABC):
    def __init__(self, name, id):
        self.sensor_name = name
        self.id = id
    
    @abstractmethod
    def read_temperature(self):
        raise NotImplementedError("Subclasses must implement this method.")

# DHT22 Temp Sensor Class
class DHT22Sensor(TemperatureSensor):
    def __init__(self, pin: int, name: str, id: int):
        super().__init__(name, id)
        self.pin = pin
        self.sensor = dht11.DHT11(pin)

    def read_temperature(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)
        count = 0
        while True:
            temp = self.sensor.read()
            time.sleep(0.1)
            if temp.is_valid() and temp.temperature != 0:
                return temp.temperature
            else:
                # temp read error, try again
                count += 1
            if count >= 15:
                # print(f"Error reading DHT22 temp: {self.sensor_name}")
                raise SensorError(f"DHT22 read error {self.sensor_name}")


# Tuya Temp Sensor Class
class TuyaSensor(TemperatureSensor):
    tuya_access_id = None
    tuya_access_key = None

    # Statická metoda naznačuje, že není závislá na konkrétní instanci ani na třídě.
    # Pomocné funkce, které souvisejí s třídou, ale nepotřebují přístup k jejím atributům.
    @staticmethod
    def initialize(tuya_access_id: str, tuya_access_key: str):
        TuyaSensor.tuya_access_id = tuya_access_id
        TuyaSensor.tuya_access_key = tuya_access_key

    def __init__(self, tuya_device_id: str, name: str, id: int):
        super().__init__(name, id)
        self.device_id = tuya_device_id
        self.api_endpoint = "https://openapi.tuyaeu.com"

    def read_temperature(self):
        try:
            openapi = TuyaOpenAPI(
                self.api_endpoint,  self.tuya_access_id, self.tuya_access_key)
            openapi.connect()
            response = openapi.get(f"/v1.0/devices/{self.device_id}/status")
            temp = int(response["result"][0]["value"]) / 10
            humi = int(response["result"][1]["value"]) / 10
            # humitemp = {'temp': temp, 'humi': humi}
            return temp
        except Exception as e:
            # print(f"Error reading Tuya temp: {self.sensor_name}")
            raise SensorError(f"Tuya read error {self.sensor_name}")
