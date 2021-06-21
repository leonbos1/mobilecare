import requests
import socket
import time
import json
from datetime import datetime


HOST = '127.0.0.1'
PORT = 4000

left_garden = False
last_sensor_id = 0

def get_last_sensor_data():
    """Haalt de laatste sensordata vanuit de api
    """
    url = 'http://127.0.0.1:5000/sensordata'
    data = requests.get(url=url)
    text = data.text
    d = json.loads(text)
    max_id = 0
    for i in d:
        if i['id'] > max_id:
            max_id = i['id']-1

    return d[max_id]
    

def convert_to_hours(datetime):
    """Accept een datetime string en convert dit naar hele uren
    """
    return datetime[11:13]


def convert_to_unix(datetimestring):
    """accepts een datetime string en convert naar unix
    """
    format = "%d/%m/%Y %H:%M:%S"
    datetime_unix = datetime.strptime(datetimestring, format)
    unix_time = datetime.timestamp(datetime_unix)*1000
    return unix_time


def check_hours(hours):
    """Controleert of de uren op een raar tijdstip zijn
    """
    hours = int(hours)
    if hours > 21:
        return True
    elif hours < 7:
        return True

def check_for_gone():
    """controleert of de patient lang de achtertuin uit is
    """
    last_data = get_last_sensor_data()
    sensor_id = last_data['sensor_id']

    unix_time_activated = convert_to_unix(last_data['time_activated'])
    now = datetime.now()
    time_now = now.strftime("%d/%m/%Y %H:%M:%S")
    unix_time_now = convert_to_unix(time_now)
    time_difference = unix_time_now - unix_time_activated
    
    if sensor_id ==3 and time_difference > 2000000:
        return True

    
def check_for_inactivity():
    """Controleert of iemand lang op 1 plek stil zit. 
    """

    last_data = get_last_sensor_data()
    activation_duration = last_data['activation_duration']

    if activation_duration > 1600:
        return True 


def admin_login():
    """functie om in te loggen als admin op de api
    """
    login = 'http://127.0.0.1:5000/login'
    loginjson =  {'email': 'admin@test.nl','password':'Wachtwoord123!'}
    login_response = requests.post(url=login, json=loginjson)

    try:
        response = login_response.json()
        token = response['token']
    except:
        token = 'invalid token'

    headers = {'x-access-tokens':token}
    return headers


def get_patient_id(lastdata):
    """Accepts sensor data en geeft patient_id die bij deze data hoort
    """
    url = 'http://127.0.0.1:5000/sensor'

    response = requests.get(url, headers=admin_login()) #headers zijn nodig omdat alleen admins patienten mogen opvragen

    text = response.text
    sensor_id = lastdata['sensor_id']
    d = json.loads(text)
    for i in d:
        if i['id'] == sensor_id:
            patient_id = i['patient_id']
    return patient_id


def main():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')
    s.connect((HOST, PORT))
    print('Connection made')

    while True:
        last_data = get_last_sensor_data()
        patient_id = get_patient_id(last_data)
        time_activated = last_data['time_activated']
        hours = convert_to_hours(time_activated)
        reason = 'geen alarm'
        alarm = False

        if check_hours(hours):
            alarm = True
            reason = 'Activated tussen 22:00 en 06:00'

        elif check_for_gone():
            alarm = True
            reason = 'patient is een lange tijd uit de achtertuin'

        elif check_for_inactivity():
            alarm = True
            reason = 'patient zit heel lang op 1 plek'

        if alarm:
            data = {'patient_id':patient_id,
                    'reason': reason}
            json_data = json.dumps(data)
            s.send(bytes(json_data, "utf-8"))
            print(f'send {json_data}')
        time.sleep(1)

main()