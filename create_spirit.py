from PIL import Image

# Define the 8-color palette (RGB tuples)
# Index 0 MUST be the transparency color for rescomp default behavior
palette = [
    (255, 0, 255),    # 0: Transparent Magenta (will become transparent)
    (192, 192, 192),  # 1: Light Grey
    (128, 128, 128),  # 2: Medium Grey
    (64, 64, 64),     # 3: Dark Grey
    (0, 0, 255),      # 4: Blue
    (255, 0, 0),      # 5: Red
    (255, 255, 0),    # 6: Yellow
    (0, 0, 0),        # 7: Black (or another color if needed)
    # Pad palette to 256 colors for Pillow format if necessary
    # (though Pillow usually handles short palettes)
    # Add (0,0,0) entries here if needed to reach 256*3 values
]

# Flatten palette for Pillow: [R0, G0, B0, R1, G1, B1, ...]
flat_palette = [value for color in palette for value in color]
# Ensure palette has 768 values (256 colors * 3 RGB) - pad with black
flat_palette.extend([0] * (768 - len(flat_palette)))


# Define 16x16 pixel data using palette indices (0-7)
# T = Transparent (Index 0)
# This matches the visual description from before
pixel_indices = [
    0, 0, 0, 0, 0, 3, 3, 0, 0, 3, 3, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 3, 2, 2, 3, 3, 2, 2, 3, 0, 0, 0, 0,
    0, 0, 0, 3, 2, 1, 1, 2, 1, 1, 2, 3, 0, 0, 0, 0,
    0, 0, 3, 2, 1, 1, 1, 1, 1, 1, 1, 2, 3, 0, 0, 0,
    0, 3, 2, 1, 1, 4, 4, 4, 4, 1, 1, 2, 3, 0, 0, 0,
    0, 3, 2, 1, 1, 4, 4, 4, 4, 1, 1, 2, 3, 0, 0, 0,
    3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 0, # Adjusted last pixel
    3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 0, # Adjusted last pixel
    0, 3, 2, 2, 2, 5, 5, 5, 5, 2, 2, 2, 3, 0, 0, 0,
    0, 0, 3, 2, 2, 5, 6, 5, 2, 2, 3, 0, 0, 0, 0, 0,
    0, 0, 0, 3, 3, 5, 6, 5, 3, 3, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 3, 5, 3, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]

# Create a 16x16 image in Palette mode
img = Image.new('P', (16, 16))

# Apply the palette
img.putpalette(flat_palette)

# Apply the pixel data
img.putdata(pixel_indices)

# Define the output path (inside the 'res' folder)
output_path = "res/player_sprite.png"

# Save the image as PNG, specifying index 0 is transparent
try:
    img.save(output_path, transparency=0)
    print(f"Successfully created '{output_path}'")
except Exception as e:
    print(f"Error saving image: {e}")
