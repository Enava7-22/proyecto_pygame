import pygame
import sys

ancho = 1200
alto = 700

# Frames globales (cargados una vez)
frames_p1 = None  # ([derecha], [izquierda])
frames_p2 = None

def cargar_frames():
    global frames_p1, frames_p2
    if frames_p1 is not None:
        return frames_p1, frames_p2  # Ya cargados
    
    # Personaje 1
    f1 = pygame.image.load("imgs/frame1.png").convert_alpha()
    f2 = pygame.image.load("imgs/frame2.png").convert_alpha()
    f3 = pygame.image.load("imgs/frame3.png").convert_alpha()
    f1 = pygame.transform.scale(f1, (80, 100))
    f2 = pygame.transform.scale(f2, (80, 100))
    f3 = pygame.transform.scale(f3, (80, 100))
    f1l = pygame.transform.flip(f1, True, False)
    f2l = pygame.transform.flip(f2, True, False)
    f3l = pygame.transform.flip(f3, True, False)
    
    f1_up = pygame.image.load("imgs/frame1.png").convert_alpha() 
    f2_up = pygame.image.load("imgs/frame2.png").convert_alpha()
    f3_up = pygame.image.load("imgs/frame3.png").convert_alpha()
    f1_up = pygame.transform.scale(f1_up, (80, 100))
    f2_up = pygame.transform.scale(f2_up, (80, 100))
    f3_up = pygame.transform.scale(f3_up, (80, 100))
    
    f1_down = pygame.image.load("imgs/frame1.png").convert_alpha()
    f2_down = pygame.image.load("imgs/frame2.png").convert_alpha()
    f3_down = pygame.image.load("imgs/frame3.png").convert_alpha()
    f1_down = pygame.transform.scale(f1_down, (80, 100))
    f2_down = pygame.transform.scale(f2_down, (80, 100))
    f3_down = pygame.transform.scale(f3_down, (80, 100))

    frames_p1 = ([f1, f2, f1, f3], [f1l, f2l, f1l, f3l], [f1_up, f2_up, f1_up, f3_up], [f1_down, f2_down, f1_down, f3_down]) # Ciclo: 0,1,0,2 para fluidez

    # Personaje 2
    p2_1 = pygame.image.load("imgs/p2_frame1.png").convert_alpha()
    p2_2 = pygame.image.load("imgs/p2_frame2.png").convert_alpha()
    p2_3 = pygame.image.load("imgs/p2_frame3.png").convert_alpha()
    p2_1 = pygame.transform.scale(p2_1, (80, 100))
    p2_2 = pygame.transform.scale(p2_2, (80, 100))
    p2_3 = pygame.transform.scale(p2_3, (80, 100))
    p2_1l = pygame.transform.flip(p2_1, True, False)
    p2_2l = pygame.transform.flip(p2_2, True, False)
    p2_3l = pygame.transform.flip(p2_3, True, False)
    p2_1_up = pygame.image.load("imgs/p2_frame1.png").convert_alpha()
    p2_2_up = pygame.image.load("imgs/p2_frame2.png").convert_alpha()
    p2_3_up = pygame.image.load("imgs/p2_frame3.png").convert_alpha()
    p2_1_up = pygame.transform.scale(p2_1_up, (80, 100))
    p2_2_up = pygame.transform.scale(p2_2_up, (80, 100))
    p2_3_up = pygame.transform.scale(p2_3_up, (80, 100))

    
    p2_1_down = pygame.image.load("imgs/p2_frame1.png").convert_alpha()
    p2_2_down = pygame.image.load("imgs/p2_frame2.png").convert_alpha()
    p2_3_down = pygame.image.load("imgs/p2_frame3.png").convert_alpha()
    p2_1_down = pygame.transform.scale(p2_1_down, (80, 100))
    p2_2_down = pygame.transform.scale(p2_2_down, (80, 100))
    p2_3_down = pygame.transform.scale(p2_3_down, (80, 100))

    frames_p2 = ([p2_1, p2_2, p2_1, p2_3], [p2_1l, p2_2l, p2_1l, p2_3l], [p2_1_up, p2_2_up, p2_1_up, p2_3_up], [p2_1_down, p2_2_down, p2_1_down, p2_3_down])

    return frames_p1, frames_p2

# Pantalla de selección con animación preview
def elegir_personaje():
    global frames_p1, frames_p2
    cargar_frames()  # Carga si no está
    
    ventana = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Elige tu personaje")
    
    fuente = pygame.font.SysFont(None, 60)
    texto = fuente.render("Elige tu personaje", True, (255, 255, 255))
    
    # Imágenes preview escaladas para selección
    p1_preview = frames_p1[0][0]  # Primer frame derecha, escalado
    p1_preview = pygame.transform.scale(p1_preview, (150, 200))
    rect1 = p1_preview.get_rect(center=(ancho // 3, alto // 2))
    
    p2_preview = frames_p2[0][0]
    p2_preview = pygame.transform.scale(p2_preview, (150, 200))
    rect2 = p2_preview.get_rect(center=(2 * ancho // 3, alto // 2))
    
    # Animación preview: frame actual y timer
    frame_p1_actual = 0
    frame_p2_actual = 0
    tiempo_preview = pygame.time.get_ticks()
    velocidad_preview = 500  # ms por frame en preview (lento)
    
    # Dirección preview (oscila izquierda/derecha)
    dir_p1 = 0  # 0: derecha, 1: izquierda
    dir_p2 = 0
    
    elegido = None
    clock = pygame.time.Clock()
    
    while elegido is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if rect1.collidepoint(mouse_pos):
                    elegido = "p1"
                elif rect2.collidepoint(mouse_pos):
                    elegido = "p2"
        
        # Animar preview
        ahora = pygame.time.get_ticks()
        if ahora - tiempo_preview > velocidad_preview:
            tiempo_preview = ahora
            # Ciclar frames
            frame_p1_actual = (frame_p1_actual + 1) % len(frames_p1[0])
            frame_p2_actual = (frame_p2_actual + 1) % len(frames_p2[0])
            # Oscilar dirección cada 2 ciclos
            if frame_p1_actual % 4 == 0:
                dir_p1 = 1 - dir_p1
            if frame_p2_actual % 4 == 0:
                dir_p2 = 1 - dir_p2
        
        # Obtener frames actuales para preview
        frame_p1 = frames_p1[dir_p1][frame_p1_actual]
        frame_p1 = pygame.transform.scale(frame_p1, (150, 200))
        frame_p2 = frames_p2[dir_p2][frame_p2_actual]
        frame_p2 = pygame.transform.scale(frame_p2, (150, 200))
        
        # Dibujar
        ventana.fill((50, 50, 50))
        ventana.blit(texto, (ancho // 2 - texto.get_width() // 2, 50))
        
        # Hover: Escala si mouse encima
        mouse_pos = pygame.mouse.get_pos()
        if rect1.collidepoint(mouse_pos):
            frame_p1_hover = pygame.transform.scale(frame_p1, (160, 210))
            ventana.blit(frame_p1_hover, (rect1.x - 5, rect1.y - 5))
        else:
            ventana.blit(frame_p1, rect1)
        
        if rect2.collidepoint(mouse_pos):
            frame_p2_hover = pygame.transform.scale(frame_p2, (160, 210))
            ventana.blit(frame_p2_hover, (rect2.x - 5, rect2.y - 5))
        else:
            ventana.blit(frame_p2, rect2)
        
        pygame.display.flip()
        clock.tick(60)
    
    return elegido  # 'p1' o 'p2'
