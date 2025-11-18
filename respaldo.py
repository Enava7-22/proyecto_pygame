import pygame
import random 
import sys
pygame.mixer.init()
pygame.init()

contador_sillas = 0

def level2():
    
    pygame.mixer.music.load("mu.WAV")
    pygame.mixer.music.play(-1)

    pygame.init()

    ANCHO = 1400
    ALTO = 700
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("minilevel1")

    fondo = pygame.image.load("imgs/l2img.jpeg")
    fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
    BLANCO = (255, 255, 255)
    NEGRO = (0, 0, 0)
    ROJO = (255, 0, 0)
    
    jugadorimg = pygame.image.load("imgs/personaje.png")
    jugadorimg = pygame.transform.scale(jugadorimg,(60,70))

    jugador = pygame.Rect(100, 500, 60, 70)
    velocidad_jugador = 15
    velocidad_y = 0
    gravedad = 1
    fuerza_salto = -15
    en_suelo = True
    suelo_y = 690

    objetos = []
    velocidad_objeto = 5
    cajaimg=pygame.image.load("imgs/caja.png")
    cajaimg=pygame.transform.scale(cajaimg,(70,70))
    global contador_sillas
    
    puntos = 0
    fuente = pygame.font.SysFont(None, 48)

    reloj = pygame.time.Clock()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and en_suelo:
                    velocidad_y = fuerza_salto
                    en_suelo = False

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and jugador.left > 0:
            jugador.x -= velocidad_jugador
        if teclas[pygame.K_RIGHT] and jugador.right < ANCHO:
            jugador.x += velocidad_jugador

        velocidad_y += gravedad
        jugador.y += velocidad_y
        if jugador.y >= suelo_y - jugador.height:
            jugador.y = suelo_y - jugador.height
            velocidad_y = 0
            en_suelo = True

        if random.randint(1, 30) == 1:
            x = random.randint(0, ANCHO - 50)
            objetos.append(pygame.Rect(x, 0, 70, 70))

        for obj in objetos[:]:
            obj.y += velocidad_objeto
            if obj.colliderect(jugador):
                l1()
                return
            if obj.y > ALTO:
                objetos.remove(obj)
                puntos += 1
                
                
                
        if puntos >= 10:
            contador_sillas += 20
            l1()
            return
        
        
        for obj in objetos:
            if jugador.colliderect(obj):
                l1()
                return

        ventana.fill(NEGRO)
        ventana.blit(fondo, (0, 0))
        ventana.blit(jugadorimg,(jugador.x,jugador.y))
        #pygame.draw.rect(ventana, BLANCO, jugador)
        
        for obj in objetos:
            ventana.blit(cajaimg,(obj.x,obj.y))
            #pygame.draw.rect(ventana, ROJO, obj)
            
        ventana.blit(fuente.render(f"Puntos: {puntos}", True, BLANCO), (10, 10))

        pygame.display.update()
        reloj.tick(120)



def level3():
    pygame.mixer.music.load("l3.WAV")
    pygame.mixer.music.play(-1)

    ancho, alto = 1400, 500
    ventana = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("minilevel 2")

    jugador = pygame.Rect(200, 400, 70, 90)
    velocidad_jugador = 10
    velocidad_y = 0
    gravedad = 1
    fuerza_salto = -20
    en_suelo = True
    suelo_y = 450
    jugador_img = pygame.image.load("imgs/personaje.png")
    jugador_img = pygame.transform.scale(jugador_img, (jugador.width, jugador.height))

    fondo = pygame.image.load("imgs/l3img.png")
    fondo = pygame.transform.scale(fondo, (ancho, alto))

    fuente = pygame.font.SysFont(None, 50)
    tiempo_inicio = pygame.time.get_ticks()
    contador_daño = 0
    puntos = 0
    
    global contador_sillas

    fantasmas = []
    for _ in range(5):
        rect = pygame.Rect(random.randint(700, 1400), suelo_y - 90, 80, 90)
        img = pygame.image.load("imgs/fantasma.png")
        img = pygame.transform.scale(img, (rect.width, rect.height))
        fantasmas.append({"rect": rect, "img": img, "vel": random.randint(3, 6)})

    objetos = []
    objeto_img = pygame.image.load("imgs/silla.png")
    objeto_img = pygame.transform.scale(objeto_img, (70, 90))

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
            jugador.x -= velocidad_jugador
        if teclas[pygame.K_RIGHT] and jugador.right < ancho:
            jugador.x += velocidad_jugador
        #if teclas[pygame.K_UP] and jugador.top >0:
            #jugador.y -= velocidad_jugador

        for fantasma in fantasmas:
            if fantasma["rect"].x < jugador.x:
                fantasma["rect"].x += fantasma["vel"]
            elif fantasma["rect"].x > jugador.x:
                fantasma["rect"].x -= fantasma["vel"]
            if fantasma["rect"].colliderect(jugador):
                contador_daño += 1

        if random.randint(1, 50) == 1:
            x = random.randint(0, ancho - 50)
            objetos.append(pygame.Rect(x, suelo_y - 50, 50, 50))

        for obj in objetos[:]:
            if obj.colliderect(jugador):
                puntos += 1
                objetos.remove(obj)

        tiempo_actual = (pygame.time.get_ticks() - tiempo_inicio) // 1000
        if contador_daño >= 100:
            l1()
            return
        if puntos >= 30:
            contador_sillas += 30
            l1()
            return
        if tiempo_actual >= 40:
            l1()
            return

        ventana.fill((0, 0, 0))
        ventana.blit(fondo, (0, 0))
        ventana.blit(jugador_img, (jugador.x, jugador.y))
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

    BLANCO = (255, 255, 255)
    NEGRO = (0, 0, 0)
    ROJO = (255, 0, 0)
    VERDE = (0, 255, 0)
    AZUL = (0, 0, 255)
    AMARILLO = (255, 255, 0)

    jugador = pygame.Rect(100, 600, 80, 80)
    velocidad_x = 8
    velocidad_y = 0
    gravedad = 1
    en_suelo = False

    global contador_sillas
    

    jugador_img = pygame.image.load("imgs/personaje.png")
    jugador_img = pygame.transform.scale(jugador_img,(jugador.width,jugador.height))

    objetos_esquivar_img = pygame.image.load("imgs/caja.png")
    objetos_esquivar_img = pygame.transform.scale(objetos_esquivar_img,(80,80))

    objetos_recoger_img = pygame.image.load("imgs/silla.png")
    objetos_recoger_img = pygame.transform.scale(objetos_recoger_img,(80,80))
    
    enemigos_img = pygame.image.load("imgs/fantasma.png")
    enemigos_img = pygame.transform.scale(enemigos_img,(80,80))

    plataformas = [
        pygame.Rect(0, 650, ANCHO, 50),
        pygame.Rect(300, 500, 200, 20),
        pygame.Rect(700, 400, 200, 20),
    ]

    enemigos = [pygame.Rect(random.randint(0, ANCHO-50), random.randint(0, 600), 40, 40) for _ in range(6)]
    velocidad_enemigo = 3

    objetos_recoger = []
    objetos_esquivar = []
    TIEMPO_OBJETO = pygame.USEREVENT + 1
    pygame.time.set_timer(TIEMPO_OBJETO, 1500)

    puntaje = 0
    fuente = pygame.font.SysFont(None, 36)
    contador_daño = 0
    fuente = pygame.font.SysFont(None, 36)


    reloj = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == TIEMPO_OBJETO:
                for _ in range(random.randint(2, 3)):
                    x = random.randint(0, ANCHO-30)
                    objetos_esquivar.append(pygame.Rect(x, 0, 30, 30))
                x_rec = random.randint(0, ANCHO-30)
                objetos_recoger.append(pygame.Rect(x_rec, 0, 30, 30))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            jugador.x -= velocidad_x
        if keys[pygame.K_RIGHT]:
            jugador.x += velocidad_x
        if keys[pygame.K_SPACE] and en_suelo:
            velocidad_y = -20
            en_suelo = False

        jugador.left = max(jugador.left, 0)
        jugador.right = min(jugador.right, ANCHO)
        jugador.top = max(jugador.top, 0)
        jugador.bottom = min(jugador.bottom, ALTO)

        velocidad_y += gravedad
        jugador.y += velocidad_y
        en_suelo = False
        for plat in plataformas:
            if jugador.colliderect(plat) and velocidad_y >= 0:
                jugador.bottom = plat.top
                velocidad_y = 0
                en_suelo = True

        for e in enemigos:
            if e.x < jugador.x:
                e.x += velocidad_enemigo
            if e.x > jugador.x:
                e.x -= velocidad_enemigo
            if e.y < jugador.y:
                e.y += velocidad_enemigo
            if e.y > jugador.y:
                e.y -= velocidad_enemigo
            e.left = max(e.left, 0)
            e.right = min(e.right, ANCHO)
            e.top = max(e.top, 0)
            e.bottom = min(e.bottom, ALTO)

        for obj in objetos_recoger[:]:
            obj.y += 5
            if jugador.colliderect(obj):
                puntaje += 1
                objetos_recoger.remove(obj)
            elif obj.y > ALTO:
                objetos_recoger.remove(obj)

        for obj in objetos_esquivar[:]:
            obj.y += 5
            if jugador.colliderect(obj):
                puntaje -= 1
                objetos_esquivar.remove(obj)
            elif obj.y > ALTO:
                objetos_esquivar.remove(obj)
        if puntaje >= 4:
            contador_sillas += 20
            l1()
            return
        if jugador.colliderect(enemigos):
            contador_daño += 1
        if contador_daño >= 500:
            l1()
            return

        ventana.fill(BLANCO)
        ventana.blit(jugador_img,(jugador.x,jugador.y))
        for e in enemigos:
            ventana.blit(enemigos_img,(e.x,e.y))
        for plat in plataformas:
            pygame.draw.rect(ventana, NEGRO, plat)
        #pygame.draw.rect(ventana, AZUL, jugador)
        #for e in enemigos:
            #pygame.draw.rect(ventana, ROJO, e)
        for e in objetos_esquivar:
            ventana.blit(objetos_esquivar_img,(e.x,e.y))
        for e in objetos_recoger:
            ventana.blit(objetos_recoger_img,(e.x,e.y))
        #for obj in objetos_recoger:
            #pygame.draw.rect(ventana, VERDE, obj)
        #for obj in objetos_esquivar:
            #pygame.draw.rect(ventana, AMARILLO, obj)
        texto = fuente.render(f"Puntaje: {puntaje}", True, NEGRO)
        ventana.blit(texto, (10,10))
        pygame.display.update()

        reloj.tick(60)

    
    
    
def level5():
    

    ancho = 1200
    alto = 700
    ventana = pygame.display.set_mode((ancho,alto))
    pygame.display.set_caption("mini level 5")

    jugador = pygame.Rect(600,600,30,30)
    color_jugador = (255,255,255)
    velocidad = 15

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and jugador.left >0:
            jugador.x -= velocidad   
        if teclas[pygame.K_RIGHT] and jugador.right <ancho:
            jugador.x += velocidad 
        if teclas[pygame.K_UP] and jugador.top >0:
            jugador.y -= velocidad
        if teclas[pygame.K_DOWN] and jugador.bottom <alto:
            jugador.y += velocidad
                        
        ventana.fill((0,0,0))
        pygame.draw.rect(ventana,color_jugador,jugador)
        
        
        pygame.display.flip()
        
        clock.tick(60)

    pygame.quit
    sys.exit
    
    
    
def level6():
    

    ancho = 1200
    alto = 700
    ventana = pygame.display.set_mode((ancho,alto))
    pygame.display.set_caption("mini level 6")

    jugador = pygame.Rect(600,600,30,30)
    color_jugador = (255,255,255)
    velocidad = 15

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and jugador.left >0:
            jugador.x -= velocidad   
        if teclas[pygame.K_RIGHT] and jugador.right <ancho:
            jugador.x += velocidad 
        if teclas[pygame.K_UP] and jugador.top >0:
            jugador.y -= velocidad
        if teclas[pygame.K_DOWN] and jugador.bottom <alto:
            jugador.y += velocidad
                        
        ventana.fill((0,0,0))
        pygame.draw.rect(ventana,color_jugador,jugador)
        
        
        pygame.display.flip()
        
        clock.tick(60)

    pygame.quit
    sys.exit
    
def l1():
    pygame.mixer.music.stop()
    pygame.mixer.music.load("l3.WAV")
    pygame.mixer.music.play(-1)
    
    ancho = 1200
    alto = 700
    ventana = pygame.display.set_mode((ancho,alto))
    pygame.display.set_caption("julioxromario")
    black = (0,0,0)
    white = (255,255,255)
    fondo = pygame.image.load("imgs/nuevo mapa.png")
    fondo = pygame.transform.scale(fondo,(ancho,alto))
    
    personaje = pygame.Rect(700,600,60,90)
    velocidad = 6
    
  
    fuente = pygame.font.SysFont(None,50)
    balnco = (255,255,255)
    
    imagen_jugador=pygame.image.load("imgs/personaje.png")
    imagen_jugador=pygame.transform.scale(imagen_jugador,(personaje.width,personaje.height))
    
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

    puerta1 = pygame.Rect(1100,450,80,40)
    puerta2 = pygame.Rect(260,450,120,40)
    puerta3 = pygame.Rect(400,130,180,40)
    puerta4 = pygame.Rect(606,130,90,40)
    puerta5 = pygame.Rect(950,130,130,40)
    puerta_exit = pygame.Rect(550,690,180,20)

    red =(255,0,0)

    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        x_anterior, y_anterior = personaje.x, personaje.y                   
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and personaje.left >0:
            personaje.x -= velocidad
        if teclas[pygame.K_RIGHT] and personaje.right <ancho:
            personaje.x += velocidad  
        if teclas[pygame.K_UP] and personaje.top >0:
            personaje.y -= velocidad
        if teclas[pygame.K_DOWN] and personaje.bottom <alto:
            personaje.y += velocidad  
            
        for p in pared:
            if personaje.colliderect(p):
                personaje.x, personaje.y = x_anterior, y_anterior
        
        
        if personaje.colliderect(puerta1):
            level2()
            return
        if personaje.colliderect(puerta2):
            level3()
            return
        if personaje.colliderect(puerta3):
            level4()
            return
        if personaje.colliderect(puerta4):
            level5()
            return
        if personaje.colliderect(puerta5):
            level6()
            return
        if personaje.colliderect(puerta_exit):
            menulevels()
         
             
             
        ventana.blit(fondo,(0,0))
        #pygame.draw.rect(ventana,red,puerta_exit)
        #pygame.draw.rect(ventana,white,personaje)
        #pygame.draw.rect(ventana,red,puerta1)
        #pygame.draw.rect(ventana,red,puerta2)
        #pygame.draw.rect(ventana,red,puerta3)
        #pygame.draw.rect(ventana,red,puerta4)
        #pygame.draw.rect(ventana,red,puerta5)
        texto = fuente.render(f"sillas: {contador_sillas}", True, balnco,)
        ventana.blit(texto, (20, 100))
        #for p in pared:
            #pygame.draw.rect(ventana,red,p)
        ventana.blit(imagen_jugador,(personaje.x,personaje.y))
        pygame.display.flip()
        clock.tick(60)

def menulevels():
    pygame.mixer.music.stop()
    ancho = 1200
    alto = 700
    ventana = pygame.display.set_mode((ancho,alto))
    pygame.display.set_caption("ml")

    botones_ancho , botones_alto = 300,100

    fondo = pygame.image.load("imgs/menulevels.jpg")
    fondo = pygame.transform.scale(fondo,(ancho,alto))

    boton_level1 =pygame.image.load("imgs/boton level1.png")
    boton_level1 =pygame.transform.scale(boton_level1,(botones_ancho,botones_alto))

    botonl1 = pygame.Rect(450,100,botones_ancho,botones_alto)

    x1 = 0
    x2 = ancho
    velocidad = 2 

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if botonl1.collidepoint(event.pos):
                    l1()
                    
        x1 -= velocidad
        x2 -= velocidad
        if x1 <= -ancho:
            x1 = x2 + ancho
        if x2 <= -ancho:
            x2 = x1 + ancho
        
        ventana.blit(fondo,(x1,0))
        ventana.blit(fondo,(x2,0))
        ventana.blit(boton_level1,(botonl1.x,botonl1.y))
        pygame.display.flip()
        clock.tick(60)
        
    pygame.quit()
    sys.exit()




        
def mainmenu():
    ancho = 1200
    alto = 700
    ancho_botones=300
    alto_botones=100

    ventana = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("integrador equpo 6")

    fondo = pygame.image.load("imgs/img.jpg")
    fondo = pygame.transform.scale(fondo, (ancho, alto))
    botones= pygame.image.load("imgs/boton inicio.png")
    botones= pygame.transform.scale(botones,(ancho_botones,alto_botones))
    configuracion =pygame.image.load("imgs/boton configuracion.png")
    configuracion = pygame.transform.scale(configuracion,(ancho_botones,alto_botones))

    boton_inicio_rect = pygame.Rect(450,300,ancho_botones,alto_botones)

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
        ventana.blit(botones,(450,300))
        ventana.blit(configuracion,(450,450))

        pygame.display.flip()
        reloj.tick(60)  

    pygame.quit()
    sys.exit()
mainmenu()