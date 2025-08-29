import pygame
import sys
import random

pygame.init()

# Configuración de la pantalla
ancho =1200
alto = 700

ventana = pygame.display.set_mode((ancho,alto))
pygame.display.set_caption("1d integrador")

# jugador
jugador = pygame.Rect(50,50,120,120)
velocidad_jugador = 8
red =(255,0,0)

clock = pygame.time.Clock()

#bucle principal
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done =True
            
    # movimien       
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and jugador.left >0:
        jugador.x -= velocidad_jugador
    if teclas[pygame.K_RIGHT] and jugador.right <ancho:
        jugador.x +=velocidad_jugador
    if teclas[pygame.K_UP] and jugador.top >0:
        jugador.y -= velocidad_jugador
    if teclas[pygame.K_DOWN] and jugador.bottom <alto:
        jugador.y +=velocidad_jugador
        
        
    #movimiento con wasd
    if teclas[pygame.K_a] and velocidad_jugador >0:
        jugador.x -= velocidad_jugador
    if teclas[pygame.K_d] and jugador.right <ancho:     
        jugador.x +=velocidad_jugador                       
    if teclas[pygame.K_w] and jugador.top >0:
        jugador.y -= velocidad_jugador
    if teclas[pygame.K_s] and jugador.bottom <alto:
        jugador.y += velocidad_jugador
        
        
        
        
    ventana.fill((0,0,0))
    pygame.draw.rect(ventana,red,jugador)
    
    pygame.display.update()
    clock.tick(60)


pygame.quit()