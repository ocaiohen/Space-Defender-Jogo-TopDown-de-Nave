import pygame
import math

pygame.init()
largura, altura = 1200, 800
screen = pygame.display.set_mode((largura, altura))
clock = pygame.time.Clock()
velocidadeDeAtualizacao = 15
running = True
tamanhoQuadrado = 40

class Jogador():
    def __init__(self) -> None:
        self.x = 50
        self.y = 200
        self.velocidadeX = 0
        self.velocidadeY = 0
        self.valorVelocidade = 1
    def verificarInput(self, teclas):
        if teclas[pygame.K_w]:
            self.velocidadeY -= self.valorVelocidade
        if teclas[pygame.K_s]:
            self.velocidadeY += self.valorVelocidade
        if teclas[pygame.K_d]:
            self.velocidadeX += self.valorVelocidade
        if teclas[pygame.K_a]:
            self.velocidadeX -= self.valorVelocidade
    def zerarVelocidades(self):
        self.velocidadeX = 0  # Zera a velocidade inicialmente
        self.velocidadeY = 0
    def normalizarVelocidade(self):
        if self.velocidadeX != 0 and self.velocidadeY != 0:
            self.velocidadeX /= math.sqrt(2)
            self.velocidadeY /= math.sqrt(2)
    def mover(self, velAtualizacao):    
        self.x += self.velocidadeX * velAtualizacao
        self.y += self.velocidadeY * velAtualizacao

def imprimirVelocidade(vX, vY):
    fonte = pygame.font.SysFont("Roboto", 35)
    texto = fonte.render(f"Vx = {vX}; Vy = {vY}", True, (255,255,255))
    screen.blit(texto, [largura/2, altura/2])

jogador = Jogador()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    teclas = pygame.key.get_pressed()

    jogador.zerarVelocidades()
    jogador.verificarInput(teclas)
    jogador.normalizarVelocidade()
    jogador.mover(velocidadeDeAtualizacao)

    screen.fill((154, 205, 50))  # Apaga o quadro atual
    
    # Lógica de jogo e renderização do novo quadro
    figura = pygame.Surface([tamanhoQuadrado, tamanhoQuadrado])  # Cria uma superfície quadrada com 30 pixels de lado
    figura.fill((252, 64, 0))  
    screen.blit(figura, (jogador.x, jogador.y))  # Desenha figura sobre o quadro atual nas coordenadas indicadas
    
    imprimirVelocidade(jogador.velocidadeX, jogador.velocidadeY)

    pygame.display.flip()  # Desenha o quadro atual na tela
    clock.tick(velocidadeDeAtualizacao)

pygame.quit()