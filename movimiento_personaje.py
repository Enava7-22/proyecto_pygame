def jugar_nivel(fondo_img, frames_derecha, frames_izquierda, pos_inicial=(560, 350)):
    ventana_nivel = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Nivel")
    
    fondo = pygame.image.load(fondo_img)
    fondo = pygame.transform.scale(fondo, (ancho, alto))
    
    ancho_jugador, alto_jugador = 70, 100
    jugador = pygame.Rect(pos_inicial[0], pos_inicial[1], ancho_jugador, alto_jugador)

    frames_derecha = [pygame.transform.scale(img, (ancho_jugador, alto_jugador)) for img in frames_derecha]
    frames_izquierda = [pygame.transform.scale(img, (ancho_jugador, alto_jugador)) for img in frames_izquierda]

    frame_index = 0
    contador = 0
    tiempo_animacion = 8
    direccion = "derecha"

    clock = pygame.time.Clock()
    ejecutar_nivel = True
    
    while ejecutar_nivel:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        teclas = pygame.key.get_pressed()
        moviendo = False

        if teclas[pygame.K_LEFT] and jugador.left > 0:
            jugador.x -= 10
            moviendo = True
            direccion = "izquierda"
        if teclas[pygame.K_RIGHT] and jugador.right < ancho:
            jugador.x += 10
            moviendo = True
            direccion = "derecha"
        if teclas[pygame.K_UP] and jugador.top > 0:
            jugador.y -= 10
            moviendo = True
        if teclas[pygame.K_DOWN] and jugador.bottom < alto:
            jugador.y += 10
            moviendo = True

        # Animación
        if moviendo:
            contador += 1
            if contador >= tiempo_animacion:
                contador = 0
                frame_index = (frame_index + 1) % 4
            imagen_jugador = frames_derecha[frame_index] if direccion == "derecha" else frames_izquierda[frame_index]
        else:
            imagen_jugador = frames_derecha[0] if direccion == "derecha" else frames_izquierda[0]

        # Dibujar
        ventana_nivel.blit(fondo, (0, 0))
        ventana_nivel.blit(imagen_jugador, (jugador.x, jugador.y))
        pygame.display.flip()
        clock.tick(60)
        
        # Cargar frames del jugador
        frame1 = pygame.image.load("frame1.png").convert_alpha()
        frame2 = pygame.image.load("frame2.png").convert_alpha()
        frame3 = pygame.image.load("frame3.png").convert_alpha()

        frame1_left = pygame.transform.flip(frame1, True, False)
        frame2_left = pygame.transform.flip(frame2, True, False)
        frame3_left = pygame.transform.flip(frame3, True, False)

        frames_derecha = [frame1, frame2, frame1, frame3]
        frames_izquierda = [frame1_left, frame2_left, frame1_left, frame3_left]

        # Fondo en movimiento
        x1 = 0
        x2 = ancho
        velocidad = 2

        reloj = pygame.time.Clock()
        ejecutar = True