from PIL import Image

# Use the SAME 8-color palette as the player sprite
# Index 0 is transparency, Index 6 is Yellow
palette = [
    (255, 0, 255),    # 0: Transparent Magenta
    (192, 192, 192),  # 1: Light Grey
    (128, 128, 128),  # 2: Medium Grey
    (64, 64, 64),     # 3: Dark Grey
    (0, 0, 255),      # 4: Blue
    (255, 0, 0),      # 5: Red
    (255, 255, 0),    # 6: Yellow << Bullet Color
    (0, 0, 0),        # 7: Black
]
flat_palette = [value for color in palette for value in color]
flat_palette.extend([0] * (768 - len(flat_palette)))

# Define 8x8 pixel data using palette indices (0-7)
# Simple yellow vertical line/dot
pixel_indices = [
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 6, 6, 0, 0, 0,
    0, 0, 0, 6, 6, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, # Add some padding maybe?
    0, 0, 0, 0, 0, 0, 0, 0,
]

# Create an 8x8 image in Palette mode
img = Image.new('P', (8, 8))
img.putpalette(flat_palette)
img.putdata(pixel_indices)

# Define the output path (inside the 'res' folder)
output_path = "res/bullet_sprite.png"

# Save the image as PNG, specifying index 0 is transparent
try:
    img.save(output_path, transparency=0)
    print(f"Successfully created '{output_path}'")
except Exception as e:
    print(f"Error saving image: {e}")