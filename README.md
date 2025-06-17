# Hand-Gesture-Recognition-System
Live Link: https://hand-gesture-recognition-system-ww5e55xyuphcvfcz3reqvb.streamlit.app/
Here’s a basic implementation of hand gesture recognition
Step-by-Step Guide
1. Install Required Libraries
First, ensure you have the necessary libraries installed. You can install them using pip:
pip install flask opencv-python mediapipe numpy

3. Hand Gesture Recognition Code
Here’s a basic implementation of hand gesture recognition:
gesture.py


Explanation

Initialization:

MediaPipe's Hands class is initialized for hand tracking.
OpenCV is used to capture video from the webcam.
Gesture Recognition:

The function recognize_gesture determines the state (open/closed) of each finger based on the landmarks.
It then matches the states to predefined gestures (e.g., Open Hand, Pointing, Victory, Fist).
Main Loop:

Captures frames from the webcam.
Processes each frame with MediaPipe to detect hand landmarks.
Draws landmarks and recognized gesture on the frame.
Displays the processed frame.
Stopping Condition:

The loop stops when the 'q' key is pressed.


Explanation of New Gestures
Five Fingers Spread: Recognized when all five fingers are spread apart.
Palm Closed with Thumb Up: Recognized when the four fingers are closed, and the thumb is up.
Palm Closed with Thumb Down: Recognized when the four fingers are closed, and the thumb is down.
Shaka Sign: Recognized when the thumb and pinky fingers are extended, and other fingers are folded.
Finger Gun: Recognized when the thumb and index fingers are extended, and other fingers are folded.

Gesture Logic Details
Five Fingers Spread: Checks if all five fingers are open and significantly spread apart.
Palm Closed with Thumb Up: Four fingers closed, pinky open.
Palm Closed with Thumb Down: Four fingers closed, thumb closed and pointing downward.
Shaka Sign: Thumb and pinky open, all other fingers closed.
Finger Gun: Thumb and index open, all other fingers closed.

This code enhances the hand gesture recognition system by adding more gestures, making it suitable for more interactive applications. You can further expand it by adding more gestures or refining the existing ones based on more detailed landmark analysis.
