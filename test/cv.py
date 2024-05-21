import cv2

# Open the default camera
cap = cv2.VideoCapture(-1)

if not cap.isOpened():
    print("Error: Could not open video device.")
    exit()

# Set camera resolution (optional)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Read a frame from the camera
ret, frame = cap.read()
print(ret, frame)
if ret:
    # Save the frame as an image file
    cv2.imwrite('captured_image.jpg', frame)
    print("Image captured and saved as 'captured_image.jpg'")
else:
    print("Error: Could not read frame.")

# Release the camera
cap.release()

# Close any OpenCV windows
cv2.destroyAllWindows()
