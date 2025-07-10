from preflight import preFlight
from take_pic import takePic
import time


def scanAndPhoto(d):
    
    padId = []
    #Hard coded coordinates (in cm) to avoid
    avoid = [ [0, 105], [180, 105], [0, 185], [180, 185] ]

    #hardcoded height of qr
    time.sleep(3)
    

    d.takeoff()
    d.enable_mission_pads()
    qrHeight = 80 - d.get_height()
    time.sleep(3)
    d.move_up(qrHeight)

    #pads = list(map(int, input().split(" ")))
    pads = [1, 6, 3,7]

    completed = False

    print(d.get_mission_pad_id())
    d.move_forward(80)
    d.go_xyz_speed_mid(0, 0, qrHeight, 30, pad) #- This commands sucks from long range, use to adjust minor flight inaccuracies :)
    time.sleep(1)
    takePic(d)
    time.sleep(1)

    d.land()










    # for i in range(4):
    #     #if d.get_mission_pad_id() == -1:
    #     d.move_forward(80)
    #     padId.append(d.get_mission_pad_id())
    #     if i == 3:
    #         d.rotate_clockwise(90)
    #         takePic(d)
    #         d.rotate_counter_clockwise(90)
    #     else:
    #         takePic(d)

    #     d.rotate_counter_clockwise(90)
    #     d.move_forward(90)
    # d.land()



