import cv2
import numpy as np
import os

def crop(image, x, y, w):
    '''
    Crops wanted area.
    '''
    return image[y:y+w, x:x+w]

def binarize(image, threshold=235):
    '''
    Converts image to black and white.
    '''
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)

    return binary

def apply_circle_mask(raw_mask, radius, offset=0):
    '''
    Applies a circle mask to remove background.
    '''
    center = (radius, radius)
    circle_mask = np.zeros((2 * radius, 2 * radius), dtype=np.uint8)
    cv2.circle(circle_mask, center, radius - offset, 255, -1)

    mask = np.where(circle_mask == 255, raw_mask, 255).astype(np.uint8)

    return mask

def load_masks(folder):
    '''
    Load masks from a folder.
    '''
    masks = {}
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        image = cv2.imread(path)
        name = os.path.splitext(filename)[0]
        masks[name] = binarize(image)
        
    return masks

def compute_iou(mask1, mask2):
    '''
    Computes intersection over union score of two black and white images.
    '''
    mask1 = (mask1 == 0)
    mask2 = (mask2 == 0)
    intersection = np.logical_and(mask1, mask2).sum()
    union = np.logical_or(mask1, mask2).sum()

    return intersection / union if union > 0 else 0