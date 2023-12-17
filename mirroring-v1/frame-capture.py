import cv2
import pytesseract
from ppadb.client import Client as AdbClient

# Connect to your Android device or emulator
client = AdbClient(host="127.0.0.1", port=5037)
devices = client.devices()

if len(devices) == 0:
    print('No devices')
    quit()

device = devices[0]

# Open the video source
video_source = r'C:\Users\User_01\Desktop\mirroring-v1\myrecording.mp4'
cap = cv2.VideoCapture(video_source)

# Check if the video source was opened successfully
if not cap.isOpened():
    print("Error: Could not open video source")
    exit()

# Create a VideoWriter to record the video
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (frame_width, frame_height))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to grayscale for better OCR results
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Perform OCR on the frame
    text = pytesseract.image_to_string(gray)

    # Print the extracted text
    print(text)

    # Write the frame to the output video
    out.write(frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and VideoWriter
cap.release()
out.release()

# Close all OpenCV windows
cv2.destroyAllWindows()
