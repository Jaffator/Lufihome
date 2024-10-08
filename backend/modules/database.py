import mariadb
import sys
import json
import RPi.GPIO as GPIO
from modules import errors
# Connect to MariaDB Platform


def connect_to_database():
    try:
        conn = mariadb.connect(
            user="jaffa",
            password="tanvald222",
            host="localhost",
            port=3306,
            database="homedb"
        )
        # print("MariaDB Database connection successful")
    except mariadb.Error as err:
        print(f"Error connecting to MariaDB Platform: {err}")
        sys.exit(1)
    return conn


def write_query(query, var):
    connection = connect_to_database()
    cursor = connection.cursor()
    try:
        cursor.execute(query, var)
        connection.commit()
    except mariadb.Error as err:
        print(f"Write DB Error: '{err}'")
        raise err
    else:
        result = True
    finally:
        cursor.close()
    return result


def read_query(query, usedict=False):
    print(query)
    connection = connect_to_database()
    cursor = connection.cursor(dictionary=usedict)
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except mariadb.Error as err:
        print(f"Read DB Error: '{err}'")
    cursor.close()


def convertListOfTuplesto_Json(listwithtuples=[]):
    newlist = []
    for item in listwithtuples:
        newlist.append(item[0])
    jsonString = json.dumps(newlist)
    return jsonString


def convertListOfTuplesto_List(listwithtuples=[]):
    newlist = []
    for item in listwithtuples:
        newlist.append(item[0])
    return newlist
