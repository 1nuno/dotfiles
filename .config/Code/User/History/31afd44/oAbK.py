#!/usr/bin/env python
import time
import os
from scipy.stats import truncnorm
from kafka import KafkaAdminClient, KafkaConsumer, KafkaProducer
from kafka.admin import NewTopic

if __name__ == "__main__":
    MEAN = float(os.environ['MEAN'])
    STD = float(os.environ['STD'])
    LOWER = float(os.environ['LOWER'])
    UPPER = float(os.environ['UPPER'])
    SLEEP = float(os.environ['SLEEP'])
    TOPIC_NAME = os.environ['TOPIC_NAME']
    MESUREMENT = os.environ['MESUREMENT']
    LOCATION_TAG = os.environ['LOCATION_TAG']
    FIELD_NAME = os.environ['FIELD_NAME']
    random_value_generator = truncnorm((LOWER - MEAN) / STD, (UPPER - MEAN) / STD, loc=MEAN, scale=STD)
    
    print("Starting temperature sensor script...")
    try:
        admin = KafkaAdminClient(bootstrap_servers='kafka:9093')
        print("KafkaAdminClient passed!")
        topic = NewTopic(name=TOPIC_NAME,
        num_partitions=1,
        replication_factor=1)
        admin.create_topics([topic])
        print(f"New topic created! - {TOPIC_NAME}")
    except Exception as e:
        print(f'An error has occured: {str(e)}')

    producer = KafkaProducer(bootstrap_servers='kafka:9093')
    print("KafkaProducer passed!")
    
    while True:
        value = round(random_value_generator.rvs(),2)
        line_protocol_msg = bytes(f"{MESUREMENT},location={LOCATION_TAG} {FIELD_NAME}={value}", encoding="utf-8")
        producer.send(TOPIC_NAME, line_protocol_msg)
        print(f"Message sent! - {line_protocol_msg}")
        producer.flush()
        time.sleep(SLEEP)
   
    print("Ending script!")