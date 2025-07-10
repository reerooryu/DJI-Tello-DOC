from djitellopy import Tello as t
import cv2
import time
import os


def takePic(tel):
    tel.streamon()
    
    try:

        #----------set up-------------
        
        #make directory to store pictures taken from tello.
        dir = "tello_pics"  
        os.makedirs(dir, exist_ok=True) #doesn't create directory if it already exists
        
    
        #camera on
        time.sleep(2)



        #-------Take Photo-----------
        
        #take a picture (with timestamps)
        frame = tel.get_frame_read().frame
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"tello_{timestamp}.jpg"
        filepath = os.path.join(dir,filename)
        
        
        #save image
        cv2.imwrite(filepath, frame)
        print(f"Saved {filepath}")
        
        time.sleep(1)
        
        
    except KeyboardInterrupt:
        print("interrupted by user")

    finally:
        tel.streamoff()
        print("Turned off camera")


