import os
import face_recognition
import pickle
import numpy as np
import cv2
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import time

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {'databaseURL': "https://facial-recognition-b6693-default-rtdb.firebaseio.com/",
                                     'storageBucket': "facial-recognition-b6693.appspot.com"
                                     })
bucket = storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3, 640)  # width
cap.set(4, 480)  # height
imgBackground = cv2.imread('resources/background 4.png')

# Importing the mode images
folderModePath = 'resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))

print('Loading encode file....')
file = open("EncodingFile.p", 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, peopleIds = encodeListKnownWithIds
print('Encode file Loaded')

modeType = 0
counter = 0
id = -1
imgPeople = []
marked_people = set()
detection_count = {}

# Flag to control the flow after first verification
face_verified = False
peopleInfo = []

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgResized = cv2.resize(imgModeList[modeType], (414, 633))
    imgBackground[44:44 + 633, 808:808 + 414] = imgResized

    if not face_verified:  # Only run facial recognition if not already verified
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                print('KNOWN FACE DETECTED')
                id = peopleIds[matchIndex]
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)

                # Check if the person has already been marked
                if id in marked_people:
                    print(f'Person {id} already marked!')
                    modeType = 3  # "Already Marked" UI
                    imgResized = cv2.resize(imgModeList[modeType], (414, 633))
                    imgBackground[44:44 + 633, 808:808 + 414] = imgResized
                    #time.sleep(2)  # Show "Already Marked" for 2 seconds
                    break  # Stop further face checks in this frame

                if id not in detection_count:
                    detection_count[id] = 0
                detection_count[id] += 1

                if detection_count[id] == 2:
                    print(f'Person {id} marked successfully!')
                    marked_people.add(id)
                    modeType = 1  # Switch to "Marked" UI
                    face_verified = True  # Face verified, enter waiting state
                    counter = 0

                    # Load user image and details
                    blob = bucket.get_blob(f'images1/{id}.png')
                    array = np.frombuffer(blob.download_as_string(), np.uint8)
                    imgPeople = cv2.imdecode(array, cv2.COLOR_BGR2RGB)
                    peopleInfo = db.reference(f"People/{id}").get()
                    print(peopleInfo)
                    break  # Exit the loop to avoid further face checks in this frame

    if face_verified:
        # Display the user info on the background UI
        if counter <= 10:
            cv2.putText(imgBackground, str(peopleInfo['NAME']), (900, 445),
                        cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 0), 1)
            cv2.putText(imgBackground, str(peopleInfo['CONSTITUENCY']), (1050, 550),
                        cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 0), 1)
            cv2.putText(imgBackground, str(id), (1006, 493),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.9, (0, 0, 0), 1)
            imgBackground[175:175 + 216, 909:909 + 216] = imgPeople

        counter += 1

        if counter >= 20:
            # Wait for a key press to proceed to the next verification
            print("Waiting for key press to proceed to the next verification...")
            key = cv2.waitKey(0)  # Wait indefinitely for a key press
            if key != -1:  # If any key is pressed, reset and move to the next verification
                print("Key pressed, proceeding to the next person.")
                face_verified = False  # Reset for the next person
                detection_count.clear()  # Clear the detection count for the next verification
                modeType = 0  # Reset the mode type
                counter = 0  # Reset counter for the next person
                peopleInfo = []  # Clear person information
        if 10 < counter < 20:
            modeType = 2
        imgResized = cv2.resize(imgModeList[modeType], (414, 633))

    # Display the UI and camera frames
    cv2.imshow("camera", img)
    cv2.imshow("Facial Verification", imgBackground)
    cv2.waitKey(1)
