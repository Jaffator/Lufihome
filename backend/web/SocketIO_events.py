from web import socketio
from modules import query
from flask import jsonify, json

# message after home page refresh - send list of areas to client
elementsName = ["AllHouse", "Nightmode",
                "GateStatus", "alarm_last_container"]

# --- function to call ---


def broadcast_updatedAreas():
    areasDict = query.get_Areas()
    print('--- Broadcast update Areas called ---')
    socketio.emit('broadcast_updatedAreas', areasDict, broadcast=True)


def broadcast_updatedAlarmEvent():
    print('--- Broadcast update alarm events ---')
    socketio.emit('updateAlarmEvents', None, broadcast=True)


def broadcast_sensorState(sensors):
    print('--- Broadcast update sensor state ---')
    socketio.emit('broadcast_sensorState', sensors, broadcast=True)


def broadcast_gateState(state):
    print('--- Broadcast gate state ---')
    socketio.emit('broadcast_gateState', state, broadcast=True)


def broadcast_setting(arraySetting):
    print('--- Broadcast Setting called ---')
    socketio.emit('broadcast_setting', arraySetting, broadcast=True)


def broadcast_houseall(state):
    socketio.emit('broadcast_houseall', state, broadcast=True)

# ------ socketio message pockets ------


# message after first client connection
@socketio.on('my event')
def handle_message(data):
    print(data)


@socketio.on('nightmode')
def handle_message(data):
    socketio.emit('broadcast_nightmode', data, broadcast=True)


@socketio.on('houseall')
def handle_message(data):
    broadcast_houseall(data)


@socketio.on('resetOrigin')
def handle_message():
    socketio.emit('reset_origin', broadcast=True)


@socketio.on('pushSetting')
def handle_message(selectSetting):
    arraySetting = []
    try:
        for setingName in selectSetting:
            setting = query.get_Setting(setingName)
            if not setting:
                raise Exception(
                    f'Error DB read, check settingName: "{setingName}"')
            else:
                arraySetting.append(setting)
    except Exception as e:
        result = e
        print(e)
    else:
        result = True
        print('--- Read setting OK -> broadcast it to clients ---')
    finally:
        if result == True:
            broadcast_setting(arraySetting)


def refresh_clients():
    print("\n\n\n\n------broadcast refresh page------\n\n\n\n")
    socketio.emit("refresh", {'data': 0}, broadcast=True)
