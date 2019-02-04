#!/usr/bin/env python3
from flask import Flask, render_template, request
from src import get_flights

app = Flask(__name__, template_folder=".")

@app.route("/")
def hello():
                
    return render_template('web/hello.html')

@app.route("/get_flights")
def get_flight_page():
                
    return render_template('web/get_flights.html')

@app.route("/get_flights_result", methods = ['POST'])
def get_flight():
    max_flights = int(request.form['max_flights'])
    flights = get_flights.get_flights(max_flights)
    output = ''

    for item in flights:
        output += '''
            <br>Callsign: {0}
            <br>Origin: {1}
            <br>Destination: {2}
            <br>Aircraft: {3}
            <br>Route: {4}
            <br>Dep Time: {5}
            <br>Arr Time: {6}
            <br>Dep Metar: {7}
            <br>Arr Metar: {8}
            <br><br>
            '''.format(
                    item, 
                    [x for x in flights[item][0][0]['origin'].keys()][0],
                    [x for x in flights[item][0][0]['destination'].keys()][0],
                    flights[item][0][0]['aircraft'],
                    flights[item][0][0]['route'],
                    flights[item][0][0]['dep_time'],
                    flights[item][0][0]['arr_time'],
                    flights[item][0][0]['dep_metar']['Raw-Report'],
                    flights[item][0][0]['arr_metar']['Raw-Report'],
                )
    return output

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')