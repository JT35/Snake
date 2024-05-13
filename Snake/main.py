from settings import *
from snake import Snake
from apple import Apple

class Main:
    def __init__(self):
        # General
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Snake')

        # Game objects
        self.bg_tiles = [pygame.Rect((column + int(row % 2 == 0)) * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE) 
                         for column in range(0, COLUMN_COUNT, 2) for row in range(ROW_COUNT)]
        self.snake = Snake()
        self.apple = Apple(self.snake)

        # Timer
        self.update_event = pygame.event.custom_type()
        pygame.time.set_timer(self.update_event, 200)
        self.game_active = False

        # Audio
        self.crunch_sound = pygame.mixer.Sound(join('resources', 'audio', 'crunch.wav'))
        self.bg_music = pygame.mixer.Sound(join('resources', 'audio', 'arcade.ogg'))
        self.bg_music.set_volume(0.5)
        self.bg_music.play(-1)

    def draw_bg(self):
        self.window.fill(LIGHT_GREEN)
        for tile in self.bg_tiles:
            pygame.draw.rect(self.window, DARK_GREEN, tile)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]: 
            self.snake.direction = pygame.Vector2(1,0) if self.snake.direction.x != -1 else self.snake.direction
        if keys[pygame.K_LEFT]: 
            self.snake.direction = pygame.Vector2(-1,0) if self.snake.direction.x != 1 else self.snake.direction
        if keys[pygame.K_UP]: 
            self.snake.direction = pygame.Vector2(0,-1) if self.snake.direction.y != 1 else self.snake.direction
        if keys[pygame.K_DOWN]: 
            self.snake.direction = pygame.Vector2(0,1) if self.snake.direction.y != -1 else self.snake.direction

    def check_collisions(self):
        # Apple
        if self.snake.body[0] == self.apple.position:
            self.apple.consume(self.crunch_sound)

        # Self and Boundaries
        if self.snake.body[0] in self.snake.body[1:] or \
            not 0 <= self.snake.body[0].x < COLUMN_COUNT or \
            not 0 <= self.snake.body[0].y < ROW_COUNT:
            # Game Over
            self.snake.die()
            self.game_active = False

    def draw_shadow(self):
        shadow_surface = pygame.Surface((self.window.get_size()))
        shadow_surface.fill((0,255,0))
        shadow_surface.set_colorkey((0,255,0))

        # Surface
        shadow_surface.blit(self.apple.scaled_surface, self.apple.scaled_rect.topleft + SHADOW_SIZE)
        for surface, rect in self.snake.draw_data:
            shadow_surface.blit(surface, rect.topleft + SHADOW_SIZE)
        
        mask = pygame.mask.from_surface(shadow_surface)
        mask.invert()
        shadow_surface = mask.to_surface()
        shadow_surface.set_colorkey((255,255,255))
        shadow_surface.set_alpha(SHADOW_OPACITY)

        self.window.blit(shadow_surface, (0,0))

    def play(self):
        while True:
            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                
                if event.type == self.update_event and self.game_active:
                    self.snake.update()

                if event.type == pygame.KEYDOWN and not self.game_active:
                    self.game_active = True

            # Updates
            self.handle_input()
            self.check_collisions()

            # Drawing
            self.draw_bg()
            self.draw_shadow()
            self.snake.draw()
            self.apple.draw()
            pygame.display.update()

if __name__ == '__main__':
    game = Main()
    game.play()
