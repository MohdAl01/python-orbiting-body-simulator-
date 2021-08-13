import pygame
from random import randint
from math import *
import numpy as np

pygame.init()

WIDTH, HEIGHT = 1200, 700
CENTER = (WIDTH//2, HEIGHT//2)
FPS = 60
TIME = 1/FPS

SOL_MASS = 10**16
PLANET_MASS = 10**9
G = 6.67 * 10**(-12)

WHITE = (225,225,225)
BLACK = (0,0,0)

Bodies = []

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grav sim")

"""
interesting init settings:
Initial_Body_Properties(False, CENTER[0]-100, CENTER[1], 0, 5, SOL_MASS)
Initial_Body_Properties(False, CENTER[0]+100, CENTER[1], 0, -5, SOL_MASS)
Initial_Body_Properties(False, CENTER[0]-200, CENTER[1], 0, 10, PLANET_MASS)
"""

def Initial_Body_Properties(random, init_pos_x=0,init_pos_y=0, init_vel_x=0, init_vel_y=0,mass=PLANET_MASS):
    # returns the initial x and y positions and velocities as a list
    # if random is ture, the x and y positions and velocities will be random, as well as the color
    R = randint(0,225)
    G = randint(0,225)
    B = randint(0,225)
    COLOR = (R,G,B)

    if random == True:
        random_pos_x = randint(WIDTH//3,2*WIDTH//3)
        random_pos_y = randint(HEIGHT//3,2*HEIGHT//3)
        random_vel_x = randint(3,5)
        random_vel_y = randint(3,5)

        Bodies.append([random_pos_x, random_pos_y, 0, 0, COLOR, mass])
    else:
        Bodies.append([init_pos_x, init_pos_y, init_vel_x, init_vel_y, COLOR,mass])



# Initial_Body_Properties(False, 800, 300, 0, 0, 10)
# Initial_Body_Properties(False, 400, 300, 0, -6, SOL_MASS)
# #Initial_Body_Properties(False, 600, 300, 0, 6, SOL_MASS)

def Cos_Sin(x,y):

    Vector1 = [1,0]
    Vector2 = [x,y]
    Vector2_array = np.array(Vector2)
    Vector2_array_mag = np.linalg.norm(Vector2)

    Dot_Product = np.dot(Vector1,Vector2)
    Cross_Product = np.cross(Vector1, Vector2)

    Cos = Dot_Product / Vector2_array_mag
    Sin = Cross_Product / Vector2_array_mag

    return Cos, Sin

def Radius_Comp(x1,y1,x2,y2):
    Radius = sqrt((x1-x2)**2 + (y1-y2)**2)
    Xcomp = (x1-x2)
    Ycomp = (y1-y2)

    return Radius, Xcomp, Ycomp

def Acceleration():
    # loops through all items in Bodies. calculates the acceleration due to gravity felt, breaks that into its components
    # then calculates the change in velocity and position, and changes the values stored in Bodies accordingly
    for i in range(len(Bodies)):
        for j in range(len(Bodies)):
            if i != j:

                Radius, Xcomp, Ycomp = Radius_Comp(Bodies[i][0],Bodies[i][1],Bodies[j][0],Bodies[j][1])
                Cos, Sin = Cos_Sin(Xcomp, Ycomp)

                acc = (G * Bodies[j][5]) / (Radius**2)

                print(acc)
                x_acc = -Cos * acc
                y_acc = -Sin * acc

                Bodies[i][2] += x_acc*TIME
                Bodies[i][3] += y_acc*TIME

                Bodies[i][0] += Bodies[i][2]
                Bodies[i][1] += Bodies[i][3]

def Draw_body(body):
    if body[5] == SOL_MASS:
        pygame.draw.circle(WIN,body[4],(body[0],body[1]),10)
    else:
        pygame.draw.circle(WIN,body[4],(body[0],body[1]),5)


# Initial_Body_Properties(False, CENTER[0]+100, CENTER[1], 0, 1, SOL_MASS)
# Initial_Body_Properties(False, CENTER[0]-100, CENTER[1], 0, -1, SOL_MASS)
# Initial_Body_Properties(False, CENTER[0]+200, CENTER[1], 0, 2)


Initial_Body_Properties(False, CENTER[0]+100, CENTER[1], 0, 1, SOL_MASS)
Initial_Body_Properties(False, CENTER[0]-100, CENTER[1], 0, -1, SOL_MASS)
Initial_Body_Properties(False, CENTER[0]+250, CENTER[1], 0, 2)

def Draw_win():
    WIN.fill(BLACK)

    for i in range(len(Bodies)):
        Draw_body(Bodies[i])
    # pygame.draw.rect(WIN, BLACK, (CENTER[0]+200,CENTER[1],3,3), 0)

#        Bodies[i][0] += Bodies[i][2]
#        Bodies[i][1] += Bodies[i][3]
        # Bodies[i][0] is the x position, Bodies[i][2] is the x velocity. bottom line is the y pos and vel
    pygame.display.update()




def Main():

    clock = pygame.time.Clock()
    run = True
    while run:

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        Acceleration()
        Draw_win()


Main()
