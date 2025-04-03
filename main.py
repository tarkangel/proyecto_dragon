 
# main.py
import sys
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from states.menu_state import MenuState
from states.game_state import PlayState

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Aliento de Dragón")
    clock = pygame.time.Clock()

    # Empezamos en la pantalla de menú
    current_state = MenuState()

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # Tiempo entre frames en segundos

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                current_state.handle_event(event)

        current_state.update(dt)
        current_state.draw(screen)
        pygame.display.flip()

        # Transición de estados
        if current_state.done:
            if current_state.next_state == "game":
                current_state = PlayState()
            elif current_state.next_state == "menu":
                current_state = MenuState()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
