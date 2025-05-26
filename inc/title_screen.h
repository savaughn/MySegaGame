// title_screen.h
#ifndef TITLE_SCREEN_H
#define TITLE_SCREEN_H

#include <genesis.h> // For u16

void joyEvent(u16 joy, u16 changed, u16 state);
void title_screen(void);
void init_game_vars(void);

#endif // TITLE_SCREEN_H