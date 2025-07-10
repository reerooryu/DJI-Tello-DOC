##xperimental

from djitellopy import Tello
import cv2
import os
import threading
import time

"""
DroneTello - Enhanced Tello Drone Controller

BASIC USAGE:
    # Simple connection and flight
    drone = DroneTello()
    drone.takeoff()
    drone.wait(2)
    drone.land()
    drone.cleanup()

CAMERA USAGE:
    # With live camera display
    drone = DroneTello(show_cam=True)
    drone.takeoff()
    drone.capture("my_photo.jpg")           # Take picture
    data = drone.scan_qr("my_photo.jpg")    # Read QR code
    drone.land()
    drone.cleanup()

MISSION PAD USAGE:
    # With mission pad detection
    drone = DroneTello(enable_mission_pad=True)
    drone.takeoff()
    # Use mission pad commands like go_xyz_speed_mid()
    drone.land()
    drone.cleanup()

MOVEMENT COMMANDS (inherited from Tello):
    drone.move_up(50)        # Move up 50cm
    drone.move_down(50)      # Move down 50cm
    drone.move_forward(50)   # Move forward 50cm
    drone.move_back(50)      # Move backward 50cm
    drone.move_left(50)      # Move left 50cm
    drone.move_right(50)     # Move right 50cm
    drone.rotate_clockwise(90)        # Rotate 90 degrees clockwise
    drone.rotate_counter_clockwise(90) # Rotate 90 degrees counter-clockwise
"""

class DroneTello(Tello):
    """
    Enhanced Tello drone class with camera display and mission pad support.
    
    Usage:
        drone = DroneTello(show_cam=True, enable_mission_pad=True)
        drone.takeoff()
        drone.capture("photo.jpg")
        data = drone.scan_qr("photo.jpg")
        drone.land()
    """
    def __init__(self, show_cam=False, enable_mission_pad=False):
        """
        Initialize DroneTello with optional camera display and mission pads.
        
        Args:
            show_cam (bool): If True, shows live camera feed in a window
            enable_mission_pad (bool): If True, enables mission pad detection
            
        Usage:
            drone = DroneTello()  # Basic connection
            drone = DroneTello(show_cam=True)  # With camera display
            drone = DroneTello(show_cam=True, enable_mission_pad=True)  # Full features
        """
        super().__init__()

        # connect to the Tello drone
        print("Connecting to Tello drone...")
        self.connect()
        print(f"Battery: {self.get_battery()}%")
        print(f"Temperature: {self.get_temperature()}°C")
        
        # camera display attribute
        self.show_camera = False
        self._camera_thread = None
        self._stream_active = False
        
        # landing status tracking
        self.is_land = True  # Drone starts on ground
        
        # show camera in realtime if requested
        if show_cam:
            # start video stream
            self._start_video_stream()
            self.start_camera_display()
        
        # enable mission pads if requested
        if enable_mission_pad:
            print("Enabling mission pads...")
            self.enable_mission_pads()
        
        print("Drone Tello initialized successfully.")

    def __del__(self):
        """
        Destructor to ensure cleanup when object is deleted.
        
        Usage: Automatically called when drone object goes out of scope
        """
        try:
            self.cleanup()
        except:
            pass
    
    def _start_video_stream(self):
        """
        Start video stream with error handling and retry mechanism.
        
        Usage: Internal method called automatically when needed
        """
        try:
            print("Starting video stream...")
            self.streamon()
            time.sleep(5)  # Wait longer for stream to initialize
            
            # Try multiple times to get frame
            for _ in range(3):
                try:
                    test_frame = self.get_frame_read().frame
                    
                    # Convert BGR to RGB
                    test_frame_rgb = cv2.cvtColor(test_frame, cv2.COLOR_BGR2RGB)
                    
                    if test_frame_rgb is not None:
                        self._stream_active = True
                        print("Video stream started successfully")
                        return
                except:
                    time.sleep(1)
                    continue
                    
            print("Warning: Video stream started but no frames available")
            self._stream_active = False
        except Exception as e:
            print(f"Failed to start video stream: {e}")
            self._stream_active = False

    def start_camera_display(self):
        """
        Start displaying camera feed in a GUI window.
        
        Usage:
            drone.start_camera_display()  # Opens camera window
            # Press 'q' in the window to close it
        """
        if not self._stream_active:
            self._start_video_stream()
            
        if self._stream_active:
            self.show_camera = True
            self._camera_thread = threading.Thread(target=self._camera_loop)
            self._camera_thread.daemon = True
            self._camera_thread.start()
        
    def stop_camera_display(self):
        """
        Stop displaying camera feed and close the window.
        
        Usage:
            drone.stop_camera_display()  # Closes camera window
        """
        self.show_camera = False
        if self._camera_thread:
            self._camera_thread.join()
        cv2.destroyAllWindows()
        
    def _camera_loop(self):
        """
        Internal method to continuously display camera feed.
        
        Usage: Called automatically by start_camera_display()
        """
        while self.show_camera and self._stream_active:
            try:
                frame = self.get_frame_read().frame
                
                # Convert BGR to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                if frame_rgb is not None:
                    cv2.imshow("Tello Camera Feed", frame_rgb)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        self.stop_camera_display()
                        break
                else:
                    time.sleep(0.1)
            except Exception as e:
                print(f"Camera error: {e}")
                self._stream_active = False
                break

    def capture(self, filename="tello_picture.jpg"):
        """
        Capture current frame and save it to pictures/ folder in RGB format.
        
        Args:
            filename (str): Name of the image file to save
            
        Returns:
            str: Full path of saved image file, or None if failed
            
        Usage:
            drone.capture()  # Saves as "tello_picture.jpg"
            drone.capture("my_photo.jpg")  # Saves with custom name
        """
        if not self._stream_active:
            self._start_video_stream()
            
        if not self._stream_active:
            print("Cannot capture: Video stream not available")
            return None
            
        try:
            frame = self.get_frame_read().frame
            
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            if frame_rgb is None:
                print("No frame available for capture")
                return None
                
            path = "pictures/"
            if not os.path.exists(path):
                os.makedirs(path)
                
            full_path = path + filename
            cv2.imwrite(full_path, frame_rgb)
            print(f"Picture saved as {full_path}")
            return full_path
        except Exception as e:
            print(f"Capture error: {e}")
            return None
    
    def scan_qr(self, filename):
        """
        Scan QR code from saved image file and return decoded data.
        
        Args:
            filename (str): Name of the image file in pictures/ folder
            
        Returns:
            str: Decoded QR code data, or None if no QR code found
            
        Usage:
            data = drone.scan_qr("my_photo.jpg")
            if data:
                print(f"QR code says: {data}")
        """
        path = "pictures/"
        full_path = path + filename
        
        if not os.path.exists(full_path):
            print(f"File {full_path} not found")
            return None
            
        try:
            frame = cv2.imread(full_path)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            qcd = cv2.QRCodeDetector()
            data, points, _ = qcd.detectAndDecode(gray)
            
            if points is not None and data:
                print(f"QR Code detected in {filename}: {data}")
                return data
            else:
                print(f"No QR code detected in {filename}")
                return None
        except Exception as e:
            print(f"QR scan error: {e}")
            return None
        
    def wait(self, seconds):
        """
        Wait for a specified number of seconds with status messages.
        
        Args:
            seconds (int/float): Number of seconds to wait
            
        Usage:
            drone.wait(2)      # Wait 2 seconds
            drone.wait(0.5)    # Wait half a second
        """
        print(f"Waiting for {seconds} seconds...")
        time.sleep(seconds)
        print("Wait complete.")
        
    def takeoff(self):
        """
        Take off and update landing status.
        
        Usage:
            drone.takeoff()  # Drone takes off and is_land becomes False
        """
        super().takeoff()
        self.is_land = False
        
    def land(self):
        """
        Land and update landing status.
        
        Usage:
            drone.land()  # Drone lands and is_land becomes True
        """
        super().land()
        self.is_land = True
        
    def cleanup(self):
        """
        Clean shutdown of drone resources to prevent errors.
        
        Usage:
            drone.cleanup()  # Call before ending program
            # Or use in finally block for automatic cleanup
        """
        try:
            self.stop_camera_display()
            
            # Land if drone is still flying
            if not self.is_land:
                print("Landing drone before cleanup...")
                try:
                    self.land()
                except Exception as e:
                    print(f"Warning: Could not land drone: {e}")
            
            # Stop video stream
            if hasattr(self, '_stream_active') and self._stream_active:
                try:
                    self.streamoff()
                    print("Video stream stopped")
                except Exception as e:
                    print(f"Warning: Could not stop video stream: {e}")
                    
        except Exception as e:
            print(f"Cleanup error: {e}")
        