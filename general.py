import pygame
import sys
import random

pygame.init()


ancho =1200
alto = 700

ventana = pygame.display.set_mode((ancho,alto))
pygame.display.set_caption("1d integrador")


jugador = pygame.Rect(50,50,120,120)
velocidad_jugador = 7
red =(255,0,0)




clock = pygame.time.Clock()

done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done =True
            
            
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and jugador.left >0:
        jugador.x -= velocidad_jugador
    if teclas[pygame.K_RIGHT] and jugador.right <ancho:
        jugador.x +=velocidad_jugador
    if teclas[pygame.K_UP] and jugador.top >0:
        jugador.y -= velocidad_jugador
    if teclas[pygame.K_DOWN] and jugador.bottom <alto:
        jugador.y +=velocidad_jugador
    
    ventana.fill((0,0,0))
    pygame.draw.rect(ventana,red,jugador)
    
    pygame.display.update()
    clock.tick(60)


pygame.quit()