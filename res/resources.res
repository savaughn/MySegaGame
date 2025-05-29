// res/resources.res


// // Background Layer (Far Stars - Plane B)
// PALETTE bg_far_palette      "far_stars_tiles.png"
// TILESET bg_far_tiles        "far_stars_tiles.png" NONE
//
// // Foreground Layer (Near Stars - Plane A)
// PALETTE bg_near_palette     "near_stars_tiles.png"
// TILESET bg_near_tiles       "near_stars_tiles.png" NONE

// Image for background
IMAGE 	starbg 			        "Star_Map.png" 		BEST 
IMAGE   title 					"Title_screen.png"	BEST

// Sprite Resources
SPRITE  player_sprite_res     	"player_sprite_sheet.png"   2    2    NONE        0         NONE      NONE
SPRITE  mine_explode_res        "Mine_explode.png"          2    2    NONE        0         NONE      NONE
SPRITE  bullet_sprite_res     	"bullet_sprite.png"         1    1    NONE        0         NONE      NONE
SPRITE  sbullet_sprite_res     	"sbullet_sprite.png"        1    1    NONE        0         NONE      NONE
SPRITE  ebullet_sprite_res      "ebullet_sprite.png"        1    1    NONE        0         NONE      NONE
SPRITE  fighter_sprite_res     	"fighter_sprite-Sheet.png"  1    1    NONE        0         NONE      NONE
SPRITE  fighter_explode_res     "Fighter_explode.png"       1    1    NONE		  0			NONE	  NONE
SPRITE  space_mine_res			"spaceMine-sheet.png"		1    1    NONE  	  0 		NONE      NONE

// Palettes
PALETTE player_palette        	"Fighter_explode.png"
PALETTE player_pal2				"Player_PAL2.png"
PALETTE player_pal3				"Player_PAL3.png"
PALETTE player_pal4				"Player_PAL4.png"

PALETTE star_bg_pal 	        "Star_Map.png"

PALETTE title_pal_1				"Title_screen.png"
PALETTE title_pal_2				"TS_P2.png"
PALETTE title_pal_3				"TS_P3.png"
PALETTE title_pal_4				"TS_P4.png"

// Sound effects
WAV 	sfx_laser 				"laser.wav" 				  XGM2
WAV     sfx_elaser				"elaser.wav"				  XGM2
WAV     sfx_explode				"explosion_decompression.wav" XGM2
WAV     sfx_ding                "shield_ready.wav"			  XGM2
WAV     sfx_turbo				"turbo_jet.wav"				  XGM2
WAV     sfx_mexplode            "mexplode.wav"                XGM2

// Songs
XGM2 	track1 					"UpBeat.vgm"	
XGM2 	title_music 			"Title_music.vgm"	