
import os
import json
import time
import kuksa_viss_client as kuksa
import paho.mqtt.client as mqtt

BROKER_URL = os.environ['MQTT_URL']
BROKER_PORT = os.environ['MQTT_PORT']
KUKSAVAL_HOST = os.environ['KUKSAVAL_HOST']
KUKSAVAL_PORT = os.environ['KUKSAVAL_PORT']
TOPIC_PREFIX = os.environ['TOPIC_PREFIX']
is_connected = False

PATH_LIST = ["Vehicle.DriveTime", 
"Vehicle.Powertrain.CombustionEngine.Engine.Speed", 
"Vehicle.OBD.Speed",
"Vehicle.Powertrain.Transmission.Gear",
"Vehicle.Powertrain.CombustionEngine.Engine.TPS",
"Vehicle.Chassis.Brake.PedalPosition",
"Vehicle.TravelledDistance"]

def main():

    mqtt_client = mqtt.Client()
    mqtt_client.tls_set("ca.crt")
    mqtt_client.tls_insecure_set(True)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_publish = on_publish
    mqtt_client.connect(BROKER_URL, int(BROKER_PORT))
    mqtt_client.loop_start()

    while is_connected != True:
        
        print("Connecting...")
        time.sleep(5)
    config = {
        "ip" : KUKSAVAL_HOST,
        "port" : KUKSAVAL_PORT
    }
    kuksa_client = kuksa.KuksaClientThread(config)
    time.sleep(5)
    kuksa_client.authorize()
    kuksa_client.start()
    while True:

        for path in PATH_LIST:

            response = kuksa_client.getValue(path)
            r_json = json.loads(response)
            topic_path = path.replace(".", "/")
            sentPayload = str(r_json["data"]["dp"]["value"])
            mqtt_client.publish(topic= TOPIC_PREFIX + "/" + topic_path,payload=sentPayload , qos=0, retain=False)
        
        
    
def on_connect(client, userdata, flags, rc):
    if rc==0:
        global is_connected
        is_connected = True
        print("Connected to broker")
    else:
        is_connected = False
        print("Failed to connected with result " + str(rc))

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")

def on_publish(client, userdata, result):
        print("Msg id published: "+ str(result))

if __name__ == "__main__":
    main()