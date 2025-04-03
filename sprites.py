import pygame
import math

class Dragon(pygame.sprite.Sprite):
    def __init__(self, x, y, element='fuego', size=(150, 150)):
        super().__init__()
        self.element = element
        self.speed = 200  # pixels por segundo
        self.size = size
        # Estados posibles: "reposo", "volando", "atacando", "tierra", "caminando", "ataque_cola"
        self.state = "reposo"
        self.attacking = False
        self.attack_timer = 0
        self.attack_cooldown = 0.0
        self.on_ground = False  # Se actualizará desde el estado del juego

        # Variables para animación (para estados animados)
        self.frame_duration = 0.2  # segundos por frame
        self.animation_timer = 0
        self.current_frame = 0

        self.load_images()
        self.image = self.images["reposo"][0]
        self.rect = self.image.get_rect(center=(x, y))

    def load_images(self):
        self.images = {}

        # Animación para "reposo" (3 frames)
        reposo_frames = []
        for i in range(1, 4):
            try:
                image_path = f'assets/images/dragon_{self.element}_reposo_{i}.png'
                img = pygame.image.load(image_path).convert_alpha()
                img = pygame.transform.scale(img, self.size)
                reposo_frames.append(img)
            except Exception:
                placeholder = pygame.Surface(self.size, pygame.SRCALPHA)
                if self.element == 'fuego':
                    placeholder.fill((255, 100, 0))
                elif self.element == 'tierra':
                    placeholder.fill((139, 69, 19))
                elif self.element == 'hielo':
                    placeholder.fill((0, 191, 255))
                elif self.element == 'veneno':
                    placeholder.fill((0, 255, 0))
                else:
                    placeholder.fill((200, 200, 200))
                reposo_frames.append(placeholder)
        self.images["reposo"] = reposo_frames

        # Animación para "volando" (3 frames)
        movimiento_frames = []
        for i in range(1, 4):
            try:
                image_path = f'assets/images/dragon_{self.element}_movimiento_{i}.png'
                img = pygame.image.load(image_path).convert_alpha()
                img = pygame.transform.scale(img, self.size)
                movimiento_frames.append(img)
            except Exception:
                placeholder = pygame.Surface(self.size, pygame.SRCALPHA)
                if self.element == 'fuego':
                    placeholder.fill((255, 50, 0))
                else:
                    placeholder.fill((100, 100, 100))
                movimiento_frames.append(placeholder)
        self.images["volando"] = movimiento_frames

        # Animación para "tierra" (dragon en el suelo sin movimiento, 3 frames)
        tierra_frames = []
        for i in range(1, 4):
            try:
                image_path = f'assets/images/dragon_{self.element}_tierra_{i}.png'
                img = pygame.image.load(image_path).convert_alpha()
                img = pygame.transform.scale(img, self.size)
                tierra_frames.append(img)
            except Exception:
                placeholder = pygame.Surface(self.size, pygame.SRCALPHA)
                if self.element == 'fuego':
                    placeholder.fill((200, 100, 0))
                else:
                    placeholder.fill((120, 120, 120))
                tierra_frames.append(placeholder)
        self.images["tierra"] = tierra_frames

        # Animación para "caminando" (dragon en movimiento sobre el suelo, 3 frames)
        caminando_frames = []
        for i in range(1, 4):
            try:
                image_path = f'assets/images/dragon_{self.element}_caminando_{i}.png'
                img = pygame.image.load(image_path).convert_alpha()
                img = pygame.transform.scale(img, self.size)
                caminando_frames.append(img)
            except Exception:
                placeholder = pygame.Surface(self.size, pygame.SRCALPHA)
                if self.element == 'fuego':
                    placeholder.fill((255, 0, 0))
                else:
                    placeholder.fill((150, 150, 150))
                caminando_frames.append(placeholder)
        self.images["caminando"] = caminando_frames

        # Imagen para "atacando" (ataque a distancia, imagen única)
        try:
            image_path = f'assets/images/dragon_{self.element}_atacando.png'
            img = pygame.image.load(image_path).convert_alpha()
            img = pygame.transform.scale(img, self.size)
            self.images["atacando"] = img
        except Exception:
            img = pygame.Surface(self.size, pygame.SRCALPHA)
            if self.element == 'fuego':
                img.fill((255, 0, 0))
            else:
                img.fill((150, 150, 150))
            self.images["atacando"] = img

        # Animación para "ataque_cola" (ataque cuerpo a cuerpo con la cola, 3 frames)
        cola_frames = []
        for i in range(1, 4):
            try:
                image_path = f'assets/images/dragon_{self.element}_cola_{i}.png'
                img = pygame.image.load(image_path).convert_alpha()
                img = pygame.transform.scale(img, self.size)
                cola_frames.append(img)
            except Exception:
                placeholder = pygame.Surface(self.size, pygame.SRCALPHA)
                if self.element == 'fuego':
                    placeholder.fill((255, 0, 0))
                else:
                    placeholder.fill((150, 150, 150))
                cola_frames.append(placeholder)
        self.images["ataque_cola"] = cola_frames

    def attack(self):
        # Ataque a distancia (por ejemplo, lanzamiento de bola de fuego) cuando no está en el suelo
        if not self.on_ground and self.attack_cooldown <= 0:
            self.state = "atacando"
            self.attacking = True
            self.attack_timer = 0.7
            self.attack_cooldown = 0.75

    def tail_attack(self):
        # Ataque con cola (cuando el dragón está en el suelo)
        if self.on_ground and self.attack_cooldown <= 0:
            self.state = "ataque_cola"
            self.attacking = True
            self.attack_timer = 0.7
            self.attack_cooldown = 0.75

    def update(self, dt, keys):
        # Actualizar el cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt

        # Actualizar temporizador de ataque
        if self.attacking:
            self.attack_timer -= dt
            if self.attack_timer <= 0:
                self.attacking = False

        # Calcular movimiento con WASD
        movement = False
        dx = 0
        dy = 0
        if keys[pygame.K_a]:
            dx = -self.speed * dt
            movement = True
        if keys[pygame.K_d]:
            dx = self.speed * dt
            movement = True
        if keys[pygame.K_w]:
            dy = -self.speed * dt
            movement = True
        if keys[pygame.K_s]:
            dy = self.speed * dt
            movement = True

        self.rect.x += int(dx)
        self.rect.y += int(dy)

        # Determinar el estado del dragón según si está en el suelo o en el aire
        if self.on_ground:
            if self.attacking:
                self.state = "ataque_cola"
            elif movement:
                self.state = "caminando"
            else:
                self.state = "tierra"
        else:
            if self.attacking:
                self.state = "atacando"
            elif movement:
                self.state = "volando"
            else:
                self.state = "reposo"

        # Actualizar la imagen según el estado (para estados animados con múltiples frames)
        if self.state in ["reposo", "volando", "tierra", "caminando", "ataque_cola"]:
            self.animation_timer += dt
            if self.animation_timer >= self.frame_duration:
                self.animation_timer -= self.frame_duration
                self.current_frame = (self.current_frame + 1) % len(self.images[self.state])
            self.image = self.images[self.state][self.current_frame]
        else:
            self.image = self.images[self.state]

class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y, target_pos, element='fuego', size=(50, 20), speed=350):
        """
        Inicializa un proyectil de bola de fuego.

        :param x: Coordenada x inicial (normalmente el centro del dragón)
        :param y: Coordenada y inicial (normalmente el centro del dragón)
        :param target_pos: Tupla (x, y) con la posición del mouse al momento del ataque.
        :param element: Elemento del dragón (p.ej. "fuego") para cargar la imagen correspondiente.
        :param size: Tamaño deseado del proyectil.
        :param speed: Velocidad del proyectil.
        """
        super().__init__()
        self.element = element
        self.size = size

        # Cargar la imagen del proyectil usando el patrón de nombre
        try:
            image_path = f'assets/images/bola_{self.element}.png'
            original_image = pygame.image.load(image_path).convert_alpha()
            original_image = pygame.transform.scale(original_image, self.size)
        except Exception:
            original_image = pygame.Surface(self.size, pygame.SRCALPHA)
            original_image.fill((255, 255, 0))
        # Calcular el vector dirección desde (x, y) hasta target_pos
        dx = target_pos[0] - x
        dy = target_pos[1] - y
        distance = math.hypot(dx, dy)
        if distance == 0:
            distance = 1
        self.dx = dx / distance * speed
        self.dy = dy / distance * speed

        # Calcular el ángulo para rotar la imagen y que apunte hacia el target
        angle_rad = math.atan2(-dy, dx)  # Nota: -dy porque en Pygame el eje y se invierte
        angle_deg = math.degrees(angle_rad)
        self.image = pygame.transform.rotate(original_image, angle_deg)
        self.rect = self.image.get_rect(center=(x, y))

        # Reproducir el efecto de sonido para la bola de fuego
        try:
            sound_path = f'assets/sounds/bola_{self.element}_sonido.mp3'
            sound_effect = pygame.mixer.Sound(sound_path)
            sound_effect.set_volume(0.6)
            sound_effect.play()
        except Exception as e:
            print("Error al reproducir el sonido:", e)

    def update(self, dt):
        self.rect.x += int(self.dx * dt)
        self.rect.y += int(self.dy * dt)
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, size=(100, 100), health=10, speed=100):
        """
        Inicializa un enemigo (caballero) que se mueve a nivel del suelo.
        :param x: Posición inicial en x (por ejemplo, fuera de la pantalla por la derecha).
        :param y: Posición en y (usualmente GROUND_LEVEL).
        :param size: Tamaño del sprite.
        :param health: Salud inicial (se destruye al recibir 3 impactos).
        :param speed: Velocidad horizontal de aproximación.
        """
        super().__init__()
        self.size = size
        self.health = health
        self.max_health = health
        self.speed = speed

        # Cargar animación de reposo (3 frames)
        self.reposo_frames = []
        for i in range(1, 4):
            try:
                image_path = f'assets/images/caballero_normal_reposo_{i}.png'
                img = pygame.image.load(image_path).convert_alpha()
                img = pygame.transform.scale(img, self.size)
                self.reposo_frames.append(img)
            except Exception:
                placeholder = pygame.Surface(self.size, pygame.SRCALPHA)
                placeholder.fill((100, 100, 100))
                self.reposo_frames.append(placeholder)
        
        # Cargar animación para "moviendose" hacia la derecha
        self.moviendose_derecha_frames = []
        for i in range(1, 4):
            try:
                image_path = f'assets/images/caballero_normal_moviendoseDerecha_{i}.png'
                img = pygame.image.load(image_path).convert_alpha()
                img = pygame.transform.scale(img, self.size)
                self.moviendose_derecha_frames.append(img)
            except Exception:
                placeholder = pygame.Surface(self.size, pygame.SRCALPHA)
                placeholder.fill((150, 150, 150))
                self.moviendose_derecha_frames.append(placeholder)
        
        # Cargar animación para "moviendose" hacia la izquierda
        self.moviendose_izquierda_frames = []
        for i in range(1, 4):
            try:
                image_path = f'assets/images/caballero_normal_moviendoseIzquierda_{i}.png'
                img = pygame.image.load(image_path).convert_alpha()
                img = pygame.transform.scale(img, self.size)
                self.moviendose_izquierda_frames.append(img)
            except Exception:
                placeholder = pygame.Surface(self.size, pygame.SRCALPHA)
                placeholder.fill((120, 120, 120))
                self.moviendose_izquierda_frames.append(placeholder)
        
        # Estado inicial y animación
        self.state = "reposo"  # Puede ser "reposo", "moviendose_derecha" o "moviendose_izquierda"
        self.current_frame = 0
        self.frame_duration = 0.2  # segundos por frame
        self.animation_timer = 0
        self.image = self.reposo_frames[0]
        self.rect = self.image.get_rect(midbottom=(x, y))
        
        # Atributos para blinking (efecto de parpadeo al recibir daño)
        self.is_blinking = False
        self.blink_timer = 0
        self.blink_count = 0
        self.visible = True

    def update(self, dt, target_x=None):
        # Actualizar blinking si está activo
        if self.is_blinking:
            self.blink_timer -= dt
            if self.blink_timer <= 0:
                self.visible = not self.visible
                self.blink_timer = 0.1  # Duración de cada parpadeo
                self.blink_count += 1
                if self.blink_count >= 4:  # 2 ciclos completos (parpadea 2 veces)
                    self.is_blinking = False
                    self.visible = True

        # Movimiento horizontal hacia target_x (si se especifica)
        if target_x is not None:
            if self.rect.centerx < target_x:
                self.rect.x += int(self.speed * dt)
            elif self.rect.centerx > target_x:
                self.rect.x -= int(self.speed * dt)
            # Determinar el estado según la dirección y diferencia
            if abs(self.rect.centerx - target_x) > 5:
                if self.rect.centerx < target_x:
                    self.state = "moviendose_derecha"
                else:
                    self.state = "moviendose_izquierda"
            else:
                self.state = "reposo"
        else:
            self.state = "reposo"

        # Actualizar la animación
        self.animation_timer += dt
        if self.animation_timer >= self.frame_duration:
            self.animation_timer -= self.frame_duration
            self.current_frame = (self.current_frame + 1) % 3  # 3 frames
        if self.state == "moviendose_derecha":
            self.image = self.moviendose_derecha_frames[self.current_frame]
        elif self.state == "moviendose_izquierda":
            self.image = self.moviendose_izquierda_frames[self.current_frame]
        else:
            self.image = self.reposo_frames[self.current_frame]

    def take_tail_damage(self, damage, knockback, dragon_centerx):
        """
        Aplica daño de ataque con cola, retroceso y activa el efecto de parpadeo.
        :param damage: Daño a aplicar (ej. 3).
        :param knockback: Cantidad de retroceso en píxeles.
        :param dragon_centerx: La posición x del dragón, para determinar la dirección del knockback.
        """
        self.health -= damage
        # Retroceso: se mueve en dirección opuesta al dragón
        if self.rect.centerx < dragon_centerx:
            self.rect.x -= knockback
        else:
            self.rect.x += knockback
        # Iniciar efecto de parpadeo (2 veces: 4 cambios de visibilidad)
        self.is_blinking = True
        self.blink_timer = 0.1
        self.blink_count = 0
        self.visible = True

    def draw_health_bar(self, screen):
        bar_width = self.rect.width
        bar_height = 5
        ratio = self.health / self.max_health
        bg_rect = pygame.Rect(self.rect.x, self.rect.y - bar_height - 2, bar_width, bar_height)
        pygame.draw.rect(screen, (255, 0, 0), bg_rect)
        current_rect = pygame.Rect(self.rect.x, self.rect.y - bar_height - 2, int(bar_width * ratio), bar_height)
        pygame.draw.rect(screen, (0, 255, 0), current_rect)
