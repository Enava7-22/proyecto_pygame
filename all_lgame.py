import pygame
import random
import sys
from personajes import cargar_frames, elegir_personaje

pygame.mixer.init()
pygame.init()

contador_sillas = 0

# Variable global para el personaje elegido (se ejecuta al inicio)
personaje_elegido = None  # Pantalla de selección animada

# Clase Jugador con animaciones (unifica movimiento, física y dibujo)
class Jugador:
    def __init__(self, x, y, width, height, con_gravedad=False, personaje='p1', ancho_max=1200, ancho_hitbox=20, alto_hitbox=30):
        # Parámetros opcionales para hitbox (por defecto 20x30)
        self.rect = pygame.Rect(
            x + (width - ancho_hitbox)//2,  # centrado horizontal
            y + height - alto_hitbox,       # pie del jugador
            ancho_hitbox,
            alto_hitbox
        )
        self.velocidad_x = 10  # Horizontal (ajustable)
        self.velocidad_y = 0
        self.gravedad = 1 if con_gravedad else 0
        self.fuerza_salto = -15 if con_gravedad else 0
        self.en_suelo = not con_gravedad
        self.suelo_y = 690 if con_gravedad else None  # Por defecto; ajusta por nivel
        self.direccion = 1  # 1: derecha, -1: izquierda
        self.estado = 'idle'  # 'idle', 'walking', 'walking_up', 'walking_down'
        self.con_gravedad = con_gravedad
        self.personaje = personaje
        self.ancho_max = ancho_max  # Para límites horizontales
        
        # Cargar frames para este personaje (de personajes.py)
        frames_p1, frames_p2 = cargar_frames()
        frames_globales = {'p1': frames_p1, 'p2': frames_p2}
        self.frames = frames_globales[self.personaje]  # ([derecha], [izquierda], [arriba], [abajo])
        
        self.frames_derecha = [pygame.transform.scale(f, (width, height)) for f in self.frames[0]]
        self.frames_izquierda = [pygame.transform.scale(f, (width, height)) for f in self.frames[1]]
        self.frames_arriba = [pygame.transform.scale(f, (width, height)) for f in self.frames[2]]  # Nuevo: frames para arriba
        self.frames_abajo = [pygame.transform.scale(f, (width, height)) for f in self.frames[3]]   # Nuevo: frames para abajo
        
        try:
            self.imagen_actual = self.frames_derecha[0]
            self.tiene_frames = True
        except Exception as e:
            self.imagen_estatica = pygame.image.load("imgs/personaje.png")
            self.imagen_estatica = pygame.transform.scale(self.imagen_estatica, (width, height))
            self.imagen_actual = self.imagen_estatica
            self.tiene_frames = False
            print(f"Advertencia: Usando imagen estática para {personaje}. Error: {e}")
        
        self.frame_actual = 0
        self.tiempo_animacion = pygame.time.get_ticks()
        self.velocidad_animacion_walking = 150  
        self.velocidad_animacion_idle = 500
    
    def actualizar(self, teclas, paredes=None, limite_superior=0, limite_inferior=float('inf')):
        x_ant, y_ant = self.rect.x, self.rect.y
        moviendo_horizontal = teclas[pygame.K_LEFT] or teclas[pygame.K_RIGHT]
        moviendo_vertical = teclas[pygame.K_UP] or teclas[pygame.K_DOWN]

        # --- ACTUALIZAR ESTADO ---
        if moviendo_horizontal and not moviendo_vertical:
            self.estado = 'walking'
        elif moviendo_vertical and not moviendo_horizontal:
            self.estado = 'walking_up' if teclas[pygame.K_UP] else 'walking_down'
        elif moviendo_horizontal and moviendo_vertical:
            self.estado = 'walking'
        else:
            self.estado = 'idle'

        # ============================
        # 1. MOVIMIENTO HORIZONTAL
        # ============================
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidad_x
            self.direccion = -1
        if teclas[pygame.K_RIGHT] and self.rect.right < self.ancho_max:
            self.rect.x += self.velocidad_x
            self.direccion = 1

        # Colisión horizontal (solo bloquear paredes verticales)
        if paredes:
            for p in paredes:
                if self.rect.colliderect(p):
                    self.rect.x = x_ant  # revertir solo X
                    break

        # ============================
        # 2. MOVIMIENTO VERTICAL (GRAVEDAD)
        # ============================
        if self.con_gravedad:

            # SALTO
            if teclas[pygame.K_SPACE] and self.en_suelo:
                self.velocidad_y = self.fuerza_salto
                self.en_suelo = False

            # APLICAR GRAVEDAD
            self.velocidad_y += self.gravedad
            self.rect.y += self.velocidad_y

            # COLISIÓN CON EL SUELO GLOBAL
            if self.rect.bottom >= self.suelo_y:
                self.rect.bottom = self.suelo_y
                self.velocidad_y = 0
                self.en_suelo = True

            # COLISIONES VERTICALES CORRECTAS
            if paredes:
                for p in paredes:
                    if self.rect.colliderect(p):

                        # CAYENDO → PISO
                        if self.velocidad_y > 0:
                            self.rect.bottom = p.top
                            self.velocidad_y = 0
                            self.en_suelo = True

                        # SUBIENDO → TECHO
                        elif self.velocidad_y < 0:
                            self.rect.top = p.bottom
                            self.velocidad_y = 0

        else:
            # Movimiento sin gravedad
            if teclas[pygame.K_UP] and self.rect.top > 0:
                self.rect.y -= self.velocidad_x
            if teclas[pygame.K_DOWN] and self.rect.bottom < 700:
                self.rect.y += self.velocidad_x

            # Colisiones sin gravedad
            if paredes:
                if any(self.rect.colliderect(p) for p in paredes):
                    self.rect.x, self.rect.y = x_ant, y_ant

        # LIMITE DEL MAPA
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.ancho_max:
            self.rect.right = self.ancho_max
        if self.rect.top < limite_superior:
            self.rect.top = limite_superior
        if self.rect.bottom > limite_inferior:
            self.rect.bottom = limite_inferior


    def animar(self):
        ahora = pygame.time.get_ticks()
        vel_anim = self.velocidad_animacion_walking if self.estado in ['walking', 'walking_up', 'walking_down'] else self.velocidad_animacion_idle
        
        if ahora - self.tiempo_animacion > vel_anim:
            self.tiempo_animacion = ahora
            if self.tiene_frames:
                self.frame_actual = (self.frame_actual + 1) % len(self.frames_derecha)
                idx = 0 if self.estado == 'idle' else self.frame_actual

                if self.estado == 'walking':
                    self.imagen_actual = self.frames_izquierda[idx] if self.direccion == -1 else self.frames_derecha[idx]
                elif self.estado == 'walking_up':
                    self.imagen_actual = self.frames_arriba[idx]
                elif self.estado == 'walking_down':
                    self.imagen_actual = self.frames_abajo[idx]
                else:  # idle
                    self.imagen_actual = self.frames_derecha[0]  # Frame estático
            else:
                # Fallback: Flip para dirección (solo para horizontal)
                if self.estado == 'walking':
                    if self.direccion == -1:
                        self.imagen_actual = pygame.transform.flip(self.imagen_estatica, True, False)
                    else:
                        self.imagen_actual = self.imagen_estatica
                else:
                    self.imagen_actual = self.imagen_estatica
    
    def dibujar(self, superficie):
        self.animar()
        pos_x = self.rect.x + (self.rect.width - self.imagen_actual.get_width()) // 2
        pos_y = self.rect.bottom - self.imagen_actual.get_height()
        superficie.blit(self.imagen_actual, (pos_x, pos_y))
        pygame.draw.rect(superficie, (0, 255, 0), self.rect, 2)

def dialogo1():
    ancho = 1200
    alto = 700
    ventana =pygame.display.set_mode((ancho,alto))
    pygame.display.set_caption("julioxromario")
    
    fondo = pygame.image.load("comic imgs/introduccion comic.png")
    fondo = pygame.transform.scale(fondo,(ancho,alto))
    
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    l1()
        
        ventana.blit(fondo,(0,0))
        clock.tick(60)
        pygame.display.update()
        


def menulevels():
    pygame.mixer.music.stop()
    ancho = 1200
    alto = 700
    ventana = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("ml")

    botones_ancho, botones_alto = 450, 120

    fondo = pygame.image.load("imgs/menulevels.jpg")
    fondo = pygame.transform.scale(fondo, (ancho, alto))

    # Cargar imágenes normales y presionadas
    boton_level1_normal = pygame.image.load("imgs/boton_level1.png")
    boton_level1_normal = pygame.transform.scale(boton_level1_normal, (botones_ancho, botones_alto))
    boton_level1_presionado = pygame.image.load("imgs/boton_level1p.png")
    boton_level1_presionado = pygame.transform.scale(boton_level1_presionado, (botones_ancho, botones_alto))
    boton_level2_normal = pygame.image.load("imgs/boton_level2.png")
    boton_level2_normal = pygame.transform.scale(boton_level2_normal, (botones_ancho, botones_alto))
    boton_level2_presionado = pygame.image.load("imgs/boton_level2p.png")  
    boton_level2_presionado = pygame.transform.scale(boton_level2_presionado, (botones_ancho, botones_alto))
    boton_level3_normal = pygame.image.load("imgs/boton_level3.png") 
    boton_level3_normal = pygame.transform.scale(boton_level3_normal, (botones_ancho, botones_alto))
    boton_level3_presionado = pygame.image.load("imgs/boton_level3p.png")  
    boton_level3_presionado = pygame.transform.scale(boton_level3_presionado, (botones_ancho, botones_alto))

    
    centro_x = ancho // 2
    botonl1 = pygame.Rect(centro_x - botones_ancho // 2, 100, botones_ancho, botones_alto)
    botonl2 = pygame.Rect(centro_x - botones_ancho // 2, 300, botones_ancho, botones_alto)
    botonl3 = pygame.Rect(centro_x - botones_ancho // 2, 500, botones_ancho, botones_alto)
    # Estados para botones presionados
    level1_presionado = False
    level2_presionado = False
    level3_presionado = False

    x1 = 0
    x2 = ancho
    velocidad = 2 

    clock = pygame.time.Clock()

    while True:
        mouse_pos = pygame.mouse.get_pos()  # Obtener posición del mouse una vez por frame

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return()  # Regresa al menú principal
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Clic izquierdo abajo
                if botonl1.collidepoint(mouse_pos):
                    level1_presionado = True
                elif botonl2.collidepoint(mouse_pos):
                    level2_presionado = True
                elif botonl3.collidepoint(mouse_pos):
                    level3_presionado = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # Clic izquierdo up
                if level1_presionado and botonl1.collidepoint(mouse_pos):
                    dialogo1()  # Acción para nivel 1
                elif level2_presionado and botonl2.collidepoint(mouse_pos):
                    dialogo1()  # Acción para nivel 2 
                elif level3_presionado and botonl3.collidepoint(mouse_pos):
                    dialogo1()  # Acción para nivel 3 
                # Resetear estados
                level1_presionado = False
                level2_presionado = False
                level3_presionado = False
                    
        x1 -= velocidad
        x2 -= velocidad
        if x1 <= -ancho:
            x1 = x2 + ancho
        if x2 <= -ancho:
            x2 = x1 + ancho
        
        ventana.blit(fondo, (x1, 0))
        ventana.blit(fondo, (x2, 0))

        # botones con hover y presionado
        # Botón nivel 1
        if level1_presionado:
            ventana.blit(boton_level1_presionado, (botonl1.x, botonl1.y))
        elif botonl1.collidepoint(mouse_pos):
            hover_l1 = pygame.transform.scale(boton_level1_normal, (botones_ancho + 10, botones_alto + 5))
            ventana.blit(hover_l1, (botonl1.x - 5, botonl1.y - 2.5))
        else:
            ventana.blit(boton_level1_normal, (botonl1.x, botonl1.y))

        # Botón nivel 2
        if level2_presionado:
            ventana.blit(boton_level2_presionado, (botonl2.x, botonl2.y))
        elif botonl2.collidepoint(mouse_pos):
            hover_l2 = pygame.transform.scale(boton_level2_normal, (botones_ancho + 10, botones_alto + 5))
            ventana.blit(hover_l2, (botonl2.x - 5, botonl2.y - 2.5))
        else:
            ventana.blit(boton_level2_normal, (botonl2.x, botonl2.y))

        # Botón nivel 3
        if level3_presionado:
            ventana.blit(boton_level3_presionado, (botonl3.x, botonl3.y))
        elif botonl3.collidepoint(mouse_pos):
            hover_l3 = pygame.transform.scale(boton_level3_normal, (botones_ancho + 10, botones_alto + 5))
            ventana.blit(hover_l3, (botonl3.x - 5, botonl3.y - 2.5))
        else:
            ventana.blit(boton_level3_normal, (botonl3.x, botonl3.y))

        pygame.display.flip()
        clock.tick(60)


def regresar_al_hub():
    
    
    l1()
def reinicio():
    ancho = 1200
    alto = 700
    ventana = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("julioxromario")
    
    fondo = pygame.image.load("imgs/dialogo reiniciar.png")
    fondo = pygame.transform.scale(fondo, (ancho, alto))
    
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    videojuego()
        
        ventana.blit(fondo, (0, 0))
        pygame.display.update()
        clock.tick(60)


def dialogo2():
    ancho = 1200
    alto = 700
    ventana =pygame.display.set_mode((ancho,alto))
    pygame.display.set_caption("dialog2")
    
    fondo = pygame.image.load("imgs/d2.png")
    fondo = pygame.transform.scale(fondo,(ancho,alto))
    
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    videojuego()
        
        ventana.blit(fondo,(0,0))
        clock.tick(60)
        pygame.display.update()
        
def dialogo_final():
    ancho = 1200
    alto = 700
    ventana =pygame.display.set_mode((ancho,alto))
    pygame.display.set_caption("julioxromario")
    
    fondo = pygame.image.load("imgs/dialogo final l2.png")
    fondo = pygame.transform.scale(fondo,(ancho,alto))
    
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    level2()
        
        ventana.blit(fondo,(0,0))
        clock.tick(60)
        pygame.display.update()


def l1():
    
    ancho = 1200
    alto = 700
    ventana = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("nivel_principal")
    black = (0, 0, 0)
    white = (255, 255, 255)
    fondo = pygame.image.load("imgs/pul.png")
    fondo = pygame.transform.scale(fondo, (ancho, alto))
    

    global personaje_elegido
    personaje = Jugador(180,10,80,80, con_gravedad=False, personaje=personaje_elegido)
    personaje.velocidad_x = 6
    
    fuente = pygame.font.SysFont(None, 50)
    blanco = (255, 255, 255) 
    salida = pygame.Rect(192.91,0.09,58.91,4.55)
    pared = [
        pygame.Rect(189.47, 1.10, 2.74, 142.93),
        pygame.Rect(47, 239, 145, 11),
        pygame.Rect(182, 253, 13, 167),
        pygame.Rect(202, 427, 392, 12),
        pygame.Rect(252.97, 355.07, 338.31, 13.72),
        pygame.Rect(580.62, 440.41, 12.19, 115.82),
        pygame.Rect(649.19, 328.41, 12.19, 179.82),
        pygame.Rect(662.91, 496.80, 275.07, 10.67),
        pygame.Rect(595.09, 557.76, 398.51, 8.38),
        pygame.Rect(991.31, 480.80, 6.10, 84.58),
        pygame.Rect(252.97, 1.52, 18.29, 358.12),
        pygame.Rect(101.64, 170.85, 2.42, 17.42),
        pygame.Rect(104.54, 180.52, 87.60, 5.81),
        pygame.Rect(186.33, 144.23, 5.32, 34.36),
        pygame.Rect(587.55, 269.09, 7.26, 85.66),
        pygame.Rect(649.99, 260.38, 10.16, 65.82),
        pygame.Rect(930.69, 439.94, 5.32, 51.79),
        pygame.Rect(933.11, 381.38, 2.90, 112.28),
        pygame.Rect(991.68, 383.31, 7.26, 97.28),
        pygame.Rect(42.99, 97.45, 3.58, 134.71),
        pygame.Rect(101.75, 96.02, 15.76, 81.69),
    ]
#hasta aqui!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    puerta1 = pygame.Rect(56.40, 103.50, 37.24, 36.69)
    puerta2 = pygame.Rect(602.92, 255.74, 37.79, 35.59)
    puerta3 = pygame.Rect(945.70, 386.22, 36.78, 35.81)
    puerta4 = pygame.Rect(606, 130, 90, 40)
    puerta5 = pygame.Rect(950, 130, 130, 40)
    puerta_exit = pygame.Rect(550, 690, 180, 20)

    red = (255, 0, 0)
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menulevels()  
                
        teclas = pygame.key.get_pressed()
        personaje.actualizar(teclas, paredes=pared)  
        
        if personaje.rect.colliderect(puerta1):
            level2()
            return
        if personaje.rect.colliderect(puerta2):
            level3()
            return
        if personaje.rect.colliderect(puerta3):
            level4()
            return
        if personaje.rect.colliderect(puerta_exit):
            menulevels()
            
        if personaje.rect.colliderect(salida):
            level2_parte1()
            return
            
        
        ventana.blit(fondo, (0, 0))
        #texto = fuente.render(f"sillas: {contador_sillas}", True, blanco)
        #ventana.blit(texto, (20, 100))
        #for p in pared:
            #pygame.draw.rect(ventana, red, p)
        #pygame.draw.rect(ventana, red, puerta1)  
        #pygame.draw.rect(ventana, red, puerta2)
        #pygame.draw.rect(ventana, red, puerta3)  
        pygame.draw.rect(ventana,red,salida)
        personaje.dibujar(ventana)
        pygame.display.flip()
        clock.tick(60)
def level2():
    

    
    ancho, alto = 1200, 700
    ventana = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("minilevel 2")

    # Jugador con animaciones y gravedad
    global personaje_elegido
    jugador = Jugador(600.38, 480, 100, 120, con_gravedad=False, personaje=personaje_elegido, ancho_max=ancho) 
    velo =30
    fondo = pygame.image.load("imgs/nuevo l2.png")
    fondo = pygame.transform.scale(fondo, (ancho, alto))
    red = (255,0,0,0)
    pared = [
    pygame.Rect(340.70,39.91,279.36,93.86),
    pygame.Rect(642.97,38.43,114.55,90.16),
    pygame.Rect(777.47,38.43,72.43,92.38),
    pygame.Rect(561.67,203.98,147.07,180.33),
    pygame.Rect(355.48,383.56,50.99,53.95),
    pygame.Rect(356.96,229.84,50.25,51.73),
    pygame.Rect(339.22,468.55,70.21,126.38),
    pygame.Rect(842.51,390.22,47.30,48.78),
    pygame.Rect(841.77,231.32,48.04,50.25),
    pygame.Rect(315.87,628.41,212.43,25.58),
    pygame.Rect(724.06,628.41,211.32,24.47),
    pygame.Rect(314.76,31.14,22.24,608.39),
    pygame.Rect(911.47,33.49,24.75,596.97),
    pygame.Rect(307.22,33.49,631.92,16.02),
    
    
    
]
    
    puerta = pygame.Rect(531.09,614.40,188.93,59.51)
    dialogo1 = pygame.Rect(613.46,382.28,47.79,25.83)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # Regresa al hub
                if event.key == pygame.K_SPACE and jugador.en_suelo:
                    jugador.velocidad_y = jugador.fuerza_salto
                    jugador.en_suelo = False
        if jugador.rect.colliderect(puerta):
            l1()
            return
        if jugador.rect.colliderect(dialogo1):
            dialogo2()
            return
        teclas = pygame.key.get_pressed()
        jugador.actualizar(teclas,paredes=pared)


        ventana.fill((0, 0, 0))
        ventana.blit(fondo, (0, 0))
        
        jugador.dibujar(ventana)
        pygame.draw.rect(ventana,red,dialogo1)
        pygame.display.flip()
        clock.tick(60)
import random
import pygame
import sys

pygame.init()

def videojuego():
    ancho = 1200
    alto = 700
    ventana = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("minilevel 2")
    
    global personaje_elegido
    jugador = Jugador(486.86, 400, 100, 120, con_gravedad=False, personaje=personaje_elegido, ancho_max=ancho,ancho_hitbox=60,alto_hitbox=100)

    fondo = pygame.image.load("imgs/fondo def videojuego.png")
    fondo = pygame.transform.scale(fondo, (ancho, alto))

    misil_img = pygame.image.load("imgs/misil.png")
    misil_img = pygame.transform.scale(misil_img, (30, 70))

    velocidad_y = 0
    gravedad = 1
    fuerza_salto = -18
    piso = 580
    en_suelo = True

    objetos = []
    daño = 0
    fuente = pygame.font.SysFont(None, 40)

    tiempo_inicio = pygame.time.get_ticks()
    pared = 0

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and en_suelo:
                    velocidad_y = fuerza_salto
                    en_suelo = False

        teclas = pygame.key.get_pressed()
        jugador.actualizar(teclas, paredes=pared)

        jugador.rect.y += velocidad_y
        velocidad_y += gravedad

        if jugador.rect.y >= piso:
            jugador.rect.y = piso
            velocidad_y = 0
            en_suelo = True

        if random.randint(0, 20) == 0:
            x = random.randint(0, ancho - 30)
            rect = misil_img.get_rect(topleft=(x, 0))
            objetos.append(rect)

        tiempo_actual = pygame.time.get_ticks()
        segundos = (tiempo_actual - tiempo_inicio) // 1000

        if segundos >= 30:
            dialogo_final()
            return

        ventana.blit(fondo, (0, 0))
        jugador.dibujar(ventana)

        texto_daño = fuente.render(f"Daño: {daño}%", True, (255, 255, 255))
        ventana.blit(texto_daño, (20, 20))

        texto_tiempo = fuente.render(f"Tiempo: {segundos}s", True, (255, 255, 255))
        ventana.blit(texto_tiempo, (20, 60))

        for obj in objetos[:]:
            obj.y += 5
            ventana.blit(misil_img, obj)

            if jugador.rect.colliderect(obj):
                objetos.remove(obj)
                daño += 20
                if daño > 100:
                    daño = 100
                    reinicio()
                    return

            if obj.top > alto:
                objetos.remove(obj)

        pygame.display.flip()
        clock.tick(60)




        
def dialogo1_l3():
    ancho = 1200
    alto = 700
    ventana =pygame.display.set_mode((ancho,alto))
    
    fondo = pygame.image.load("imgs/d1l3.png")
    fondo = pygame.transform.scale(fondo,(ancho,alto))
    
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dialogo2_l3()
        
        ventana.blit(fondo,(0,0))
        clock.tick(60)
        pygame.display.update()
        
def dialogo2_l3():
    ancho = 1200
    alto = 700
    ventana =pygame.display.set_mode((ancho,alto))
    
    fondo = pygame.image.load("imgs/d2l3.png")
    fondo = pygame.transform.scale(fondo,(ancho,alto))
    
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    level3()
        
        ventana.blit(fondo,(0,0))
        clock.tick(60)
        pygame.display.update()

def dialogo3_l3():
    ancho = 1200
    alto = 700
    ventana =pygame.display.set_mode((ancho,alto))
    
    fondo = pygame.image.load("imgs/d3l3.png")
    fondo = pygame.transform.scale(fondo,(ancho,alto))
    
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dialogo4_l3()
        
        ventana.blit(fondo,(0,0))
        clock.tick(60)
        pygame.display.update()
        
def dialogo4_l3():
    ancho = 1200
    alto = 700
    ventana =pygame.display.set_mode((ancho,alto))
    
    fondo = pygame.image.load("imgs/d4l3.png")
    fondo = pygame.transform.scale(fondo,(ancho,alto))
    
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    level3()
        
        ventana.blit(fondo,(0,0))
        clock.tick(60)
        pygame.display.update()


        
def level3():

    ancho, alto = 1200, 700
    ventana = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("minilevel 2")

    global personaje_elegido
    jugador = Jugador(486.86,400, 100, 120, con_gravedad=False, personaje=personaje_elegido, ancho_max=ancho)
    velo =30
    fondo = pygame.image.load("imgs/fondo nuevo bebe.png")
    fondo = pygame.transform.scale(fondo, (ancho, alto))
    pared = 0
    clock = pygame.time.Clock()
    pared = [
        pygame.Rect(38.09,320.58,637.20,57.13),
        pygame.Rect(42.43,445.62,63.95,10.48),
        pygame.Rect(107.92,378.51,41.26,103.95,),
        pygame.Rect(160.81,428.21,150.85,79.30),
        pygame.Rect(320.20,379.93,41.75,102.08),
        pygame.Rect(371.23,444.46,59.75,15.72),
        pygame.Rect(438.03,424.54,63.48,69.04),
        pygame.Rect(506.96,449.55,56.61,10.48),
        pygame.Rect(569.75,383.27,104.08,108.71),
        pygame.Rect(17.35,650.38,435.37,12.52),
        pygame.Rect(396.84,659.80,51.05,36.60),
        pygame.Rect(10.60,22.15,18.30,615.49),
        pygame.Rect(38.78,284.40,637.37,24.73),
        pygame.Rect(610.67,645.35,44.31,39.49),
        pygame.Rect(657.87,671.35,528.80,19.26),
        pygame.Rect(1174.92,10.54,11.85,659.91),
        
        
        pygame.Rect(685.00,19.67,57.00,113.67),
    
   
        
        
    ]
    
    
    abrir_dialogo = pygame.Rect(369.21,485.34,60.07,76.09)
    
    foto = pygame.Rect(561.52,67.63,61.43,57.70)
    
    red = (255,0,0)
    
    puerta = pygame.Rect(457.62,678.24,143.73,17.29)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # Regresa al hub
                if event.key == pygame.K_SPACE and jugador.en_suelo:
                    jugador.velocidad_y = jugador.fuerza_salto
                    jugador.en_suelo = False
        if jugador.rect.colliderect(puerta):
            l1()
            return
        
        if jugador.rect.colliderect(abrir_dialogo):
            dialogo1_l3()
            return
        if jugador.rect.colliderect(foto):
            dialogo3_l3()
            return
        
        teclas = pygame.key.get_pressed()
        jugador.actualizar(teclas,paredes=pared)
        

        ventana.fill((0, 0, 0))
        ventana.blit(fondo, (0, 0))
        for p in pared:
            pygame.draw.rect(ventana,red,p)
        jugador.dibujar(ventana)
        pygame.display.flip()
        clock.tick(60)

def level4():
    
    ancho = 1200
    alto = 700
    ventana = pygame.display.set_mode((ancho, alto))
    global personaje_elegido
    jugador = Jugador(486.86,400, 100, 120, con_gravedad=False, personaje=personaje_elegido, ancho_max=ancho)
    
    fondo = pygame.image.load("imgs/level 3 nueva.png")
    fondo = pygame.transform.scale(fondo, (ancho, alto))
    pared = [
        pygame.Rect(312.67,20.67,140.00,108.00),
        pygame.Rect(312.67,20.67,140.00,108.00),
        pygame.Rect(524.00,296.00,142.00,80.00),
        pygame.Rect(463.33,39.33,222.00,118.67),
        pygame.Rect(469.33,104.00,64.00,107.33),
        pygame.Rect(783.00,113.33,49.67,44.67),
        pygame.Rect(793.67,43.33,26.67,71.00),
        pygame.Rect(762.00,35.67,94.33,62.67),
        pygame.Rect(782.67,536.67,49.00,46.00),
        pygame.Rect(795.33,468.33,25.00,70.33),
        pygame.Rect(762.33,460.00,94.33,62.33),
        pygame.Rect(257.33,6.00,674.50,46.17),
        pygame.Rect(714.50,602.50,218.00,45.00),
        pygame.Rect(258.00,602.50,193.50,45.50),
        pygame.Rect(255.00,3.00,51.00,644.00),
        pygame.Rect(887.00,0.00,47.00,650.00)
    ]
    red = (255,0,0)
    
    puerta = pygame.Rect(453.00,629.50,263.50,21.00)
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        teclas = pygame.key.get_pressed()
        jugador.actualizar(teclas,paredes=pared)
        
        if jugador.rect.colliderect(puerta):
            l1()
            return
        
        
        ventana.blit(fondo, (0, 0))
        jugador.dibujar(ventana)
        #for p in pared:
        # pygame.draw.rect(ventana,red,p)
        pygame.display.update()
        clock.tick(60)

import pygame
pygame.init()

def level2_parte1():
    ANCHO_WIN, ALTO_WIN = 1400, 800
    ventana = pygame.display.set_mode((ANCHO_WIN, ALTO_WIN))
    fondo = pygame.image.load("imgs/f.png").convert()

    ANCHO_MAPA, ALTO_MAPA = fondo.get_width(), fondo.get_height()

    jugador = Jugador(
        600.38, 480, 100, 120,
        con_gravedad=True,
        personaje=personaje_elegido,
        ancho_max=ANCHO_MAPA,
        ancho_hitbox=50,
        alto_hitbox=80
    )
    jugador.suelo_y = 622
    jugador.fuerza_salto = -23

    pared = [
        pygame.Rect(290, 527, 82, 80),
        pygame.Rect(608, 498, 14, 82),
        pygame.Rect(596, 564, 37, 40),
        pygame.Rect(825, 561, 22, 42),
        pygame.Rect(1200, 519, 60, 89),
        pygame.Rect(1497, 559, 44, 50),
        pygame.Rect(1511, 514, 17, 71),
        pygame.Rect(1552, 528, 51, 80),
        pygame.Rect(1798, 516, 65, 93),
        pygame.Rect(1864, 526, 80, 81),
    ]

    clock = pygame.time.Clock()
    run = True
    contador_vida = 0
    colisionando = False  # Flag para evitar contar múltiples veces por colisión continua

    while run:
        clock.tick(60)

        teclas = pygame.key.get_pressed()
        # Actualizar con paredes y límites del mapa integrados
        jugador.actualizar(teclas, paredes=pared, limite_inferior=ALTO_MAPA)

        # Chequear colisiones para contador de vida (solo primera vez por colisión)
        colision_actual = any(jugador.rect.colliderect(p) for p in pared)
        if colision_actual and not colisionando:
            contador_vida += 1
            colisionando = True
        elif not colision_actual:
            colisionando = False  # Resetear cuando deja de colisionar

        if contador_vida >= 3:
            l1()
            return

        # Cámara (calculada después de actualizar)
        cam_x = jugador.rect.x - ANCHO_WIN // 2
        cam_y = jugador.rect.y - ALTO_WIN // 2
        cam_x = max(0, min(cam_x, ANCHO_MAPA - ANCHO_WIN))
        cam_y = max(0, min(cam_y, ALTO_MAPA - ALTO_WIN))

        ventana.blit(fondo, (-cam_x, -cam_y))

        # Dibujar paredes para debug
        for p in pared:
            pygame.draw.rect(ventana, (255, 0, 0), (p.x - cam_x, p.y - cam_y, p.width, p.height))

        # Dibujar jugador (ajuste temporal para pantalla)
        temp_x, temp_y = jugador.rect.x, jugador.rect.y
        jugador.rect.x -= cam_x
        jugador.rect.y -= cam_y
        jugador.dibujar(ventana)
        jugador.rect.x, jugador.rect.y = temp_x, temp_y  # Restaurar posición del mundo

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()