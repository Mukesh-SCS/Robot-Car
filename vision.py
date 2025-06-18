# vision.py

import cv2
# Placeholder imports for inference
# e.g., import tflite_runtime.interpreter as tflite


def init_camera():
    """
    Initialize camera for frame capture.
    """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Cannot open camera")
    return cap


def capture_frame(cap):
    """
    Capture a single frame from the camera.
    """
    ret, frame = cap.read()
    if not ret:
        raise RuntimeError("Failed to capture image")
    return frame


def detect_objects(frame):
    """
    Placeholder for object detection inference.
    Returns a list of bounding boxes [(x, y, w, h), ...].
    """
    # TODO: load and run your model here
    return []


def main():
    cap = init_camera()
    try:
        while True:
            frame = capture_frame(cap)
            boxes = detect_objects(frame)
            for (x, y, w, h) in boxes:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.imshow("Vision", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()