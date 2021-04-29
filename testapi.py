import requests

#url = 'http://127.0.0.1:5000/sensordata/'
#url = 'http://127.0.0.1:5000/verzorgers/'
url = 'http://127.0.0.1:5000/login/'

#data = {'verzorger_id' : 1,'username' : 'testusername','password' : 'testpassword'}

#data = {'verzorger_id' : 1,'username' : 'testusername','password' : 'testpassword'}

data = {
    'email' : 'leonbos@mail.com',
    'password' : 'test123'
}

response = requests.post(url, data)

print(response)