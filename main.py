import pygame
import random
import sys
import os
import time
from pygame.locals import *

# parameters that you can change for a change of gameplay ( just let it be, if you dont want to resize entity images)
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
TEXTCOLOR = (255, 255, 255)
BACKGROUNDCOLOR = (0, 0, 0)
FPS = 60
BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 6
BADDIEMAXSPEED = 12
ADDNEWBADDIERATE = 6
PLAYERMOVERATE = 5
MAX_SPEED_TIME_THRESHOLD = 300
count = 3

def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return

def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False

def generate_road(road_width, road_height):
    road_surface = pygame.image.load('road.png')
    road_surface = pygame.transform.scale(road_surface, (road_width, road_height))
    return road_surface

def increase_speed(elapsed_time, BADDIEMINSPEED, BADDIEMAXSPEED):
    max_speed_increase_rate = (BADDIEMAXSPEED - BADDIEMINSPEED) / MAX_SPEED_TIME_THRESHOLD
    current_max_speed = BADDIEMINSPEED + max_speed_increase_rate * elapsed_time
    current_max_speed = min(current_max_speed, BADDIEMAXSPEED)
    return BADDIEMINSPEED, round(current_max_speed)

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# setting up the window (change as u like, dont blame me if it looks ugly then)
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Simple 2D car game(made in an hour)')
pygame.mouse.set_visible(False)

font = pygame.font.SysFont(None, 30)

# sound
gameOverSound = pygame.mixer.Sound('crash.wav')
pygame.mixer.music.load('car.wav')
boo = pygame.mixer.Sound('boo.wav')

# images
playerImage = pygame.image.load('car1.png')
baddieImage = pygame.image.load('car2.png')

# start screen
drawText('Press any key to start, esc to quit', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3))
drawText('And play', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3) + 30)
pygame.display.update()
waitForPlayerToPressKey()

zero = 0 # apparently we have to use variables for readability, so....
if not os.path.exists("highscore.dat"):
    f = open("highscore.dat", 'w')
    f.write(str(zero))
    f.close()
v = open("highscore.dat", 'r')
topScore = int(v.readline())
v.close()

while count > 0:
    # game starting here
    baddies = []
    score = 0
    playerRect = playerImage.get_rect(topleft=(WINDOWWIDTH / 2, WINDOWHEIGHT - 50))
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)

    trial_BADDIEMINSPEED = BADDIEMINSPEED
    trial_BADDIEMAXSPEED = BADDIEMAXSPEED

    road_width = WINDOWWIDTH
    road_height = WINDOWHEIGHT
    road_surface = generate_road(road_width, road_height)
    road_y_pos = 0

    while True:
        score += 1
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == ord('z'):
                    reverseCheat = True
                if event.key == ord('x'):
                    slowCheat = True
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                if event.key == ord('z'):
                    reverseCheat = False
                    score = 0
                if event.key == ord('x'):
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False

        trial_BADDIEMINSPEED, trial_BADDIEMAXSPEED = increase_speed(score, trial_BADDIEMINSPEED, trial_BADDIEMAXSPEED)

        # adding obstacles
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1

        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize = 30

            newBaddie = {'rect': pygame.Rect(random.randint(0, road_width - 1), 0 - baddieSize, 25, 50),
                        'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                        'surface': pygame.transform.scale(random.choice([baddieImage]), (25, 50))}
            baddies.append(newBaddie)

        # player car movement
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)

        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)

        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)

        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)


        for b in baddies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

        for b in baddies[:]:
            if b['rect'].top > WINDOWHEIGHT:
                baddies.remove(b)

        windowSurface.fill(BACKGROUNDCOLOR)

        windowSurface.blit(road_surface, (0, road_y_pos))

        drawText('Score: %s' % (score), font, windowSurface, 128, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 128, 20)
        drawText('Rest Life: %s' % (count), font, windowSurface, 128, 40)

        windowSurface.blit(playerImage, playerRect)
        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])

        pygame.display.update()

        BADDIEMINSPEED, BADDIEMAXSPEED = increase_speed(score, BADDIEMINSPEED, BADDIEMAXSPEED)

        # check is crash (booom)
        if playerHasHitBaddie(playerRect, baddies):
            if score > topScore:
                g = open("highscore.dat", 'w')
                g.write(str(score))
                g.close()
                topScore = score
            break
        mainClock.tick(FPS)

    # YOU LOSE SCREEN 
    pygame.mixer.music.stop()
    count -= 1
    gameOverSound.play()
    time.sleep(1)
    if count == 0:
        boo.play()
        drawText('YOU LOSE!', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
        drawText('Press any key to play again or esc to quit', font, windowSurface, (WINDOWWIDTH / 3) - 80,
                 (WINDOWHEIGHT / 3) + 30)
        pygame.display.update()
        time.sleep(2)
        waitForPlayerToPressKey()
        count = 3
        gameOverSound.stop()
