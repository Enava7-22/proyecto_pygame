import pygame
pygame.init()

def game():
    ANCHO_WIN, ALTO_WIN = 1400, 800
    ventana = pygame.display.set_mode((ANCHO_WIN, ALTO_WIN))
    pygame.display.set_caption("Juego con objetos en fila separados")

    fondo = pygame.image.load("imgs/f2.png").convert()
    ANCHO_MAPA, ALTO_MAPA = fondo.get_width(), fondo.get_height()

    jugador = pygame.Rect(2854, 551, 50, 70)
    vel = 10

    vel_y = 0
    gravedad = 1
    saltando = False
    fuerza_salto = -20

    suelo = 600

    objetos = []  
    frame_counter = 0
    frame_aparicion = 60
    separacion_horizontal = 60

    clock = pygame.time.Clock()
    run = True
    
    contador_daño = 0
    
    
    while run:
        clock.tick(60)
        frame_counter += 1
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            jugador.x -= vel
        if keys[pygame.K_RIGHT]:
            jugador.x += vel
        if keys[pygame.K_SPACE] and not saltando:
            vel_y = fuerza_salto
            saltando = True

        vel_y += gravedad
        jugador.y += vel_y
        
        if jugador

        if jugador.y + jugador.height >= suelo:
            jugador.y = suelo - jugador.height
            vel_y = 0
            saltando = False

        jugador.x = max(0, min(jugador.x, ANCHO_MAPA - jugador.width))
        jugador.y = max(0, min(jugador.y, ALTO_MAPA - jugador.height))

        if jugador.x >= 600 and frame_counter >= frame_aparicion:
            for i in range(5):
                obj_x = 600 + i * separacion_horizontal
                obj_y = 521
                obj = pygame.Rect(obj_x, obj_y, 50, 50)
                objetos.append(obj)
            frame_counter = 0

        for obj in objetos[:]:
            obj.x += 10
            if obj.x > ANCHO_MAPA:
                objetos.remove(obj)

        cam_x = jugador.x - ANCHO_WIN // 2
        cam_y = jugador.y - ALTO_WIN // 2
        cam_x = max(0, min(cam_x, ANCHO_MAPA - ANCHO_WIN))
        cam_y = max(0, min(cam_y, ALTO_MAPA - ALTO_WIN))

        ventana.blit(fondo, (-cam_x, -cam_y))
        pygame.draw.rect(ventana, (255, 0, 0), (jugador.x - cam_x, jugador.y - cam_y, jugador.width, jugador.height))
        for obj in objetos:
            pygame.draw.rect(ventana, (0, 255, 0), (obj.x - cam_x, obj.y - cam_y, obj.width, obj.height))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
        print(contador_daño)

    pygame.quit()

game()
