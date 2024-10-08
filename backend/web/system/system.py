from flask import Blueprint, render_template, jsonify, request
from modules import query, AlarmFunctions, GarageGate
from werkzeug.security import generate_password_hash, check_password_hash
from web import SocketIO_events
import time
from flask_jwt_extended import jwt_required
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies
from flask_jwt_extended import jwt_required
from datetime import datetime
from datetime import date
from datetime import timedelta
from datetime import timezone
system = Blueprint('system', __name__)

# check if header in request contain valid auth cookie¨


@system.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        print(f'refresh token---system {exp_timestamp}')
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        print('token expire---system')
        # Case where there is not a valid JWT. Just return the original response
        return response


@system.route('/pushSetting', methods=['GET', 'POST'])
@jwt_required()
def pushSetting():
    arraySetting = []
    try:
        for setingName in request.json:
            setting = query.get_Setting(setingName)[0]
            if not setting:
                raise Exception(
                    f'Error DB read, check settingName: "{setingName}"')
            else:
                arraySetting.append(setting)
    except Exception as e:
        result = e
    else:
        result = True
        print('--- Read setting OK -> broadcast it to clients ---')
    finally:
        if result == True:
            SocketIO_events.broadcast_setting(arraySetting)
    return str(result)


@system.route('/gateSwitch', methods=['GET', 'POST'])
@jwt_required()
def gateSwitch():
    try:
        GarageGate.apply_gate_switch()
        result = True
    except:
        result = "Problem when open gate"
    return jsonify(result)


@system.route('/system/deleteUnreadAlarmMsg', methods=['GET', 'POST'])
@jwt_required()
def deleteUnreadAlarmMsg():
    try:
        query.delete_unreadAlarmMsg(request.json["username"], "alarm")
    except Exception as err:
        response = jsonify({'msg': 'Error when get AlarmUnreadMsg'})
        return response, 400
    response = jsonify({'msg': 'Succesfull delete alarmEventsMsgs'})
    return response, 200


@system.route('/system/getUnreadAlarmMsg', methods=['GET', 'POST'])
@jwt_required()
def getUnreadAlarmMsg():
    try:
        numberUnreadAlarmMsg = query.get_unreadMsg(
            request.json["username"], "alarm")
        msgdates = query.get_unreadMsg_dates(request.json["username"], "alarm")
        if not msgdates:
            oldestMsgDate = datetime.today()
            latestMsgDate = datetime.today()
            numberUnreadAlarmMsg = 0
        else:
            dateslist = []
            for date in msgdates:
                dateslist.append(date["TimeStamp"])
            oldestMsgDate = str(min(dateslist))
            latestMsgDate = str(max(dateslist))
        print(oldestMsgDate)
        response = jsonify({'msgcount': numberUnreadAlarmMsg,
                           'latestDate': latestMsgDate, 'oldestDate': oldestMsgDate})
    except Exception as err:
        response = jsonify({'msg': 'Error when get AlarmUnreadMsg'})
        return response, 400
    return response, 200


@system.route('/getSetting', methods=['GET', 'POST'])
@jwt_required()
def getSetting():
    arraySetting = []
    # if payload is array of JSONs
    try:
        for item in request.json:
            setting = query.get_Setting(item)
            arraySetting.append(setting[0])
        result = arraySetting
        # print(' --- ARRAY json setting')
    # if payload is single JSON
    except:
        result = query.get_Setting(request.json['settingName'])
        # print(' --- SINGLE json setting')
    return jsonify(result)


@system.route('/deleteUser', methods=['GET', 'POST'])
@jwt_required()
def deleteUser():
    try:
        query.delete_User(request.json['UserID'])
        result = True
    except:
        result = f"Error delete user"
    return jsonify(result)


@system.route('/updateUser', methods=['GET', 'POST'])
@jwt_required()
def updateUser():
    try:
        query.update_User(request.json['UserName'], request.json['email'], request.json['PushBulletToken'],
                          request.json['SendMsg'], request.json['AccountType'], request.json['UserID'])
    except Exception as err:
        response = jsonify({'msg': 'Error when update User'})
        return response, 400
    response = jsonify({'msg': 'User was successfully updated'})
    return response, 200


@system.route('/updateUserPass', methods=['GET', 'POST'])
@jwt_required()
def updateUserPass():
    passw = generate_password_hash(request.json['NewPass'])
    try:
        query.update_User_Pass(passw, request.json['UserID'])
    except Exception as err:
        response = jsonify({'msg': 'Error when update password'})
        return response, 400
    response = jsonify({'msg': 'New pass created'})
    return response, 200


@system.route('/newUser', methods=['GET', 'POST'])
@jwt_required()
def newUser():
    passw = generate_password_hash(request.json['Pass'])
    try:
        query.set_newUser(request.json['UserName'], request.json['Email'], request.json['PushBulletToken'], passw,
                          request.json['SendMsg'], request.json['AccountType'])
    except Exception as err:
        response = jsonify({'msg': 'User was not created'})
        return response, 400
    response = jsonify({'msg': 'New user successfully created'})
    return response, 200


@system.route('/useraccount', methods=['GET', 'POST'])
@jwt_required()
def useraccount():
    try:
        user = query.get_User(request.json['username'])
    except Exception as err:
        response = jsonify({'msg': 'Error when get user data'})
        response.status_code = 400
        return response
    response = jsonify(user)
    return response, 200


@system.route('/system/getLogs', methods=['GET', 'POST'])
@jwt_required()
def getLogs():
    try:
        startdate = str(request.json["startdate"]) + " 00:00:00"
        enddate = request.json["enddate"] + " 23:59:59"
        alarmLogs = query.get_AlarmLog(startdate, enddate)
    except Exception as err:
        response = jsonify({'msg': 'Error when getting logs'})
        response.status_code = 400
        return response
    response = jsonify(alarmLogs)
    return response, 200


@ system.route('/saveGateSensors', methods=['GET', 'POST'])
@ jwt_required()
def saveGateSensors():
    try:
        query.set_Setting('GateSensorUp', request.json['gateUp'])
        query.set_Setting('GateSensorDown', request.json['gateDown'])
        result = True
    except:
        result = 'Error when saving gate sensors to DB'
    return jsonify(result)


@ system.route('/getAllSetting', methods=['GET', 'POST'])
@ jwt_required()
def getAllSetting():
    result = query.get_allSetting(True)
    return jsonify(result)


@ system.route('/reinit_alarm', methods=['GET', 'POST'])
@ jwt_required()
def reinit():
    AlarmFunctions.reinit_alarm()
    return jsonify(True)


@ system.route('/getSensorsState', methods=['GET', 'POST'])
@ jwt_required()
def getSensorsState():
    result = AlarmFunctions.get_sensors_state()
    return jsonify(result)


@ system.route('/getUsers', methods=['GET', 'POST'])
@ jwt_required()
def getUsers():
    result = query.get_allUsers()
    for item in result:
        item['Pass'] = ""
    return jsonify(result)


# @system.route('/checkConnection', methods=['GET', 'POST'])
# def checkConnection():
#     result = True
#     return jsonify(result)


@ system.route('/setSetting', methods=['GET', 'POST'])
@ jwt_required()
def setSetting():
    arraySetting = []
    # if payload is array of JSONs
    try:
        try:
            for item in request.json:
                query.set_Setting(item['settingName'], item['value'])

        # if payload is single JSON
        except:
            query.set_Setting(
                request.json['settingName'], request.json['value'])
        result = True
    except:
        result = "Error when to write to DB"
    result = True
    return jsonify(result)
