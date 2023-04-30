"""Measurement API backend. """

import math
import os
import random

import sqlite3 as sql
import pandas as pd

from pint import UnitRegistry, UndefinedUnitError

dbConn = sql.connect(":memory:", check_same_thread=False)
dbConn.row_factory = sql.Row
u_reg = UnitRegistry()
u_reg.default_format = "H"


def setup():
    cur = dbConn.cursor()
    for root, _dirs, files in os.walk("data"):
        for file in files:
            if file.endswith(".csv"):
                readFile = pd.read_csv(os.path.join(root, file))
                readFile.to_sql(file.split(".")[0], dbConn, index=False)
                cur.execute("SELECT * FROM " + file.split(".")[0] + ";")


def get_random_record(record_type: str):
    if record_type not in ["volumes", "times", "mass", "lengths"]:
        return None

    cur = dbConn.cursor()
    cur.execute(
        "SELECT * FROM "
        + record_type
        + " WHERE rowid = abs(random()) % (SELECT max(rowid) FROM "
        + record_type
        + ") + 1;"
    )
    row = cur.fetchone()

    return row


def getComparisonFromType(unitType: str, bigger: bool) -> str:
    dumb = random.randint(0, 1000)
    if dumb == 1000:
        return "thiccer" if bigger else "less thiccer"
    if unitType == "times" or unitType == "lengths":
        return "longer" if bigger else "shorter"
    if unitType == "mass":
        return "heavier" if bigger else "lighter"
    return "bigger" if bigger else "smaller"


def getComparison2FromType(unitType: str) -> str:
    if unitType == "volumes":
        return "size"
    if unitType == "lengths":
        return "length"
    if unitType == "mass":
        return "mass"
    if unitType == "times":
        return "length"
    return ""


def getUnitDisplayName(unitType: str) -> str:
    if unitType == "metrescubed":
        return "m&#179"
    return unitType


def capitalise(string: str) -> str:
    if len(string) == 0:
        return string
    if len(string) == 1:
        return string.capitalize()
    return string[0].capitalize() + string[1:]


def makeSentence(
    unitType: str,
    inValue: float,
    inValueNormalised: float,
    inUnit: str,
    compareValue: float,
    compareUnit: str,
    sentenceType: int | None = None,
    intensity: int | None = None,
    inString: str | None = None,
) -> str:
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
            a, b = ratioString.split("e")
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
            sentence += f"{inValue} {inUnit} is about the same as {ratioString} times {compareUnit}"
        else:
            sentence += (
                f"{inString} is about the same as {ratioString} times {compareUnit}"
            )

    elif sentenceType == 1:
        if ratio < 1:
            invRatio = 1 / ratio
            sentence += (
                f"{capitalise(str(compareUnit))} is {invRatio} "
                f"times {getComparisonFromType(unitType, True)}"
            )
        else:
            sentence += (
                f"{capitalise(str(compareUnit))} is {ratioString} "
                f"times {getComparisonFromType(unitType, False)}"
            )

        sentence += " than " + str(inString)

    elif sentenceType == 2:
        if inString is None:
            sentence += (
                f"{capitalise(str(inValue))} {getUnitDisplayName(inUnit)} "
                f"is about {ratioString} times {compareUnit}"
            )
        else:
            sentence += (
                f"{capitalise(str(inString))} is about {ratioString} "
                f"times {compareUnit}"
            )
    return sentence


def generate_from_query_string(query: str) -> str:
    try:
        parsed_input = u_reg(query)
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
        return makeSentence(
            unitType,
            float(parsed_input.magnitude),
            normalised_input.magnitude,
            f"{parsed_input.units}",
            random_record["Value"],
            random_record["Unit"],
            inString=query,
        )
    except UndefinedUnitError:
        raise FailedGenerationError("Invalid unit type")


class FailedGenerationError(Exception):
    pass
