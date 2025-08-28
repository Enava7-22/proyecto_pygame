import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
ANCHO, LARGO = 1100, 800
pantalla = pygame.display.set_mode((ANCHO, LARGO))
pygame.display.set_caption('no se: Abrasos no balasos')

#colores
VERDE = (34, 139, 34)
AZUL = (220, 112, 255)

# Configuración del jugador
jugador_pos = [ANCHO // 15, LARGO // 2]
jugador_radio = 30
velocidad = 2

# Bucle principal del juego

# configurar enemigos
enemigos = []
enemigos_radio = 20
enemigos_color = (255, 0, 0)
enemigo_velocidad = 3

# crear enemigos en posiciones aleatorias
import random
for _ in range(5):
    x = random.randint(ANCHO // 2, ANCHO - enemigos_radio)
    y = random.randint(-800, -50)
    enemigos.append([x, y])




while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
#  mover jugador           
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        jugador_pos[0] -= velocidad
    if teclas[pygame.K_RIGHT]:
        jugador_pos[0] += velocidad
    if teclas[pygame.K_UP]:
        jugador_pos[1] -= velocidad
    if teclas[pygame.K_DOWN]:
        jugador_pos[1] += velocidad
        
    # wasd
    if teclas[pygame.K_a]:
        jugador_pos[0] -= velocidad
    if teclas[pygame.K_d]:
        jugador_pos[0] += velocidad 
    if teclas[pygame.K_w]:
        jugador_pos[1] -= velocidad
    if teclas[pygame.K_s]:
        jugador_pos[1] += velocidad   
        
        
    # limites de pantalla
    jugador_pos[0] = max(jugador_radio, min(ANCHO - jugador_radio, jugador_pos[0]))
    jugador_pos[1] = max(jugador_radio, min(LARGO - jugador_radio, jugador_pos[1]))
    
    # mover y dibujar enemigos
    for enemigo in enemigos:
        enemigo[1] += enemigo_velocidad
        # si el enemigo sale de la pantalla, reubicarlo arriba
        if enemigo[1] > LARGO + enemigos_radio:
            enemigo[0] = random.randint(enemigos_radio, ANCHO - enemigos_radio)
            enemigo[1] = random.randint(-800, -50)
        pygame.draw.circle
        
    # dibujar fondo y jugador
    pantalla.fill(VERDE)
    pygame.draw.circle(pantalla, AZUL, jugador_pos, jugador_radio)
    pygame.display.flip()
    
    
    
    
    