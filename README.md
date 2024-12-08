# Video Evolution Algorithm

This project implements an **image evolution algorithm** that recreates a source video iteratively adding randomly generated shapes to a blank canvas. The algorithm refines the canvas step by step, improving its similarity to the each video frame over time. This version of the algorithm also does not have subdivided lines that the image version does. 


## Features

- Replicate videos abstractly frame-by-frame.
- Fine-tune the algorithm with customizable parameters.
- Handles both simple and complex visuals using subdivisions and iterative refinement.


## Installation

1. Clone this repository:
   ```bash
   git clone -b video_evolution https://github.com/sam-b02/image-evolution-algorithm.git
   cd image-evolution-algorithm
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```


## Usage

### Step 1: Prepare Video or Image
- Place the video you want to replicate in the `video source` directory.

### Step 2: Split Video into Frames
- Open `helper programs/video splitter.py` and replace the following line with your video path:
  
   ```python
   video_path = r"video source/input_video.mp4"
   ```
- Run the script to split your video into individual frames.

### Step 3: Configure Parameters
Edit the `main()` function in `main.py` to customize algorithm behavior:

(See Configuration Options for explanations of each variable)
```python
video_source = r"video source/input_video.mp4"
use_custom_background = False
number_of_subdivisions = 4096
number_of_subdivided_objects = 10
target_goal = 0
best_print = False
clean_output = True
diff_sort = True
```
### Step 4: Run the Algorithm
Execute the script:
```bash
python main.py
```

### Step 5: View Results
- Final outputs are saved in the `frames output` directory.
- Each frame represents a progressively refined recreation of the source video or image.


## How It Works

1. **Initial Setup**:  
   - Starts with either a blank canvas or a custom background.  
   - Random shapes are added iteratively.

2. **Subdivision**:  
   - The canvas is divided into smaller regions for precise edits.  
   - Subdivisions improve accuracy, especially for detailed images.

3. **Shape Addition**:  
   - Random shapes (ellipses, rectangles) are drawn.  
   - Only changes that reduce the Root Mean Square Error (RMSE) are kept.

4. **Iterative Refinement**:  
   - This process repeats across subdivisions until the similarity goal or maximum iterations are reached.


## Configuration Options

| Parameter                  | Description                                                                 |
|----------------------------|-----------------------------------------------------------------------------|
| `use_custom_background`    | Use a custom image as the starting canvas (default: blank white canvas).    |
| `number_of_subdivisions`   | Number of image subdivisions (higher = finer detail; powers of 2 work best).|
| `number_of_subdivided_objects` | Number of shapes drawn per subdivision (controls density of shapes).    |
| `target_goal`              | Desired RMSE for each subdivision (lower = higher quality).                |
| `best_print`               | Debugging tool to identify algorithm bottlenecks.                          |
| `clean_output`             | Deletes previous outputs from the `frames output` folder before starting.  |
| `diff_sort`                | Changes the order in which shapes are drawn; useful for enhancing detail.  |

## Usage with images

As this algorithm does not have visible subdivision lines on the image, you may want to use this program for images as well, not just videos. Accomplishing this is very simple: 

1. Place the image you wish to recreate in the `frame source` directory
2. Replace the "get_dimensions" at line 153 with the actual width and height of the image as shown below:

   ```WIDTH, HEIGHT = get_dimensions()``` ⇨ ```WIDTH, HEIGHT = 512, 512``` (example width and height)
4. You can then change the parameters and run the program as you please.

   
## License

This project is distributed under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! Feel free to submit issues or feature requests.
