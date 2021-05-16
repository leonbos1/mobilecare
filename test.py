from datetime import datetime
import requests
import time
import sqlite3

sensor_url = 'http://ronleon.nl/sensordata/'
verzorgers_url = 'http://ronleon.nl/verzorgers/'
login_url = 'http://ronleon.nl/login/'

#data = {'verzorger_id' : 1, 'username' : 'testusername', 'password' : 'testpassword'}

#data = {    'email' : 'leonbos@mail.com',    'password' : 'test123'}

#response = requests.post(url, data)


sensor_id = 1
datetime_string = '14/05/2021 14:16:48'
starttime = 1621161849
enddatetime_string = '14/05/2021 14:17:05'
endtime = 1621161866
tag = 'EF9VRF'
activation_duration = round(endtime - starttime)

data = {'sensor_id':sensor_id, 'time_activated':datetime_string, 'time_deactivated':enddatetime_string, 'tag':tag, 'activation_duration':activation_duration}

#requests.put(sensor_url, data)

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

last_id = cursor.execute('select max(id) from sensor_time').fetchone()[0]
last_sensordata = cursor.execute(f'select * from sensor_time where id = {last_id}').fetchall()[0]
conn.close()

print(last_sensordata)

new_id = last_sensordata[0]
new_sensor_id = last_sensordata[1]
new_time_activated = last_sensordata[2]
new_time_deactivated = last_sensordata[3]
new_tag = last_sensordata[4]
new_activation_duration = last_sensordata[5]


assert last_id == new_id
assert sensor_id == new_sensor_id
assert datetime_string == new_time_activated
assert enddatetime_string == new_time_deactivated
assert tag == new_tag
assert activation_duration == new_activation_duration






