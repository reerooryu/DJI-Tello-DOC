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

        

#slayyy - ryu

    
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
        


