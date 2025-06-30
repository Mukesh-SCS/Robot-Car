#!/usr/bin/env python3
import os
import time
import base64

import cv2
import numpy as np
from dotenv import load_dotenv
from picamera2 import Picamera2
from openai import OpenAI

# 1) Load your OpenAI key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("Missing OPENAI_API_KEY in environment")

# 2) Instantiate the v1+ client
client = OpenAI(api_key=api_key)

def identify(image_bytes: bytes, prompt: str = "What do you see?") -> str:
    b64 = base64.b64encode(image_bytes).decode("utf-8")
    content = [
        {"type": "text", "text": prompt},
        {"type": "image_url", "image_url": {
            "url": f"data:image/jpeg;base64,{b64}",
            "detail": "auto"
        }}
    ]
    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": content}],
        temperature=0.0,
    )
    return resp.choices[0].message.content.strip()

# 3) Load MobileNet-SSD
PROTOTXT = "models/MobileNetSSD_deploy.prototxt"
MODEL    = "models/MobileNetSSD_deploy.caffemodel"
net = cv2.dnn.readNetFromCaffe(PROTOTXT, MODEL)
CLASS_NAMES = [
    "background","aeroplane","bicycle","bird","boat","bottle","bus","car",
    "cat","chair","cow","diningtable","dog","horse","motorbike","person",
    "pottedplant","sheep","sofa","train","tvmonitor"
]

# 4) Setup Picamera2 to output 3-channel BGR888 frames
picam2 = Picamera2()
video_config = picam2.create_video_configuration(main={
    "size":   (640, 480),
    "format": "BGR888"    # ← three-channel BGR for OpenCV/DNN :contentReference[oaicite:0]{index=0}
})
picam2.configure(video_config)
picam2.start()

# 5) Prepare OpenCV window (now with GUI support installed)
cv2.namedWindow("Detection", cv2.WINDOW_NORMAL)
print("Live view started. Press 's' to snapshot+identify, 'q' to quit.")

try:
    while True:
        # Now capture_array() is H×W×3 in BGR order
        frame = picam2.capture_array()

        # build blob & run through the network
        blob = cv2.dnn.blobFromImage(
            cv2.resize(frame, (300, 300)),
            0.007843, (300, 300), 127.5
        )
        net.setInput(blob)
        detections = net.forward()

        # draw green boxes on that 3-channel frame
        h, w = frame.shape[:2]
        for i in range(detections.shape[2]):
            conf = detections[0, 0, i, 2]
            if conf > 0.5:
                idx = int(detections[0, 0, i, 1])
                x1, y1, x2, y2 = (detections[0, 0, i, 3:7] * np.array([w, h, w, h])).astype(int)
                label = CLASS_NAMES[idx]
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
                cv2.putText(frame, f"{label}: {conf:.2f}",
                            (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

        # display it
        cv2.imshow("Detection", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):
            _, jpg = cv2.imencode('.jpg', frame)
            print("\n[Snapshot] Sending to GPT for identification…")
            desc = identify(jpg.tobytes(),
                            prompt="Please identify the main object in this image.")
            print("GPT says:", desc, "\n")

        elif key == ord('q'):
            break

finally:
    picam2.stop()
    cv2.destroyAllWindows()
