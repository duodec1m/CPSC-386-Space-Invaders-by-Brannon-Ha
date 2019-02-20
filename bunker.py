from pygame import sprite, Surface, PixelArray
from pygame.sprite import Sprite
from random import randrange


class BunkerBlock(Sprite):
    def __init__(self, ai_settings, screen):
        super().__init__()
        self.screen = screen
        self.height = self.width = 5
        self.image = Surface((self.width, self.height))
        self.image.fill((0,255,0))
        self.rect = self.image.get_rect()
        self.tookDamage = False

    def damage(self, top):
        if not self.tookDamage:
            pix = PixelArray(self.image)
            if top:
                for i in range(self.height * 3):
                    pix[randrange(0, self.width - 1),
                             randrange(0, self.height // 2)] = (0, 0, 0, 0)  # get rid of pixel by making it invisiable
            else:
                for i in range(self.height * 3):
                    pix[randrange(0, self.width - 1),
                             randrange(self.height // 2, self.height - 1)] = (0, 0, 0, 0)   # get rid of pixel by making it invisible
            self.tookDamage = True
        else:
            self.kill()

    def update(self):
        self.screen.blit(self.image, self.rect)


def spawn_bunker(ai_settings, screen, position):
    """Bunker is made of several little blocks"""
    bunker = sprite.Group()
    for row in range(5):
        for col in range(9):
            if not ((row > 3 and (1 < col < 7)) or (row > 2 and (2 < col < 6)) or (row == 0 and (col < 1 or col > 7))):
                block = BunkerBlock(ai_settings, screen)
                block.rect.x = int(ai_settings.screen_width * 0.1) + (150 * position) + (col * block.width)
                block.rect.y = int(ai_settings.screen_height * 0.8) + (row * block.height)
                bunker.add(block)
    return bunker