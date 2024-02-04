#!/usr/bin/env python
import time
import os
from scipy.stats import truncnorm
from kafka import KafkaAdminClient,KafkaProducer
from kafka.admin import NewTopic

if __name__ == "__main__":
    SLEEP = 30
    TOPIC_NAME = "teste"

    
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
    
    for i in range(10):
        producer.send(TOPIC_NAME, b'hey %s'%i)
        print("Message sent!")
        producer.flush()
        time.sleep(30)