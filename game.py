import pygame
import sys
from game.obstacle import Obstacle
import utils
import logging
from settings import *
from graphics import Graphics

class Game:
    def __init__(self):
        # Set up logging
        self.logger = logging.getLogger(__name__)
        self.logger.info("Game started.")

        # Initialize Pygame and game state
        pygame.init()
        self.clock = pygame.time.Clock()
        self.graphics = Graphics()
        
        # Game state
        self.running = True
        self.start_screen = True
        
        # Plane properties
        self.plane_x = 100
        self.plane_y = screen_height // 2 + 100
        self.plane_angle = 0
        self.plane_rect = None
        self.rotated_plane = None
        
        # Obstacles
        self.mountains = []
        self.mountains_frequency = 2000
        
        # Background
        self.background_x = 0
        self.forward_speed = 5  # default speed

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.start_screen:
                self.handle_start_screen_events(event)
            else:
                self.handle_game_events(event)

    def handle_start_screen_events(self, event):
        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and 
            self.graphics.start_button_rect.collidepoint(event.pos)):
            self.start_screen = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.start_screen = False

    def handle_game_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.start_screen = True
            elif event.key == pygame.K_1:
                self.forward_speed = 50
            elif event.key == pygame.K_2:
                self.forward_speed = 100
            elif event.key == pygame.K_3:
                self.forward_speed = 200
            elif event.key == pygame.K_0:
                self.forward_speed = 5

    def update_game_state(self):
        if not self.start_screen:
            self.handle_player_movement()
            self.update_background()
            self.update_obstacles()

    def handle_player_movement(self):
        keys = pygame.key.get_pressed()
        
        # Handle horizontal movement
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.plane_x -= left_speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.plane_x += right_speed
            
        # Handle vertical movement
        if keys[pygame.K_s] or keys[pygame.K_UP]:
            self.plane_y -= 5.0
            self.plane_angle = 5
        if keys[pygame.K_w] or keys[pygame.K_DOWN]:
            self.plane_y = min(self.plane_y + 5, screen_height - plane_height - 25)
            self.plane_angle = -5
            
        # Reset angle when no vertical movement
        if not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            self.plane_angle = 0
            
        # Keep plane within boundaries
        self.plane_x = max(0, min(self.plane_x, screen_width - plane_width))
        self.plane_y = max(0, min(self.plane_y, screen_height - plane_height))

    def update_background(self):
        self.background_x -= self.forward_speed
        if self.background_x <= -self.graphics.background_image.get_width():
            self.background_x = 0

    def update_obstacles(self):
        if len(self.mountains) == 0 or self.mountains[-1].rect.right < screen_width - self.mountains_frequency:
            self.mountains.append(Obstacle(screen_width, 
                screen_height - self.graphics.mountain_image.get_height() - (runway_height * 2 + 10)))
        
        for obstacle in self.mountains:
            obstacle.move(self.forward_speed)

    def check_collisions(self):
        for obstacle in self.mountains:
            if self.plane_rect and self.plane_rect.colliderect(obstacle.rect):
                self.handle_collision()

    def handle_collision(self):
        self.plane_x = 100
        self.plane_y = screen_height // 2 + 100
        self.logger.info("BOOM! The concord flew into a mountain!")

    def render(self):
        screen.fill(self.graphics.WHITE)
        
        if self.start_screen:
            try:
                self.graphics.draw_start_screen(screen, self.graphics.start_button_rect)
            except Exception as e:
                self.logger.error("An error occurred while loading the start screen")
        else:
            self.render_game()

        pygame.display.flip()

    def render_game(self):
        try:
            # Update plane graphics
            self.rotated_plane = pygame.transform.rotate(self.graphics.plane_image, self.plane_angle)
            self.plane_rect = self.rotated_plane.get_rect()
            self.plane_rect.topleft = (self.plane_x, self.plane_y)
            
            # Draw game elements
            self.graphics.draw_game_screen(
                screen, self.background_x, runway_x, runway_y,
                runway_width, runway_height, self.mountains,
                self.plane_rect, self.rotated_plane
            )
        except Exception as e:
            self.logger.error(f"An error occurred while loading the game screen: {e}")

    def run(self):
        try:
            while self.running:
                self.handle_events()
                self.update_game_state()
                self.check_collisions()
                self.render()
                self.clock.tick(60)
        except Exception as e:
            self.logger.exception("An error occurred:")
        finally:
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
