#!/usr/bin/env python3
from collections import defaultdict
import json
import random

def get_flights(total):
    with open('data/output.json', 'r') as file:
        items = json.loads(file.read())

    flights = defaultdict(list)
    callsigns = []
    for callsign in items:
            callsigns.append(callsign)

    random_callsigns = random.sample(callsigns, len(callsigns))

    for x in range(0, total):
        flights[random_callsigns[x]].append(items[random_callsigns[x]])  

    return flights


    with open('data/final_random_flights.json', 'w') as file:
        file.write(json.dumps(get_flights(1), indent=4))