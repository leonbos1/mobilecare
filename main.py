import socket
from machine import Pin, ADC
import time
import network
import mfrc522

def uidToString(uid):
    mystring = ""
    for i in uid:
        mystring = "%02X" % i + mystring
    return mystring

PORT = 4000
HOST = "192.168.178.69"

def main():
    do_connect()
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')
    s.connect((HOST, PORT))
    print('Connection made')
<<<<<<< HEAD

    while True:
        scan1 = scanner1()
        scan2 = scanner2()
       # scan3 = scanner3()
       # scan4 = scanner4()
        print(scan1)
        print(scan2)
        #print(scan3)
        #print(scan4)
        try:
            s.send(bytes(str(scan1), "utf-8"))
            print(scan1)
            time.sleep(0.1)
            s.send(bytes(str(scan2), "utf-8"))
            print(scan2)
            #time.sleep(0.1)
            #s.send(bytes(str(scan3), "utf-8"))
            #print(scan3)
            #time.sleep(0.1)
           # s.send(bytes(str(scan4), "utf-8"))
          #  print(scan4)
        except Exception as e:
            print(e)

def scanner1():
    rdr1 = mfrc522.MFRC522(sck=18, mosi=23, miso=19, rst=0, cs=22, baudrate=100000)
    (stat1, tag_type1) = rdr1.request(rdr1.REQIDL)

    if stat1 == rdr1.OK:
        (stat1, uid) = rdr1.SelectTagSN()
        if stat1 == rdr1.OK:
            print("Card detected at scanner #1 %s" % uidToString(uid))
            data = str(uidToString(uid)) + ' Scanner_1'
            return data

        else:
            return 'no_contact'
    else:
        return 'no_contact'

def scanner2():
    rdr2 = mfrc522.MFRC522(sck=18, mosi=23, miso=19, rst=0, cs=15, baudrate=100000)
    (stat2, tag_type2) = rdr2.request(rdr2.REQIDL)

    if stat2 == rdr2.OK:
        (stat2, uid) = rdr2.SelectTagSN()
        if stat2 == rdr2.OK:
            print("Card detected at scanner #2 %s" % uidToString(uid))
            data = str(uidToString(uid)) + ' Scanner_2'
            return data

        else:
            return 'no_contact'
    else:
        return 'no_contact'
"""
def scanner3():
    rdr3 = mfrc522.MFRC522(sck=18, mosi=23, miso=19, rst=0, cs=12, baudrate=100000)
    (stat3, tag_type3) = rdr3.request(rdr3.REQIDL)

    if stat3 == rdr3.OK:
        (stat3, uid) = rdr3.SelectTagSN()
        if stat3 == rdr3.OK:
            print("Card detected at scanner #3 %s" % uidToString(uid))
            data = str(uidToString(uid)) + ' Scanner_3'
            return data

        else:
            return 'no_contact'
    else:
        return 'no_contact'

def scanner4():
    rdr4 = mfrc522.MFRC522(sck=18, mosi=23, miso=19, rst=0, cs=5, baudrate=100000)
    (stat4, tag_type4) = rdr4.request(rdr4.REQIDL)
    print(rdr4)
    print(stat4)
    if stat4 == rdr4.OK:
        (stat4, uid) = rdr4.SelectTagSN()
        if stat4 == rdr4.OK:
            print("Card detected at scanner #4 %s" % uidToString(uid))
            data = str(uidToString(uid)) + ' Scanner_4'
            return data

        else:
            return 'no_contact'
    else:
        return 'no_contact'
"""
=======

    if uname()[0] == 'esp32':
        rdr1 = mfrc522.MFRC522(sck=18, mosi=23, miso=19, rst=0, cs=22)
        rdr2 = mfrc522.MFRC522(sck=18, mosi=23, miso=19, rst=0, cs=15)

    while True:
        (stat1, tag_type1) = rdr1.request(rdr1.REQIDL)
        (stat2, tag_type2) = rdr2.request(rdr2.REQIDL)
        if stat1 == rdr1.OK:
            (stat1, uid) = rdr1.SelectTagSN()
            if stat1 == rdr1.OK:
                print("Card detected at scanner #1 %s" % uidToString(uid))
                data = str(uidToString(uid)) + ' Scanner_1'
                s.send(bytes(data, "utf-8"))

        if stat2 == rdr2.OK:
            (stat2, uid) = rdr2.SelectTagSN()
            if stat2 == rdr2.OK:
                print("Card detected at scanner #2 %s" % uidToString(uid))
                data = str(uidToString(uid)) + ' Scanner_2'
                s.send(bytes(data, "utf-8"))

>>>>>>> parent of 0ad35d1 (update)
def do_connect():

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('Covid19 5G Afluistermast', 'Kaaskaas123')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())



if __name__ == '__main__':
    main()




