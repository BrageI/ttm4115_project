from __future__ import annotations
import pickle
import random

from sense_hat import SenseHat
from stmpy import Machine
import paho.mqtt.client as mqtt

import shared.mqtt_opts

def get_charger_pixels_from_top_left_pixel(top_left_pixel):
    x, y = top_left_pixel
    # Define the relative movements from the top-left pixel
    movements = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
    # Apply each movement to the top-left pixel to get each position
    pixel_array = [(x + dx, y + dy) for dx, dy in movements]
    return pixel_array


class Color:
    red = [255, 0, 0]  # Color for occupied charger
    green = [0, 255, 0]  # Color for free charger



class Charger:
    location: Location

    sense: SenseHat
    stm: Machine

    class Status:
        NO_CAR = 0
        CHARGING = 1


    class Data:
        charger_number: int
        status: Charger.Status
        charge_percentage: float = 20.0  # [%] 0.0 - 100.0
        charging_rate: float = 8.0  # [%/s]

    def __init__(self, number, location: Location, sense: SenseHat):
        self.data = self.Data()
        self.data.charger_number = number
        self.data.status = Charger.Status.NO_CAR

        self.location = location
        self.sense = sense

    def read_charging_parameters(self):
        self.data.charge_percentage = random.uniform(10.0, 40.0)
        self.data.charging_rate = random.uniform(1.0, 2.0)

    def toggle_status(self):
        if self.data.status == Charger.Status.NO_CAR:
            self.data.status = Charger.Status.CHARGING
        else:
            self.data.status = Charger.Status.NO_CAR
            self.data.charge_percentage = 0.0
        self.render()

    def set_status(self, new_status):
        self.data.status = new_status

    def increment_charge(self):
        self.data.charge_percentage += self.data.charging_rate
        if self.data.charge_percentage >= 100.0:
            self.data.charge_percentage = 100.0
            self.stm.send("charge_complete")
        print(f"Charger {self.data.charger_number}: at {self.data.charge_percentage}%")

    def render(self):
        render_color = Color.green
        if self.data.status == Charger.Status.CHARGING:
            render_color = Color.red

        charger_top_left_pixel = [
            (self.data.charger_number % 3) * 3,
            (self.data.charger_number // 3) * 5,
        ]
        charger_pixels = get_charger_pixels_from_top_left_pixel(charger_top_left_pixel)

        for pixel in charger_pixels:
            self.sense.set_pixel(pixel[0], pixel[1], render_color)


class Location:
    sense: SenseHat

    stm: Machine

    def __init__(self, name: str, sense: SenseHat):
        self.name: str = name
        self.sense = sense
        self.chargers: list[Charger] = [Charger(i, self, sense) for i in range(6)]

        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_mqtt_connect
        self.mqtt_client.connect(shared.mqtt_opts.BROKER, shared.mqtt_opts.PORT)

    def on_mqtt_connect(self, client, userdata, flags, rc):
        print("on_mqtt_connect(): {}".format(mqtt.connack_string(rc)))

    def increment_charge(self):
        for charger in self.chargers:
            charger.stm.send("trigger_charging_increment")

    def render(self):
        for charger in self.chargers:
            charger.render()

    def find_free_charger_number(self):
        free_charger_number = 0
        for charger in self.chargers:
            if charger.data.status == Charger.Status.NO_CAR:
                return free_charger_number
            free_charger_number += 1
        return -1

    def park_car(self):
        free_charger_number = self.find_free_charger_number()
        if free_charger_number != -1:
            self.chargers[free_charger_number].stm.send("start_charging")
            print("Parking car at spot", free_charger_number)

    def send_data(self):
        out = list()
        for charger in self.chargers:
            out.append(charger.data)
        self.mqtt_client.publish(f"ttm4115/gruppe21/fromstation", pickle.dumps(out))
        
