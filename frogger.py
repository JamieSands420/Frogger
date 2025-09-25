import pygame
import random

pygame.init()

font = pygame.font.SysFont(None, 48)
score = 0
realScore = 0

scr = pygame.display.set_mode((1120, 700))
clock = pygame.time.Clock()

# Load sprites
frog_sprite = pygame.image.load(f"{__file__[:-10]}/Resources/frog.png")
frog_sprite = pygame.transform.scale(frog_sprite, (46, 58))

raft_sprite = pygame.image.load(f"{__file__[:-10]}/Resources/log.png")
raft_sprite = pygame.transform.scale(raft_sprite, (46, 58))

car_sprite = pygame.image.load(f"{__file__[:-10]}/Resources/Car.png")
car_sprite = pygame.transform.scale(car_sprite, (46, 58))

grass_sprite = pygame.image.load(f"{__file__[:-10]}/Resources/grass..png")
grass_sprite = pygame.transform.scale(grass_sprite, (46, 58))

play_button = pygame.image.load(f"{__file__[:-10]}/Resources/play.png")
forfeit_button = pygame.image.load(f"{__file__[:-10]}/Resources/forfeit.png")

button = pygame.Rect((920, 50), (200, 100))

flip_car_sprite = pygame.transform.flip(car_sprite, False, True)

# Animated water sprites
water_sprites = [
    pygame.transform.scale(pygame.image.load(f"{__file__[:-10]}/Resources/water1.gif"), (46, 58)),
    pygame.transform.scale(pygame.image.load(f"{__file__[:-10]}/Resources/water2.gif"), (46, 58)),
    pygame.transform.scale(pygame.image.load(f"{__file__[:-10]}/Resources/water3.gif"), (46, 58)),
    pygame.transform.scale(pygame.image.load(f"{__file__[:-10]}/Resources/water4.png"), (46, 58))
]
water_frame = 0

# Game objects
player = pygame.Rect((0, 300), (46, 58))
levelobj = pygame.Rect((0, 0), (46, 58))
logs = []
cars = []
direction = "down"
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

        if rng == 1:  # grass
            level.append("g")
            filled_tiles += 1
        elif rng == 2:  # highway
            length = random.randint(1, 4)
            length = min(length, 18 - filled_tiles)
            level.extend(["h"] * length)
            filled_tiles += length
        elif rng == 3:  # river
            length = random.randint(1, 4)
            length = min(length, 18 - filled_tiles)
            level.extend(["r"] * length)
            filled_tiles += length

    level.append("g")


def populate_level():
    logs.clear()
    cars.clear()
    global direction

    for i in range(len(level)):
        if level[i] == "h":
            if direction == "down":
                cars.append(pygame.Rect((46 * i, 0 - random.randint(1, 500)), (46, 58)))
            else:
                cars.append(pygame.Rect((46 * i, 642 + random.randint(1, 500)), (46, 58)))

        if level[i] == "r":
            if direction == "down":
                logs.append(pygame.Rect((46 * i, 0 - random.randint(1, 500)), (46, 58)))
            else:
                logs.append(pygame.Rect((46 * i, 642 + random.randint(1, 500)), (46, 58)))

        direction = "up" if direction == "down" else "down"

    if len(logs) % 2 != 0:
        logs.append(pygame.Rect((-1000, 0), (0, 0)))

    if len(cars) % 2 != 0:
        cars.append(pygame.Rect((-1000, 0), (0, 0)))


def draw_level():
    global water_frame
    levelobj.x = 0
    levelobj.y = 0

    current_water_sprite = water_sprites[int(water_frame) % len(water_sprites)]

    for i in range(len(level)):
        for j in range(12):  # 12 tiles tall
            if level[i] == "g":
                scr.blit(grass_sprite, levelobj)
            elif level[i] == "h":
                pygame.draw.rect(scr, (60, 60, 60), levelobj)
            elif level[i] == "r":
                scr.blit(current_water_sprite, levelobj)

                for log in logs:
                    if log.colliderect(player):
                        player.y = log.y
                    if levelobj.colliderect(player):
                        if player.colliderect(log):
                            break

            levelobj.y += 58

        levelobj.y = 0
        levelobj.x += 46


def game_over():
    global run
    run = False


generate_level()
populate_level()

run = True
while True:
    while run:
        scr.fill((255, 255, 255))
        scr.blit(forfeit_button, button)

        scoreText = font.render(f"score: {realScore}", True, (0, 0, 0))

        draw_level()

        for log in logs:
            scr.blit(raft_sprite, log)
            if direction == "down":
                log.y += 1.5
                direction = "up"
            else:
                log.y -= 1.5
                direction = "down"

            if log.y > 750:
                log.y = 0 - random.randint(1, 200)
            elif log.y < -50:
                log.y = 700 + random.randint(1, 200)

            if log.x == player.x and not player.colliderect(log):
                game_over()

        direction = "down"

        for car in cars:
            scr.blit(car_sprite, car)
            if direction == "down":
                scr.blit(flip_car_sprite, car)
                car.y += 1.5
                direction = "up"
            else:
                scr.blit(car_sprite, car)
                car.y -= 1.5
                direction = "down"

            if car.y > 750:
                car.y = 0 - random.randint(1, 50)
            elif car.y < -50:
                car.y = 700 + random.randint(1, 50)

            if car.colliderect(player):
                game_over()

        scr.blit(frog_sprite, player)
        scr.blit(scoreText, (925, 15))
        
        pygame.display.flip()
        if realScore < score:
            realScore = score

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.x += 46
                    score+=1
                elif event.key == pygame.K_UP:
                    player.y -= 58
                elif event.key == pygame.K_LEFT:
                    player.x -= 46
                    score-=1
                elif event.key == pygame.K_RIGHT:
                    player.x += 46
                    score+=1
                elif event.key == pygame.K_DOWN:
                    player.y += 58

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(event.pos):
                    run = False

        if player.x == 874:
            player.x = 0
            generate_level()
            populate_level()

        water_frame += 0.05 
        clock.tick(60)

    for event in pygame.event.get():   
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button.collidepoint(event.pos):
                # restart it
                player.x = 0
                generate_level()
                populate_level()
                realScore = 0
                score = 0
                run = True
                player.y = 350
        
    scr.blit(play_button, button)

    pygame.display.flip()

pygame.quit()
