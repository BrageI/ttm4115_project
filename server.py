import pickle
import json

import paho.mqtt.client as mqtt
from shared.charger_data import Charger, Location

import shared.mqtt_opts

class Server:
    def __init__(self) -> None:
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_mqtt_connect
        self.mqtt_client.on_message = self.on_mqtt_message
        self.mqtt_client.connect(shared.mqtt_opts.BROKER, shared.mqtt_opts.PORT)

        self.mqtt_client.subscribe("ttm4115/gruppe21/fromstation")

    def on_mqtt_connect(self, client, userdata, flags, rc):
        print("on_mqtt_connect(): {}".format(mqtt.connack_string(rc)))

    def on_mqtt_message(self, client, userdata, msg: mqtt.MQTTMessage):
        print("on_mqtt_message(): topic: {}".format(msg.topic))
        location: Location.Data = pickle.loads(msg.payload)
        
        available_now = len([0 for c in location.chargers if c.status == Charger.Status.NO_CAR])
        available_on_arrival = available_now
        for charger in location.chargers:
            if charger.status == Charger.Status.CHARGING and charger.charge_percentage > 75.0:
                available_on_arrival += 1

        out = {
            "location_name": location.name,
            "location_id": location.id,
            "available_chargers": available_now,
            "available_chargers_arrival": available_on_arrival,
            "total_chargers": len(location.chargers),
            "time_until_arrival": 15.0
        }

        self.mqtt_client.publish(f"ttm4115/gruppe21/fromserver", json.dumps(out))
    
        


server = Server()

server.mqtt_client.loop_forever()
