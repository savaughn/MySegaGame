from PIL import Image
import math # Needed for rotation calculation if not using simple steps

# Define the 8-color palette (RGB tuples) - SAME AS BEFORE
palette = [
    (255, 0, 255),    # 0: Transparent Magenta
    (192, 192, 192),  # 1: Light Grey
    (128, 128, 128),  # 2: Medium Grey
    (64, 64, 64),     # 3: Dark Grey
    (0, 0, 255),      # 4: Blue
    (255, 0, 0),      # 5: Red
    (255, 255, 0),    # 6: Yellow
    (0, 0, 0),        # 7: Black
]

# Flatten palette for Pillow and pad to 768 values
flat_palette = [value for color in palette for value in color]
flat_palette.extend([0] * (768 - len(flat_palette)))

# Define 16x16 base sprite pixel data using palette indices - SAME AS BEFORE
pixel_indices = [
    0, 0, 0, 0, 0, 3, 3, 0, 0, 3, 3, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 3, 2, 2, 3, 3, 2, 2, 3, 0, 0, 0, 0,
    0, 0, 0, 3, 2, 1, 1, 2, 1, 1, 2, 3, 0, 0, 0, 0,
    0, 0, 3, 2, 1, 1, 1, 1, 1, 1, 1, 2, 3, 0, 0, 0,
    0, 3, 2, 1, 1, 4, 4, 4, 4, 1, 1, 2, 3, 0, 0, 0,
    0, 3, 2, 1, 1, 4, 4, 4, 4, 1, 1, 2, 3, 0, 0, 0,
    3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 0,
    3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 0,
    0, 3, 2, 2, 2, 5, 5, 5, 5, 2, 2, 2, 3, 0, 0, 0,
    0, 0, 3, 2, 2, 5, 6, 5, 2, 2, 3, 0, 0, 0, 0, 0,
    0, 0, 0, 3, 3, 5, 6, 5, 3, 3, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 3, 5, 3, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]

# Create the 16x16 base sprite image in memory
base_img = Image.new('P', (16, 16))
base_img.putpalette(flat_palette)
base_img.putdata(pixel_indices)

# --- Create Sprite Sheet ---
num_frames = 24
frame_width = 16
frame_height = 16
sheet_width = frame_width * num_frames
sheet_height = frame_height

# Create blank sprite sheet canvas
sprite_sheet = Image.new('P', (sheet_width, sheet_height))
sprite_sheet.putpalette(flat_palette) # Apply the same palette

# Loop through frames, rotate, and paste
degrees_per_step = 360.0 / num_frames # Should be 15 degrees

for i in range(num_frames):
    # Calculate rotation angle (Pillow rotates counter-clockwise)
    # Angle 0 = ri 0 (facing right)
    angle = i * degrees_per_step

    # Rotate the base image
    # Use NEAREST resampling to avoid introducing new colors
    # Expand=False keeps size 16x16
    # Fill background with transparent color index 0
    rotated_frame = base_img.rotate(angle, resample=Image.NEAREST, expand=False, fillcolor=0)

    # Calculate position to paste onto the sheet
    paste_x = i * frame_width
    paste_y = 0

    # Paste the rotated frame
    sprite_sheet.paste(rotated_frame, (paste_x, paste_y))

    print(f"Processed frame {i} (angle {angle:.1f} degrees)")

# Define the output path for the sheet
output_sheet_path = "res/player_sprite_sheet.png"

# Save the sprite sheet PNG, specifying index 0 is transparent
try:
    sprite_sheet.save(output_sheet_path, transparency=0)
    print(f"\nSuccessfully created sprite sheet '{output_sheet_path}'")
except Exception as e:
    print(f"\nError saving image: {e}")