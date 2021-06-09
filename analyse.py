import requests
import socket
import time
import json

def get_last_sensor_data():
    """Haalt de laatste sensordata vanuit de api
    """
    url = 'http://ronleon.nl/sensordata'
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

def check_hours(hours):
    """Controleert of de uren op een raar tijdstip zijn
    """
    hours = int(hours)
    if hours > 21:
        return True
    elif hours < 7:
        return True

def check_for_gone():
    """controleert of de patient de achtertuin uit is
    """
    pass

def get_patient(lastdata):
    """Accepts sensor data en geeft patient_id die bij deze data hoort
    """
    url = 'http://ronleon.nl/sensor'
    login = 'http://ronleon.nl/login'
    loginjson =  {'email': 'admin@test.nl','password':'Wachtwoord123!'}
    login_response = requests.post(url=login, json=loginjson)

    try:
        response = login_response.json()
        token = response['token']
    except:
        token = 'invalid token'

    headers = {'x-access-tokens':token}
    response = requests.get(url, headers=headers)

    text = response.text
    sensor_id = lastdata['sensor_id']
    d = json.loads(text)
    for i in d:
        if i['id'] == sensor_id:
            patient_id = i['patient_id']
    return patient_id

def main():
    while True:
        
        last_data = get_last_sensor_data()
        patient_id = get_patient(last_data)
        time_activated = last_data['time_activated']
        hours = convert_to_hours(time_activated)

        if check_hours(hours):
            alarm = True

        if alarm:
            pass# hier moet iets met sockets gebeuren om het alarm te versturen
        time.sleep(1)
main()