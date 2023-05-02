import pygame
import math

# Define constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FOV = math.pi / 3  # 60 degrees
NUM_RAYS = 120
WALL_HEIGHT = 32

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Define map data
MAP_WIDTH = 10
MAP_HEIGHT = 10
MAP_DATA = [
    "##########",
    "#        #",
    "#  ##    #",
    "#  ##    #",
    "#         ",
    "#  ##    #",
    "#  ##    #",
    "#        #",
    "#        #",
    "##########",
]

# Initialize Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create the font
font = pygame.font.SysFont(None, 20)

# Create the player
player_x = 2.5
player_y = 2.5
player_angle = 0

# Define the raycasting function
def cast_rays():
    # Loop over each ray
    for i in range(NUM_RAYS):
        # Calculate the angle of the current ray
        angle = player_angle - FOV / 2 + (i / NUM_RAYS) * FOV

        # Initialize the ray distance to infinity
        ray_distance = float("inf")

        # Loop over each vertical slice of the screen
        for j in range(SCREEN_WIDTH):
            # Calculate the angle of the current slice
            slice_angle = player_angle - FOV / 2 + (j / SCREEN_WIDTH) * FOV

            # Calculate the distance to the wall at the current slice
            distance = 0
            hit_wall = False
            hit_boundary = False
            while not hit_wall and distance < 10:
                x = player_x + distance * math.cos(slice_angle)
                y = player_y + distance * math.sin(slice_angle)

                # Check if the current point is inside a wall
                if x < 0 or x >= MAP_WIDTH or y < 0 or y >= MAP_HEIGHT or MAP_DATA[int(y)][int(x)] == "#":
                    hit_wall = True

                    # Calculate the distance to the wall
                    wall_distance = distance * math.cos(angle - slice_angle)

                    # Calculate the height of the wall
                    wall_height = WALL_HEIGHT / wall_distance * SCREEN_HEIGHT

                    # Calculate the top and bottom of the wall on the screen
                    wall_top = SCREEN_HEIGHT / 2 - wall_height / 2
                    wall_bottom = SCREEN_HEIGHT / 2 + wall_height / 2

                    # Draw the wall slice on the screen
                    pygame.draw.line(screen, WHITE, (j, wall_top), (j, wall_bottom))

                    # Update the ray distance if necessary
                    if wall_distance < ray_distance:
                        ray_distance = wall_distance

                    # Check if the current point is on a wall boundary
                    if x % 1 == 0 and y % 1 == 0:
                        hit_boundary = True
                else:
                    # Draw the floor and ceiling slices on the screen
                    pygame.draw.line(screen, BLACK, WHITE, RED, GREEN, BLUE)
