import mariadb
import sys


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
# query = f"INSERT INTO Areas (AreaName) VALUES ('{value}')"
query = "SELECT `AreaName` FROM `Areas` WHERE `AreaID` = 3"
cur.execute(query)
print(cur.fetchall())
conn.commit()
