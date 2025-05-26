// player.c
#include <genesis.h>
#include "globals.h"   // For player variables, sin_fix, cos_fix, screen boundaries
#include "player.h"
#include "bullets.h"   // For fireBullet()

// --- Input Handling Function ---
void handleInput()
{
    u16 value = JOY_readJoypad(JOY_1);

    // --- Rotation ---
    if (player_rotation_iframe >= player_rotation_iframe_threshold){
        player_rotation_iframe = 0;

        if (value & BUTTON_LEFT) {
            if (player_rotation_index == player_rotation_index_max){
                player_rotation_index = 0;
            } else {
                player_rotation_index += 1;
            }
        } else if (value & BUTTON_RIGHT) {
            if (player_rotation_index == 0){
                player_rotation_index = player_rotation_index_max;
            } else {
                player_rotation_index -= 1;
            }
        }
    }
    player_rotation_iframe += 1;

    // --- Thrust ---
    player_vx = 0; // Default is no thrust applied.
    player_vy = 0;
    if (value & BUTTON_UP) {
        player_vx = -sin_fix[player_rotation_index];
        player_vy = -cos_fix[player_rotation_index];
        player_thrust_delay_timer = 0;
    }

    // Fire main weapon
    if (value & BUTTON_B) {
        fireBullet(); // Call fireBullet from bullets module
    }
    new_bullet_delay_timer += 1; // This is related to bullet firing rate
}

// --- Physics Update Function ---
void updatePhysics()
{
    s16 xtry, ytry; // Local temps for new position
    s16 thx, thy;   // Local temps for thrust calculation

    //Update position
    player_vx_applied = ( (player_vx + player_x_remainder + player_thrust_momentum_x ) >> 9);
    player_vy_applied = ( (player_vy + player_y_remainder + player_thrust_momentum_y ) >> 9);
    player_x_remainder = player_vx + player_x_remainder + player_thrust_momentum_x - player_vx_applied * 512;
    player_y_remainder = player_vy + player_y_remainder + player_thrust_momentum_y - player_vy_applied * 512;
    xtry = player_x + player_vx_applied;
    ytry = player_y + player_vy_applied;

    //Update thrust if joystick is held.
    thx = player_thrust_momentum_x + (player_vx >> 4);
    if (thx < 1024 && thx > -1024){ // Consider using FIX16 for these limits if they are scaled
        player_thrust_momentum_x = thx;
    }
    thy = player_thrust_momentum_y + (player_vy >> 4);
    if (thy < 1024 && thy > -1024){
        player_thrust_momentum_y = thy;
    }

    //Update momentum by applying friction
    if (player_thrust_delay_timer < player_thrust_delay_max && player_thrust_counter > 100){ // magic number 100 <-- should be parameterized
        player_thrust_delay_timer += 1;
        player_thrust_counter = 0;
        if (player_vx == 0){
            player_thrust_momentum_x = player_thrust_momentum_x >> 1;
        }
        if (player_vy == 0){
            player_thrust_momentum_y = player_thrust_momentum_y >> 1;
        }
    }
    if (player_thrust_delay_timer >= player_thrust_delay_max){
        player_thrust_momentum_x = 0;
        player_thrust_momentum_y = 0;
    }

    if (player_thrust_counter < 101){ //catch runaway counter if player is idle for a long time.
        player_thrust_counter += 1;
    }
    

    // Keep spacecraft in bounds and determine scroll delta
    if (xtry > scroll_boundary_x1 && xtry < scroll_boundary_x2){
        player_x = xtry;
        player_scroll_delta_x = 0;
    } else {
        player_scroll_delta_x = (xtry - player_x);
        // player_x doesn't change here if scrolling, world moves instead
    }

    if (ytry > scroll_boundary_y1 && ytry < scroll_boundary_y2){
        player_y = ytry;
        player_scroll_delta_y = 0;
    } else {
        player_scroll_delta_y = (ytry - player_y);
        // player_y doesn't change here
    }
}