import os
import cv2
import math
import random
import time
from ultralytics import YOLO
# from tracker import Tracker

colors = [(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)) for j in range(10)]
# model = YOLO('../runs/detect/train/weights/best.pt')
model = YOLO('yolov8n.pt')
model.fuse()

video_path = os.path.join('.', 'captures', '1.mp4')
cap = cv2.VideoCapture(video_path)
assert cap.isOpened()

# fps = cap.get(cv2.CAP_PROP_FPS)
# frame_duration = max(1, math.floor(1000 / fps))

# tracker = Tracker()

ret, frame = cap.read()
while ret:

    results = model(frame)
    for result in results:
        detections = []
        for r in result.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = r
            x1, y1, x2, y2, class_id = int(x1), int(y1), int(x2), int(y2), int(class_id)
            detections.append([x1, y1, x2, y2, score])
            cv2.rectangle(frame, (x1, y1), (x1, y2), (colors[0]))
        
        # tracker.update(frame, detections)
        # for track in tracker.tracks:
        #     x1, y1, x2, y2 = track.bbox
        #     x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        #     track_id = track.track_id

            # cv2.rectangle(frame, (x1, y1), (x1, y2), (colors[0]))

            

    cv2.imshow('frame', frame)
    cv2.waitKey(1)
    ret, frame = cap.read()

cap.release()
cv2.destroyAllWindows()


