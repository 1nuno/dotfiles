import paho.mqtt.client as mqtt
import mysql.connector
import traceback


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
        return cnx
    except mysql.connector.Error as err:
        print("Error connecting to database")
        return 0

def insert_to_db(msg):
    try:
        QUERY = f"INSERT INTO sic (value) VALUES ('{str(msg.payload, 'utf-8')}');"
        cursor.execute(QUERY)
        cnx.commit()
        print(f"inserted: <<{str(msg.payload, 'utf-8')}>>")
    except:
        traceback.print_exc()

def on_message(client, userdata, msg):
    print(msg.topic+" - "+str(msg.payload))
    insert_to_db(msg)

if __name__ == '__main__':
    cnx = connect_to_mariadb('root','my-secret-pw','mariadb','sic')
    cursor = cnx.cursor()
    client= mqtt.Client("sub")
    client.on_message = on_message
    client.on_subscribe = on_subscribe
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.connect("rabbitmq",1883,60)
    client.loop_forever()
    cnx.close()
