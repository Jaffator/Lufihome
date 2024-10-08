import i2c_lcd
import RPi.GPIO as GPIO
from requests import session
import time
from curses import keyname
import pcf8574
import _thread
from flask import Flask, render_template, redirect, url_for, request, jsonify, session
from flask_socketio import SocketIO, send, emit
import mariadb
import sys
from classes import AlarmSpace


# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="jaffa",
        password="tanvald222",
        host="localhost",
        port=3306,
        database="homedb"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()
value = "asdasd"
query = f"INSERT INTO Areas (AreaName) VALUES ('{value}')"
cur.execute(query)
conn.commit()

# cur.execute(
#     "SELECT `Name` FROM `Sensors` WHERE SensorID IN(SELECT `SensorID` FROM `DefAreas` WHERE AreaID = (SELECT `AreaID` FROM `Areas` WHERE AreaName = 'patro'))")
# vysledek = cur.fetchone()[0]
# print(vysledek)
# autopep8: off



# autopep8: on

alarm = AlarmSpace.AlarmSpace()  # Initialize alarm from INI file
lcd = i2c_lcd.lcd()
keypad = pcf8574.PCF8574(1, 0x20)
keys = [["A", "3", "2", "1"],
        ["B", "6", "5", "4"],
        ["C", "9", "8", "7"],
        ["D", "#", "0", "*"]]

Areas = {
    "bla1": {
        "secured": True,
        "status": "Ok"
    },
    "bla2": {
        "secured": False,
        "status": "Ok"
    },
    "bla3": {
        "secured": True,
        "status": "Ok"
    }
}
# Areas["bla1"]["status"] = "hovno"
# print(alarm.print_areas())
# alarm.set_areas(False)
# print(alarm.print_areas())


class My_variable():
    def __init__(self) -> None:
        self.data = 0

    def set_data(self, arg):
        self.data = arg

    def get_data(self):
        return self.data


lock = _thread.allocate_lock()
data = My_variable()


def show_areas(start_index=0):
    global lock
    time.sleep(2.2)
    line = 1
    empty_string = "          "  # for clear row after long name
    for item in alarm.get_all_areas()[start_index:start_index+4]:
        # Name of area from keypad (A1,A2...)
        lock.acquire()
        lcd.lcd_display_string_pos("A" + str(line + start_index), line, 0)
        lcd.lcd_display_string_pos(str(item).upper(), line, 3)
        lcd.lcd_display_string_pos(
            empty_string[0:(10 - len(str(item)))], line, len(str(item))+3)
        lock.release()
        line += 1
    if len(alarm.get_all_areas()) > 4 and start_index < (len(alarm.get_all_areas()) - 4):
        # recursive call if number of areas is more that 4 (lcd has 4 rows)
        return show_areas(start_index+1)


def row_off():
    # Natavení čtení řádků klavesnice do default hodnoty
    for i in range(4, 8):
        keypad.set_output(i, True)


def coll_off():
    # Natavení čtení řádků klavesnice do default hodnoty
    for i in range(4):
        keypad.set_output(i, True)


def status_key():
    status = [True for i in range(8)]
    is_all_true = True
    for i in range(8):
        status[i] = keypad.get_pin_state(i)
        if not status[i]:
            is_all_true = False
    return is_all_true


def read_key():
    key = ""
    for row in range(4, 8):  # První for loop zaponá postupně řádky
        while not status_key():
            row_off()
            coll_off()
        keypad.set_output(row, False)

        for key_index in range(4):  # Druhý for loop čte znaky na zapnutém řádku
            if not keypad.get_pin_state(key_index):
                key = keys[abs(row-7)][key_index]
                # print(keys[abs(row-7)][key])
                while not keypad.get_pin_state(key_index):
                    coll_off()
                    row_off()
                continue
            else:
                continue
    return key


def button_pressed_callback(d):
    print("Button pressed " + str(d))


def core2_auto_scroll_names():
    global lock
    count = 0
    while True:
        show_areas()
        print(count)
        count += 1


# GPIO.setmode(GPIO.BCM)
# for dig_ping in alarm.get_secured_areas():
#     GPIO.setup(dig_ping, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# for dig_ping in alarm.get_secured_areas():
#     GPIO.add_event_detect(dig_ping, GPIO.FALLING,
#                           callback=button_pressed_callback, bouncetime=10)


# ______________Server handling SOCKET IO______________
# put them all together as a string that shows SQLAlchemy where the database is


# NOTHING BELOW THIS LINE NEEDS TO CHANGE
# this route will test the database connection and nothing more


# Message to client
# def button(data):
#     print("Send")
#     socketio.emit('some event', data)


# ______________Server handling SOCKET IO______________


# def core2():
#     global lock
#     while True:
#         if input("a"):
#             data.set_data(Areas)
#             alarm.send_func(Areas)


# def core1():
# if __name__ == '__main__':
#     while True:

        # @socketio.event
        # def my_event(message):
        #     session['receive_count'] = session.get('receive_count', 0) + 1
        #     emit('my_response',
        #          {'data': message['data'], 'count': session['receive_count']})

        # ####### Example fetch ############
        # @app.route('/test', methods=['GET', 'POST'])
        # def testfn():
        #     # POST request
        #     if request.method == 'POST':
        #         print(request.get_json())  # parse as JSON
        #         return 'OK', 200
        #     # GET request
        #     else:
        #         message = {'greeting': data.get_data()}
        #         return jsonify(message)  # serialize and use JSON headers

        # def core1_keypad():
        #     global lock
        #     while True:
        #         key = read_key()
        #         if key == "A":
        #             lock.acquire()
        #             lcd.lcd_display_string_pos("ON", 2, 13)
        #             lcd.lcd_display_string_pos(" ", 2, 15)
        #             lock.release()
        #         if key == "B":
        #             lock.acquire()
        #             lcd.lcd_display_string_pos("OFF", 2, 13)
        #             lcd.lcd_display_string_pos(" ", 2, 16)
        #             lock.release()
        #         if key == "C":
        #             lock.acquire()
        #             lcd.lcd_clear()
        #             lock.release()
