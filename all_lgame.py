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
        self.rect = pygame.Rect(x, y, width, height)
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
        
        # Escalar frames al tamaño del jugador
        self.frames_derecha = [pygame.transform.scale(f, (width, height)) for f in self.frames[0]]
        self.frames_izquierda = [pygame.transform.scale(f, (width, height)) for f in self.frames[1]]
        
        # Fallback si no hay frames o error
        try:
            self.imagen_actual = self.frames_derecha[0]
            self.tiene_frames = True
        except Exception as e:
            self.imagen_estatica = pygame.image.load("imgs/personaje.png")
            self.imagen_estatica = pygame.transform.scale(self.imagen_estatica, (width, height))
            self.imagen_actual = self.imagen_estatica
            self.tiene_frames = False
            print(f"Advertencia: Usando imagen estática para {personaje}. Error: {e}")
        
        # Timing de animación
        self.frame_actual = 0
        self.tiempo_animacion = pygame.time.get_ticks()
        self.velocidad_animacion_walking = 150  # ms por frame
        self.velocidad_animacion_idle = 500
    
    def actualizar(self, teclas, paredes=None):
        x_ant, y_ant = self.rect.x, self.rect.y
        moviendo_horizontal = False
        moviendo_vertical = False

    # Movimiento horizontal
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidad_x
            self.direccion = -1
            moviendo_horizontal = True
        if teclas[pygame.K_RIGHT] and self.rect.right < self.ancho_max:
            self.rect.x += self.velocidad_x
            self.direccion = 1
            moviendo_horizontal = True

        if self.con_gravedad:
            # Salto
            if teclas[pygame.K_SPACE] and self.en_suelo:
                self.velocidad_y = self.fuerza_salto
                self.en_suelo = False
            # Gravedad
            self.velocidad_y += self.gravedad
            self.rect.y += self.velocidad_y

            if self.rect.bottom >= self.suelo_y:
                self.rect.bottom = self.suelo_y
                self.velocidad_y = 0
                self.en_suelo = True

            # Colisiones con paredes/plataformas
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
        superficie.blit(self.imagen_actual, (self.rect.x, self.rect.y))

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
                    l1()
                    
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
# Helper para regresar al hub (definida después de l1 para evitar error de definición)
def regresar_al_hub():
    l1()

def l1():
    pygame.mixer.music.stop()
    pygame.mixer.music.load("l3.WAV")
    pygame.mixer.music.play(-1)
    
    ancho = 1200
    alto = 700
    ventana = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("nivel_principal")
    black = (0, 0, 0)
    white = (255, 255, 255)
    fondo = pygame.image.load("imgs/nuevo mapa.png")
    fondo = pygame.transform.scale(fondo, (ancho, alto))
    
    # Jugador con animaciones (movimiento libre, sin gravedad)
    global personaje_elegido
    personaje = Jugador(700, 600, 70, 90, con_gravedad=False, personaje=personaje_elegido)
    personaje.velocidad_x = 6
    
    fuente = pygame.font.SysFont(None, 50)
    blanco = (255, 255, 255) 
    
    pared = [
        pygame.Rect(16, 172, 384, 15),
        pygame.Rect(15, 440, 242, 15),
        pygame.Rect(700, 171, 246, 15),
        pygame.Rect(1080, 165, 108, 15),
        pygame.Rect(380, 439, 17, 247),
        pygame.Rect(992, 438, 110, 15),
        pygame.Rect(580, 19, 20, 168),
        pygame.Rect(926, 15, 20, 168),
        pygame.Rect(992, 452, 20, 230)
    ]

    puerta1 = pygame.Rect(1100, 450, 80, 40)
    puerta2 = pygame.Rect(260, 450, 120, 40)
    puerta3 = pygame.Rect(400, 130, 180, 40)
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
                    menulevels()  # Regresa al menú de niveles
                
        teclas = pygame.key.get_pressed()
        personaje.actualizar(teclas, paredes=pared)  # Pasa paredes para colisiones
        
        # Chequeo de puertas (usa personaje.rect)
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
        # Opcional: Dibuja paredes/puertas para debug
        # for p in pared:
        #     pygame.draw.rect(ventana, red, p)
        # pygame.draw.rect(ventana, red, puerta1)  # etc.
        personaje.dibujar(ventana)
        pygame.display.flip()
        clock.tick(60)
def level2():
    pygame.mixer.music.stop()
    pygame.mixer.music.load("mu.WAV")
    pygame.mixer.music.play(-1)

    ANCHO = 1400
    ALTO = 700
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("minilevel1")

    fondo = pygame.image.load("imgs/l2img.jpeg")
    fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

    BLANCO = (255, 255, 255)
    NEGRO = (0, 0, 0)

    # Jugador con animaciones y gravedad
    global personaje_elegido
    jugador = Jugador(100, 500, 80, 100, con_gravedad=True, personaje=personaje_elegido, ancho_max=ANCHO)
    jugador.velocidad_x = 15
    jugador.suelo_y = 690
    jugador.fuerza_salto = -15

    # Objetos
    cajas = []
    sillas = []
    velocidad_objeto = 5

    # Cargar imágenes
    try:
        caja_img = pygame.image.load("imgs/caja.png")
        caja_img = pygame.transform.scale(caja_img, (70, 70))
    except Exception as e:
        print(f"No se pudo cargar caja.png: {e}")
        caja_img = pygame.Surface((70, 70))
        caja_img.fill((255, 0, 0))

    try:
        silla_img = pygame.image.load("imgs/silla.png")
        silla_img = pygame.transform.scale(silla_img, (50, 50))
    except Exception as e:
        print(f"No se pudo cargar silla.png: {e}")
        silla_img = pygame.Surface((50, 50))
        silla_img.fill((0, 255, 0))

    global contador_sillas
    sillas_recogidas = 0  # Contador local de sillas
    fuente = pygame.font.SysFont(None, 48)
    reloj = pygame.time.Clock()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return
                if evento.key == pygame.K_SPACE and jugador.en_suelo:
                    jugador.velocidad_y = jugador.fuerza_salto
                    jugador.en_suelo = False

        teclas = pygame.key.get_pressed()
        jugador.actualizar(teclas)

        # Generar objetos aleatorios
        if random.randint(1, 30) == 1:
            x = random.randint(0, ANCHO - 70)
            cajas.append(pygame.Rect(x, 0, 70, 70))
        if random.randint(1, 50) == 1:
            x = random.randint(0, ANCHO - 50)
            sillas.append(pygame.Rect(x, 0, 50, 50))

        # Actualizar cajas
        for c in cajas[:]:
            c.y += velocidad_objeto
            if c.colliderect(jugador.rect):
                regresar_al_hub()  # Golpe de caja: fin de nivel
                return
            if c.y > ALTO:
                cajas.remove(c)

        # Actualizar sillas
        for s in sillas[:]:
            s.y += velocidad_objeto
            if s.colliderect(jugador.rect):
                sillas_recogidas += 1
                contador_sillas += 1  # Suma global
                sillas.remove(s)
            elif s.y > ALTO:
                sillas.remove(s)

        # Condición de victoria: recoger 10 sillas
        if sillas_recogidas >= 10:
            regresar_al_hub()
            return

        # Dibujar todo
        ventana.fill(NEGRO)
        ventana.blit(fondo, (0, 0))
        jugador.dibujar(ventana)
        for c in cajas:
            ventana.blit(caja_img, (c.x, c.y))
        for s in sillas:
            ventana.blit(silla_img, (s.x, s.y))
        ventana.blit(fuente.render(f"Sillas recogidas: {sillas_recogidas}", True, BLANCO), (10, 10))
        ventana.blit(fuente.render(f"Sillas totales: {contador_sillas}", True, BLANCO), (10, 60))

        pygame.display.update()
        reloj.tick(60)

def level3():
    pygame.mixer.music.stop()
    pygame.mixer.music.load("l3.WAV")
    pygame.mixer.music.play(-1)

    ancho, alto = 1400, 500
    ventana = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("minilevel 2")

    # Jugador con animaciones y gravedad
    global personaje_elegido
    jugador = Jugador(200, 400, 100, 120, con_gravedad=True, personaje=personaje_elegido, ancho_max=ancho)
    jugador.velocidad_x = 10
    jugador.suelo_y = 450
    jugador.fuerza_salto = -20

    fondo = pygame.image.load("imgs/l3img.png")
    fondo = pygame.transform.scale(fondo, (ancho, alto))

    fuente = pygame.font.SysFont(None, 50)
    tiempo_inicio = pygame.time.get_ticks()
    contador_daño = 0
    puntos = 0
    
    global contador_sillas

    fantasmas = []
    for _ in range(5):
        rect = pygame.Rect(random.randint(700, ancho), jugador.suelo_y - 90, 60, 70)
        img = pygame.image.load("imgs/fantasma.png")
        img = pygame.transform.scale(img, (80, 90))
        fantasmas.append({"rect": rect, "img": img, "vel": random.randint(3, 6)})

    objetos = []
    objeto_img = pygame.image.load("imgs/silla.png")
    objeto_img = pygame.transform.scale(objeto_img, (50, 50))  # Ajustado a tamaño de rect

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

        teclas = pygame.key.get_pressed()
        jugador.actualizar(teclas)

        # Actualizar fantasmas
        for fantasma in fantasmas:
            if fantasma["rect"].x < jugador.rect.x:
                fantasma["rect"].x += fantasma["vel"]
            elif fantasma["rect"].x > jugador.rect.x:
                fantasma["rect"].x -= fantasma["vel"]
            if fantasma["rect"].colliderect(jugador.rect):
                contador_daño += 1

        # Generar objetos
        if random.randint(1, 50) == 1:
            x = random.randint(0, ancho - 50)
            objetos.append(pygame.Rect(x, jugador.suelo_y - 50, 50, 50))

        # Actualizar objetos
        for obj in objetos[:]:
            if obj.colliderect(jugador.rect):
                puntos += 1
                objetos.remove(obj)

        tiempo_actual = (pygame.time.get_ticks() - tiempo_inicio) // 1000
        if contador_daño >= 100:
            regresar_al_hub()
            return
        if puntos >= 30:
            contador_sillas += 30
            regresar_al_hub()
            return
        if tiempo_actual >= 40:
            regresar_al_hub()
            return

        ventana.fill((0, 0, 0))
        ventana.blit(fondo, (0, 0))
        jugador.dibujar(ventana)
        for fantasma in fantasmas:
            ventana.blit(fantasma["img"], (fantasma["rect"].x, fantasma["rect"].y))
        for obj in objetos:
            ventana.blit(objeto_img, (obj.x, obj.y))

        texto_tiempo = fuente.render(f"Tiempo: {tiempo_actual}s", True, (255, 255, 255))
        ventana.blit(texto_tiempo, (20, 100))
        texto_daño = fuente.render(f"Daño: {contador_daño}", True, (255, 0, 0))
        ventana.blit(texto_daño, (20, 20))
        texto_puntos = fuente.render(f"Puntos: {puntos}", True, (0, 255, 0))
        ventana.blit(texto_puntos, (20, 60))

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
