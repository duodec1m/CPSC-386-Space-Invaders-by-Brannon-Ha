import pygame
from pygame.sprite import Sprite
from pygame import mixer
from SpriteSheet import spritesheet


class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_settings, screen, type = 0):
        """Initialize the alien, and set its starting position."""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #Alien classification
        self.type = type

        #Alien's death status
        self.dead=False

        # Load the alien image, and set its rect attribute.
        self.ss = spritesheet('images/SpriteSheet.png')
        if(type == 0):
            self.imageT1 = self.ss.image_at((96, 160, 32, 32))
            self.imageT2 = self.ss.image_at((96, 192, 32, 32))
            self.image = self.imageT1
        elif(type == 1):
            self.imageT1 = self.ss.image_at((0, 96, 32, 32))
            self.imageT2 = self.ss.image_at((0, 128, 32, 32))
            self.image = self.imageT1
        elif(type == 2):
            self.imageT1 = self.ss.image_at((64, 96, 32, 32))
            self.imageT2 = self.ss.image_at((64, 128, 32, 32))
            self.image = self.imageT1
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position.
        self.x = float(self.rect.x)

        #Animation variable detector
        self.index = 0

        # Death frames Storage
        self.dFrames = [self.ss.image_at((0, 0, 32, 32)), self.ss.image_at((32, 0, 32, 32)),
                   self.ss.image_at((0, 32, 32, 32)), self.ss.image_at((32, 32, 32, 32)),
                   self.ss.image_at((0, 64, 32, 32)), self.ss.image_at((32, 64, 32, 32))]
        # Death Frames Location
        self.dIndex = 0

        # Sound
        self.death_sound = pygame.mixer.Sound('sound/invaderkilled.wav')
        self.fire_sound = pygame.mixer.Sound('sound/shoot.wav')
        self.channel = mixer.Channel(2)
        self.channel.set_volume(0.01)

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Move the alien right or left."""
        self.x += (self.ai_settings.alien_speed_factor *
                self.ai_settings.fleet_direction)
        self.rect.x = self.x

        """Sprite Animation"""
        self.index += 1
        if(self.index == 30):
            self.image = self.imageT2
        elif(self.index == 60):
            self.image = self.imageT1
            self.index = 0

        """Death Animation"""
        if(self.dead):
            self.dIndex += 1
            if self.dIndex >= len(self.dFrames):
                self.channel.play(self.death_sound)
                self.kill()
            else:
                self.image = self.dFrames[self.dIndex]


    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)

    def death_animation(self):
        self.dead = True
        self.dIndex = 0
        self.image = self.dFrames[self.dIndex]

    def fire_weapon(self):
        self.channel.play(self.fire_sound)