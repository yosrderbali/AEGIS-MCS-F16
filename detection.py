import cv2
import serial
import time
arduino = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)
eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_eye.xml'
)

cap = cv2.VideoCapture(0)

eyes_closed_start = None
DROWSY_THRESHOLD = 3  

print("Smart Car - Drowsiness Detection Started")
print("Press 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    eyes_detected = False

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 3)

        if len(eyes) >= 2:
            eyes_detected = True
            eyes_closed_start = None
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color,
                    (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

    if not eyes_detected and len(faces) > 0:
        if eyes_closed_start is None:
            eyes_closed_start = time.time()
        else:
            elapsed = time.time() - eyes_closed_start
            cv2.putText(frame,
                f"Eyes closed: {elapsed:.1f}s",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                0.8, (0, 0, 255), 2)

            if elapsed >= DROWSY_THRESHOLD:
                print("ALERT: Drowsiness detected!")
                arduino.write(b'1')  # Send signal to Arduino
                cv2.putText(frame,
                    "DROWSINESS ALERT!",
                    (10, 70), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 3)

    cv2.imshow('Smart Car - Driver Monitor', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()