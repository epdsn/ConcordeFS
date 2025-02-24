# Set up the runway
import pygame

# Set up the screen
screen_width = 1000
screen_height = 850
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Concorde Flight Simulator 8-bit")

runway_width = screen_width
runway_height = 25
runway_x = 0
runway_y = screen_height - 50

# Set up the plane
plane_width = 50
plane_height = 50
plane_x = 100  # Initial x-coordinate of the plane
plane_y = screen_height // 2 + 100  # Initial y-coordinate of the plane

# Angle of rotation for the plane
plane_angle = 0

# Set up the initial position of the background
background_x = 0

# Set up speed values
forward_speed = 5
left_speed = 3
right_speed = 8