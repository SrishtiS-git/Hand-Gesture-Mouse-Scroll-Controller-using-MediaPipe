import cv2
import mediapipe as mp
import pyautogui
from time import sleep

class HandRecog:
    def __init__(self, mp_hands):
        self.mp_hands = mp_hands
        self.thumb_is_open = False
        self.index_is_open = False
        self.middle_is_open = False
        self.palm_open = False

    def update_hand_result(self, hand_landmarks):
        # Thumb tip and index finger tip detection
        thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
        index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        middle_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

        # Logic to determine if thumb and index finger are open
        if thumb_tip.y < index_tip.y:  # Thumb is higher than the index finger (open)
            self.thumb_is_open = True
        else:
            self.thumb_is_open = False
        
        if index_tip.y < thumb_tip.y:  # Index finger is higher than the thumb (open)
            self.index_is_open = True
        else:
            self.index_is_open = False
        
        # Logic to detect if middle finger is open
        if middle_tip.y < index_tip.y:  # Middle finger is higher than the index (open)
            self.middle_is_open = True
        else:
            self.middle_is_open = False

        # Detect palm open (spread out fingers)
        # Check the distance between the tips of the fingers; if they are spread out significantly, consider it an open palm
        if abs(index_tip.x - middle_tip.x) > 0.1 and abs(index_tip.y - middle_tip.y) > 0.1:
            self.palm_open = True
        else:
            self.palm_open = False

    def get_thumb_status(self):
        return self.thumb_is_open
    
    def get_index_status(self):
        return self.index_is_open
    
    def get_middle_status(self):
        return self.middle_is_open
    
    def get_palm_status(self):
        return self.palm_open


class GestureController:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.mp_draw = mp.solutions.drawing_utils
        self.hr_major = HandRecog(self.mp_hands)

    def start(self):
        # Start the webcam
        cap = cv2.VideoCapture(0)
        
        # Get screen dimensions for mouse movement
        screen_width, screen_height = pyautogui.size()
        
        while True:
            ret, image = cap.read()
            if not ret:
                print("Failed to grab frame.")
                break
            
            # Flip the image horizontally for a later selfie-view display
            image = cv2.flip(image, 1)

            # Convert the BGR image to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Process the frame and get the hand landmarks
            results = self.hands.process(image_rgb)

            # Draw the hand landmarks if they are detected
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_draw.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    self.classify_hands(results, image, hand_landmarks, screen_width, screen_height)

            # Show the image with drawn landmarks
            cv2.imshow("Hand Gesture Control", image)

            # Press 'q' to quit the application
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the webcam and close all OpenCV windows
        cap.release()
        cv2.destroyAllWindows()

    def classify_hands(self, results, image, hand_landmarks, screen_width, screen_height):
        # Classify the hands into left or right hand and update hand recognition
        self.hr_major.update_hand_result(hand_landmarks)

        # Simulate click if both thumbs and index fingers are open
        if self.hr_major.get_thumb_status() and self.hr_major.get_index_status():
            print("Both thumb and index finger are open!")
            
            # Get the position of the index finger tip for the click location
            index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
            h, w, _ = image.shape
            index_x, index_y = int(index_tip.x * w), int(index_tip.y * h)

            # Convert to screen coordinates
            screen_x = int(index_x * screen_width / w)
            screen_y = int(index_y * screen_height / h)

            # Move the mouse to the index finger's tip and click
            pyautogui.moveTo(screen_x, screen_y)
            pyautogui.click()

        # Scroll up or down if middle finger is open and index is down
        elif self.hr_major.get_middle_status() and not self.hr_major.get_index_status():
            print("Middle finger detected! Scroll down.")
            pyautogui.scroll(-10)  # Scroll down when middle finger is open
        elif self.hr_major.get_middle_status() and self.hr_major.get_index_status():
            print("Middle finger detected! Scroll up.")
            pyautogui.scroll(10)  # Scroll up when both middle and index fingers are open

        # Detect palm open for custom action
        elif self.hr_major.get_palm_status():
            print("Palm is open! Performing custom action.")
            # Add any custom action here, such as triggering a keyboard action
            # Example: Minimize all windows using a hotkey
            pyautogui.hotkey('win', 'd')  # Minimize all windows when palm is open

        else:
            # Move the mouse to the index finger's tip
            index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
            h, w, _ = image.shape
            index_x, index_y = int(index_tip.x * w), int(index_tip.y * h)

            # Convert to screen coordinates
            screen_x = int(index_x * screen_width / w)
            screen_y = int(index_y * screen_height / h)

            # Move the mouse to the index finger's tip
            pyautogui.moveTo(screen_x, screen_y)


# Main code execution
if __name__ == "__main__":
    controller = GestureController()
    controller.start()
