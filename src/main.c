#include <genesis.h>
#include <maths.h>
#include "res/resources.h"

// --- Pre-calculated Sine/Cosine Tables ---
// Scaled by 255, 24 steps (+1 for wraparound)
static const s16 sin_fix[] = {
      0,  65, 127, 180, 220, 246, 255, 246, 220, 180, 127,  65,
      0, -65,-127,-180,-220,-246,-255,-246,-220,-180,-127, -65, 0 // Index 24 = Index 0
};
static const s16 cos_fix[] = {
    255, 246, 220, 180, 127,  65,   0, -65,-127,-180,-220,-246,
   -255,-246,-220,-180,-127, -65,   0,  65, 127, 180, 220, 246, 255 // Index 24 = Index 0
};
// Calculate the number of unique steps (excluding the wrap-around entry)
#define SINCOS_TABLE_STEPS (sizeof(sin_fix) / sizeof(sin_fix[0]) - 1) // Should be 24

// --- Game Variables ---
Sprite* player_sprite;

// Spacecraft properties
#define SHIP_ROT_SPEED 3 // How fast the spaceship can rotate, must be >= 1.
// Makes rotation of ship slower
s16 iframe     = 0;
s16 iframe_old = SHIP_ROT_SPEED;

s16 ri     = 0;   // current rotation info for spaceship
s16 ri_max = 23;  // max rotations 
// Initial position and velocity of spacecraft
s16 x      = 144;  //Screen-coordinates of spacecraft
s16 y      = 104;
s16 vx     = 0;   //Requested velocity of spacecraft.
s16 vy     = 0;
s16 vxapp  = 0;   //Applied velocity of spacecraft.
s16 vyapp  = 0;

s16 xtry = 144; //For displaying Space ship
s16 ytry = 104;
s16 xrem = 0; //Tracking remainder for smooth motion of space ship
s16 yrem = 0;

s16 tdelay = 0;     // Counter for thrust/momentum/friction 
s16 tdelay_max = 8; // momentum
s16 tcount = 0;

s16 thrust_x = 0;       // Initialize amount of thrust applied (acts like momentum)
s16 thrust_y = 0;

s16 thx = 0; //Checking thrust for max allowed values.
s16 thy = 0;


// --- ADD BUFFERS FOR DEBUG TEXT ---
#define DEBUG_TEXT_LEN 16 // Max length for the velocity strings
char text_vel_x[DEBUG_TEXT_LEN];
char text_vel_y[DEBUG_TEXT_LEN];
// -----------------------------------

// Function prototypes
void handleInput();
void updatePhysics(); // Keep the zero-crossing version for now

// --- Main Function ---
int main()
{
    SYS_disableInts();

    VDP_init();
    SPR_init();
    JOY_init();
    // VDP text system is implicitly initialized by VDP_init

    VDP_setScreenWidth320();
    VDP_setTextPlane(BG_B); // Draw text on background plane B (usually above BG_A)
    VDP_setTextPalette(0);  // Use palette 0 for text (standard white/black)

    PAL_setPalette(PAL1, player_palette.data, DMA_QUEUE);


    // Create sprite
    player_sprite = SPR_addSprite(
                        &player_sprite_res,
                        x,
                        y,
                        TILE_ATTR(PAL1, TRUE, FALSE, FALSE));

    // DEBUG Check
    if (player_sprite == NULL) {
         PAL_setColor(18, 0x00E0);
         VDP_setBackgroundColor(18);
         while(1) { SYS_doVBlankProcess(); }
    }

    VDP_setBackgroundColor(0);
    SYS_enableInts();

    // Main Game Loop
    while (1)
    {

        vx = 0;
        vy = 0;
        handleInput();
        updatePhysics(); // Update velocities BEFORE drawing them

        // --- Set Sprite Frame based on Rotation ---
        SPR_setFrame(player_sprite, ri); // Use 'ri' to select the frame

        // --- Draw Debug Text ---
        // Clear previous text (optional, avoids ghosting if text length changes)
        VDP_clearText(1, 1, DEBUG_TEXT_LEN + 6); // Clear area for X velocity (X=1, Y=1, Length="VelX: "+value)
        VDP_clearText(1, 2, DEBUG_TEXT_LEN + 6); // Clear area for Y velocity (X=1, Y=2, Length="VelY: "+value)

        // Convert fix16 velocities to strings (e.g., 3 decimal places)
        intToStr(x, text_vel_x, 0);
        intToStr(y, text_vel_y, 0);

        // Draw labels and values
        VDP_drawText("PosX:", 1, 1);
        VDP_drawText(text_vel_x, 7, 1); // Draw value starting at column 7
        VDP_drawText("PosY:", 1, 2);
        VDP_drawText(text_vel_y, 7, 2); // Draw value starting at column 7
        // -----------------------

        // Update Graphics
        SPR_setPosition(player_sprite,
                        x,
                        y);

        SPR_update();
        SYS_doVBlankProcess(); // VDP text updates happen during VBlank
    }
    return (0);
}

// --- Input Handling Function ---
void handleInput()
{
    u16 value = JOY_readJoypad(JOY_1);

    // --- Rotation ---
    if (iframe >= iframe_old){
        iframe = 0;

        if (value & BUTTON_LEFT) {

            if (ri == ri_max){
                ri = 0;
            } else {
                ri += 1;
            }

        } else if (value & BUTTON_RIGHT) {

            if (ri == 0){
                ri = ri_max;
            } else {
                ri -= 1;
            }
        }

        // --- Thrust ---
        if (value & BUTTON_UP) {

            vx = -sin_fix[ri];
            vy = -cos_fix[ri];
            tdelay = 0;
            
        }
    }
    iframe += 1;
}

// --- Physics Update Function ---
void updatePhysics()
{

    //Update position
    vxapp = ( (vx + xrem + thrust_x ) >> 9); //Apply velocity, remainder and momentum 
    vyapp = ( (vy + yrem + thrust_y ) >> 9); // 9 and 512 must balance (e.g., 2^9 = 512)
    xrem = vx + xrem + thrust_x - vxapp * 512; //Update remainder
    yrem = vy + yrem + thrust_y - vyapp * 512;
    xtry = x + vxapp; //Update ship position
    ytry = y + vyapp;

    //Update thrust if joystick is held.
    thx = thrust_x + (vx >> 4);
    if (thx < 1024 && thx > -1024){
        thrust_x = thx;
    }
    thy = thrust_y + (vy >> 4);
    if (thy < 1024 && thy > -1024){
        thrust_y = thy;
    }

    //Update momentum by applying friction 
    if (tdelay < tdelay_max && tcount > 50){
        tdelay += 1;
        tcount = 0;
        if (vx == 0){
            thrust_x = thrust_x >> 1;
        }
        if (vy == 0){
            thrust_y = thrust_y >> 1;
        }
    }
    if (tdelay >= tdelay_max){
        thrust_x = 0;
        thrust_y = 0;
    }
    tcount += 1;


    // --- Update Position ---
    x = xtry;
    y = ytry;


    // --- Screen Wrapping ---
    const s16 screen_w = VDP_getScreenWidth();
    const s16 screen_h = VDP_getScreenHeight();

    if (x < 0) {
        x = x + screen_w;
    } else if (x >= screen_w) {
        x = x - screen_w;
    }

    if (y < 0) {
        y = y + screen_h;
    } else if (y >= screen_h) {
        y = y - screen_h;
    }
}