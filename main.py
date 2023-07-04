from machine import Pin
import time
from dht11module import DHT11
import ubinascii
from umqttsimple import MQTTClient
import machine
import json

# Sensor setup
pin = Pin(13, Pin.OUT, Pin.PULL_DOWN)
sensor = DHT11(pin)

# MQTT setup
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
MQTT_BROKER = "io.adafruit.com"
PORT = 1883
ADAFRUIT_USERNAME = "ek223ur"
ADAFRUIT_PASSWORD = ""
SUBSCRIBE_TOPIC = b"ek223ur/f/led"
PUBLISH_TEMP = b"ek223ur/f/temp"
PUBLISH_HUMIDITY = b"ek223ur/f/humidity"

# LED setup
led = machine.Pin("LED", machine.Pin.OUT)

last_publish = time.time()  # time of the last published message
publish_interval = 5  # send message every 5 seconds

def sub_cb(topic, msg):
    print((topic, msg))
    if msg.decode() == "ON":
        led.value(1)
    else:
        led.value(0)

def reset():
    print("Resetting...")
    time.sleep(5)
    machine.reset()

def get_sensor_reading():
    time.sleep(2)
    try:
        t = sensor.temperature
        time.sleep(2)
        h = sensor.humidity
    except Exception as e:
        print("An exception occurred:", str(e))
        return None
    return {"Temperature": t, "Humidity": h}

def main():
    print(f"Begin connection with MQTT Broker :: {MQTT_BROKER}")
    mqttClient = MQTTClient(CLIENT_ID, MQTT_BROKER, PORT, ADAFRUIT_USERNAME, ADAFRUIT_PASSWORD, keepalive=60)
    mqttClient.set_callback(sub_cb)
    mqttClient.connect()
    mqttClient.subscribe(SUBSCRIBE_TOPIC)
    print(f"Connected to MQTT Broker :: {MQTT_BROKER}, and waiting for callback function to be called!")

    while True:
        mqttClient.check_msg()
        global last_publish
        if (time.time() - last_publish) >= publish_interval:
            sensor_data = get_sensor_reading()
            if sensor_data is not None:

                temperature = sensor_data["Temperature"]
                humidity = sensor_data["Humidity"]

                mqttClient.publish(PUBLISH_TEMP, str(temperature).encode())
                mqttClient.publish(PUBLISH_HUMIDITY, str(humidity).encode())

                last_publish = time.time()
                print("Sent temperature data:", temperature)
                print("Sent humidity data:", humidity)
        time.sleep(1)

if __name__ == "__main__":
    while True:
        try:
            main()
        except OSError as e:
            print("Error: " + str(e))
            reset()
