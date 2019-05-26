import sqlite3 as sql
import pandas as pd
from pandas import DataFrame
import random
import os

dbConn = sql.connect(":memory:")

def setup():
    cur = dbConn.cursor()
    for root, dirs, files in os.walk("data"):
        for file in files:
            if file.endswith(".csv"):
                readFile = pd.read_csv(os.path.join(root, file))
                readFile.to_sql(file.split(".")[0], dbConn, index=False)
                cur.execute("SELECT * FROM " + file.split(".")[0] + ";")
                print(cur.fetchall())


def wide(unit, value):
    filename = getTypeFromUnit(unit)

    lineCount = sum(1 for line in open(filename + '.csv')) - 1
    skip = random.randint(1, lineCount)
    data = pd.read_csv(filename + '.csv', skiprows=skip)

    output = "The value of " + value + " " + unit + " is the same as " + data[0] + " " + data[1]

    return output

#metrescubed / seconds / kg

def getTypeFromUnit(unit):
    if unit == 'metrescubed':
        return 'volumes'
    elif unit == 'seconds':
        return 'times'
    elif unit == 'kg':
        return 'mass'