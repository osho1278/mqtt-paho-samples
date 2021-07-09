import paho.mqtt.client as mqtt
from pykafka import KafkaClient
import time

mqtt_broker = "127.0.0.1"
mqtt_client = mqtt.Client()
mqtt_client.username_pw_set("admin","admin")
mqtt_client.connect(mqtt_broker)

kafka_client = KafkaClient(hosts="localhost:9092")
kafka_topic = kafka_client.topics['telemetry']
kafka_producer = kafka_topic.get_sync_producer()

def on_message(client, userdata, message):
    msg_payload = str(message.payload)
    kafka_producer.produce(msg_payload.encode('ascii'))
    

mqtt_client.subscribe("telemetry")
mqtt_client.on_message = on_message
mqtt_client.loop_forever()