import os
import cv2
import math
import random
import time
from ultralytics import YOLO
# from tracker import Tracker

frame_count = 15
model = YOLO('yolov8n.pt')
model.fuse()

output_folder = 'spatial_boxes_train'
os.makedirs(output_folder, exist_ok=True)



# Function to save spatial box
def save_spatial_box(spatial_box, s_box_id):
    for idx, image in enumerate(spatial_box):
        image_name = f"b_{s_box_id}_{idx}.jpg"
        cv2.imwrite(f'{output_folder}/{image_name}', image)

# Spatial Box data structure
class S_Box:
    def __init__(self, x1, x2, y1, y2, id):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.id = id
        self.spatial_box = []

    def add_spatial_box(self, frame):
        # print("herh herh")
        self.spatial_box.append(frame[self.y1: self.y2, self.x1: self.x2])
        if len(self.spatial_box) == frame_count:
            save_spatial_box(self.spatial_box, self.id)

s_boxes = []
s_box_id_counter = 0
video_path = os.path.join('.', 'captures', '5min_15fps.mp4')
cap = cv2.VideoCapture(video_path)
assert cap.isOpened()


# fps = cap.get(cv2.CAP_PROP_FPS)
# frame_duration = max(1, math.floor(1000 / fps))

# tracker = Tracker()

ret, frame = cap.read()
while ret:

    results = model(frame)
    for result in results:
        for r in result.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = r
            x1, y1, x2, y2, class_id = int(x1), int(y1), int(x2), int(y2), int(class_id)
            # print(f"Coordinates are: x1={x1}, y1={y1}, x2={x2}, y2={y2}, Score is {score}, Class ID is {class_id}")
            if score > 0.3 and class_id == 0:
                s_box_id_counter += 1
                s_boxes.append(S_Box(x1, x2, y1, y2, s_box_id_counter))

    for s_box in s_boxes:
        # print('in the loop')
        s_box.add_spatial_box(frame)

    s_boxes  = [sb for sb in s_boxes if len(sb.spatial_box) < frame_count]


    # cv2.imshow('frame', frame)
    cv2.waitKey(1)
    ret, frame = cap.read()

cap.release()
cv2.destroyAllWindows()


