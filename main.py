from PIL import Image, ImageDraw
import numpy as np
import random
import os
import time
import cv2

def rms_diff(image1, image2):
    image1_arr = np.asarray(image1, dtype=np.float64)
    image2_arr = np.asarray(image2, dtype=np.float64)
    diff = image1_arr - image2_arr
    return np.sqrt(np.mean(diff ** 2))

def compare_images(image1_path, image2_path):
    image1 = Image.open(image1_path).convert("RGB")
    image2 = Image.open(image2_path).convert("RGB")
    rmse = rms_diff(image1, image2)
    return rmse

def load_image(image_path):
    return np.array(Image.open(image_path).convert("RGB"))

def draw_random_shape(arr, color_palette, height, width):
    new_arr = arr.copy()
    shape = random.choice(["ellipse", "rectangle"])
    color = random.choice(color_palette)

    if shape == "ellipse":
        x = random.randint(0, width)
        y = random.randint(0, height)
        radius_x = random.randint(1, width)
        radius_y = random.randint(1, height)
        y_coords, x_coords = np.ogrid[:arr.shape[0], :arr.shape[1]]
        mask = ((x_coords - x) / radius_x) ** 2 + ((y_coords - y) / radius_y) ** 2 <= 1
        new_arr[mask] = color
        shape_info = {
            "shape" : shape,
            "color" : color,
            "x" : x,
            "y" : y,
            "radius_x" : radius_x,
            "radius_y" : radius_y,
        }
    else:
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        rect_width = random.randint(1, width)
        rect_height = random.randint(1, height)
        new_arr[y1:y1+rect_height, x1:x1+rect_width] = color

        shape_info = {
                "shape": shape,
                "color": color,
                "x1": x1,
                "y1": y1,
                "rect_height": rect_height,
                "rect_width": rect_width
                }

    return shape_info, new_arr

def kill(kill_list=None):
    if kill_list is None:
        kill_list = []
    elif kill_list is not None:
        kill_list = kill_list.split("/")[1]
    directory = "frames output"
    for filename in os.listdir(directory):
        if filename != kill_list:
            file_path = os.path.join(directory, filename)
            os.remove(file_path)
            
def subdivide_image(arr, number_of_subdivisions, HEIGHT, WIDTH):
    subdivided_images = []
    sub_height = HEIGHT // int(np.sqrt(number_of_subdivisions))
    sub_width = WIDTH // int(np.sqrt(number_of_subdivisions))
    for i in range(0, HEIGHT, sub_height):
        for j in range(0, WIDTH, sub_width):
            subdivided_image = arr[i:i+sub_height, j:j+sub_width]
            subdivided_images.append((i, j, subdivided_image))
    return subdivided_images

def draw_shape_on_full_image(draw, shape_info, x_offset, y_offset):
    if shape_info["shape"] == "ellipse":
        x = shape_info["x"] + x_offset
        y = shape_info["y"] + y_offset
        x1 = x - shape_info["radius_x"]
        y1 = y - shape_info["radius_y"]
        x2 = x + shape_info["radius_x"]
        y2 = y + shape_info["radius_y"]
        draw.ellipse([x1, y1, x2, y2], fill=tuple(shape_info["color"]))
    else:
        x1 = shape_info["x1"] + x_offset
        y1 = shape_info["y1"] + y_offset
        x2 = x1 + shape_info["rect_width"]
        y2 = y1 + shape_info["rect_height"]
        draw.rectangle([x1, y1, x2, y2], fill=tuple(shape_info["color"]))

def final_evolution(arr, source_arr, number_of_subdivisions, HEIGHT, WIDTH, number_of_subdivided_objects, target_goal, best_print, sub_HEIGHT, sub_WIDTH, diff_sort):
    subdivided_images = subdivide_image(arr, number_of_subdivisions, HEIGHT, WIDTH)
    source_subdivided_images = subdivide_image(source_arr, number_of_subdivisions, HEIGHT, WIDTH)
    
    successful_shapes = []

    for i, (y, x, current_image) in enumerate(subdivided_images):
        source_current_image = source_subdivided_images[i][2]
        color_palette = list(np.unique(np.reshape(source_current_image, (-1, source_current_image.shape[2])), axis=0))
        cmp = rms_diff(current_image, source_current_image)
        best = cmp
        attempts = 0
        while best > target_goal and attempts < number_of_subdivided_objects:
            shape_info, new_arr = draw_random_shape(current_image, color_palette, sub_HEIGHT, sub_WIDTH)
            attempts += 1
            cmp = rms_diff(new_arr, source_current_image)
            if cmp < best:
                best = cmp
                current_image = new_arr
                successful_shapes.append((shape_info, x, y, best))

    # Create a new image to draw all shapes
    full_image = Image.fromarray(arr.astype('uint8'), 'RGB')
    draw = ImageDraw.Draw(full_image)

    if diff_sort:
        successful_shapes.sort(key=lambda x: x[3], reverse=True)

    # Draw all successful shapes on the full image
    for shape_info, x_offset, y_offset, _ in successful_shapes:
        draw_shape_on_full_image(draw, shape_info, x_offset, y_offset)

    return np.array(full_image), len(successful_shapes)

def get_dimensions(video_path):
    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    return width, height

def create_white_image(width, height):
    white_image = Image.new("RGB", (width, height), color=(255, 255, 255))
    white_image.save(r"frames source\white_image.png")

def main():
    WIDTH, HEIGHT = get_dimensions(r"video source\input_video.mp4")
    directory = "frames source"

    use_custom_background = False #use a custom background
    number_of_subdivisions = 4096 #number of subdivisions the image will be broken into, improves image "resolution"
    number_of_subdivided_objects = 10 #number of objects per subdivision, fills out the image more
    target_goal = 0 #rmse goal each subdivision should achieve
    best_print = False #debugging tool, use when the image is getting stuck to see where its getting stuck
    clean_output = True #delete files from frames output upon running
    diff_sort = True #changes shape redrawing order. helpful at lower subdivisions, does not add too much at higher.
 
    if clean_output:
        kill()

    if not use_custom_background:
        create_white_image(WIDTH,HEIGHT)
        background = r"frames source\white_image.png"
    else:
        background = r""  # your custom file goes here.

    sub_HEIGHT = HEIGHT // int(np.sqrt(number_of_subdivisions))
    sub_WIDTH = WIDTH // int(np.sqrt(number_of_subdivisions))

    background_arr = load_image(background)
    program_time_start = time.time()
    frame_count = 0
    for filename in os.listdir(directory):
        if frame_count != 0:
            background_arr = arr #incremental improvements
        
        file_time = time.time()
        print(f"processing {filename}")
        image_path = os.path.join(directory, filename)
        image_arr = load_image(image_path)
        arr, shapeno = final_evolution(background_arr, image_arr, number_of_subdivisions, HEIGHT, WIDTH, number_of_subdivided_objects, target_goal, best_print, sub_HEIGHT, sub_WIDTH, diff_sort)
        image_output = Image.fromarray(arr.astype('uint8'), 'RGB')
        image_output.save(f"frames output/final_image{frame_count:04d}.png")

        frame_count += 1

        file_time_end = time.time()
        curr = str(file_time_end - file_time)
        print(f"{filename} took {curr[:4]} seconds to draw {shapeno} shapes")

    program_time_end = time.time()
    print(f"total time taken was: {program_time_end - program_time_start}")

if __name__ == "__main__":
    main()
