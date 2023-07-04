# boot.py -- run on boot-up
import network, utime
from machine import Pin

# Replace the following with your WIFI Credentials
SSID = ""
SSID_PASSWORD = ""


pin = Pin(13, Pin.OUT, Pin.PULL_DOWN)

def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(False) # Disconnect from any active connection
    print('connecting to network...')
    sta_if.active(True)
    sta_if.connect(SSID, SSID_PASSWORD)
    while not sta_if.isconnected():
        print("Attempting to connect....")
        utime.sleep(1)
    print('Connected! Network config:', sta_if.ifconfig())
    
print("Connecting to your wifi...")
do_connect()
