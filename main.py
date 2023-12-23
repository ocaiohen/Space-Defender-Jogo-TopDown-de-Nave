import pygame
from pygame import mixer
import math

pygame.init()

screenWidth = 1280
screenHeight = 720
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()
fps = 60

mixer.init()
playerShotSound = mixer.Sound("./Sounds/170161__timgormly__8-bit-laser.mp3")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.playerSize = 0.1
        self.playerPosition = pygame.math.Vector2(screenWidth / 2, screenHeight / 2)
        self.image = pygame.transform.rotozoom(pygame.image.load("./Sprites/Nave Nova Girada Para Direita PNG.png").convert_alpha(), 0, self.playerSize)
        self.baseImage = self.image
        self.rect = self.image.get_rect(center=self.playerPosition)
        self.timeOfLastShot = 0
        self.shotCooldown = fps / 3
        self.speed = 5

    def userInput(self):
        self.velocityX = 0
        self.velocityY = 0

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.velocityY -= self.speed
        if keys[pygame.K_s]:
            self.velocityY += self.speed
        if keys[pygame.K_a]:
            self.velocityX -= self.speed
        if keys[pygame.K_d]:
            self.velocityX += self.speed

        if self.velocityY != 0 and self.velocityX != 0:
            self.velocityX /= (2) ** (1/2)
            self.velocityY /= (2) ** (1/2)

        if pygame.mouse.get_pressed() == (1, 0, 0) and self.timeOfLastShot >= self.shotCooldown:
            self.shoot()
            self.timeOfLastShot = 0

    def move(self):
        self.playerPosition += pygame.math.Vector2(self.velocityX, self.velocityY)
        self.rect.center = self.playerPosition

    def playerRotation(self):
        self.mouseCoordinates = pygame.mouse.get_pos()
        self.deltaX = (self.mouseCoordinates[0] - self.rect.centerx)
        self.deltaY = (self.mouseCoordinates[1] - self.rect.centery)
        self.angle = math.degrees(math.atan2(-self.deltaY, self.deltaX))
        self.image = pygame.transform.rotate(self.baseImage, self.angle)
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect(center=self.rect.center)

    def getRotatedPoint(self, relativePoint):
        rotatedVector = pygame.math.Vector2(relativePoint).rotate(-self.angle)
        return self.rect.center + rotatedVector

    def shoot(self):
        bulletStartPoint = self.getRotatedPoint((self.image.get_width() / 2, 0))  # Extremidade no meio do lado direito
        bullet = Bullet(bulletStartPoint.x, bulletStartPoint.y, -self.angle)
        bulletsGroup.add(bullet)
        allSpritesGroup.add(bullet)
        playerShotSound.play()

    def update(self):
        self.userInput()
        self.move()
        self.playerRotation()
        self.timeOfLastShot += 1

class Bullet(pygame.sprite.Sprite):
    def __init__(self, startPositionX, startPositionY, angle):
        super().__init__()
        self.startPositionX, self.startPositionY, self.angle = startPositionX, startPositionY, angle
        self.x, self.y = self.startPositionX, self.startPositionY
        self.image = pygame.image.load("./Sprites/Bullet.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.03)
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.speed = 9
        self.velocityY = math.sin(self.angle * (2 * math.pi / 360)) * self.speed
        self.velocityX = math.cos(self.angle * (2 * math.pi / 360)) * self.speed
        self.lifetime = fps * 3.5 
        self.age = 0

    def move(self):
        self.x += self.velocityX
        self.y += self.velocityY

        self.rect.x, self.rect.y = self.x, self.y
    def getOld(self):
        self.age += 1
        if self.age >= self.lifetime: self.kill()
    def update(self):
        self.move()
        self.getOld()
        

player = Player()

allSpritesGroup = pygame.sprite.Group()
bulletsGroup = pygame.sprite.Group()
allSpritesGroup.add(player)

endTheGame = False
while not endTheGame:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            endTheGame = True

    screen.fill((0, 0, 0))
    allSpritesGroup.draw(screen)
    allSpritesGroup.update()

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
