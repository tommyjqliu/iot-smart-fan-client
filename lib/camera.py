import boto3
import botocore
from picamera2 import Picamera2
from datetime import datetime
import os
from asyncio import sleep, create_task
from rpi_ws281x import Color

class Camera():
    def __init__(self, smart_fan):
        self.picam = Picamera2()
        self.rekognition = boto3.client('rekognition')
        self.picam.start()
        self.active = False
        self.detect_task = create_task(self.run())
        self.smart_fan = smart_fan
        self.last_speed = 0


    def capture_image(self, file_name):
        self.picam.capture_file(file_name)
        return file_name
    
    
    async def run(self):
        await sleep(5)
        while True:
            if self.active:
               self.detect_human()
            await sleep(15)  # Wait for 15 seconds

    def detect_human(self):
        # Create a temporary directory if it doesn't exist
        temp_dir = ".temp"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        # Generate the filename with the current date and time
        # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        timestamp = "temp" # production setting
        image_file = os.path.join(temp_dir, f"{timestamp}.jpg")

        # Capture the image
        self.capture_image(image_file)

        # Open the image file
        with open(image_file, "rb") as file:
            image_bytes = file.read()

        # Call the Rekognition DetectLabels API
        try:
            response = self.rekognition.detect_labels(
                Image={'Bytes': image_bytes},
                MaxLabels=10
            )
            print(response)

            # Check if any of the labels contain 'Person'
            for label in response['Labels']:
                if label['Name'] == 'Person' and label['Confidence'] > 85:
                    print("Humans detected in the image!")
                    if self.last_speed:
                        self.smart_fan.modules["fan"].speed = self.last_speed
                        self.last_speed = 0
                        self.smart_fan.modules["led"].run_color_wipe(0,0,255)
                    return
            print("No humans detected in the image.")
            if self.smart_fan.modules["fan"].speed:
                self.last_speed = self.smart_fan.modules["fan"].speed
                self.smart_fan.modules["fan"].speed = 0
                self.smart_fan.modules["led"].run_color_wipe(0,255,0)
            return

        except botocore.exceptions.ClientError as e:
            print(f"Error: {e.response['Error']['Message']}")
            return False

    def on_close(self):
        self.detect_task.cancel()
        self.picam.close()