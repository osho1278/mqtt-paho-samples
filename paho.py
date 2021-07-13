import paho.mqtt.client as mqtt
import random,time
import json
import base64

def on_connect(client, userdata, rc,c):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

def on_publish(client, userdata, msg):
    print(client,msg,userdata)
    # print(msg.topic+" "+str(msg.payload))

client = mqtt.Client("telemetry1")
client.on_connect = on_connect
client.on_message = on_message
client.on_publish=on_publish
client.username_pw_set("admin","admin")
client.connect("ec2-13-232-244-246.ap-south-1.compute.amazonaws.com", 1883)
f = open('test.json',)
  
# returns JSON object as 
# a dictionary
data = json.load(f)
# sample_string = str(data)
# sample_string_bytes = sample_string.encode("ascii")
  
# base64_bytes = base64.b64encode(sample_string_bytes)
# base64_string = base64_bytes.decode("ascii")

while True:
    rand=random.randint(0,9)
    # print("publishing ",rand)
    client.publish("telemetry",json.dumps({"origin":"local","data":json.dumps(data)}))
    time.sleep(.1)
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()