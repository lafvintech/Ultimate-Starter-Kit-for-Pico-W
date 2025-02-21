from machine import Pin
import socket
import math
from dht import DHT11, InvalidPulseCount
from time import sleep
from secrets import *
from do_connect import *

# rgb led
red=machine.Pin(13,machine.Pin.OUT)
green=machine.Pin(14,machine.Pin.OUT)
blue=machine.Pin(15,machine.Pin.OUT)

sensor_pin = Pin(16, Pin.IN)
dht_sensor = DHT11(sensor_pin)

def get_temperature_humidity():
    try:
        dht_sensor.measure()
        temperature = dht_sensor.temperature
        humidity = dht_sensor.humidity
        return temperature, humidity
    except:
        return None, None

def webpage(temp, hum):
    html = f"""
            <!DOCTYPE html>
            <html>
            <body>
            <form action="./red">
            <input type="submit" value="red " />
            </form>
            <form action="./green">
            <input type="submit" value="green" />
            </form>
            <form action="./blue">
            <input type="submit" value="blue" />
            </form>
            <form action="./off">
            <input type="submit" value="off" />
            </form>
            <p>Temperature: {temp}C</p>
            <p>Humidity: {hum}%</p>
            </body>
            </html>
            """
    return html

def serve(connection):
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        
        print(request)
        
        if request == '/off?':
            red.low()
            green.low()
            blue.low()
        elif request == '/red?':
            red.high()
            green.low()
            blue.low()
        elif request == '/green?':
            red.low()
            green.high()
            blue.low()
        elif request == '/blue?':
            red.low()
            green.low()
            blue.high()

        temperature, humidity = get_temperature_humidity()
        if temperature is None:
            temperature = "Error"
            humidity = "Error"
        else:
            temperature = "{:.1f}".format(temperature)
            humidity = "{:.1f}".format(humidity)
            
        html = webpage(temperature, humidity)
        client.send(html)
        client.close()

def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    print(connection)
    return(connection)

try:
    ip=do_connect()
    if ip is not None:
        connection=open_socket(ip)
        serve(connection)
except KeyboardInterrupt:
    machine.reset()