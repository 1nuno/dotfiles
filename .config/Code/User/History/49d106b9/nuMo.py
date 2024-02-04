#!/usr/bin/env python
import time
from kafka import KafkaAdminClient, KafkaConsumer, KafkaProducer
from kafka.admin import NewTopic

if __name__ == "__main__":
    # Create 'my-topic' Kafka topic
    print("Starting producer script...")
    try:
        admin = KafkaAdminClient(bootstrap_servers='192.168.23.130:9093')
        print("KafkaAdminClient passed!")
        topic = NewTopic(name='sic-topic',
        num_partitions=1,
        replication_factor=1)
        admin.create_topics([topic])
        print("New topic created!")
    except Exception:
        print('Upsy daisy')

    producer = KafkaProducer(bootstrap_servers='192.168.23.130:9093')
    print("KafkaProducer passed!")
    
    for n in range(1,100):
        print("N: "+str(n))
        time.sleep(1)
        producer.send('sic-topic', b'number %d' % n)
        print("Message sent!")
        producer.flush()

    print("Ending script!")