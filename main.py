import pygame
import sys
import random
import time

pygame.init()
pygame.display.set_caption("My first PyGame program")
screen = pygame.display.set_mode((1280, 768))  # Sets resolution.

screenWidth = 1280
screenHeight = 768

clock = pygame.time.Clock()  # Built-in function that enables frame-rate control.
playerImage = pygame.image.load("player.png")  # Loading an image from a file. Put the file inside the project folder.
playerProjImage = pygame.image.load("playerproj.png")
alien1Image = pygame.image.load("alien1.png")
alien1hitBox = alien1Image.get_rect()  # Draw hit box without figuring out size of image.
alien2Image = pygame.image.load("alien2.png")
alien3Image = pygame.image.load("alien3.png")
alienProjImage = pygame.image.load("alienshot.png")
backgroundImage = pygame.image.load("backgrounds_stars.jpg")


class Player:

    def __init__(self):
        self.xPosition = 0
        self.yPosition = 886 - 192
        self.hitBox = playerImage.get_rect(topleft=(self.xPosition, self.yPosition))

    def draw(self):
        screen.blit(playerImage, (self.xPosition, self.yPosition))
        self.hitBox = playerImage.get_rect(topleft=(self.xPosition, self.yPosition))
        # pygame.draw.rect(screen, (200, 0, 0), self.hitBox)

    def move(self):
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.xPosition -= 10
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.xPosition += 10

    def fire(self):
        projectileInstance = Projectile(self.xPosition + self.hitBox.width / 2, self.yPosition)
        projectileList.append(projectileInstance)


class Projectile:

    def __init__(self, x, y):
        self.xPosition = x
        self.yPosition = y
        self.startSpeed = -20
        self.hitBox = playerProjImage.get_rect(topleft=(self.xPosition, self.yPosition))

    def draw(self):
        screen.blit(playerProjImage, (self.xPosition, self.yPosition))
        self.hitBox = playerProjImage.get_rect(topleft=(self.xPosition, self.yPosition))
        # pygame.draw.rect(screen, (0, 0, 200), self.hitBox)

    def move(self):
        projectile.yPosition += self.startSpeed


class Enemy:

    def __init__(self, x, y, colour):  # On initiation, give the raindrops these values. These are randomised ONE TIME per instance of raindrop.
        self.xPosition = x
        self.yPosition = y
        self.size = random.randint(1, 5)
        self.startSpeed = random.uniform(0.05, 0.1)
        self.velocity = random.uniform(0.05, 0.2)
        self.speed = self.startSpeed
        self.colour = colour
        self.hitBox = alien1Image.get_rect(topleft=(self.xPosition, self.yPosition))

    def draw(self):  # Called every frame, takes the values from initialisation. Different for each instance of raindrop.
        screen.blit(alien1Image, (self.xPosition, self.yPosition))
        self.hitBox = alien1Image.get_rect(topleft=(self.xPosition, self.yPosition))
        # pygame.draw.rect(screen, (200, 0, 0), self.hitBox)

    def move(self):  # Called every frame, takes the values from initialisation. Different for each instance of raindrop.
        self.yPosition += self.speed + self.velocity
        self.velocity += 0.05


lives = 5
score = 0

enemyList = []  # MUST be defined outside the while loop, otherwise list is erased every frame (duh).
projectileList = []

playerInstance = Player()

timeSinceLastEnemy = 0
timeSinceLastProjectile = 0

while True:

    clock.tick(60)  # Setting the frame-rate.
    for event in pygame.event.get():  # See the pygame user guide for various events (e.g. get button down).
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # Doesn't spam-fire when key is held down.
            playerInstance.fire()


    # Rendering section (order matters).
    screen.fill((150, 150, 150))  # Filling the screen with a colour.
    screen.blit(backgroundImage, (0, 0))

    if playerInstance.xPosition >= (screenWidth - 119):  # Check the position of each droplet.
        playerInstance.xPosition = (screenWidth - 119)  # Delete the droplets if they cross the bottom border.
    elif playerInstance.xPosition <= -30:
        playerInstance.xPosition = -30
    playerInstance.move()
    playerInstance.draw()

    if time.time() - timeSinceLastEnemy > 3:
        enemy = Enemy(random.randint(0, screenWidth), 0, (100, 100, 100))
        enemyList.append(enemy)
        timeSinceLastEnemy = time.time()

    for projectile in projectileList[:]:  # When removing an item from a list, use a copy of the list as the iterator so the indices don't get mixed up.
        for enemyInstance in enemyList[:]:

            if projectile.hitBox.colliderect(enemyInstance.hitBox):
                projectileList.remove(projectile)
                enemyList.remove(enemyInstance)
                score += 5

            else:
                projectile.move()
                projectile.draw()

    for enemyInstance in enemyList[:]:  # Iterate through the list.

        if playerInstance.hitBox.colliderect(enemyInstance.hitBox):
            lives -= 1
            enemyList.remove(enemyInstance)

        if enemyInstance.yPosition >= screenHeight:
            enemyList.remove(enemyInstance)  # Delete the droplets if they cross the bottom border.
        else:
            enemyInstance.move()  # Also move its position.
            enemyInstance.draw()  # If the droplet isn't below the bottom border, draw it on screen.

    pygame.display.flip()  # 2 buffers: stuff that's going to draw, stuff that's already drawn. Flip turns the two.
