from PIL import Image
import random
import os

# --- Parameters ---
NUM_FG_TILES = 8 # Foreground (near stars) tiles
NUM_BG_TILES = 8 # Background (far stars) tiles
TILE_SIZE = 8
FG_FILENAME = "res/near_stars_tiles.png"
BG_FILENAME = "res/far_stars_tiles.png"

# --- Palettes ---
# PAL0 (Background - Plane B) - Indices 0-3 used
bg_palette_rgb = [
    (0, 0, 34),       # 0: BG Color
    (50, 50, 50),     # 1: Dim Star 1
    (85, 85, 85),     # 2: Dim Star 2
    (100, 100, 100),  # 3: Dim Star 3
    # Pad rest of PAL0
    (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0),
    (0,0,0), (0,0,0), (0,0,0), (0,0,0)
]
# PAL2 (Foreground - Plane A) - Indices 32-35 used (relative index 0-3)
# Index 0 (32) MUST be transparent for parallax
fg_palette_rgb = [
    (255, 0, 255),    # 0 (32): Transparent Magenta
    (153, 153, 153),  # 1 (33): Bright Star 1
    (200, 200, 200),  # 2 (34): Bright Star 2
    (238, 238, 238),  # 3 (35): Bright Star 3
     # Pad rest of PAL2
    (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0),
    (0,0,0), (0,0,0), (0,0,0), (0,0,0)
]

# Flatten and pad palettes
def flatten_pad_palette(rgb_list):
    flat = [value for color in rgb_list for value in color]
    flat.extend([0] * (768 - len(flat)))
    return flat

flat_bg_palette = flatten_pad_palette(bg_palette_rgb)
flat_fg_palette = flatten_pad_palette(fg_palette_rgb)

# --- Tile Generation Functions ---
def create_star_tile(width, height, density_percent, star_colors, bg_color=0):
    tile_data = [bg_color] * (width * height)
    num_pixels = width * height
    num_stars = int(num_pixels * (density_percent / 100.0))
    for _ in range(num_stars):
        pos = random.randint(0, num_pixels - 1)
        tile_data[pos] = random.choice(star_colors)
    return tile_data

# --- Generate and Save Function ---
def generate_and_save(filename, num_tiles, palette_flat, tile_generator_func):
    img_width = num_tiles * TILE_SIZE
    img_height = TILE_SIZE
    tileset_img = Image.new('P', (img_width, img_height))
    tileset_img.putpalette(palette_flat)

    print(f"\nGenerating {filename}...")
    for i in range(num_tiles):
        tile_data = tile_generator_func(i) # Pass index to generator
        tile_img = Image.new('P', (TILE_SIZE, TILE_SIZE))
        tile_img.putpalette(palette_flat)
        tile_img.putdata(tile_data)
        tileset_img.paste(tile_img, (i * TILE_SIZE, 0))
        print(f"  Generated tile {i}")

    if not os.path.exists("res"): os.makedirs("res")
    try:
        # Save FG tiles WITH transparency on index 0, BG without
        is_fg = "near_stars" in filename
        transparency_index = 0 if is_fg else None
        tileset_img.save(filename, transparency=transparency_index)
        print(f"Successfully created '{filename}'")
    except Exception as e: print(f"Error saving '{filename}': {e}")

# --- Define Tile Generators ---
def bg_tile_gen(index):
    if index == 0: return [0] * 64 # Blank BG tile
    density = random.uniform(1.0, 5.0) # Very sparse
    colors = [1, 2, 3] # Dim stars
    return create_star_tile(TILE_SIZE, TILE_SIZE, density, colors, bg_color=0)

def fg_tile_gen(index):
    if index == 0: return [0] * 64 # TRANSPARENT FG tile (uses index 0 of fg_palette)
    density = random.uniform(1.0, 3.0) # Slightly denser
    colors = [1, 2, 3] # Brighter stars (indices relative to fg_palette)
    return create_star_tile(TILE_SIZE, TILE_SIZE, density, colors, bg_color=0)

# --- Execute ---
generate_and_save(BG_FILENAME, NUM_BG_TILES, flat_bg_palette, bg_tile_gen)
generate_and_save(FG_FILENAME, NUM_FG_TILES, flat_fg_palette, fg_tile_gen)