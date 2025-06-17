import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import av

st.set_page_config(page_title="Hand Gesture Recognition", layout="centered")
st.title("🖐️ Hand Gesture Recognition (Streamlit + WebRTC)")

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Gesture recognition logic
def recognize_gesture(landmarks):
    thumb = landmarks[4].x < landmarks[3].x < landmarks[2].x
    index = landmarks[8].y < landmarks[6].y
    middle = landmarks[12].y < landmarks[10].y
    ring = landmarks[16].y < landmarks[14].y
    pinky = landmarks[20].y < landmarks[18].y

    if all([thumb, index, middle, ring, pinky]):
        return " Open Hand"
    elif not thumb and index and not middle and not ring and not pinky:
        return " Pointing"
    elif not thumb and index and middle and not ring and not pinky:
        return " Victory"
    elif not thumb and not index and not middle and not ring and not pinky:
        return " Fist"
    elif not thumb and not index and not middle and ring and pinky:
        return " Rock Sign"
    elif thumb and not index and not middle and not ring and not pinky:
        return " Thumbs Up"
    elif not thumb and not index and not middle and not ring and not pinky and landmarks[4].y > landmarks[3].y > landmarks[2].y:
        return " Thumbs Down"
    elif thumb and index and not middle and not ring and pinky:
        return " OK Sign"
    elif not thumb and index and middle and ring and not pinky:
        return " Three Fingers Up"
    elif not thumb and index and middle and ring and pinky:
        return " Four Fingers Up"
    elif thumb and not index and not middle and not ring and pinky:
        return " Call Me"
    elif not thumb and index and middle and not ring and not pinky:
        return " Peace Sign"
    elif thumb and index and middle and ring and pinky and all([
        abs(landmarks[8].x - landmarks[4].x) > 0.1,
        abs(landmarks[12].x - landmarks[4].x) > 0.1,
        abs(landmarks[16].x - landmarks[4].x) > 0.1,
        abs(landmarks[20].x - landmarks[4].x) > 0.1]):
        return " Five Fingers Spread"
    elif not thumb and not index and not middle and not ring and pinky:
        return " Palm Closed with Thumb Up"
    elif not thumb and not index and not middle and not ring and not pinky and landmarks[4].y > landmarks[3].y:
        return " Palm Closed with Thumb Down"
    elif thumb and not index and not middle and not ring and pinky:
        return " Shaka Sign"
    elif thumb and index and not middle and not ring and not pinky:
        return " Finger Gun"
    else:
        return " Unknown"

# Define video transformer class
class VideoProcessor(VideoTransformerBase):
    def transform(self, frame):
        image = frame.to_ndarray(format="bgr24")
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                gesture = recognize_gesture(hand_landmarks.landmark)
                cv2.putText(image, gesture, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 20, 147), 2)

        return image

# Activate webcam in browser
webrtc_streamer(key="gesture-detect", video_transformer_factory=VideoProcessor)
