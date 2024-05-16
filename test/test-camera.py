import time, libcamera
from picamera2 import Picamera2, Preview

picam = Picamera2()


picam.start()
picam.capture_file("test-python.jpg")
picam.close()