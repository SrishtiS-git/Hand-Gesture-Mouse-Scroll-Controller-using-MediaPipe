This Python project allows you to control your mouse and simulate actions (clicking, scrolling, minimizing windows) using hand gestures detected via your webcam. It uses MediaPipe for real-time hand landmark detection and PyAutoGUI to control mouse and keyboard actions.

✨ Features
🖱️ Move Mouse Cursor: Track the index finger to move the mouse.

👆 Click Detection: Open thumb + index finger triggers a mouse click.

🖕 Scroll Control:

Middle finger alone → Scroll down.

Middle + index finger → Scroll up.

✋ Palm Open Gesture: Triggers a "Minimize All Windows" action (Win + D).

📦 Requirements
Make sure you have the following libraries installed:

bash
Copy
Edit
pip install opencv-python mediapipe pyautogui
🛠️ How It Works
Uses cv2.VideoCapture to read webcam feed.

MediaPipe Hands detects hand landmarks.

Custom logic evaluates the state of fingers (open or closed).

Mouse movement and actions are simulated using pyautogui.

🚀 How to Run
bash
Copy
Edit
python gesture_controller.py
Press q to quit the program.

📁 File Structure
gesture_controller.py: Main file containing hand detection and action logic.

HandRecog class: Handles gesture recognition logic.

GestureController class: Orchestrates webcam capture, hand tracking, and gesture-based control.

📸 Preview
You can add a screenshot or GIF of your program in action here for better visual understanding.

⚠️ Notes
Works best in well-lit environments.

Make sure your camera is unobstructed and facing your hand.

Use steady, deliberate hand movements for optimal detection.

🧠 Future Improvements
Add support for more gestures.

Implement gesture-based app switching or volume control.

Multi-hand support for more complex interactions.

📄 License
This project is licensed under the MIT License.
