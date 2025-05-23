// background.h
#ifndef BACKGROUND_H
#define BACKGROUND_H

#include <genesis.h> // For u16

void initBackground(void); // For initial setup if needed, like clearing map data
void generateRandomMapLayer(u16* mapData, u16 mapWidth, u16 mapHeight, u16 baseTileIndex, u16 numTilesInSet, u16 pal);
void updateScrolling(void);

#endif // BACKGROUND_H