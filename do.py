import pygame
import sys

pygame.init()

class Jugador:
    def __init__(self, x, y, w, h):
        self.image = pygame.Surface((w, h))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocidad = 8
        self.vy = 0
        self.en_suelo = False

    def actualizar(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocidad
        if keys[pygame.K_SPACE] and self.en_suelo:
            self.vy = -20
            self.en_suelo = False

        self.vy += 1
        self.rect.y += self.vy
        if self.rect.y >= 600:
            self.rect.y = 600
            self.vy = 0
            self.en_suelo = True


def nivel_scroll():
    ancho_ventana = 1400
    alto_ventana = 800
    ventana = pygame.display.set_mode((ancho_ventana, alto_ventana))

    fondo = pygame.image.load("imgs/fondo largo.png").convert()
    ancho_fondo = fondo.get_width()

    jugador = Jugador(200, 600, 80, 120)

    scroll_x = 0

    reloj = pygame.time.Clock()
    run = True

    while run:
        reloj.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        jugador.actualizar()

        if jugador.rect.centerx > ancho_ventana // 2 and scroll_x > -(ancho_fondo - ancho_ventana):
            scroll_x -= jugador.velocidad
        elif jugador.rect.centerx < ancho_ventana // 2 and scroll_x < 0:
            scroll_x += jugador.velocidad

        ventana.blit(fondo, (scroll_x, 0))
        ventana.blit(jugador.image, jugador.rect)

        pygame.display.update()


nivel_scroll()
