import paho.mqtt.client as mqtt
import time
time.sleep(10)

def on_disconnect(client, userdata, rc):
    print("Disconnected with result code "+str(rc))

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_publish(client, userdata, result):
    print("Message published: "+str(result))

if __name__ == '__main__':
    client= mqtt.Client("pub")
    client.on_publish = on_publish
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.connect("rabbitmq",1883) # because "rabbitmq" is the name of our broker container inside the global network
    client.publish("/sic/tokens", "hello world")