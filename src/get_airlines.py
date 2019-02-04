#!/usr/bin/env python3
import flightradar24
from collections import defaultdict

fr = flightradar24.Api()
airlines = fr.get_airlines()

def get_airlines():
    output = list()
    string = ''

    for airline in airlines['rows']:
        output.append((airline['ICAO'], airline['Name'].replace('-', '')))

    for item in output:
        string += '{icao} {name} - Unknow\r'.format(icao=item[0], name=item[1])

    '''with open('teste.txt', 'w') as file:
        file.write(string)'''

    return output