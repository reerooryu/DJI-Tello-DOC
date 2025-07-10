from djitellopy import Tello as t
import cv2
import time
import os

from preflight import preFlight

def Stream(tel):
    tel.streamon()
    while True:
            #-------STREAM TO PC----------
        
        frame = tel.get_frame_read().frame

        frame = cv2.resize(frame, (960, 720))

        cv2.imshow("Tello live feed", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break




