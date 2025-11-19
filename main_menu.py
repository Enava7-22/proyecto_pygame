import pygame
import sys
from personajes import elegir_personaje
import all_lgame  # importa al inicio

def configuracion():
    # Pantalla de configuración simple
    ancho, alto = 1200, 700
    ventana = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Configuración")
    # Cargar fondo 
    fondo = pygame.image.load("imgs/menulevels.jpg")
    fondo = pygame.transform.scale(fondo, (ancho, alto))
    # Texto y botón volver
    fuente = pygame.font.SysFont(None, 60)
    texto_config = fuente.render("Configuración", True, (255, 255, 255))
    boton_volver = pygame.image.load("imgs/boton inicio.png")  # Reusa imagen o cambia
    boton_volver = pygame.transform.scale(boton_volver, (300, 100))
    boton_volver_rect = pygame.Rect(450, 400, 300, 100)
    reloj = pygame.time.Clock()
    ejecutar = True
    while ejecutar:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejecutar = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if boton_volver_rect.collidepoint(mouse_pos):
                    ejecutar = False  # Vuelve al menú principal
        ventana.blit(fondo, (0, 0))
        ventana.blit(texto_config, (ancho // 2 - texto_config.get_width() // 2, 200))
        mouse_pos = pygame.mouse.get_pos()
        # Hover para botón volver
        if boton_volver_rect.collidepoint(mouse_pos):
            hover_volver = pygame.transform.scale(boton_volver, (310, 105))
            ventana.blit(hover_volver, (445, 395))
        else:
            ventana.blit(boton_volver, (450, 400))
        pygame.display.flip()
        reloj.tick(60)

def mainmenu():
    pygame.init()  
    ancho, alto = 1200, 700
    ancho_botones, alto_botones = 300, 100
    ancho_logo,alto_logo=500,200

    ventana = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Integrador equipo 6")

    # Cargar imágenes
    fondo = pygame.image.load("imgs/fondo_principal.jpeg")
    fondo = pygame.transform.scale(fondo, (ancho, alto))
    logo = pygame.image.load("imgs/logo_juego.png")
    logo = pygame.transform.scale(logo, (ancho_logo, alto_logo))
    boton_inicio = pygame.image.load("imgs/boton_play.png")
    boton_inicio = pygame.transform.scale(boton_inicio, (ancho_botones, alto_botones))
    boton_config = pygame.image.load("imgs/boton configuracion.png")
    boton_config = pygame.transform.scale(boton_config, (ancho_botones, alto_botones))
    boton_salir = pygame.image.load("imgs/boton_play.png")
    boton_salir = pygame.transform.scale(boton_salir, (ancho_botones, alto_botones))

    # Rects para detectar clics y hover
    boton_inicio_rect = pygame.Rect(450, 250, ancho_botones, alto_botones)
    boton_config_rect = pygame.Rect(450, 400, ancho_botones, alto_botones)
    boton_salir_rect = pygame.Rect(450, 550, ancho_botones, alto_botones)


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
                    configuracion()  # Abre la pantalla de configuración
                elif boton_salir_rect.collidepoint(mouse_pos):
                    ejecutar = False  # Cierra el menú y termina el programa

        ventana.blit(fondo, (0, 0))
        ventana.blit(logo, (350,30))

        # Hover simple (escala si mouse encima)
        mouse_pos = pygame.mouse.get_pos()
        if boton_inicio_rect.collidepoint(mouse_pos):
            hover_inicio = pygame.transform.scale(boton_inicio, (ancho_botones + 10, alto_botones + 5))
            ventana.blit(hover_inicio, (445, 245))
        else:
            ventana.blit(boton_inicio, (450, 250))

        if boton_config_rect.collidepoint(mouse_pos):
            hover_config = pygame.transform.scale(boton_config, (ancho_botones + 10, alto_botones + 5))
            ventana.blit(hover_config, (445, 395))
        else:
            ventana.blit(boton_config, (450, 400))
            
        if boton_salir_rect.collidepoint(mouse_pos):
            hover_salir = pygame.transform.scale(boton_salir, (ancho_botones + 10, alto_botones + 5))
            ventana.blit(hover_salir, (445, 545))
        else:
            ventana.blit(boton_salir, (450, 550))

        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    mainmenu()
