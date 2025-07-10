from djitellopy import Tello as t

d = t()
d.connect()

print(d.get_battery())

#get MISSION PAD

    # coordList = []
    # d.takeoff()

    # d.move_down(37)

    # for j in range(3):
    #     c = 0
    #     for i in range(3):
    #         c += 1
    #         d.get_mission_pad_id()
    #         if d.get_mission_pad_id() != -1:
    #             print('Pad detected')
    #             if j == 1:
    #                 y = i
    #                 x = 2-j
    #             else:
    #                 y = i
    #                 x = j
    #             # d.go_xyz_speed_mid(0,0,20,20,int(d.get_mission_pad_id()))

    #             coordList.append([x,y])
    #             print(coordList)
    #             print(d.get_mission_pad_id())
    #         if c != 3:
    #             d.move_forward(72)
    #         else:
    #             if j == 1:
    #                 d.rotate_counter_clockwise(90)
    #                 d.move_forward(72)
    #                 d.rotate_counter_clockwise(90)
    #             elif j == 0:
    #                 d.rotate_clockwise(90)
    #                 d.move_forward(72)
    #                 d.rotate_clockwise(90)
    #             else:
    #                 d.land()
    #         time.sleep(2)
    #     time.sleep(2)



    # for n in coordList:
    #     print(n)
        
        
