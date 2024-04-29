from sense_hat import InputEvent, DIRECTION_MIDDLE, DIRECTION_LEFT, DIRECTION_RIGHT
from shared.charger_data import *
from stmpy import Machine, Driver

sense = SenseHat()



driver = Driver()

locations: list[Location] = []

for location_id in range(Location.amount):
    location = Location(location_id, f"Location {location_id}", sense)

    location.stm = Machine(
        name=f"location_{location_id}",
        transitions=[{"source": "initial", "target": "provide_power"}],
        obj=location,
        states=[
            {
                "name": "provide_power",
                "entry": f'start_timer("trigger_charging_increment", 1000); start_timer("send_data", 1000)',
                f"trigger_charging_increment": f'increment_charge; start_timer("trigger_charging_increment", 1000)',
                f"send_data": f'send_data; start_timer("send_data", 1000)',
            }
        ],
    )
    driver.add_machine(location.stm)


    for i, charger in enumerate(location.chargers):
        charger.stm = Machine(
            name=f"charger_{location_id}_{i}",
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
                    f"trigger_charging_increment": "increment_charge",
                    "exit": "toggle_status",
                },
            ],
        )
        driver.add_machine(charger.stm)

    locations.append(location)

driver.start()
#driver.start()
#driver.start()
sense.clear()

selected_location_id = 0

locations[selected_location_id].is_rendering = True
locations[selected_location_id].render()

while True:
    event: InputEvent
    for event in sense.stick.get_events():
        if event.action == "released":
            if event.direction == DIRECTION_MIDDLE:
                locations[selected_location_id].park_car()

            if event.direction == DIRECTION_LEFT:
                locations[selected_location_id].is_rendering = False
                selected_location_id = (selected_location_id - 1) % Location.amount
                locations[selected_location_id].is_rendering = True
                locations[selected_location_id].render()

            elif event.direction == DIRECTION_RIGHT:
                locations[selected_location_id].is_rendering = False
                selected_location_id = (selected_location_id + 1) % Location.amount
                locations[selected_location_id].is_rendering = True
                locations[selected_location_id].render()
