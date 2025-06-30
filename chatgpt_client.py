import cv2
import numpy as np
from picamera2 import Picamera2

# 1) Load the SSD model
net = cv2.dnn.readNetFromTensorflow(
    "models/frozen_inference_graph.pb",
    "models/ssd_mobilenet_v2_coco_2018_03_29.pbtxt"
)

# 2) Start Picamera2 for BGR frames
picam2 = Picamera2()
cfg = picam2.create_preview_configuration(main={"size": (640, 480), "format": "BGR888"})
picam2.configure(cfg)
picam2.start()

while True:
    frame = picam2.capture_array()  # H×W×3 BGR image

    # 3) Run it through the network
    blob = cv2.dnn.blobFromImage(frame, size=(300, 300), swapRB=False, crop=False)
    net.setInput(blob)
    detections = net.forward()

    # 4) Draw green boxes on any detection >50%
    h, w = frame.shape[:2]
    for i in range(detections.shape[2]):
        conf = float(detections[0, 0, i, 2])
        if conf > 0.5:
            x1, y1, x2, y2 = (detections[0, 0, i, 3:7] * [w, h, w, h]).astype(int)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)

    cv2.imshow("Detections", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

picam2.stop()
cv2.destroyAllWindows()
