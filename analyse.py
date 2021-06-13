import requests
import socket
import time
import json

HOST = '127.0.0.1'
PORT = 5000


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


def check_hours(hours):
    """Controleert of de uren op een raar tijdstip zijn
    """
    hours = int(hours)
    if hours > 21:
        return True
    elif hours < 7:
        return True


def check_for_gone(count):
    """controleert of de patient lang de achtertuin uit is
    """
    sensor_id = lastdata['sensor_id']

    #Telt het aantal keer dat sensor gactiveerd is.
    tell = 0
    
    while count > 0:
        count -= 1
        tell += 1
    print(tell)
    
    #Als het getelde aantal op oneven staat, is de patient uit. Anders op in.
    if tell % 2 == 1:
        print("Uit")
    else:
        print("In")

    return check_for_gone(sensor_id)

    
    #hier moet een functie komen die controleert of iemand een lange periode uit de achtertuin is. 
    #sensor 3 is de uitgang van de achtertuin. Als deze dus 1x wordt geactivateerd weet je dat de patient de tuin uit is.
    #Als die weer wordt geactivateerd is de patient weer in de tuin.


def check_for_inactivity():
    """Controleert of iemand lang op 1 plek stil zit. 
    """

    last_data = get_last_sensordata()
    activation_duration = last_data['activation_duration']

    if activation_duration > 20:
        return "Alarm"

    #gebruik hier activation_duration uit de database
    #als dit getal heel groot is gaat er een alarm af


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
    while True:
        
        last_data = get_last_sensor_data()
        patient_id = get_patient_id(last_data)
        time_activated = last_data['time_activated']
        hours = convert_to_hours(time_activated)
        reason = 'geen alarm' #alleen voor debuggen nodig
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
        print(reason) # alleen voor debuggen nodig
        if alarm:
            alarm = True
            patient_id
            reason = 'Er is iets met patient'
            pass# hier moet via sockets verstuurd worden dat er een alarm is. het patient id en de reden moeten dan meegegeven worden.

        
        time.sleep(1)
main()