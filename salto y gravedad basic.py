def l2p1():
    ancho = 1200
    alto = 700
    ventana = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("minilevel limpio")

    global personaje_elegido
    jugador = Jugador(486.86, 400, 100, 120, con_gravedad=False, personaje=personaje_elegido, ancho_max=ancho, ancho_hitbox=60, alto_hitbox=100)

    velocidad_y = 0
    gravedad = 1
    fuerza_salto = -18
    piso = 580
    en_suelo = True

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

        teclas = pygame.key.get_pressed()
        jugador.actualizar(teclas, paredes=0)

        jugador.rect.y += velocidad_y
        velocidad_y += gravedad

        if jugador.rect.y >= piso:
            jugador.rect.y = piso
            velocidad_y = 0
            en_suelo = True

        ventana.fill((0, 0, 0))
        jugador.dibujar(ventana)

        pygame.display.flip()
        clock.tick(60)
