import os
import mysql.connector
import paho.mqtt.client as mqtt
from mysql.connector import errorcode
import time

# Define the MQTT and MariaDB connection parameters
#MQTT_SERVER = os.getenv('MQTT_SERVER',"rabbitmq")
#MARIADB_SERVER = os.getenv('MARIADB_SERVER', 'mariadb')
#DB_USER = os.getenv('DB_USER', 'projeto')
#DB_PASSWORD = os.getenv('DB_PASSWORD', 'projeto')
#DB_NAME = os.getenv('DB_NAME', 'sic')

# Callback function for MQTT on_connect
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT server with result code " + str(rc))
    client.subscribe("/sic/#")  

# Callback function for MQTT on_message
def on_message(client, userdata, msg):
    print("Received token: " + msg.payload.decode())

    # Insert received token into the MariaDB database
    # try:

    #     # Define the table structure
    #     TABLE = (
    # 	    "CREATE TABLE IF NOT EXISTS 'tokens' ("
    # 	    " 'id' int(11) NOT NULL AUTO_INCREMENT,"
    # 	    " 'token' varchar(255) NOT NULL,"
   	#     " PRIMARY KEY ('id')"
   	#     ") ENGINE=InnoDB"
	# )
    #     cursor.execute(TABLE)

    #     # Insert the received token
    #     add_token = ("INSERT INTO tokens (token) VALUES (%s)")
    #     data = (msg.payload.decode(),)
    #     cursor.execute(add_token, data)
    #     cnx.commit()
        
    # except mysql.connector.Error as err:
    #     print("Error: " + str(err))

if __name__ == '__main__':
    print('joana')
    #time.sleep(20)

    cnx = mysql.connector.connect(user='root', password='projeto', host='mariadb', database='sic')
    cursor = cnx.cursor()
    print('mysql')

    # Create an MQTT client
    client = mqtt.Client("sic-sub")
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to the MQTT server
    client.connect("rabbitmq", 1883 , 60)
    print('rabbit')

    # Start listening for MQTT messages
    client.loop_forever()
    cnx.close()
