import boto3
import botocore
from picamera2 import Picamera2
from datetime import datetime
import os

class Camera():
    def __init__(self):
        self.picam = Picamera2()
        self.rekognition = boto3.client('rekognition')
        self.picam.start()

    def capture_image(self, file_name):
        self.picam.capture_file(file_name)
        return file_name

    def detect_human(self):
        # Create a temporary directory if it doesn't exist
        temp_dir = ".temp"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        # Generate the filename with the current date and time
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
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
                if label['Name'] == 'Person':
                    print("Humans detected in the image!")
                    return True
            print("No humans detected in the image.")
            return False

        except botocore.exceptions.ClientError as e:
            print(f"Error: {e.response['Error']['Message']}")
            return False

    def on_close(self):
        self.picam.close()