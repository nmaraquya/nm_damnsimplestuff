
import pygame
pygame.init()
import random
import numpy
import math
import sys


class space:
    height, width, title = 0,0,0
    content = []
    window = False
    simulate = False

    def __init__(self, height, width, title="Simulation"):
        self.height = height
        self.width = width
        self.title = title

    def start(self):
        self.window = pygame.display.set_mode((self.width,self.height))
        pygame.display.set_caption(self.title)
    
    def run(self):
        self.simulate = True
        while self.simulate:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.simulate = False
            self.iterate()
            pygame.time.delay(15)
        pygame.quit()
        return False

    def redrawGameWindow(self):
        self.window.fill((0,0,0))
        for i in self.content:
            pygame.draw.circle(self.window, i.color, (i.XY[0], i.XY[1]), i.radius)
        pygame.display.update()
    
    def iterate(self):
        for i in self.content:
            i.edge = False
        for i in self.content:
            self.move(i)
        self.redrawGameWindow()
    
    def move(self, ball):
        ball.XY[0] += ball.velocity[0] * math.cos( ball.velocity[1] )
        ball.XY[1] += ball.velocity[0] * math.sin( ball.velocity[1] )
        if (ball.XY[0] + ball.radius >= self.width or ball.XY[0] - ball.radius <= 0):
            ball.velocity[1] = (3 * math.pi - ball.velocity[1])%(2*math.pi)
        elif (ball.XY[1] + ball.radius >= self.height or ball.XY[1] - ball.radius <= 0):
            ball.velocity[1] = (4 * math.pi - ball.velocity[1])%(2*math.pi)
        for i in self.content:
            if i.title != ball.title and not ball.edge and not i.edge:
                bounce = self.getBounce(ball, i)

    def getBounce(self,ball_1, ball_2):
        dist = self.getDistance(ball_1.XY,ball_2.XY)

        # https://williamecraver.wixsite.com/elastic-equations

        if (dist+5 <= ball_1.radius + ball_2.radius and not ball_1.edge and not ball_2.edge):
            
            phi = self.getphi(ball_2.XY[0]-ball_1.XY[0],ball_2.XY[1]-ball_1.XY[1])

            vx1 = ((ball_1.velocity[0]*math.cos(ball_1.velocity[1] - phi)*(ball_1.mass - ball_2.mass) + 2*ball_2.mass*ball_2.velocity[0] * math.cos(ball_2.velocity[1] - phi)) / (ball_1.mass + ball_2.mass))*math.cos(phi) + ball_1.velocity[0]*math.sin(ball_1.velocity[1] - phi)*math.cos(phi + math.pi/2)

            vy1 = ((ball_1.velocity[0]*math.cos(ball_1.velocity[1] - phi)*(ball_1.mass - ball_2.mass) + 2*ball_2.mass*ball_2.velocity[0] * math.cos(ball_2.velocity[1] - phi)) / (ball_1.mass + ball_2.mass))*math.sin(phi) + ball_1.velocity[0]*math.sin(ball_1.velocity[1] - phi)*math.sin(phi + math.pi/2)
            
            vx2 = ((ball_2.velocity[0]*math.cos(ball_2.velocity[1] - phi)*(ball_2.mass - ball_1.mass) + 2*ball_1.mass*ball_1.velocity[0]*math.cos(ball_1.velocity[1] - phi)) / (ball_2.mass + ball_1.mass))*math.cos(phi) + ball_2.velocity[0]*math.sin(ball_2.velocity[1] - phi)*math.cos(phi + math.pi/2)

            vy2 = ((ball_2.velocity[0]*math.cos(ball_2.velocity[1] - phi)*(ball_2.mass - ball_1.mass) + 2*ball_1.mass*ball_1.velocity[0]*math.cos(ball_1.velocity[1] - phi)) / (ball_2.mass + ball_1.mass))*math.sin(phi) + ball_2.velocity[0]*math.sin(ball_2.velocity[1] - phi)*math.sin(phi + math.pi/2)
            
            vp1 = math.sqrt(math.pow(vx1,2)+math.pow(vy1,2))
            vp2 = math.sqrt(math.pow(vx2,2)+math.pow(vy2,2))

            va1 = self.getphi(vx1,vy1)
            va2 = self.getphi(vx2,vy2)

            ball_1.velocity=[vp1,va1]
            ball_2.velocity=[vp2,va2]

#            ball_1.edge = True
#            ball_2.edge = True

        elif (dist > ball_1.radius + ball_2.radius and ball_1.edge and ball_2.edge):
            ball_1.edge = False
            ball_2.edge = False

    def getphi(self,x,y):
        if(x > 0 and y >= 0):
            return math.atan(y/x)
        elif(x > 0 and y < 0):
            return math.atan(y/x) + 2*math.pi
        elif(x < 0):
            return math.atan(y/x) + math.pi
        elif(x == 0 and y > 0):
            return  math.pi / 2
        elif(x == 0 and y < 0):
            return  3 * math.pi / 2
        else:
            return 0


    def getDistance(self,XY1,XY2):
        X1,Y1 = XY1
        X2,Y2 = XY2
        distance = math.sqrt(math.pow((X2-X1),2) + math.pow((Y2-Y1),2))
        return distance

    def __repr__(self):  
        return "NOT IMPLEMENTED YET"

class ball:
    VX, VY, mass, X, Y, radius, color, title, edge = 0,0,0,0,0,0,0,0,False

    def __init__(self, velocity, XY, radius, title):
        self.velocity = velocity
        self.XY = XY
        self.radius = radius
        self.mass = math.pi*radius
        self.color = (random.randint(1,255), random.randint(1,255), random.randint(1,255))
        self.title = title

    def __repr__(self):  
        return "Title: %s; [X,Y]: [%s,%s]; mass: %s; velocity: [%s,%s]; radius: %s; color: %s" % (self.title, self.XY[0], self.XY[1], self.mass, self.velocity[0], self.velocity[1], self.radius, self.color)

if __name__ == "__main__":
    size = 1300
    bs = 140
    field = space(1080,1920,"TestWindow")
    for i in range(3):
        field.content.append(ball(
             [random.randint(1,20),
             (random.randint(1,360)/360)*2*math.pi],
             [random.randint(200,size-200),
             random.randint(200,size-200)],
             random.randint(bs-20,bs),
            str(i)))
    for i in field.content:
        print(i)
    field.start()
    field.run()