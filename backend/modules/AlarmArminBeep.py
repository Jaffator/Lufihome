import RPi.GPIO as GPIO
from modules import query, AlarmFunctions
import time


def arming_beep_thread():
    def armin_beeping():  # short beep sound that indicates arming
        sirenPin = AlarmFunctions.sireneOutput()
        armingTime = int(query.get_Setting('ArmTime')[0]['Value'])
        GPIO.setup(sirenPin, GPIO.OUT)
        while armingTime > 0:
            if AlarmFunctions.arming:
                armingStop = False
                GPIO.output(sirenPin, GPIO.LOW)
                time.sleep(0.035)
                GPIO.output(sirenPin, GPIO.HIGH)
                time.sleep(1.5)
                print(f'arming...{armingTime}')
                armingTime -= 1.535
            else:
                armingStop = True
                break
        # print(f'var {AlarmFunctions.beep_request_app}')
        AlarmFunctions.arming = False

        if armingStop == False:
            if AlarmFunctions.beep_request_app == False:
                print('secure all house becouse request came from remote key')
                AlarmFunctions.secure_all_house()

            else:
                print('do nothing beacouse request came from app')
                AlarmFunctions.beep_request_app = False
    while True:
        time.sleep(0.01)
        if AlarmFunctions.arming:
            armin_beeping()
