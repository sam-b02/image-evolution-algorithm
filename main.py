import os
import time
import random
import numpy as np
from PIL import Image, ImageDraw
from collections import Counter

def rms_diff(image1, image2):
    """Calculate the Root Mean Square Error (RMSE) between two images."""
    image1_arr = np.asarray(image1, dtype=np.float64)
    image2_arr = np.asarray(image2, dtype=np.float64)
    diff = image1_arr - image2_arr
    return np.sqrt(np.mean(diff**2))

def compare_images(image1_path, image2_path):
    """Compare two images and return their RMSE. Lower values indicate higher similarity."""
    image1 = Image.open(image1_path).convert("RGB")
    image2 = Image.open(image2_path).convert("RGB")
    return rms_diff(image1, image2)

def load_image(image_path):
    """Load an image and return it as a numpy array."""
    return np.array(Image.open(image_path).convert("RGB"))

def first_round_drawing(HEIGHT, WIDTH):
    """Generate an image with a random colored circle."""
    img = Image.new("RGB", (HEIGHT, WIDTH), "white")
    draw = ImageDraw.Draw(img)
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    radius = random.randint(10, WIDTH)
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)
    return img

def first_round(x, source_image, HEIGHT, WIDTH):
    """Generate the first round of backgrounds and select the most similar to the source image."""
    lowest = float("inf")
    lowest_file = None
    for i in range(x):
        image = first_round_drawing(WIDTH, HEIGHT)
        image_path = f"output image/circles{i}.png"
        image.save(image_path)
        cmp = compare_images(source_image, image_path)
        if cmp < lowest:
            lowest = cmp
            lowest_file = image_path

    kill(lowest_file)
    return lowest_file

def draw_random_shape(arr, color_palette, height, width):
    """Draw a random shape (ellipse, rectangle, or triangle) on an image."""
    new_arr = arr.copy()
    shape = random.choice(["ellipse", "rectangle", "triangle"])
    color = random.choice(color_palette)

    if shape == "ellipse":
        x, y = random.randint(0, width), random.randint(0, height)
        radius_x, radius_y = random.randint(1, width), random.randint(1, height)
        y_coords, x_coords = np.ogrid[: arr.shape[0], : arr.shape[1]]
        mask = ((x_coords - x) / radius_x) ** 2 + ((y_coords - y) / radius_y) ** 2 <= 1
        new_arr[mask] = color

    elif shape == "rectangle":
        x1, y1 = random.randint(0, width), random.randint(0, height)
        rect_width, rect_height = random.randint(1, width), random.randint(1, height)
        new_arr[y1 : y1 + rect_height, x1 : x1 + rect_width] = color

    elif shape == "triangle":
        points = [(random.randint(0, width), random.randint(0, height)) for _ in range(3)]
        y_coords, x_coords = np.ogrid[: arr.shape[0], : arr.shape[1]]
        mask = np.zeros(arr.shape[:2], dtype=bool)
        for i in range(3):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % 3]
            mask |= (y2 - y1) * (x_coords - x1) - (x2 - x1) * (y_coords - y1) >= 0
        new_arr[mask] = color

    return new_arr

def kill(keep_file=None):
    """Remove all files from the output directory except the specified file."""
    directory = "output image"
    if keep_file:
        keep_file = keep_file.split("/")[-1]
    for filename in os.listdir(directory):
        if filename != keep_file:
            os.remove(os.path.join(directory, filename))

def subdivide_image(arr, number_of_subdivisions, HEIGHT, WIDTH):
    """Subdivide an image into smaller regions."""
    subdivided_images = []
    sub_height = HEIGHT // int(np.sqrt(number_of_subdivisions))
    sub_width = WIDTH // int(np.sqrt(number_of_subdivisions))
    for i in range(0, HEIGHT, sub_height):
        for j in range(0, WIDTH, sub_width):
            subdivided_image = arr[i : i + sub_height, j : j + sub_width]
            subdivided_images.append((i, j, subdivided_image))
    return subdivided_images

def final_evolution(
    arr, source_arr, number_of_subdivisions, HEIGHT, WIDTH,
    number_of_subdivided_objects, target_goal, best_print
):
    """Perform the final evolution step by subdividing the image and adding random shapes to match the target image."""
    subdivided_images = subdivide_image(arr, number_of_subdivisions, HEIGHT, WIDTH)
    source_subdivided_images = subdivide_image(source_arr, number_of_subdivisions, HEIGHT, WIDTH)
    sub_HEIGHT = HEIGHT // int(np.sqrt(number_of_subdivisions))
    sub_WIDTH = WIDTH // int(np.sqrt(number_of_subdivisions))

    for i, (y, x, current_image) in enumerate(subdivided_images):
        source_current_image = source_subdivided_images[i][2]
        color_palette = list(np.unique(source_current_image.reshape(-1, source_current_image.shape[2]), axis=0))
        best = rms_diff(current_image, source_current_image)
        att = 0
        
        while att < number_of_subdivided_objects:
            if best <= target_goal:
                break
            new_arr = draw_random_shape(current_image, color_palette, sub_HEIGHT, sub_WIDTH)
            cmp = rms_diff(new_arr, source_current_image)
            if cmp < best:
                best = cmp
                if best_print:
                    print(f"Subdivision {i+1}/{len(subdivided_images)}: New best RMSE = {best:.4f}: Shape Count = {att}")
                current_image = new_arr
                att += 1

        arr[y : y + sub_HEIGHT, x : x + sub_WIDTH] = current_image

    return arr

def main():
    source_image_path = r"source image\pinguin.png"  # Path to the source image
    number_of_backgrounds = 3  # Number of initial background images to generate
    start_from_custom_image = False  # Set to False to generate a new starting image
    custom_image_path = r""  # Path to custom starting image
    number_of_subdivisions = 512  # Number of subdivisions for the image
    number_of_subdivided_objects = 15  # Number of shape additions per subdivision
    target_goal = 1  # Target RMSE (lower values produce more accurate results but take longer)
    best_print = False  # Set to True to print progress updates

    print("Loading source image...")
    source_arr = load_image(source_image_path)
    HEIGHT, WIDTH = source_arr.shape[:2]
    print("--- done ---")

    print("Generating initial background...")
    if not start_from_custom_image:
        first_file = first_round(number_of_backgrounds, source_image_path, HEIGHT, WIDTH)
    else:
        first_file = custom_image_path

    first_arr = load_image(first_file)

    print("--- done ---")

    print("Starting image evolution...")
    start_time = time.time()

    final_arr = final_evolution(
        first_arr, source_arr, number_of_subdivisions, HEIGHT, WIDTH,
        number_of_subdivided_objects, target_goal, best_print
    )

    final_time = time.time() - start_time
    print("--- done ---")
    print(f"Image evolution completed in {final_time:.2f} seconds.")

    final_image = Image.fromarray(final_arr.astype("uint8"), "RGB")
    output_path = f"output image/{number_of_subdivisions}-{number_of_subdivided_objects}-{target_goal}-{str(time.time())[::4]}.png"
    final_image.save(output_path)
    print(f"Final image saved as: {output_path}")

if __name__ == "__main__":
    main()