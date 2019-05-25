import pandas as pd
import random

def wide(unit, value):
    filename = ''
    if (unit == 'metrescubed'):
        filename = 'volumes'
    elif (unit == 'seconds'):
        filename = 'times'
    elif (unit == 'kg'):
        filename = 'mass'

    lineCount = sum(1 for line in open(filename + '.csv')) - 1
    skip = random.randint(1, lineCount)
    data = pd.read_csv(filename + '.csv', skiprows=skip)

    output = "The value of " + value + " " + unit + " is the same as " + data[0] + " " + data[1]

    return output

#metrescubed / seconds / kg