import pygame
from states.base_state import GameState
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from sprites import Dragon, Fireball, Enemy

# Definir el nivel del suelo (por ejemplo, 50 píxeles desde el fondo)
GROUND_LEVEL = SCREEN_HEIGHT - 50

class PlayState(GameState):
    def __init__(self):
        super().__init__()
        # Cargar fondo del juego
        try:
            self.background = pygame.image.load('assets/images/game_background.png').convert()
            self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception:
            self.background = None

        # Instanciar el dragón en el centro, posicionado en el suelo
        self.dragon = Dragon(x=SCREEN_WIDTH // 2, y=GROUND_LEVEL, element='fuego', size=(150, 150))
        # Grupo para las bolas de fuego
        self.projectiles = pygame.sprite.Group()
        # Grupo para los enemigos (caballeros)
        self.enemies = pygame.sprite.Group()
        # Temporizador para la generación de enemigos (cada 5 segundos)
        self.enemy_spawn_timer = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.done = True
                self.next_state = "menu"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Clic izquierdo: se ejecuta el ataque; si el dragón está en el suelo, usa ataque con cola
            if event.button == 1:
                if self.dragon.on_ground:
                    self.dragon.tail_attack()
                else:
                    self.dragon.attack()
                    mouse_pos = pygame.mouse.get_pos()
                    fireball = Fireball(self.dragon.rect.centerx, self.dragon.rect.centery, mouse_pos, element=self.dragon.element)
                    self.projectiles.add(fireball)

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.dragon.update(dt, keys)
        self.projectiles.update(dt)
        for enemy in self.enemies:
            # Los enemigos se mueven hacia el dragón en el eje x
            enemy.update(dt, target_x=self.dragon.rect.centerx)
        
        # Posicionar el dragón sobre el suelo
        if self.dragon.rect.bottom >= GROUND_LEVEL:
            self.dragon.rect.bottom = GROUND_LEVEL
            self.dragon.on_ground = True
        else:
            self.dragon.on_ground = False

        # Eliminar proyectiles que toquen el suelo
        for projectile in self.projectiles.copy():
            if projectile.rect.bottom >= GROUND_LEVEL:
                projectile.kill()

        # Colisiones: Si un proyectil impacta a un enemigo, se reduce la salud y se elimina el proyectil
        for enemy in self.enemies:
            for projectile in self.projectiles.copy():
                if enemy.rect.colliderect(projectile.rect):
                    enemy.health -= 1
                    projectile.kill()
                    if enemy.health <= 0:
                        enemy.kill()

        # Generar enemigos cada 5 segundos
        self.enemy_spawn_timer += dt
        if self.enemy_spawn_timer >= 5.0:
            self.enemy_spawn_timer = 0
            # Por ejemplo, se genera un enemigo en el lado derecho de la pantalla
            enemy = Enemy(x=SCREEN_WIDTH + 50, y=GROUND_LEVEL, size=(100, 100), health=3, speed=100)
            self.enemies.add(enemy)

        # Opcional: eliminar enemigos que se salgan de la pantalla (lado izquierdo)
        for enemy in self.enemies.copy():
            if enemy.rect.right < 0:
                enemy.kill()

    def draw(self, screen):
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill((50, 50, 100))
        # Dibujar el dragón
        screen.blit(self.dragon.image, self.dragon.rect)
        # Dibujar las bolas de fuego
        for projectile in self.projectiles:
            screen.blit(projectile.image, projectile.rect)
        # Dibujar los enemigos y su barra de salud
        for enemy in self.enemies:
            screen.blit(enemy.image, enemy.rect)
            enemy.draw_health_bar(screen)
        # Dibujar el suelo (un rectángulo verde)
        pygame.draw.rect(screen, (50, 205, 50), (0, GROUND_LEVEL, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_LEVEL))
