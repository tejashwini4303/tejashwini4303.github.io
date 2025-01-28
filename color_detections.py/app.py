from flask import Flask, request, render_template
import cv2
import numpy as np

app = Flask(__name__)

# Color ranges (HSV values for red, blue, etc.)
color_ranges = {
    "red": ([0, 120, 70], [10, 255, 255]),
    "blue": ([94, 80, 2], [126, 255, 255]),
    # Add more colors if needed
}

@app.route("/")
def index():
    return render_template("index.html")  # Your frontend file

@app.route("/detect", methods=["POST"])
def detect():
    color_to_detect = request.form.get("color")
    if not color_to_detect:
        return "Error: No color selected!"

    # Debugging: print selected color
    print(f"Selected color: {color_to_detect}")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return "Error: Could not access the camera."

    detected = False
    while True:
        ret, frame = cap.read()
        if not ret:
            cap.release()
            cv2.destroyAllWindows()
            return "Error: Could not read frame from camera."

        # Convert frame to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Get color range
        if color_to_detect not in color_ranges:
            cap.release()
            cv2.destroyAllWindows()
            return f"Error: Color '{color_to_detect}' not supported!"

        lower, upper = color_ranges[color_to_detect]
        lower = np.array(lower)
        upper = np.array(upper)

        # Create mask
        mask = cv2.inRange(hsv, lower, upper)

        # Detect contours
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if cv2.contourArea(contour) > 500:
                cap.release()
                cv2.destroyAllWindows()
                return f"Success! Detected {color_to_detect} color."

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return f"{color_to_detect.capitalize()} color not detected."

if __name__ == "__main__":
    app.run(debug=True)

import cv2

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Camera not accessible")
else:
    ret, frame = cap.read()
    if ret:
        cv2.imshow('Camera Frame', frame)
        cv2.waitKey(0)
    cap.release()
    cv2.destroyAllWindows()
