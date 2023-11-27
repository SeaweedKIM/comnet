import pygame

win_width = 500
win_height = 500

class Player:
    def initialize(self, image_path, start_x, start_y):
        self.image = pygame.image.load(image_path)
        self.size = self.image.get_rect().size
        self.width = self.size[0]
        self.height = self.size[1]
        self.x_pos = start_x
        self.y_pos = start_y
        self.to_x = 0
        self.to_y = 0

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.to_x = -5
        elif keys[pygame.K_RIGHT]:
            self.to_x = 5
        else:
            self.to_x = 0

        if keys[pygame.K_UP]:
            self.to_y = -5
        elif keys[pygame.K_DOWN]:
            self.to_y = 5
        else:
            self.to_y = 0

        self.x_pos += self.to_x
        self.y_pos += self.to_y

        # 이동 가능범위(가로)
        if self.x_pos < 0:
            self.x_pos = 0
        elif self.x_pos > win_width - self.width:
            self.x_pos = win_width - self.width

        # 이동 가능 범위(세로)
        if self.y_pos < 0:
            self.y_pos = 0
        elif self.y_pos > win_height - self.height:
            self.y_pos = win_height - self.height

    def draw(self, window):
        window.blit(self.image, (self.x_pos, self.y_pos))

    def get_state(self):
        return {
            'x_pos': self.x_pos,
            'y_pos': self.y_pos,
            'to_x': self.to_x,
            'to_y': self.to_y
        }

    def update_state(self, state):
        self.x_pos = state['x_pos']
        self.y_pos = state['y_pos']
        self.to_x = state['to_x']
        self.to_y = state['to_y']