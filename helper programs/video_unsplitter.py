import cv2
import os


def create_video_from_images(folder_path, output_video_path, fps=30):
    # Get all image files in the folder
    images = [
        img
        for img in os.listdir(folder_path)
        if img.endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif"))
    ]
    images.sort()  # Sort images by name, assuming they should be in order

    if not images:
        print("No images found in the folder.")
        return

    # Get the size of the first image
    first_image_path = os.path.join(folder_path, images[0])
    first_image = cv2.imread(first_image_path)
    height, width, layers = first_image.shape

    # Initialize the video writer
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # For .mp4 videos
    video = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    # Add each image to the video
    for image in images:
        print(image)
        image_path = os.path.join(folder_path, image)
        img = cv2.imread(image_path)
        video.write(img)

    # Release the video writer
    video.release()
    print(f"Video created successfully: {output_video_path}")


# Example usage:
create_video_from_images(r"frames output", "output_video.mp4", fps=8)
