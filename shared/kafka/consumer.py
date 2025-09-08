from kafka import KafkaConsumer
import os
import json

from dotenv import load_dotenv

load_dotenv()

def get_consumer(topic, group_id="default-group"):
    kafka_server = os.getenv("KAFKA_SERVERS")
    return KafkaConsumer(
        topic,
        bootstrap_servers=kafka_server,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='earliest',
        group_id=group_id
    )
