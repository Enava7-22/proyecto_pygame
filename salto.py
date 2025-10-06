import random
import pygame
import sys

pygame.init()

def level4():
    
    ancho = 1200
    alto = 700
    ventana = pygame.display.set_mode((ancho,alto))
    pygame.display.set_caption("minilevel 2")

    jugador = pygame.Rect(600,600,30,30)
    color_jugador = (255,255,255)
    velocidad = 15
    
   
   
    

    
    velocidad_jugador = 15
    velocidad_y = 0
    gravedad = 1
    fuerza_salto = -15
    en_suelo = True
    suelo_y = 690

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and en_suelo:
                    velocidad_y = fuerza_salto
                    en_suelo = False 
        velocidad_y += gravedad
        jugador.y += velocidad_y
        if jugador.y >= suelo_y - jugador.height:
            jugador.y = suelo_y - jugador.height
            velocidad_y = 0
            en_suelo = True   
    
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and jugador.left >0:
            jugador.x -= velocidad   
        if teclas[pygame.K_RIGHT] and jugador.right <ancho:
            jugador.x += velocidad 
        if teclas[pygame.K_UP] and jugador.top >0:
            jugador.y -= velocidad
        if teclas[pygame.K_DOWN] and jugador.bottom <alto:
            jugador.y += velocidad
    
                        
        ventana.fill((0,0,0))
        pygame.draw.rect(ventana,color_jugador,jugador) 
        
        
        pygame.display.flip()
        
        clock.tick(60)

    pygame.quit
    sys.exit
level4()


