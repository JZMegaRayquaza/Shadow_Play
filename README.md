# Shadow Play Assistant

This project removes the difficulty of finding the correct shape for Player 1 (by detecting the shape for you) using computer vision and an Elgato capture card.

## Installing Required Libraries

Install the required Python libraries:

```bash
pip install opencv-python numpy
```

## Main Code

Make sure `combined_masks/`, `p1_masks/`, `p2_masks`, and `mask_utils.py` are in the same directory as `shadow_play.py`.

Run:

```bash
python shadow_play.py
```

The correct shape on the wheel of Player 1 will be circled in green if at the top and red otherwise.

## Folder Structure

```
PRIME_CUT/
├── combined_masks/
├── p1_masks/
├── p2_masks/
├── mask_utils.py
├── shadow_play.py
└── README.md
```