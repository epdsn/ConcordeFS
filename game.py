import pygame
import sys
import utils # automatically initializes logging
import logging
from settings import *
from graphics import Graphics

# Set up logging
logging = logging.getLogger(__name__)
logging.info("Game started.")

# Initialize Pygame
pygame.init()

# Set up game loop
clock = pygame.time.Clock()

# Initialize the Graphics class
graphics = Graphics()

# Set up buttons
start_button_text = graphics.button_font.render('START', True, graphics.BUTTON_TEXT_COLOR)
start_button_rect = start_button_text.get_rect(center=(screen_width // 2, screen_height // 2 + 225))

# Define obstacle class
class Obstacle:
    def __init__(self, x, y):
        self.image = graphics.mountain_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def move(self, speed):
        self.rect.x -= speed

# Create a list to hold obstacles
obstacles = []
obstacle_frequency = 2000  # Add an obstacle every 100 pixels

# Main game loop
start_screen = True
running = True
rotated_plane = None  # Initialize rotated_plane outside of the game loop
plane_rect = None  # Initialize plane_rect outside of the game loop

try:
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if start_screen:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if start_button_rect.collidepoint(event.pos):
                        start_screen = False  # Start the game when the start button is clicked
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    start_screen = False  # Start the game when the return key is pressed           
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    start_screen = True  # Go back to the start screen if Escape is pressed

                # Adjust speeds based on key presses
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        forward_speed = 50  # Set forward speed to 3 for mock speed 1
                    elif event.key == pygame.K_2:
                        forward_speed = 100  # Set forward speed to 5 for mock speed 2
                    elif event.key == pygame.K_3:
                        forward_speed = 200  # Set forward speed to 8 for mock speed 3
                    elif event.key == pygame.K_0:
                        forward_speed = 5  # back to normal speed

        if not start_screen:  # If not in the start screen
            # Handle key events
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                plane_x -= left_speed  # Move the plane left by decreasing its x-coordinate
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                plane_x += right_speed  # Move the plane right by increasing its x-coordinate
            if keys[pygame.K_s] or keys[pygame.K_UP]:
                plane_y -= 5.0  # Move the plane up by decreasing its y-coordinate
                plane_angle = 5  # Adjust the angle of rotation when K_UP is pressed
            if keys[pygame.K_w] or keys[pygame.K_DOWN]:
                plane_y = min(plane_y + 5, screen_height - plane_height - 25)  # Move the plane down by increasing its y-coordinate, but not below the bottom boundary
                plane_angle = -5  # Adjust the angle of rotation when K_DOWN is pressed

            # Keep plane within screen boundaries
            plane_x = max(0, min(plane_x, screen_width - plane_width))
            plane_y = max(0, min(plane_y, screen_height - plane_height))

            # Update the position of the background
            background_x -= forward_speed  # Adjust the scrolling speed here

            # If the background has scrolled off the screen, reset its position
            if background_x <= -graphics.background_image.get_width():
                background_x = 0

            # Add obstacles
            if len(obstacles) == 0 or obstacles[-1].rect.right < screen_width - obstacle_frequency:
                obstacles.append(Obstacle(screen_width, screen_height - graphics.mountain_image.get_height() - (runway_height * 2 + 10)))

            # Move obstacles
            for obstacle in obstacles:
                obstacle.move(forward_speed)

        # Clear the screen
        screen.fill(graphics.WHITE)

        if start_screen:
            # Draw start screen background
            try:
                graphics.draw_start_screen(screen, start_button_rect)
            except Exception as e:
                logging.error("An error occured while loading the start screen")

        else:  # If not in the start screen

            # Rotate the plane image
            rotated_plane = pygame.transform.rotate(graphics.plane_image, plane_angle)
            # Get the bounding rectangle of the rotated plane image
            plane_rect = rotated_plane.get_rect()
            # Set its position
            plane_rect.topleft = (plane_x, plane_y)

            try:
                graphics.draw_game_screen(screen, background_x, runway_x, runway_y, runway_width, runway_height, obstacles, plane_rect, rotated_plane)
            except Exception as e:
                logging.error("An error occurred while loading the game screen: {e}")

            # Mountain Collision detection
            for obstacle in obstacles:
                if plane_rect and plane_rect.colliderect(obstacle.rect):
                    # Collision detected
                    # Implement collision response here
                    # For simplicity, let's reset the plane position
                    plane_x = 100
                    plane_y = screen_height // 2 + 100
                    logging.info("BOOM! The concord flew into a mountain!")

            # Reset the angle when neither UP nor DOWN key is pressed
            if not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
                plane_angle = 0

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

except Exception as e:
    # Log errors to the file
    logging.exception("An error occurred:")

# Quit Pygame
pygame.quit()
sys.exit()
