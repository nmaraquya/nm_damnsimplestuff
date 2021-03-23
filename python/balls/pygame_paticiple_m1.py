import pygame
pygame.init()
import random
import numpy
import math

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
        simulate = True
        while simulate:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.simulate = False
            self.iterate()
            pygame.time.delay(20)
        pygame.quit()
        return False

    def redrawGameWindow(self):
        self.window.fill((0,0,0))
        for i in self.content:
            pygame.draw.circle(self.window, i.color, (i.X, i.Y), i.radius)
        pygame.display.update()
    
    def iterate(self):
        for i in self.content:
            self.move(i)
        self.redrawGameWindow()
    
    def move(self, ball):
        ball.X += ball.VX
        ball.Y += ball.VY
        if (ball.X+ball.radius > self.width  or ball.X-ball.radius < 0):  
            ball.VX = -ball.VX
        if (ball.Y+ball.radius > self.height or ball.Y-ball.radius < 0):  
            ball.VY = -ball.VY
        for i in self.content:
            if i.title != ball.title:
                bounce = False
                bounce = self.getBounce(ball, i)
                if bounce:
                    ball.VX = -ball.VX
                    ball.VY = -ball.VY

    def getBounce(self,ball_1, ball_2):
        dist = self.getDistance(ball_1.X,ball_1.Y,ball_2.X,ball_2.Y)
        if (dist < ball_1.radius + ball_2.radius):
            return True
        else: 
            return False

    def getDistance(self,X1,Y1,X2,Y2):
        distance = math.sqrt(math.pow((X2-X1),2) + math.pow((Y2-Y1),2))
        return distance


    def __repr__(self):  
        return "NOT IMPLEMENTED YET"

class ball:
    VX, VY, mass, X, Y, radius, color, title = 0,0,0,0,0,0,0,0

    def __init__(self, VX, VY, X, Y, radius, color, title):
        self.VX = VX
        self.VY = VY
        self.X = X
        self.Y = Y
        self.radius = radius
        self.mass = math.pi*radius
        self.color = color
        self.title = title

    def __repr__(self):  
        return "Title: %s; [X,Y]: [%s,%s]; mass: %s; velocity: [%s,%s]; radius: %s; color: %s" % (self.title, self.X, self.Y, self.mass, self.VX, self.VY, self.radius, self.color)

def newrandom(MIN,MAX):
    global seed
    seed += 1
    random.seed(seed)
    return(random.randint(MIN,MAX))

seed = random.randint(1,1400)

if __name__ == "__main__":
    size = 1100
    field = space(size,size,"TestWindow")
    j=0
    for i in range(12):
        field.content.append(ball(
             newrandom(1,10),
             newrandom(1,10),
             newrandom(1,size),
             newrandom(1,size),
             newrandom(1,30),
            (newrandom(1,255),
             newrandom(1,255),
             newrandom(1,255)),
            str(i)))
    for i in field.content:
        print(i)
    field.start()
    field.run()