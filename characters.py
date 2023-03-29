import pygame
# Import random for random numbers
import random
import enum

from pygame.locals import (
    RLEACCEL, K_UP, K_DOWN, K_LEFT, K_RIGHT
)

greek = [ "Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta", "Theta", "Iota", "Kappa", "Lambda", "Mu", "Nu", "Xi", "Omicron", 
         "Pi", "Rho", "Sigma", "Tau", "Upsilon", "Phi", "Chi", "Psi", "Omega"]

class imageResources:
    CLOUD_IMAGE_FILE = "resources/cloud.png"
    ENEMY_IMAGE1_FILE = "resources/attacker1.png"
    ENEMY_IMAGE2_FILE = "resources/attacker2.png"
    ENEMY_IMAGE3_FILE = "resources/attacker3.png"
    BOOM_IMAGE_FILE = 'resources/explosion{}.png'
    BULLET_IMAGE_FILE = "resources/missile.png"
    PLAYER_IMAGE_FILE = "resources/plane2.png"
    GAME_BACKGROUND = "resources/background.png"

class CharacterSprite( pygame.sprite.Sprite):
    def __init__(self, virtualScreen):
        super().__init__()
        self.virtualScreen = pygame.Rect(virtualScreen)
    def loadImageFile( self, file, shipSize ):
        img = pygame.image.load( file )
        if shipSize != 1:
            sz = img.get_size()
            img = pygame.transform.scale(img, (int(sz[0]*shipSize), int(sz[1]*shipSize)))
        self.surf = img.convert()
        transColor = self.surf.get_at((0,0))
        self.surf.set_colorkey(transColor, RLEACCEL)
        #pygame.draw.rect(self.surf, "red", self.surf.get_rect(), 1)
        

# Define the cloud object extending pygame.sprite.Sprite
# Use an image for a better looking sprite
class Cloud(CharacterSprite):
    def __init__(self, virtualScreen ):
        super().__init__(virtualScreen)
        self.speed = -5 
        img = pygame.image.load( imageResources.CLOUD_IMAGE_FILE )
        sz = img.get_size()
        asize = random.random() * 2.0
        if asize < 0.25:
            asize = 1.00
        img = pygame.transform.scale(img, (int(sz[0]*asize), int(sz[1]*asize)))
        self.surf = img.convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(self.virtualScreen.width + 20, self.virtualScreen.width + 100),
                random.randint(self.virtualScreen.top+int(img.get_height()/2), self.virtualScreen.height),
            )
        )

    # Move the cloud based on a constant speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class EnemyShipType(enum.IntEnum):
    PLAYER_SHIP  = 0
    SMALL_SHIP  = 1
    MEDIUM_SHIP = 3
    LARGE_SHIP = 5

class Squadron(CharacterSprite):
    def __init__(self, virtualScreen ):
        super().__init__(virtualScreen)
    def createSquadronLarge(self, enemies, all_sprites ):
        ary = [ [EnemyShipType.LARGE_SHIP,  0,   0] ]

        r = random.randint(1, 3)
        for k in range(1, r):
            ary.append( [EnemyShipType.MEDIUM_SHIP, 30*k, 20*k])
            ary.append( [EnemyShipType.MEDIUM_SHIP, 30*k, -20*k])
        self.createSquadronArray( enemies, all_sprites, ary, "LargeSquadron")
    def createSquadronMiddle(self, enemies, all_sprites ):
        ary = [ [EnemyShipType.MEDIUM_SHIP,  0,   0] ]
               
        r = random.randint(1, 5)
        for k in range(1, r):
            ary.append( [EnemyShipType.MEDIUM_SHIP, 25*k, 20*k])
            ary.append( [EnemyShipType.MEDIUM_SHIP, 25*k, -20*k])
        self.createSquadronArray( enemies, all_sprites, ary, "MiddleSquadron")
        
    def createSquadronBattleSpread(self, enemies, all_sprites ):          
        r = random.randint(1,3)
        yd = 20
        shiptype = EnemyShipType.SMALL_SHIP
        if r == 2:
            yd = 30
            shiptype = EnemyShipType.MEDIUM_SHIP 
        if r == 3:
            yd = 35
            shiptype = EnemyShipType.LARGE_SHIP 
        ary =     [ ]
        for k in range(0, 4):
            ary.append( [shiptype, 0, yd*k])
        self.createSquadronArray( enemies, all_sprites, ary, "BattleSpread")

    def createSquadronF(self, enemies, all_sprites ):
        r = random.randint(1,3)
        xd = 25
        yd = 20
        shiptype = EnemyShipType.SMALL_SHIP
        if r == 2:
            xd = 35
            yd = 30
            shiptype = EnemyShipType.MEDIUM_SHIP 
        if r == 3:
            xd = 40
            yd = 35
            shiptype = EnemyShipType.LARGE_SHIP 
        ary =     [ [shiptype,  0,   0] ]
        ary.append( [shiptype,  0, yd*1])
        ary.append( [shiptype,  0, yd*2])
        ary.append( [shiptype,  0, yd*3])
        ary.append( [shiptype,  0, yd*4])
        ary.append( [shiptype, xd*1, yd*2])
        ary.append( [shiptype, xd*2, yd*2])
        ary.append( [shiptype, xd*1,   0])
        ary.append( [shiptype, xd*2,   0])
        ary.append( [shiptype, xd*3,   0])
        self.createSquadronArray( enemies, all_sprites, ary, "FSquadron")
    def createSquadronK(self, enemies, all_sprites ):
        r = random.randint(1,3)
        xd = 25
        yd = 20
        shiptype = EnemyShipType.SMALL_SHIP
        if r == 2:
            xd = 35
            yd = 30
            shiptype = EnemyShipType.MEDIUM_SHIP 
        if r == 3:
            xd = 40
            yd = 35
            shiptype = EnemyShipType.LARGE_SHIP 
        ary =     [ [shiptype,    0,   0] ]
        ary.append( [shiptype,    0,  yd*1])
        ary.append( [shiptype,    0,  yd*2])
        ary.append( [shiptype,    0,  yd*3])
        ary.append( [shiptype,    0,  yd*4])
        ary.append( [shiptype, xd*1,  yd*2])
        ary.append( [shiptype, xd*2,  yd*1])
        ary.append( [shiptype, xd*2,  yd*3])
        ary.append( [shiptype, xd*3,   0])
        ary.append( [shiptype, xd*3,  yd*4])
        self.createSquadronArray( enemies, all_sprites, ary, "SpecialKSquad")
    def createSquadronFluidFour(self, enemies, all_sprites ):
        r = random.randint(1,3)
        xd = 25
        yd = 20
        shiptype = EnemyShipType.SMALL_SHIP
        if r == 2:
            xd = 35
            yd = 30
            shiptype = EnemyShipType.MEDIUM_SHIP 
        if r == 3:
            xd = 40
            yd = 35
            shiptype = EnemyShipType.LARGE_SHIP 
        ary =     [ [shiptype,  0,   0] ]
        ary.append( [shiptype,  0,  yd])
        ary.append( [shiptype, xd,  yd*2])
        ary.append( [shiptype, xd, -yd])
        self.createSquadronArray( enemies, all_sprites, ary, "FluidFour")
    def createSquadronTiny( self, enemies, all_sprites ):
        ary = [ [EnemyShipType.SMALL_SHIP,  0,   0]]
        r = random.randint(1, 5)
        for k in range(1, r):
            ary.append( [EnemyShipType.SMALL_SHIP, 20*k, 15*k])
            ary.append( [EnemyShipType.SMALL_SHIP, 20*k, -15*k])
        self.createSquadronArray( enemies, all_sprites, ary, "TinySquadron")
    def calculateBonusPoints( self, ary, xr ):
        bonusPoints = 0
        for j in ary:
            if j[0] == EnemyShipType.SMALL_SHIP:
                bonusPoints += 10
            elif j[0] == EnemyShipType.MEDIUM_SHIP:
                bonusPoints += 30
            else:
                bonusPoints += 50
        if xr == 1: 
            # Double the points if its a hardened ship
            bonusPoints += bonusPoints
        return bonusPoints
    
    def createSquadronArray(self, enemies, all_sprites, ary, squadName ):
        y = random.randint( self.virtualScreen.top, self.virtualScreen.height+self.virtualScreen.top)
        speed = random.randint(6, 20)
        xr = random.randint(1,5)
        callsign = 1
        bonusPoints = self.calculateBonusPoints( ary, xr )
        squadName = squadName + "-" + str(5) + "-" + random.choice(greek)
        ships = []
        for j in ary:
            new_ss = SquadShip( self.virtualScreen, j[0], [self.virtualScreen.width+j[1], y+j[2]], speed, xr)
            new_ss.squadName = squadName 
            new_ss.callSign = str(callsign) + "-" + str(len(ary))
            callsign += 1
            new_ss.bonusPoints = bonusPoints
            ships.append( new_ss )
            enemies.add(new_ss)
            all_sprites.add(new_ss)
        
        # "Fix" the new ships that are outside the viewable range
        maxShift = 0
        for ship in ships:
            # These are to high and must move down
            if ship.rect.top < self.virtualScreen.top:
                dx = self.virtualScreen.top - ship.rect.top
                if abs( dx ) > abs( maxShift ):
                    maxShift = dx
            # These are to low and must move up
            if ship.rect.bottom > self.virtualScreen.bottom:
                dx = self.virtualScreen.bottom - ship.rect.bottom
                if abs( dx ) > abs( maxShift ):
                    maxShift = dx
        # If we have to shift any ship lets shift all ships to ensure all are in window
        if maxShift != 0:
            for ship in ships:
                ship.rect.move_ip( 0, maxShift )

class SquadShip(CharacterSprite):

    def __str__(self):
        s = f"Squad Ship: {self.squadName}-{self.callSign}, Type: {self.ship}, Speed: {self.speed}, Points: {self.points}, Health: {self.health}, Upgraded: {self.upgraded}\n\t"
        s = s + dumpRect( "Rectangle", self.rect) 
        return s

    def initImage(self, shipType, location, xr, shipSize=1):
        if shipType == EnemyShipType.PLAYER_SHIP:
            self.loadImageFile( imageResources.PLAYER_IMAGE_FILE, shipSize )
            self.health = 5
        if shipType == EnemyShipType.LARGE_SHIP:
            self.loadImageFile( imageResources.ENEMY_IMAGE3_FILE, shipSize )
            self.health = 5
        if shipType == EnemyShipType.MEDIUM_SHIP:
            self.loadImageFile( imageResources.ENEMY_IMAGE2_FILE, shipSize )
            self.health = 3
        if shipType == EnemyShipType.SMALL_SHIP:
            self.loadImageFile( imageResources.ENEMY_IMAGE1_FILE, shipSize )
            self.health = 1
        self.rect = pygame.Rect( location[0], location[1], self.surf.get_width(), self.surf.get_height())
        self.valid = True
        if xr == 1:
            self.xray( )
    def configure( self, shipType, speed, xr ):
        self.ship = shipType
        self.points = shipType * 10
        self.speed = speed
        self.upgraded = False
        if xr == 1:
            self.health += self.health
            self.speed += 5
            self.upgraded = True
            self.points += self.points

    def __init__(self, virtualScreen, shipType, location, speed, xr, shipSize=1 ):
        super().__init__(virtualScreen)
        self.initImage(shipType, location, xr, shipSize)
        self.configure( shipType, speed, xr)
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
    def xray( self ):
        sz = self.surf.get_size()
        blank = self.surf.get_at((0,0))
        for x in range( 0, sz[0]):
            for y in range( 0, sz[1]):
                t = self.surf.get_at((x,y)) 
                if t[0] == blank[0] and t[1] == blank[1] and t[2] == blank[2]:
                    pass
                else:
                    h0, h1, h2, h3 = t
                    t[0] = h2
                    t[1] = h1
                    t[2] = h0
                    self.surf.set_at((x,y),t )


class CollisionType(enum.Enum):
    MISSLE = 0
    PLAYER = 1

class Boom(pygame.sprite.Sprite ):
    def __init__(self, collisiontype, arect, bonus):
        super().__init__()
        self.images = []
        self.frame = 0
        for i in range(3):
            file = imageResources.BOOM_IMAGE_FILE.format(i)
            exp_img = pygame.image.load(file).convert()
            exp_img.set_colorkey((0, 0, 0), RLEACCEL)
            sz = exp_img.get_size()
            tsize = 0.75
            if collisiontype == CollisionType.MISSLE:
                if bonus > 0:
                    self.font = pygame.font.SysFont("couriernew", 50, bold=True)
                    score_text1 = self.font.render(f'+{bonus}', True, "RED")
                    exp_img.blit(score_text1, (5, 5))
                tsize = 0.35
            exp_img = pygame.transform.scale(exp_img, (int(sz[0]*tsize), int(sz[1]*tsize)))
            self.images.append( exp_img )
        self.rect = pygame.Rect(arect)
        self.rect.move_ip( -20, -20)

        self.surf = self.images[self.frame]
        self.lifespan = 0
        
    # Move the cloud based on a constant speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        if self.lifespan > 30:
            self.kill()
        self.lifespan += 1
        self.frame = int(self.lifespan/10)
        if self.frame > 2:
            self.frame = 2
        #self.rect.move_ip(self.speed, 0)
        self.surf = self.images[self.frame]



class Bullet(CharacterSprite):
    def __init__(self, player, rocket_sound, virtualScreen, vertspeed):
        super().__init__(virtualScreen)
        self.loadImageFile( imageResources.BULLET_IMAGE_FILE, 1 )
        # Flip the missel around
        self.surf = pygame.transform.rotate( self.surf, 180 - vertspeed )
        # The starting position is based on where the player is
        self.rect = pygame.Rect( self.surf.get_rect() )

        self.rect.top = ( player.rect.top + player.rect.bottom - self.surf.get_height() ) / 2
        self.rect.left = player.rect.right - self.surf.get_width()
        self.speed = 20
        self.vertspeed = vertspeed
        self.rocket_sound = rocket_sound
        self.rocket_sound.play()


    def __str__(self):
        s = dumpRect( "Bullet", self.rect) 
        s = s + f"\n\tSpeed: {self.speed}"
        return s

    # Move the enemy based on speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(self.speed, self.vertspeed)
        if self.rect.left > self.virtualScreen.width:
            self.kill()
            self.rocket_sound.stop()

#  limit a number to be within a certain range
def clamp_to_min_max( n, minn, maxn):
    if n < minn:
        return minn
    if n > maxn:
        return maxn
    return n    


# Define the Player object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Player(CharacterSprite):
    def __str__(self):
        s = dumpRect( "Player", self.rect) 
        s = s+ f"\n\tPlayer Health: {self.health}"
        return s

    def reset( self ):
        self.rect.left = 50
        self.rect.top = 200
        self.health = 10
        self.rotate = 0
        self.rotate_life = 0
        self.shots_fired = 0
        self.hits = 0
        self.rotate_life = 0
        self.surf = self.origional_surf    

    def __init__(self, up_sound, down_sound, virtualScreen):
        super().__init__(virtualScreen)
        self.loadImageFile( imageResources.PLAYER_IMAGE_FILE, 1 )
        self.rect = self.surf.get_rect()
        self.origional_surf = self.surf
        self.up_sound = up_sound
        self.down_sound = down_sound
        self.reset()

    # Move the sprite based on keypresses
    def update(self, pressed_keys):

        if self.health <= 0 :
            self.rect.move_ip(0, 5)
            self.rotate -= 15
            self.rotate_life = 100
        if pressed_keys[K_UP]:
            self.rotate += 5
            self.rect.move_ip(0, -5)
            self.rotate_life = 10
            self.up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            self.rotate -= 5
            self.rotate_life = 10
            self.down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
            self.rotate = 1
            self.rotate_life = 1
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
            self.rotate = 1
            self.rotate_life = 1

        self.rotate = clamp_to_min_max( self.rotate, -20, 20 )
            
        if self.rotate != 0:
            self.rotate_life -= 1
            if self.rotate_life > 0:
                self.surf = pygame.transform.rotate( self.origional_surf, self.rotate )
            else:
                self.surf = self.origional_surf
                self.rotate = 0
        

        # Keep player on the screen
        self.rect.left = clamp_to_min_max(self.rect.left, self.virtualScreen.left, self.virtualScreen.width)
        self.rect.right = clamp_to_min_max(self.rect.right, self.virtualScreen.left, self.virtualScreen.width)
        self.rect.top = clamp_to_min_max(self.rect.top, self.virtualScreen.top, self.virtualScreen.height+60)
        self.rect.bottom = clamp_to_min_max(self.rect.bottom, self.virtualScreen.top, self.virtualScreen.height+60)

# Define the ScoreBoard object extending pygame.sprite.Sprite
# Use an image for a better looking sprite
class ScoreBoard(CharacterSprite):
    def __init__(self, virtualScreen):
        super().__init__(virtualScreen)
        self.surf = pygame.Surface( [ virtualScreen.width, virtualScreen.height] )
        self.rect = pygame.Rect( virtualScreen )
        self.font = pygame.font.Font(None, 24)
        self.font = pygame.font.SysFont("couriernew", 24, bold=True)

    def draw(self, health, shots_fired, hits, points):
        pygame.draw.rect(self.surf, (131,139,139), self.virtualScreen, 0)
        pygame.draw.rect(self.surf, (119, 136, 153), self.virtualScreen, 5)
        pygame.draw.circle( self.surf, (0,0,0), (30,30), 15 )
        pygame.draw.circle( self.surf, (255,255,0), (30,30), 15, draw_top_right=True, draw_bottom_left=True )


        healthcolor = "darkgreen"
        if ( health <= 4 ):
            healthcolor = "red"
        score_text1 = self.font.render(f'Health: {health}', True, healthcolor)
        self.surf.blit(score_text1, (10, 10))
        if shots_fired > 0:
            score_text2 = self.font.render(f'   H/S: {hits}/{shots_fired} ({100*hits/shots_fired:.0f}%)', True, "darkgreen")
        else:
            score_text2 = self.font.render(f'   H/S: {hits}/{shots_fired} ({100:.0f}%)', True, "darkgreen")
        self.surf.blit(score_text2, (10, 30))
        score_text3 = self.font.render(f'Points: {points:,}', True, "darkgreen")
        
        self.surf.blit(score_text3, (self.virtualScreen.width - score_text3.get_width() - 20, 10))

    # Never move this 
    def update(self):
        return

def dumpRect(label, r):
    s = f"{label}: T/L: [{r.top}, {r.left}], B/R: [{r.bottom}, {r.right}], w/h: [{r.right-r.left}, {r.bottom-r.top}]"
    return s

class GameStats:
    def awardBonus( self, bonus):
        self.points += bonus
    def hit( self, ship ):
        self.hits += 1
    def markKIA( self, ship ):
        self.kills += 1
        self.points += ship.points
    def __init__(self):
        self.playershots = 0
        self.points = 0
        self.hits = 0
        self.kills = 0
    def getPoints( self ):
        return self.points
    def fire(self, count=1):
        self.playershots += count
    def __str__(self):
        result = f"Game Stats:\n\tPoints: {self.points}\n\tShots Fired: {self.playershots}\n\tHits: {self.hits}\n\tKills: {self.kills}"
        return result