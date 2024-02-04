import paho.mqtt.client as mqtt
import mysql.connector
import traceback 
import time

cnx = mysql.connector.connect(
                            user='root',
                            password='my-secret-pw',
                            host='mariadb',
                            database='sic')
cursor = cnx.cursor()


def on_disconnect(client, userdata, rc):
    print("disc")
    print("Disconnected with result code "+str(rc))

def on_connect(client, userdata, flags, rc):
    print("conn")
    print("Connected with result code "+str(rc))
    client.subscribe("/sic/tokens")

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed")

def connect_to_mariadb(user,password,host,database):
    try:
        cnx = mysql.connector.connect(
                            user=user,
                            password=password,
                            host=host,
                            database=database)
        print("Connected to database")
    except mysql.connector.Error as err:
        print("Error connecting to database")

def insert_to_db(msg):
    try:
        cursor = cnx.cursor()
        QUERY = f"INSERT INTO sic (value) VALUES ({str(msg.payload, 'utf-8')});"
        cursor.execute(QUERY)
        cnx.commit()
    except:
        traceback.print_exc()

def on_message(client, userdata, msg):
    print(msg.topic+" - "+str(msg.payload))
    print()

    try:
        QUERY = f"INSERT INTO sic (value) VALUES ('myString');"
        cursor.execute(QUERY)
        cnx.commit()
    except:
        traceback.print_exc()

if __name__ == '__main__':
    time.sleep(20)
    client= mqtt.Client("sub")
    client.on_message = on_message
    client.on_subscribe = on_subscribe
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.connect("rabbitmq",1883,60)
    client.loop_forever()
    cnx.close()