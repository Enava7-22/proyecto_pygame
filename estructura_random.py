import random
import pygame
import sys

pygame.init()

def videojuego():
    
    ancho = 1200
    alto = 700
    ventana = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("minilevel 2")

    img_jugador = pygame.image.load("imgs/player.png")
    img_jugador = pygame.transform.scale(img_jugador, (60, 80))
    jugador = img_jugador.get_rect(center=(600, 600))

    misil_img = pygame.image.load("imgs/misil.png")
    misil_img = pygame.transform.scale(misil_img, (30, 70))

    velocidad = 15

    velocidad_y = 0
    gravedad = 1
    fuerza_salto = -15
    en_suelo = True
    suelo_y = 690

    objetos = []

  
    daño = 0
    fuente = pygame.font.SysFont(None, 40)

    tiempo_inicio = pygame.time.get_ticks()  # milisegundos
    # --------------------------------

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
        if teclas[pygame.K_LEFT] and jugador.left > 0:
            jugador.x -= velocidad   
        if teclas[pygame.K_RIGHT] and jugador.right < ancho:
            jugador.x += velocidad 

        if teclas[pygame.K_UP] and jugador.top > 0:
            jugador.y -= velocidad
        if teclas[pygame.K_DOWN] and jugador.bottom < alto:
            jugador.y += velocidad

        if random.randint(0, 20) == 0:
            x = random.randint(0, ancho - 30)
            rect = misil_img.get_rect(topleft=(x, 0))
            objetos.append(rect)
            
        ventana.fill((0, 0, 0))
        ventana.blit(img_jugador, jugador)

        # ----- MOSTRAR DAÑO -----
        texto_daño = fuente.render(f"Daño: {daño}%", True, (255, 255, 255))
        ventana.blit(texto_daño, (20, 20))

        # ----- CALCULAR SEGUNDOS -----
        tiempo_actual = pygame.time.get_ticks()
        segundos = (tiempo_actual - tiempo_inicio) // 1000

        texto_tiempo = fuente.render(f"Tiempo: {segundos}s", True, (255, 255, 255))
        ventana.blit(texto_tiempo, (20, 60))
        # --------------------------------

        for obj in objetos[:]:
            obj.y += 5
            ventana.blit(misil_img, obj)

            if jugador.colliderect(obj):
                objetos.remove(obj)
                daño += 20
                if daño > 100:
                    daño = 100

            if obj.top > alto:
                objetos.remove(obj)

        pygame.display.flip()
        clock.tick(60)

videojuego()
