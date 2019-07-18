import sqlite3 as sql
import pandas as pd
import random
import math
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

    ratio = float(value) / row["Value"]

    output = makeSentence(value, unit, row["Value"], row["Unit"], sentenceType=2)

    # output = str(value) + " " + str(unit) + " is the same as " + str(ratio) + " times " + str(row["Unit"])

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

def getComparisonFromType(unitType, bigger):
    dumb = random.randint(0, 1000)
    if dumb is 1000:
        if bigger:
            return "thiccer"
        else:
            return "less thiccer"
    if unitType == "volumes":
        if bigger:
            return "more spacious"
        else:
            return "less spacious"
    elif unitType == "times" or unitType == "lengths":
        if bigger:
            return "longer"
        else:
            return "shorter"
    elif unitType == "mass":
        if bigger:
            return "heavier"
        else:
            return "lighter"
    else:
        if bigger:
            return "bigger"
        else:
            return "smaller"

def getComparison2FromType(unitType):
    if unitType == "volumes":
        return "size"
    if unitType == "lengths":
        return "length"
    if unitType == "mass":
        return "mass"
    if unitType == "times":
        return "length"

def getUnitDisplayName(unitType):
    if unitType == "metrescubed":
        return "m&#179";
    else:
        return unitType

def makeSentence(inValue, inUnit, compareValue, compareUnit, sentenceType = None, intensity = None):
    if sentenceType is None:
        sentenceType = random.randint(0, 2)
    if intensity is None:
        intensity = random.randint(0, 100)

    ratio = float(inValue) / float(compareValue)

    ratio = float("%.4g" % ratio)

    if ratio.is_integer():
        ratio = int(ratio)

    same = False
    if math.isclose(float(inValue), float(compareValue), abs_tol=1e-2):
        same = True

    exact = False
    if math.isclose(round(ratio), ratio, abs_tol=1e-2):
        exact = True

    if "e" in str(ratio):
        ratioString = str(ratio)
        a,b = ratioString.split("e")
        print(a,b)
        ratio = a + "x10<sup>" + str(int(b)) + "</sup>"
    
    sentence = ""

    if sentenceType is 0:
        if intensity > 90:
            sentence += "WOW! "
        elif intensity < 10:
            sentence += "oh. "
        sentence += str(inValue) + " " + str(inUnit) + " is about the same as " + str(ratio) + " times " + str(compareUnit)
    elif sentenceType is 1:
        if ratio < 1:
            invRatio = 1 / ratio
            sentence += str(compareUnit) + " is " + str(invRatio) + " times " + getComparisonFromType(getTypeFromUnit(inUnit), False)
        else:
            sentence += str(compareUnit) + " is " + str(ratio) + " times " + getComparisonFromType(getTypeFromUnit(inUnit), True)
        
        sentence += " than " + str(inValue) + " " + str(inUnit)
    elif sentenceType is 2:
        sentence += str(inValue) + " " + str(getUnitDisplayName(inUnit)) + " is about " + str(ratio) + " times " + str(compareUnit)

    return sentence
