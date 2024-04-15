from sense_hat import SenseHat
from shared.charger_data import *
from stmpy import Machine, Driver

sense = SenseHat()

location = Location("Location 1")

class Color:
    red = [255, 0, 0] #Color for occupied charger
    green = [0, 255, 0] #Color for free charger

def get_charger_pixels_from_top_left_pixel(top_left_pixel):
    x, y = top_left_pixel
    # Define the relative movements from the top-left pixel
    movements = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
    # Apply each movement to the top-left pixel to get each position
    pixel_array = [(x + dx, y + dy) for dx, dy in movements]
    return pixel_array

def render_charger(charger):
    render_color = Color.green
    if charger.status == Charger.Status.CHARGING:
        render_color = Color.red
        
    charger_top_left_pixel = [(charger.charger_number % 3)*3, (charger.charger_number//3)*5]
    charger_pixels = get_charger_pixels_from_top_left_pixel(charger_top_left_pixel)
    
    for pixel in charger_pixels:
        sense.set_pixel(pixel[0], pixel[1], render_color)
        

def render_led_matrix(location):
    for charger in location.chargers:
        render_charger(charger)
        
def find_free_charger_number(location):
    free_charger_number = 0
    for charger in location.chargers:
        if charger.status == Charger.Status.NO_CAR:
            return free_charger_number
        free_charger_number+=1
    return -1

def park_car(location):
    free_charger_number = find_free_charger_number(location)
    if free_charger_number != -1:
        location.chargers[free_charger_number].stm.send("start_charging")
        print("Parking car at spot", free_charger_number)
    render_led_matrix(location)


driver = Driver()

location.stm = Machine(
    name='charger',
    transitions=[{
        'source': 'initial',
        'target': 'provide_power'
    }],
    obj=location,
    states=[{
        'name': 'provide_power',
        'entry': 'start_timer("trigger_charging_increment", 1000)',
        'trigger_charging_increment': 'increment_charge; start_timer("trigger_charging_increment", 1000)'
    }])

driver.add_machine(location.stm)

for charger in location.chargers:
    charger.stm = Machine(
        name='charger',
        transitions=[{
            'source': 'initial',
            'target': 'no_car'
        }, {
            'trigger': 'start_charging',
            'source': 'no_car',
            'target': 'charging'
        }, {
            'trigger': 'charge_complete',
            'source': 'charging',
            'target': 'no_car'
        }],
        obj=charger,
        states=[{
            'name': 'no_car',
            'exit': 'toggle_status'
        }, {
            'name': 'charging',
            'trigger_charging_increment': 'increment_charge',
            'exit': 'toggle_status'
        }])
    driver.add_machine(charger.stm)
    
driver.start()

sense.clear()
render_led_matrix(location)

while True:
    for event in sense.stick.get_events():
        if event.action == "released":
            park_car(location)
            
    
    
    
            
            
            