import asyncio
import json
import os
import sched, time
import websockets
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

s = sched.scheduler(time.time, time.sleep)


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SECRET_KEY'] = 'secretkey'
regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
db = SQLAlchemy(app)

class SensorData(db.Model):
    """Model voor de tabel van sensordata
    """
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensors.id'))
    time_activated = db.Column(db.String)
    time_deactivated = db.Column(db.String)
    tag = db.Column(db.Integer, db.ForeignKey('tags.id'))
    activation_duration = db.Column(db.Integer)

    def __repr__(self):
        return f"Sensors(id={self.id}, sensorId={self.sensor_id}, timeActivated={self.time_activated}, timeDeactivated={self.time_deactivated}, tag={self.tag}, activationDuration={self.activation_duration})"

class Users(db.Model):
    """Model voor de tabel van users
    """
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    role = db.Column(db.String)
    patient_verzorger = db.relationship('PatientVerzorger', backref = 'PatientVerzorger_Users')

    def __repr__(self):
        return f'Gebruiker(id={self.id}, public_id={self.public_id}, firstname={self.firstname}, lastname={self.lastname}, email={self.email}, password={self.password}), role={self.role}'

    def encode(self):
        return {
            'id': self.id,
            'publicId': self.public_id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'role': self.role
        }

class Patients(db.Model):
    """Model van tabel van patienten
    """
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    patient_verzorger = db.relationship('PatientVerzorger', backref = 'PatientVerzorger_Patients')
    sensors = db.relationship('Sensors', backref = 'Sensors_Patients')
    tags = db.relationship('Tags', backref = 'Tags_Patients')

    def __repr__(self):
        return f'Patient(id={self.id}, firstname={self.firstname}, lastname={self.lastname}, sensors={self.sensors})'

    def encode(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'patientNurse': self.patient_verzorger,
            'sensors': self.sensors,
            'tags': self.tags,
        }


class PatientVerzorger(db.Model):
    """Model van koppeltabel tussen patienten en verzorgers
    """
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    verzorger_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'PatientVerzorger(id={self.id}, patient_id={self.patient_id}, verzorger_id={self.verzorger_id}'

class Sensors(db.Model):
    """Model van tabel van de sensoren
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    sensor_data = db.relationship('SensorData', backref = 'SensorData_Sensors')

    def __repr__(self):
        return f'Sensors(id={self.id}, name={self.name}, patient_id={self.patient_id}, sensor_data={self.sensor_data})'

class Tags(db.Model):
    """Model van tabel van de tags
    """
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    sensor_data = db.relationship('SensorData', backref = 'SensorData_Tags')

    def __repr__(self):
        return f'Tags(id={self.id}, tag={self.tag}, patient_id={self.patient_id})'


def check_for_anomaly(sc):
    patients = Patients.query.all()

    for patient in patients:
        all_sensors = []
        for sensor in patient.sensors:
            data = sensor.sensor_data

            sorted_data = sorted(data, key=lambda x: datetime.strptime(x.time_activated, '%d/%m/%Y %H:%M:%S'))[::-1]
            obj = {
                'sensor': sensor.name,
                'data': sorted_data[0]
            }
            all_sensors.append(obj)


        sorted_sensors = sorted(all_sensors, key=lambda x: datetime.strptime(x['data'].time_activated, '%d/%m/%Y %H:%M:%S'))[::-1]

        if len(sorted_sensors) > 0:
            sensor = sorted_sensors[0]
            if sensor['sensor'].lower() == 'uitgang' \
                or sensor['sensor'].lower() == 'deur' \
                   or sensor['sensor'].lower() == 'voordeur' \
                    or sensor['sensor'].lower() == 'achterdeur':
                if sensor['data'].activation_duration > 180:
                    nursesIds = []

                    for nurse in patient.patient_verzorger:
                        nursesIds.append(str(nurse.verzorger_id))

                    obj = {
                        "patient_name": f"{patient.firstname} {patient.lastname}",
                        "nurses":  nursesIds
                    }
                    asyncio.get_event_loop().run_until_complete(connect_websocket(json.dumps(obj)))
            else:
                time_deactivated = datetime.strptime(sensor['data'].time_deactivated, '%d/%m/%Y %H:%M:%S')

                diff = datetime.now() - time_deactivated

                if (diff.seconds / 60) > 10:
                    nursesIds = []

                    for nurse in patient.patient_verzorger:
                        nursesIds.append(str(nurse.verzorger_id))

                    obj = {
                        "patient_name": f"{patient.firstname} {patient.lastname}",
                        "nurses":  nursesIds
                    }
                    asyncio.get_event_loop().run_until_complete(connect_websocket(json.dumps(obj)))
    s.enter(10, 1, check_for_anomaly, (sc,))


async def connect_websocket(data = None):
    uri = 'ws://127.0.0.1:4000/server'
    if data != None:
        async with websockets.connect(uri) as websocket:
            await websocket.send(data)

asyncio.get_event_loop().run_until_complete(connect_websocket())

s.enter(10, 1, check_for_anomaly, (s,))
s.run()
