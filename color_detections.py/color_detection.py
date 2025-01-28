


import cv2
import numpy as np
import speech_recognition as sr
import pyttsx3
import sys

sys.stdout = sys.stderr  # Redirect print statements to the console

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Define color ranges (Red, Green, Blue, Yellow, Orange, Purple, Pink)
color_ranges = {
    "red": ([0, 120, 70], [10, 255, 255]),
    "green": ([35, 50, 50], [85, 255, 255]),
    "blue": ([100, 100, 50], [140, 255, 255]),
    "yellow": ([20, 100, 100], [30, 255, 255]),
    "orange": ([10, 100, 100], [25, 255, 255]),
    "purple": ([130, 50, 50], [160, 255, 255]),
    "pink": ([140, 50, 50], [180, 255, 255]),
}

# Function to announce messages
def speak(message):
    engine.say(message)
    engine.runAndWait()

# Function to detect the color
def detect_color(color_to_detect):
    speak("Starting the camera.")
    print("Starting camera...")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        speak("Error. Could not access the camera.")
        print("Error: Could not access the camera.")
        return

    color_detected = False  # Flag to indicate whether the color has been detected

    while True:
        ret, frame = cap.read()
        if not ret:
            speak("Error. Failed to grab frame.")
            print("Error: Failed to grab frame.")
            break

        # Convert frame to HSV and try detecting the color
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower, upper = color_ranges.get(color_to_detect, ([0, 0, 0], [0, 0, 0]))
        lower = np.array(lower)
        upper = np.array(upper)
        mask = cv2.inRange(hsv, lower, upper)

        # Find contours of the detected color
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if cv2.contourArea(contour) > 500:  # Threshold to ignore small detections
                cv2.drawContours(frame, [contour], -1, (0, 255, 0), 3)
                if not color_detected:  # Only speak the message once
                    speak(f"{color_to_detect.capitalize()} color detected.")
                    print(f"{color_to_detect.capitalize()} color detected!")
                    color_detected = True  # Set the flag to true

                cv2.putText(frame, f"Detected {color_to_detect}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        if not contours:  # Reset color detected flag if no contours found
            color_detected = False

        cv2.imshow("Color Detection", frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Function to get the input method
def get_input_method():
    speak("Choose the input method. Press one for voice command or two for typing.")
    print("Choose the input method:")
    print("1. Voice Command")
    print("2. Type the color")

    choice = input("Enter 1 for Voice or 2 for Text: ").strip()

    if choice == "1":
        speak("You selected voice command.")
        return "voice"
    elif choice == "2":
        speak("You selected text input.")
        return "text"
    else:
        speak("Invalid choice. Defaulting to voice command.")
        print("Invalid choice. Defaulting to voice command.")
        return "voice"

# Function to listen for a color via microphone
def listen_for_color():
    speak("Please say the name of the color you want to detect.")
    print("Listening for color...")
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            color = recognizer.recognize_google(audio).lower()
            speak(f"You said {color}.")
            print(f"Recognized color: {color}")
            return color
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            print("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            speak("Speech recognition service is unavailable.")
            print("Speech recognition service is unavailable.")
            return None

# Main function to start the program
def main():
    input_method = get_input_method()

    if input_method == "voice":
        color = listen_for_color()
    elif input_method == "text":
        speak("Please type the color you want to detect.")
        color = input("Type the color name (e.g., red, blue, green): ").strip().lower()

    if color and color in color_ranges:
        speak(f"Looking for {color} color.")
        print(f"Looking for {color} color.")
        detect_color(color)
    else:
        speak("Invalid color or no color command received. Please try again.")
        print("Invalid color or no color command received.")

if __name__ == "__main__":
    main()



