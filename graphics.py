# graphics.py

import pygame
from settings import screen_width, screen_height  

class Graphics:
    def __init__(self):
        # Load images and other graphics resources here
        self.background_image = pygame.image.load('assets/images/background_pixel_001.jpg')
        self.start_screen_background = pygame.image.load('assets/images/start_screen_image.png')
        self.plane_image = pygame.image.load('assets/images/plane_pixel.png')
        self.mountain_image = pygame.image.load('assets/images/mountain.png')

        # Set up colors
        self.WHITE = (255, 255, 255)
        self.DARK_GREY = (50, 50, 50)
        self.BUTTON_COLOR = (0, 150, 0)
        self.BUTTON_TEXT_COLOR = (255, 255, 255)

        # Set up fonts
        self.button_font = pygame.font.Font(None, 36)

        # Set up buttons
        self.start_button_text = self.button_font.render('START', True, self.BUTTON_TEXT_COLOR)
        self.start_button_rect = self.start_button_text.get_rect(center=(screen_width // 2, screen_height // 2 + 225))

    def draw_start_screen(self, screen, start_button_rect):
        # Draw start screen background
        screen.blit(self.start_screen_background, (0, 0))

        # Draw start button
        pygame.draw.rect(screen, self.BUTTON_COLOR, start_button_rect)
        pygame.draw.rect(screen, self.DARK_GREY, start_button_rect, 2)  # Border
        start_button_text = self.button_font.render('START', True, self.BUTTON_TEXT_COLOR)
        screen.blit(start_button_text, start_button_rect)

    def draw_game_screen(self, screen, background_x, runway_x, runway_y, runway_width, runway_height, obstacles, plane_rect, rotated_plane):
        # Draw background
        screen.blit(self.background_image, (background_x, 0))
        screen.blit(self.background_image, (background_x + self.background_image.get_width(), 0))

        # Draw runway
        pygame.draw.rect(screen, self.DARK_GREY, (runway_x, runway_y, runway_width, runway_height))

        # Draw obstacles
        for obstacle in obstacles:
            screen.blit(self.mountain_image, obstacle.rect)

        # Draw plane
        screen.blit(rotated_plane, plane_rect)

    def draw_collision_message(self, screen):
        # Draw collision message or effects
        pass
