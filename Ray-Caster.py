import pygame
import math

# initialization
pygame.init()

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SKY_BLUE = (135, 206, 235)
YELLOW = (255, 255, 0)


# Constant
WINDOW_HEIGHT = 480
WINDOW_WIDTH = WINDOW_HEIGHT * 2
HORIZON = WINDOW_HEIGHT / 2
MAP_SIZE = 8
TILE_SIZE = int((WINDOW_WIDTH / 2) / MAP_SIZE)
MAX_DEPTH = int(MAP_SIZE * TILE_SIZE)
FOV = math.pi / 3
HALF_FOV = FOV / 2
CASTED_RAYS = 120
CASTED_RAY_LENGTH = 60
SCALE = ((WINDOW_WIDTH / 2) / CASTED_RAY_LENGTH)
CASTED_STEP_ANGLE = (FOV) / CASTED_RAYS

# Timer
clock = pygame.time.Clock()

# Player
player_x = (WINDOW_WIDTH / 2) / 2
player_y = WINDOW_HEIGHT / 2
player_angle = math.pi
move_forward = True
move_backward = True
 
MAP = [ [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 0, 1, 1, 1, 1],
        [1, 0, 1, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1] 
      ]

# Window
font = pygame.font.SysFont("Arial", 18)
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
gamedisplay = pygame.display.set_caption("Ray Caster")


# Draw map 
def draw_map():
    for x in range(MAP_SIZE):
        for y in range(MAP_SIZE):
            if(MAP[x][y] == 1):
                pygame.draw.rect(window, BLACK, (y * TILE_SIZE, x * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2))
    
    pygame.draw.circle(window, BLUE, (player_x, player_y), 8)

    pygame.draw.aaline(window, RED, (int(player_x) , int(player_y)), 
                    (player_x - math.sin(player_angle) * 30,
                     player_y + math.cos(player_angle) * 30), 3)

    # draw player FOV
    pygame.draw.line(window, (0, 255, 0), (player_x, player_y),
                                       (player_x - math.sin(player_angle - HALF_FOV) * 30,
                                        player_y + math.cos(player_angle - HALF_FOV) * 30), 3)
    
    pygame.draw.line(window, (0, 255, 0), (player_x, player_y),
                                       (player_x - math.sin(player_angle + HALF_FOV) * 30,
                                        player_y + math.cos(player_angle + HALF_FOV) * 30), 3)

def player_movement():
    pass


def update_fps():
	fps = str(int(clock.get_fps()))
	fps_text = font.render(fps, 1, pygame.Color("coral"))
	return fps_text

def ray_casting():
    start_angle = player_angle - HALF_FOV
    for ray in range(CASTED_RAYS):
        for depth in range(MAX_DEPTH):
            target_x = player_x - math.sin(start_angle) * depth
            target_y = player_y + math.cos(start_angle) * depth
            
            col = int(target_x / TILE_SIZE)
            row = int(target_y / TILE_SIZE)
            
            depth *= math.cos(player_angle - start_angle)

            color = 255 / (1 + depth * depth * 0.00002)
            COLOR = (0, 0, color)

            if MAP[row][col] == 1:
                pygame.draw.line(window, YELLOW, (player_x, player_y), (target_x, target_y))
                wall_height = 12000 / (depth + 0.0001)
                pygame.draw.rect(window, COLOR, 
                            (480 + ray * SCALE, 240 - wall_height / 2,
                             SCALE, wall_height))
                break
                
        # increment angle by a single step
        start_angle += CASTED_STEP_ANGLE

def detect_collision():
    global player_x
    global player_y
    col = int(player_x / TILE_SIZE)
    row = int(player_y / TILE_SIZE)
    if MAP[row][col] == 1:
        if move_forward:
            player_x -= -math.sin(player_angle)
            player_y -= math.cos(player_angle)
        else:
            player_x += -math.sin(player_angle)
            player_y += math.cos(player_angle)

state = True
while state:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state = False

    window.fill(GREY, (0, 0, WINDOW_WIDTH / 2, WINDOW_HEIGHT))
    window.fill(SKY_BLUE, (WINDOW_WIDTH / 2, 0, WINDOW_WIDTH, WINDOW_HEIGHT / 2))
    window.fill(GREY, (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, WINDOW_WIDTH, WINDOW_HEIGHT))
    
    detect_collision()
    #Draw map
    draw_map()

    # Ray Casting
    ray_casting()

    # FPS Counter
    window.blit(update_fps(), (10, 0))

    # Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] : player_angle -= 0.0500
    if keys[pygame.K_RIGHT] : player_angle += 0.0500
    if keys[pygame.K_UP]:
        move_forward = True 
        player_x += -math.sin(player_angle)
        player_y += math.cos(player_angle)
    if keys[pygame.K_DOWN] and move_backward:
        move_forward = False
        player_x -= -math.sin(player_angle) 
        player_y -= math.cos(player_angle)
 
    pygame.display.update()

    #set fPS
    clock.tick(60)

# pygame Quit
pygame.quit()
quit()