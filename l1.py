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
imagen_jugador=pygame.image.load("l1/personaje.png")
imagen_jugador=pygame.transform.scale(imagen_jugador,(20,20))

fondo = pygame.image.load("l1/fondolevel1.png")
fondo=pygame.transform.scale(fondo,(ancho,alto))

pared = [
    pygame.Rect(370,513,517,6),
    pygame.Rect(0,513,300,6),
    pygame.Rect(944,513,250,7),
    pygame.Rect(399,450,480,8),
    pygame.Rect(399,280,90,8),
    pygame.Rect(596,280,287 ,8),
    pygame.Rect(428,225,359,8),
    pygame.Rect(370,513,517,6),
    pygame.Rect(370,80,900,6),
    pygame.Rect(370,80,900,6),
    
    
    
        
]

white = (255,255,255)



red=(255,0,0)
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    x_anterior , y_anterior = jugador.x, jugador.y
    
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and jugador.left >0:
        jugador.x -= velocidad_jugador
    if teclas[pygame.K_RIGHT] and jugador.right <ancho:
        jugador.x += velocidad_jugador
    if teclas[pygame.K_UP] and jugador.top >0:
        jugador.y -= velocidad_jugador
    if teclas[pygame.K_DOWN] and jugador.bottom <alto:
        jugador.y += velocidad_jugador  
        
        
    for p in pared:
        if jugador.colliderect(p):
            jugador.x, jugador.y = x_anterior, y_anterior    
    
    ventana.fill((0,0,0))
    ventana.blit(fondo,(0,0))
    ventana.blit(imagen_jugador,(jugador.x,jugador.y))
    for p in pared:
        pygame.draw.rect(ventana,white,p)
        
 
    pygame.display.flip()
    
    clock.tick(60)
  
    
    