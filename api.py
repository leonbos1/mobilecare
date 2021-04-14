from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
api = Api(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'sensor.db')

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

sensor_put_args = reqparse.RequestParser()
sensor_put_args.add_argument("id", type=int, help="Dit is het id van de log")
sensor_put_args.add_argument("sensor_id", type=int, help="Dit is het id van de sensor die iets heeft gescand")
sensor_put_args.add_argument("time_activated", type=str, help='Dit is de tijd dat de sensor is geactivate')
sensor_put_args.add_argument("sensor_deactivated", type=str, help='dit is de tijd dat de sensor is gedeactvate')
sensor_put_args.add_argument("tag", type=str, help='dit is de tag die de sensor heeft gescand')
sensor_put_args.add_argument("activation_duration", type=int, help='dit is de tijd in seconde dat de sensor is geactivate')

resource_fields = {
    'id': fields.Integer,
    'sensor_id': fields.Integer,
    'time_activated': fields.String,
    'time_deactivated': fields.String,
    'tag': fields.String,
    'activation_duration': fields.Integer
}

class Sensor(Resource):
    @marshal_with(resource_fields)
    def get(self, id):
        result = SensorTime.query.filter_by(id=id).first()
        if not result:
            abort(404, message="Geen data gevonden met dit ID")
        return result

api.add_resource(Sensor, "/id/<int:id>")    
   
if __name__ == '__main__':
    app.run(host='192.168.178.69', port='80', debug=True)