from settings import *
from random import choice
from math import sin

class Apple:
    def __init__(self, snake):
        self.position = pygame.Vector2()
        self.window = pygame.display.get_surface()
        self.snake = snake
        self.set_position()

        self.surface = pygame.image.load(join('resources', 'graphics', 'apple.png')).convert_alpha()
        self.scaled_surface = self.surface.copy()
        self.scaled_rect = self.scaled_surface.get_rect(
            center = (self.position.x * CELL_SIZE + CELL_SIZE / 2, self.position.y * CELL_SIZE + CELL_SIZE / 2))

    def set_position(self):
        available_positions = [pygame.Vector2(x,y) for x in range(COLUMN_COUNT) for y in range(ROW_COUNT) 
                               if pygame.Vector2(x,y) not in self.snake.body]
        self.position = choice(available_positions)

    def consume(self, audio_file):
        self.snake.has_eaten = True
        self.set_position()
        audio_file.play()

    def draw(self):
        scale = 1 + sin(pygame.time.get_ticks() / 600) / 3
        self.scaled_surface = pygame.transform.smoothscale_by(self.surface, scale)
        self.scaled_rect = self.scaled_surface.get_rect(
            center = (self.position.x * CELL_SIZE + CELL_SIZE / 2, self.position.y * CELL_SIZE + CELL_SIZE / 2))
        self.window.blit(self.scaled_surface, self.scaled_rect)