import pygame
import random
import sys

pygame.init()

ancho = 1200
alto =700

ventana = pygame.display.set_mode((ancho,alto))
pygame.display.set_caption("first level")
jugador = pygame.Rect(560,alto//2,40,70)
velocidad_jugador= 10
imagen_jugador=pygame.image.load("level1picture/personaje.png")
imagen_jugador=pygame.transform.scale(imagen_jugador,(jugador.width,jugador.height))

fondo = pygame.image.load("level1picture/fondolevel1.png")
fondo=pygame.transform.scale(fondo,(ancho,alto))



red=(255,0,0)
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and jugador.left >0:
        jugador.x -= velocidad_jugador
    if teclas[pygame.K_RIGHT] and jugador.right <ancho:
        jugador.x += velocidad_jugador
    if teclas[pygame.K_UP] and jugador.top >0:
        jugador.y -= velocidad_jugador
    if teclas[pygame.K_DOWN] and jugador.bottom <alto:
        jugador.y += velocidad_jugador  
    
    ventana.fill((0,0,0))
    ventana.blit(fondo,(0,0))
    ventana.blit(imagen_jugador,(jugador.x,jugador.y))
 
    pygame.display.flip()
    
    clock.tick(60)
  
    
    