from settings import *
from os import walk

class Snake:
    def __init__(self):
        # Setup
        self.window = pygame.display.get_surface()
        self.body = [pygame.Vector2(START_COLUMN - column, START_ROW) for column in range(START_LENGTH)]
        self.direction = pygame.Vector2(1,0)
        
        self.has_eaten = False

        # Graphics
        self.surfaces = self.import_surfaces()
        self.draw_data = []
        self.head_surface = self.surfaces['head_right']
        self.tail_surface = self.surfaces['tail_left']
        
        self.update_body()

    def import_surfaces(self):
        surface_dict = {}
        for folder_path, _, image_names in walk(join('resources', 'graphics', 'snake')):
            for image_name in image_names:
                full_path = join(folder_path, image_name)
                surface = pygame.image.load(full_path).convert_alpha()
                surface_dict[image_name.split('.')[0]] = surface
        return surface_dict

    def update(self):
        body_copy = self.body[:-1] if not self.has_eaten else self.body[:]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy[:]
        if self.has_eaten:
            self.has_eaten = False

        self.update_head()
        self.update_tail()
        self.update_body()

    def die(self):
        self.body = [pygame.Vector2(START_COLUMN - column, START_ROW) for column in range(START_LENGTH)]
        self.direction = pygame.Vector2(1,0)

        self.update_head()
        self.update_tail()
        self.update_body()

    def update_head(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == pygame.Vector2(-1,0): self.head_surface = self.surfaces['head_right']
        elif head_relation == pygame.Vector2(1,0): self.head_surface = self.surfaces['head_left']
        elif head_relation == pygame.Vector2(0,-1): self.head_surface = self.surfaces['head_down']
        elif head_relation == pygame.Vector2(0,1): self.head_surface = self.surfaces['head_up']

    def update_tail(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == pygame.Vector2(1,0): self.tail_surface = self.surfaces['tail_left']
        elif tail_relation == pygame.Vector2(-1,0): self.tail_surface = self.surfaces['tail_right']
        elif tail_relation == pygame.Vector2(0,1): self.tail_surface = self.surfaces['tail_up']
        elif tail_relation == pygame.Vector2(0,-1): self.tail_surface = self.surfaces['tail_down']

    def update_body(self):
        self.draw_data = []
        for i, part in enumerate(self.body):
            # Position
            x = part.x * CELL_SIZE
            y = part.y * CELL_SIZE
            rect = pygame.Rect(x,y, CELL_SIZE, CELL_SIZE)

            if i == 0:
                self.draw_data.append((self.head_surface, rect))
            elif i == len(self.body)-1:
                self.draw_data.append((self.tail_surface, rect))
            else:
                last_part = self.body[i+1] - part
                next_part = self.body[i-1] - part
                if last_part.x == next_part.x:
                    self.draw_data.append((self.surfaces['body_horizontal'], rect))
                elif last_part.y == next_part.y:
                    self.draw_data.append((self.surfaces['body_vertical'], rect))
                else:
                    # Corners
                    if last_part.x == -1 and next_part.y == -1 or last_part.y == -1 and next_part.x == -1: 
                        self.draw_data.append((self.surfaces['body_tl'], rect))
                    elif last_part.x == -1 and next_part.y == 1 or last_part.y == 1 and next_part.x == -1: 
                        self.draw_data.append((self.surfaces['body_bl'], rect))
                    elif last_part.x == 1 and next_part.y == -1 or last_part.y == -1 and next_part.x == 1: 
                        self.draw_data.append((self.surfaces['body_tr'], rect))
                    elif last_part.x == 1 and next_part.y == 1 or last_part.y == 1 and next_part.x == 1: 
                        self.draw_data.append((self.surfaces['body_br'], rect))

    def draw(self):
        for surface, rect in self.draw_data:
            self.window.blit(surface, rect)
