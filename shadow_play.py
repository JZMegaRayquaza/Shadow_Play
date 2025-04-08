import math
import cv2
import os
from mask_utils import crop, binarize, apply_circle_mask, compute_iou
import config as c

COMBINED_DIR = 'combined_masks'
P1_DIR = 'p1_masks'
P2_DIR = 'p2_masks'

def draw_circle_on_wheel(wheel_img, index, center, polar_radius, color=(0, 0, 255), thickness=4):
    '''
    Draws red/green circle around correct shape.
    '''
    # If top shape, draw green circle
    if index == 0:
        color = (0, 255, 0)

    angle_rad = math.radians(-index * c.ANGLE - 90)
    x = int(center[0] - polar_radius * math.cos(angle_rad))
    y = int(center[1] + polar_radius * math.sin(angle_rad))
    cv2.circle(wheel_img, (x, y), c.TOP_RADIUS, color, thickness)

    return wheel_img

def get_shapes(combined_shape):
    '''
    Get indivdual shape masks from combined shape.
    '''
    p1_p2, ext = os.path.splitext(combined_shape)
    p1, p2 = p1_p2.split('_')

    p1_path = os.path.join(P1_DIR, f'{p1}{ext}')
    p2_path = os.path.join(P2_DIR, f'{p2}{ext}')

    p1_binary = binarize(cv2.imread(p1_path))
    p2_binary = binarize(cv2.imread(p2_path))

    return p1_binary, p2_binary

def find_combined_shape(target_mask):
    '''
    Return name of mask that matches best with target mask.
    Returns None if no good match.
    '''
    best_score = 0
    best_match = None

    for combined in os.listdir(COMBINED_DIR):
        path = os.path.join(COMBINED_DIR, combined)
        template = cv2.imread(path)

        # Get template mask
        template_mask = binarize(template)

        # Compute IoU over binary masks
        iou_fill = compute_iou(template_mask, target_mask)

        if iou_fill > best_score and iou_fill > 0.6:
            best_score = iou_fill
            best_match = combined

    return best_match

def detect_wheel_shape(frame, target_mask):
    '''
    Given a player1's shape, return best shape match index.
    '''
    # Resize target mask to match size of shapes on wheel
    target_resized = cv2.resize(target_mask, (c.TOP_W, c.TOP_W), interpolation=cv2.INTER_NEAREST)
    
    # Crop frame
    cropped1 = crop(frame, c.WHEEL1_X, c.WHEEL_Y, c.WHEEL_W)

    best_score = 0
    best_index = 0

    for i in range(8):
        # Create rotation matrix
        M = cv2.getRotationMatrix2D(c.WHEEL_CENTER, i * c.ANGLE, scale=1)

        # Rotate the image
        rotated1 = cv2.warpAffine(cropped1, M, (c.WHEEL_W, c.WHEEL_W), flags=cv2.INTER_NEAREST)

        # Extract top shape
        top1 = crop(rotated1, c.TOP_X, c.TOP_Y, c.TOP_W)

        # Convert top shape to binary mask
        raw_mask1 = binarize(top1, c.TOP_THRESHOLD)

        # Ignore background
        mask1 = apply_circle_mask(raw_mask1, c.TOP_RADIUS, c.TOP_RADIUS_OFFSET)

        iou = compute_iou(mask1, target_resized)

        if iou > best_score:
            best_score = iou
            best_index = i

    return best_index

def run_shadow_play():
    video_source = 0  # Elgato

    # Open the video capture
    cap = cv2.VideoCapture(video_source)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1440)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    cap.set(cv2.CAP_PROP_FPS, 60)

    # Get crop region for target shape
    _, frame = cap.read()

    # Frame dimensions
    height, width, _ = frame.shape

    # xy-coordinates for target shape
    target_x = (width - c.W) // 2
    target_y = (height // 6) - 10

    # Main loop
    while True:
        _, frame = cap.read()

        # Crop target shape
        target = crop(frame, target_x, target_y, c.W)

        # Get target mask
        target_mask = binarize(target)

        # Find best match
        combined_shape = find_combined_shape(target_mask)

        if combined_shape:
            # Get player1's shape
            p1, _ = get_shapes(combined_shape)

            # Detect location of correct shape
            index = detect_wheel_shape(frame, p1)

            # Crop P1 wheel for drawing
            cropped_wheel = crop(frame, c.WHEEL1_X, c.WHEEL_Y, c.WHEEL_W)

            # Draw red circle
            highlighted = draw_circle_on_wheel(cropped_wheel, index, c.WHEEL_CENTER, c.POLAR_RADIUS)

            # Replace cropped section in frame
            frame[c.WHEEL_Y:c.WHEEL_Y+c.WHEEL_W, c.WHEEL1_X:c.WHEEL1_X+c.WHEEL_W] = highlighted

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    run_shadow_play()