import pygame
import time
from pygame.sprite import Sprite
from pygame import mixer
from SpriteSheet import spritesheet

class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        """Initialize the ship, and set its starting position."""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the ship image, and get its rect.
        self.ss = spritesheet('images/SpriteSheet.png')
        self.image = self.ss.image_at((0,160,32,32))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store a decimal value for the ship's center.
        self.center = float(self.rect.centerx)

        # Movement flags.
        self.moving_right = False
        self.moving_left = False

        # Sound
        self.death_sound = pygame.mixer.Sound('sound/explosion.wav')
        self.fire_sound = pygame.mixer.Sound('sound/shoot.wav')
        self.channel = mixer.Channel(1)
        self.channel.set_volume(0.01)

        # Death tag
        self.dead = False

        # Death index
        self.dIndex = 0

    def center_ship(self):
        """Center the ship on the screen."""
        self.center = self.screen_rect.centerx

    def update(self):
        """Update the ship's position, based on movement flags."""
        # Update the ship's center value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # Update rect object from self.center.
        self.rect.centerx = self.center

        """Death Animation"""
        if(self.dead):

            #Stop the ship from moving
            self.moving_left = False
            self.moving_right = False

            if(self.dIndex == 0):
                self.image = self.ss.image_at((32,160,32,32))
            elif (self.dIndex == 10):
                self.image = self.ss.image_at((64, 160, 32, 32))
            elif (self.dIndex == 20):
                self.image = self.ss.image_at((0, 192, 32, 32))
            elif (self.dIndex == 30):
                self.image = self.ss.image_at((32, 192, 32, 32))
            elif (self.dIndex == 40):
                self.image = self.ss.image_at((64, 192, 32, 32))
            elif (self.dIndex == 50):
                self.image = self.ss.image_at((0,224,32,32))
            elif (self.dIndex >= 60):
                self.dIndex = 0
                self.dead = False
            self.dIndex += 1
        else:
            self.image = self.ss.image_at((0, 160, 32, 32))

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def play_shoot_sound(self):
        self.channel.play(self.fire_sound)

    def play_death_sound(self):
        self.channel.play(self.death_sound)
