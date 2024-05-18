from picamera2 import Picamera2, Preview
import boto3
import botocore

# Set up the camera
picam = Picamera2()

# Set up the Rekognition client
rekognition = boto3.client('rekognition')
picam.start()
# Capture an image
image_capture = picam.capture_file("test-image.jpg")
picam.close()
# Open the image file
with open("test-image.jpg", "rb") as image_file:
    image_bytes = image_file.read()

# Call the Rekognition DetectLabels API
try:
    response = rekognition.detect_labels(
        Image={
            'Bytes': image_bytes
        },
        MaxLabels=10
    )
    print(response)
    # Check if any of the labels contain 'Human'
    for label in response['Labels']:
        if label['Name'] == 'Person':
            print("Humans detected in the image!")
            break
    else:
        print("No humans detected in the image.")

except botocore.exceptions.ClientError as e:
    print(f"Error: {e.response['Error']['Message']}")

# Clean up
picam.close()