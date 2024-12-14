import database

# -------------------------- write query --------------------------
def write_temp(sensorID: int, temp: float):
    database.write_query(
        "INSERT INTO TempLog (SensorID,Temperature) VALUES (%s, %s)", (sensorID, temp))


def set_newArea(AreaName):
    # Create new area in DB
    database.write_query(
        "INSERT INTO Areas (AreaName) VALUES ('%s')" % AreaName, None)
    # Get ID of new created area
    newAreaID = database.read_query(
        """SELECT AreaID FROM Areas Where AreaName = '%s';""" % AreaName)[0][0]
    return newAreaID


def update_AreaDefinition(SensorID, AreaID):
    result = database.write_query(
        "INSERT INTO AreaDefiniton (SensorID,AreaID) VALUES (%s,%s)", (SensorID, AreaID))
    return result


def set_newSensor(name, type, pin):
    database.write_query(
        "INSERT INTO Sensors (Name,Type,DigitalPin) VALUES (%s, %s, %s)", (name, type, pin))


def set_newUser(username: str, email: str, pushToken: str, passw, sendmsg: str, accounType: str):
    database.write_query(
        "INSERT INTO Users (UserName,email,PushBulletToken,Pass,SendMsg,AccountType) VALUES (%s,%s, %s, %s, %s, %s)", (username, email, pushToken, passw, sendmsg, accounType))


def update_Sensor(name, type, pin, id):
    database.write_query(
        "UPDATE Sensors SET Name=(%s),Type=(%s),DigitalPin=(%s) WHERE SensorID=(%s)", (name, type, pin, id))


def update_User_Pass(passw, userid):
    database.write_query(
        "UPDATE Users SET Pass=(%s) WHERE UserID=(%s)", (passw, userid))


def update_User(name, email, pushtoken, sendmsg, accounttype, userid):
    database.write_query(
        "UPDATE Users SET UserName=(%s),email=(%s),PushBulletToken=(%s),SendMsg=(%s),AccountType=(%s) WHERE UserID=(%s)", (name, email, pushtoken, sendmsg, accounttype, userid))


def update_Output(name, type, pin, id):
    database.write_query(
        "UPDATE Outputs SET Name=(%s),Type=(%s),DigitalPin=(%s) WHERE OutputID=(%s)", (name, type, pin, id))


def set_newOutput(name, type, pin):
    database.write_query(
        "INSERT INTO Outputs (Name,Type,DigitalPin) VALUES (%s, %s, %s)", (name, type, pin))


def delete_Output(id):
    database.write_query(
        "DELETE FROM Outputs WHERE OutputID=%s" % id, None)


def delete_User(userid):
    database.write_query(
        "DELETE FROM Users WHERE UserID=%s" % userid, None)


def delete_AreaDef(AreaID):
    database.write_query(
        "DELETE FROM AreaDefiniton WHERE AreaID=%s" % AreaID, None)


def delete_Area(id):
    database.write_query(
        "DELETE FROM Areas WHERE AreaID=%s" % id, None)


def delete_Sensor(id):
    database.write_query(
        "DELETE FROM Sensors WHERE SensorID=%s" % id, None)


def set_Alert_Log(pin_number):
    database.write_query(
        """INSERT INTO AlarmEventLog(AreaName, SensorName, TimeStamp) VALUES 
        ((SELECT AreaName FROM Areas Where AreaID IN(SELECT AreaID FROM AreaDefiniton WHERE SensorID IN
        (SELECT SensorID FROM Sensors WHERE DigitalPin = %s))), (SELECT Name FROM Sensors Where DigitalPin = %s), CURRENT_TIMESTAMP())""", (pin_number, pin_number))


def set_Actual_areaStatus(areaID, status):
    database.write_query(
        "UPDATE Areas SET Status= %s  WHERE AreaID= %s", (status, areaID))


def update_AreaName(AreaName, AreaID):
    database.write_query(
        "UPDATE Areas SET AreaName=%s WHERE AreaID= %s", (AreaName, AreaID))


def update_Areas(AreaID, AreaName, Secured, Status):
    database.write_query(
        "UPDATE Areas SET AreaName=%s, Switch=%s, Status=%s  WHERE AreaID= %s", (AreaName, Secured, Status, AreaID))


def delete_all_Nightmode():
    result = database.write_query(
        "TRUNCATE TABLE Nightmode", None)
    return result


def delete_area_Nightmode(AreaID):
    result = database.write_query(
        "DELETE FROM Nightmode WHERE AreaID=%s" % AreaID, None)
    return result


def set_Nightmode(AreaID):
    result = database.write_query(
        "INSERT INTO Nightmode (AreaID) VALUES ('%s')" % AreaID, None)
    return result

# -------------------------- read query --------------------------

def get_last_temp(sensorID: int):
    result = database.read_query(
        "SELECT * FROM TempLog WHERE SensorID=%s ORDER BY DateTime DESC LIMIT 1;" % sensorID, True)
    return result[0]

def get_Nightmode():
    result = database.read_query(
        "SELECT * FROM `Nightmode`", True)
    return result


def get_AllInputs():
    result = database.read_query("SELECT * FROM Inputs", True)
    return result


def get_AllOutputs():
    result = database.read_query("SELECT * FROM Outputs", True)
    return result


def get_Outputs(Name):
    result = database.read_query(
        "SELECT * FROM Outputs WHERE Name = '%s'" % Name, True)
    return result


def get_default(sql_message):
    result = database.read_query(sql_message, True)
    return result


def set_unreadMsg(username, type, eventID):
    database.write_query(
        "INSERT INTO UnreadMsg (userName,type,eventID) VALUES (%s,%s,%s)", (username, type, eventID))


def get_unreadMsg(username, type):
    result = database.read_query(
        "SELECT COUNT(*) FROM UnreadMsg WHERE userName='%s' AND type='%s'" % (username, type), True)
    return result[0]["COUNT(*)"]


def get_unreadMsg_dates(username, type):
    result = database.read_query(
        "SELECT TimeStamp FROM AlarmEventLog WHERE AlarmEventID IN (SELECT eventID FROM UnreadMsg WHERE userName = '%s' AND type='%s')" % (username, type), True)
    return result


def delete_unreadAlarmMsg(username, type):
    database.write_query(
        "DELETE FROM UnreadMsg WHERE userName ='%s' AND type='%s' " % (username, type), None)


def get_AlarmLog(startDate, endDate):
    # startDate = "2023-07-15 00:00:00"
    # endDate = "2023-07-30 00:00:00"
    result = database.read_query(
        "SELECT * FROM AlarmEventLog WHERE TimeStamp BETWEEN '%s' AND '%s' ORDER BY TimeStamp DESC" % (startDate, endDate), True)
    return result


def get_LastAlarmLog():
    lastlog = database.read_query(
        "SELECT AreaName, SensorName, Datetime FROM AlarmEventLog ORDER BY DateTime DESC LIMIT 1", None)
    location = lastlog[0][0] + ":" + " " + lastlog[0][0]
    dateTime = str(lastlog[0][2])
    return location, dateTime


def get_AreasStatus():
    result = database.read_query(
        "SELECT AreaID, Status FROM Areas", True)
    return result
    # return json.dumps(result)


def get_Setting(settingName):
    result = database.read_query(
        """SELECT * FROM Setting WHERE Name = '%s';""" % settingName, True)
    return result


def get_allSetting():
    result = database.read_query("SELECT * FROM Setting", True)
    return result


def set_Setting(name, value):
    result = database.write_query(
        "UPDATE Setting SET Value = (%s) WHERE Name = (%s)", (value, name))
    return result


def set_Output(name, value):
    result = database.write_query(
        "UPDATE Outputs SET Name = (%s) WHERE Name = (%s)", (value, name))
    return result


def get_Areas():
    result = database.read_query("SELECT * FROM `Areas`", True)
    return result


def get_AreasName():
    result = database.read_query("SELECT AreaName FROM `Areas`", True)
    return result


def get_AreaName_byID(AreaID):
    result = database.read_query(
        "SELECT AreaName FROM `Areas` WHERE AreaID = '%s'" % AreaID, True)
    return result


def get_AreaStatus_byID(AreaID):
    result = database.read_query(
        "SELECT Status FROM `Areas` WHERE AreaID = '%s'" % AreaID)
    return result


def get_LogSensorsGPIOpin():
    result = database.read_query(
        "Select DigitalPin FROM Sensors WHERE SensorID IN (SELECT SensorID FROM SensorContinuosLogDefiniton)", None)
    return result


def get_AllSensorsGPIOpin():
    result = database.read_query(
        "SELECT DigitalPin FROM Sensors WHERE NOT Type = 'temp'", True)
    return result


def get_AllSensorsNameType():
    result = database.read_query("SELECT Name, Type FROM Sensors", True)
    return result


# def get_AreasSensorsPIN(areaName):
#     result = database.convertListOfTuplesto_List(database.read_query(
#         """SELECT DigitalPin FROM Sensors Where SensorId IN
#             (SELECT SensorID FROM AreaDefiniton WHERE AreaID IN
#             (SELECT AreaID FROM Areas WHERE AreaName = '%s'));""" % areaName, None))
#     return result


def get_AreaName_by_pin(pin_number):
    result = database.read_query(
        """SELECT AreaName FROM Areas Where AreaID IN
            (SELECT AreaID FROM AreaDefiniton WHERE SensorID IN
            (SELECT SensorID FROM Sensors WHERE DigitalPin = '%s'));""" % pin_number, None)
    return result[0][0]


def get_areaID_by_pin(pin_number):
    result = database.read_query("""SELECT AreaID FROM Areas Where AreaID IN
            (SELECT AreaID FROM AreaDefiniton WHERE SensorID IN
            (SELECT SensorID FROM Sensors WHERE DigitalPin = '%s'))""" % pin_number, None)
    return result[0][0]


def get_sensor_name_by_pin(pin_number):
    result = database.read_query(
        "SELECT Name FROM Sensors Where DigitalPin = '%s'" % pin_number, True)
    return result[0]['Name']


def get_sensor_type_by_pin(pin_number):
    result = database.read_query(
        "SELECT Type FROM Sensors Where DigitalPin = '%s'" % pin_number, True)
    return result[0]['Type']


def get_pin_by_sensorName(SensorName):
    result = database.read_query(
        """SELECT DigitalPin FROM Sensors Where Name = '%s';""" % SensorName, None)
    return result[0][0]


def get_sensorID_by_pin(pin_number):
    result = database.read_query(
        """SELECT SensorID FROM Sensors Where DigitalPin = '%s';""" % pin_number, True)
    return result[0]


def get_sensorID_by_name(name):
    result = database.read_query(
        """SELECT SensorID FROM Sensors Where Name = '%s';""" % name, None)
    return result[0][0]


def get_sensor_by_type(type):
    result = database.read_query(
        """SELECT * FROM Sensors Where Type = '%s';""" % type, True)
    return result


def get_sensorsNames_AreasDefition(AreaName):
    result = database.convertListOfTuplesto_List(database.read_query(
        """SELECT Name FROM Sensors Where SensorId IN
            (SELECT SensorID FROM AreaDefiniton WHERE AreaID IN
            (SELECT AreaID FROM Areas WHERE AreaName = '%s'));""" % AreaName, None))
    return result


def get_AreaDefiniton():
    result = database.read_query("SELECT * FROM AreaDefiniton", True)
    return result


def get_AllSensor():
    result = database.read_query(
        "SELECT * FROM Sensors WHERE NOT Type = 'temp'", True)
    return result


def get_allUsers():
    result = database.read_query(
        "SELECT * FROM Users", True)
    return result


def get_User(userName):
    result = database.read_query(
        "SELECT * FROM Users WHERE UserName = '%s'" % userName, True)
    return result

# def update_Area(name, id):
#     database.write_query(
#         "UPDATE Areas SET AreaName=(%s) WHERE AreaID=(%s)", (name, id))
