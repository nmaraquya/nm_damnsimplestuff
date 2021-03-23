import pygame
pygame.init()
import random
import numpy

HEIGHT = 1200
WIDTH = 1200
NUM_BALLS = 20


#setup
win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Simulation")

class Particle(object):
    def __init__(self, x, y , radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.xvel = random.randint(1,15)
        self.yvel = random.randint(1,15)
        self.colideCheck = []
        
    def Draw_circle(self):
        pygame.draw.circle(win, (255,0,0), (int(self.x), int(self.y)), self.radius)


def redrawGameWindow():
    win.fill((0,0,0))
    for ball in balls:
        ball.Draw_circle()
    pygame.display.update()

def bounce(v1,v2, mass1 = 1, mass2 = 1):
    multi1 = mass1/(mass1+mass2)
    multi2 = mass2/(mass1+mass2)
    deltaV2 = (multi1*v1[0]-multi2*v2[0],multi1*v1[1]-multi2*v2[1])
    deltaV1 = (multi2*v2[0]-multi1*v1[0],multi2*v2[1]-multi1*v1[1])
    print("preVelocities:",v1,v2)
    return deltaV1,deltaV2

def checkCollide(circ1Cord,circ1Rad,circ2Cord,circ2Rad):
    tryDist = circ1Rad+circ2Rad
    actualDist = dist(circ1Cord,circ2Cord)
    if dist(circ1Cord,circ2Cord) <= tryDist:
        return True
    return False

def dist(pt1,pt2):
    dX = pt1[0]-pt2[0]
    dY = pt1[1]-pt2[1]
    return (dX**2 + dY**2)**0.5

balls = []  

for turn in range(NUM_BALLS):
    balls.append(Particle(random.randint(60,WIDTH-60),random.randint(60,HEIGHT-60),40))


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    for ball in balls:
         if (ball.x + ball.radius) <= WIDTH and (ball.x - ball.radius) >= 0:
             ball.x += ball.xvel
         else:
             ball.xvel *= -1
             ball.x += ball.xvel

         if (ball.y + ball.radius) <= HEIGHT and (ball.y - ball.radius) >= 0:
             ball.y += ball.yvel
         else:
             ball.yvel *= -1
             ball.y += ball.yvel

    for ball in balls:
        for secBallCheck in balls:
            if secBallCheck not in ball.colideCheck and ball!= secBallCheck and checkCollide((ball.x,ball.y),ball.radius,(secBallCheck.x,secBallCheck.y),secBallCheck.radius):
                print("COLLIDE")
                vel1,vel2 = bounce((ball.xvel,ball.yvel),(secBallCheck.xvel,secBallCheck.yvel))
                print(vel1,vel2)
                ball.xvel = vel1[0]
                ball.yvel = vel1[1]
                ball.colideCheck.append(secBallCheck)
                secBallCheck.xvel = vel2[0]
                secBallCheck.yvel = vel2[1]
                secBallCheck.colideCheck.append(ball)
            elif not checkCollide((ball.x,ball.y),ball.radius,(secBallCheck.x,secBallCheck.y),secBallCheck.radius):
                if ball in secBallCheck.colideCheck:
                    secBallCheck.colideCheck.remove(ball)
                    ball.colideCheck.remove(secBallCheck)
    redrawGameWindow()
    pygame.time.delay(20)

pygame.quit()