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
    def __init__(self, x, y, width, height, con_gravedad=False, personaje='p1', ancho_max=1200):
        ancho_hitbox = 20
        alto_hitbox = 30

        
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
        self.estado = 'idle'  # 'idle' o 'walking'
        self.con_gravedad = con_gravedad
        self.personaje = personaje
        self.ancho_max = ancho_max  # Para límites horizontales
        
        # Cargar frames para este personaje (de personajes.py)
        frames_p1, frames_p2 = cargar_frames()
        frames_globales = {'p1': frames_p1, 'p2': frames_p2}
        self.frames = frames_globales[self.personaje]  # ([derecha], [izquierda])
        
        self.frames_derecha = [pygame.transform.scale(f, (width, height)) for f in self.frames[0]]
        self.frames_izquierda = [pygame.transform.scale(f, (width, height)) for f in self.frames[1]]
        
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
    
    def actualizar(self, teclas, paredes=None):
        x_ant, y_ant = self.rect.x, self.rect.y
        moviendo_horizontal = False
        moviendo_vertical = False


        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidad_x
            self.direccion = -1
            moviendo_horizontal = True
        if teclas[pygame.K_RIGHT] and self.rect.right < self.ancho_max:
            self.rect.x += self.velocidad_x
            self.direccion = 1
            moviendo_horizontal = True

        if self.con_gravedad:
            
            if teclas[pygame.K_SPACE] and self.en_suelo:
                self.velocidad_y = self.fuerza_salto
                self.en_suelo = False
            
            self.velocidad_y += self.gravedad
            self.rect.y += self.velocidad_y

            if self.rect.bottom >= self.suelo_y:
                self.rect.bottom = self.suelo_y
                self.velocidad_y = 0
                self.en_suelo = True

            if paredes:
                for p in paredes:
                    if self.rect.colliderect(p) and self.velocidad_y >= 0:
                        self.rect.bottom = p.top
                        self.velocidad_y = 0
                        self.en_suelo = True
                if any(self.rect.colliderect(p) for p in paredes):
                    self.rect.x, self.rect.y = x_ant, y_ant
        else:
            # Movimiento vertical libre (solo si no hay gravedad)
            if teclas[pygame.K_UP] and self.rect.top > 0:
                self.rect.y -= self.velocidad_x
                moviendo_vertical = True
            if teclas[pygame.K_DOWN] and self.rect.bottom < 700:  # Ajusta alto si es distinto
                self.rect.y += self.velocidad_x
                moviendo_vertical = True
                
            if paredes:
                if any(self.rect.colliderect(p) for p in paredes):
                    self.rect.x, self.rect.y = x_ant, y_ant

        # Estado de animación
        if moviendo_horizontal:
            self.estado = 'walking'
        else:
            self.estado = 'idle'

    
    def animar(self):
        ahora = pygame.time.get_ticks()
        vel_anim = self.velocidad_animacion_walking if self.estado == 'walking' else self.velocidad_animacion_idle
        
        if ahora - self.tiempo_animacion > vel_anim:
            self.tiempo_animacion = ahora
            if self.tiene_frames:
                self.frame_actual = (self.frame_actual + 1) % len(self.frames_derecha)
                
                if self.estado == 'idle':
                    idx = 0  # Frame estático para idle
                else:
                    idx = self.frame_actual  # Ciclo para walking
                
                if self.direccion == -1:
                    self.imagen_actual = self.frames_izquierda[idx]
                else:
                    self.imagen_actual = self.frames_derecha[idx]
            else:
                # Fallback: Flip para dirección
                if self.direccion == -1:
                    self.imagen_actual = pygame.transform.flip(self.imagen_estatica, True, False)
                else:
                    self.imagen_actual = self.imagen_estatica
    
    def dibujar(self, superficie):
        self.animar()
        
        
        
        pos_x = self.rect.x + (self.rect.width - self.imagen_actual.get_width()) // 2
        pos_y = self.rect.bottom - self.imagen_actual.get_height()
        superficie.blit(self.imagen_actual, (pos_x, pos_y))
        
        
        
        
        pygame.draw.rect(superficie, (0, 255, 0), self.rect, 2)

def mainmenu():
    ancho = 1200
    alto = 700
    ancho_botones = 300
    alto_botones = 100

    ventana = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("integrador equipo 6")

    fondo = pygame.image.load("imgs/img.jpg")
    fondo = pygame.transform.scale(fondo, (ancho, alto))
    botones = pygame.image.load("imgs/boton inicio.png")
    botones = pygame.transform.scale(botones, (ancho_botones, alto_botones))
    configuracion = pygame.image.load("imgs/boton configuracion.png")
    configuracion = pygame.transform.scale(configuracion, (ancho_botones, alto_botones))

    boton_inicio_rect = pygame.Rect(450, 300, ancho_botones, alto_botones)

    x1 = 0
    x2 = ancho
    velocidad = 2 
    reloj = pygame.time.Clock()
    ejecutar = True

    while ejecutar:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejecutar = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
                if boton_inicio_rect.collidepoint(event.pos):  
                    menulevels()   

        x1 -= velocidad
        x2 -= velocidad

        if x1 <= -ancho:
            x1 = x2 + ancho
        if x2 <= -ancho:
            x2 = x1 + ancho

        ventana.blit(fondo, (x1, 0))
        ventana.blit(fondo, (x2, 0))
        ventana.blit(botones, (450, 300))
        ventana.blit(configuracion, (450, 450))

        pygame.display.flip()
        reloj.tick(60)  

    pygame.quit()
    sys.exit()
    
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

    botones_ancho, botones_alto = 300, 100

    fondo = pygame.image.load("imgs/menulevels.jpg")
    fondo = pygame.transform.scale(fondo, (ancho, alto))

    boton_level1 = pygame.image.load("imgs/boton level1.png")
    boton_level1 = pygame.transform.scale(boton_level1, (botones_ancho, botones_alto))

    botonl1 = pygame.Rect(450, 100, botones_ancho, botones_alto)

    x1 = 0
    x2 = ancho
    velocidad = 2 

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainmenu()  # Regresa al menú principal
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if botonl1.collidepoint(event.pos):
                    dialogo1()
                    
        x1 -= velocidad
        x2 -= velocidad
        if x1 <= -ancho:
            x1 = x2 + ancho
        if x2 <= -ancho:
            x2 = x1 + ancho
        
        ventana.blit(fondo, (x1, 0))
        ventana.blit(fondo, (x2, 0))
        ventana.blit(boton_level1, (botonl1.x, botonl1.y))
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
    pygame.display.set_caption("julioxromario")
    
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
    
    # Jugador con animaciones (movimiento libre, sin gravedad)
    global personaje_elegido
    personaje = Jugador(180,10,80,80, con_gravedad=False, personaje=personaje_elegido)
    personaje.velocidad_x = 6
    
    fuente = pygame.font.SysFont(None, 50)
    blanco = (255, 255, 255) 
    #coliciones para Abril------------------------------------------------
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
        if personaje.rect.colliderect(puerta4):
            level5()
            return
        if personaje.rect.colliderect(puerta5):
            level6()
            return
        if personaje.rect.colliderect(puerta_exit):
            menulevels()
        
        ventana.blit(fondo, (0, 0))
        texto = fuente.render(f"sillas: {contador_sillas}", True, blanco)
        ventana.blit(texto, (20, 100))
        #for p in pared:
            #pygame.draw.rect(ventana, red, p)
        #pygame.draw.rect(ventana, red, puerta1)  
        #pygame.draw.rect(ventana, red, puerta2)
        #pygame.draw.rect(ventana, red, puerta3)  
        personaje.dibujar(ventana)
        pygame.display.flip()
        clock.tick(60)
def level2():
    

    
    ancho, alto = 1200, 700
    ventana = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("minilevel 2")

    # Jugador con animaciones y gravedad
    global personaje_elegido
    jugador = Jugador(600.38,480, 100, 120, con_gravedad=False, personaje=personaje_elegido, ancho_max=ancho)
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
    
    fondo = pygame.image.load("imgs/fondo def videojuego.png")
    fondo = pygame.transform.scale(fondo,(ancho,alto))

    img_jugador = pygame.image.load("imgs/player.png")
    img_jugador = pygame.transform.scale(img_jugador, (60, 80))
    jugador = img_jugador.get_rect(center=(600, 600))

    misil_img = pygame.image.load("imgs/misil.png")
    misil_img = pygame.transform.scale(misil_img, (30, 70))

    velocidad = 15
    velocidad_y = 0
    gravedad = 1
    fuerza_salto = -15
    en_suelo = True
    suelo_y = 690

    objetos = []

    daño = 0
    fuente = pygame.font.SysFont(None, 40)

    tiempo_inicio = pygame.time.get_ticks()

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

        velocidad_y += gravedad
        jugador.y += velocidad_y
        if jugador.y >= suelo_y - jugador.height:
            jugador.y = suelo_y - jugador.height
            velocidad_y = 0
            en_suelo = True   

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and jugador.left > 0:
            jugador.x -= velocidad   
        if teclas[pygame.K_RIGHT] and jugador.right < ancho:
            jugador.x += velocidad 
        if teclas[pygame.K_UP] and jugador.top > 0:
            jugador.y -= velocidad
        if teclas[pygame.K_DOWN] and jugador.bottom < alto:
            jugador.y += velocidad

        if random.randint(0, 20) == 0:
            x = random.randint(0, ancho - 30)
            rect = misil_img.get_rect(topleft=(x, 0))
            objetos.append(rect)

        tiempo_actual = pygame.time.get_ticks()
        segundos = (tiempo_actual - tiempo_inicio) // 1000

        if segundos >= 30:
            dialogo_final()
            return

        ventana.blit(fondo,(0,0))
        ventana.blit(img_jugador, jugador)

        texto_daño = fuente.render(f"Daño: {daño}%", True, (255, 255, 255))
        ventana.blit(texto_daño, (20, 20))

        texto_tiempo = fuente.render(f"Tiempo: {segundos}s", True, (255, 255, 255))
        ventana.blit(texto_tiempo, (20, 60))

        for obj in objetos[:]:
            obj.y += 5
            ventana.blit(misil_img, obj)

            if jugador.colliderect(obj):
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
        




        
        
        
def level3():

    ancho, alto = 1200, 700
    ventana = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("minilevel 2")

    # Jugador con animaciones y gravedad
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
        
   
        
        
    ]
    
    
    abrir_dialogo = pygame.Rect(369.21,485.34,60.07,76.09)
    
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
        
        teclas = pygame.key.get_pressed()
        jugador.actualizar(teclas,paredes=pared)

       

      

        ventana.fill((0, 0, 0))
        ventana.blit(fondo, (0, 0))
        jugador.dibujar(ventana)
        pygame.display.flip()
        clock.tick(60)

def level4():
    pygame.mixer.music.stop()
    ANCHO, ALTO = 1200, 700
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("level 4")

    fondo = pygame.image.load("imgs/l3img.png")
    fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
    NEGRO = (0, 0, 0)

    # Jugador con animaciones y gravedad
    global personaje_elegido
    jugador = Jugador(100, 600, 80, 80, con_gravedad=True, personaje=personaje_elegido, ancho_max=ANCHO)
    jugador.velocidad_x = 8
    jugador.fuerza_salto = -20
    jugador.suelo_y = ALTO - 50  # Suelo base

    global contador_sillas

    # Imágenes para objetos/enemigos
    objetos_esquivar_img = pygame.image.load("imgs/caja.png")
    objetos_esquivar_img = pygame.transform.scale(objetos_esquivar_img, (50, 50))  # Imagen más grande

    objetos_recoger_img = pygame.image.load("imgs/silla.png")
    objetos_recoger_img = pygame.transform.scale(objetos_recoger_img, (50, 50))  # Imagen más grande

    enemigos_img = pygame.image.load("imgs/fantasma.png")
    enemigos_img = pygame.transform.scale(enemigos_img, (40, 40))  # Fantasma más pequeño

    plataformas = [
        pygame.Rect(0, 650, ANCHO, 50),
        pygame.Rect(300, 500, 200, 20),
        pygame.Rect(700, 400, 200, 20),
    ]

    # Fantasmas
    enemigos = [pygame.Rect(random.randint(0, ANCHO-30), random.randint(0, 600), 30, 30) for _ in range(6)]
    velocidad_enemigo = 3

    objetos_recoger = []
    objetos_esquivar = []
    TIEMPO_OBJETO = pygame.USEREVENT + 1
    pygame.time.set_timer(TIEMPO_OBJETO, 1500)

    puntaje = 0
    contador_daño = 0
    ultimo_daño = 0
    fuente = pygame.font.SysFont(None, 36)

    reloj = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == TIEMPO_OBJETO:
                # Crear cajas
                for _ in range(random.randint(2, 3)):
                    x = random.randint(0, ANCHO-50)
                    hitbox_esquivar = pygame.Rect(x + 10, 0 + 10, 30, 30)  # Hitbox más pequeña y centrada
                    objetos_esquivar.append(hitbox_esquivar)
                # Crear sillas
                for _ in range(random.randint(1, 2)):
                    x = random.randint(0, ANCHO-50)
                    hitbox_recoger = pygame.Rect(x + 10, 0 + 10, 30, 30)
                    objetos_recoger.append(hitbox_recoger)

        teclas = pygame.key.get_pressed()
        jugador.actualizar(teclas, paredes=plataformas)

        # Límites de pantalla
        jugador.rect.left = max(jugador.rect.left, 0)
        jugador.rect.right = min(jugador.rect.right, ANCHO)
        jugador.rect.top = max(jugador.rect.top, 0)
        jugador.rect.bottom = min(jugador.rect.bottom, ALTO)

        # Actualizar enemigos
        for e in enemigos:
            if e.x < jugador.rect.x:
                e.x += velocidad_enemigo
            elif e.x > jugador.rect.x:
                e.x -= velocidad_enemigo
            if e.y < jugador.rect.y:
                e.y += velocidad_enemigo
            elif e.y > jugador.rect.y:
                e.y -= velocidad_enemigo
            # Limites de pantalla
            e.left = max(e.left, 0)
            e.right = min(e.right, ANCHO)
            e.top = max(e.top, 0)
            e.bottom = min(e.bottom, ALTO)

        tiempo_actual_ms = pygame.time.get_ticks()
        for e in enemigos:
            if jugador.rect.colliderect(e):
                if tiempo_actual_ms - ultimo_daño > 1000:
                    contador_daño += 1
                    ultimo_daño = tiempo_actual_ms

        # Actualizar objetos recoger
        for obj in objetos_recoger[:]:
            obj.y += 5
            if jugador.rect.colliderect(obj):
                puntaje += 1
                objetos_recoger.remove(obj)
            elif obj.y > ALTO:
                objetos_recoger.remove(obj)

        # Actualizar objetos esquivar
        for obj in objetos_esquivar[:]:
            obj.y += 5
            if jugador.rect.colliderect(obj):
                puntaje -= 1
                objetos_esquivar.remove(obj)
            elif obj.y > ALTO:
                objetos_esquivar.remove(obj)

        if puntaje >= 5:
            contador_sillas += 5
            regresar_al_hub()
            return

        if contador_daño >= 20:
            regresar_al_hub()
            return

        ventana.fill((0, 0, 0))
        ventana.blit(fondo, (0, 0))
        jugador.dibujar(ventana)
        for e in enemigos:
            ventana.blit(enemigos_img, (e.x, e.y))
        for plat in plataformas:
            pygame.draw.rect(ventana, NEGRO, plat)
        for e in objetos_esquivar:
            ventana.blit(objetos_esquivar_img, (e.x - 10, e.y - 10))  # Ajuste hitbox a imagen
        for e in objetos_recoger:
            ventana.blit(objetos_recoger_img, (e.x - 10, e.y - 10))

        texto = fuente.render(f"Puntaje: {puntaje}", True, NEGRO)
        ventana.blit(texto, (10, 10))
        texto_daño = fuente.render(f"Daño: {contador_daño}", True, (255, 0, 0))
        ventana.blit(texto_daño, (10, 50))

        pygame.display.update()
        reloj.tick(60)


def level5():
    ancho = 1200
    alto = 700
    ventana = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("mini level 5")

    # Jugador con animaciones (movimiento libre, sin gravedad)
    global personaje_elegido
    jugador = Jugador(600, 600, 30, 30, con_gravedad=False, personaje=personaje_elegido, ancho_max=ancho)
    jugador.velocidad_x = 15  # Velocidad para horizontal y vertical

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # Regresa al hub
        
        teclas = pygame.key.get_pressed()
        # Movimiento libre (horizontal y vertical)
        # Llama a actualizar() que ahora maneja horizontal y vertical y cambia estado
        jugador.actualizar(teclas)

# Luego dibuja (actualiza la animación dentro de dibujar)
        jugador.dibujar(ventana)  # Anima manualmente ya que no hay actualizar() para vertical
        
        ventana.fill((0, 0, 0))
        jugador.dibujar(ventana)  # Dibuja animado (no rect blanco)
        
        pygame.display.flip()
        clock.tick(60)

def level6():
    ancho = 1200
    alto = 700
    ventana = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("mini level 6")

    # Jugador con animaciones (movimiento libre, sin gravedad)
    global personaje_elegido
    jugador = Jugador(600, 600, 30, 30, con_gravedad=False, personaje=personaje_elegido, ancho_max=ancho)
    jugador.velocidad_x = 15  # Velocidad para horizontal y vertical

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # Regresa al hub
        
        teclas = pygame.key.get_pressed()
        # Movimiento libre (horizontal y vertical)
        if teclas[pygame.K_LEFT] and jugador.rect.left > 0:
            jugador.rect.x -= jugador.velocidad_x
            jugador.direccion = -1
        if teclas[pygame.K_RIGHT] and jugador.rect.right < ancho:
            jugador.rect.x += jugador.velocidad_x
            jugador.direccion = 1
        if teclas[pygame.K_UP] and jugador.rect.top > 0:
            jugador.rect.y -= jugador.velocidad_x
        if teclas[pygame.K_DOWN] and jugador.rect.bottom < alto:
            jugador.rect.y += jugador.velocidad_x
        
        # Actualiza estado para animación (solo horizontal)
        if teclas[pygame.K_LEFT] or teclas[pygame.K_RIGHT]:
            jugador.estado = 'walking'
        else:
            jugador.estado = 'idle'
        
        jugador.animar()  # Anima manualmente ya que no hay actualizar() para vertical
        
        ventana.fill((0, 0, 0))
        jugador.dibujar(ventana)  # Dibuja animado (no rect blanco)
        
        pygame.display.flip()
        clock.tick(60)

# Llamada final para ejecutar el juego
if __name__ == "__main__":
    mainmenu()
