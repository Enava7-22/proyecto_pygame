import pygame
import sys
import random
pygame.init()


def level1():
    
    ancho = 1200
    alto = 700
    ventana = pygame.display.set_mode((ancho,alto))
    pygame.display.set_caption("julioxromario")
    black = (0,0,0)
    white = (255,255,255)
    fondo = pygame.image.load("nuevo mapa.png")
    fondo = pygame.transform.scale(fondo,(ancho,alto))
    
    personaje = pygame.Rect(600,600,60,90)
    velocidad = 15
    
    imagen_jugador=pygame.image.load("personaje.png")
    imagen_jugador=pygame.transform.scale(imagen_jugador,(personaje.width,personaje.height))
    
    pared = [
    pygame.Rect(16, 172, 384, 15),
    pygame.Rect(15, 440, 242, 15),
    pygame.Rect(700, 171, 246, 15),
    pygame.Rect(1080, 165, 108, 15),
    pygame.Rect(380, 439, 17, 247),
    pygame.Rect(992, 438, 110, 15),
    pygame.Rect(580, 19, 20, 168),
    pygame.Rect(926, 15, 20, 168),
    pygame.Rect(992, 452, 20, 230)
    ]

    puerta1 = pygame.Rect(1100,450,80,40)
    puerta2 = pygame.Rect(260,450,120,40)
    puerta3 = pygame.Rect(400,130,180,40)
    puerta4 = pygame.Rect(606,130,90,40)
    puerta5 = pygame.Rect(950,130,130,40)

    red =(255,0,0)

    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        x_anterior, y_anterior = personaje.x, personaje.y                   
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and personaje.left >0:
            personaje.x -= velocidad
        if teclas[pygame.K_RIGHT] and personaje.right <ancho:
            personaje.x += velocidad  
        if teclas[pygame.K_UP] and personaje.top >0:
            personaje.y -= velocidad
        if teclas[pygame.K_DOWN] and personaje.bottom <alto:
            personaje.y += velocidad  
            
        for p in pared:
            if personaje.colliderect(p):
                personaje.x, personaje.y = x_anterior, y_anterior
        
        
        if personaje.colliderect(puerta1):
            level2()
            return
        if personaje.colliderect(puerta2):
            level2()
            return
        if personaje.colliderect(puerta3):
            level2()
            return
        if personaje.colliderect(puerta4):
            level2()
            return
        if personaje.colliderect(puerta5):
            level2()
            return
         
             
             
        ventana.blit(fondo,(0,0))
        #pygame.draw.rect(ventana,white,personaje)
        #pygame.draw.rect(ventana,red,puerta1)
        #pygame.draw.rect(ventana,red,puerta2)
        #pygame.draw.rect(ventana,red,puerta3)
        #pygame.draw.rect(ventana,red,puerta4)
        #pygame.draw.rect(ventana,red,puerta5)
        #for p in pared:
            #pygame.draw.rect(ventana,red,p)
        ventana.blit(imagen_jugador,(personaje.x,personaje.y))
        pygame.display.flip()
        clock.tick(60)
    
def level2():

    ancho = 1200
    alto = 700
    ventana = pygame.display.set_mode((ancho,alto))
    pygame.display.set_caption("minilevel2")

    personaje = pygame.Rect(600,600,60,90)
    velocidad = 20
    
    imagen_jugador=pygame.image.load("personaje.png")
    imagen_jugador=pygame.transform.scale(imagen_jugador,(personaje.width,personaje.height))
    
    white = (255,255,255)
    
    obstaculo = pygame.Rect(100,100,40,40)
    red =(255,0,0)
    
    fondo = pygame.image.load("l2img.png").convert()
    fondo = pygame.transform.scale(fondo,(ancho,alto))
    
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and personaje.left >0:
            personaje.x -= velocidad
        if teclas[pygame.K_RIGHT] and personaje.right <ancho:
            personaje.x += velocidad  
        if teclas[pygame.K_UP] and personaje.top >0:
            personaje.y -= velocidad
        if teclas[pygame.K_DOWN] and personaje.bottom <alto:
            personaje.y += velocidad   
        
        if personaje.colliderect(obstaculo):
            print("puto")
            level1()
            return   
        
        ventana.fill((0,0,0))
        ventana.blit(fondo,(0,0))
        pygame.draw.rect(ventana,red,obstaculo)
        ventana.blit(imagen_jugador,(personaje.x,personaje.y))
        pygame.display.flip()
        clock.tick(60)
   
level1()
       