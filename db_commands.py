import sqlite3

conn = sqlite3.connect('sensor.db', check_same_thread=False)
c = conn.cursor()

def addtosensordata(id, timeactivated, timedeactivated, tag, activation_duration):
    c.execute(f"insert into sensor_time(sensor_id,time_activated, time_deactivated, tag, activation_duration) values ({id},'{timeactivated}','{timedeactivated}','{tag}','{activation_duration}')")
    conn.commit()

"""
CREATE TABLE "sensor_time" (
	"id"	INTEGER NOT NULL,
	"sensor_id"	INTEGER NOT NULL,
	"time_activated"	TEXT,
	"time_deactivated"	TEXT,
	"tag"	TEXT,
	"activation_duration"	INTEGER,
	PRIMARY KEY("id")
);

CREATE TABLE "sensor" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	PRIMARY KEY("id")
);


"""