import cv2
import numpy as np
import mediapipe as mp
import tensorflow.lite as tflite

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.9)
mpDraw = mp.solutions.drawing_utils

model = tflite.Interpreter(model_path='model.tflite')
model.allocate_tensors()

input_details = model.get_input_details()
output_details = model.get_output_details()

f = open('gesture.names', 'r')
classNames = f.read().split('\n')
f.close()
print(classNames)

# Initialize the webcam for Hand Gesture Recognition Python project
cap = cv2.VideoCapture(0)
_, frame = cap.read()
h,w,c = frame.shape

while True:
    detected_gesture = ''
    _, frame = cap.read()
    h,w,c = frame.shape
    frame = cv2.flip(frame, 1)
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(framergb)
    hand_landmarks = result.multi_hand_landmarks
    if hand_landmarks:
        landmarks = []
        for handLMs in hand_landmarks:
            x_max = 0
            y_max = 0
            x_min = w
            y_min = h
            for lm in handLMs.landmark:
                x, y = int(lm.x * w), int(lm.y * h)
                if x > x_max:
                    x_max = x
                if x < x_min:
                    x_min = x
                if y > y_max:
                    y_max = y
                if y < y_min:
                    y_min = y
                lmx = int(lm.x * x)
                lmy = int(lm.y * y)

                landmarks.append([lmx, lmy])
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            mpDraw.draw_landmarks(frame, handLMs, mpHands.HAND_CONNECTIONS)
            input_data = np.expand_dims(landmarks, axis=0,)
            input_data = np.float32(input_data)
            model.set_tensor(input_details[0]['index'], input_data)
            model.invoke()
            output_details = model.get_output_details()
            output_data = model.get_tensor(output_details[0]['index'])
            prediction = np.squeeze(output_data)
            # print(prediction)
            classID = np.argmax(prediction)
            detected_gesture = classNames[classID]
            
    cv2.putText(frame, detected_gesture, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
            
    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
  