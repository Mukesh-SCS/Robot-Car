from picamera2 import Picamera2, Preview
import time

def test_picamera2():
    picam2 = Picamera2()
    # optional: no preview window
    preview_config = picam2.create_preview_configuration(main={"size": (800, 600)})
    picam2.configure(preview_config)
    picam2.start_preview(Preview.QTGL)
    picam2.start()
    print("Camera started, warming up for 2 seconds…")
    time.sleep(2)  # let auto‐exposure settle

    # Capture to file
    output_path = "test.jpg"
    picam2.capture_file(output_path)
    print(f"✔ Captured image saved to {output_path}")

    picam2.stop()

if __name__ == "__main__":
    test_picamera2()


#/ #!/usr/bin/env python3
import os
import time
import base64

import cv2
import numpy as np
from dotenv import load_dotenv
from picamera2 import Picamera2, Preview
from openai import OpenAI

# ─── 1. Load your OpenAI key ───────────────────────────────────────────────
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("Missing OPENAI_API_KEY in environment")

# ─── 2. Instantiate the v1+ OpenAI client ──────────────────────────────────
client = OpenAI(api_key=api_key)

def identify(image_bytes: bytes, prompt: str = "What do you see?") -> str:
    b64 = base64.b64encode(image_bytes).decode("utf-8")
    content = [
        {"type": "text",      "text": prompt},
        {"type": "image_url", "image_url": {
            "url": f"data:image/jpeg;base64,{b64}",
            "detail": "auto"
        }}
    ]
    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or "o4-mini" once you're verified
        messages=[{"role": "user", "content": content}],
        temperature=0.0,
    )
    return resp.choices[0].message.content.strip()

# ─── 3. Load MobileNet-SSD detector ────────────────────────────────────────
PROTOTXT = "models/MobileNetSSD_deploy.prototxt"
MODEL    = "models/MobileNetSSD_deploy.caffemodel"

net = cv2.dnn.readNetFromCaffe(PROTOTXT, MODEL)
CLASS_NAMES = [
    "background","aeroplane","bicycle","bird","boat","bottle","bus","car",
    "cat","chair","cow","diningtable","dog","horse","motorbike","person",
    "pottedplant","sheep","sofa","train","tvmonitor"
]

# ─── 4. Set up Picamera2 for preview ───────────────────────────────────────
picam2 = Picamera2()
preview_config = picam2.create_preview_configuration(main={"size": (640, 480)})
picam2.configure(preview_config)
picam2.start_preview(Preview.QTGL)
picam2.start()

# Give auto-exposure a moment
time.sleep(2)

print(
    "\nPreview running.",
    "Type Enter to snapshot+identify,",
    "or type 'q' + Enter to quit.\n"
)

try:
    while True:
        cmd = input("> ")
        if cmd.strip().lower() == "q":
            break

        # 1) grab a frame
        frame = picam2.capture_array()  # BGR NumPy array

        # 2) run detection
        blob = cv2.dnn.blobFromImage(
            cv2.resize(frame, (300, 300)),
            0.007843, (300, 300), 127.5
        )
        net.setInput(blob)
        detections = net.forward()

        # 3) annotate
        h, w = frame.shape[:2]
        for i in range(detections.shape[2]):
            conf = float(detections[0, 0, i, 2])
            if conf > 0.5:
                idx = int(detections[0, 0, i, 1])
                label = CLASS_NAMES[idx]
                box = (detections[0, 0, i, 3:7] * np.array([w, h, w, h])).astype(int)
                x1, y1, x2, y2 = box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(
                    frame, f"{label}: {conf:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2
                )

        # 4) encode and send to GPT
        _, jpg = cv2.imencode('.jpg', frame)
        print("\n[Snapshot] Sending to GPT for identification…")
        description = identify(
            jpg.tobytes(),
            prompt="Please identify the main object in this image."
        )
        print("GPT says:", description, "\n")

finally:
    picam2.stop_preview()
    picam2.close()
    print("Camera closed. Bye!")
/#/