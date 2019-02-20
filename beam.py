import pygame
from pygame.sprite import Sprite


class Beam(Sprite):
    """Manages beams fired from aliens"""
    def __init__(self, ai_settings, screen, alien):
        super().__init__()
        self.screen = screen

        # Initialize beam image and related variables
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
                                ai_settings.bullet_height)
        self.rect.centerx = alien.rect.centerx
        self.rect.top = alien.rect.top
        self.color = (250,250,250)

        # Y position and speed factor
        self.y = float(self.rect.y)
        self.speed_factor = ai_settings.beam_speed_factor

    def update(self):
        """Move the beam down the screen"""
        self.y += self.speed_factor
        self.rect.y = self.y

    def blitme(self):
        """Draw the beam on the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)