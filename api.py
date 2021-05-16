from flask import Flask, request, make_response, g, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
import os
from werkzeug.security import generate_password_hash, check_password_hash
import re


app = Flask(__name__)
api = Api(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SECRET_KEY'] = 'secretkey'
regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
db = SQLAlchemy(app)

sensor = {}

class SensorTime(db.Model): #door leon
    id =  db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer)
    time_activated = db.Column(db.String)
    time_deactivated = db.Column(db.String)
    tag = db.Column(db.String)
    activation_duration = db.Column(db.Integer)

    def __repr__(self):
        return f"Sensor(id={self.id}, sensor_id={self.sensor_id}, time_activated={self.time_activated}, time_deactivated={self.time_deactivated}, tag={self.tag}, activation_duration={self.activation_duration})"


class Verzorgers(db.Model): #door leon
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)

    def __repr__(self):
        return f'Verzorger(id={self.id}, firstname={self.firstname}, lastname={self.lastname}, email={self.email}, password={self.password})'

#door leon
sensor_put_args = reqparse.RequestParser()
#sensor_put_args.add_argument("id", type=int, help="Dit is het id van de log")
sensor_put_args.add_argument("sensor_id", type=int, help="Dit is het id van de sensor die iets heeft gescand")
sensor_put_args.add_argument("time_activated", type=str, help='Dit is de tijd dat de sensor is geactivate')
sensor_put_args.add_argument("time_deactivated", type=str, help='dit is de tijd dat de sensor is gedeactvate')
sensor_put_args.add_argument("tag", type=str, help='dit is de tag die de sensor heeft gescand')
sensor_put_args.add_argument("activation_duration", type=int, help='dit is de tijd in seconde dat de sensor is geactivate')

verzorger_put_args = reqparse.RequestParser()
verzorger_put_args.add_argument("firstname", type=str, help="dit is de voornaam van een verzorger")
verzorger_put_args.add_argument("lastname", type=str, help='dit is de achternaam van een verzorger')
verzorger_put_args.add_argument("email", type=str, help='dit is de email van een verzorger')
verzorger_put_args.add_argument("password", type=str, help='dit is de password van een verzorger')

verzorger_login_args = reqparse.RequestParser()
verzorger_login_args.add_argument("email", type=str, help='dit is de email van een verzorger')
verzorger_login_args.add_argument("password", type=str, help='dit is de password van een verzorger')

#door leon
sensor_data = {
    'id': fields.Integer,
    'sensor_id': fields.Integer,
    'time_activated': fields.String,
    'time_deactivated': fields.String,
    'tag': fields.String,
    'activation_duration': fields.Integer
}
#door leon
verzorger_data = {
    'id' : fields.Integer,
    'firstname' : fields.String,
    'lastname' : fields.String,
    'email' : fields.String,
    'password' : fields.String
}
#door leon
verzorger_login = {
    'email' : fields.String,
    'password' : fields.String
}
#door leon
class Sensor(Resource):
    @marshal_with(sensor_data)
    def get(self):
        result = SensorTime.query.all()
        return result

    @marshal_with(sensor_data)
    def put(self):
        args = sensor_put_args.parse_args()
        data = SensorTime(sensor_id=args['sensor_id'], time_activated=args['time_activated'], time_deactivated=args['time_deactivated'], tag=args['tag'], activation_duration=args['activation_duration'])
        db.session.add(data)
        db.session.commit()
        return data, 201
#door leon
class Verzorger(Resource):
    @marshal_with(verzorger_data)
    def get(self):
        result = Verzorgers.query.all()
        return result

    @marshal_with(verzorger_data)
    def put(self):
        args = verzorger_put_args.parse_args()
        email = args['email']
        email_result = Verzorgers.query.filter_by(email=email).first()
        if email_result != None:
            abort(401, message = 'Email is already taken')
        if self.check_mail(email) != 'Valid':
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
            

        data = Verzorgers(firstname=args['firstname'], lastname=args['lastname'], email=args['email'], password=generate_password_hash(args['password'], method='sha256'))
        db.session.add(data)
        db.session.commit()
        return data, 201

    def check_mail(self, email):
        if(re.search(regex, email)):
            return 'Valid'
        return 'Invalid'

#door leon
class VerzorgerLogin(Resource):
    @marshal_with(verzorger_login)
    def post(self):
        args = verzorger_login_args.parse_args()
        email = args['email']
        password = args['password']
        print(email, password)
    
api.add_resource(Sensor, "/sensordata/")    
api.add_resource(Verzorger, "/verzorgers/")
api.add_resource(VerzorgerLogin, "/login/")


if __name__ == '__main__':
    app.run(host='192.168.178.69', port=80,debug=True)


