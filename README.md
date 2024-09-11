# Image Evolution Algorithm

This project implements an image evolution algorithm that attempts to recreate a source image using randomly generated shapes. The algorithm works by iteratively refining a canvas, starting from a simple background and progressively adding shapes to match the target image.

## Features

- Generates an initial background with random colored circles
- Subdivides the image into smaller regions for detailed refinement
- Adds random shapes (ellipses, rectangles, triangles) to match the source image
- Uses Root Mean Square Error (RMSE) to measure similarity between images
- Supports custom starting images and various configuration options

## Requirements

- Python 3.x
- NumPy
- Pillow (PIL)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/sam-b02/image-evolution-algorithm.git
   cd image-evolution-algorithm
   ```

2. Install the required packages:
   ```
   pip install numpy pillow
   ```

## Usage

1. Place your source image in the `source image` directory.

2. Modify the `main()` function in the script to set your desired parameters:

   ```python
   source_image_path = r"source image\your_image.png"
   number_of_backgrounds = 50
   start_from_custom_image = False
   custom_image_path = r""
   number_of_subdivisions = 512
   number_of_subdivided_objects = 15
   target_goal = 1
   best_print = False
   ```

3. Run the script:
   ```
   python image_evolution.py
   ```

4. The final image will be saved in the `output image` directory.

## PLEASE NOTE

Running the script will clear the output images file, deleting any previous creations. Be sure to save the images in a different directory if you wish to keep them permanently.

## How It Works

1. **Initial Background Generation**: The algorithm starts by creating several random backgrounds with colored circles and selects the one most similar to the source image.

2. **Image Subdivision**: The canvas is divided into smaller regions for more detailed processing.

3. **Shape Addition**: Random shapes (ellipses, rectangles, triangles) are added to each subdivision, keeping changes that improve similarity to the source image.

4. **Iterative Refinement**: The process continues until the similarity reaches the target goal or the maximum number of iterations is reached.

## Configuration Options

- `number_of_backgrounds`: Number of initial backgrounds to generate
- `start_from_custom_image`: Whether to start from a custom image or generate a new one
- `number_of_subdivisions`: Number of regions to divide the image into
- `number_of_subdivided_objects`: Maximum number of shapes to add per subdivision
- `target_goal`: Target RMSE (lower values produce more accurate results but take longer)
- `best_print`: Whether to print progress updates

## License

[MIT License](LICENSE)

## Contributing

Contributions, issues, and feature requests are welcome.
