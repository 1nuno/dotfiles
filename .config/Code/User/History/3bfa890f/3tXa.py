import os
import secrets
import time
import paho.mqtt.client as mqtt

#token_length = int(os.getenv('LENGTHTOKEN', 3))
#num_tokens = int(os.getenv('NUMTOKENS', 10))
#MQTT_SERVER = os.getenv('MQTT_SERVER', '192.168.40.130')

def on_disconnect(client, userdata, rc):
    print("Disconnected with result code " + str(rc))

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT server with result code " + str(rc))

# Callback function for MQTT on_publish
def on_publish(client, userdata, result):
    print("Message published: " + str(result))

if __name__ == '__main__':
    time.sleep(20)
    client = mqtt.Client("sic-pub")
    client.on_publish = on_publish
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    # Connect to the MQTT server
    print("Estou aqui")
    client.connect("rabbitmq",1883,60)
    print("rabbit")

    # Generate and publish tokens
    for _ in range(2):
        token = secrets.token_hex(4)
        # Publish the token to the tokens topic
        client.publish("/sic/tokens", str(token))
        print(f"Published token: {token}")
