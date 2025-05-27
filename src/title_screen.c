// title_screen.c
#include <genesis.h>
#include "globals.h" // For Fighter struct, fighters array, player_x/y, map constants, screen_width_pixels etc.
#include "res/resources.h" 
#include "title_screen.h"


u16 button_delay = 30;
u16 fcounter_l = 0;
u16 fcounter_r = 0;

void title_screen(){

	VDP_drawText("  Ready?  ", 15, 13);
    VDP_drawText("Push Start", 15, 14);

    intToStr(game_level, text_vel_x, 2);
    VDP_drawText(" Level:   ", 15, 15);
    VDP_drawText(text_vel_x  , 22, 15);

    fcounter_l = 0;
    fcounter_r = 0;

    u16 value_old = JOY_readJoypad(JOY_1);

    while(1){
        
        
        u16 value = JOY_readJoypad(JOY_1);

        if (value != value_old){
        	value_old = value;
        	fcounter_l = 0;
        	fcounter_r = 0;
        }

        if (value & BUTTON_START) {
            break;  // Let's start the game.
        }

        if (value & BUTTON_LEFT){
        	if (fcounter_l == 0){
	        	game_level -= 1;
	        	if (game_level < 1){
	        		game_level = 1;
	        	}
	        	fcounter_l = 1;
	        }
        }

        if (value & BUTTON_RIGHT){
        	if (fcounter_r == 0){
	        	game_level += 1;
	        	if (game_level > 10){
	        		game_level = 10;
	        	}
	        	fcounter_r = 1;
	        }
        }

        if (game_level != game_level_old){
        	game_level_old = game_level;
        	VDP_clearText(15, 15, DEBUG_TEXT_LEN + 6);
        	intToStr(game_level, text_vel_x, 2);
		    VDP_drawText(" Level:   ", 15, 15);
		    VDP_drawText(text_vel_x  , 22, 15);
        }

        
        if (fcounter_l > button_delay){
        	fcounter_l = 0;
        }
        if (fcounter_l > 0){
        	fcounter_l += 1;
        }

        if (fcounter_r > button_delay){
        	fcounter_r = 0;
        }
        if (fcounter_r > 0){
        	fcounter_r += 1;
        }

        SPR_update();
        SYS_doVBlankProcess();
    }

    VDP_clearText(15, 13, DEBUG_TEXT_LEN + 6);
    VDP_clearText(15, 14, DEBUG_TEXT_LEN + 6);
    VDP_clearText(15, 15, DEBUG_TEXT_LEN + 6);
    game_level_old = 0; // Reset to allow screen updates
    efire_cooldown_timer = 4 * (5 - game_level);
    if (efire_cooldown_timer > 16){
        efire_cooldown_timer = 16;
    }
    else if (efire_cooldown_timer < 4){
        efire_cooldown_timer = 4;
    }

}

// Set up scoring and level details
void init_game_vars(){
	player_score = 0;
    player_score_old = 1;
    fighters_score = 0;
    fighters_score_old = 1;
    score_to_win = 100;
    game_level = 1;
    game_level_old = 0;
}