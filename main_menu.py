import pygame
import sys
from personajes import elegir_personaje
import all_lgame 

# Variables globales para configuración
volumen = 50  # 1-100
idioma = "es"  # "es" o "en"

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
    boton_inicio_normal = pygame.image.load("imgs/boton_jugar.png")
    boton_inicio_normal = pygame.transform.scale(boton_inicio_normal, (ancho_botones, alto_botones))
    boton_inicio_presionado = pygame.image.load("imgs/boton_jugarp.png")
    boton_inicio_presionado = pygame.transform.scale(boton_inicio_presionado, (ancho_botones, alto_botones))
    boton_config_normal = pygame.image.load("imgs/boton_opciones.png")
    boton_config_normal = pygame.transform.scale(boton_config_normal, (ancho_botones, alto_botones))
    boton_config_presionado = pygame.image.load("imgs/boton_opciones.png")
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

def configuracion():
    global volumen, idioma  # Declarar globales al inicio
    ancho, alto = 1200, 700
    ventana = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Configuración")

    
    try:
        bandera_ingles = pygame.image.load("imgs/british.png")
        bandera_espanol = pygame.image.load("imgs/españa.png")
        boton_salir_normal = pygame.image.load("imgs/boton_salir.png")
        boton_salir_presionado = pygame.image.load("imgs/boton_salirp.png")  # Imagen presionada
    except FileNotFoundError:
        print("Error cargando imágenes de configuración")
        return

    # Escalar imágenes
    bandera_ingles = pygame.transform.scale(bandera_ingles, (100, 60))
    bandera_espanol = pygame.transform.scale(bandera_espanol, (100, 60))
    boton_salir_normal = pygame.transform.scale(boton_salir_normal, (200, 80))
    boton_salir_presionado = pygame.transform.scale(boton_salir_presionado, (200, 80))

    # Fuentes
    fuente_titulo = pygame.font.SysFont("arial", 60)
    fuente_texto = pygame.font.SysFont("arial", 40)
    fuente_volumen = pygame.font.SysFont("arial", 30)

    # Rects para elementos
    rect_bandera_ingles = pygame.Rect(400, 300, 100, 60)
    rect_bandera_espanol = pygame.Rect(700, 300, 100, 60)
    rect_slider_volumen = pygame.Rect(400, 200, 400, 20) 
    rect_boton_salir = pygame.Rect(500, 500, 200, 80)

    slider_pos = 400 + (volumen / 100) * 400 

    # Estado para botón salir
    salir_presionado = False

    clock = pygame.time.Clock()
    ejecutando = True

    while ejecutando:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if rect_bandera_ingles.collidepoint(mouse_pos):
                    idioma = "en"
                elif rect_bandera_espanol.collidepoint(mouse_pos):
                    idioma = "es"
                elif rect_slider_volumen.collidepoint(mouse_pos):
                    # Mover slider
                    slider_pos = max(400, min(mouse_pos[0], 800))
                    volumen = int((slider_pos - 400) / 400 * 100)
                elif rect_boton_salir.collidepoint(mouse_pos):
                    salir_presionado = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if salir_presionado and rect_boton_salir.collidepoint(mouse_pos):
                    ejecutando = False
                salir_presionado = False  # Resetear
            elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                if rect_slider_volumen.collidepoint(mouse_pos):
                    slider_pos = max(400, min(mouse_pos[0], 800))
                    volumen = int((slider_pos - 400) / 400 * 100)

        # Dibujar
        ventana.fill((50, 50, 50))

        # Título
        titulo = fuente_titulo.render("Configuración", True, (255, 255, 255))
        ventana.blit(titulo, (ancho // 2 - titulo.get_width() // 2, 50))

        # Volumen
        texto_volumen = fuente_texto.render("Volumen", True, (255, 255, 255))
        ventana.blit(texto_volumen, (400, 150))
        # Barra del slider
        pygame.draw.rect(ventana, (200, 200, 200), rect_slider_volumen)
        # Indicador
        pygame.draw.circle(ventana, (255, 0, 0), (int(slider_pos), 210), 10)
        # Texto del valor
        texto_valor_volumen = fuente_volumen.render(f"{volumen}", True, (255, 255, 255))
        ventana.blit(texto_valor_volumen, (820, 190))

        # Idioma
        texto_idioma = fuente_texto.render("Idioma", True, (255, 255, 255))
        ventana.blit(texto_idioma, (400, 250))
        ventana.blit(bandera_ingles, (400, 300))
        ventana.blit(bandera_espanol, (700, 300))
        # Indicador de selección
        if idioma == "en":
            pygame.draw.rect(ventana, (0, 255, 0), rect_bandera_ingles, 3)
        elif idioma == "es":
            pygame.draw.rect(ventana, (0, 255, 0), rect_bandera_espanol, 3)

        # Botón salir con animación
        if salir_presionado:
            ventana.blit(boton_salir_presionado, (rect_boton_salir.x, rect_boton_salir.y))
        elif rect_boton_salir.collidepoint(mouse_pos):
            hover_salir = pygame.transform.scale(boton_salir_normal, (210, 85))  # Hover
            ventana.blit(hover_salir, (rect_boton_salir.x - 5, rect_boton_salir.y - 2.5))
        else:
            ventana.blit(boton_salir_normal, (rect_boton_salir.x, rect_boton_salir.y))

        pygame.display.flip()
        clock.tick(60)
    mainmenu()


if __name__ == "__main__":
<<<<<<< HEAD
    mainmenu() 
    
    #hola
=======
    mainmenu()
>>>>>>> 5fc28d0ba4fcece03ed931013a949ba138f8c54a
