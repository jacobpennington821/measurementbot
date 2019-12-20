import sqlite3 as sql
import pandas as pd
import random
import math
import os
from pint import UnitRegistry, UndefinedUnitError

dbConn = sql.connect(":memory:", check_same_thread=False)
dbConn.row_factory = sql.Row
u_reg = UnitRegistry()
u_reg.default_format = "H"

def setup():
    cur = dbConn.cursor()
    for root, dirs, files in os.walk("data"):
        for file in files:
            if file.endswith(".csv"):
                readFile = pd.read_csv(os.path.join(root, file))
                readFile.to_sql(file.split(".")[0], dbConn, index=False)
                cur.execute("SELECT * FROM " + file.split(".")[0] + ";")

def get_random_record(record_type: str):
    if record_type not in ["volumes", "times", "mass", "lengths"]:
        return None

    cur = dbConn.cursor()
    cur.execute("SELECT * FROM " + record_type + " WHERE rowid = abs(random()) % (SELECT max(rowid) FROM " + record_type + ") + 1;")
    row = cur.fetchone()

    return row

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
    if dumb == 1000:
        if bigger:
            return "thiccer"
        else:
            return "less thiccer"
    if unitType == "times" or unitType == "lengths":
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
        return "m&#179"
    else:
        return unitType

def capitalise(string: str) -> str:
    if len(string) == 0:
        return string
    elif len(string) == 1:
        return string.capitalize()
    else:
        return string[0].capitalize() + string[1:]

def makeSentence(unitType: str, inValue: float, inValueNormalised: float, inUnit: str, compareValue: float, compareUnit: str, sentenceType: int = None, intensity: int = None, inString: str = None):
    if sentenceType is None:
        sentenceType = random.randint(0, 2)
    if intensity is None:
        intensity = random.randint(0, 100)
    
    if inValue.is_integer():
        inValue = int(inValue)

    ratio = float(inValueNormalised) / float(compareValue)

    ratio = float("%.4g" % ratio)

    fraction = False

    if ratio.is_integer():
        ratio = int(ratio)
        ratioString = str(ratio)
    elif fraction and ratio < 1:
        top, bottom = ratio.as_integer_ratio()
        ratioString = "<sup>" + str(top) + "</sup>&frasl;<sub>" + str(bottom) + "</sub>"
    else:
        ratioString = str(ratio)
        if "e" in ratioString:
            a,b = ratioString.split("e")
            ratioString = a + "x10<sup>" + str(int(b)) + "</sup>"

    same = False
    if math.isclose(float(inValueNormalised), float(compareValue), abs_tol=1e-2):
        same = True

    exact = False
    if math.isclose(round(ratio), ratio, abs_tol=1e-2):
        exact = True

    sentence = ""

    if sentenceType == 0:
        if intensity > 90:
            sentence += "WOW! "
        elif intensity < 10:
            sentence += "oh. "
        
        if inString is None:
            sentence += str(inValue) + " " + str(inUnit) + " is about the same as " + ratioString + " times " + str(compareUnit)
        else:
            sentence += str(inString) + " is about the same as " + ratioString + " times " + str(compareUnit)
    elif sentenceType == 1:
        if ratio < 1:
            invRatio = 1 / ratio
            sentence += capitalise(str(compareUnit)) + " is " + str(invRatio) + " times " + getComparisonFromType(getTypeFromUnit(inUnit), True)
        else:
            sentence += capitalise(str(compareUnit)) + " is " + ratioString + " times " + getComparisonFromType(getTypeFromUnit(inUnit), False)
        
        sentence += " than " + inString
    elif sentenceType == 2:
        if inString is None:
            sentence += capitalise(str(inValue)) + " " + str(getUnitDisplayName(inUnit)) + " is about " + ratioString + " times " + str(compareUnit)
        else:
            sentence += capitalise(str(inString)) + " is about " + ratioString + " times " + str(compareUnit)
    return sentence    

def generate_from_query_string(query: str) -> str:
    try:
        parsed_input = u_reg.parse_expression(query)
        if not hasattr(parsed_input, "dimensionality"):
            raise FailedGenerationError("Provided query is not valid")

        normalised_input = parsed_input.to_base_units()
        
        if normalised_input.dimensionality == {"[length]": 1}:
            unitType = "lengths"
        elif normalised_input.dimensionality == {"[time]": 1}:
            unitType = "times"
        elif normalised_input.dimensionality == {"[mass]": 1}:
            unitType = "mass"
        elif normalised_input.dimensionality == {"[length]": 3}:
            unitType = "volumes"
        else:
            raise FailedGenerationError("Invalid unit type")

        random_record = get_random_record(unitType)
        return makeSentence(unitType,
            float(parsed_input.magnitude), normalised_input.magnitude, "{0.units}".format(parsed_input),
            random_record["Value"], random_record["Unit"], inString=query)
    except UndefinedUnitError:
        raise FailedGenerationError("Invalid unit type")

class FailedGenerationError(Exception):
    pass

