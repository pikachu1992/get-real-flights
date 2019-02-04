#!/usr/bin/env python3
"""
Args:

Returns:

"""
import asyncio
import json
from datetime import datetime
from collections import defaultdict
from src import get_airlines
from src import make_route
import flightradar24

RESULT_LIST = defaultdict(list)

async def get_flights_by_company(company):
    """
    Args:

    Returns:

    """
    try:
        data = flightradar24.Api()
        flights_data = data.get_flights(company)
        
        ignore = ['version', 'total', 'full_count', 'stats']
        for item in flights_data:
            if item not in ignore:
                flight_infos = flights_data[item]
                callsign = flight_infos[16]
                aircraft = flight_infos[8]
                count_exist = len(RESULT_LIST[callsign])
                try:
                    infos = data.get_flight(flight_infos[13])
                    
                    for item in infos['result']['response']['data']:
                        today = datetime.utcnow().strftime("%Y-%m-%d")
                        flightdate = datetime.utcfromtimestamp(item['time']['scheduled']['departure']).strftime('%Y-%m-%d')
                        if flightdate == today and callsign != '':
                            dep_position = defaultdict(list)
                            arr_position = defaultdict(list)
                            dep_icao = item['airport']['origin']['code']['icao']
                            arr_icao = item['airport']['destination']['code']['icao']
                            dep_time = item['time']['scheduled']['departure']
                            arr_time = item['time']['scheduled']['arrival']

                            dep_position[dep_icao].append({
                                        'latitude':item['airport']['origin']['position']['latitude'],
                                        'longitude':item['airport']['origin']['position']['longitude']
                                        })
                            arr_position[arr_icao].append({
                                    'latitude':item['airport']['destination']['position']['latitude'],
                                    'longitude':item['airport']['destination']['position']['longitude']
                                    })

                            if count_exist == 0:                               
                                RESULT_LIST[callsign].append({
                                    'origin':dep_position,
                                    'destination':arr_position,
                                    'aircraft':aircraft,
                                    'dep_time':datetime.utcfromtimestamp(dep_time).strftime('%Y-%m-%d %H:%M'),
                                    'arr_time':datetime.utcfromtimestamp(arr_time).strftime('%Y-%m-%d %H:%M')
                                    })
                            else:
                                RESULT_LIST[callsign].clear()
                                RESULT_LIST[callsign].append({
                                    'origin':dep_position,
                                    'destination':arr_position,
                                    'aircraft':aircraft,
                                    'dep_time':datetime.utcfromtimestamp(dep_time).strftime('%Y-%m-%d %H:%M'),
                                    'arr_time':datetime.utcfromtimestamp(arr_time).strftime('%Y-%m-%d %H:%M')
                                    })
                
                except:
                    pass

    except:
        pass

    return RESULT_LIST

async def main():
    """
    Args:

    Returns:

    """
    
    airlines = ['TAP']
    while True:
        data = get_airlines.get_airlines()
        for item in airlines:
            for airline in data:           
                if item == airline[0]:
                    await get_flights_by_company(item)
        with open('data/flight_radar.json', 'w') as file:
            file.write(json.dumps(RESULT_LIST, indent=4))
        make_route.make_route()
        await asyncio.sleep(5)


def get_start():
    """
    Args:

    Returns:

    """
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

get_start()
