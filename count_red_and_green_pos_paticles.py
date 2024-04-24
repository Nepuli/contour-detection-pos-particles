import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

'''Functions'''
def apply_threshold(image, threshold_value):
    _, thresholded = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY)
    return thresholded

def find_contours(thresholded_image):
    contours, _ = cv2.findContours(thresholded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def draw_contours(image, contours, color):
    img_with_contours = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(img_with_contours, contours, -1, color, 2)
    return img_with_contours

def display_and_save_images(original_image, image_with_contours, filename, save_path=None):
    if save_path:
        save_filename = os.path.splitext(filename)[0] + '_with_contours.png'
        save_filepath = os.path.join(save_path, save_filename)
        cv2.imwrite(save_filepath, image_with_contours)
    else:
        plt.figure(figsize=(8, 4), dpi=300)
        plt.subplot(121), plt.imshow(original_image, cmap='gray'), plt.title('Original')
        plt.axis('off')
        plt.subplot(122), plt.imshow(cv2.cvtColor(image_with_contours, cv2.COLOR_BGR2RGB)), plt.title('With Contours')
        plt.axis('off')
        plt.show()

def find_and_count_particles(image_path, save_path, color):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Processing first with a threshold value of 30
    threshold_value = 30 if color == (0, 255, 0) else 40
    thresholded = apply_threshold(img, threshold_value)
    contours = find_contours(thresholded)
    particle_count = len(contours)
    
    # Checking if the particle count is greater than 500
    if particle_count > 500:
        # If yes, processing again with a threshold value of 60
        threshold_value = 70
        thresholded = apply_threshold(img, threshold_value)
        contours = find_contours(thresholded)
        particle_count = len(contours)
        
    img_with_contours = draw_contours(img, contours, color)
    display_and_save_images(img, img_with_contours, os.path.basename(image_path), save_path)
    
    return particle_count

def process_main_folder(main_folder_path, save_folder_path, color):
    particle_counts = {}
    for folder_name in os.listdir(main_folder_path):
        folder_path = os.path.join(main_folder_path, folder_name)
        if os.path.isdir(folder_path):
            for filename in os.listdir(folder_path):
                if filename.endswith('.png'):
                    image_path = os.path.join(folder_path, filename)
                    count = find_and_count_particles(image_path, save_folder_path, color)
                    particle_counts[filename] = count
    return particle_counts

'''Define paths'''
dataset_root_dir = #TODO:  # Adjust the path for your Dataset
cellline_dir = os.path.join(dataset_root_dir, "arpe")  # Change the cell line here

input_green_dir = os.path.normpath(os.path.join(cellline_dir, "input/pos_green"))
input_red_dir = os.path.normpath(os.path.join(cellline_dir, "input/pos_red"))

output_green_dir = os.path.normpath(os.path.join(cellline_dir, "output/green"))
output_red_dir = os.path.normpath(os.path.join(cellline_dir, "output/red"))

# Process images with green color
result_dict_green = process_main_folder(input_green_dir, output_green_dir, (0, 255, 0))  # Green color

# Process images with red color
result_dict_red = process_main_folder(input_red_dir, output_red_dir, (0, 0, 255))  # Red color

# Print particle counts for green images
for filename, count in result_dict_green.items():
    print(f'GREEN Number of particles in {filename}: {count}')

# Print particle counts for red images
for filename, count in result_dict_red.items():
    print(f'RED Number of particles in {filename}: {count}')
