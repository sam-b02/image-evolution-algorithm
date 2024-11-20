import cv2
import os


def kill():
    directory = "frames source"
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        os.remove(file_path)


def split_video_into_frames(video_path, output_folder):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Check if output folder exists, if not, create it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Initialize frame counter
    frame_count = 1

    while True:
        # Read a frame from the video
        ret, frame = cap.read()

        # If the frame was not read successfully, break the loop
        if not ret:
            break

        # Save the frame as an image file
        frame_filename = os.path.join(output_folder, f"frame_{frame_count:04d}.png")
        cv2.imwrite(frame_filename, frame)

        # Increment the frame counter
        print(frame_count)
        frame_count += 1

    # Release the video capture object
    cap.release()


kill()

video_path = r"video source\input_video.mp4"
output_folder = r"frames source"
split_video_into_frames(video_path, output_folder)

print(f"done")
