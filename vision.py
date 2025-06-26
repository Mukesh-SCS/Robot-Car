import time
from picamera2 import Picamera2
import cv2


def detect_objects(frame):
    """Placeholder for your model inference"""
    return []


def main():
    picam2 = Picamera2()
    picam2.start()
    try:
        while True:
            frame = picam2.capture_array()
            boxes = detect_objects(frame)
            for (x, y, w, h) in boxes:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.imshow("Vision", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            time.sleep(0.01)
    except Exception as e:
        print(f"Vision error: {e}")
    finally:
        picam2.stop()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()