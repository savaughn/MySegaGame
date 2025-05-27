// bullets.c
#include <genesis.h>
#include "globals.h" // For Bullet struct, bullets array, player_x/y, sin_fix, cos_fix, screen_width_pixels, etc.
#include "game_level_screen.h"
#include "res/resources.h" // For sprites



void level_up(){


	// Game over loop
    
    XGM2_stop();
    if (player_score > fighters_score){
        VDP_drawText(" You Win! ", 15, 13);

        game_level += 1;
        efire_cooldown_timer -= 4;
        if (efire_cooldown_timer < 4){
            efire_cooldown_timer = 4;
        }

        // player_score = 0;
        // player_score_old = 1;
        // fighters_score = 0;
        // fighters_score_old = 1;
        score_to_win += 100;

    }
    else {
        VDP_drawText(" You Lose ", 15, 13);

        player_score = 0;
        player_score_old = 1;
        fighters_score = 0;
        fighters_score_old = 1;
    }

    VDP_drawText("Push Start", 15, 14);
    while(1){
        
        u16 value = JOY_readJoypad(JOY_1);
        if (value & BUTTON_START) {
            break;
        }

        SPR_update();
        SYS_doVBlankProcess();
    }

    VDP_clearText(15, 13, DEBUG_TEXT_LEN + 6);
    VDP_clearText(15, 14, DEBUG_TEXT_LEN + 6);


    XGM2_play(track1);

}