import requests

url = 'http://127.0.0.1:5000/sensordata/'


data = {
    "sensor_id": 2,
    "time_activated": "14/04/2021 13:43:11",
    "time_deactivated": "14/04/2021 13:43:19",
    "tag": "1BBD2EE2 ",
    "activation_duration": 4
}

response = requests.put(url, data)

#print(response.json())