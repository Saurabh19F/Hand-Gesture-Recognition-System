from flask import Flask, render_template, request, Response
import cv2
import numpy as np
import mediapipe as mp
import base64

app = Flask("GestureRecognition")

# Initialize MediaPipe Hand model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

def recognize_gesture(landmarks):
    thumb_is_open = landmarks[4].x < landmarks[3].x < landmarks[2].x
    index_is_open = landmarks[8].y < landmarks[6].y
    middle_is_open = landmarks[12].y < landmarks[10].y
    ring_is_open = landmarks[16].y < landmarks[14].y
    pinky_is_open = landmarks[20].y < landmarks[18].y

    if thumb_is_open and index_is_open and middle_is_open and ring_is_open and pinky_is_open:
        return "Open Hand"
    elif not thumb_is_open and index_is_open and not middle_is_open and not ring_is_open and not pinky_is_open:
        return "Pointing"
    elif not thumb_is_open and index_is_open and middle_is_open and not ring_is_open and not pinky_is_open:
        return "Victory"
    elif not thumb_is_open and not index_is_open and not middle_is_open and not ring_is_open and not pinky_is_open:
        return "Fist"
    else:
        return "Unknown Gesture"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_frame', methods=['POST'])
def process_frame():
    try:
        data = request.json['image']
        img_data = base64.b64decode(data.split(',')[1])
        np_arr = np.frombuffer(img_data, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # Convert to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                gesture = recognize_gesture(hand_landmarks.landmark)
                cv2.putText(frame, gesture, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = base64.b64encode(buffer).decode('utf-8')
        return {"image": f"data:image/jpeg;base64,{frame_bytes}"}

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000, debug=True)
