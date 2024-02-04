import paho.mqtt.client as mqtt
import mysql.connector
from mysql.connector import errorcode

def on_disconnect(client, userdata, rc):
    print("Disconnected with result code "+str(rc))

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("/sic/tokens")

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed")

def on_message(client, userdata, msg):
    try:
        cnx = mysql.connector.connect(
                                        user='root',
                                        password='my-secret-pw',
                                        host='mariadb',
                                        database='sic')
        print("Connected to database")
        cursor = cnx.cursor()
        QUERY = f"INSERT INTO sic (value) VALUES ({msg});"
        cursor.execute(QUERY)
        cnx.commit()

    except mysql.connector.Error as err:
        print("Error connecting to database")
        exit(0)

    try:
        TABLE = (
        "CREATE TABLE 'sic' ("
        " 'id' int(11) NOT NULL AUTO_INCREMENT,"
        " 'date' TIMESTAMP NOT NULL,"
        " 'client' varchar(64) NOT NULL,"
        " 'value' int(11) NOT NULL,"
        " PRIMARY KEY ('id')"
        ") ENGINE=InnoDB")
        cursor.execute(TABLE)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("Table already exists")
        else:
            print("Error creating table")

    print(msg.topic+" "+str(msg.payload))

if __name__ == '__main__':
    client= mqtt.Client("sub")
    client.on_message = on_message
    client.on_subscribe = on_subscribe
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.connect("rabbitmq",1883)
    client.loop_forever()