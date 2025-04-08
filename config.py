# Width and height of crop
W = 174

# Radius of light disk
RADIUS = W // 2

# Number of pixels to shrink radius, so background is white
RADIUS_OFFSET = 3           

# Threshold for binarization
THRESHOLD = 235

# x-coordinate of player 1 shape
X1 = 149

# x-coordinate of player 2 shape
X2 = X1 + W - 3

# y-coordinate of both players' shapes
Y = 97

# Angle of wheel
ANGLE = 45

# Crop region (player 1 wheel)
WHEEL_W = 190
WHEEL1_X = 117
WHEEL_Y = 2 * WHEEL_W + 29

# Crop region (player 2 wheel)
WHEEL2_X = WHEEL1_X + WHEEL_W + 25

# Center of wheel
WHEEL_CENTER = (WHEEL_W // 2 - 1, WHEEL_W // 2 - 1)

# Threshold for binarization (top shape of wheel)
TOP_THRESHOLD = 150

# Crop region (top shape of wheel)
TOP_W = 50
TOP_RADIUS = TOP_W // 2
TOP_RADIUS_OFFSET = 4
TOP_X = (WHEEL_W - TOP_W) // 2 + 1
TOP_Y = 5

POLAR_RADIUS = 65