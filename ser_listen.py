# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ser_listen.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mmorel <mmorel@student.42.us.org>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2017/06/27 21:05:28 by mmorel            #+#    #+#              #
#    Updated: 2017/06/27 21:05:29 by mmorel           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sqlite3
import db_func as dbf
from time import time, gmtime, strftime, sleep

def log_data(arr, buff):
	try:
	    arr.append(float(bluff))
	except (RuntimeError, TypeError, NameError):
	    print("Could not convert to float!")
	    continue
	return (arr)

def output_logs(h_arr, t_arr):
	hum_record = dbf.get_db().execute('SELECT humidity FROM humidity ORDER BY time DESC')
	hum_test = hum_record.fetchall()
	hum_record.close()
	f = open('out.txt', 'w')
	f.write("\n\n\n\n Latest Humidity Readings\n\n\n\n")
	f.write(str(hum_test))
	f.write("\n\n\n\n\nValues stored in h_minute_values\n\n\n\n\n")
	f.write(str(h_arr))
	f.write("\n\n\n\n\nValues stored in t_minute_values\n\n\n\n\n")
	f.write(str(t_arr))
	f.close()

def listen(ser):
    time_taken = 0
    min_check = gmtime().tm_min
    test_check = gmtime().tm_min
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
                h_minute_values = log_data(split[0])
                t_minute_values = log_data(split[1])

                print (h_minute_values)
                print (t_minute_values)

                min_check = min_check + 1
                sleep(2)
            # if gmtime().tm_hour == hour_check + 1:
            if gmtime().tm_min == test_check + 5:
                with app.app_context():
                	output_logs(h_minute_values, t_minute_values)
                    db = dbf.get_db()    
                    cur = db.cursor()
                    time_taken = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                    cur.execute('INSERT INTO humidity VALUES (?,?)', (time_taken, hrlyAvg(h_minute_values)))
                    cur.execute('INSERT INTO temperature VALUES (?,?)', (time_taken, hrlyAvg(t_minute_values)))
                    db.commit()
                    h_minute_values = []
                    t_minute_values = []
                    # hour_check = hour_check + 1
                    test_check = test_check + 5
