import pygame
import sys
pygame.init()



def l2p2():
    ancho = 1400
    alto = 700
    ventana = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("minilevel limpio")

    global personaje_elegido
    jugador = Jugador(1282.29,359.04, 100, 120, con_gravedad=False,
                      personaje=personaje_elegido, ancho_max=ancho,
                      ancho_hitbox=60, alto_hitbox=100)

    fondo = pygame.image.load("imgs/f2.png")
    fondo = pygame.transform.scale(fondo, (ancho, alto))

    velocidad_y = 0
    gravedad = 1
    fuerza_salto = -18
    piso = 350
    en_suelo = True

    clock = pygame.time.Clock()

    objetos = [
        pygame.Rect(100, 350, 40, 40),
        pygame.Rect(600, 350, 40, 40),
        pygame.Rect(1000, 350, 40, 40)
    ]

    velocidades = [4, -3, 5]

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

        for i in range(len(objetos)):
            objetos[i].x += velocidades[i]
            if objetos[i].right >= ancho or objetos[i].left <= 0:
                velocidades[i] *= -1

        ventana.blit(fondo, (0, 0))
        jugador.dibujar(ventana)

        for obj in objetos:
            pygame.draw.rect(ventana, (255, 0, 0), obj)

        pygame.display.flip()
        clock.tick(60)
