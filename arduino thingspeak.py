import serial
import threading
import json
import urllib.request
import requests
from twilio.rest import Client

global flag
flag = False

def post_cloud_humidity():
    global flag
    threading.Timer(15,post_cloud_humidity).start()
    val=read_data()
    my_hum,my_temp=val.split(",")
    url='https://api.thingspeak.com/update?api_key=xx&field1={}&field2={}'.format(my_hum,my_temp)
    data=urllib.request.urlopen(url)
    print(data)
    print(my_temp)
    print(type(my_temp))

    if my_temp >= str(29):
        if (not flag):
            send_sms_alert(my_temp)
            iftt(my_temp)
            flag= True


def iftt(my_temp):
    payload = { 'value1' : 'P', 'value2' : 'Q', 'value3' : 'R'}
    url='https://maker.ifttt.com/trigger/test/with/keyxxx'
    payload['value1']=Q
    print(payload)
    requests.post(url, data=payload)
    print('Done')


def read_data():
    try:

        arduinodata =serial.Serial('COM8',9600,timeout=0.1)
        while arduinodata.inWaiting:
            val=arduinodata.readline().decode('ascii')
            if len(val) == 13 :
                return val
    except:
        print('Cannot read data !')

def send_sms_alert(my_temp):

    try:
        # Define your body
        my_body="Temperature is high {} *C !".format(my_temp)
        # define client
        client = Client('xx','xx')
        client.messages.create(to='+xx',
                               from_= '+xx',
                               body=my_body)
    except:
        print('Cannot send Sms!')


if __name__ == '__main__':
    post_cloud_humidity()

