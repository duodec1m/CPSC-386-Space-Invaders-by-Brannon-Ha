import sys
from time import sleep

import pygame
import random
from bullet import Bullet
from alien import Alien
from beam import Beam
from SpriteSheet import spritesheet
from ufo import Ufo
from game_stats import GameStats


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, hs_button, ship, aliens,
                 bullets, beams):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            stats.hs_menu = False # To get out of the High Scores menu
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button,
                              ship, aliens, bullets, beams, mouse_x, mouse_y)
            check_hs_button(screen, stats, hs_button, mouse_x, mouse_y)

def check_hs_button(screen, stats, hs_button, mouse_x, mouse_y):
    button_clicked = hs_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        stats.hs_menu = True;


def check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                      aliens, bullets, beams, mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()

        # Reset the game statistics.
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
        beams.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Reset ship death animation if still playing
        ship.dead=False

def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet, if limit not reached yet."""
    # Create a new bullet, add to bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        ship.play_shoot_sound()

    bullets.update()

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bunkers, beams, bullets,
                  play_button, hs_button, ufo_group):
    """Update images on the screen, and flip to the new screen."""
    # Draw the main menu if the game is inactive.
    if not stats.game_active:
        screen.fill((0, 0, 0))  # Clear the screen
        # High Scores menu
        if(stats.hs_menu):
            pygame.font.init()
            myfont = pygame.font.SysFont(None, 40)
            score1 = myfont.render('1. ' + str(stats.high_scores_all[0]), False, (255, 255, 255))
            score2 = myfont.render('2. ' + str(stats.high_scores_all[1]), False, (255, 255, 255))
            score3 = myfont.render('3. ' + str(stats.high_scores_all[2]), False, (255, 255, 255))
            notify = myfont.render('Click anywhere on the screen to go back', False, (255, 255, 255))
            screen.blit(score1, (150, 58))
            screen.blit(score2, (150, 188))
            screen.blit(score3, (150, 318))
            screen.blit(notify, (50, 400))
        else:
            play_button.draw_button()
            hs_button.draw_button()

            ss = spritesheet('SpriteSheet.png')
            alienType0 = ss.image_at((96, 160, 32, 32))
            alienType1 = ss.image_at((0, 96, 32, 32))
            alienType2 = ss.image_at((64, 96, 32, 32))
            alienType3 = ss.image_at((64, 0, 32, 32))
            screen.blit(alienType0, (250, 150))
            screen.blit(alienType1, (250, 180))
            screen.blit(alienType2, (250, 210))
            screen.blit(alienType3, (250, 240))

            pygame.font.init()
            myfont = pygame.font.SysFont(None, 20)
            title = pygame.font.SysFont(None, 80).render('Space Invaders', False, (255, 255, 255))
            textsurface0 = myfont.render('= 10 points', False, (255, 255, 255))
            textsurface1 = myfont.render('= 20 points', False, (255, 255, 255))
            textsurface2 = myfont.render('= 40 points', False, (255, 255, 255))
            textsurface3 = myfont.render('= ??? points', False, (255, 255, 255))
            screen.blit(title, (120, 70))
            screen.blit(textsurface0, (300, 158))
            screen.blit(textsurface1, (300, 188))
            screen.blit(textsurface2, (300, 218))
            screen.blit(textsurface3, (300, 248))

    # Going in-game
    else:
        ufo_event_check(ai_settings, screen, ufo_group)
        # Redraw the screen, each pass through the loop.
        screen.fill(ai_settings.bg_color)

        # Redraw all bullets, behind ship and aliens.
        for bullet in bullets.sprites():
            bullet.draw_bullet()
        # Redraw all beams
        for beam in beams.sprites():
            beam.blitme()
        if ufo_group:
            ufo_group.update()
            for ufo in ufo_group.sprites():
                ufo.blitme()
        ship.blitme()
        aliens.draw(screen)
        check_bunker_collisions(beams, bullets, bunkers)
        # Draw the score information.
        sb.show_score()

        bunkers.update()
    # Make the most recently drawn screen visible.
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, beams, ufo):
    """Update position of bullets, and get rid of old bullets."""
    # Update bullet positions.
    bullets.update()

    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                  aliens, bullets, beams, ufo)

def update_beams(ai_settings, screen, stats, sb, ship, aliens, bullets, beams):
    beams.update()
    for beam in beams.copy():
        if beam.rect.bottom > ai_settings.screen_height:
            beams.remove(beam)
    check_ship_beam_collisions(ai_settings, screen, stats, sb, ship, aliens, beams, bullets)

def check_ship_beam_collisions(ai_settings, screen, stats, sb, ship, aliens, beams, bullets):
    collisions = pygame.sprite.spritecollideany(ship, beams)
    if collisions:
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, beams)

def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                  aliens, bullets, beams, ufo):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, False)

    if collisions:
        for aliens in collisions.values():
            for single_alien in aliens:
                if(single_alien.type == 0):
                    stats.score += 10 * len(aliens)
                elif(single_alien.type == 1):
                    stats.score += 20 * len(aliens)
                elif (single_alien.type == 2):
                    stats.score += 40 * len(aliens)
                single_alien.death_animation()
            sb.prep_score()
        check_high_score(stats, sb)
        ai_settings.alien_speed_factor += .01

    ufo_collide = pygame.sprite.groupcollide(bullets, ufo, True, False)
    if ufo_collide:
        for ufo in ufo_collide.values():
            for u in ufo:
                stats.score += u.score
                u.begin_death()
            sb.prep_score()
        check_high_score(stats, sb)

    if (len(aliens) == 0 and stats.ships_left > 0):
        # If the entire fleet is destroyed and there are still lives left, start a new level.
        if ufo:
            for u in ufo.sprites():
                u.kill()  # kill any UFOs before start of new level
        bullets.empty()
        beams.empty()
        ai_settings.increase_speed()

        # Increase level.
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet, and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, beams):
    """Respond to ship being hit by alien."""
    ship.play_death_sound()
    ship.dead = True
    if stats.ships_left > 0:
        # Decrement ships_left.
        stats.ships_left -= 1

        # Update scoreboard.
        sb.prep_ships()

        # Get rid of all bullets and beams so you don't hit it again
        bullets.empty()
        beams.empty()

    else:
        # Game over procedure
        aliens.empty()
        bullets.empty()
        beams.empty()

        basicfont = pygame.font.SysFont(None, 48)
        text = basicfont.render('Game Over', True, (255, 255, 255), (0, 0, 0, 0))
        textrect = text.get_rect()
        textrect.centerx = screen.get_rect().centerx
        textrect.centery = screen.get_rect().centery

        screen.blit(text, textrect)
        pygame.display.update()

        stats.save_hs_to_file()

        stats.game_active = False;

        sleep(2)




def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens,
                        bullets, beams):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            stats.ships_left = 0 # Instant death if aliens hit the bottom
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, beams)
            break


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, beams, ufo):
    """
    Check if the fleet is at an edge,
      then update the postions of all aliens in the fleet.
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        stats.ships_left = 0  # Instant death when aliens touch ship
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, beams)

    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets, beams)
    if aliens.sprites():
        fire_random_beam(ai_settings, screen, aliens, beams)

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien, and place it in the row."""
    if (row_number == 1 or row_number == 2):
        alien = Alien(ai_settings, screen, 1)
    elif (row_number == 0):
        alien = Alien(ai_settings, screen, 2)
    else:
        alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 1.2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 1.2 * alien.rect.height * row_number + 50 # The 50 is the offset from the ceiling
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    # Create an alien, and find number of aliens in a row.
    alien = Alien(ai_settings, screen)
    number_aliens_x = 11
    number_rows = 5

    # Create the fleet of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                         row_number)

def check_bunker_collisions(beams, bullets, bunkers):
    """Respond to bullet/beam to bunker collision"""
    collisions = pygame.sprite.groupcollide(bullets, bunkers, True, False)
    for bullets in collisions.values():
        for single_bullet in bullets:
            single_bullet.damage(top=False)
    collisions = pygame.sprite.groupcollide(beams, bunkers, True, False)
    for beams in collisions.values():
        for single_beam in beams:
            single_beam.damage(top=True)

def fire_random_beam(ai_settings, screen, aliens, beams):
    """Fire a beam from a random alien in the fleet"""
    firing_alien = random.choice(aliens.sprites())
    if len(beams) < ai_settings.beams_allowed and \
            (ai_settings.beam_stamp is None or
             (abs(pygame.time.get_ticks() - ai_settings.beam_stamp) > ai_settings.beam_time)):
        new_beam = Beam(ai_settings, screen, firing_alien)
        firing_alien.fire_weapon()
        beams.add(new_beam)

def create_random_ufo(ai_settings, screen):
    """With a chance of 10% create a Ufo and return it with the time it was created"""
    ufo = None
    if random.randrange(0, 100) <= 15:  # 15% chance of ufo
        ufo = Ufo(ai_settings, screen)
    time_stamp = pygame.time.get_ticks()
    return time_stamp, ufo


def ufo_event_check(ai_settings, screen, ufo_group):
    """Check if now is a good time to create a ufo and if so create one and add it to the ufo group"""
    if not ai_settings.last_ufo and not ufo_group:
        ai_settings.last_ufo, n_ufo = create_random_ufo(ai_settings, screen)
        if n_ufo:
            ufo_group.add(n_ufo)
    elif abs(pygame.time.get_ticks() - ai_settings.last_ufo) > ai_settings.ufo_min_interval and not ufo_group:
        ai_settings.last_ufo, n_ufo = create_random_ufo(ai_settings, screen)
        if n_ufo:
            ufo_group.add(n_ufo)