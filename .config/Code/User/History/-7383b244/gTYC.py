#!/usr/bin/env python
import time
import os
from scipy.stats import truncnorm
from kafka import KafkaAdminClient, KafkaConsumer, KafkaProducer
from kafka.admin import NewTopic

MEAN = float(os.environ['MEAN'])
STD = float(os.environ['STD'])
LOWER = -5
UPPER = 45

if __name__ == "__main__":
    # Create 'my-topic' Kafka topic
    print("Starting producer script...")
    try:
        admin = KafkaAdminClient(bootstrap_servers='kafka:9093')
        print("KafkaAdminClient passed!")
        topic = NewTopic(name='sh-temperature',
        num_partitions=1,
        replication_factor=1)
        admin.create_topics([topic])
        print(f"New topic created! - {topic}")
    except Exception:
        print('Upsy daisy')

    producer = KafkaProducer(bootstrap_servers='kafka:9093')
    print("KafkaProducer passed!")
    

    generate = truncnorm((LOWER - MEAN) / STD, (UPPER - MEAN) / STD, loc=MEAN, scale=STD)
    
    for n in range(1,100):
        print("N: "+str(n))
        time.sleep(0.1)
        producer.send('sic-topic', b'number %d' % n)
        print("Message sent!")
        producer.flush()

    print("Ending script!")