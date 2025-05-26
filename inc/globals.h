// globals.h
#ifndef GLOBALS_H
#define GLOBALS_H

#include <genesis.h> // For Sprite, u16, s16 etc.
#include "res/resources.h" // For bg_far_tiles.numTile etc.
#include "constants.h"     // Include our constants

// --- Struct Definitions ---
typedef struct {
    s16 status;
    s16 x;
    s16 y;
    s16 bvxrem;
    s16 bvyrem;
    s16 new_bullet; // Renamed from 'new' to avoid keyword clash if C++ compiler/linter
    Sprite* sprite_ptr;
} Bullet;

typedef struct {
    s16 status;
    s16 x;
    s16 y;
    s16 lx1old; // Consider if these 'old' vars are still needed
    s16 lx2old;
    s16 ly1old;
    s16 ly2old;
    s16 dx;
    s16 dy;
    s16 vx;
    s16 vy;
    s16 vxi;
    s16 vyi;
    s16 xrem;
    s16 yrem;
    s16 new_fighter; // Renamed
    s16 nframe_fighter; // Renamed to avoid clash with global nframe
    Sprite* sprite_ptr;
} Fighter;


// --- Global Variables (declared as extern) ---

// Screen Dimensions (Consolidated)
extern s16 screen_width_pixels;
extern s16 screen_height_pixels;

// Scroll Boundaries
extern s16 scroll_boundary_x1; // Renamed BX1
extern s16 scroll_boundary_x2; // Renamed BX2
extern s16 scroll_boundary_y1; // Renamed BY1
extern s16 scroll_boundary_y2; // Renamed BY2

// Background Scroll Offsets
extern s16 scroll_a_x; extern s16 scroll_a_y; // Plane A (Near)
extern s16 scroll_b_x; extern s16 scroll_b_y; // Plane B (Far)
// extern s16 scroll_x; extern s16 scroll_y; // Overall map scroll if different (seems covered by dx/dy from player)

// Sine/Cosine Tables
extern const s16 sin_fix[];
extern const s16 cos_fix[];
#define SINCOS_TABLE_STEPS (24) // Hardcode for now based on data, or calculate in game_data.c

// Player Sprite
extern Sprite* player_sprite;

// Background Map Data Arrays
// These are large, could be static in background.c if only used there.
// If generateRandomMapLayer is in background.c and uses them, they can be static there.
// Let's make them static in background.c for now to keep globals.h cleaner.
// extern u16 farMapData[MAP_HW_WIDTH * MAP_HW_HEIGHT];
// extern u16 nearMapData[MAP_HW_WIDTH * MAP_HW_HEIGHT];

// Player/Spacecraft properties
extern s16 player_x; extern s16 player_y;
extern s16 player_vx; extern s16 player_vy;
extern s16 player_vx_applied; extern s16 player_vy_applied; // Renamed vxapp, vyapp
extern s16 player_x_remainder; extern s16 player_y_remainder; // Renamed xrem, yrem
extern s16 player_rotation_index; // Renamed ri
extern const s16 player_rotation_index_max; // Renamed ri_max
extern s16 player_rotation_iframe; // Renamed iframe
extern const s16 player_rotation_iframe_threshold; // Renamed iframe_old
extern s16 player_thrust_delay_timer; // Renamed tdelay
extern const s16 player_thrust_delay_max; // Renamed tdelay_max
extern s16 player_thrust_counter; // Renamed tcount
extern s16 player_thrust_momentum_x; // Renamed thrust_x
extern s16 player_thrust_momentum_y; // Renamed thrust_y
extern s16 player_scroll_delta_x; // Renamed dx (player's contribution to scroll)
extern s16 player_scroll_delta_y; // Renamed dy

// Bullet Pool and related
extern Bullet bullets[NBULLET];
extern s16 fire_cooldown_timer; // Renamed fire_cooldown
extern s16 current_bullet_index; // Renamed bullet_c
extern s16 new_bullet_delay_timer; // Renamed bullet_timer
// extern s16 bullet_vx_req; // Renamed bvx - seems calculated on the fly
// extern s16 bullet_vy_req; // Renamed bvy
// extern s16 bullet_vx_applied; // Renamed bvxapp
// extern s16 bullet_vy_applied; // Renamed bvyapp

// E-Bullet Pool
extern Bullet ebullets[NEBULLET];
extern s16 efire_cooldown_timer; 
extern s16 current_ebullet_index; 
extern s16 new_ebullet_delay_timer; 

// Fighter Pool and related
extern Fighter fighters[NFIGHTER_MAX];
extern Fighter fexplode[NFIGHTER_MAX];
extern s16 active_fighter_count; // Renamed nfighter (maybe better to count active ones)

// Debug Text Buffers
extern char text_vel_x[DEBUG_TEXT_LEN];
extern char text_vel_y[DEBUG_TEXT_LEN];

// General frame counter
extern s16 game_nframe; // Renamed nframe to be more specific

// Tile indexing based on resource sizes
#define BG_NEAR_TILE_INDEX (BG_FAR_TILE_INDEX + bg_far_tiles.numTile)

// Loading background map
extern u16 ind;

// Scores
extern u16 player_score;
extern u16 player_score_old;
extern u16 fighters_score;
extern u16 fighters_score_old;
extern u16 score_to_win;

#endif // GLOBALS_H