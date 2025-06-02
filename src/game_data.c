// game_data.c
#include "globals.h" // Includes genesis.h, constants.h, res/resources.h

// Screen Dimensions
s16 screen_width_pixels;
s16 screen_height_pixels;
s16 screen_width_pixels_d2; //dimensions / 2
s16 screen_height_pixels_d2; 

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

// Sine/Cosine Tables
const s16 sin_fix_d2[] = {
      0,  32,  63,  90, 110, 123, 127, 123, 110,  90,  63,  32,    
      0, -32, -63, -90,-110,-123,-127,-123,-110, -90, -63, -32,   0
};
const s16 cos_fix_d2[] = {
    127, 123, 110,  90,  63,  32,   0, -32, -63, -90,-110,-123,
   -127,-123,-110, -90, -63, -32,   0,  32,  63,  90, 110, 123, 127
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
s16 boost_factor = 5; 

// Player D-control
u8 dpadUp;
u8 dpadDown;
u8 dpadLeft;
u8 dpadRight;

// Bullet Pool and related
Bullet bullets[NBULLET];
u16 fire_cooldown_timer = 0;
u16 current_bullet_index = 0;
u16 new_bullet_delay_timer = 0;

// EBullet Pool and related
Bullet ebullets[NEBULLET];
u16 efire_cooldown_timer = 16;
u16 efire_cooldown_timer_min = 4;  // 4 is the minimum.. anything less breaks game.
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
s16 fighter_speed_1 = 8;   //8
s16 fighter_speed_2 = 256; //256 was default 9/512 is a bit too slow
u16 game_ai_decision = 20000;      // when ships will change direction (when == game_nframe)

// s16 game_ai_decision_time = 60; // How often to reset game_nframe
// s16 game_ai_rand = 0;           // AI random number

// Debug Text Buffers
char text_vel_x[DEBUG_TEXT_LEN];  // defaulting to 16
char text_vel_y[DEBUG_TEXT_LEN];

// General frame counter
s16 game_nframe = 0;

// Backgrounds
u16 ind = TILE_USER_INDEX;
u16 ind_sc = 0;

// Score
s16 player_score = 0;
s16 player_score_old = 1;
u16 fighters_score = 0;
u16 fighters_score_old = 1;
u16 game_level = 1;
u16 game_level_old = 2;
u16 score_to_win = 100;
u16 game_score = 0;
u16 game_score_old = 1;

// HUD
u16 player_tiles;
// u16 player_tiles_red;
u16 coffset;
u16 STRIP_TILE_8_IDX;
u16 EMPTY_BAR_TILE_IDX;

// Title screen
s16 control_style = 1;
s16 control_style_old = 0;

// Shield
u16 new_shield_delay_timer = 0;
u16 shield_delay_max = 30;
u16 shield_timer = 0;
u16 shield_duration = 30;
u16 shield_pal = 0;
s16 shield_status = -1; // Shield is off.
u16 shield_pal_timer = 0;
u16 shield_pal_timer_switch = 10;

// Boost
u16 player_boost_timer = 0;
u16 player_boost_timer_max = 20; // How long the boost lasts
u16 player_boost_delay_timer = 60;
u16 player_boost_delay_timer_max = 60; // How often the player can boost
s16 player_boost_status = -1; // If boost is enabled

// Space Mines
s16 mine_status = 0; // No mine is placed
s16 mine_x = 0;
s16 mine_y = 0;
u16 mine_timer      = 0;   // Time for mine to arm itself
u16 mine_timer_max  = 30; // 120 -> 2 seconds to get away
s16 mexplode_status = 0;
Sprite* mine_sprite_ptr;
Sprite* mexplode_sprite_ptr;


