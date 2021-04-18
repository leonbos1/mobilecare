from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
api = Api(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)

sensor = {}

class SensorTime(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer)
    time_activated = db.Column(db.String)
    time_deactivated = db.Column(db.String)
    tag = db.Column(db.String)
    activation_duration = db.Column(db.Integer)

    def __repr__(self):
        return f"Sensor(id={id}, sensor_id={sensor_id}, time_activated={time_activated}, time_deactivated={time_deactivated}, tag={tag}, activation_duration={activation_duration})"

class Verzorgers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    email = db.Column(db.String)

    def __repr__(self):
        return f'Verzorger(id={id}, firstname={firstname}, lastname={lastname}, email={email}'

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


sensor_data = {
    'id': fields.Integer,
    'sensor_id': fields.Integer,
    'time_activated': fields.String,
    'time_deactivated': fields.String,
    'tag': fields.String,
    'activation_duration': fields.Integer
}

verzorger_data = {
    'id' : fields.Integer,
    'firstname' : fields.String,
    'lastname' : fields.String,
    'email' : fields.String
}

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


class Verzorger(Resource):
    @marshal_with(verzorger_data)
    def get(self):
        result = Verzorgers.query.all()
        return result

    @marshal_with(verzorger_data)
    def put(self):
        args = verzorger_put_args.parse_args()
        data = Verzorgers(firstname=args['firstname'], lastname=args['lastname'], email=args['email'])
        db.session.add(data)
        db.session.commit()
        return data, 201

api.add_resource(Sensor, "/sensordata/")    
api.add_resource(Verzorger, "/verzorgers/")
   
if __name__ == '__main__':
    app.run(port='5000', debug=True)