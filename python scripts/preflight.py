from djitellopy import Tello as t


def preFlight():
    d = t()
    d.connect()
    if d.get_battery() < 10:
        print("Battery is low")
        return False, d
    elif d.get_temperature() > 90:
        print("Overheat warning")
        return False, d
    else:
        return True, d