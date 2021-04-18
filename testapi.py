import requests

#url = 'http://127.0.0.1:5000/sensordata/'
#url = 'http://127.0.0.1:5000/verzorgers/'
url = 'http://127.0.0.1:5000/verzorgercredentials/'

#data = {'verzorger_id' : 1,'username' : 'testusername','password' : 'testpassword'}

#data = {'verzorger_id' : 1,'username' : 'testusername','password' : 'testpassword'}

data = {
    'verzorger_id' : 1,
    'username' : 'testusername',
    'password' : 'testpassword'
}

response = requests.put(url, data)

print(response.json())