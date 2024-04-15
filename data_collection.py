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
    
    #print("Top left: ", charger_top_left_pixel)
    
    charger_pixels = get_charger_pixels_from_top_left_pixel(charger_top_left_pixel)
    
    #print("Charger pixels: ", charger_pixels)
    
    for pixel in charger_pixels:
        #print("Pixel position: ", pixel[0], pixel[1])
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
    render_led_matrix(location)
        
#Initial transition
t0 = {
    'source': 'initial',
    'target': 'no_car'
}

#Transition from no_car to charging
t1 = {
    'trigger': 'start_charging',
    'source': 'no_car',
    'target': 'charging'
}

#Transition from charging to no_car
t2 = {
    'trigger': 'charge_complete',
    'source': 'charging',
    'target': 'no_car'
}

#Trigger to increment charge in charing state
t3 = {
    'trigger': 't',
    'source': 'charging',
    'target': 'charging',
    'effect': 'increment_charge'
}

#States

no_car = {
    'name': 'no_car',
    'entry': 'toggle_status'
}

charging = {
    'name': 'charging',
    'entry': 'toggle_status; start_timer("t", 1000)'
}

for charger in location.chargers:
    machine = Machine(name='charger', transitions=[t0, t1, t2, t3], obj=charger, states=[no_car, charging])
    charger.stm = machine



sense.clear()
render_led_matrix(location)

while True:
    for event in sense.stick.get_events():
        if event.action == "released":
            park_car(location)
            
    
    
    
            
            
            