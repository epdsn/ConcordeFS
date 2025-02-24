# Define obstacle class
from graphics import Graphics

graphics = Graphics()

class Obstacle:
    def __init__(self, x, y):
        self.image = graphics.mountain_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def move(self, speed):
        self.rect.x -= speed