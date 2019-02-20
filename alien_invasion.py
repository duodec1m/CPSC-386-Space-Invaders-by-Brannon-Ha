import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import game_functions as gf
from bunker import spawn_bunker


def run_game():
    # Initialize pygame, settings, and screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Space Invaders")

    # Make the Play button.
    play_button = Button(ai_settings, screen, "Play")
    # Make the High Scores Button
    hs_button = Button(ai_settings, screen, "High Scores")

    # Create an instance to store game statistics, and a scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Make a ship, a group of bullets, and a group of aliens.
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    beams = Group()
    bunkers = Group()
    ufo = Group()

    # Create the fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship, aliens)

    for i in range(4):
        bunkers.add(spawn_bunker(ai_settings, screen, i))

    # Start the main loop for the game.
    while True:
        pygame.time.Clock().tick(60)  #set fps to 60
        gf.check_events(ai_settings, screen, stats, sb, play_button, hs_button, ship,
                        aliens, bullets, beams)

        if stats.game_active:
            ship.update()
            if(ship.dead == False): #Stop game to play death animation
                gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens,
                                bullets, beams, ufo)
                gf.update_beams(ai_settings, screen, stats, sb, ship, aliens,
                                bullets, beams)
                gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens,
                                bullets, beams, ufo)

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bunkers, beams,
                         bullets, play_button, hs_button, ufo)


run_game()