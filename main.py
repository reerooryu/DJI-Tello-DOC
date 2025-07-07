from djitellopy import Tello as t
import time
import math
from preflight import preFlight
from take_pic import takePic
from stream import Stream

import threading

# def preFlight():
#     d = t()
#     d.connect()
#     if d.get_battery() < 10:
#         print("Battery is low")
#         return False, d
#     elif d.get_temperature() > 100:
#         print("Overheat warning")
#         print(d)
#         return False, d
#     else:
#         return True, d

def getTime(func):
    def wrapper(*args):
        start = time.time()
        func(d)
        end = time.time()
        print(f"Took {end-start} seconds to run")
    return wrapper

@getTime #get runtime for code
def main(d):

    padId = []

    d.takeoff()
    d.enable_mission_pads()
    d.move_up(75 - d.get_height())


    for i in range(4):
        #if d.get_mission_pad_id() == -1:
        d.move_forward(80)
        padId.append(d.get_mission_pad_id())
        if i == 3:
            d.rotate_clockwise(90)
            takePic(d)
            d.rotate_counter_clockwise(90)
        else:
            takePic(d)

        d.rotate_counter_clockwise(90)
        d.move_forward(90)
    d.land()
        

#slayyy - ry

    
#----------------------------------- RUNNING --------------------------

canFly, d = preFlight()
if canFly:
    print("Start up successful")
    t1 = threading.Thread(target=Stream, args=(d,))
    t2 = threading.Thread(target=main, args=(d,))

    
    t1.start()
    t2.start()

    t1.join()
    t2.join()

else:
    pass
        


