import pygame
import random

scr = pygame.display.set_mode((900, 700))
clock = pygame.time.Clock()

# scale image 2x + 10

"""
added log texture
make it longer
"""

frog_sprite = pygame.image.load(f"{__file__[:-10]}/Resources/frog.png")
frog_sprite = pygame.transform.scale(frog_sprite, (46, 58))

raft_sprite = pygame.image.load(f"{__file__[:-10]}/Resources/log.png")
raft_sprite = pygame.transform.scale(raft_sprite, (46, 58))

player = pygame.Rect((0, 300), (46, 58))
levelobj = pygame.Rect((0, 0), (46, 58))
logs = []

level = ["g"]
def generate_level():
    level.clear()
    level.append("g")

    previous_rng = None
    filled_tiles = 0

    while filled_tiles < 18:
        rng = random.randint(1, 3)

        while rng == previous_rng:
            rng = random.randint(1, 3)

        previous_rng = rng

        if rng == 1:
            # grass
            level.append("g")
            filled_tiles += 1

        elif rng == 2:
            # highway
            length = random.randint(1, 4)
            length = min(length, 18 - filled_tiles)
            level.extend(["h"] * length)
            filled_tiles += length

        elif rng == 3:
            # river
            length = random.randint(1, 4)
            length = min(length, 18 - filled_tiles)
            level.extend(["r"] * length)
            filled_tiles += length

    # Add final grass
    level.append("g")

logs = []
cars = []
direction = "down"
def populate_level():
    logs.clear()
    cars.clear()
    global direction

    for i in range(len(level)):

        if level[i] == "h":
            if direction == "down":
                cars.append(pygame.Rect((46*i, 0 - random.randint(1, 50)), (46, 58)))
            else:
                cars.append(pygame.Rect((46*i, 642 + random.randint(1, 50)), (46, 58)))

        if level[i] == "r":
            if direction == "down":
                logs.append(pygame.Rect((46*i, 0 - random.randint(1, 50)), (46, 58)))
            else:
                logs.append(pygame.Rect((46*i, 642 + random.randint(1, 50)), (46, 58)))

        if direction == "down":
            direction = "up"

        else:
            direction = "down"

    if len(logs) % 2 != 0:
        logs.append(pygame.Rect((-1000, 0), (0, 0)))

    if len(cars) % 2 != 0:
        cars.append(pygame.Rect((-1000, 0), (0, 0)))

def draw_level():
    for i in range(len(level)):
        
        if level[i] == "g":
            for i in range(12):
                pygame.draw.rect(scr, (0, 66, 0), levelobj)
                levelobj.y += 58

        elif level[i] == "h":
            for i in range(12):
                pygame.draw.rect(scr, (0, 0, 0), levelobj)
                levelobj.y += 58

        elif level[i] == "r":
            for i in range(12):
                pygame.draw.rect(scr, (0, 0, 66), levelobj)
                levelobj.y += 58

                for log in logs:
                    if log.colliderect(player):
                       player.y = log.y
                    if levelobj.colliderect(player):
                        if player.colliderect(log):
                            break
                        #game_over()

        levelobj.y = 0
        levelobj.x += 46

    levelobj.x = 0

def game_over():
    global run
    run = False

generate_level()
populate_level()

pygame.init()
run = True
while run:

    scr.fill((255, 255, 255))

    draw_level()
    
    for log in logs:

       #move log
       scr.blit(raft_sprite, log)
       if direction == "down":
           log.y += 1.5
           direction = "up"
       else:
           log.y -= 1.5
           direction = "down"

       #move log if reaches end
       if log.y > 750:
           log.y = 0 - random.randint(1, 50)
       elif log.y < -50:
               log.y = 700 + random.randint(1, 50)

       if log.x == player.x and not player.colliderect(log):
           game_over()
           
    direction = "down"
    
    for car in cars:
        pygame.draw.rect(scr, (200, 0, 0), car)
        if direction == "down":
           car.y += 1.5
           direction = "up"
        else:
           car.y -= 1.5
           direction = "down"
        if car.y > 750:
           car.y = 0 - random.randint(1, 50)
        elif car.y < -50:
               car.y = 700 + random.randint(1, 50)

        if car.colliderect(player):
            game_over()
        
    scr.blit(frog_sprite, player)

    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:

            # player movement
            if event.key == pygame.K_SPACE:
                player.x += 46
            elif event.key == pygame.K_UP:
                player.y -= 58
            elif event.key == pygame.K_LEFT:
                player.x -= 46
            elif event.key == pygame.K_RIGHT:
                player.x += 46
            elif event.key == pygame.K_DOWN:
                player.y += 58
                
        if event.type == pygame.QUIT:
            run = False

    if player.x == 874:
        player.x = 0
        generate_level()
        populate_level()

    clock.tick(60)
pygame.quit()
