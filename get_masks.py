import cv2
import os
from mask_utils import crop, binarize, apply_circle_mask
import config as c

# Input and output directories
input_dir = 'shadow_shapes'
p1_mask_dir = 'p1_masks'
p2_mask_dir = 'p2_masks'

# Create output directories if they don't exist
os.makedirs(p1_mask_dir, exist_ok=True)
os.makedirs(p2_mask_dir, exist_ok=True)

for i, shape in enumerate(os.listdir(input_dir)):
    input_path = os.path.join(input_dir, shape)

    image = cv2.imread(input_path)

    # Crop images
    cropped1 = crop(image, c.X1, c.Y, c.W)
    cropped2 = crop(image, c.X2, c.Y, c.W)

    # Convert colored images into binary images
    raw_mask1 = binarize(cropped1)
    raw_mask2 = binarize(cropped2)

    # Ignore background
    mask1 = apply_circle_mask(raw_mask1, c.RADIUS, c.RADIUS_OFFSET)
    mask2 = apply_circle_mask(raw_mask2, c.RADIUS, c.RADIUS_OFFSET)

    # Save the final masks
    mask_path1 = os.path.join(p1_mask_dir, f'{i}.png')
    mask_path2 = os.path.join(p2_mask_dir, f'{i}.png')
    cv2.imwrite(mask_path1, mask1)
    cv2.imwrite(mask_path2, mask2)