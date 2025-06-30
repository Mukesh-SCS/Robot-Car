from time import sleep
import cv2
from picamera2 import Picamera2


def main():
    # Load labels
    label_dict = {}
    with open('models/ssd_mobilenet/labels.txt', 'r') as f:
        for l in f:
            arr = l.strip().split(':')
            label_dict[int(arr[0])] = arr[1].strip()

    # Load model
    model = cv2.dnn.readNetFromTensorflow(
        'models/ssd_mobilenet/frozen_inference_graph.pb',
        'models/ssd_mobilenet/ssd_mobilenet_v2_coco_2018_03_29.pbtxt'
    )

    # Start Picamera2 for BGR frames
    picam2 = Picamera2()
    resolution = (640, 480)
    cols, rows = resolution
    cfg = picam2.create_preview_configuration(main={"size": resolution, "format": "BGR888"})
    picam2.configure(cfg)
    picam2.start()
    sleep(1)  # let camera warm up

    color = (23, 230, 210)

    while True:
        image = picam2.capture_array()  # H×W×3 BGR image

        # Run it through the network
        blob = cv2.dnn.blobFromImage(image, size=resolution, swapRB=True, crop=False)
        model.setInput(blob)
        net_out = model.forward()

        for detection in net_out[0, 0, :, :]:
            score = float(detection[2])
            if score > 0.5:
                label = int(detection[1])
                label_str = label_dict.get(label, 'unknown')
                print(label_str)

                left = int(detection[3] * cols)
                top = int(detection[4] * rows)
                right = int(detection[5] * cols)
                bottom = int(detection[6] * rows)
                cv2.rectangle(image, (left, top), (right, bottom), color, thickness=2)
                cv2.putText(image, label_str, (left + 3, bottom - 3), cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 2)

        cv2.imshow('press Q to exit', image)
        key = cv2.waitKey(1) & 0xff
        if key == ord('q'):
            break

    picam2.stop()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
