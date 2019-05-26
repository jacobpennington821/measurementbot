import sqlite3 as sql
import pandas as pd
from pandas import DataFrame
import random
import os

dbConn = sql.connect(":memory:", check_same_thread=False)
dbConn.row_factory = sql.Row

def setup():
    cur = dbConn.cursor()
    for root, dirs, files in os.walk("data"):
        for file in files:
            if file.endswith(".csv"):
                readFile = pd.read_csv(os.path.join(root, file))
                readFile.to_sql(file.split(".")[0], dbConn, index=False)
                cur.execute("SELECT * FROM " + file.split(".")[0] + ";")

def wide(unit, value):
    tableName = getTypeFromUnit(unit)

    cur = dbConn.cursor()
    cur.execute("SELECT * FROM " + tableName + " WHERE rowid = abs(random()) % (SELECT max(rowid) FROM " + tableName + ") + 1; ")
    row = cur.fetchone()

    output = "The value of " + value + " " + unit + " is the same as " + str(row["Unit"]) + " " + str(row["Value"])

    print(output)
    return output

#metrescubed / seconds / kg

def getTypeFromUnit(unit):
    if unit == 'metrescubed':
        return 'volumes'
    elif unit == 'seconds':
        return 'times'
    elif unit == 'kg':
        return 'mass'
    elif unit == 'metres':
        return "lengths"