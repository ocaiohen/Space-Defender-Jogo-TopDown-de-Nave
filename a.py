import pygame
import sys
import math

pygame.init()

largura_tela = 800
altura_tela = 600

tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption('Inimigo Seguindo o Personagem')

branco = (255, 255, 255)
vermelho = (255, 0, 0)

# Personagem
x_personagem = largura_tela // 2
y_personagem = altura_tela // 2
tamanho_personagem = 30
velocidade_personagem = 5

# Inimigo
x_inimigo = 100
y_inimigo = 100
tamanho_inimigo = 30
velocidade_inimigo = 2

clock = pygame.time.Clock()

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    teclas = pygame.key.get_pressed()

    # Mover o personagem
    if teclas[pygame.K_w]:
        y_personagem -= velocidade_personagem
    if teclas[pygame.K_s]:
        y_personagem += velocidade_personagem
    if teclas[pygame.K_a]:
        x_personagem -= velocidade_personagem
    if teclas[pygame.K_d]:
        x_personagem += velocidade_personagem

    # Mover o inimigo em direção ao personagem
    direcao_x = x_personagem - x_inimigo #cateto adjacente
    direcao_y = y_personagem - y_inimigo #cateto oposto
    distancia = math.sqrt(direcao_x**2 + direcao_y**2) #hipotenusa

    if distancia != 0:
        direcao_x /= distancia #cosseno
        direcao_y /= distancia #seno

    x_inimigo += direcao_x * velocidade_inimigo
    y_inimigo += direcao_y * velocidade_inimigo

    tela.fill(branco)

    # Desenhar o personagem
    pygame.draw.rect(tela, vermelho, (x_personagem, y_personagem, tamanho_personagem, tamanho_personagem))

    # Desenhar o inimigo
    pygame.draw.rect(tela, vermelho, (x_inimigo, y_inimigo, tamanho_inimigo, tamanho_inimigo))

    pygame.display.flip()
    clock.tick(60)
