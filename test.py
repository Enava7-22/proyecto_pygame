import pygame
import random
import sys

pygame.init()

ancho = 800
alto = 500
ventana = pygame.display.set_mode((ancho, alto))
clock = pygame.time.Clock()

objetos = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if random.randint(0, 20) == 0:
        x = random.randint(0, ancho - 30)
        rect = pygame.Rect(x, 0, 30, 30)
        objetos.append(rect)

    ventana.fill((0, 0, 0))

    for rect in objetos:
        rect.y += 5
        pygame.draw.rect(ventana, (255, 0, 0), rect)

    pygame.display.update()
    clock.tick(60)
