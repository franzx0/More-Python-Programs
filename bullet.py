import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Uma classe para gerenciar os projéteis disparados pela nave."""
    
    def __init__(self, ai_game):
        """Cria um objeto de projétil na posição atual da nave."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color
        
        # Cria um rect para o projétil em (0, 0) e então define a posição correta
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                               self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        
        # Armazena a posição do projétil como um valor decimal
        self.y = float(self.rect.y)
        
    def update(self):
        """Move o projétil pela tela."""
        # Atualiza a posição decimal do projétil
        self.y -= self.settings.bullet_speed
        # Atualiza a posição do rect
        self.rect.y = self.y
        
    def draw_bullet(self):
        """Desenha o projétil na tela."""
        pygame.draw.rect(self.screen, self.color, self.rect)
