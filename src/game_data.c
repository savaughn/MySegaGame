// game_data.c
#include "globals.h" // Includes genesis.h, constants.h, res/resources.h

// Screen Dimensions
s16 screen_width_pixels;
s16 screen_height_pixels;

// Scroll Boundaries
s16 scroll_boundary_x1; s16 scroll_boundary_x2;
s16 scroll_boundary_y1; s16 scroll_boundary_y2;

// Background Scroll Offsets
s16 scroll_a_x = 0; s16 scroll_a_y = 0;
s16 scroll_b_x = 0; s16 scroll_b_y = 0;

// Sine/Cosine Tables
const s16 sin_fix[] = {
      0,  65, 127, 180, 220, 246, 255, 246, 220, 180, 127,  65,
      0, -65,-127,-180,-220,-246,-255,-246,-220,-180,-127, -65, 0
};
const s16 cos_fix[] = {
    255, 246, 220, 180, 127,  65,   0, -65,-127,-180,-220,-246,
   -255,-246,-220,-180,-127, -65,   0,  65, 127, 180, 220, 246, 255
};

// Player Sprite
Sprite* player_sprite;

// Player/Spacecraft properties
s16 player_x = 144; s16 player_y = 104;
s16 player_vx = 0; s16 player_vy = 0;
s16 player_vx_applied = 0; s16 player_vy_applied = 0;
s16 player_x_remainder = 0; s16 player_y_remainder = 0;
s16 player_rotation_index = 0;
const s16 player_rotation_index_max = 23;
s16 player_rotation_iframe = 0;
const s16 player_rotation_iframe_threshold = SHIP_ROT_SPEED;
s16 player_thrust_delay_timer = 0;
const s16 player_thrust_delay_max = 8;
s16 player_thrust_counter = 0;
s16 player_thrust_momentum_x = 0;
s16 player_thrust_momentum_y = 0;
s16 player_scroll_delta_x = 0;
s16 player_scroll_delta_y = 0;

// Bullet Pool and related
Bullet bullets[NBULLET];
u16 fire_cooldown_timer = 0;
u16 current_bullet_index = 0;
u16 new_bullet_delay_timer = 0;

// EBullet Pool and related
Bullet ebullets[NEBULLET];
u16 efire_cooldown_timer = 16;
u16 current_ebullet_index = 0;
u16 new_ebullet_delay_timer = 0;

// SBullet Pool and related
Bullet sbullets[NSBULLET];
u16 sfire_cooldown_timer = 0;
u16 current_sbullet_index = 0;
u16 new_sbullet_delay_timer = 0;

// Fighter Pool and related
Fighter fighters[NFIGHTER_MAX];
Fighter fexplode[NFIGHTER_MAX];
s16 active_fighter_count = NFIGHTER_MAX; // Initial number of fighters

// Debug Text Buffers
char text_vel_x[DEBUG_TEXT_LEN];  // defaulting to 16
char text_vel_y[DEBUG_TEXT_LEN];

// General frame counter
s16 game_nframe = 0;

// Backgrounds
u16 ind = TILE_USER_INDEX;

// Score
u16 player_score = 0;
u16 player_score_old = 1;
u16 fighters_score = 0;
u16 fighters_score_old = 1;
u16 score_to_win = 10;
u16 game_level = 1;
u16 game_level_old = 1;