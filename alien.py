import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Uma classe para representar um único alienígena na frota."""
    
    def __init__(self, ai_game):
        """Inicializa o alienígena e define sua posição inicial."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        # Carrega a imagem do alienígena e define seu atributo rect
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 255, 0))  # Alienígena verde simples
        self.rect = self.image.get_rect()
        
        # Inicia cada novo alienígena próximo ao canto superior esquerdo da tela
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        # Armazena a posição horizontal exata do alienígena
        self.x = float(self.rect.x)
        
    def check_edges(self):
        """Retorna True se o alienígena estiver na borda da tela."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
            
    def update(self):
        """Move o alienígena para a direita ou esquerda."""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x
