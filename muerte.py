import pygame
from personajes import cargar_frames

# Variables globales para muerte
muerto = False
pos_muerte = (0, 0)  #muerte personaje

def pantalla_muerte(personaje_elegido, nivel_actual):
    global muerto
    muerto = True
    print("Entrando a pantalla_muerte")  # Debug
    
    # Cargar y reproducir música de muerte
    try:
        pygame.mixer.music.load("music/Moog City (cover).mp3")
        pygame.mixer.music.play(-1)  # Reproducir en loop
        print("Música de muerte cargada y reproduciendo")  # Debug
    except pygame.error as e:
        print(f"Error cargando música: {e}")
    
    # Aseguramos que los frames estén cargados
    cargar_frames()
    
    # Cargar animación de muerte
    try:
        frames_muerte = cargar_frames()[personaje_elegido][4]
        frames_muerte = [pygame.transform.scale(f, (100, 120)) for f in frames_muerte]
        tiene_animacion = True
        print(f"Frames de muerte cargados para {personaje_elegido}: {len(frames_muerte)} frames")  # Debug
    except (IndexError, TypeError, KeyError) as e:
        print(f"Error cargando frames de muerte: {e}")  # Debug
        frames_muerte = [pygame.image.load("imgs/personaje.png")]
        frames_muerte[0] = pygame.transform.scale(frames_muerte[0], (100, 120))
        tiene_animacion = False
        print("Fallback a imagen estática")  # Debug

    # Cargar botones (igual que antes)
    try:
        boton_reiniciar_normal = pygame.image.load("imgs/boton_reiniciar.png")
        boton_reiniciar_presionado = pygame.image.load("imgs/boton_reiniciarp.png")
        boton_menu_normal = pygame.image.load("imgs/boton_menu.png")
        boton_menu_presionado = pygame.image.load("imgs/boton_menup.png")
        print("Botones cargados")  # Debug
    except FileNotFoundError:
        print("Error: Imágenes de botones no encontradas")  # Debug
        return

    ancho_boton, alto_boton = 300, 100
    boton_reiniciar_normal = pygame.transform.scale(boton_reiniciar_normal, (ancho_boton, alto_boton))
    boton_reiniciar_presionado = pygame.transform.scale(boton_reiniciar_presionado, (ancho_boton, alto_boton))
    boton_menu_normal = pygame.transform.scale(boton_menu_normal, (ancho_boton, alto_boton))
    boton_menu_presionado = pygame.transform.scale(boton_menu_presionado, (ancho_boton, alto_boton))

    try:
        fuente_texto = pygame.font.Font("fuentes/leadcoat.ttf", 80)
    except:
        fuente_texto = pygame.font.SysFont("arial", 80)  # Fuente del sistema, más grande
    texto_mensaje = fuente_texto.render("Esa escuela no se salvara sola", True, (255, 255, 255))
    
    ventana_actual = pygame.display.get_surface()
    centro_x = ventana_actual.get_width() // 2
    rect_reiniciar = pygame.Rect(centro_x - ancho_boton // 2, 300, ancho_boton, alto_boton)
    rect_menu = pygame.Rect(centro_x - ancho_boton // 2, 450, ancho_boton, alto_boton)

    reiniciar_presionado = False
    menu_presionado = False

    frame_actual = 0
    tiempo_anim = pygame.time.get_ticks()
    alpha = 0
    fade_completo = False
    tiempo_inicio = pygame.time.get_ticks()

    print(f"muerto antes del bucle: {muerto}")  # Debug
    while muerto:
        ahora = pygame.time.get_ticks()
        mouse_pos = pygame.mouse.get_pos()

        # Animar muerte (pausa en el último frame)
        if tiene_animacion and ahora - tiempo_anim > 500 and frame_actual < len(frames_muerte) - 1:
            tiempo_anim = ahora
            frame_actual += 1  # Avanzar sin ciclar

        # Fade to black (más lento: 4 segundos)
        if not fade_completo:
            alpha = min(255, (ahora - tiempo_inicio) / 4000 * 255)
            if alpha >= 255:
                fade_completo = True
                print("Fade completo")  # Debug

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif fade_completo and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if rect_reiniciar.collidepoint(mouse_pos):
                    reiniciar_presionado = True
                elif rect_menu.collidepoint(mouse_pos):
                    menu_presionado = True
            elif fade_completo and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if reiniciar_presionado and rect_reiniciar.collidepoint(mouse_pos):
                    print("Reiniciando nivel")  # Debug
                    pygame.mixer.music.stop()
                    muerto = False
                    if nivel_actual:
                        nivel_actual()
                    return
                elif menu_presionado and rect_menu.collidepoint(mouse_pos):
                    print("Saliendo al menú")  # Debug
                    pygame.mixer.music.stop()
                    muerto = False
                    from main_menu import mainmenu
                    mainmenu()
                    return
                reiniciar_presionado = False
                menu_presionado = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                print("P presionado, saliendo")  # Debug
                muerto = False
                return

        # Dibujar
        ventana_actual.fill((0, 0, 0))
        if not fade_completo:
            imagen_muerte = frames_muerte[frame_actual]
            # Centrar en la pantalla
            x_centro = ventana_actual.get_width() // 2 - imagen_muerte.get_width() // 2
            y_centro = ventana_actual.get_height() // 2 - imagen_muerte.get_height() // 2
            ventana_actual.blit(imagen_muerte, (x_centro, y_centro))

        if alpha > 0:
            superficie_fade = pygame.Surface(ventana_actual.get_size())
            superficie_fade.set_alpha(alpha)
            superficie_fade.fill((0, 0, 0))
            ventana_actual.blit(superficie_fade, (0, 0))

        if fade_completo:
            ventana_actual.blit(texto_mensaje, (centro_x - texto_mensaje.get_width() // 2, 100))
            # Dibujar botones (igual que antes)
            if reiniciar_presionado:
                ventana_actual.blit(boton_reiniciar_presionado, (rect_reiniciar.x, rect_reiniciar.y))
            elif rect_reiniciar.collidepoint(mouse_pos):
                hover_reiniciar = pygame.transform.scale(boton_reiniciar_normal, (ancho_boton + 10, alto_boton + 5))
                ventana_actual.blit(hover_reiniciar, (rect_reiniciar.x - 5, rect_reiniciar.y - 2.5))
            else:
                ventana_actual.blit(boton_reiniciar_normal, (rect_reiniciar.x, rect_reiniciar.y))

            if menu_presionado:
                ventana_actual.blit(boton_menu_presionado, (rect_menu.x, rect_menu.y))
            elif rect_menu.collidepoint(mouse_pos):
                hover_menu = pygame.transform.scale(boton_menu_normal, (ancho_boton + 10, alto_boton + 5))
                ventana_actual.blit(hover_menu, (rect_menu.x - 5, rect_menu.y - 2.5))
            else:
                ventana_actual.blit(boton_menu_normal, (rect_menu.x, rect_menu.y))

        pygame.display.flip()
        pygame.time.Clock().tick(60)
    print("Saliendo de pantalla_muerte")  # Debug
