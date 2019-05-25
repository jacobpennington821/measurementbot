import pandas as pd

def wide(unit, value):
    if (unit == 'metrescubed'):
        unit = 'volumes'
    elif (unit == 'seconds'):
        unit = 'times'
    elif (unit == 'kg'):
        unit = 'mass'

    data = pd.read_csv(unit + '.csv')

    return 'WIDE'

#metrescubed / seconds / kg