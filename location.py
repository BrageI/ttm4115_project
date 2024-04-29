from sense_hat import InputEvent, DIRECTION_MIDDLE
from shared.charger_data import *
from stmpy import Machine, Driver

sense = SenseHat()

location = Location("Location 1", sense)

driver = Driver()

location.stm = Machine(
    name="charger",
    transitions=[{"source": "initial", "target": "provide_power"}],
    obj=location,
    states=[
        {
            "name": "provide_power",
            "entry": 'start_timer("trigger_charging_increment", 1000); start_timer("send_data", 1000)',
            "trigger_charging_increment": 'increment_charge; start_timer("trigger_charging_increment", 1000)',
            "send_data": 'send_data; start_timer("send_data", 1000)',
        }
    ],
)

driver.add_machine(location.stm)

for charger in location.chargers:
    charger.stm = Machine(
        name="charger",
        transitions=[
            {"source": "initial", "target": "no_car"},
            {"trigger": "start_charging", "source": "no_car", "target": "charging"},
            {"trigger": "charge_complete", "source": "charging", "target": "no_car"},
        ],
        obj=charger,
        states=[
            {"name": "no_car", "exit": "toggle_status"},
            {
                "name": "charging",
                "entry": "read_charging_parameters",
                "trigger_charging_increment": "increment_charge",
                "exit": "toggle_status",
            },
        ],
    )
    driver.add_machine(charger.stm)

driver.start()

sense.clear()
location.render()

while True:
    event: InputEvent
    for event in sense.stick.get_events():
        if event.direction == DIRECTION_MIDDLE and event.action == "released":
            location.park_car()
