import threading
import eventlet
import serial
import subprocess
import os
import sys
import sqlite3
import plotly
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go

eventlet.monkey_patch()

from flask import Flask, render_template, jsonify, g
from flask_socketio import SocketIO, send, emit
from time import time, gmtime, strftime, sleep

app = Flask(__name__)
fieldnames = ['temperature', 'humidity', 'time']
data = []
output_logs = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "output.logs"
)

DATABASE = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "sensor_data.db"
)

def get_db():
    # with app.app_context():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        print ('Connection established')
    return db

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as file:
            db.cursor().executescript(file.read())
        db.commit()

def listen():
    global ser, data_file
    temp = 0
    hum = 0
    time_taken = []
    min_check = gmtime().tm_min
    hour_check = gmtime().tm_hour
    t_minute_values = []
    h_minute_values = []
    if ser:
        while True:
            if gmtime().tm_min == min_check + 1:
                read_serial = ser.readline()
                read_serial = read_serial.decode("utf-8")
                print("Read serial data")
                print(read_serial)
                split = read_serial.split(',');
                try:
                    h_minute_values.append(float(split[0]))
                    # time_taken.append(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
                except (RuntimeError, TypeError, NameError):
                    print("Could not convert to float!")
                    continue
                try:
                    t_minute_values.append(float(split[1]))
                except (RuntimeError, TypeError, NameError):
                    print("Could not convert to float!")
                    continue
                print (h_minute_values)
                print (t_minute_values)
                min_check = min_check + 1
                sleep(2)
            if gmtime().tm_hour == hour_check + 1:
                hum = hrlyAvg(h_minute_values)
                temp = hrlyAvg(t_minute_values)
                with app.app_context():

                    #Code below for debugging purposes
                    hum_record = get_db().execute('SELECT humidity FROM humidity ORDER BY time DESC')
                    hum_test = hum_record.fetchall()
                    hum_record.close()
                    f = open('out.txt', 'w')
                    f.write("\n\n\n\n Latest Humidity Readings")
                    f.write(str(hum_test))
                    #Code above for debugging purposes

                    db = get_db()    
                    cur = db.cursor()
	            #Code below for debugging purposes
                    f.write("\n\n\n\n\nValues stored in h_minute_values")
                    f.write(str(h_minute_values))
                    f.write("\n\n\n\n\nValues stored in t_minute_values")
                    f.write(str(t_minute_values))
                    f.close()
                    #Code above for debugging purposes

                    time_taken = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                    cur.execute('INSERT INTO humidity VALUES (?,?)', (time_taken, hum))
                    cur.execute('INSERT INTO temperature VALUES (?,?)', (time_taken, temp))
                    db.commit()
                    h_minute_values = []
                    t_minute_values = []
                    hour_check = hour_check + 1

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/data")
def dataPi():
    temp = 0
    hum = 0
    time_taken = 0
    while True:
         read_serial = ser.readline()
         print(read_serial)
         split = read_serial.split(',');
         try:
             hum = float(split[0])
         except (RuntimeError, TypeError, NameError):
             print("Could not convert to float!")
             continue
         try:
              temp = float(split[1])
         except:
             print("Could not convert to float!")
             continue
         time_taken = strftime("%H:%M:%S %m-%d-%Y")
         break
    return render_template('data.html', humidity=hum, temperature=temp, time_taken=time_taken)

@app.route("/sensor_data")
def graphDisplay():
    return render_template("sensor_data.html", h_graph=populateHumGraph())

def populateHumGraph():
    conn = get_db()
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("select humidity from humidity where strftime('%d', time) > '25' and strftime('%d', time) < '31'")
    hum_data = c.fetchall()
    hum = []
    for member in hum_data:
        hum.append(member[0])
    c.execute("select strftime('%m-%d %H:%M', time) from humidity where strftime('%d', time) > '25' and strftime('%d', time) < '31'")
    hum_time = c.fetchall()
    c.close()
    time = []
    for member in hum_time:
        time.append(member[0])
    trace_hum = go.Scatter(
                    x=time,
                    y=hum,
                    name = "Humidity",
                    line = dict(color = '#17BECF'),
                    opacity = 0.8)
    data = [trace_hum]
    layout = dict(
        title = "Humidity History",
        xaxis = dict(
            range = ['2017-06-23','2017-06-30'],
            autotick = False,
            tick0 = 0,
            dtick = 6
            )
    )
    fig = dict(data=data, layout=layout)
    h_graph = plotly.offline.plot(fig, show_link=False, filename="humidity_graph.html", output_type='div', auto_open=False)
    return (h_graph)

def hrlyAvg(data):
    sum = 0
    for entry in data:
        sum += entry
    return sum / len(data)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        print ('Closing Connection')
        db.close()

dev = False
ser = False
try:
    dev = subprocess.check_output('ls /dev/ttyACM*', shell=True).decode('utf-8')
    print(dev)
    ser = serial.Serial(dev.strip(), 9600)
except:
    print("Couldn't find any devices.")

eventlet.spawn(listen)

if __name__ == "__main__":
    if not DATABASE:
        print('Initializing db')
        init_db()
    print('Starting app')
    app.run(debug=True)
