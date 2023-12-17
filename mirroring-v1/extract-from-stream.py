import cv2
import pytesseract

# Create a capture object for screen mirroring
cap = cv2.VideoCapture("screen:0")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Apply OCR on the frame
    text = pytesseract.image_to_string(frame)

    if text.strip():  # Check if text is not empty
        print("Extracted Text:")
        print(text)
        print('-' * 30)  # Separator for clarity

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture object
cap.release()
cv2.destroyAllWindows()
