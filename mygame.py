#!/usr/bin/python3.10

# Import the pygame module
import pygame
# Import random for random numbers
import random

import characters
import aboutDialog

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_ESCAPE,
    K_m,
    K_b,
    K_k,
    K_g,
    K_f,
    KEYDOWN,
    QUIT,
    K_SPACE,
    MOUSEBUTTONDOWN
)

def resetGame():
    player1.reset()
    stats.reset()
    #print( player1 )
    for e in enemies:
        e.kill()
    for e in booms:
        e.kill()

def drawGrid( virtualScreen ):
    surface = pygame.Surface([virtualScreen.width,virtualScreen.height])
    for i in range(0, virtualScreen.width, 50 ):
        lwidth = 1
        if (i % 200) == 0:
            lwidth = 3
        pygame.draw.line( surface, "gray", [i,0], [i,virtualScreen.height], lwidth)
    for i in range(0, virtualScreen.height, 50 ):
        lwidth = 1
        if (i % 200) == 0:
            lwidth = 3
        pygame.draw.line( surface, "gray", [0,i], [virtualScreen.width,i], lwidth)
    screen.blit(surface, virtualScreen)    
    return

# Load and play our background music
# Sound source: http://ccmixter.org/files/Apoxode/59262
# License: https://creativecommons.org/licenses/by/3.0/
SOUND_BACKGROUND="resources/Apoxode_-_Electric_1.mp3"
# Load all our sound files
# Sound sources: Jon Fincher
SOUND_MOVE_UP="resources/Rising_putter.ogg"
SOUND_MOVE_DOWN="resources/Falling_putter.ogg"
SOUND_COLLISION="resources/Collision.ogg"
# These are from Asteroids https://www.classicgaming.cc/classics/asteroids/
SOUND_ROCKET="resources/fire.ogg"
SOUND_BANG1="resources/bangSmall.ogg"
SOUND_BANG2="resources/bangLarge.ogg"


# Setup for sounds, defaults are good
pygame.mixer.init()

# Initialize pygame
pygame.init()

stats = characters.GameStats()
# Setup the clock for a decent framerate
clock = pygame.time.Clock()
# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
#screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, display=0)
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface().get_size()

virtualScreen = pygame.Rect( 0, 60, SCREEN_WIDTH, SCREEN_HEIGHT-60 )
scoreScreen   = pygame.Rect( 0, 0, SCREEN_WIDTH, 60 )

pygame.mixer.music.load( SOUND_BACKGROUND)
pygame.mixer.music.play(loops=-1)

rocket_sound = pygame.mixer.Sound(SOUND_ROCKET)
move_up_sound = pygame.mixer.Sound(SOUND_MOVE_UP)
move_down_sound = pygame.mixer.Sound(SOUND_MOVE_DOWN)
collision_sound = pygame.mixer.Sound(SOUND_COLLISION)
bang_sound1 = pygame.mixer.Sound( SOUND_BANG1 )
bang_sound2 = pygame.mixer.Sound( SOUND_BANG2 )

# Set the base volume for all sounds
move_up_sound.set_volume(0.5)
move_down_sound.set_volume(0.5)
collision_sound.set_volume(0.3)
rocket_sound.set_volume(0.1)
bang_sound1.set_volume(.3)
bang_sound2.set_volume(.6)

# Create our 'player'
player1 = characters.Player( move_up_sound, move_down_sound, virtualScreen)
scoreboard = characters.ScoreBoard( scoreScreen )

# Create groups to hold enemy sprites, cloud sprites, and all sprites
# - enemies is used for collision detection and position updates
# - clouds is used for position updates
# - all_sprites isused for rendering
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
booms = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player1)
all_sprites.add( scoreboard )
# Variable to keep our main loop running
running = True
# Our main loop
pygame.mixer.music.stop()
displaygrid = False

# Create custom events for adding a new enemy and cloud
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 1250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

about = aboutDialog.aboutDialog(screen, clock)
result = about.doModal()
if result != "play":
    exit(0)

multiGun = False
middleBullet = False
while running:
    # Look at every event in the queue
    mylist = pygame.sprite.groupcollide(bullets, enemies, True, False)
    for entity in mylist:
        #print( "BLB  : " + str(entity) )
        bonus = 0
        shippoints = 0
        for enemy in mylist[entity]:
            # Test, just in case this enemy has already been killed
            if enemy.alive():
                enemy.health -= 1
                stats.hit( enemy )
                #print( "BLE: " + str(enemy) )
                if enemy.health <= 0: 
                    cntr = -1 # Ignore current one
                    for finder in enemies:
                        if finder.squadName == enemy.squadName:
                            cntr += 1
                    #print(f" Destroyed: {enemy.squadName}-{enemy.callSign}  Remaining: {cntr}" )
                    if cntr <= 0:
                        print(f"\t\tDestroyed: {enemy.squadName} {enemy.bonusPoints} extra points awarded!!" )
                        bonus += enemy.bonusPoints
                        cntr += 1

                    print(f"{enemy.squadName}-{enemy.callSign} blasted out of the sky {-enemy.health}" )

                    stats.markKIA( enemy )
                    enemy.kill()
                    shippoints += enemy.points
                    if enemy.ship == characters.EnemyShipType.LARGE_SHIP:
                        bang_sound2.play()
                    else:
                        bang_sound1.play()
                else:
                    bang_sound1.play()
        stats.awardBonus( bonus )
        stats.points += shippoints + bonus
        rocket_sound.stop()
        new_boom = characters.Boom( characters.CollisionType.MISSLE, entity.rect, bonus + shippoints )
        booms.add(new_boom)
        all_sprites.add(new_boom)
         
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:

            x, y = event.pos
            for e in enemies:
                biggerrect = pygame.Rect( e.rect )
                biggerrect.inflate_ip( 5, 5 )
                if biggerrect.collidepoint( x, y ):
                    print( e )
                
            print(f"Mouse!, {x},{y}")
                
            new_bullet = characters.Bullet(player1, rocket_sound, virtualScreen, int(y - player1.rect.centery )/(2*(20+15)) )
            
            bullets.add( new_bullet )
            all_sprites.add( new_bullet )
            stats.fire()

        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop
            if event.key == K_ESCAPE:
                running = False
            # Was it the g key? If so toggle grid
            if event.key == K_g:
                displaygrid = not displaygrid
            if event.key == K_b:
                middleBullet = not middleBullet

            if event.key == K_f:
                multiGun = not multiGun
            # Was it the Escape key? If so, stop the loop
            if event.key == K_m:
                pygame.mixer.music.stop()
            if event.key == K_k: # Added this just for eli
                for e in enemies:
                    # Add an explosion
                    new_boom = characters.Boom( characters.CollisionType.MISSLE, e.rect, 0 )
                    booms.add(new_boom)
                    all_sprites.add(new_boom)
                    stats.markKIA( e )
                    e.kill()
            if event.key == K_SPACE:
                player1.shots_fired += 1
                if multiGun:
                    new_bullet = characters.Bullet(player1, rocket_sound, virtualScreen, 0 )
                    new_bullet.rect.move_ip(0,16)
                    bullets.add( new_bullet )
                    all_sprites.add( new_bullet )
                    stats.fire()

                    new_bullet = characters.Bullet(player1, rocket_sound, virtualScreen, 0 )
                    new_bullet.rect.move_ip(0,-16)
                    bullets.add( new_bullet )
                    all_sprites.add( new_bullet )
                    stats.fire()
                if middleBullet or not multiGun:
                    new_bullet = characters.Bullet(player1, rocket_sound, virtualScreen, 0 )
                    bullets.add( new_bullet )
                    all_sprites.add( new_bullet )
                    stats.fire()


        # Did the user click the window close button? If so, stop the loop
        elif event.type == QUIT:
            running = False          

        # Should we add a new enemy?
        elif event.type == ADDENEMY:
            if player1.health > 0:
                squadron = characters.Squadron( virtualScreen )
                i = random.randint(1,7)
                if i == 1:
                    squadron.createSquadronLarge( enemies, all_sprites )
                elif i == 2:
                    squadron.createSquadronMiddle( enemies, all_sprites )
                elif i == 3:
                    squadron.createSquadronFluidFour( enemies, all_sprites )
                elif i == 4:
                    squadron.createSquadronBattleSpread( enemies, all_sprites )
                elif i == 5:
                    squadron.createSquadronK( enemies, all_sprites )
                elif i == 6:
                    squadron.createSquadronF( enemies, all_sprites )
                else:
                    squadron.createSquadronTiny( enemies, all_sprites )
                
        # Should we add a new cloud?
        elif event.type == ADDCLOUD:
            if player1.health > 0:
                # Create the new cloud, and add it to our sprite groups
                new_cloud = characters.Cloud( virtualScreen )
                clouds.add(new_cloud)
                all_sprites.add(new_cloud)

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    player1.update(pressed_keys)
    # Update the position of our enemies and clouds
    enemies.update()
    clouds.update()
    booms.update()
    bullets.update()

    # Fill the screen with sky blue
    screen.fill((135, 206, 250))
    img = pygame.image.load( "resources/scene.png" ).convert()
    rect = pygame.Rect( virtualScreen )
    screen.blit( img, rect )

    # Check if any enemies have collided with the player
    #collisions = pygame.sprite.spritecollide(player1, enemies )
    if pygame.sprite.spritecollideany(player1, enemies):
        c = pygame.sprite.spritecollideany(player1, enemies)
        print(f"{c.squadName}-{c.callSign} destroyed in mid air collision {-c.health}" )
        stats.markKIA( c )
        c.kill()

        # Stop any moving sounds and play the collision sound
        move_up_sound.stop()
        move_down_sound.stop()
        rocket_sound.stop()
        collision_sound.play()

        # Add an explosion
        new_boom = characters.Boom( characters.CollisionType.PLAYER, player1.rect, 0 )
        booms.add(new_boom)
        all_sprites.add(new_boom)

        player1.health -= c.health

    # Stop the loop
    if player1.health <= 0 and player1.rect.bottom > virtualScreen.bottom-player1.rect.height-scoreScreen.bottom:
        for b in bullets:
            b.kill()
        result = about.doModal( str( stats.getPoints() ))
        if result == "play":
            resetGame()
            for event in pygame.event.get():
                pass
        else:
            running = False           

    scoreboard.draw( player1.health, player1.shots_fired, stats.hits, stats.getPoints() )


    if displaygrid:
        drawGrid( virtualScreen )

    # Draw all our sprites

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    pygame.display.flip()

    # Ensure we maintain a 30 frames per second rate
    clock.tick(30)

# At this point, we're done, so we can stop and quit the mixer
pygame.mixer.music.stop()
pygame.mixer.quit()
print( stats )
