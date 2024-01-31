from moviepy.editor import VideoFileClip

def change_frame_rate(input_video_path, output_video_path, new_fps):
    # Load the video
    clip = VideoFileClip(input_video_path)

    # Set the new frame rate
    new_clip = clip.set_fps(new_fps)

    # Write the video file with the new frame rate
    new_clip.write_videofile(output_video_path, fps=new_fps)

input_video_path = 'captures/5min.mp4'  # Replace with your input video file path
output_video_path = 'captures/5min_15fps.mp4'  # Replace with your desired output video file path

# Change the frame rate to 15 FPS
change_frame_rate(input_video_path, output_video_path, 15)