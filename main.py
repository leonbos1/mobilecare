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

def main(): #door leon
    do_connect()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')
    s.connect((HOST, PORT))
    print('Connection made')

    while True:
        rdr1 = mfrc522.MFRC522(sck=18, mosi=23, miso=19, rst=0, cs=22)
        rdr2 = mfrc522.MFRC522(sck=18, mosi=23, miso=19, rst=0, cs=15)
        (stat1, tag_type1) = rdr1.request(rdr1.REQIDL)
        (stat2, tag_type2) = rdr2.request(rdr2.REQIDL)
        if stat1 == rdr1.OK:
            (stat1, uid) = rdr1.SelectTagSN()
            if stat1 == rdr1.OK:
                print("Card detected at scanner #1 %s" % uidToString(uid))
                data = str(uidToString(uid)) + ' Scanner_1'
                s.send(bytes(data, "utf-8"))


        elif stat2 == rdr2.OK:
            (stat2, uid) = rdr2.SelectTagSN()
            if stat2 == rdr2.OK:
                print("Card detected at scanner #2 %s" % uidToString(uid))
                data = str(uidToString(uid)) + ' Scanner_2'
                s.send(bytes(data, "utf-8"))
        else:
            s.send(bytes('no_contact', "utf-8"))

def do_connect(): #door leon

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




