#------------------------- All Packages ----------------------
import face_recognition
import cv2
import numpy as np
import os
import csv
from datetime import datetime


#------------------------- All list variables ----------------------
path = 'photos'
images = []  # LIST CONTAINING ALL THE IMAGES
className = []  # LIST CONTAINING ALL THE CORRESPONDING CLASS Names
myList = os.listdir(path)

#------------------------- Other variables -------------------------
face_names = []
name = ''

#------------------------- Counting all images in folder ----------------------

print("Total Student Detected:", len(myList))

#-------------- adding all name in className variable ----------------------

for x, cl in enumerate(myList):
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    className.append(os.path.splitext(cl)[0])
print(className)

#------------------------- copy of all name list ----------------------

students = className.copy()

#-------------- function to encode all images in a list --------------

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

#-------------- storing all encoded image in encodeListKnown --------------
encodeListKnown = findEncodings(images)
print('Encodings Completed')


#------------------------- CSV File creation of same date ----------------------
now = datetime.now()
current_date = now.strftime("%d-%m-%Y")
csv_filename = current_date + '.csv'

if not os.path.exists(csv_filename):
    # If the file exists, append data to it
    with open(csv_filename, 'w', newline='') as f:
        csv.writer(f)

f = open(csv_filename,'a',newline='')
lnwriter = csv.writer(f)
Name = 'Name'
Time = 'Time'
lnwriter.writerow(['Name', 'Time'])

#-------------- Web Cam START --------------------

print('Web Cam Starts \n')
video_capture = cv2.VideoCapture(0)

while True:
    success, img = video_capture.read()
    imgS = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

#--------- This 2 line will scan and then encode the image ----------
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)


#-----------------  loop will check the encoded image in database --------------
    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        # print(faceDis)
        matchIndex = np.argmin(faceDis)

#------------- It will mark the attendance in csv file -------------------------
        if matches[matchIndex]:
            name = className[matchIndex]
            print(name)
            if name in className:
                if name in students:
                        students.remove(name)
                        print('\n Students left for attendance : ')
                        print(students)
                        print('\n')
                        current_time = now.strftime("%H:%M")
                        lnwriter.writerow([name, current_time])

#-------------- It will show the name of image in webcam -----------------------

            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 280, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 280, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 8, y2 - 6), cv2.FONT_HERSHEY_DUPLEX,
                        1.0, (255, 255, 255), 1)




    cv2.imshow('Attendance System', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


video_capture.release()
video_capture.destroyAllWindows()