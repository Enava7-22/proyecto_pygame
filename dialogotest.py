import pygame
import sys

pygame.init()

def l1():
    pass

def lastdialogo():
    ancho = 1200
    alto = 800
    ventana = pygame.display.set_mode((ancho, alto))
   
    
    fondo = pygame.image.load("imgs/df.png")
    fondo = pygame.transform.scale(fondo, (ancho, alto))
    
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    l1()
        
        ventana.blit(fondo, (0, 0))
        pygame.display.update()
        clock.tick(60)

lastdialogo()
