from functools import wraps
import jwt
from cerberus import Validator
from flask import Flask, request, Response, g, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import os
import re
import bcrypt
import string
import random 
from flask_cors import CORS
from sqlalchemy.orm import backref


app = Flask(__name__)
CORS(app)
api = Api(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SECRET_KEY'] = 'secretkey'
regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
db = SQLAlchemy(app)

sensor = {}

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
        return f"Sensors(id={self.id}, sensor_id={self.sensor_id}, time_activated={self.time_activated}, time_deactivated={self.time_deactivated}, tag={self.tag}, activation_duration={self.activation_duration})"

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
        return f'Patient(id={self.id}, firstname={self.firstname}, lastname={self.lastname}'

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
        return f'Sensors(id={self.id}, name={self.name}, patient_id={self.patient_id})'

class Tags(db.Model):
    """Model van tabel van de tags
    """
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    sensor_data = db.relationship('SensorData', backref = 'SensorData_Tags')
    
    def __repr__(self):
        return f'Tags(id={self.id}, tag={self.tag}, patient_id={self.patient_id})'

def token_required(f):
    """Decorator die de token van de user checkt
    """
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            abort(401)

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = Users.query.filter_by(public_id=data['public_id']).first()
        except:
            abort(401)

        return f(current_user, *args, **kwargs)
    return decorator


def admin_required(f):
    """Decorator die checkt of de user een admin is
    """
    @wraps(f)
    @token_required
    def check_admin(current_user, *args, **kwargs):
        if current_user.role == 'admin':
            pass
        else:
            abort(401)
        return f(*args, **kwargs)

    return check_admin

sensor_put_args = reqparse.RequestParser()
#sensor_put_args.add_argument("id", type=int, help="Dit is het id van de log")
sensor_put_args.add_argument("sensor_id", type=int, help="Dit is het id van de sensor die iets heeft gescand")
sensor_put_args.add_argument("time_activated", type=str, help='Dit is de tijd dat de sensor is geactivate')
sensor_put_args.add_argument("time_deactivated", type=str, help='dit is de tijd dat de sensor is gedeactvate')
sensor_put_args.add_argument("tag", type=str, help='dit is de tag die de sensor heeft gescand')
sensor_put_args.add_argument("activation_duration", type=int, help='dit is de tijd in seconde dat de sensor is geactivate')

user_post_args = reqparse.RequestParser()
user_post_args.add_argument("firstname", type=str, help="dit is de voornaam van een gebruiker")
user_post_args.add_argument("lastname", type=str, help='dit is de achternaam van een gebruiker')
user_post_args.add_argument("email", type=str, help='dit is de email van een gebruiker')
user_post_args.add_argument("password", type=str, help='dit is de password van een gebruiker')

patient_post_args = reqparse.RequestParser()
patient_post_args.add_argument("firstname", type=str, help="dit is de voornaam van een patient")
patient_post_args.add_argument("lastname", type=str, help='dit is de achternaam van een patient')

user_login_args = reqparse.RequestParser()
user_login_args.add_argument("email", type=str, help='dit is de email van een gebruiker')
user_login_args.add_argument("password", type=str, help='dit is de password van een gebruiker')


sensor_data = {
    'id': fields.Integer,
    'sensor_id': fields.Integer,
    'time_activated': fields.String,
    'time_deactivated': fields.String,
    'tag': fields.String,
    'activation_duration': fields.Integer
}

sensors_data = {
    'id': fields.Integer,
    'name': fields.String,
    'patient_id' : fields.Integer
}

tag_data = {
    'id': fields.Integer,
    'tag': fields.String,
    'patient_id' : fields.Integer
}

user_data = {
    'id': fields.Integer,
    'public_id': fields.String,
    'firstname': fields.String,
    'lastname': fields.String,
    'email': fields.String,
    'password': fields.String,
    'role': fields.String
}
patient_data = {
    'id': fields.Integer,
    'firstname': fields.String,
    'lastname': fields.String
}

patient_verzorger_data = {
    'id': fields.Integer,
    'firstname': fields.String,
    'lastname': fields.String
}

user_login = {
    'email': fields.String,
    'password': fields.String
}

class SensorsData(Resource):
    """Class voor het handelen van sensordata requests
    """
    @marshal_with(sensor_data)
    def get(self):
        result = SensorData.query.all()
        return result

    @marshal_with(sensor_data)
    def put(self):
        args = sensor_put_args.parse_args()
        data = SensorData(sensor_id=args['sensor_id'], time_activated=args['time_activated'], time_deactivated=args['time_deactivated'], tag=args['tag'], activation_duration=args['activation_duration'])
        db.session.add(data)
        db.session.commit()
        return data, 201


class User(Resource):
    """Class voor het handelen van user requests
    """
    def __init__(self):
        schema = {
            'id' : {'required': False, 'type':'integer'},
            'email': {'required': True, 'type': 'string'},
            'firstname': {'required': True, 'type': 'string'},
            'lastname': {'required': True, 'type': 'string'},
            'password': {'required': True, 'type': 'string'},
            'role': {'required': True, 'type': 'string'}
        }
        self.v = Validator(schema)

    @marshal_with(user_data)
    @token_required
    @admin_required
    def get(self, current_user):
        result = Users.query.all()
        return result

    @token_required
    @admin_required
    def post(self, current_user):
        args = request.get_json(force=True)
        if current_user.v.validate(args):
            email = args['email']
            email_result = Users.query.filter_by(email=email).first()
            if email_result != None:
                abort(401, message = 'Email is already taken')
            if current_user.check_mail(email) != 'Valid':
                abort(401, message = 'Invalid email')

            password = args['password']
            if len(password) < 10:
                abort(401, message = 'Password is too short')
            weird_char = False
            number = False
            hoofdletter = False
            for element in password:
                if element in '~!@#$%^&*()_+=-,.<>/?;:"':
                    weird_char = True
                if element in '0123456789':
                    number = True
                if element in 'QWERTYUIOPASDFGHJKLZXCVBNM':
                    hoofdletter = True
            if not weird_char or not number or not hoofdletter:
                abort(401, message = 'Password does not meet security requirements')

            data = Users(
                public_id=current_user.id_generator(80),
                firstname=args['firstname'],
                lastname=args['lastname'],
                email=args['email'],
                password=bcrypt.hashpw(args['password'].encode('utf-8'), salt=bcrypt.gensalt()),
                role=args['role']
            )
            db.session.add(data)
            db.session.commit()
            return Response(data, 201)
        else:
            return Response('missing fields', 400)

    @token_required
    @admin_required
    def delete(self, current_user):
        args = request.get_json(force=True)
        user_id = args['id']
        result = Users.query.filter_by(id=user_id).first()
        if result != None:
            db.session.delete(result)
            db.session.commit()
            return Response(result,201)
        return Response('Dit id is niet geldig', 401)

    def check_mail(self, email):
        if(re.search(regex, email)):
            return 'Valid'
        return 'Invalid'

    def id_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

class Patient(Resource):
    """Class voor het handelen van patients requests
    """
    def __init__(self):
        schema = {
            'id' : {'required': False, 'type':'integer'},
            'firstname': {'required': True, 'type': 'string'},
            'lastname': {'required': True, 'type': 'string'}
        }
        self.v = Validator(schema)

    @marshal_with(patient_data)
    @token_required
    @admin_required
    def get(self, current_user):
        result = Patients.query.all()
        return result

    @token_required
    @admin_required
    def post(self, current_user):
        args = request.get_json(force=True)
        if current_user.v.validate(args):
            firstname = args['firstname']
            lastname = args['lastname']
            result = Patients.query.filter_by(firstname=firstname).first()
            if result != None:
                result = Patients.query.filter_by(lastname=lastname).first()
                if result != None:
                    return Response('Patient already added',401)
            data = Patients(firstname=args['firstname'], lastname=args['lastname'])
            db.session.add(data)
            db.session.commit()
            return Response(data, 201)
        else:
            return Response('missing fields', 400)
    
    @token_required
    @admin_required
    def delete(self, current_user):
        args = request.get_json(force=True)
        patient_id = args['id']
        result = Patients.query.filter_by(id=patient_id).first()
        if result != None:
            db.session.delete(result)
            db.session.commit()
            return Response(result,201)
        return Response('Dit id is niet geldig', 401)

class PatientVerzorgers(Resource):
    """Class voor het handelen van verzorger patient koppel requests
    """
    def __init__(self):
        schema = {
            'id': {'required': False, 'type': 'integer'},
            'patient_id': {'required': True, 'type': 'integer'},
            'verzorger_id': {'required': True, 'type': 'integer'}
        }
        self.v = Validator(schema)

    @marshal_with(patient_verzorger_data)
    @token_required
    @admin_required
    def get(self, current_user):
        result = PatientVerzorger.query.all()
        return result

    @token_required
    @admin_required
    def post(self, current_user):
        args = request.get_json(force=True)
        if current_user.v.validate(args):
            patient_id = args['patient_id']
            verzorger_id = args['verzorger_id']
            result = PatientVerzorger.query.filter_by(patient_id=patient_id).first()
            if result != None:
                result = PatientVerzorger.query.filter_by(verzorger_id=verzorger_id).first()
                if result != None:
                    return Response('Patient is al gekoppeld met verzorger',401)
            data = PatientVerzorger(patient_id=args['patient_id'], verzorger_id=args['verzorger_id'])
            db.session.add(data)
            db.session.commit()
            return Response(data, 201)
        else:
            return Response('missing fields', 400)

    @token_required
    @admin_required
    def delete(self, current_user):
        args = request.get_json(force=True)
        tag_id = args['id']
        result = PatientVerzorgers.query.filter_by(id=tag_id).first()
        if result != None:
            db.session.delete(result)
            db.session.commit()
            return Response(result,201)
        return Response('Dit id is niet geldig', 401)

class Sensor(Resource):
    """Class voor het handelen van sensor requests
    """
    def __init__(self):
        schema = {
            'id' : {'required': False, 'type':'integer'},
            'name': {'required': True, 'type': 'string'},
            'patient_id': {'required': True, 'type': 'integer'}
        }
        self.v = Validator(schema)

    @marshal_with(sensors_data)
    @token_required
    @admin_required
    def get(self, current_user):
        result = Sensors.query.all()
        return result

    @token_required
    @admin_required
    def post(self, current_user):
        args = request.get_json(force=True)
        if current_user.v.validate(args):
            name = args['name']
            patient_id = args['patient_id']
            result = Sensors.query.filter_by(name=name).first()
            if result != None:
                result = Sensors.query.filter_by(patient_id=patient_id).first()
                if result != None:
                    return Response('Patient is al gekoppeld met sensor',401)
            data = Sensors(name=args['name'], patient_id=args['patient_id'])
            db.session.add(data)
            db.session.commit()
            return Response(data, 201)
        else:
            return Response('missing fields', 400)

    @token_required
    @admin_required
    def delete(self, current_user):
        args = request.get_json(force=True)
        sensor_id = args['id']
        result = Sensors.query.filter_by(id=sensor_id).first()
        if result != None:
            db.session.delete(result)
            db.session.commit()
            return Response(result,201)
        return Response('Dit id is niet geldig', 401)

class Tag(Resource):
    """Class voor het handelen van tag requests
    """
    def __init__(self):
        schema = {
            'id': {'required': False, 'type': 'integer'},
            'tag': {'required': True, 'type': 'string'},
            'patient_id': {'required': True, 'type': 'integer'}
        }
        self.v = Validator(schema)

    @marshal_with(tag_data)
    @token_required
    @admin_required
    def get(self, current_user):
        result = Tags.query.all()
        return result

    @token_required
    @admin_required
    def post(self, current_user):
        args = request.get_json(force=True)
        if current_user.v.validate(args):
            tag = args['tag']
            patient_id = args['patient_id']
            result = Tags.query.filter_by(tag=tag).first()
            if result != None:
                result = Tags.query.filter_by(patient_id=patient_id).first()
                if result != None:
                    return Response('Patient is al gekoppeld met tag',401)
            data = Tags(tag=args['tag'], patient_id=args['patient_id'])
            db.session.add(data)
            db.session.commit()
            return Response(data, 201)
        else:
            return Response('missing fields', 400)

    @token_required
    @admin_required
    def delete(self, current_user):
        args = request.get_json(force=True)
        tag_id = args['id']
        result = Tags.query.filter_by(id=tag_id).first()
        if result != None:
            db.session.delete(result)
            db.session.commit()
            return Response(result,201)
        return Response('Dit id is niet geldig', 401)

class UserLogin(Resource):
    """Class voor het handelen van login requests
    """
    def __init__(self):
        self.schema = {'email': {'required': True, 'type': 'string'}, 'password': {'required': True, 'type': 'string'}}
        self.v = Validator(self.schema)

    def post(self):
        args = request.get_json(force=True)

        if self.v.validate(args):
            email = args['email']
            password = args['password']
            user = Users.query.filter(Users.email == email).first()
            if user:
                if bcrypt.checkpw(password.encode('utf-8'), user.password):
                    token = jwt.encode({'public_id': user.public_id}, app.config['SECRET_KEY'], algorithm='HS256')
                    return jsonify({'token': token, 'user': user.encode()})
                else:
                    return Response('invalid combination', status=400)
            else:
                return Response('invalid combination', status=400)
        else:
            return Response('missing fields', status=400)
    
api.add_resource(SensorsData, "/sensordata")
api.add_resource(User, "/users")
api.add_resource(UserLogin, "/login")
api.add_resource(Patient, "/patients")
api.add_resource(PatientVerzorgers, "/patientverzorger")
api.add_resource(Sensor, "/sensor")
api.add_resource(Tag, "/tag")

if __name__ == '__main__':
    app.run(host='192.168.178.69', port=80, debug=True)


