import paho.mqtt.client as mqtt
import time

def on_disconnect(client, userdata, rc):
    print("Disconnected with result code "+str(rc))

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_publish(client, userdata, result):
    print("Message published: "+str(result))

if __name__ == '__main__':
    time.sleep(5)
    print('YO1')
    client= mqtt.Client("pub")
    print('YO2')
    client.on_publish = on_publish
    print('YO3')
    client.on_connect = on_connect
    print('YO4')
    client.on_disconnect = on_disconnect
    print('YO5')
    client.connect("rabbitmq",15672,60) # because "rabbitmq" is the name of our broker container inside the global network
    print('YO6')
    client.publish("/sic/tokens", 0)