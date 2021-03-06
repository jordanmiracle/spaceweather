import json
import urllib.request


def chunks(data, rows=10000):
    """ Divides the data into 10000 rows each """

    for i in range(0, len(data), rows):
        yield data[i:i + rows]


url_mag = "https://services.swpc.noaa.gov/products/solar-wind/mag-7-day.json"
url_plasma = "https://services.swpc.noaa.gov/products/solar-wind/plasma-7-day.json"
# url_plasma="https://services.swpc.noaa.gov/json/goes/primary/xray-plasmas-7-day.json"

mag = urllib.request.urlopen(url_mag)
plasma = urllib.request.urlopen(url_plasma)

mag_json = json.loads(mag.read())
plasma_json = json.loads(plasma.read())

mag_json[0:2]

plasma_json[0:2]

import pandas as pd
import numpy as np

df_mag = pd.DataFrame(columns=["Date_time", "Bx", "By", "Bz", "Bt"])
df_plasma = pd.DataFrame(columns=["Date_time", "density", "speed", "temp"])

import sqlite3

# conn = sqlite3.connect("space.db", isolation_level=None)
conn = sqlite3.connect("space.db")
cur = conn.cursor()

cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='mag'")

result = cur.fetchone()

if (result[0] == "mag"):
    cur.execute("drop table mag")

divData = chunks(mag_json[1:])  # divide into 10000 rows each

cur.execute('''
    CREATE TABLE mag (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_time DATETIME,
    bx REAL,
    by REAL,
    bz REAL,
    bt REAL
    );
    ''')

import ipdb

for chunk in divData:
    cur.execute('BEGIN TRANSACTION')

    #     ipdb.set_trace()

    for line in chunk:
        query = 'INSERT INTO mag (date_time, bx, by, bz, bt) VALUES ("%s", "%s", "%s", "%s", "%s")' % (
        line[0][:19], line[1], line[2], line[3], line[6])
        cur.execute(query)

    cur.execute('COMMIT')

divData = chunks(plasma_json[1:])  # divide into 10000 rows each

cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='plasma'")

result = cur.fetchone()

if (result[0] == "plasma"):
    cur.execute("drop table plasma")

cur.execute('''
    CREATE TABLE plasma (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_time DATETIME,
    density REAL,
    speed REAL,
    temp REAL
    );
    ''')

for chunk in divData:
    cur.execute('BEGIN TRANSACTION')

    #     ipdb.set_trace()

    for line in chunk:
        #         ipdb.set_trace()
        query = 'INSERT INTO plasma (date_time, density, speed, temp) VALUES ("%s", "%s", "%s", "%s")' % (
        line[0][:19], line[1], line[2], line[3])
        cur.execute(query)

    cur.execute('COMMIT')