import datetime
import json
import os
import ssl
import time
#from time import sleep

import jwt
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

from sense_hat import SenseHat

# LED Matrix colours
red = (255, 0, 0)
green = (0, 255, 0)

# Used pins
RED_LED_PIN = 18
GREEN_LED_PIN = 17
BUTTON_PIN = 21

# GCP parameters 
project_id = 'virgin-hackathon-1'  # Your project ID.
registry_id = 'my-registry'  # Your registry name.
device_id = 'my-device'  # Your device name.
private_key_file = 'rsa_private.pem'  # Path to private key.
algorithm = 'RS256'  # Authentication key format.
cloud_region = 'us-central1'  # Project region.
ca_certs = 'roots.pem'  # CA root certificate path.
mqtt_bridge_hostname = 'mqtt.googleapis.com'  # GC bridge hostname.
mqtt_bridge_port = 8883  # Bridge port.
message_type = 'event'  # Message type (event or state).

def create_jwt(project_id, private_key_file, algorithm):
    # Create a JWT (https://jwt.io) to establish an MQTT connection.
    token = {
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'aud': project_id
    }
    with open(private_key_file, 'r') as f:
        private_key = f.read()
    print('Creating JWT using {} from private key file {}'.format(
        algorithm, private_key_file))
    return jwt.encode(token, private_key, algorithm=algorithm)


def error_str(rc):
    # Convert a Paho error to a human readable string.
    return '{}: {}'.format(rc, mqtt.error_string(rc))




sense = SenseHat()

y = (255, 255, 0) #Yellow
b = (0, 0, 0) # Black

smiley_face = [
   y, y, y, y, y, y, y, y,
   y, y, y, y, y, y, y, y,
   y, b, b, y, y, b, b, y,
   y, b, b, y, y, b, b, y,
   y, y, y, y, y, y, y, y,
   y, b, b, y, y, b, b, y,
   y, y, y, b, b, y, y, y,
   y, y, y, y, y, y, y, y
]

frowning_face = [
   y, y, y, y, y, y, y, y,
   y, y, y, y, y, y, y, y,
   y, b, b, y, y, b, b, y,
   y, b, b, y, y, b, b, y,
   y, y, y, y, y, y, y, y,
   y, y, y, b, b, y, y, y,
   y, y, b, y, y, b, y, y,
   y, b, y, y, y, y, b, y
]

stripes_1 = [
   y, y, y, b, b, b, y, y,
   y, y, b, b, b, y, y, y,
   y, b, b, b, y, y, y, b,
   b, b, b, y, y, y, b, b,
   b, b, y, y, y, b, b, b,
   b, y, y, y, b, b, b, y,
   y, y, y, b, b, b, y, y,
   y, y, b, b, b, y, y, y
]

stripes_2 = [
   b, y, y, y, b, b, b, y,
   y, y, y, b, b, b, y, y,
   y, y, b, b, b, y, y, y,
   y, b, b, b, y, y, y, b,
   b, b, b, y, y, y, b, b,
   b, b, y, y, y, b, b, b,
   b, y, y, y, b, b, b, y,
   y, y, y, b, b, b, y, y
]

stripes_3 = [
   b, b, y, y, y, b, b, b,
   b, y, y, y, b, b, b, y,
   y, y, y, b, b, b, y, y,
   y, y, b, b, b, y, y, y,
   y, b, b, b, y, y, y, b,
   b, b, b, y, y, y, b, b,
   b, b, y, y, y, b, b, b,
   b, y, y, y, b, b, b, y
]

stripes_4 = [
   b, b, b, y, y, y, b, b,
   b, b, y, y, y, b, b, b,
   b, y, y, y, b, b, b, y,
   y, y, y, b, b, b, y, y,
   y, y, b, b, b, y, y, y,
   y, b, b, b, y, y, y, b,
   b, b, b, y, y, y, b, b,
   b, b, y, y, y, b, b, b
]

stripes_5 = [
   y, b, b, b, y, y, y, b,
   b, b, b, y, y, y, b, b,
   b, b, y, y, y, b, b, b,
   b, y, y, y, b, b, b, y,
   y, y, y, b, b, b, y, y,
   y, y, b, b, b, y, y, y,
   y, b, b, b, y, y, y, b,
   b, b, b, y, y, y, b, b
]

stripes_6 = [
   y, y, b, b, b, y, y, y,
   y, b, b, b, y, y, y, b,
   b, b, b, y, y, y, b, b,
   b, b, y, y, y, b, b, y,
   b, y, y, y, b, b, b, y,
   y, y, y, b, b, b, y, y,
   y, y, b, b, b, y, y, y,
   y, b, b, b, y, y, y, b
]



class Device(object):
    # Device implementation.
    def __init__(self):
        self.connected = False
        self.led1 = False
        self.led2 = False
        
        # Pins setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(RED_LED_PIN,GPIO.OUT)
        GPIO.setup(GREEN_LED_PIN,GPIO.OUT)
        GPIO.setup(BUTTON_PIN,GPIO.IN)

    def update_led_state(self):
        if self.led1:
            GPIO.output(RED_LED_PIN,GPIO.HIGH)
        else:
            GPIO.output(RED_LED_PIN,GPIO.LOW)
        if self.led2:
            GPIO.output(GREEN_LED_PIN,GPIO.HIGH)
        else:
            GPIO.output(GREEN_LED_PIN,GPIO.LOW)

    def wait_for_connection(self, timeout):
        # Wait for the device to become connected.
        total_time = 0
        while not self.connected and total_time < timeout:
            time.sleep(1)
            total_time += 1

        if not self.connected:
            raise RuntimeError('Could not connect to MQTT bridge.')

    def on_connect(self, unused_client, unused_userdata, unused_flags, rc):
        # Callback on connection.
        print('Connection Result:', error_str(rc))
        self.connected = True

    def on_disconnect(self, unused_client, unused_userdata, rc):
        # Callback on disconnect.
        print('Disconnected:', error_str(rc))
        self.connected = False

    def on_publish(self, unused_client, unused_userdata, unused_mid):
        # Callback on PUBACK from the MQTT bridge.
        print('Published message acked.')

    def on_subscribe(self, unused_client, unused_userdata, unused_mid,
                     granted_qos):
        # Callback on SUBACK from the MQTT bridge.
        print('Subscribed: ', granted_qos)
        if granted_qos[0] == 128:
            print('Subscription failed.')

    def on_message(self, unused_client, unused_userdata, message):
        # Callback on a subscription.
        payload = message.payload.decode('utf-8')
        print('Received message \'{}\' on topic \'{}\' with Qos {}'.format(payload, message.topic, str(message.qos)))
        
        # incoming message 'animation' START
        sense.set_pixels(stripes_1)
        time.sleep(0.1)
        sense.set_pixels(stripes_2)
        time.sleep(0.1)
        sense.set_pixels(stripes_3)
        time.sleep(0.1)
        sense.set_pixels(stripes_4)
        time.sleep(0.1)
        sense.set_pixels(stripes_5)
        time.sleep(0.1)
        sense.set_pixels(stripes_6)
        time.sleep(0.1)
        sense.set_pixels(stripes_1)
        time.sleep(0.1)
        sense.set_pixels(stripes_2)
        time.sleep(0.1)
        sense.set_pixels(stripes_3)
        time.sleep(0.1)
        sense.set_pixels(stripes_4)
        time.sleep(0.1)
        sense.set_pixels(stripes_5)
        time.sleep(0.1)
        sense.set_pixels(stripes_6)
        time.sleep(0.1)
        sense.set_pixels(stripes_1)
        time.sleep(0.1)
        sense.set_pixels(stripes_2)
        time.sleep(0.1)
        sense.set_pixels(stripes_3)
        time.sleep(0.1)
        sense.set_pixels(stripes_4)
        time.sleep(0.1)
        sense.set_pixels(stripes_5)
        time.sleep(0.1)
        sense.set_pixels(stripes_6)
        time.sleep(0.1)
        sense.clear
        # incoming message 'animation' END

        if not payload:
            print('no data?')
            return

        # Parse incoming JSON.
        print('Parsing data from incoming config')
        data = json.loads(payload)
        # THIS WILL NOT PROGRESS UNLESS JSON IS VALID!!!

        print('Checking LED1 from incoming config')
        if data['led1'] != self.led1:
            self.led1 = data['led1']
            if self.led1:
                print('Led1 is on')
            else:
                print('Led1 is off')

        print('Checking LED2 from incoming config')
        if data['led2']!=self.led2:
            self.led2 = data['led2']
            if self.led2:
                print('Led2 is on')
            else:
                print('Led2 is off')

        print('Checking Versa Status from incoming config')
        if data['versastatus'] == "up":
            print('Versa is UP!')
            fillgreen()
        elif data['versastatus'] == "down":
            print('Versa is DOWN!')
            fillred()
        else:
            print('Versa is UNKNOWN!')
            fillblue()


def joystick_any(event):
    if event.action == 'pressed':
        print('You pressed me')
        if event.direction == 'up':
            print('Up')
        elif event.direction == 'down':
            print('Down')
    elif event.action == 'released':
        print('You released me')

def fillred():
  sense.clear(255, 0, 0)

def fillblue():
  sense.clear(0, 0, 255)

def fillgreen():
  sense.clear(0, 255, 0)
  
def fillyellow():
  sense.clear(255, 255, 0)



def main():

    client = mqtt.Client(
        client_id='projects/{}/locations/{}/registries/{}/devices/{}'.format(
            project_id,
            cloud_region,
            registry_id,
            device_id))
    client.username_pw_set(
        username='unused',
        password=create_jwt(
            project_id,
            private_key_file,
            algorithm))
    client.tls_set(ca_certs=ca_certs, tls_version=ssl.PROTOCOL_TLSv1_2)

    device = Device()

    client.on_connect = device.on_connect
    client.on_publish = device.on_publish
    client.on_disconnect = device.on_disconnect
    client.on_subscribe = device.on_subscribe
    client.on_message = device.on_message
    client.connect(mqtt_bridge_hostname, mqtt_bridge_port)
    client.loop_start()

    mqtt_telemetry_topic = '/devices/{}/events'.format(device_id)
    mqtt_config_topic = '/devices/{}/config'.format(device_id)

    # Wait up to 5 seconds for the device to connect.
    device.wait_for_connection(5)

    client.subscribe(mqtt_config_topic, qos=1)
    
    num_message = 0

    try:        
        while True:
            #device.update_led_state()
            # If button was pressed - send message.
            #if not GPIO.input(BUTTON_PIN):   
            #    currentTime = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            #    num_message += 1
            #    # Form payload in JSON format.
            #    data = {
            #        'num_message' : num_message,
            #        'led1': device.led1,
            #        'led2': device.led2,
            #        'message': "Hello",
            #        'time' : currentTime
            #    }
            #    payload = json.dumps(data, indent=4)
            #    print('Publishing payload', payload)
            #    client.publish(mqtt_telemetry_topic, payload, qos=1)
            #    # Make sure that message was sent once on press.
            #    #while not GPIO.input(BUTTON_PIN):
            #         # waiting 'animation' START
            #         sense.clear()
            #         time.sleep(0.5)
            #         sense.show_letter(".", green)
            #         # waiting 'animation' END 
            #         time.sleep(0.1)   
            #time.sleep(0.1)

            #sense.stick.direction_any = joystick_any

            sense.stick.direction_up = fillred
            sense.stick.direction_down = fillblue
            sense.stick.direction_left = fillgreen
            sense.stick.direction_right = fillyellow

            acceleration = sense.get_accelerometer_raw()
            x = acceleration['x']
            y = acceleration['y']
            z = acceleration['z']

            x = abs(x)
            y = abs(y)
            z = abs(z)

            if x > 1.5 or y > 1.5 or z > 1.5:
                print('motion detected')

            currentTime = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            num_message += 1
            # Form payload in JSON format.
            data = {
                'num_message' : num_message,
                'version': "3",
                'led1': device.led1,
                'led2': device.led2,
                'message': "Hello",
                'time' : currentTime,
                'temperature' : sense.get_temperature(),
                'pressure' : sense.get_pressure(),
                'humidity' : sense.get_humidity(),
            }
            payload = json.dumps(data, indent=4)
            print('Publishing payload', payload)
            client.publish(mqtt_telemetry_topic, payload, qos=1)
            # Clear the sensor data - is this needed?
            #sense.clear()
            time.sleep(10)

    except KeyboardInterrupt:
        # Exit script on ^C.
        pass
        GPIO.output(GREEN_LED_PIN,GPIO.LOW)
        GPIO.output(RED_LED_PIN,GPIO.LOW)
        GPIO.cleanup()
        client.disconnect()
        client.loop_stop()
        print('Exit with ^C. Goodbye!')
        

if __name__ == '__main__':
    main()


#while True:
#   sense.set_pixels(stripes_1)
#   time.sleep(0.1)
#   sense.set_pixels(stripes_2)
#   time.sleep(0.1)
#   sense.set_pixels(stripes_3)
#   time.sleep(0.1)
#   sense.set_pixels(stripes_4)
#   time.sleep(0.1)
#   sense.set_pixels(stripes_5)
#   time.sleep(0.1)
#   sense.set_pixels(stripes_6)
#   time.sleep(0.1)