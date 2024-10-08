from curses import keyname
import i2c_lcd
import time
import pcf8574
import psutil
import _thread
import os


lcd = i2c_lcd.lcd()
keypad = pcf8574.PCF8574(1, 0x20)

keys = [["A", "3", "2", "1"],
        ["B", "6", "5", "4"],
        ["C", "9", "8", "7"],
        ["D", "#", "0", "*"]]


def getCPUuse():
    return(str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip(
    )))


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


def core0():
    key = ""
    pos = 5
    while True:
        key = read_key()
        if key != "":
            lcd.lcd_display_string_pos(key, 3, pos)
            pos = pos+1
            if pos > 10:
                pos = 5
                lcd.lcd_clear()


def core1():

    while True:
        if input() == "a":
            print(getCPUuse())


second_thread = _thread.start_new_thread(core1, ())

core0()
