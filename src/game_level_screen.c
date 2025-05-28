// bullets.c
#include <genesis.h>
#include "globals.h" // For Bullet struct, bullets array, player_x/y, sin_fix, cos_fix, screen_width_pixels, etc.
#include "game_level_screen.h"
#include "clear_sprites.h"
#include "res/resources.h" // For sprites

#include "bullets.h"
#include "ebullets.h"
#include "sbullets.h"
#include "fighters.h"

#include "title_screen.h"
#include "background.h"

void level_up(){


	// Game over loop

    u8 game_over = 0;
    u16 value;
    u16 value_old;
    
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
        VDP_drawText(" You Lose ", 15, 13);  // This is the game-over part...

        // Once we have a proper game loop the next 4 lines can probably be removed.
        player_score = 0;
        player_score_old = 1;
        fighters_score = 0;
        fighters_score_old = 1;

        game_over = 1;
    }

    VDP_drawText("Push Start", 15, 14);
    while(1){
        
        value = JOY_readJoypad(JOY_1);
        if (value & BUTTON_START) {
            break;
        }

        SPR_update();
        SYS_doVBlankProcess();
    }

    VDP_clearText(15, 13, DEBUG_TEXT_LEN + 6); // Remove text
    VDP_clearText(15, 14, DEBUG_TEXT_LEN + 6);

    // Reset game.
    if (game_over){

        // u8 x = 0;
        // while(x == 0){
        //     value = JOY_readJoypad(JOY_1);
        //     if ((value & BUTTON_START) & (value_old != value)){
        //         x = 1;
        //     } else {
        //         value_old = value;
        //     }
        // }
        

        // This fucking won't work....
        value_old = JOY_readJoypad(JOY_1);
        u8 x = 1;
        while(x){
            value = JOY_readJoypad(JOY_1);
            if (value != value_old){
                x = 0;
            } 
            // else {
            //     VDP_clearText(1, 5, DEBUG_TEXT_LEN + 6);
            //     intToStr(value, text_vel_x, 5);
            //     VDP_drawText("Button ", 1, 5);
            //     VDP_drawText(text_vel_x , 9, 5);
            //     value_old = value;
            // }

            SPR_update();
            SYS_doVBlankProcess();
        }

        // VDP_clearText(1, 5, DEBUG_TEXT_LEN + 6);

        // VDP_drawText("Hello? ", 1, 7);

        clear_sprites();

        init_game_vars(); // Set up player/enemy scores

        title_screen();   // Show title screen.

        initBackground(); // Initializes tiles, maps, and initial scroll

        // Initialize game entities
        initBullets();
        init_SBullets();
        initFighters();
        init_eBullets();

        // Create player sprite (player_x, player_y are from game_data.c)
        player_sprite = SPR_addSprite(&player_sprite_res,
                                    player_x, player_y,
                                    TILE_ATTR(PAL1, TRUE, FALSE, FALSE));

    }




    XGM2_play(track1);

}