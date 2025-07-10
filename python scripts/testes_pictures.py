from djitellopy import Tello
from drone_tello import DroneTello
import math

def main(field):
    tel = DroneTello(show_cam=True, enable_mission_pad=True)
    d = Tello()
    d.connect()
    print(f"Battery: {d.get_battery()}%")

    d.takeoff()
    height = d.get_height()
    d.move_up(100 - height)  # Ensure height is safe

    current_pos = [0, 0]
    pad_coordinates = {}
    pad_id_input = [] 

    # Input target pad IDs
    for i in range(4):
        pad_id_input.append(int(input(f"Enter pad ID #{i+1}: ")))

    # Reset to starting scan position
    d.move_forward(190)
    d.rotate_counter_clockwise(90)
    d.move_forward(95)
    d.rotate_clockwise(90)

    # ---------------------------------------------
    # Scan the field in a serpentine pattern for mission pads
    # ---------------------------------------------

    for i in range(len(field)):
        for j in range(len(field[i])):
            # Move logic: serpentine pattern
            if i % 2 == 0:  # even row: left to right
                if j > 0:
                    d.move_right(95)
            else:  # odd row: right to left
                if j > 0:
                    d.move_left(95)

            # Scan pad
            if field[i][j] == 1:
                d.move_down(50)
                pad_id = d.get_mission_pad_id()
                if pad_id != -1:
                    pad_coordinates[pad_id] = [i, j]
                d.move_up(50)

        # Move to next row if not at the last one
        if i < len(field) - 1:
            d.move_back(95)

    # Go to each specified pad

    tel._start_video_stream(d)
    tel.start_camera_display(d)

    for pad_id in pad_id_input:
        if pad_id in pad_coordinates:
            target = pad_coordinates[pad_id]
            x_diff = target[0] - current_pos[0]
            y_diff = target[1] - current_pos[1]
            
            if x_diff > 0:
                d.move_back(95 * x_diff)
            else:
                d.move_forward(95 * abs(x_diff))
            
            if y_diff > 0:
                d.move_right(95 * y_diff)
            else:
                d.move_left(95 * abs(y_diff))

            
            current_pos = target
            d.move_down(30)
            print(f"Reached pad ID {pad_id} at coordinates {target}.")
            tel.wait(3)
            tel.capture(f"pad_{pad_id}.jpg")
            data = tel.scan_qr(f"pad_{pad_id}.jpg")
            print(f"QR Data for pad ID {pad_id}: {data}")
            tel.cleanup


        else:
            print(f"Pad ID {pad_id} not found in scanned coordinates.")

    d.land()


# Fixed field map (replacing "S" with a valid value like 0)
field = [[1,  0,  1],
         [2,  2,  0],
         [1,  0,  1]]

main(field)
