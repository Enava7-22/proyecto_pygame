import pygame
import sys

pygame.init()
ancho = 1200
alto = 700

# -------------------------
# Clase base de escena
# -------------------------
class Scene:
    def __init__(self, manager):
        self.manager = manager

    def handle_events(self, events): pass
    def update(self, dt): pass
    def render(self, screen): pass

# -------------------------
# Gestor de escenas
# -------------------------
class SceneManager:
    def __init__(self):
        self.scenes = {}
        self.current = None

    def register(self, name, scene):
        self.scenes[name] = scene

    def go_to(self, name):
        self.current = self.scenes[name]

    def handle_events(self, events):
        self.current.handle_events(events)

    def update(self, dt):
        self.current.update(dt)

    def render(self, screen):
        self.current.render(screen)

# -------------------------
# Escena: Menú principal
# -------------------------
class Menu(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.fondo_menu = pygame.transform.scale(pygame.image.load("img.jpg"), (ancho, alto))
        self.ancho_botones = 300
        self.alto_botones = 100

        self.boton_inicio_img = pygame.transform.scale(pygame.image.load("boton inicio.png"), (self.ancho_botones, self.alto_botones))
        self.boton_config_img = pygame.transform.scale(pygame.image.load("boton configuracion.png"), (self.ancho_botones, self.alto_botones))

        self.boton_inicio_rect = pygame.Rect(450, 300, self.ancho_botones, self.alto_botones)
        self.boton_config_rect = pygame.Rect(450, 450, self.ancho_botones, self.alto_botones)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.boton_inicio_rect.collidepoint(event.pos):
                    self.manager.go_to("nivel1")
                elif self.boton_config_rect.collidepoint(event.pos):
                    print("Botón CONFIGURACIÓN presionado")

    def update(self, dt):
        pass

    def render(self, screen):
        screen.blit(self.fondo_menu, (0, 0))
        screen.blit(self.boton_inicio_img, self.boton_inicio_rect)
        screen.blit(self.boton_config_img, self.boton_config_rect)

# -------------------------
# Escena: Nivel 1
# -------------------------
class Nivel1(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.fondo = pygame.transform.scale(pygame.image.load("Gemini_Generated_Image_rglu37rglu37rglu.png"), (ancho, alto))
        self.jugador = pygame.Rect(560, alto // 2, 40, 70)
        self.velocidad = 5
        self.img_jugador = pygame.transform.scale(pygame.image.load("personaje.png"), (40, 70))
        self.puerta = pygame.Rect(1100, 300, 60, 100)  # puerta para pasar a nivel 2

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self, dt):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_a] and self.jugador.left > 0:
            self.jugador.x -= self.velocidad
        if teclas[pygame.K_d] and self.jugador.right < ancho:
            self.jugador.x += self.velocidad
        if teclas[pygame.K_w] and self.jugador.top > 0:
            self.jugador.y -= self.velocidad
        if teclas[pygame.K_s] and self.jugador.bottom < alto:
            self.jugador.y += self.velocidad

        # Cambio de escena si toca la puerta
        if self.jugador.colliderect(self.puerta):
            self.manager.go_to("nivel2")

    def render(self, screen):
        screen.blit(self.fondo, (0, 0))
        pygame.draw.rect(screen, (0, 255, 0), self.puerta)  # puerta
        screen.blit(self.img_jugador, self.jugador)

# -------------------------
# Escena: Nivel 2
# -------------------------
class Nivel2(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.fondo = pygame.transform.scale(pygame.image.load("fondolevel1.png"), (ancho, alto))
        self.jugador = pygame.Rect(50, alto // 2, 40, 70)
        self.velocidad = 5
        self.img_jugador = pygame.transform.scale(pygame.image.load("personaje.png"), (40, 70))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self, dt):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_a] and self.jugador.left > 0:
            self.jugador.x -= self.velocidad
        if teclas[pygame.K_d] and self.jugador.right < ancho:
            self.jugador.x += self.velocidad
        if teclas[pygame.K_w] and self.jugador.top > 0:
            self.jugador.y -= self.velocidad
        if teclas[pygame.K_s] and self.jugador.bottom < alto:
            self.jugador.y += self.velocidad

    def render(self, screen):
        screen.blit(self.fondo, (0, 0))
        screen.blit(self.img_jugador, self.jugador)

# -------------------------
# Bucle principal
# -------------------------
ventana = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Juego con cambio de escenas")

manager = SceneManager()
manager.register("menu", Menu(manager))
manager.register("nivel1", Nivel1(manager))
manager.register("nivel2", Nivel2(manager))
manager.register("nivel3", Nivel2(manager))  # Reutilizando Nivel2 para Nivel3 como ejemplo
manager.go_to("menu")

clock = pygame.time.Clock()

while True:
    dt = clock.tick(60) / 1000
    events = pygame.event.get()
    manager.handle_events(events)
    manager.update(dt)
    manager.render(ventana)
    pygame.display.flip()
