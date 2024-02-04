#!/usr/bin/env python
import time
import os
from scipy.stats import truncnorm
from kafka import KafkaAdminClient, KafkaConsumer, KafkaProducer
from kafka.admin import NewTopic

if __name__ == "__main__":
    MEAN = float(os.environ['MEAN'])
    STD = float(os.environ['STD'])
    LOWER = -5
    UPPER = 45
    random_temperature_generator = truncnorm((LOWER - MEAN) / STD, (UPPER - MEAN) / STD, loc=MEAN, scale=STD)
    

    print("Starting temperature sensor script...")
    try:
        admin = KafkaAdminClient(bootstrap_servers='kafka:9093')
        print("KafkaAdminClient passed!")
        topic_name = 'sh-temperature'
        topic = NewTopic(name=topic_name,
        num_partitions=1,
        replication_factor=1)
        admin.create_topics([topic])
        print(f"New topic created! - {topic_name}")
    except Exception:
        print('Upsy daisy')

    producer = KafkaProducer(bootstrap_servers='kafka:9093')
    print("KafkaProducer passed!")
    
    while True:
        temperature = round(random_temperature_generator.rvs(),2)
        producer.send(topic_name, temperature)
        print(f"Message sent! - {temperature}")
        producer.flush()
        time.sleep(30)
   
    print("Ending script!")