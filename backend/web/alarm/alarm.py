from flask import Blueprint, render_template, jsonify, request
from modules import query
from werkzeug.security import generate_password_hash, check_password_hash
from web import SocketIO_events
from copy import deepcopy
import RPi.GPIO as GPIO
from modules import query, AlarmFunctions
import time
from web import SocketIO_events
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies
from datetime import datetime
from datetime import timedelta
from datetime import timezone

alarm = Blueprint('alarm', __name__)


@alarm.route('/api/updateAlarmSetting', methods=['GET', 'POST'])
@jwt_required()
def updateAlarmSetting():
    try:
        query.set_Setting(
            'ArmTime', request.json['armtime'])
        query.set_Setting(
            'AlertTime', request.json['alerttime'])
        result = True
    except:
        result = "Error when update alarm setting"
    return jsonify(result)


@alarm.route('/api/updateAlarmOutput', methods=['GET', 'POST'])
@jwt_required()
def updateAlarmOutput():
    try:
        query.update_Output(
            request.json['Name'], 'alarm', request.json['DigitalPin'], request.json['OutputID'])
        result = True
    except:
        result = "Error when update Outputs"
    return jsonify(result)


@alarm.route('/api/deleteAlarmOutput', methods=['GET', 'POST'])
@jwt_required()
def deleteAlarmOutput():
    try:
        query.delete_Output(request.json['OutputID'])
        result = True
    except:
        result = f"Error delete output"
    return jsonify(result)


@alarm.route('/api/newAlarmOutput', methods=['GET', 'POST'])
@jwt_required()
def newAlarmOutput():
    try:
        query.set_newOutput(
            request.json['Name'], 'alarm', request.json['DigitalPin'])
        result = True
    except:
        result = "Error when set new Outputs"
    return jsonify(result)


@alarm.route('/api/getAlarmSetting', methods=['GET', 'POST'])
@jwt_required()
def getAlarmSetting():
    try:
        result = {}
        alerttime = query.get_Setting('AlertTime')[0]['Value']
        armtime = query.get_Setting('ArmTime')[0]['Value']
        result['armtime'] = armtime
        result['alerttime'] = alerttime
    except:
        result = False
    return jsonify(result)


@alarm.route('/api/getSensors', methods=['GET', 'POST'])
@jwt_required()
def getSensors():
    try:
        result = query.get_AllSensor()
    except:
        result = False
    return jsonify(result)


@alarm.route('/api/updateSensor', methods=['GET', 'POST'])
@jwt_required()
def updateSensor():
    try:
        query.update_Sensor(request.json['Name'], request.json['Type'],
                            request.json['DigitalPin'], request.json['SensorID'])
        result = True
    except:
        sensorsName = request.json['Name']
        result = f"Error update sensor: {sensorsName} "
    return jsonify(result)


@alarm.route('/api/deleteSensor', methods=['GET', 'POST'])
@jwt_required()
def deleteSensor():
    try:
        query.delete_Sensor(request.json['SensorID'])
        result = True
    except:
        result = f"Error delete sensor"
    AlarmFunctions.reinit_alarm()
    return jsonify(result)


@alarm.route('/api/newSensor', methods=['GET', 'POST'])
@jwt_required()
def newSensor():
    try:
        query.set_newSensor(request.json['Name'], request.json['Type'],
                            request.json['DigitalPin'])
        result = True
    except:
        sensorName = request.json['Name']
        result = f"Error set new sensor: {sensorName} "
    AlarmFunctions.reinit_alarm()
    return jsonify(result)


@alarm.route('/api/deleteArea', methods=['GET', 'POST'])
@jwt_required()
def deleteArea():
    try:
        query.delete_Area(request.json['AreaID'])
        result = True
    except:
        areaname = query.get_AreaName_byID(request.json['AreaID'])
        result = f"Error when delete Area: {areaname} "
    return jsonify(result)


@alarm.route('/api/getAlarmOutputs', methods=['GET', 'POST'])
@jwt_required()
def getAlarmOutputs():
    try:
        result = query.get_AllOutputs()
    except:
        result = f"Error when read Outputs from DB"
    return jsonify(result)


@alarm.route('/api/newAreaDef', methods=['GET', 'POST'])
@jwt_required()
def newAreaDef():
    # try:
    newAreaID = query.set_newArea(request.json['AreaName'])
    for item in request.json['Sensors']:
        if item['use'] == True:
            query.update_AreaDefinition(
                item['SensorID'], newAreaID)
    result = True
    # except:
    #     result = f"Error when try to create new Area: {request.json['AreaName']} "
    return jsonify(result)


@alarm.route('/api/updateAreaDef', methods=['GET', 'POST'])
@jwt_required()
def updateAreaDef():
    try:
        query.delete_AreaDef(request.json['AreaID'])
        for item in request.json['Sensors']:
            if item['use'] == True:
                query.update_AreaDefinition(
                    item['SensorID'], request.json['AreaID'])
        query.update_AreaName(request.json['AreaName'], request.json['AreaID'])
        result = True
    except:
        areaname = query.get_AreaName_byID(request.json['AreaID'])
        result = f"Error when try to update AreaDefinition: {areaname[0][0]} "
    return jsonify(result)


@alarm.route('/api/getAreaDef', methods=['GET', 'POST'])
@jwt_required()
def getAreaDef():
    areas = query.get_Areas()
    areadef = query.get_AreaDefiniton()
    sensors = query.get_AllSensor()
    resultAreaDef = {}
    for item in sensors:
        item.pop("Type")
        item.pop("DigitalPin")
        item["use"] = False
    for a in areas:
        resultAreaDef[a["AreaID"]] = {}
    for a in areas:
        for sen in sensors:
            sen['use'] = False
        for area in areadef:
            if area['AreaID'] == a['AreaID']:
                for sensor in sensors:
                    if sensor['SensorID'] == area['SensorID']:
                        sensor['use'] = True
        resultAreaDef[a['AreaID']] = deepcopy(sensors)
    return jsonify(resultAreaDef)


@alarm.route('/api/deleteNightmodeArea', methods=['GET', 'POST'])
@jwt_required()
def deleteNightmodeArea():
    try:
        query.delete_area_Nightmode(request.json['AreaID'])
        result = True
    except:
        areaname = query.get_AreaName_byID(request.json['AreaID'])[0][0]
        result = f"Error when try dlete area from NightMode: {areaname}"
    return jsonify(result)


@alarm.route('/api/updateNightmode', methods=['GET', 'POST'])
@jwt_required()
def updateNightmode():
    try:
        query.delete_all_Nightmode()
        for item in request.json:
            if item['use'] == True:
                query.set_Nightmode(item['AreaID'])
        result = True
    except:
        result = f"Error when try to set NightMode"
    return jsonify(result)


@alarm.route('/api/getCode')
@jwt_required()
def getCode():
    passw = query.get_Setting('AlarmCode', True)[0]['Value']
    result = (check_password_hash(passw, 'abc'))
    return jsonify(result)


@alarm.route('/api/broad')
@jwt_required()
def update():
    SocketIO_events.broadcast_updatedAreas()
    result = True
    return jsonify(result)


@alarm.route('/api/getNightmode')
@jwt_required()
def getNightmode():
    nightmodeAreas = query.get_Nightmode()
    for item in nightmodeAreas:
        item['AreaName'] = query.get_AreaName_byID(item['AreaID'])[
            0]['AreaName']
    return jsonify(nightmodeAreas)


@alarm.route('/api/turnOffSirene', methods=['GET', 'POST'])
@jwt_required()
def turnOffSirene():
    AlarmFunctions.alert = False
    return jsonify(True)


@alarm.route('/api/disarm', methods=['GET', 'POST'])
@jwt_required()
def disarm():
    print('disarm')
    AlarmFunctions.unsecure_all_house()
    return jsonify(True)


@alarm.route('/api/startBeeping', methods=['GET', 'POST'])
@jwt_required()
def startBeeping():
    try:
        AlarmFunctions.start_armin_beeping_from_app(request.json['beep'])
        result = True
    except:
        result = False
    return jsonify(result)


@alarm.route('/api/getAreas', methods=['GET', 'POST'])
@jwt_required()
def getAreas():
    result = query.get_Areas()
    return jsonify(result)


@alarm.route('/api/checkAlarmCode', methods=['GET', 'POST'])
@jwt_required()
def checkAlarmCode():
    alarmCodeDB = query.get_Setting('AlarmCode')[0]['Value']
    alarmCodeClient = request.json['alarmCode']
    result = (check_password_hash(alarmCodeDB, str(alarmCodeClient)))
    return jsonify(result)


@alarm.route('/api/updateAreas', methods=['GET', 'POST'])
@jwt_required()
def updateAreas():
    areas = []
    areas = request.json
    errormsg = ""
    updateCheck = []
    result = {
        "errortext": "",
        "errorstatus": bool
    }
    for key in range(len(areas)):
        if areas[key]['Switch'] == True:
            status = 'secured'
        else:
            status = 'unsecured'
        areas[key]['Status'] = status
        try:
            query.update_Areas(areas[key]['AreaID'], areas[key]['AreaName'],
                               areas[key]['Switch'], areas[key]['Status'])
        except:
            # ERROR when writing to database
            updateCheck.append(False)
            result.update({"errortext": all(updateCheck)})
            errormsg = errormsg + \
                f"error area: {areas[key]['AreaName']}" + " / "
        else:
            # OK updated database
            updateCheck.append(True)
    errorstatus = all(updateCheck)
    result.update({"errorstatus": errorstatus})
    result.update({"errortext": errormsg})
    if errorstatus:
        SocketIO_events.broadcast_updatedAreas()
    return jsonify(result)


# check if header in request contain valid auth cookie

@alarm.after_request
def refresh_expiring_jwts(response):
    try:
        # print('refresh token---alarm')
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            # print('get longer token--------------')
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # print('token expire---alarm')
        # Case where there is not a valid JWT. Just return the original response
        return response
