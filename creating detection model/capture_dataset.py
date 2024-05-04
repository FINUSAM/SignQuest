import cv2
import os

# Create a directory to save images if it doesn't exist
save_folder = 'E'
os.makedirs(save_folder, exist_ok=True)

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Counter for file naming
counter = 25

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Resize the frame to 224x224
    resized_frame = cv2.resize(frame, (224, 224))

    # Display the resized frame
    cv2.imshow('Captured Image', resized_frame)

    # Check for 'c' key pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):
        # Save the resized frame
        filename = os.path.join(save_folder, f"{counter}.jpg")
        cv2.imwrite(filename, resized_frame)
        print(f"Image saved as {filename}")
        counter += 1
    elif key == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
