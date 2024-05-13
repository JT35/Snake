import pygame
from sys import exit
from os.path import join

CELL_SIZE = 80
ROW_COUNT = 10
COLUMN_COUNT = 16

WINDOW_WIDTH = COLUMN_COUNT * CELL_SIZE
WINDOW_HEIGHT = ROW_COUNT * CELL_SIZE

# Colours
LIGHT_GREEN = '#AAD751'
DARK_GREEN = "#A2D149"

# Starting position
START_LENGTH = 3
START_ROW = ROW_COUNT // 2
START_COLUMN = START_LENGTH + 2

# Shadow
SHADOW_SIZE = pygame.Vector2(4,4)
SHADOW_OPACITY = 50