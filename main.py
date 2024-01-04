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
enemyShooterSound = mixer.Sound("./Sounds/49242__zerolagtime__tape_slow5 reverb wav.wav")
shieldSound = mixer.Sound("./Sounds/322875__thedonkey__sci-fi-door.mp3")
explosionSound = mixer.Sound("./Sounds/369524__johandeecke__long-decay-explosion-1.wav")

class EnemyGenerator():
    def __init__(self):
        self.maxNumberOfShooters = 1
        self.maxNumberOfKamikazes = 1
        self.timeForIncreaseMaxShooters = 21
        self.timeForIncreaseMaxKamikazes = 15
        self.timeForAnotherAsteroid = 15
        self.currentNumberOfShooters = 0
        self.currentNumberOfKamikazes = 0
        self.numberOfAnyEnemiesKilled = 0
        self.numberOfShootersKilled = 0
        self.numberOfKamikazesKilled = 0
        self.lastShooterIncreaseTime = pygame.time.get_ticks()
        self.lastKamikazeIncreaseTime = pygame.time.get_ticks()
        self.lastAsteroidCreationTime = pygame.time.get_ticks()

    def generateRandomPositionOffScreen(self):
        x = random.choice([int(random.uniform(-150, screenWidth - 10)), int(random.uniform(screenWidth + 10, screenWidth + 150))])
        y = random.choice([int(random.uniform(screenHeight + 100, screenHeight + 300)), int(random.uniform(300 - screenHeight, 100 - screenHeight)) ])
        
        # if x >= 0 and x <= screenWidth: caso queira que inimigos surjam pelos lados também
        #     y = random.choice([int(random.uniform(screenHeight + 100, screenHeight + 300)), int(random.uniform(300 - screenHeight, 100 - screenHeight)) ])
        # else:
        #     y = random.choice([int(random.uniform(screenHeight / 3, screenHeight + 300)), int(random.uniform(300 - screenHeight, 100 - screenHeight)) ])
        return (x, y)
    def generateRandomPositionOffScreenForAsteroid(self):
        x = random.choice([int(random.uniform(-400, screenWidth - 10)), int(random.uniform(screenWidth + 10, screenWidth + 400))])
        
        if x >= 0 and x <= screenWidth:
            y = random.choice([int(random.uniform(screenHeight + 100, screenHeight + 400)), int(random.uniform(300 - screenHeight, 400 - screenHeight)) ])
        else:
            y = int(random.uniform(-400, screenHeight + 400))
        
        return (x, y)
    def createShootPoint(self):
        x = int(random.uniform(40, screenWidth - 40))
        y = int(random.uniform(40, screenHeight - 40))
        return (x, y)
    def createShooter(self):
        creationPosition = self.generateRandomPositionOffScreen()
        shooter = EnemyShooter(creationPosition[0], creationPosition[1], self.createShootPoint())
        self.currentNumberOfShooters += 1
        allSpritesGroup.add(shooter)
        enemiesGroup.add(shooter)
    def createKamikaze(self):
        creationPosition = self.generateRandomPositionOffScreen()
        kamikaze = EnemyKamikaze(creationPosition[0], creationPosition[1])
        self.currentNumberOfKamikazes += 1
        allSpritesGroup.add(kamikaze)
        enemiesGroup.add(kamikaze)
    def createAsteroid(self):
        x, y = self.generateRandomPositionOffScreenForAsteroid()
        namesOfAsteroidsSprites = ["Asteroid1.png"]
        chosenSpriteName = random.choice(namesOfAsteroidsSprites)
        playerCoordinates = player.playerPosition
        deltaX = playerCoordinates[0] - x
        deltaY = playerCoordinates[1] - y

        angle = math.degrees(math.atan2(deltaY, deltaX))
        speed = random.uniform(0.9, 3.5)
        asteroid = Asteroid(x, y, angle, speed, chosenSpriteName, 0.17)

        allSpritesGroup.add(asteroid)
        asteroidsGroup.add(asteroid)

        
    def update(self):
        currentTime = pygame.time.get_ticks()

        if(self.maxNumberOfKamikazes > self.currentNumberOfKamikazes):
            self.createKamikaze()
        if(self.maxNumberOfShooters > self.currentNumberOfShooters):
            self.createShooter()

        if (currentTime - self.lastShooterIncreaseTime) / 1000 >= self.timeForIncreaseMaxShooters:
            self.maxNumberOfShooters += 1
            print(f"Número máximo de shooters aumentado: {self.maxNumberOfShooters}")
            self.lastShooterIncreaseTime = currentTime

        if (currentTime - self.lastKamikazeIncreaseTime) / 1000 >= self.timeForIncreaseMaxKamikazes:
            self.maxNumberOfKamikazes += 1
            print(f"Número máximo de kamikazes aumentado: {self.maxNumberOfKamikazes}")
            self.lastKamikazeIncreaseTime = currentTime
        if (currentTime - self.lastAsteroidCreationTime) / 1000 >= self.timeForAnotherAsteroid:
            self.createAsteroid()
            print("Asteroide Criado")
            self.lastAsteroidCreationTime = currentTime

# class EffectsGenerator():
#     def generateExplosion(self, position):
#         explosion = Explosion(position)
#         pass
#     def update(self):
#         pass
class Explosion(pygame.sprite.Sprite):
    def __init__(self, position, scale):
        super().__init__()
        self.image = pygame.image.load("./Sprites/ex.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, scale)
        self.rect = self.image.get_rect(center=position)
        self.lifetime = 0.7 * fps  # 1.5 segundos em frames
        self.age = 0
        explosionSound.play()

    def update(self):
        self.age += 1
        if self.age >= self.lifetime:
            self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.playerSize = 0.1
        self.playerPosition = pygame.math.Vector2(screenWidth / 2, screenHeight / 2)
        self.image = pygame.transform.rotozoom(pygame.image.load("./Sprites/Nave Nova Girada Para Direita PNG.png").convert_alpha(), 0, self.playerSize)
        self.baseImage = self.image
        self.rect = self.image.get_rect(center=self.playerPosition)
        self.timeOfLastShot = 0
        self.shotCooldown = fps / 3.5
        self.shieldCooldown = 10 # segundos
        self.timeOfLastShieldActivation = pygame.time.get_ticks()
        self.speed = 5
        self.shieldsOn = False
        self.endTheGame = False

    def canShield(self):
        timeEnoughtToShield = False
        if (self.currentTime - self.timeOfLastShieldActivation) / 1000 >= self.shieldCooldown:
            timeEnoughtToShield = True

        if self.shieldsOn == False and timeEnoughtToShield:
            return True
        else:
            return False
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

        if (pygame.mouse.get_pressed() == (0,0,1) or keys[pygame.K_SPACE]) and self.canShield():
            self.createShield()

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
    
    def createShield(self):
        shieldSound.play()
        shield = Shield()
        self.shieldsOn = True
        allSpritesGroup.add(shield)
        shieldsGroup.add(shield)
        self.timeOfLastShieldActivation = pygame.time.get_ticks()
    def getHit(self):
        if not self.shieldsOn:
            self.endTheGame = True
    def update(self):
        self.currentTime = pygame.time.get_ticks()
        self.userInput()
        self.move()
        self.playerRotation()
        if self.playerPosition[0] < -10:
            self.playerPosition[0] = screenWidth + 7 
        if self.playerPosition[0] > screenWidth + 10:
            self.playerPosition[0] = 7
        if self.playerPosition[1] < -10:
            self.playerPosition[1] = screenHeight + 7
        if self.playerPosition[1] > screenHeight + 10:
            self.playerPosition[1] = 7
        self.rect.center = self.playerPosition
        pygame.draw.rect(screen, "red", player.rect, width=2)
        self.timeOfLastShot += 1

class Bullet(pygame.sprite.Sprite):
    def __init__(self, startPositionX, startPositionY, angle):
        super().__init__()
        self.startPositionX, self.startPositionY, self.angle = startPositionX, startPositionY, angle
        self.position = pygame.math.Vector2(self.startPositionX, self.startPositionY)
        self.image = pygame.image.load("./Sprites/Bullet 2.0.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.025)
        # self.transparencyColor = self.image.get_at((0,0))
        # self.image.set_colorkey(self.transparencyColor)
        self.rect = self.image.get_rect()
        self.rect.center = (self.position[0], self.position[1])
        self.speed = 9
        self.velocityY = math.sin(self.angle * (2 * math.pi / 360)) * self.speed
        self.velocityX = math.cos(self.angle * (2 * math.pi / 360)) * self.speed
        self.lifetime = fps * 3.5 
        self.age = 0

    def move(self):
        self.position[0] += self.velocityX
        self.position[1] += self.velocityY

        self.rect.x, self.rect.y = self.position[0], self.position[1]
    def getOld(self):
        self.age += 1
        if self.age >= self.lifetime: self.die()
    def die(self):
        self.kill()
    def update(self):
        self.move()
        self.getOld()

class Shield(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.position = player.playerPosition
        self.image = pygame.image.load("./Sprites/Shield.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.4)
        self.transparencyColor = self.image.get_at((int(self.image.get_width() / 2), int(self.image.get_height() / 2)))
        self.image.set_colorkey(self.transparencyColor)
        self.rect = self.image.get_rect()
        self.rect.center = (self.position[0], self.position[1])
        self.lifeTime = 3 # em segundos
        self.age = pygame.time.get_ticks() / 1000
    def moveWithPlayer(self):
        self.position = player.playerPosition
        self.rect.center = (self.position[0], self.position[1])
    def die(self):
        player.shieldsOn = False
        self.kill()
    def update(self):
        currentTime = pygame.time.get_ticks() / 1000

        if currentTime - self.age >= self.lifeTime:
            self.die()

        self.moveWithPlayer()
        pygame.draw.rect(screen, "red", self.rect, width=2)
        
class EnemyBullet(Bullet):
    def __init__(self, startPositionX, startPositionY, angle):
        super().__init__(startPositionX, startPositionY, angle)
        self.image = pygame.image.load("./Sprites/Enemy Bullet.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.03)
        self.transparencyColor = self.image.get_at((0,0))
        self.image.set_colorkey(self.transparencyColor)
    def die(self):
        self.kill()
  
class EnemyShooter(pygame.sprite.Sprite):
    def __init__(self, startX, startY, shootPoint):
        self.position = pygame.math.Vector2(startX, startY)
        self.shootPoint = shootPoint
        self.distanceToSPToShoot = 100
        self.size = 0.1
        self.image = pygame.transform.rotozoom(pygame.image.load("./Sprites/Nave-Inimiga-Shooter.png").convert_alpha(), 0, self.size)
        self.baseImage = self.image
        self.rect = self.image.get_rect(center=self.position)
        self.speed = 3
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
        enemyShooterSound.play()

    def moveToShootPoint(self):
        self.deltaXtoSP = (self.shootPoint[0] - self.position[0])
        self.deltaYtoSP = (self.shootPoint[1] - self.position[1])

        angleRadians = math.atan2(self.deltaYtoSP, self.deltaXtoSP)

        self.vX = self.speed * math.cos(angleRadians)
        self.vY = self.speed * math.sin(angleRadians)

        self.position[0] += self.vX 
        self.position[1] += self.vY

        self.rect = self.image.get_rect(center=self.position)
    def die(self):
        enemyGenerator.currentNumberOfShooters -= 1
        enemyGenerator.numberOfAnyEnemiesKilled += 1
        enemyGenerator.numberOfShootersKilled += 1
        explosion = Explosion(self.rect.center, 1.1)
        allSpritesGroup.add(explosion)
        self.kill()
    def update(self):
        # if int(self.position[0]) != int(self.shootPoint[0]) and  int(self.position[1]) != int(self.shootPoint[1]):
        #     self.moveToShootPoint()
        if abs(self.position[0] - self.shootPoint[0]) > 2 and abs(self.position[1] - self.shootPoint[1]) > 2:
            self.moveToShootPoint()
        pygame.draw.rect(screen, "red", self.rect, width=2)
        self.rotateToPlayer()
        if abs(self.position[0] - self.shootPoint[0]) <= self.distanceToSPToShoot and abs(self.position[1] - self.shootPoint[1]) <= self.distanceToSPToShoot:
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
    def die(self):
        enemyGenerator.currentNumberOfKamikazes -= 1
        enemyGenerator.numberOfAnyEnemiesKilled += 1
        enemyGenerator.numberOfKamikazesKilled += 1
        explosion = Explosion(self.rect.center, 1)
        allSpritesGroup.add(explosion)
        self.kill()
    def update(self):
        self.rotateAndMoveToPlayer()
        pygame.draw.rect(screen, "red", self.rect, width=2)

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, startPositionX, startPositionY, angle, speed, imageName, scale):
        super().__init__()
        self.startPositionX, self.startPositionY, self.angle = startPositionX, startPositionY, angle
        self.position = pygame.math.Vector2(self.startPositionX, self.startPositionY)
        self.image = pygame.image.load(f"./Sprites/{imageName}").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, scale)
        self.transparencyColor = self.image.get_at((0,0))
        self.image.set_colorkey(self.transparencyColor)
        self.rect = self.image.get_rect()
        self.rect.center = (self.position[0], self.position[1])
        self.speed = speed
        self.velocityY = math.sin(self.angle * (2 * math.pi / 360)) * self.speed
        self.velocityX = math.cos(self.angle * (2 * math.pi / 360)) * self.speed
    def move(self):
        self.position[0] += self.velocityX
        self.position[1] += self.velocityY

        self.rect.x, self.rect.y = self.position[0], self.position[1]
    def die(self):
        explosion = Explosion(self.rect.center, 1.2)
        allSpritesGroup.add(explosion)
        self.kill()
    def update(self):
        self.move()
        if self.position[0] < -1000:
            self.die()
        if self.position[0] > screenWidth + 1000:
            self.die()
        if self.position[1] < -1000:
            self.die()
        if self.position[1] > screenHeight + 1000:
            self.die()
        pygame.draw.rect(screen, "red", self.rect, width=2)

def writeSomething(fontstyle, fontsize, textContent, color, x, y, screen):
     font = pygame.font.SysFont(f"{fontstyle}", fontsize)
     text = font.render(f"{textContent}", True, color)
     screen.blit(text, [x, y])

def write_centered_text(fontstyle, fontsize, text_content, color, screen):
    font = pygame.font.SysFont(fontstyle, fontsize)
    text = font.render(text_content, True, color)
    text_rect = text.get_rect(center=(screenWidth // 2, screenHeight // 2))
    screen.blit(text, text_rect)

def checkIfPlayerGotHitByEnemies(playerGroup, enemiesGroup):
    collisions = pygame.sprite.groupcollide(enemiesGroup, playerGroup, False, False)
    if collisions: 
        player.getHit()
    

def checkIfPlayerGotHitByAsteroids(playerGroup, asteroidsGroup):
    collisions = pygame.sprite.groupcollide(asteroidsGroup, playerGroup, False, False)
    if collisions: 
        player.getHit()

def checkIfEnemiesGotHitByBullets(enemiesGroup, bulletsGroup):
    collisions = pygame.sprite.groupcollide(enemiesGroup, bulletsGroup, False, True)
    if collisions: 
        for enemy, bullet in collisions.items():
            enemyX, enemyY = enemy.position
            if ((enemyX >= 0 and enemyX <= screenWidth) and (enemyY >= 0 and enemyY <= screenWidth)):
                enemy.die()

def checkIfEnemiesGotHitByAsteroids(enemiesGroup, asteroidsGroup):
    collisions = pygame.sprite.groupcollide(enemiesGroup, asteroidsGroup, False, False)
    if collisions: 
        for enemy, asteroid in collisions.items():
            enemyX, enemyY = enemy.position
            if ((enemyX >= 0 and enemyX <= screenWidth) and (enemyY >= 0 and enemyY <= screenWidth)):
                enemy.die()

def checkIfAsteroidsGotHitByBullets(bulletsGroup, asteroidsGroup):
    collisions = pygame.sprite.groupcollide(bulletsGroup, asteroidsGroup, True, False)
    if collisions: 
        for bullet, asteroid in collisions.items():
            bullet.die()
            
def checkIfEnemiesGotHitByShields(shieldsGroup, enemiesGroup):
    collisions = pygame.sprite.groupcollide(shieldsGroup, enemiesGroup, False, False)
    if collisions:
        for shield, enemies in collisions.items():
            for enemy in enemies:
                enemy.die()

def checkIfAsteroidsGotHitByShields(shieldsGroup, asteroidsGroup):
    collisions = pygame.sprite.groupcollide(shieldsGroup, asteroidsGroup, False, False)
    if collisions:
        for shield, asteroids in collisions.items():
            for asteroid in asteroids:
                asteroid.die()



background = pygame.transform.scale(pygame.image.load("./Sprites/pexels-instawalli-176851.jpg").convert(), (screenWidth, screenHeight))

endTheGame = False
gameOver = False

player = Player()
# asteroid = Asteroid(10,200, 45, 1, "Asteroid1.png", 0.12)
enemyGenerator = EnemyGenerator()
allSpritesGroup = pygame.sprite.Group()
playerGroup = pygame.sprite.Group()
playerGroup.add(player)
bulletsGroup = pygame.sprite.Group()
enemiesGroup = pygame.sprite.Group()
asteroidsGroup = pygame.sprite.Group()
shieldsGroup = pygame.sprite.Group()
# asteroidsGroup.add(asteroid)
# allSpritesGroup.add(asteroid)
allSpritesGroup.add(player)

background = pygame.transform.scale(pygame.image.load("./Sprites/pexels-instawalli-176851.jpg").convert(), (screenWidth, screenHeight))
menuBackground = pygame.transform.scale(pygame.image.load("./Sprites/Capa Jogo.png").convert(), (screenWidth, screenHeight))

initTheGame = False
endTheGame = False
gameOver = False

def resetTheGame():
    global player, enemyGenerator, allSpritesGroup, playerGroup, bulletsGroup, enemiesGroup, asteroidsGroup, shieldsGroup
    player = Player()
    enemyGenerator = EnemyGenerator()
    player = Player()
    # asteroid = Asteroid(10,200, 45, 1, "Asteroid1.png", 0.12)
    enemyGenerator = EnemyGenerator()
    allSpritesGroup.empty()
    playerGroup.empty()
    playerGroup.add(player)
    bulletsGroup.empty()
    enemiesGroup.empty()
    asteroidsGroup.empty()
    shieldsGroup.empty()
    # asteroidsGroup.add(asteroid)
    # allSpritesGroup.add(asteroid)
    allSpritesGroup.add(player)



while not endTheGame:
    while not initTheGame and not endTheGame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                endTheGame = True
        
        screen.blit(menuBackground, (0,0))
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            initTheGame = True
        
        
        write_centered_text("Roboto", 72, 'Press "Space" to begin the game!', (255,255,255), screen)
        pygame.display.update()
        clock.tick(fps)
    while not gameOver and not endTheGame and initTheGame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                endTheGame = True
        print("Main game")
        screen.blit(background, (0,0))
        allSpritesGroup.draw(screen)
        allSpritesGroup.update()
        enemyGenerator.update()
        checkIfPlayerGotHitByEnemies(playerGroup, enemiesGroup)
        checkIfPlayerGotHitByAsteroids(playerGroup, asteroidsGroup)
        if player.endTheGame:
            gameOver = True
        checkIfEnemiesGotHitByBullets(enemiesGroup, bulletsGroup)
        checkIfEnemiesGotHitByAsteroids(enemiesGroup, asteroidsGroup)
        checkIfAsteroidsGotHitByBullets(bulletsGroup, asteroidsGroup)
        checkIfAsteroidsGotHitByShields(shieldsGroup, asteroidsGroup)
        checkIfEnemiesGotHitByShields(shieldsGroup, enemiesGroup)
        writeSomething("Roboto", 38, f"Enemies Destroyed: {enemyGenerator.numberOfAnyEnemiesKilled}", (255,255,255), 5,5, screen)
        if player.canShield():
            writeSomething("Roboto", 38, "Shields: Ready", (255,255,255), 5, screenHeight - 50, screen)
        elif player.shieldsOn:
            writeSomething("Roboto", 38, "Shields: On", (255,255,255), 5, screenHeight - 50, screen)
        elif player.canShield() == False:
            writeSomething("Roboto", 38, "Shields: Preparing", (255,255,255), 5, screenHeight - 50, screen)

        
        pygame.display.update()
        clock.tick(fps)
    
    while gameOver and not endTheGame:
        print("Game over")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                endTheGame = True
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_r]:
            resetTheGame()
            endTheGame = False
            gameOver = False    
        elif keys[pygame.K_ESCAPE]:
            endTheGame = True
        screen.fill((0,0,0))
        write_centered_text("Roboto", 72, "Game Over!", (255,255,255), screen)
        writeSomething("Roboto", 36, 'Press "r" to restart the game', (255,255,255), screenWidth - 350, screenHeight - 30, screen)
        writeSomething("Roboto", 36, 'Press "Esc" to exit the game', (255,255,255), 5, 5, screen)
        pygame.display.update()
        clock.tick(fps)
pygame.quit()