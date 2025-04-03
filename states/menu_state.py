import pygame
from states.base_state import GameState
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

def render_text_with_outline(font, text, text_color, outline_color, outline_width):
    """
    Renderiza un texto con un borde.
    
    :param font: objeto pygame.font.Font
    :param text: cadena a renderizar
    :param text_color: color principal, por ejemplo (255, 255, 255)
    :param outline_color: color del contorno, por ejemplo (0, 0, 0)
    :param outline_width: grosor del borde en píxeles
    :return: Surface con el texto y su borde
    """
    # Renderizar el texto base
    base = font.render(text, True, text_color)
    # Calcular dimensiones agregando el borde
    w = base.get_width() + 2 * outline_width
    h = base.get_height() + 2 * outline_width
    outline_surface = pygame.Surface((w, h), pygame.SRCALPHA)
    
    # Dibujar el contorno desplazando el texto en todas direcciones
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx != 0 or dy != 0:
                pos = (outline_width + dx, outline_width + dy)
                outline_surface.blit(font.render(text, True, outline_color), pos)
    
    # Dibujar el texto original en el centro
    outline_surface.blit(base, (outline_width, outline_width))
    return outline_surface

class MenuState(GameState):
    def __init__(self):
        super().__init__()
        # Definir fuentes
        self.title_font = pygame.font.Font(None, 50)
        self.instruction_font = pygame.font.Font(None, 30)
        
        # Renderizar el título con borde usando la función creada
        self.title_text = render_text_with_outline(
            self.title_font,
            "Aliento de Dragón",
            text_color=(102, 0, 0),
            outline_color=(0, 0, 0),  # borde negro
            outline_width=2         # grosor del borde
        )
        # Renderizar el texto de instrucciones
        self.instruction_text = self.instruction_font.render(
            "Presiona ENTER para jugar", True, (200, 200, 200)
        )
        
        # Cargar la imagen de fondo del menú (menu_principal.png)
        try:
            self.background = pygame.image.load('assets/images/menu_principal.png').convert()
            self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception:
            self.background = None

        
        # Cargar y reproducir la música del menú en loop
        try:
            pygame.mixer.music.load('assets/sounds/menu_music.mp3')
            pygame.mixer.music.play(-1)  # -1 para loop infinito
            pygame.mixer.music.set_volume(0.3)  # Ajusta el volumen (0.0 a 1.0)
        except Exception as e:
            print("No se pudo cargar la música del menú:", e)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.done = True
            self.next_state = "game"

    def update(self, dt):
        pass

    def draw(self, screen):
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill((0, 0, 0))
        
        # Dibujar el título centrado
        screen.blit(
            self.title_text,
            (SCREEN_WIDTH // 2 - self.title_text.get_width() // 2,
             SCREEN_HEIGHT // 2 - 100)
        )
        # Dibujar las instrucciones centradas
        screen.blit(
            self.instruction_text,
            (SCREEN_WIDTH // 2 - self.instruction_text.get_width() // 2,
             SCREEN_HEIGHT // 2)
        )
