#!/usr/bin/env python3
import json
from src import AIRPORT_SETTINGS
from datetime import datetime
from collections import defaultdict

def make_route():
    items_list = defaultdict(list)
    output = defaultdict(list)

    with open('data/flight_radar.json', 'r') as file:
        items_tap = json.loads(file.read())
    print('='  * 10)
    for item in items_tap:
        items_list[item].append(items_tap[item])

    for item in items_list:
        if len(items_list[item][0]) != 0:
            dep_icao = items_list[item][0][0]['origin']
            arr_icao = items_list[item][0][0]['destination']
            dep_time = items_list[item][0][0]['dep_time']
            arr_time = items_list[item][0][0]['arr_time']
            aircraft = items_list[item][0][0]['aircraft']
            d_icao = ''
            a_icao = ''
            route = ''
            for key in dep_icao:
                d_icao = key
            for key in arr_icao:
                a_icao = key

            if d_icao != '':
                try:
                    route = AIRPORT_SETTINGS[d_icao][a_icao]['ROUTE']
                except:
                    print((d_icao, a_icao))
                    pass
        
        if len(items_list[item][0]) != 0:
            if route != '':
                output[item].append({
                            'origin':dep_icao,
                            'destination':arr_icao,
                            'aircraft':aircraft,
                            'dep_time':dep_time,
                            'arr_time':arr_time,
                            'route':route
                            })     


    with open('data/output.json', 'w') as file:
        file.write(json.dumps(output, indent=4))
