# MQTT publisher application for Kuksa Val
For demonstration purposes.

This application listens to separately specified paths of kuksa.val server, and then sends the value of these paths to MQTT broker.

Feeder listens to the following paths

```python
PATH_LIST = ["Vehicle.DriveTime", 
"Vehicle.Powertrain.CombustionEngine.Engine.Speed", 
"Vehicle.OBD.Speed",
"Vehicle.Powertrain.Transmission.Gear",
"Vehicle.Powertrain.CombustionEngine.Engine.TPS",
"Vehicle.Chassis.Brake.PedalPosition",
"Vehicle.TravelledDistance"]
```

and uses included ca.crt with insecure connection by default.

## Environment variables
```
KUKSAVAL_HOST: <kuksa.val server address>
KUKSAVAL_PORT: <kuksa.val server port>
MQTT_URL: <mqtt-url>
MQTT_PORT: <mqtt-port>
TOPIC_PREFIX: <prefix for mqtt topic>
```

## Topic format

Eg, for Vehicle.OBD.Speed path

```
<TOPIC_PREFIX>/Vehicle/OBD/Speed
```