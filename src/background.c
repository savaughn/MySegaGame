// background.c
#include <genesis.h>
#include "globals.h"    // For scroll offsets, player_scroll_delta_x/y, map constants
#include "background.h"
#include "res/resources.h" // For bg_far_tiles, bg_near_tiles for numTile

// // --- Background Map Data Arrays (Static to this file) ---
// static u16 farMapData[MAP_HW_WIDTH * MAP_HW_HEIGHT];   // Plane B
// static u16 nearMapData[MAP_HW_WIDTH * MAP_HW_HEIGHT];  // Plane A

// void initBackground(void) {
//     // Clear planes and map data if not done elsewhere or if re-initializing
//     VDP_clearPlane(BG_A, TRUE);
//     VDP_clearPlane(BG_B, TRUE);
//     // Could memset farMapData and nearMapData to 0 here if needed

//     // Load tiles (could also be here or in main)
//     VDP_loadTileData(bg_far_tiles.tiles, BG_FAR_TILE_INDEX, bg_far_tiles.numTile, DMA_QUEUE);
//     VDP_loadTileData(bg_near_tiles.tiles, BG_NEAR_TILE_INDEX, bg_near_tiles.numTile, DMA_QUEUE);

//     // Generate and upload maps
//     generateRandomMapLayer(farMapData, MAP_HW_WIDTH, MAP_HW_HEIGHT, BG_FAR_TILE_INDEX, bg_far_tiles.numTile, PAL0);
//     generateRandomMapLayer(nearMapData, MAP_HW_WIDTH, MAP_HW_HEIGHT, BG_NEAR_TILE_INDEX, bg_near_tiles.numTile, PAL2);

//     VDP_setTileMapDataRect(BG_B, farMapData,  0, 0, MAP_HW_WIDTH, MAP_HW_HEIGHT, MAP_HW_WIDTH, DMA_QUEUE);
//     VDP_setTileMapDataRect(BG_A, nearMapData, 0, 0, MAP_HW_WIDTH, MAP_HW_HEIGHT, MAP_HW_WIDTH, DMA_QUEUE);

//     // Initial scroll positions
//     scroll_a_x = 0; scroll_a_y = 0;
//     scroll_b_x = 0; scroll_b_y = 0;
//     VDP_setHorizontalScroll(BG_A, scroll_a_x);
//     VDP_setVerticalScroll(BG_A, scroll_a_y);
//     VDP_setHorizontalScroll(BG_B, scroll_b_x);
//     VDP_setVerticalScroll(BG_B, scroll_b_y);
// }


// // --- Generate Random Background Map Layer ---
// void generateRandomMapLayer(u16* mapData, u16 mapWidth, u16 mapHeight, u16 baseTileIndex, u16 numTilesInSet, u16 pal) {
//     u32 mapIdx = 0;
//     for (u16 ty = 0; ty < mapHeight; ty++) {
//         for (u16 tx = 0; tx < mapWidth; tx++) {
//             u16 randomTileOffset = random() % numTilesInSet;
//             u16 tileVRAMIndex = baseTileIndex + randomTileOffset;
//             mapData[mapIdx] = TILE_ATTR_FULL(pal, FALSE, FALSE, FALSE, tileVRAMIndex); // Low priority for background
//             mapIdx++;
//         }
//     }
// }

void initBackground(void) {

    // Initial scroll positions
    scroll_a_x = 0; scroll_a_y = 0;
    scroll_b_x = 0; scroll_b_y = 0;

    // VDP_loadTileSet(&star_bg_tiles, ind, DMA_QUEUE);
    // star_map = MAP_create(&star_bg_map, BG_B, TILE_ATTR_FULL(PAL0, FALSE, FALSE, FALSE, ind));
    // PAL_setPalette(PAL0, star_bg_pal.data, DMA_QUEUE);
    // MAP_scrollTo(star_map, scroll_b_x, scroll_b_y);

    // New background
    PAL_setPalette(PAL0, star_bg_pal.data, DMA_QUEUE);
    VDP_drawImageEx(BG_B, &starbg, TILE_ATTR_FULL(PAL0, FALSE, FALSE, FALSE, ind), 0, 0, FALSE, TRUE);
}

// --- Update Scrolling Function ---
void updateScrolling() {
    // player_scroll_delta_x/y is how much the player *would* move if not for screen boundaries
    // This delta is applied to the background scroll in the opposite direction

    scroll_a_x -= player_scroll_delta_x; // Near layer (Plane A)
    scroll_a_y += player_scroll_delta_y; // SGDK Y scroll is often inverted depending on perspective

    // Parallax for far layer (Plane B)
    // Original had dx/2. If player_scroll_delta_x is already the pixel delta, use that.
    scroll_b_x -= (player_scroll_delta_x / PARALLAX_FACTOR_BG_B) % 512; // Or use PARALLAX_FACTOR_BG_B as per defines
    scroll_b_y += (player_scroll_delta_y / PARALLAX_FACTOR_BG_B) % 256; // Assuming A is near, B is far from defines

    // if (scroll_b_x < 0){
    //     scroll_b_x += 640;
    // }

    // if (scroll_b_x > 639){
    //     scroll_b_x -= 640;
    // }

    // if (scroll_b_y < 0){
    //     scroll_b_y += 320;
    // }

    // if (scroll_b_y > 319){
    //     scroll_b_y -= 320;
    // }

    // VDP_setHorizontalScroll(BG_A, scroll_a_x);
    // VDP_setVerticalScroll(BG_A, scroll_a_y);
    VDP_setHorizontalScroll(BG_B, scroll_b_x);
    VDP_setVerticalScroll(BG_B, scroll_b_y);
}