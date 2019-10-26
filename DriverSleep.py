import cv2
import face_recognition
import sys
import numpy as np
import time

cap = cv2.VideoCapture(0)
eye_1 = []
eye_2 = []
ctr1 = 0
ctr2 = 0
t1 = time.time()

prevCtr = 0
inc = 0


while True:
    t2 = time.time()
    if t2-t1 > 3:
        if np.average([eye_1[-1], eye_1[-2], eye_1[-3]]) <= 12:
            ctr1 += 1
        if np.average([eye_2[-1], eye_2[-2], eye_2[-3]]) <= 12:
            ctr2 += 1
    if (ctr1+ctr2)/2 - prevCtr > 0:
        inc += 1
    else:
        inc = 0
    if inc >= 3:
        print('Sleeping')
    else:
        print('Awake')

    _, frame = cap.read()
    rgb_frame = frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_frame)
    face_landmarks = face_recognition.face_landmarks(rgb_frame)

    for poly in face_landmarks:
        pts = np.array([poly['left_eye']], np.int32)
        pts = pts.reshape((-1, 1, 2))

        eye_1.append((poly['left_eye'][5][1] +
                      poly['left_eye'][4][1] +
                      poly['left_eye'][0][1]) -
                     (poly['left_eye'][2][1] +
                      poly['left_eye'][3][1] +
                      poly['left_eye'][1][1]))

        eye_2.append((poly['right_eye'][5][1] +
                      poly['right_eye'][4][1] +
                      poly['right_eye'][0][1]) -
                     (poly['right_eye'][2][1] +
                      poly['right_eye'][3][1] +
                      poly['right_eye'][1][1]))

        cv2.polylines(frame, [pts], True, (255, 255, 255))
        pts = np.array([poly['right_eye']], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(frame, [pts], True, (255, 255, 255))

    for(y, w, h, x) in face_locations:
        cv2.rectangle(frame, (x, y), (w, h), (0, 255, 255), 2)
    cv2.imshow('Video', frame)
    prevCtr = (ctr1+ctr2)/2

    if cv2.waitKey(1) & 0xFF == ord('q'):
        sys.exit()

cap.release()
cv2.destroyAllWindows()
