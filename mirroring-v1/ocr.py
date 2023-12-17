import cv2
import pytesseract
import os

# Define the video source (replace 'video.mp4' with your video file)
video_source = r'C:\Users\User_01\Desktop\mirroring-v1\myrecording.mp4'

# Initialize an empty string to store the extracted text
all_text = ""

# config = '--psm 6'  # Adjust the OCR configuration as needed
cap = cv2.VideoCapture(video_source)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to grayscale for better OCR results
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Perform OCR on the frame
    text = pytesseract.image_to_string(gray)  # Remove the config parameter for now

    # Append the extracted text to the all_text variable
    all_text += text + "\n"  # Add a newline between frames

    # Display the video frame (optional)
    cv2.imshow('Video', frame)

    # Exit the loop on key press (e.g., 'q')
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close any OpenCV windows
cap.release()
cv2.destroyAllWindows()

# Display all extracted text in a single window
cv2.namedWindow('Extracted Text', cv2.WINDOW_NORMAL)
cv2.imshow('Extracted Text', all_text)
cv2.waitKey(0)  # Wait until a key is pressed to close the window

# Close the window when a key is pressed
cv2.destroyAllWindows()

# Save the extracted text to a file
with open('extracted_text.txt', 'w', encoding='utf-8') as file:
    file.write(all_text)

