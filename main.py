import pygame
from pygame.locals import *
import numpy as np

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

snakeSize = 20
snakeTail = 10
snakePos = np.random.choice(np.arange(0, 600, snakeSize) ,size=(2))
snakePos = np.vstack([snakePos])

eat = False
foodPos = np.random.choice(np.arange(0, 600, snakeSize) ,size=(2))

movePos = [0, 0]

pressed = True

def getColor(BG_Color : str) -> tuple[int, int ,int]:
        colors = {"black" : (0, 0, 0), "white" : (255,255,255),
                 "blue" : (0, 0, 255), "red" : (255, 0, 0),
                 "green" : (0, 255, 0), "sky blue" : (135, 206, 235),
                 "blue violet" : (138, 43, 226), "royal blue" : (65, 105, 225)}
        
        for color, rgbCode in colors.items():
            checkColor = [col in color for col in BG_Color]
            if (False in checkColor):
                continue
            elif not (False in checkColor):
                return rgbCode
            
        print("Write the right Color!!!")
        return (0, 0 ,0)

def outOfBorder(snake) -> object:
    snakeX = snake[0]
    snakeY = snake[1]
    
    if (snakeX < 0):
        snakeX = 600 - 20
    elif (snakeX > 580):
        snakeX = 0
    if (snakeY < 0):
        snakeY = 580
    elif (snakeY > 580):
        snakeY = 0
        
    return np.array([snakeX,snakeY])

pygame.init()
surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
surface.fill(getColor("blvi"))
fps = 5

running = True
clock = pygame.time.Clock()

while running:
    surface.fill(getColor("blvi"))
    keys = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if (event.type == QUIT or keys[K_q]):
            running = False 
        if (event.type == KEYDOWN):
            if event.key == K_a and not movePos[0]:
                movePos[0] = -snakeSize
                movePos[1] = 0
            elif event.key == K_d and not movePos[0]:
                movePos[0] = snakeSize
                movePos[1] = 0
            elif event.key == K_w and not movePos[1]:
                movePos[1] = -snakeSize
                movePos[0] = 0
            elif event.key == K_s and not movePos[1]:
                movePos[1] = snakeSize
                movePos[0] = 0
            
    
    if movePos[0] and not movePos[1]:
        snakePos[0][0] += movePos[0]
    elif movePos[1] and not movePos[0]:
        snakePos[0][1] += movePos[1]
            
    snakePos[0] = outOfBorder(snakePos[0])
    
    # Snake Eating
    if snakePos[0][0] == foodPos[0] and snakePos[0][1] == foodPos[1] and not eat: 
        snakePos = np.vstack((snakePos, snakePos[0]))
        eat = True
        fps += 0.1
    if eat:
        foodPos = np.random.choice(np.arange(0, 600, snakeSize) ,size=(2))    
    eat = False
    
    for i in range(len(snakePos) - 1, 0, -1):
        if (foodPos[0] == snakePos[i][0] and foodPos[1] == snakePos[i][1]):
            foodPos = np.random.choice(np.arange(0, 600, snakeSize) ,size=(2)) 
        snakePos[i][0] = snakePos[i - 1][0] 
        snakePos[i][1] = snakePos[i - 1][1]
        if (snakePos[0][0] == snakePos[i][0] and snakePos[0][1] == snakePos[i][1] and not i == 1):
            running = False
        pygame.draw.rect(surface=surface,color=getColor("skyblue"), rect=(snakePos[i][0], snakePos[i][1], snakeSize, snakeSize))
    
    # Food Draw
    pygame.draw.rect(surface=surface,color=getColor("green"), rect=(foodPos[0], foodPos[1], snakeSize, snakeSize))
    
    # Snake Draw
    pygame.draw.rect(surface=surface,color=getColor("red"), rect=(snakePos[0][0], snakePos[0][1], snakeSize, snakeSize))

    
    pygame.display.flip()
    clock.tick(fps)
        
pygame.quit()