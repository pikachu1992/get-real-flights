#!/usr/bin/env python3
from collections import defaultdict
import requests

def get_metar(icao):
    resp = requests.get('/'.join(['https://avwx.rest/api/metar', icao]))
    metar = resp.json()

    return metar