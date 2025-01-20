# import os
# import cv2
# import numpy as np

# def process_images(input_dir, output_dir, watermark_text):
#     # Walk through the directory structure
#     for root, dirs, files in os.walk(input_dir):
#         for file in files:
#             # Process only image files (e.g., jpg, png)
#             if file.lower().endswith(('.jpg', '.jpeg', '.png')):
#                 input_path = os.path.join(root, file)
                
#                 # Recreate the folder structure in the output directory
#                 relative_path = os.path.relpath(root, input_dir)
#                 output_folder = os.path.join(output_dir, relative_path)
#                 os.makedirs(output_folder, exist_ok=True)
                
#                 # Process the image
#                 output_path = os.path.join(output_folder, file)
#                 resize_and_add_watermark(input_path, watermark_text, output_path)

# def resize_and_add_watermark(image_path, watermark_text, output_path):
#     # Load the image
#     image = cv2.imread(image_path)
#     if image is None:
#         print(f"Error: Unable to load image {image_path}")
#         return

#     # Get original dimensions
#     original_height, original_width = image.shape[:2]

#     # Resize the image to 1/4th of its original size
#     new_width = original_width // 4
#     new_height = original_height // 4
#     resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)

#     # Scale watermark properties proportionally to the image size
#     font_scale = max(0.3, min(new_width, new_height) / 1000)  # Scale font size with limits
#     font_thickness = max(1, int(min(new_width, new_height) / 500))  # Scale thickness
#     margin = max(10, int(min(new_width, new_height) / 50))  # Scale margin

#     # Add watermark
#     font = cv2.FONT_HERSHEY_SIMPLEX
#     watermark_color = (255, 255, 255)  # White color

#     # Calculate text size
#     text_size = cv2.getTextSize(watermark_text, font, font_scale, font_thickness)[0]
#     text_x = new_width - text_size[0] - margin
#     text_y = new_height - margin

#     # Create a transparent overlay for the watermark
#     overlay = resized_image.copy()
#     cv2.putText(overlay, watermark_text, (text_x, text_y), font, font_scale, watermark_color, font_thickness)

#     # Blend the overlay with the image to make the watermark translucent
#     alpha = 0.5  # Transparency factor (0: invisible, 1: opaque)
#     cv2.addWeighted(overlay, alpha, resized_image, 1 - alpha, 0, resized_image)

#     # Save the processed image
#     cv2.imwrite(output_path, resized_image)
#     print(f"Processed and saved: {output_path}")

# # Example usage
# input_dir = "images"  # Path to the input directory
# output_dir = "res_images"  # Path to the output directory
# watermark_text = "audistherbs"  # Text for the watermark

# process_images(input_dir, output_dir, watermark_text)
import os
import cv2
import numpy as np

def process_images(input_dir, output_dir, watermark_text):
    # Walk through the directory structure
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            # Process only image files (e.g., jpg, png)
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                input_path = os.path.join(root, file)
                
                # Recreate the folder structure in the output directory
                relative_path = os.path.relpath(root, input_dir)
                output_folder = os.path.join(output_dir, relative_path)
                os.makedirs(output_folder, exist_ok=True)
                
                # Process the image
                output_path = os.path.join(output_folder, file)
                resize_and_add_watermark(input_path, watermark_text, output_path)

def resize_and_add_watermark(image_path, watermark_text, output_path):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Unable to load image {image_path}")
        return

    # Get original dimensions
    original_height, original_width = image.shape[:2]

    # Define the minimum dimensions below which resizing is skipped
    min_dimension = 300  # e.g., skip resizing if width or height < 300 pixels

    if original_width < min_dimension or original_height < min_dimension:
        print(f"Skipping resizing for small image: {image_path}")
        resized_image = image.copy()  # Use the original image without resizing
    else:
        # Resize the image to 50% of its original size
        new_width = original_width // 2
        new_height = original_height // 2
        resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)

    # Scale watermark properties proportionally to the image size
    font_scale = max(0.3, min(resized_image.shape[1], resized_image.shape[0]) / 1000)  # Scale font size with limits
    font_thickness = max(1, int(min(resized_image.shape[1], resized_image.shape[0]) / 500))  # Scale thickness
    margin = max(10, int(min(resized_image.shape[1], resized_image.shape[0]) / 50))  # Scale margin

    # Add watermark
    font = cv2.FONT_HERSHEY_SIMPLEX
    watermark_color = (255, 255, 255)  # White color

    # Calculate text size
    text_size = cv2.getTextSize(watermark_text, font, font_scale, font_thickness)[0]
    text_x = resized_image.shape[1] - text_size[0] - margin
    text_y = resized_image.shape[0] - margin

    # Create a transparent overlay for the watermark
    overlay = resized_image.copy()
    cv2.putText(overlay, watermark_text, (text_x, text_y), font, font_scale, watermark_color, font_thickness)

    # Blend the overlay with the image to make the watermark translucent
    alpha = 0.5  # Transparency factor (0: invisible, 1: opaque)
    cv2.addWeighted(overlay, alpha, resized_image, 1 - alpha, 0, resized_image)

    # Save the processed image
    cv2.imwrite(output_path, resized_image)
    print(f"Processed and saved: {output_path}")

# Example usage
input_dir = "images"  # Path to the input directory
output_dir = "res_images"  # Path to the output directory
watermark_text = "audistherbs"  # Text for the watermark

process_images(input_dir, output_dir, watermark_text)
