import cv2
import math
import os
import shutil

def extract_frames(video_path, num_images, output_folder, clear_output_folder=False):
    # Clear the output folder if requested
    if clear_output_folder:
        if os.path.exists(output_folder):
            shutil.rmtree(output_folder)
        os.makedirs(output_folder)
    elif not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Load the video
    video = cv2.VideoCapture(video_path)

    # Total number of frames in the video
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate the interval at which to capture frames
    capture_interval = math.floor(total_frames / num_images)

    # Read frames and save them at the specified interval
    count = 0
    img_count = 0
    while video.isOpened():
        ret, frame = video.read()

        # If frame is read correctly ret is True
        if not ret:
            break

        if count % capture_interval == 0 and img_count < num_images:
            # Save frame as an image
            cv2.imwrite(f'{output_folder}/frame{img_count}.jpg', frame)
            img_count += 1

        count += 1

    video.release()
    print(f'Extracted {img_count} images.')

extract_frames('5min.mp4', 100, 'train_raw', clear_output_folder=True)
