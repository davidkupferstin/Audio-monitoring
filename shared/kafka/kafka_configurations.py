from kafka import KafkaProducer
import os
import json

from dotenv import load_dotenv

load_dotenv()

def get_producer_config():
    kafka_server = os.getenv("KAFKA_SERVERS")
    return KafkaProducer(
        bootstrap_servers=kafka_server,
        value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8')
    )
