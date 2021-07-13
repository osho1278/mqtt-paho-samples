import paho.mqtt.client as mqtt
import random
import time
import json
import base64


def on_connect(client, userdata, rc, c):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.


def on_message(client, userdata, msg):
    print("OnMessage ",msg.topic+" "+str(msg.payload))


def on_publish(client, userdata, msg):
    print(client, msg, userdata)
    # print(msg.topic+" "+str(msg.payload))


def buildDittoProtocolMsg(namespace, name, group, channel, criterion, action, path, dittoHeaders, value, status, extra):
    topic = buildTopic(namespace, name, group, channel, criterion, action)

    return {
        "topic": topic,
        "path": path,
        "headers": dittoHeaders,
        "value": value,
        "status": status,
        "extra": extra,
    }


def buildTopic(namespace, name, group, channel, criterion, action):
    topicChannel = '' if('none' == channel) else '/' + channel
    return namespace + "/" + name + "/" + group + topicChannel + "/" + criterion + "/" + action


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
# client.username_pw_set("admin","admin")
client.connect("20.198.75.22", 1883)
f = open('test.json',)

# returns JSON object as
# a dictionary
value = {
        "temp_sensor": {
            "properties": {
                "value": [30]
            }
        },
        "altitude": {
            "properties": {
                "value": {"test":360.342}
            }
        }
    }


retval = buildDittoProtocolMsg("my.test","octopus", 
        'things', 
        'twin', 
        'commands',
        'modify', 
        '/features', 
        None, 
        value,
        None,
        None
    )
# sample_string = str(data)
# sample_string_bytes = sample_string.encode("ascii")

# base64_bytes = base64.b64encode(sample_string_bytes)
# base64_string = base64_bytes.decode("ascii")
client.subscribe("ditto-tutorial/my.test:octopus")
client.publish("ditto-tutorial/my.test:octopus", json.dumps(retval))
# while True:
#     rand=random.randint(0,9)
#     # print("publishing ",rand)
#     time.sleep(.1)
# # Blocking call that processes network traffic, dispatches callbacks and
# # handles reconnecting.
# # Other loop*() functions are available that give a threaded interface and a
# # manual interface.
client.loop_forever()

print("Done")
