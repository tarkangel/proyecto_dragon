 # states/base_state.py
class GameState:
    def __init__(self):
        self.next_state = None
        self.done = False

    def handle_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, screen):
        pass

