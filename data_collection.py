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
    pixel_array = []
    selected_pixel = top_left_pixel
    pixel_array.append(selected_pixel)
    selected_pixel[0]+=1
    pixel_array.append(selected_pixel)
    selected_pixel[0]+=1
    pixel_array.append(selected_pixel)
    selected_pixel[1]+=1
    pixel_array.append(selected_pixel)
    selected_pixel[1]-=1
    pixel_array.append(selected_pixel)
    selected_pixel[1]-=1
    pixel_array.append(selected_pixel)
    return pixel_array
    


        
def render_charger(charger):
    render_color = Color.green
    if charger.status == Charger.Status.CHARGING:
        render_color = Color.red
    sense.set_pixel(0, 0, render_color)
    sense.set_pixel(0, 1, render_color)
    sense.set_pixel(0, 2, render_color)
    sense.set_pixel(1, 0, render_color)
    sense.set_pixel(1, 1, render_color)
    sense.set_pixel(1, 2, render_color)


def render_led_matrix(location):
    for charger in location.chargers:
        render_charger(charger)
        
#location.chargers[0].status = Charger.Status.NO_CAR

sense.clear()
render_charger(location.chargers[0])

while True:
    for event in sense.stick.get_events():
        if event.action == "released":
            location.chargers[0].toggle_status()
            render_charger(location.chargers[0])
            
    
    
    
            
            
            