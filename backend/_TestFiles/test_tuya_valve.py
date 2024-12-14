from modules import garageGate, query
import sqlalchemy as sa
from sqlalchemy import select, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from web import SocketIO_events
import RPi.GPIO as GPIO  # print(query.get_Output_GPIOpins(("name"), "18"))
from tuya_iot import TuyaOpenAPI
from requests import get

ACCES_ID = "nsvjmj8pnnwr9wthe4an"
ACCESS_KEY = "78c67e670f3c4f4facec2a6cb7a3265c"
ENDPOINT = "https://openapi.tuyaeu.com"

USERNAME = "jardalufi@gmail.com"
PASSWORD = "Tanvald2664"

VALVE_1_ID = "bf975ba1f5b2f24ed2rose"
VALVE_2_ID = "bfef6635f56b48b8048syl"

openapi = TuyaOpenAPI(ENDPOINT, ACCES_ID, ACCESS_KEY)

openapi.connect(USERNAME, PASSWORD, '420')


commands = {
    'commands': [
        {
            'code': 'comfort_temp',
            'value': 7
        }
    ]
}
result = openapi.post(
    '/v1.0/iot-03/devices/bf975ba1f5b2f24ed2rose/commands', commands)
print(result)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# class Sen(Base):
#     __tablename__ = 'Sensors'
#     sensorID = sa.Column(sa.Integer, primary_key=True)
#     name = sa.Column(sa.String(length=100))
#     type = sa.Column(sa.String(length=100))
#     digitalPin = sa.Column(sa.Integer)

#     # def __init__(self, sensorID, name, type, digitalPin):
#     #     self.sensorID = sensorID
#     #     self.name = name
#     #     self.name = type
#     #     self.name = digitalPin


# Session = sessionmaker(bind=engine)
# session = Session()
# c1 = Sen(name="pokus", type="magnet", digitalPin=24)
# session.add(c1)
# session.commit()

# pokus = session.query(Sen).all()
# for row in pokus:
#     print(row.name)
# areas = query.get_Areas(True)
# for item in areas:
#     item.update({"pokus": 10})
# print(len(areas))

# print(query.get_sensorsNames_AreasDefition("asdasd"))
