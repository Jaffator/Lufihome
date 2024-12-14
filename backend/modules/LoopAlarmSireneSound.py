import RPi.GPIO as GPIO
from modules import query, AlarmFunctions
import time


def alert_beep_thread():
    def alert_sirene():  # Full sirene sound - alarm Alert
        sirenPin = AlarmFunctions.sireneOutput()
        alerttime = int(query.get_Setting('AlertTime')[0]['Value'])
        GPIO.setup(sirenPin, GPIO.OUT)
        while alerttime > 0:
            if AlarmFunctions.alert:
                time.sleep(1)
                GPIO.output(sirenPin, GPIO.LOW)
                print(f'sirene...{alerttime}')
                alerttime -= 1.535
            else:
                GPIO.output(sirenPin, GPIO.HIGH)
                break
        AlarmFunctions.alert = False
        GPIO.output(sirenPin, GPIO.HIGH)

    while True:
        time.sleep(0.02)
        if AlarmFunctions.alert:
            alert_sirene()
