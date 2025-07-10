from djitellopy import Tello as t
import time
import math
import logging
logging.getLogger("djitellopy").setLevel(logging.ERROR)


#Importing functions from different files
from preflight import preFlight
from take_pic import takePic
from stream import Stream
from scanAndPhoto import scanAndPhoto

import threading


def getTime(func):
    def wrapper(*args):
        start = time.time()
        func(d)
        end = time.time()
        print(f"Took {end-start} seconds to run")
    return wrapper


#---------------------------------Main----------------------------------
@getTime #get runtime for code
def main(d):
    scanAndPhoto(d)
    
        

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

        


