import cv2

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error: Webcam could not be opened.")
else:
    print("Webcam successfully opened.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Error: Frame could not be retrieved.")
        break

    # Display the captured frame
    cv2.imshow('Webcam Test', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
