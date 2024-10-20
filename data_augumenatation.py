import os
from PIL import Image
import Augmentor

from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

# Define the paths for the dataset and augmentation directories
DATASET_DIR = r"C:\SOP\Data augumenation\Dataset"
AUGMENTATION_DIR = r"C:\SOP\Data augumenation\Augmentation"

# Function to ensure that the directory exists, if not, create it
def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Function to downgrade image quality (reduce resolution or compression)
def downgrade_image(image_path, output_path, quality=70):
    try:
        img = Image.open(image_path)
        img = img.convert("RGB")  # Ensure RGB format
        img.save(output_path, quality=quality, optimize=True)  # Save with reduced quality
    except Exception as e:
        print(f"Error downgrading image {image_path}: {e}")

# Function to apply augmentations to images in the folder
def augment_image_folder(input_folder, output_folder, num_augmentations=4):
    p = Augmentor.Pipeline(input_folder, output_folder)
    
    # Define augmentations
    p.rotate(probability=0.7, max_left_rotation=10, max_right_rotation=10)
    p.flip_left_right(probability=0.5)
    p.flip_top_bottom(probability=0.5)
    p.zoom_random(probability=0.5, percentage_area=0.8)
    p.random_contrast(probability=0.5, min_factor=0.7, max_factor=1.3)
    
    # Create num_augmentations times the original number of images
    p.sample(num_augmentations * len(os.listdir(input_folder)))

# Main function to iterate through the Dataset folder structure
def process_dataset():
    for class_folder in os.listdir(DATASET_DIR):
        class_input_path = os.path.join(DATASET_DIR, class_folder)
        class_output_path = os.path.join(AUGMENTATION_DIR, class_folder)

        # Ensure the output folder for each class exists
        ensure_dir(class_output_path)
        
        # Downgrade the quality of all images in the class folder
        for image_file in os.listdir(class_input_path):
            image_path = os.path.join(class_input_path, image_file)
            downgraded_image_path = os.path.join(class_output_path, image_file)
            
            # Downgrade and save image in the output folder
            downgrade_image(image_path, downgraded_image_path)
        
        # After downgrading, apply augmentation to the images
        augment_image_folder(class_output_path, class_output_path)

if __name__ == "__main__":
    process_dataset()
