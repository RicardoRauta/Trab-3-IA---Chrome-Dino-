import pygame
import os
import random
import time
from sys import exit
from experta import *

pygame.init()

# Valid values: HUMAN_MODE or AI_MODE
GAME_MODE = "AI_MODE"
GRAPH = True

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
if GRAPH:
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus4.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))


class Dinosaur:
    X_POS = 90
    Y_POS = 330
    Y_POS_DUCK = 355
    JUMP_VEL = 17
    JUMP_GRAV = 1.1

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = 0
        self.jump_grav = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):
        if self.dino_duck and not self.dino_jump:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 20:
            self.step_index = 0

        if userInput == "K_UP" and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput == "K_DOWN" and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif userInput == "K_DOWN":
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = True
        elif not (self.dino_jump or userInput == "K_DOWN"):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 10]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 10]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_duck:
            self.jump_grav = self.JUMP_GRAV * 4
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel
            self.jump_vel -= self.jump_grav
        if self.dino_rect.y > self.Y_POS + 10:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL
            self.jump_grav = self.JUMP_GRAV
            self.dino_rect.y = self.Y_POS

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

    def getXY(self):
        return (self.dino_rect.x, self.dino_rect.y)


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle():
    def __init__(self, image, type):
        super().__init__()
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()

        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < - self.rect.width:
            obstacles.pop(0)

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

    def getXY(self):
        return (self.rect.x, self.rect.y)

    def getHeight(self):
        return y_pos_bg - self.rect.y

    def getType(self):
        return (self.type)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 345


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)

        # High, middle or ground
        if random.randint(0, 3) == 0:
            self.rect.y = 345
        elif random.randint(0, 2) == 0:
            self.rect.y = 260
        else:
            self.rect.y = 300
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 19:
            self.index = 0
        SCREEN.blit(self.image[self.index // 10], self.rect)
        self.index += 1


class KeyClassifier:
    def __init__(self, state):
        pass

    def keySelector(self, distance, obHeight, speed, obType):
        pass

    def updateState(self, state):
        pass

"""
def first(x):
    return x[0]
"""


class RuleBasedPlayer(KnowledgeEngine):

    def setAction(self, action):
        self.action = action

    def getAction(self):
        return self.action

    @Rule(AND(Fact(timeEnter=P(lambda x: x < 8)),
              Fact(obHeight=P(lambda x: x < 60)),
              NOT(Fact(dinoHeight=P(lambda x: x < 330)))))
    def jump(self):
           self.retract(1)
           self.declare(Fact(action='K_UP'))

    @Rule(Fact(obHeight=P(lambda x: x > 60)))  
    def getDown(self): 
           self.retract(1)
           self.declare(Fact(action='K_DOWN'))

    @Rule(AND(Fact(timeLeave=P(lambda x: x < 2)),
              Fact(dinoHeight=P(lambda x: x < 330)), 
              OR(NOT(Fact(time2=P(lambda x: x < 10))),
                  Fact(obHeight2=P(lambda x: x > 60)))))
    def getDownFast(self): 
           self.retract(1)
           self.declare(Fact(action='K_DOWN'))

    @Rule(Fact(action=MATCH.action))
    def selectAction(self, action):
        self.setAction(action)

class RuleBasedKeyClassifier(KeyClassifier):
    def __init__(self):
        self.engine = RuleBasedPlayer()

    def keySelector(self, obDistance, obHeight, scSpeed, obWidth, diHeight, obDistance2, obHeight2, obWidth2):    
        self.engine.reset()
        self.engine.declare(Fact(action='K_NO'))
        self.engine.declare(Fact(distance=obDistance-obWidth))
        self.engine.declare(Fact(obHeight=obHeight))
        self.engine.declare(Fact(speed=scSpeed))
        self.engine.declare(Fact(obWidth=obWidth))
        timeEnter=(obDistance-2*obWidth)/scSpeed
        timeLeave=(obDistance+2*obWidth)/scSpeed
        self.engine.declare(Fact(timeEnter=timeEnter))
        self.engine.declare(Fact(timeLeave=timeLeave))
        self.engine.declare(Fact(dinoHeight=diHeight))
        self.engine.declare(Fact(distance2=obDistance2))
        self.engine.declare(Fact(obHeight2=obHeight2))
        self.engine.declare(Fact(time2=obDistance2/scSpeed-11.1))
        self.engine.declare(Fact(obWidth2=obWidth2))
        self.engine.run()
        #TimeEnter - 11.4
        #TimeLeave - X
        print([obDistance-2*obWidth, obWidth, timeEnter, timeLeave, obHeight, diHeight])
        return self.engine.getAction()

def playerKeySelector():
    userInputArray = pygame.key.get_pressed()

    if userInputArray[pygame.K_UP]:
        return "K_UP"
    elif userInputArray[pygame.K_DOWN]:
        return "K_DOWN"
    else:
        return "K_NO"


def playGame():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 10
    x_pos_bg = 0
    y_pos_bg = 383
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0
    spawn_dist = 0

    def score():
        global points, game_speed
        points += 0.25
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Points: " + str(int(points)), True, (0, 0, 0))
        if GRAPH:
            textRect = text.get_rect()
            textRect.center = (1000, 40)
            SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()

        if GRAPH:
            SCREEN.fill((255, 255, 255))

        obDistance = 1500
        obHeight = 0
        obType = 2
        obWidth = 0
        obDistance2 = 0
        obHeight2 = 0
        obWidth2 = 0
        if len(obstacles) != 0:
            xy = obstacles[0].getXY()
            obDistance = xy[0]
            obHeight = obstacles[0].getHeight()
            obType = obstacles[0]
            obWidth = obstacles[0].rect.width
        if len(obstacles) > 1:
            xy2 = obstacles[1].getXY()
            obDistance2 = xy2[0]
            obHeight2 = obstacles[1].getHeight()
            obWidth2 = obstacles[1].rect.width

        if GAME_MODE == "HUMAN_MODE":
            userInput = playerKeySelector()
        else:
            userInput = aiPlayer.keySelector(obDistance, obHeight, game_speed, obWidth, player.getXY()[1], obDistance2, obHeight2, obWidth2)

        if len(obstacles) == 0 or obstacles[-1].getXY()[0] < spawn_dist:
            spawn_dist = random.randint(0, 670)
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 5) == 5:
                obstacles.append(Bird(BIRD))

        player.update(userInput)
        if GRAPH:
            player.draw(SCREEN)

        for obstacle in list(obstacles):
            obstacle.update()
            if GRAPH:
                obstacle.draw(SCREEN)

        if GRAPH:
            background()

            cloud.draw(SCREEN)
            cloud.update()

        score()
        if GRAPH:
            if obDistance > 200:
                clock.tick(60)
            else :
                clock.tick(1)
        
            pygame.display.update()

        for obstacle in obstacles:
            if player.dino_rect.colliderect(obstacle.rect):
                ### print (game_speed, distance) 
                pygame.time.delay(2000)
                death_count += 1
                return points

def main():
    global aiPlayer

    aiPlayer = RuleBasedKeyClassifier()
    print (playGame())


main()

