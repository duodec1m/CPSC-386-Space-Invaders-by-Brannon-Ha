from pygame import mixer

class Settings():
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings.
        self.screen_width = 640
        self.screen_height = 480
        self.bg_color = (0, 0, 0)

        # Ship settings.
        self.ship_limit = 3

        # Bullet settings.
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 250, 250, 250
        self.bullets_allowed = 3

        # Alien settings.
        self.fleet_drop_speed = 10

        # beam settings
        self.beam_speed_factor = 3
        self.beams_allowed = 1

        # How quickly the game speeds up.
        self.speedup_scale = 1.1
        # How quickly the alien point values increase.
        self.score_scale = 1.5

        self.beam_stamp = None

        # Ufo attributes
        self.last_ufo = None
        self.ufo_min_interval = 10000
        self.ufo_point_values = [50, 100, 150]

        self.initialize_dynamic_settings()

        self.background_music = [mixer.Sound('sound/bgm_1.wav'),
                                 mixer.Sound('sound/bgm_2.wav'),
                                 mixer.Sound('sound/bgm_3.wav'),
                                 mixer.Sound('sound/bgm_4.wav')]

        self.bgm_interval = 60 # Start with 60 frame gap between the bgm files
        self.bgm_buffer = 0
        self.bgm_index = 0

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = .1
        self.ufo_speed = self.alien_speed_factor * 2

        # fleet_direction of 1 represents right, -1 represents left.
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.beam_speed_factor *= self.speedup_scale

    def play_music(self):
        if(self.bgm_buffer == int(self.bgm_interval)):
            mixer.Channel(4).play(self.background_music[self.bgm_index])
            if(self.bgm_index == 3):
                self.bgm_index = 0
            else:
                self.bgm_index += 1
            self.bgm_buffer = 0
        if(self.bgm_interval < 5): #In case player somehow gets really far in-game
            self.bgm_interval = 5;

        self.bgm_buffer += 1