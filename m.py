@ -2,16 +2,133 @@ import pygame
import random
import sys
from personajes import cargar_frames, elegir_personaje

from main_menu import mainmenu
from muerte import muerto, pos_muerte, pantalla_muerte
pygame.mixer.init()
pygame.init()

contador_sillas = 0
# Variable global para pausa
pausa = False
personaje_elegido = None
# Variable global para pausa y nivel actual
pausa = False
nivel_actual = None  # Apuntará a la función del nivel (ej. l1)

def menu_pausa():
    global pausa
    # Estados para botones presionados (declarar al inicio)
    resume_presionado = False
    menu_presionado = False
    reiniciar_presionado = False

    # Cargar imágenes de botones con animaciones
    try:
        boton_resume_normal = pygame.image.load("imgs/boton_seguir.png")
        boton_resume_presionado = pygame.image.load("imgs/boton_seguirp.png")
        boton_menu_normal = pygame.image.load("imgs/boton_menu.png")
        boton_menu_presionado = pygame.image.load("imgs/boton_menup.png")
        boton_reiniciar_normal = pygame.image.load("imgs/boton_reiniciar.png")
        boton_reiniciar_presionado = pygame.image.load("imgs/boton_reiniciarp.png")
    except FileNotFoundError as e:
        print(f"Error cargando imágenes de pausa: {e}")
        return  # Salir si no hay imágenes

    # Escalar botones
    ancho_boton, alto_boton = 400, 120
    boton_resume_normal = pygame.transform.scale(boton_resume_normal, (ancho_boton, alto_boton))
    boton_resume_presionado = pygame.transform.scale(boton_resume_presionado, (ancho_boton, alto_boton))
    boton_menu_normal = pygame.transform.scale(boton_menu_normal, (ancho_boton, alto_boton))
    boton_menu_presionado = pygame.transform.scale(boton_menu_presionado, (ancho_boton, alto_boton))
    boton_reiniciar_normal = pygame.transform.scale(boton_reiniciar_normal, (ancho_boton, alto_boton))
    boton_reiniciar_presionado = pygame.transform.scale(boton_reiniciar_presionado, (ancho_boton, alto_boton))

    # Rects para botones
    ventana_actual = pygame.display.get_surface()
    centro_x = ventana_actual.get_width() // 2
    rect_resume = pygame.Rect(centro_x - ancho_boton // 2, 550, ancho_boton, alto_boton)
    rect_menu = pygame.Rect(centro_x - ancho_boton // 2, 400, ancho_boton, alto_boton)
    rect_reiniciar = pygame.Rect(centro_x - ancho_boton // 2, 250, ancho_boton, alto_boton)

    while pausa:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Clic izquierdo abajo
                if rect_resume.collidepoint(mouse_pos):
                    resume_presionado = True
                elif rect_menu.collidepoint(mouse_pos):
                    menu_presionado = True
                elif rect_reiniciar.collidepoint(mouse_pos):
                    reiniciar_presionado = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # Clic izquierdo arriba
                if resume_presionado and rect_resume.collidepoint(mouse_pos):

                    pausa = False
                    return
                elif menu_presionado and rect_menu.collidepoint(mouse_pos):
                    pausa = False
                    mainmenu()
                    return
                elif reiniciar_presionado and rect_reiniciar.collidepoint(mouse_pos):
                    pausa = False
                    if nivel_actual:
                        nivel_actual()
                    return
                # Resetear estados
                resume_presionado = False
                menu_presionado = False
                reiniciar_presionado = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # P para salir de pausa
                    pausa = False
                    return

        # Dibujar fondo semi-transparente
        fondo_pausa = pygame.Surface(ventana_actual.get_size())
        fondo_pausa.set_alpha(100)  # transparente
        fondo_pausa.fill((69, 63, 63))
        ventana_actual.blit(fondo_pausa, (0, 0))

        # Dibujar botones con animaciones
        # Botón Resume
        if resume_presionado:
            ventana_actual.blit(boton_resume_presionado, (rect_resume.x, rect_resume.y))
        elif rect_resume.collidepoint(mouse_pos):
            hover_resume = pygame.transform.scale(boton_resume_normal, (ancho_boton + 10, alto_boton + 5))
            ventana_actual.blit(hover_resume, (rect_resume.x - 5, rect_resume.y - 2.5))
        else:
            ventana_actual.blit(boton_resume_normal, (rect_resume.x, rect_resume.y))

        # Botón Menu
        if menu_presionado:
            ventana_actual.blit(boton_menu_presionado, (rect_menu.x, rect_menu.y))
        elif rect_menu.collidepoint(mouse_pos):
            hover_menu = pygame.transform.scale(boton_menu_normal, (ancho_boton + 10, alto_boton + 5))
            ventana_actual.blit(hover_menu, (rect_menu.x - 5, rect_menu.y - 2.5))
        else:
            ventana_actual.blit(boton_menu_normal, (rect_menu.x, rect_menu.y))

        # Botón Reiniciar
        if reiniciar_presionado:
            ventana_actual.blit(boton_reiniciar_presionado, (rect_reiniciar.x, rect_reiniciar.y))
        elif rect_reiniciar.collidepoint(mouse_pos):
            hover_reiniciar = pygame.transform.scale(boton_reiniciar_normal, (ancho_boton + 10, alto_boton + 5))
            ventana_actual.blit(hover_reiniciar, (rect_reiniciar.x - 5, rect_reiniciar.y - 2.5))
        else:
            ventana_actual.blit(boton_reiniciar_normal, (rect_reiniciar.x, rect_reiniciar.y))

        pygame.display.flip()
        pygame.time.Clock().tick(60)


# Variable global para el personaje elegido (se ejecuta al inicio)
personaje_elegido = None  # Pantalla de selección animada
# Variable global para el personaje elegido 
# # Pantalla de selección animada

# Clase Jugador con animaciones (unifica movimiento, física y dibujo)
# Clase Jugador con animaciones ( movimiento, física y dibujo)
class Jugador:
    def __init__(self, x, y, width, height, con_gravedad=False, personaje='p1', ancho_max=1200, ancho_hitbox=20, alto_hitbox=30):
        # Parámetros opcionales para hitbox (por defecto 20x30)
@ -261,7 +378,7 @@ def menulevels():
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return()  # Regresa al menú principal
                    mainmenu()  # Regresa al menú principal
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Clic izquierdo abajo
                if botonl1.collidepoint(mouse_pos):
                    level1_presionado = True
@ -498,7 +615,6 @@ def l1():
def level2():
    

    
    ancho, alto = 1200, 700
    ventana = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("minilevel 2")
@ -599,7 +715,20 @@ def videojuego():
    clock = pygame.time.Clock()

    while True:
        global nivel_actual
        nivel_actual = videojuego

        # Chequear pausa
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # P para pausar
                    global pausa
                    pausa = not pausa
                teclas = pygame.key.get_pressed()
        
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
@ -608,6 +737,9 @@ def videojuego():
                if event.key == pygame.K_SPACE and en_suelo:
                    velocidad_y = fuerza_salto
                    en_suelo = False
        if pausa:
            menu_pausa()
            continue  # Saltar el resto del bucle mientras pausa

        teclas = pygame.key.get_pressed()
        jugador.actualizar(teclas, paredes=pared)
@ -644,24 +776,22 @@ def videojuego():
        for obj in objetos[:]:
            obj.y += 5
            ventana.blit(misil_img, obj)

            if jugador.rect.colliderect(obj):
                objetos.remove(obj)
                daño += 20
                if daño > 100:
                    daño = 100
                    reinicio()
                if daño >= 100:
                    global muerto, pos_muerte
                    muerto = True
                    pos_muerte = (jugador.rect.x, jugador.rect.y)
                    print(f"muerto set a True: {muerto}")  # Debug
                    pantalla_muerte(personaje_elegido, nivel_actual)
                    return

            if obj.top > alto:
                objetos.remove(obj)

        pygame.display.flip()
        clock.tick(60)




        
def dialogo1_l3():
    ancho = 1200
@ -791,7 +921,6 @@ def level3():
        
        pygame.Rect(685.00,19.67,57.00,113.67),
    
   
        
        
    ]
@ -930,6 +1059,26 @@ def level2_parte1():

    while run:
        clock.tick(60)
<<<<<<< HEAD
=======

        global nivel_actual
        nivel_actual = level2_parte1

        # Chequear pausa
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # P para pausar
                    global pausa
                    pausa = not pausa

        if pausa:
            menu_pausa()
            continue  # Saltar el resto del bucle mientras pausa
>>>>>>> 487b8c5454bfa843b87d41f26ff112fab0df3d6c
        teclas = pygame.key.get_pressed()
        jugador.actualizar(teclas, paredes=pared, limite_inferior=ALTO_MAPA)

@ -940,10 +1089,18 @@ def level2_parte1():
            hitbox_alto
        )

<<<<<<< HEAD
        for p in pared:
            if col_rect.colliderect(p):
                l1()
                return
=======
        if contador_vida >= 3:
            muerto = True
            pos_muerte = (jugador.rect.x, jugador.rect.y)  # Guardar posición de muerte
            pantalla_muerte(personaje_elegido, nivel_actual)  # Mostrar pantalla de muerte
            return
>>>>>>> 487b8c5454bfa843b87d41f26ff112fab0df3d6c

        cam_x = jugador.rect.x - ANCHO_WIN // 2
        cam_y = jugador.rect.y - ALTO_WIN // 2
