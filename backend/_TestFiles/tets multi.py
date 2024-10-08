import threading
import time


class AlarmManager:
    def __init__(self):
        self.alarm_thread = None
        self.running = False

    def alarm(self):
        if not self.running:
            self.alarm_thread = threading.Thread(target=self._ring_alarm)
            self.alarm_thread.start()

    def _ring_alarm(self):
        self.running = True
        time_end = time.time() + 5
        while time.time() < time_end:
            time.sleep(1)
            print("ALARM: Beep!")
        print("ALARM: Alarm stopped ringing.")
        self.running = False


if __name__ == "__main__":
    alarm_manager = AlarmManager()
    i = 0
    while True:
        time.sleep(0.5)
        print("this is main")
        i = i + 1
        if i == 5:
            alarm_manager.alarm()
