import pygame
import sys
import subprocess

pygame.init()

def menulevels():
    ancho = 1200
    alto = 700
    ventana = pygame.display.set_mode((ancho,alto))
    pygame.display.set_caption("ml")

    botones_ancho , botones_alto = 300,100

    fondo = pygame.image.load("menulevels.jpg")
    fondo = pygame.transform.scale(fondo,(ancho,alto))

    boton_level1 =pygame.image.load("boton level1.png")
    boton_level1 =pygame.transform.scale(boton_level1,(botones_ancho,botones_alto))

    botonl1 = pygame.Rect(450,100,botones_ancho,botones_alto)

    x1 = 0
    x2 = ancho
    velocidad = 2 

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if botonl1.collidepoint(event.pos):
                    pygame.quit()
                    subprocess.run(["python","l1.py"])
                    sys.exit()
                    
        x1 -= velocidad
        x2 -= velocidad
        if x1 <= -ancho:
            x1 = x2 + ancho
        if x2 <= -ancho:
            x2 = x1 + ancho
        
        ventana.blit(fondo,(x1,0))
        ventana.blit(fondo,(x2,0))
        ventana.blit(boton_level1,(botonl1.x,botonl1.y))
        pygame.display.flip()
        clock.tick(60)
        
    pygame.quit()
    sys.exit()

def mainlevel():
    ancho = 1200
    alto = 700
    ancho_botones=300
    alto_botones=100

    ventana = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("integrador equpo 6")

    fondo = pygame.image.load("img.jpg")
    fondo = pygame.transform.scale(fondo, (ancho, alto))
    botones= pygame.image.load("boton inicio.png")
    botones= pygame.transform.scale(botones,(ancho_botones,alto_botones))
    configuracion =pygame.image.load("boton configuracion.png")
    configuracion = pygame.transform.scale(configuracion,(ancho_botones,alto_botones))

    boton_inicio_rect = pygame.Rect(450,300,ancho_botones,alto_botones)

    x1 = 0
    x2 = ancho
    velocidad = 2 
    reloj = pygame.time.Clock()
    ejecutar = True

    while ejecutar:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejecutar = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
                if boton_inicio_rect.collidepoint(event.pos):  
                    menulevels()   

        x1 -= velocidad
        x2 -= velocidad

        if x1 <= -ancho:
            x1 = x2 + ancho
        if x2 <= -ancho:
            x2 = x1 + ancho

        ventana.blit(fondo, (x1, 0))
        ventana.blit(fondo, (x2, 0))
        ventana.blit(botones,(450,300))
        ventana.blit(configuracion,(450,450))

        pygame.display.flip()
        reloj.tick(60)  

    pygame.quit()
    sys.exit()
    
mainlevel()
