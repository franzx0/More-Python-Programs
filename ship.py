import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """Uma classe para gerenciar a nave."""
    
    def __init__(self, ai_game):
        """Inicializa a nave e define sua posição inicial."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        
        # Carrega a imagem da nave e obtém seu rect
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 0, 255))  # Nave azul simples
        self.rect = self.image.get_rect()
        
        # Inicia cada nova nave na parte inferior central da tela
        self.rect.midbottom = self.screen_rect.midbottom
        
        # Armazena um valor decimal para a posição horizontal da nave
        self.x = float(self.rect.x)
        
        # Flags de movimento
        self.moving_right = False
        self.moving_left = False
        
    def update(self):
        """Atualiza a posição da nave com base nas flags de movimento."""
        # Atualiza o valor de x da nave, não o rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
            
        # Atualiza o objeto rect a partir de self.x
        self.rect.x = self.x
        
    def blitme(self):
        """Desenha a nave em sua posição atual."""
        self.screen.blit(self.image, self.rect)
        
    def center_ship(self):
        """Centraliza a nave na tela."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
