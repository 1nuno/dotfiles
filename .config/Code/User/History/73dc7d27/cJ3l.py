import paho.mqtt.client as mqtt

def on_disconnect(client, userdata, rc):
    print("Disconnected with result code "+str(rc))

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("/sic/#")

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

if __name__ == '__main__':
    client= mqtt.Client("sub")
    client.on_message = on_message
    client.on_subscribe = on_subscribe
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.connect("rabbitmq",1883)
    client.loop_forever()