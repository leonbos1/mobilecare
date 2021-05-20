from datetime import datetime
import requests
import time
import sqlite3

sensor_url = 'http://ronleon.nl/sensordata'
verzorgers_url = 'http://ronleon.nl/users'
login_url = 'http://ronleon.nl/login'
patient_url = 'http://ronleon.nl/patients'

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

email = 'admin@test.nl'
password = 'Password123!'

admin_data = {
            'email': email, 
            'password':password
            }

admin = requests.post(login_url, json = admin_data)


try:
    response = admin.json()
    token = response['token']
except:
    token = 'invalid token'


headers = {'x-access-tokens':token}
wrong_headers = {'x-access-tokens':'sdagfw424tg425'}


#------< Patient data tests
#tag already used
patient1_data = {
            'firstname': 'Bart',
            'lastname': 'Klaassen',
            'tag' : '21BCA31C',
            'verzorger_id' : 1,
            'sensor_1': 1,
            'sensor_2': 2,
            'sensor_3': 3,
            'sensor_4': 4
        }

patient1 = requests.post(patient_url, json=patient1_data, headers=headers)


#unauthorized
patient2_data = {
            'firstname': 'Geert',
            'lastname': 'Van Der Meer',
            'tag' : '46FCF1XC',
            'verzorger_id' : 1,
            'sensor_1': 5,
            'sensor_2': 6,
            'sensor_3': 7,
            'sensor_4': 8
        }

patient2 = requests.post(patient_url, json=patient2_data, headers=wrong_headers)

#------>

#-----<   verzorger data test
#user already created
firstname = 'Anna'
lastname = 'Bakhuizen'
email = 'anna.bakhuizen@gmail.com'
password = 'AnnaBakhuizen@19'
role = 'verzorger'

verzorger_data = {
            'email': email,
            'firstname': firstname,
            'lastname': lastname,
            'password': password,
            'role': role
        }

r1 = requests.post(verzorgers_url, json = verzorger_data, headers=headers)

#weak password
firstname = 'Henk'
lastname = 'Visscher'
email = 'henk.visscher@gmail.com'
password = 'zwakwachtwoord'
role = 'verzorger'

verzorger_data = {
            'email': email,
            'firstname': firstname,
            'lastname': lastname,
            'password': password,
            'role': role
        }


r2 = requests.post(verzorgers_url, json = verzorger_data, headers=headers)

#invalid email
firstname = 'Henk'
lastname = 'Visscher'
email = 'dit_is_geen_valide_email@'
password = 'DitIsEENsterkwachtwoord2001!@#'
role = 'verzorger'

verzorger_data = {
            'email': email,
            'firstname': firstname,
            'lastname': lastname,
            'password': password,
            'role': role
        }

r3 = requests.post(verzorgers_url, json = verzorger_data, headers=headers)

#email already used
firstname = 'Henk'
lastname = 'Visscher'
email = 'testmail@mail.com'
password = 'DitIsEENsterkwachtwoord2001!@#'
role = 'verzorger'

verzorger_data = {
            'email': email,
            'firstname': firstname,
            'lastname': lastname,
            'password': password,
            'role': role
        }

r4 = requests.post(verzorgers_url, json = verzorger_data, headers=headers)

#unauthorized
firstname = 'Henk'
lastname = 'Visscher'
email = 'henkvisscher@mail.com'
password = 'DitIsEENsterkwachtwoord2001!@#'
role = 'verzorger'

verzorger_data = {
            'email': email,
            'firstname': firstname,
            'lastname': lastname,
            'password': password,
            'role': role
        }

r5 = requests.post(verzorgers_url, json = verzorger_data, headers=wrong_headers)


#----->


#------<   Login tests

email = 'admin@test.nl'
password = 'DitWachtwoordKloptNiet'

login1_data = {
    'email':email,
    'password':password
}

login1 = requests.post(login_url, json = login1_data, headers=headers)

email = 'invalid@email.nl'
password = 'aaaaaa'


login2_data = {
    'email':email,
    'password':password
}

login2 = requests.post(login_url, json = login2_data, headers=headers)

email = 'admin@test.nl'
password = "xxx') OR 1 = 1 -- ]"

login3_data = {
    'email':email,
    'password':password
}

login3 = requests.post(login_url, json = login2_data, headers=headers)

#------>
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
if r4.status_code == 201:
    print("Verzorger r4 test failed")
    passed = False
if r4.status_code == 201:
    print("Verzorger r5 test failed")
    passed = False

if login1.text != 'invalid password':
    print("login1 test failed")
    passed = False

if login2.text != 'invalid combination':
    print('login2 test failed')
    passed = False

if login3.text != 'invalid combination':
    print('login3 test failed')
    passed = False

if patient1.text != 'Tag already used':
    print('Patient1 test failed')
    passed = False

if patient2.status_code == 201:
    print("Patient2 test failed")
    passed = False

if passed:
    print("All tests passed succesfully")





