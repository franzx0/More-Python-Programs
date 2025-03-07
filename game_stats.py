class GameStats:
    """Rastreia estatísticas do jogo."""
    
    def __init__(self, ai_game):
        """Inicializa as estatísticas."""
        self.settings = ai_game.settings
        self.reset_stats()
        
        # Inicia o jogo em um estado inativo
        self.game_active = False
        
        # A pontuação máxima nunca deve ser reinicializada
        self.high_score = 0
        
    def reset_stats(self):
        """Inicializa as estatísticas que podem mudar durante o jogo."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
