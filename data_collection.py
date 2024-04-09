from sense_hat import SenseHat
from shared.charger_data import *

sense = SenseHat()

location = Location("Location 1")

class Color:
    red = [255, 0, 0] #Color for occupied charger
    green = [0, 255, 0] #Color for free charger

# def toggle_color(color):
#     if color == Color.red:
#         color = Color.green
#     else: 
#         color = Color.red

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
        
#location.chargers[0].status = Charger.Status.NO_CAR

sense.clear()
render_led_matrix(location)

while True:
    for event in sense.stick.get_events():
        if event.action == "released":
            location.chargers[0].toggle_status()
            render_led_matrix(location)
            
    
    
    
            
            
            