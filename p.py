import pygame
import sys
import random

pygame.init()
ancho = 1200
alto = 700


def juego_nivel1():
    ventana_nivel = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("first level")
    
    fondo = pygame.image.load("fondolevel1.png")
    fondo = pygame.transform.scale(fondo, (ancho, alto))
    
    jugador = pygame.Rect(560, alto // 2, 40, 70)
    velocidad_jugador = 5
    imagen_jugador=pygame.image.load("personaje.png")
    imagen_jugador=pygame.transform.scale(imagen_jugador,(jugador.width,jugador.height))
    red = (255, 0, 0)
    
    clock = pygame.time.Clock()
    
    ejecutar_nivel = True
    while ejecutar_nivel:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and jugador.left > 0:
            jugador.x -= velocidad_jugador
        if teclas[pygame.K_RIGHT] and jugador.right < ancho:
            jugador.x += velocidad_jugador
        if teclas[pygame.K_UP] and jugador.top > 0:
            jugador.y -= velocidad_jugador
        if teclas[pygame.K_DOWN] and jugador.bottom < alto:
            jugador.y += velocidad_jugador  

        ventana_nivel.fill((0, 0, 0))
        ventana_nivel.blit(fondo, (0, 0))
        ventana.blit(imagen_jugador,(jugador.x,jugador.y))
        pygame.display.flip()
        clock.tick(60)


ventana = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("integrador equipo 6")

fondo_menu = pygame.image.load("img.jpg")
fondo_menu = pygame.transform.scale(fondo_menu, (ancho, alto))

ancho_botones = 300
alto_botones = 100

boton_inicio_img = pygame.image.load("boton inicio.png")
boton_inicio_img = pygame.transform.scale(boton_inicio_img, (ancho_botones, alto_botones))
boton_config_img = pygame.image.load("boton configuracion.png")
boton_config_img = pygame.transform.scale(boton_config_img, (ancho_botones, alto_botones))


boton_inicio_rect = pygame.Rect(450, 300, ancho_botones, alto_botones)
boton_config_rect = pygame.Rect(450, 450, ancho_botones, alto_botones)

x1 = 0
x2 = ancho
velocidad = 2

reloj = pygame.time.Clock()
ejecutar = True

while ejecutar:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecutar = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if boton_inicio_rect.collidepoint(mouse_pos):
                juego_nivel1()
            if boton_config_rect.collidepoint(mouse_pos):
                print("Botón CONFIGURACIÓN presionado")

 
    x1 -= velocidad
    x2 -= velocidad
    if x1 <= -ancho:
        x1 = x2 + ancho
    if x2 <= -ancho:
        x2 = x1 + ancho

    ventana.blit(fondo_menu, (x1, 0))
    ventana.blit(fondo_menu, (x2, 0))
    ventana.blit(boton_inicio_img, (boton_inicio_rect.x, boton_inicio_rect.y))
    ventana.blit(boton_config_img, (boton_config_rect.x, boton_config_rect.y))

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()
