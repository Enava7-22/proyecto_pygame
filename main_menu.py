import pygame
import sys
from personajes import elegir_personaje
import all_lgame  # importa al inicio

def mainmenu():
    pygame.init()  
    ancho, alto = 1200, 700
    ancho_botones, alto_botones = 300, 100

    ventana = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Integrador equipo 6")

    # Cargar imágenes
    fondo = pygame.image.load("imgs/img.jpg")
    fondo = pygame.transform.scale(fondo, (ancho, alto))
    boton_inicio = pygame.image.load("imgs/boton inicio.png")
    boton_inicio = pygame.transform.scale(boton_inicio, (ancho_botones, alto_botones))
    boton_config = pygame.image.load("imgs/boton configuracion.png")
    boton_config = pygame.transform.scale(boton_config, (ancho_botones, alto_botones))

    # Rects para detectar clics y hover
    boton_inicio_rect = pygame.Rect(450, 300, ancho_botones, alto_botones)
    boton_config_rect = pygame.Rect(450, 450, ancho_botones, alto_botones)


    reloj = pygame.time.Clock()
    ejecutar = True

    while ejecutar:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejecutar = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # clic izquierdo
                mouse_pos = event.pos
                if boton_inicio_rect.collidepoint(mouse_pos):
                    # Abrir pantalla de selección de personaje
                    personaje_elegido = elegir_personaje()
                    all_lgame.personaje_elegido = personaje_elegido
                    all_lgame.menulevels()  # Inicia niveles
                elif boton_config_rect.collidepoint(mouse_pos):
                    print("Botón CONFIGURACIÓN presionado - menú de config")

        ventana.blit(fondo, (0, 0))


        # Hover simple (escala si mouse encima)
        mouse_pos = pygame.mouse.get_pos()
        if boton_inicio_rect.collidepoint(mouse_pos):
            hover_inicio = pygame.transform.scale(boton_inicio, (ancho_botones + 10, alto_botones + 5))
            ventana.blit(hover_inicio, (445, 295))
        else:
            ventana.blit(boton_inicio, (450, 300))
        
        if boton_config_rect.collidepoint(mouse_pos):
            hover_config = pygame.transform.scale(boton_config, (ancho_botones + 10, alto_botones + 5))
            ventana.blit(hover_config, (445, 445))
        else:
            ventana.blit(boton_config, (450, 450))

        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()
    sys.exit()

# Para testing
if __name__ == "__main__":
    mainmenu()
