import os
import cv2
from mask_utils import load_masks

p1_folder = 'p1_masks'
p2_folder = 'p2_masks'
output_folder = 'combined_masks'

os.makedirs(output_folder, exist_ok=True)

# Get Player 1 mask images.
p1_masks = load_masks(p1_folder)

# Get Player 2 mask images.
p2_masks = load_masks(p2_folder)

for k1 in p1_masks:
    for k2 in p2_masks:
        mask1 = p1_masks[k1]
        mask2 = p2_masks[k2]
        combined = cv2.bitwise_and(mask1, mask2)

        out_path = os.path.join(output_folder, f'{k1}_{k2}.png')
        cv2.imwrite(out_path, combined)