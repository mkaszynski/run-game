import pygame
import time
import random
import pickle
import os
import numpy as np
import math

name = input("name: ")

pygame.init()
pygame.mixer.init()


# Set up the drawing window
# screen = pygame.display.set_mode([1800, 900])
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

font = pygame.font.Font("freesansbold.ttf", 32)


def add_line(screen, text, x, y):
    # used to print the status of the variables
    text = font.render(text, True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text, text_rect)


try:
    high_scores = pickle.load(open("save.run", "rb"))
except:
    high_scores = []


def pix(size):
    return int(size / 1) * 1


explosion = pygame.mixer.Sound("/home/michael/coding/python/games/explosion.mp3")
music = pygame.mixer.Sound("/home/michael/coding/python/games/music.mp3")

posy = 100

length = 0

color = [0, 0, 200]

speed = 10

max_platform = 1400

vely = 0

explosions = []

height = 300

ground = 500

range1 = [0, 0]

jumps = [[0, 300, 1200, [0, 0, 200]]]

power = 0

back = []

operations = False

time1 = 0

# Run until the user asks to quit
running = True
while running:
    # Fill the background with white
    screen.fill((0, 0, 0))
    pygame.event.poll()
    keys = pygame.key.get_pressed()

    time1 += 1

    pygame.mixer.Sound.play(music)

    if keys[pygame.K_SPACE] and power > 20:
        if posy == ground:
            vely = -15
        vely -= 0.5
        power -= 4
        # pygame.mixer.Sound.pause(music)
    else:
        power = 200 - (200 - power) * 0.975

    if keys[pygame.K_SPACE] and power < 20:
        power = 0

    if power > 200:
        power = 200

    posy += vely

    for i in jumps:
        if i[0] + length < 300 and i[0] + i[2] + length > 300:
            ground = i[1]

    if keys[pygame.K_m] and keys[pygame.K_i] and keys[pygame.K_c]:
        operations = True

    for i in explosions:
        i[3] += 1
        i[0] += i[2]
        i[1] += i[3]
        if i[1] > 9000:
            running = False

    vely += 1

    range1[0] += random.random() * 10 - 5
    range1[1] += random.random() * 10 - 5

    if range1[1] <= 0:
        range1[1] = random.random() * 10
    if range1[0] >= 0:
        range1[0] = random.random() * -10

    if range1[0] > range1[1]:
        range1[0] = range1[1]

    if range1[1] > 150:
        range1[1] = 150
    if range1[0] < -150:
        range1[0] = -150

    color[0] += random.random() * 16 - 8
    if color[0] > 255:
        color[0] = 255
    if color[0] < 0:
        color[0] = 0
    color[1] += random.random() * 16 - 8
    if color[1] > 255:
        color[1] = 255
    if color[1] < 0:
        color[1] = 0
    color[2] += random.random() * 16 - 8
    if color[2] > 255:
        color[2] = 255
    if color[2] < 0:
        color[2] = 0

    if random.random() > 0.9:
        back.append(
            [
                1800,
                random.random() * 1100 + posy - 900,
                (random.random() * 13 + 2) ** (2),
                (color[0], color[1], color[2]),
            ]
        )

    for i in back:
        i[0] -= i[2] / 20
        if i[0] < -500:
            back.remove(i)

        i[1] = (
            (i[1] - posy / 300 * i[2] + 300 + 300 + 300) % 1200
            - 600
            + posy / 300 * i[2]
            - 300
        )

    if vely > 25:
        vely = 25
    if posy > ground:
        if posy < ground + 30:
            posy = ground
        else:
            pygame.mixer.Sound.stop(music)
            if len(explosions) < 10:
                for i in range(200):
                    pygame.mixer.Sound.play(explosion)
                    angle = random.random() * 100
                    explosions.append(
                        [
                            600,
                            600,
                            math.sin(angle) * 40 * random.random(),
                            math.cos(angle) * 40 * random.random() - 20,
                        ]
                    )

    if len(explosions) == 0:
        length -= speed

    speed += 0.005

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for i in jumps:
        if i[0] + length < -2000:
            jumps.remove(i)

    max_platform *= 0.9999

    if max_platform < 50:
        max_platform = 50

    n = False

    for i in jumps:
        if i[0] + i[2] + length > 1800:
            n = True

    if not n:
        height -= random.randint(int(range1[0]), int(range1[1]))
        jumps.append(
            [
                1800 - length - speed,
                height,
                random.randint(0, int(max_platform)),
                (color[0], color[1], color[2]),
            ]
        )

    for i in back:
        map1 = pygame.Rect(
            pix(i[0]) + 300,
            pix(i[1] - posy / 300 * i[2] + 300) + 300,
            pix(i[2]),
            pix(i[2]),
        )
        pygame.draw.rect(screen, i[3], map1)

    for i in jumps:
        map1 = pygame.Rect(
            pix(i[0] + length) + 300,
            pix(i[1] + 10 - posy + 300) + 300,
            pix(i[2]),
            pix(10000),
        )
        pygame.draw.rect(screen, i[3], map1)

    for i in explosions:
        map1 = pygame.Rect(i[0], i[1], pix(5), pix(5))
        pygame.draw.rect(
            screen,
            (random.random() * 255, random.random() * 255, random.random() * 255),
            map1,
        )

    if len(explosions) == 0:
        # map1 = pygame.Rect(
        #     pix(300) + 300 - 10, pix(posy - posy + 300) + 300 - 10, 20, 20
        # )
        # pygame.draw.rect(screen, (200, 0, 0), map1)
        this_dir = os.path.dirname(__file__)
        image_file = os.path.join(this_dir, "person.png")
        image = pygame.image.load(image_file).convert()
        image.set_colorkey((0, 0, 0))
        image = pygame.transform.scale(image, (40, 80))
        rect = image.get_rect()
        rect.center = (600 - 10 - 10, 600 - 10 - 20)
        # screen.blit(image, rect)

        speedn = 1.5

        type1 = "person.png"
        if int(10 / speedn) < time1 % int(30 / speedn) <= int(20 / speedn):
            type1 = "person2.png"
        elif int(20 / speedn) < time1 % int(30 / speedn) <= int(30 / speedn):
            type1 = "person3.png"

        if posy < ground - 20:
            if vely < 0:
                type1 = "person_jump.png"
            else:
                type1 = "person_jump2.png"

        this_dir = os.path.dirname(__file__)
        image_file = os.path.join(this_dir, type1)
        image = pygame.image.load(image_file).convert_alpha()
        image = pygame.transform.scale(image, (40, 80))

        arr = pygame.surfarray.pixels3d(image)
        alpha = pygame.surfarray.pixels_alpha(image)

        mask = np.all(arr == (0, 0, 0), axis=-1)
        alpha[mask] = 0

        del arr
        del alpha

        rect = image.get_rect()
        rect.center = (600 - 10 - 10, 600 - 10 - 20)
        screen.blit(image, rect)

    add_line(screen, f"points: {int(length * -0.1)}", 0, 0)
    add_line(screen, f"speed {int(speed * 0.3 - 2)}", 0, 45)

    map1 = pygame.Rect(0, 80, power, 20)
    pygame.draw.rect(screen, (200 - power, 0, power), map1)

    time.sleep(1 / 60)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()

print(f"points: {int(length * -0.1)}")

has_scores = False
for i in high_scores:
    if i[0] == name:
        has_scores = True
        if int(length * -0.1) > i[1]:
            i[1] = int(length * -0.1)

if not has_scores:
    high_scores.append([name, int(length * -0.1)])

# get sorted score indices
indices = np.argsort([score for name, score in high_scores])[::-1]

print()
print("########## High Scores ##########")
for index in indices:
    name, score = high_scores[index]
    print(f"{name:15s}   {score:15d}")

if operations:
    while True:
        np = input("Operations? ")
        if np:
            if np == "c":
                lk = input("Change which high score? ")
                for i in high_scores:
                    if i[0] == lk:
                        i[1] = int(input("New number? "))
            elif np == "n":
                lk = input("New high score name? ")
                high_scores.append([lk, input("Number? ")])
            elif np == "d":
                lk = input("Delete which high score? ")
                for i in high_scores:
                    if i[0] == lk:
                        if input("Are you sure (y/n)") == "y":
                            high_scores.remove(i)
            elif np == "s":
                for i in high_scores:
                    print(f"high score for {i[0]}: {i[1]}")
            elif np == "h":
                print("""
                c: change high scores
                n: add new high scores
                d: delete high scores
                s: display high scores
                h: display help
                """)
        else:
            print("Saving changes")
            break


pickle.dump(high_scores, open("save.run", "wb"))
