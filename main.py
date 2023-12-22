import pygame
import math

pygame.init()

screenWidth = 1280
screenHeight = 720
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.playerSize = 0.1
        self.playerPosition = pygame.math.Vector2(0, 200)
        self.image = pygame.transform.rotozoom(pygame.image.load("./Sprites/Esboço nave girada pro lado.png").convert_alpha(), 0, self.playerSize)
        self.image.set_colorkey((255, 255, 255))
        self.baseImage = self.image
        self.rect = self.image.get_rect(center=self.playerPosition)
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

    def move(self):
        self.playerPosition += pygame.math.Vector2(self.velocityX, self.velocityY)
        self.rect.center = self.playerPosition  # Atualizar o centro do retângulo com a nova posição

    def playerRotation(self):
        self.mouseCoordinates = pygame.mouse.get_pos()
        self.deltaX = (self.mouseCoordinates[0] - self.rect.centerx)
        self.deltaY = (self.mouseCoordinates[1] - self.rect.centery)
        self.angle = math.degrees(math.atan2(-self.deltaY, self.deltaX))
        self.image = pygame.transform.rotate(self.baseImage, self.angle)
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect(center=self.rect.center)  # Manter o centro do retângulo após a rotação

    def update(self):
        self.userInput()
        self.move()
        self.playerRotation()

player = Player()

endTheGame = False
while not endTheGame:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            endTheGame = True

    screen.fill((0, 0, 0))
    screen.blit(player.image, player.rect)
    player.update()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
