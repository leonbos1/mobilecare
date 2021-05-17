from datetime import datetime
import requests
import time
import sqlite3

sensor_url = 'http://ronleon.nl/sensordata'
verzorgers_url = 'http://ronleon.nl/users'
login_url = 'http://ronleon.nl/login'


#-----<   Sensor data test
sensor_id = 1
datetime_string = '14/05/2021 14:16:48'
starttime = 1621161849
enddatetime_string = '14/05/2021 14:17:05'
endtime = 1621161866
tag = 'EF9VRF'
activation_duration = round(endtime - starttime)

sensordata = {'sensor_id':sensor_id, 'time_activated':datetime_string, 'time_deactivated':enddatetime_string, 'tag':tag, 'activation_duration':activation_duration}

requests.put(sensor_url, sensordata)

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

last_id = cursor.execute('select max(id) from sensor_time').fetchone()[0]
last_sensordata = cursor.execute(f'select * from sensor_time where id = {last_id}').fetchall()[0]
conn.execute(f'delete from sensor_time where id = {last_id}')
conn.commit()
conn.close()

new_id = last_sensordata[0]
new_sensor_id = last_sensordata[1]
new_time_activated = last_sensordata[2]
new_time_deactivated = last_sensordata[3]
new_tag = last_sensordata[4]
new_activation_duration = last_sensordata[5]

#----->


#-----<   verzorger data test
firstname = 'Anna'
lastname = 'Bakhuizen'
email = 'anna.bakhuizen@gmail.com'
password = 'AnnaBakhuizen@19'
role = 'verzorger'

data = {
    'email': {email},
    'firstname': {firstname},
    'lastname': {lastname},
    'password': {password},
    'role': {role}
}

r1 = requests.put(verzorgers_url, data)

firstname = 'Henk'
lastname = 'Visscher'
email = 'henk.visscher@gmail.com'
password = 'zwakwachtwoord'
role = 'verzorger'

data = {
    'email': {email},
    'firstname': {firstname},
    'lastname': {lastname},
    'password': {password},
    'role': {role}
}

r2 = requests.put(verzorgers_url, data)

firstname = 'Henk'
lastname = 'Visscher'
email = 'dit_is_geen_valide_email@'
password = 'DitIsEENsterkwachtwoord2001!@#'
role = 'verzorger'

data = {
    'email': {email},
    'firstname': {firstname},
    'lastname': {lastname},
    'password': {password},
    'role': {role}
}
r3 = requests.put(verzorgers_url, data)
#----->

passed = True

if last_id != new_id:
    print(f"Id failed, id should be {last_id} but is {new_id}")
    passed = False
if sensor_id != new_sensor_id:
    print(f"Sensor_id failed, sensor_id should be {sensor_id} but is {new_sensor_id}")
    passed = False
if datetime_string != new_time_activated:
    print(f"Time activated failed, time_activated should be {datetime_string} but is {new_time_activated}")
    passed = False
if enddatetime_string != new_time_deactivated:
    print(f"Time deactivated failed, endtime should be {enddatetime_string} but is {new_time_deactivated}")
    passed = False
if tag != new_tag:
    print(f"Tag failed, tag should be {tag} but is {new_tag}")
    passed = False
if activation_duration != new_activation_duration:
    print(f"Activation duration failed, should be {activation_duration} but is {new_activation_duration}")
    passed = False

if r1.status_code == 201:
    print("Verzorger r1 test failed")
    passed = False
if r2.status_code == 201:
    print("Verzorger r2 test failed")
    passed = False
if r3.status_code == 201:
    print("Verzorger r3 test failed")
    passed = False

if passed:
    print("All tests passed succesfully")





