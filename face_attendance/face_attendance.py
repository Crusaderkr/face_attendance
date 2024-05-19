import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

# Path to the directory containing images of known people
KNOWN_FACES_DIR = 'known_faces'
# Function to load and encode images of known people
def load_known_faces():
    known_faces = []
    known_names = []
    for name in os.listdir(KNOWN_FACES_DIR):
        # Ignore desktop.ini files or any other non-directory entries
        if os.path.isdir(os.path.join(KNOWN_FACES_DIR, name)):
            for filename in os.listdir(os.path.join(KNOWN_FACES_DIR, name)):
                image_path = os.path.join(KNOWN_FACES_DIR, name, filename)
                if os.path.isfile(image_path):
                    image = face_recognition.load_image_file(image_path)
                    encoding = face_recognition.face_encodings(image)[0]
                    known_faces.append(encoding)
                    known_names.append(name)
    return known_faces, known_names

# Load known faces
known_faces, known_names = load_known_faces()



# Initialize webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        break

    # Convert frame from BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Find all face locations and encodings in the current frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Loop through each face found in the frame
    for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
        # Check if the face matches any known faces
        matches = face_recognition.compare_faces(known_faces, face_encoding)
        name = "Unknown"


        # Draw a rectangle around the face and label it with the name
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # Display the frame
    cv2.imshow('Face Recognition', frame)

    # Check for 'q' key to close the program
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
