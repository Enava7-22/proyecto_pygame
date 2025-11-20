import pygame
pygame.init()

def game():
    ANCHO_WIN, ALTO_WIN = 1400, 800

    ventana = pygame.display.set_mode((ANCHO_WIN, ALTO_WIN))
    fondo = pygame.image.load("imgs/f.png").convert()

    ANCHO_MAPA, ALTO_MAPA = fondo.get_width(), fondo.get_height()

    jugador = pygame.Rect(200, 200, 50, 70)
    vel = 10

    clock = pygame.time.Clock()
    run = True
    
    while run:
        clock.tick(60)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            jugador.x -= vel
        if keys[pygame.K_RIGHT]:
            jugador.x += vel
        if keys[pygame.K_UP]:
            jugador.y -= vel
        if keys[pygame.K_DOWN]:
            jugador.y += vel

        jugador.x = max(0, min(jugador.x, ANCHO_MAPA - jugador.width))
        jugador.y = max(0, min(jugador.y, ALTO_MAPA - jugador.height))

        cam_x = jugador.x - ANCHO_WIN // 2
        cam_y = jugador.y - ALTO_WIN // 2

        cam_x = max(0, min(cam_x, ANCHO_MAPA - ANCHO_WIN))
        cam_y = max(0, min(cam_y, ALTO_MAPA - ALTO_WIN))

        ventana.blit(fondo, (-cam_x, -cam_y))
        pygame.draw.rect(ventana, (255, 0, 0),(jugador.x - cam_x, jugador.y - cam_y, jugador.width, jugador.height))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()

game()
