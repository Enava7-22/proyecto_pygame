import pygame
import sys
from personajes import elegir_personaje
import all_lgame 

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
    boton_volver = pygame.image.load("imgs/boton_salir.png")  # Reusa imagen o cambia
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
    ancho_botones, alto_botones = 450, 120
    ancho_logo, alto_logo = 500, 300

    ventana = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Integrador equipo 6")

    # Cargar imágenes
    fondo = pygame.image.load("imgs/fondo_principal.jpeg")
    fondo = pygame.transform.scale(fondo, (ancho, alto))
    logo = pygame.image.load("imgs/logo_juego.png")
    logo = pygame.transform.scale(logo, (ancho_logo, alto_logo))
    # Botón inicio,config,salir: normal y presionado
    boton_inicio_normal = pygame.image.load("imgs/boton_play.png")
    boton_inicio_normal = pygame.transform.scale(boton_inicio_normal, (ancho_botones, alto_botones))
    boton_inicio_presionado = pygame.image.load("imgs/boton_playp.png")
    boton_inicio_presionado = pygame.transform.scale(boton_inicio_presionado, (ancho_botones, alto_botones))
    boton_config_normal = pygame.image.load("imgs/boton_options.png")
    boton_config_normal = pygame.transform.scale(boton_config_normal, (ancho_botones, alto_botones))
    boton_config_presionado = pygame.image.load("imgs/boton_optionsp.png")
    boton_config_presionado = pygame.transform.scale(boton_config_presionado, (ancho_botones, alto_botones))
    boton_salir_normal = pygame.image.load("imgs/boton_salir.png")
    boton_salir_normal = pygame.transform.scale(boton_salir_normal, (ancho_botones, alto_botones))
    boton_salir_presionado = pygame.image.load("imgs/boton_salirp.png")
    boton_salir_presionado = pygame.transform.scale(boton_salir_presionado, (ancho_botones, alto_botones))

    # Rects para detectar clics y hover

    centro_x = ancho // 2
    boton_inicio_rect = pygame.Rect(centro_x - ancho_botones // 2, 250, ancho_botones, alto_botones)
    boton_config_rect= pygame.Rect(centro_x - ancho_botones // 2, 400, ancho_botones, alto_botones)
    boton_salir_rect = pygame.Rect(centro_x - ancho_botones // 2, 550, ancho_botones, alto_botones)
    x_logo = centro_x - ancho_logo // 2 
    # Estados para botones presionados
    inicio_presionado = False
    config_presionado = False
    salir_presionado = False
    
    x1 = 0
    x2 = ancho
    
    reloj = pygame.time.Clock()
    ejecutar = True

    while ejecutar:
        mouse_pos = pygame.mouse.get_pos()  # Obtener posición del mouse una vez por frame

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejecutar = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Clic izquierdo abajo
                if boton_inicio_rect.collidepoint(mouse_pos):
                    inicio_presionado = True
                elif boton_config_rect.collidepoint(mouse_pos):
                    config_presionado = True
                elif boton_salir_rect.collidepoint(mouse_pos):
                    salir_presionado = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # Clic izquierdo arriba
                if inicio_presionado and boton_inicio_rect.collidepoint(mouse_pos):
                    # Acción: Abrir pantalla de selección de personaje
                    personaje_elegido = elegir_personaje()
                    all_lgame.personaje_elegido = personaje_elegido
                    all_lgame.menulevels()  # Inicia niveles
                elif config_presionado and boton_config_rect.collidepoint(mouse_pos):
                    configuracion()  # Abre la pantalla de configuración
                elif salir_presionado and boton_salir_rect.collidepoint(mouse_pos):
                    ejecutar = False  # Cierra el menú y termina el programa
                # Resetear estados
                inicio_presionado = False
                config_presionado = False
                salir_presionado = False

        if x1 <= -ancho:
            x1 = x2 + ancho
        if x2 <= -ancho:
            x2 = x1 + ancho
        
        ventana.blit(fondo, (x1, 0))
        ventana.blit(fondo, (x2, 0))
        ventana.blit(logo, (x_logo, 0))


        # Botón inicio
        if inicio_presionado:
            ventana.blit(boton_inicio_presionado, (boton_inicio_rect.x, boton_inicio_rect.y))
        elif boton_inicio_rect.collidepoint(mouse_pos):
            hover_inicio = pygame.transform.scale(boton_inicio_normal, (ancho_botones + 10, alto_botones + 5))
            ventana.blit(hover_inicio, (boton_inicio_rect.x - 5, boton_inicio_rect.y - 2.5))
        else:
            ventana.blit(boton_inicio_normal, (boton_inicio_rect.x, boton_inicio_rect.y))

        # Botón config
        if config_presionado:
            ventana.blit(boton_config_presionado, (boton_config_rect.x, boton_config_rect.y))
        elif boton_config_rect.collidepoint(mouse_pos):
            hover_config = pygame.transform.scale(boton_config_normal, (ancho_botones + 10, alto_botones + 5))
            ventana.blit(hover_config, (boton_config_rect.x - 5, boton_config_rect.y - 2.5))
        else:
            ventana.blit(boton_config_normal, (boton_config_rect.x, boton_config_rect.y))
            
        # Botón salir
        if salir_presionado:
            ventana.blit(boton_salir_presionado, (boton_salir_rect.x, boton_salir_rect.y))  
        elif boton_salir_rect.collidepoint(mouse_pos):
            hover_salir = pygame.transform.scale(boton_salir_normal, (ancho_botones + 10, alto_botones + 5))
            ventana.blit(hover_salir, (boton_salir_rect.x - 5, boton_salir_rect.y - 2.5))
        else:
            ventana.blit(boton_salir_normal, (boton_salir_rect.x, boton_salir_rect.y))

        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    mainmenu()