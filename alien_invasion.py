import sys
from time import sleep
import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Classe geral para gerenciar os recursos e comportamento do jogo."""
    
    def __init__(self):
        """Inicializa o jogo e cria os recursos."""
        pygame.init()
        
        self.settings = Settings()
        
        # Configuração para tela em janela
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        
        # Cria uma instância para armazenar estatísticas do jogo
        # e cria um painel de pontuação
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        
        self._create_fleet()
        
        # Cria o botão Play
        self.play_button = Button(self, "Play")
        
    def run_game(self):
        """Inicia o loop principal do jogo."""
        while True:
            self._check_events()
            
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                
            self._update_screen()
            
    def _check_events(self):
        """Responde a eventos de pressionamento de teclas e de mouse."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                
    def _check_play_button(self, mouse_pos):
        """Inicia um novo jogo quando o jogador clica em Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reinicia as configurações do jogo
            self.settings.initialize_dynamic_settings()
            
            # Reinicia as estatísticas do jogo
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            
            # Limpa os alienígenas e projéteis restantes
            self.aliens.empty()
            self.bullets.empty()
            
            # Cria uma nova frota e centraliza a nave
            self._create_fleet()
            self.ship.center_ship()
            
            # Esconde o cursor do mouse
            pygame.mouse.set_visible(False)
                
    def _check_keydown_events(self, event):
        """Responde a pressionamentos de tecla."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
            
    def _check_keyup_events(self, event):
        """Responde a liberações de tecla."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
            
    def _fire_bullet(self):
        """Cria um novo projétil e o adiciona ao grupo de projéteis."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            
    def _update_bullets(self):
        """Atualiza a posição dos projéteis e elimina os antigos."""
        # Atualiza as posições dos projéteis
        self.bullets.update()
        
        # Elimina os projéteis que desapareceram
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
                
        self._check_bullet_alien_collisions()
            
    def _check_bullet_alien_collisions(self):
        """Responde às colisões entre projéteis e alienígenas."""
        # Remove qualquer projétil e alienígena que tenha colidido
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
            
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        
        if not self.aliens:
            # Destrói os projéteis existentes e cria uma nova frota
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            
            # Aumenta o nível
            self.stats.level += 1
            self.sb.prep_level()
            
    def _create_fleet(self):
        """Cria a frota de alienígenas."""
        # Cria um alienígena e calcula o número de alienígenas em uma linha
        # O espaçamento entre os alienígenas é igual à largura de um alienígena
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        
        # Determina o número de linhas de alienígenas que cabem na tela
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        
        # Cria a frota completa de alienígenas
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
            
    def _create_alien(self, alien_number, row_number):
        """Cria um alienígena e o posiciona na linha."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)
        
    def _check_fleet_edges(self):
        """Responde apropriadamente se algum alienígena alcançou uma borda."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
                
    def _change_fleet_direction(self):
        """Desce toda a frota e muda a sua direção."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
        
    def _update_aliens(self):
        """
        Verifica se a frota está em uma borda,
        depois atualiza as posições de todos os alienígenas na frota.
        """
        self._check_fleet_edges()
        self.aliens.update()
        
        # Verifica colisões entre alienígenas e a nave
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            
        # Verifica se algum alienígena chegou ao fundo da tela
        self._check_aliens_bottom()
        
    def _ship_hit(self):
        """Responde ao fato de a nave ter sido atingida por um alienígena."""
        if self.stats.ships_left > 0:
            # Diminui ships_left e atualiza o painel de pontuação
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            
            # Limpa os alienígenas e projéteis restantes
            self.aliens.empty()
            self.bullets.empty()
            
            # Cria uma nova frota e centraliza a nave
            self._create_fleet()
            self.ship.center_ship()
            
            # Pausa
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
    
    def _check_aliens_bottom(self):
        """Verifica se algum alienígena alcançou a parte inferior da tela."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Trata isso da mesma forma que se a nave fosse atingida
                self._ship_hit()
                break
    
    def _update_screen(self):
        """Atualiza as imagens na tela e alterna para a nova tela."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        
        # Desenha as informações de pontuação
        self.sb.show_score()
        
        # Desenha o botão Play se o jogo estiver inativo
        if not self.stats.game_active:
            self.play_button.draw_button()
            
        # Deixa a tela mais recentemente desenhada visível
        pygame.display.flip()


if __name__ == '__main__':
    # Cria uma instância do jogo e o executa
    ai = AlienInvasion()
    ai.run_game()
