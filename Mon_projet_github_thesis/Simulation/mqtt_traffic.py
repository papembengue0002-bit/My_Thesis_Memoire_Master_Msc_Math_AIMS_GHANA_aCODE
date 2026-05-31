import paho.mqtt.client as mqtt
import time
import json

BROKER = "localhost"
PORT = 1883

client = mqtt.Client()
client.connect(BROKER, PORT, 60)

print(f"Envoi de trafic MQTT vers {BROKER}:{PORT}...")
for i in range(10):
    payload = {"sensor": "temp_sensor", "value": 22.5 + i * 0.1, "unit": "C"}
    message = json.dumps(payload)
    client.publish("iot/sensors/temperature", message)
    print(f" Publié : {message}")
    time.sleep(0.5)

print("Trafic MQTT done")
client.disconnect()