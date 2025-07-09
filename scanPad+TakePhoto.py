from preflight import preFlight


def scanAndPhoto(d):
    
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