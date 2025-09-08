import pygame
import sys

pygame.init()
ancho = 1200
alto = 700

ancho_botones=300
alto_botones=100

ventana = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("integrador equpo 6")


fondo = pygame.image.load("menupic/img.jpg")
fondo = pygame.transform.scale(fondo, (ancho, alto))
botones= pygame.image.load("menupic/boton inicio.png")
botones= pygame.transform.scale(botones,(ancho_botones,alto_botones))
configuracion =pygame.image.load("menupic/boton configuracion.png")
configuracion = pygame.transform.scale(configuracion,(ancho_botones,alto_botones))



x1 = 0
x2 = ancho
velocidad = 2 

reloj = pygame.time.Clock()
ejecutar = True

while ejecutar:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecutar = False

  
    x1 -= velocidad
    x2 -= velocidad


    if x1 <= -ancho:
        x1 = x2 + ancho
    if x2 <= -ancho:
        x2 = x1 + ancho

  
    ventana.blit(fondo, (x1, 0))
    ventana.blit(fondo, (x2, 0))
    ventana.blit(botones,(450,300))
    ventana.blit(configuracion,(450,450))

    pygame.display.flip()
    reloj.tick(60)  

pygame.quit()
sys.exit()

