import pygame
import sys

pygame.init()

def l1p2():
    ANCHO_VENTANA = 1400
    ALTO_VENTANA = 800
    ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("minilevel con scroll, gravedad y salto")  

    fondo = pygame.image.load("imgs/f.png").convert()
    ANCHO_MAPA, ALTO_MAPA = fondo.get_width(), fondo.get_height()

    jugador = pygame.Rect(75, 505, 50, 100)
    color_jugador = (255, 0, 0)
    velocidad_x = 17
    gravedad = 1
    salto_vel = 20
    velocidad_y = 0
    en_suelo = False

    clock = pygame.time.Clock()
    cam_x = 0
    cam_y = 0
    suelo_y = ALTO_MAPA - 100

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            jugador.x -= velocidad_x
        if teclas[pygame.K_RIGHT]:
            jugador.x += velocidad_x
        if teclas[pygame.K_UP] and en_suelo:
            velocidad_y = -salto_vel
            en_suelo = False
        if teclas[pygame.K_SPACE] and en_suelo:
            velocidad_y = -salto_vel
            en_suelo = False

        velocidad_y += gravedad
        jugador.y += velocidad_y

        if jugador.y + jugador.height >= suelo_y:
            jugador.y = suelo_y - jugador.height
            velocidad_y = 0
            en_suelo = True

        jugador.x = max(0, min(jugador.x, ANCHO_MAPA - jugador.width))
        cam_x = jugador.x - ANCHO_VENTANA // 2
        cam_y = jugador.y - ALTO_VENTANA // 2
        cam_x = max(0, min(cam_x, ANCHO_MAPA - ANCHO_VENTANA))
        cam_y = max(0, min(cam_y, ALTO_MAPA - ALTO_VENTANA))

        ventana.blit(fondo, (-cam_x, -cam_y))
        pygame.draw.rect(ventana, color_jugador, 
                         pygame.Rect(jugador.x - cam_x, jugador.y - cam_y, jugador.width, jugador.height))

        pygame.display.flip()
        clock.tick(60)

l1p2()
