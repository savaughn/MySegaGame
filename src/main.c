// main.c
#include <genesis.h>
#include <maths.h>          // For intToStr, random etc. SGDK provides its own
#include "res/resources.h"  // For palettes, sprite resources, music track

#include "globals.h"        // For global variable declarations and structs
#include "constants.h"      // For game constants

#include "player.h"
#include "bullets.h"
#include "fighters.h"
#include "background.h"

// Palette for debug font (can be here or in globals/game_data if shared)
const u16 debug_font_palette[16] = {
    0x0000, 0x0EEE, 0x0EEE, 0x0EEE, 0x0EEE, 0x0EEE, 0x0EEE, 0x0EEE,
    0x0EEE, 0x0EEE, 0x0EEE, 0x0EEE, 0x0EEE, 0x0EEE, 0x0EEE, 0x0EEE
};

// u16 ind = TILE_USER_INDEX;
// Map* star_map;

int main()
{
    SYS_disableInts();

    VDP_init();
    SPR_init();
    JOY_init();
    JOY_setSupport(PORT_1, JOY_SUPPORT_6BTN);

    XGM_setPCM(SFX_LASER, sfx_laser, sizeof(sfx_laser)); // SFX_LASER from constants.h

    VDP_setScreenWidth320(); // Sets screen_width_pixels internally too via VDP_getScreenWidth
    //1 VDP_setPlaneSize(MAP_HW_WIDTH, MAP_HW_HEIGHT, TRUE); // Use TRUE for SGDK 1.7+ if using full 64x64 tilemap for one plane

    // Setup text plane (WINDOW)
    VDP_setTextPlane(WINDOW);
    VDP_setTextPalette(PAL3);
    VDP_setWindowHPos(FALSE, 0);
    VDP_setWindowVPos(FALSE, 0); // Usually 0 for top lines, or adjust

    // Get and store screen dimensions
    screen_width_pixels = VDP_getScreenWidth();
    screen_height_pixels = VDP_getScreenHeight();

    // Set scroll boundaries using defines from constants.h
    scroll_boundary_x1 = BBX;
    scroll_boundary_x2 = screen_width_pixels - BBX;
    scroll_boundary_y1 = BBY;
    scroll_boundary_y2 = screen_height_pixels - BBY;


    // Load Palettes
    //1 PAL_setPalette(PAL0, bg_far_palette.data, DMA_QUEUE);
    PAL_setPalette(PAL1, player_palette.data, DMA_QUEUE);
    //1 PAL_setPalette(PAL2, bg_near_palette.data, DMA_QUEUE);
    PAL_setPalette(PAL3, debug_font_palette, DMA_QUEUE);

    // Setup Background Planes
    VDP_setScrollingMode(HSCROLL_PLANE, VSCROLL_PLANE);
    initBackground(); // Initializes tiles, maps, and initial scroll

    // New background
    // u16 ind = TILE_USER_INDEX;
    // PAL_setPalette(PAL0, starbg.palette->data, DMA_QUEUE);
    // VDP_drawImageEx(BG_B, &starbg, TILE_ATTR_FULL(PAL0, FALSE, FALSE, FALSE, ind), 0, 0, FALSE, TRUE);

    // Initialize game entities
    initBullets();
    initFighters();

    // Create player sprite (player_x, player_y are from game_data.c)
    player_sprite = SPR_addSprite(&player_sprite_res,
                                player_x, player_y,
                                TILE_ATTR(PAL1, TRUE, FALSE, FALSE));

    // Start music
    XGM_setLoopNumber(-1);
    XGM_startPlay(track1);

    VDP_setBackgroundColor(0); // first index from PAL0 
    SYS_enableInts();

    // Main Game Loop
    while (1)
    {
        handleInput();
        updatePhysics();
        updateBullets();
        updateFighters();
        updateScrolling();

        SPR_setFrame(player_sprite, player_rotation_index);
        SPR_setPosition(player_sprite, player_x, player_y);


        // // --- Draw Debug Text ---
        // VDP_clearText(1, 1, DEBUG_TEXT_LEN + 6);
        // VDP_clearText(1, 2, DEBUG_TEXT_LEN + 6);
        // intToStr(player_x, text_vel_x, 0); // Using player_x from globals
        // intToStr(player_y, text_vel_y, 0); // Using player_y from globals
        // VDP_drawText("PosX:", 1, 1); VDP_drawText(text_vel_x, 7, 1);
        // VDP_drawText("PosY:", 1, 2); VDP_drawText(text_vel_y, 7, 2);
        // // char nfs[5]; intToStr(active_fighter_count, nfs, 0); VDP_drawText(nfs, 1, 3); // Example

        game_nframe++; // Use game_nframe from globals
        if (game_nframe >= 60){ // Use >= to ensure it resets
            game_nframe = 0;
        }

        SPR_update();
        SYS_doVBlankProcess();
    }
    return (0);
}