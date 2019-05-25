import pandas as pd

def wide(unit, value):
    if (unit == 'metrescubed'):
        unit = 'volumes'
    elif (unit == 'seconds'):
        unit = 'times'
    elif (unit == 'kg'):
        unit = 'mass'

    pd.

#metrescubed / seconds / kg