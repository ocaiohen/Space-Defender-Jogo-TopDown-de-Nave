import pygame
from pygame import mixer
import math
import random

pygame.init()

screenWidth = 1280
screenHeight = 720
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()
fps = 60

mixer.init()
playerShotSound = mixer.Sound("./Sounds/170161__timgormly__8-bit-laser.mp3")

class EnemyGenerator():
    def __init__(self):
        self.maxNumberOfShooters = 2
        self.maxNumberOfKamikazes = 2
        self.timeForIncreaseMaxShooters = 13
        self.timeForIncreaseMaxKamikazes = 11
        self.numberOfAnyEnemiesKilled = 0
        self.numberOfShootersKilled = 0
        self.numberOfKamikazesKilled = 0
    def generateRandomPositionOffScreen(self):
        pass
    def createShooter(self):
        pass
    def createKamikaze(self):
        pass
    def createAsteroid(self):
        pass
    def update(self):
        pass
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
        pygame.draw.rect(screen, "red", player.rect, width=2)
        self.timeOfLastShot += 1

class Bullet(pygame.sprite.Sprite):
    def __init__(self, startPositionX, startPositionY, angle):
        super().__init__()
        self.startPositionX, self.startPositionY, self.angle = startPositionX, startPositionY, angle
        self.x, self.y = self.startPositionX, self.startPositionY
        self.image = pygame.image.load("./Sprites/Bullet.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.03)
        self.transparencyColor = self.image.get_at((0,0))
        self.image.set_colorkey(self.transparencyColor)
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

class EnemyBullet(Bullet):
    def __init__(self, startPositionX, startPositionY, angle):
        super().__init__(startPositionX, startPositionY, angle)
        self.image = pygame.image.load("./Sprites/Enemy Bullet.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.03)
        self.transparencyColor = self.image.get_at((0,0))
        self.image.set_colorkey(self.transparencyColor)
  
class EnemyShooter(pygame.sprite.Sprite):
    def __init__(self, startX, startY, shootPoint):
        self.position = pygame.math.Vector2(startX, startY)
        self.shootPoint = shootPoint
        self.size = 0.1
        self.image = pygame.transform.rotozoom(pygame.image.load("./Sprites/Nave-Inimiga-Shooter.png").convert_alpha(), 0, self.size)
        self.baseImage = self.image
        self.rect = self.image.get_rect(center=self.position)
        self.speed = 1
        self.vX, self.vY = 0, 0
        self.timeOfLastShot = 0
        super().__init__()
    def rotateToPlayer(self):
        self.playerCoordinates = player.playerPosition
        self.deltaX = (self.playerCoordinates[0] - self.rect.centerx)
        self.deltaY = (self.playerCoordinates[1] - self.rect.centery)
        self.angle = math.degrees(math.atan2(-self.deltaY, self.deltaX))
        self.image = pygame.transform.rotate(self.baseImage, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        pass
    def tryToShoot(self):
        cooldown = int(random.randrange(fps * 1, 5 * fps))
        if self.timeOfLastShot >= cooldown:
            self.shoot()
            self.timeOfLastShot = 0
    def getRotatedPoint(self, relativePoint):
        rotatedVector = pygame.math.Vector2(relativePoint).rotate(-self.angle)
        return self.rect.center + rotatedVector

    def shoot(self):
        bulletStartPoint = self.getRotatedPoint((self.image.get_width() / 2, 0))  # Extremidade no meio do lado direito
        bullet = EnemyBullet(bulletStartPoint.x, bulletStartPoint.y, -self.angle)
        enemiesGroup.add(bullet)
        allSpritesGroup.add(bullet)
        playerShotSound.play()

    def moveToShootPoint(self):
        self.deltaXtoSP = (self.shootPoint[0] - self.position[0])
        self.deltaYtoSP = (self.shootPoint[1] - self.position[1])

        angleRadians = math.atan2(self.deltaYtoSP, self.deltaXtoSP)

        self.vX = self.speed * math.cos(angleRadians)
        self.vY = self.speed * math.sin(angleRadians)

        self.position[0] += self.vX 
        self.position[1] += self.vY

        self.rect = self.image.get_rect(center=self.position)

    def update(self):
        if int(self.position[0]) != int(self.shootPoint[0]) and  int(self.position[1]) != int(self.shootPoint[1]):
            self.moveToShootPoint()
        pygame.draw.rect(screen, "red", self.rect, width=2)
        self.rotateToPlayer()
        self.tryToShoot()
        self.timeOfLastShot += 1

class EnemyKamikaze(pygame.sprite.Sprite):
    def __init__(self, startX, startY):
        super().__init__()
        self.position = pygame.math.Vector2(startX, startY)
        self.size = 0.15
        self.image = pygame.transform.rotozoom(pygame.image.load("./Sprites/Nave-Inimiga-Kamikaze.png").convert_alpha(), 0, self.size)
        self.baseImage = self.image
        self.rect = self.image.get_rect(center=self.position)
        self.speed = 3

    def rotateAndMoveToPlayer(self):
        self.playerCoordinates = player.playerPosition
        self.deltaX = self.playerCoordinates[0] - self.rect.centerx
        self.deltaY = self.playerCoordinates[1] - self.rect.centery

        # Calcular o ângulo em radianos
        angleRadians = math.atan2(self.deltaY, self.deltaX)

        # Calcular o vetor de movimento
        self.vX = self.speed * math.cos(angleRadians)
        self.vY = self.speed * math.sin(angleRadians)

        # Atualizar a posição
        self.position[0] += self.vX 
        self.position[1] += self.vY

        # Atualizar a rotação
        self.angle = math.degrees(angleRadians)
        self.image = pygame.transform.rotate(self.baseImage, -self.angle)  # Corrigir a rotação
        self.rect = self.image.get_rect(center=self.position)

    def update(self):
        self.rotateAndMoveToPlayer()
        pygame.draw.rect(screen, "red", self.rect, width=2)

def writeSomething(fontstyle, fontsize, textContent, color, x, y, screen):
     font = pygame.font.SysFont(f"{fontstyle}", fontsize)
     text = font.render(f"{textContent}", True, color)
     screen.blit(text, [x, y])

def generateEnemyShooter():
    pass

def checkIfPlayerGotHit(playerGroup, enemiesGroup):
    collisions = pygame.sprite.groupcollide(enemiesGroup, playerGroup, False, False)
    if collisions: return True
    else: return False

def checkIfEnemiesGotHit(enemiesGroup, bulletsGroup):
    collisions = pygame.sprite.groupcollide(enemiesGroup, bulletsGroup, True, True)
    if collisions: return True
    else: return False

player = Player()
enemy = EnemyShooter(200,200, (500,500))
allSpritesGroup = pygame.sprite.Group()
playerGroup = pygame.sprite.Group()
playerGroup.add(player)
bulletsGroup = pygame.sprite.Group()
enemiesGroup = pygame.sprite.Group()
enemiesGroup.add(enemy)
allSpritesGroup.add(enemy)
allSpritesGroup.add(player)

background = pygame.transform.scale(pygame.image.load("./Sprites/pexels-instawalli-176851.jpg").convert(), (screenWidth, screenHeight))

endTheGame = False
while not endTheGame:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            endTheGame = True

    screen.blit(background, (0,0))
    allSpritesGroup.draw(screen)
    allSpritesGroup.update()
    
    if checkIfPlayerGotHit(playerGroup, enemiesGroup): endTheGame = True
    checkIfEnemiesGotHit(enemiesGroup, bulletsGroup)
    pygame.display.update()
    clock.tick(fps)

pygame.quit()
