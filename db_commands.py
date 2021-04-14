import sqlite3

conn = sqlite3.connect('sensor.db', check_same_thread=False)
c = conn.cursor()

def addtosensordata(id, timeactivated, timedeactivated):
    c.execute(f"insert into sensor_time(sensor_id,time_activated, time_deactivated) values ({id},'{timeactivated}','{timedeactivated}')")
    conn.commit()