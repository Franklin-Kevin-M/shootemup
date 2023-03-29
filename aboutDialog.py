import pygame
import characters

from pygame.locals import (K_p, K_ESCAPE, KEYDOWN, MOUSEBUTTONDOWN, RLEACCEL, K_KP_ENTER)

class ShipAndPoints(characters.SquadShip):
    def __init__(self, virtualScreen, shipType, location, xr, xalign):
        super().__init__(virtualScreen, shipType, location, 5, xr, 2)
        self.rect.left = xalign - self.rect.width

class PointsText():
    def __init__(self, ship, color):
        font = pygame.font.SysFont("couriernew", 24, bold=True)
        self.surf = font.render(f' = {ship.points} points', True, color)
        self.rect = pygame.Rect(0, 0, self.surf.get_width(), self.surf.get_height())
        self.rect.left = ship.rect.right
        self.rect.top = ship.rect.centery - self.surf.get_height()/2


class aboutDialog(pygame.sprite.Sprite):
    def __init__(self, screen, clock):
        super().__init__()
        self.clock = clock
        self.screen = screen
        self.ships = []
        aSCREEN_WIDTH, aSCREEN_HEIGHT = pygame.display.get_surface().get_size()
        virtualScreen = pygame.Rect(0, 0, aSCREEN_WIDTH, aSCREEN_HEIGHT)

        self.surf = pygame.image.load( characters.imageResources.GAME_BACKGROUND).convert()

        smallShip = ShipAndPoints( virtualScreen, characters.EnemyShipType.SMALL_SHIP, (0, 25), False, 150)
        self.ships.append(smallShip)
        self.ships.append(PointsText(smallShip, "Orange"))

        smallShip = ShipAndPoints( virtualScreen, characters.EnemyShipType.SMALL_SHIP, (0, 25), True, aSCREEN_WIDTH-300)
        self.ships.append(smallShip)
        self.ships.append(PointsText(smallShip, "Blue"))

        mediumShip = ShipAndPoints( virtualScreen, characters.EnemyShipType.MEDIUM_SHIP, (0, 80), False, 150)
        self.ships.append(mediumShip)
        self.ships.append(PointsText(mediumShip, "Orange"))
        mediumShip = ShipAndPoints(virtualScreen, characters.EnemyShipType.MEDIUM_SHIP, (0, 80), True, aSCREEN_WIDTH-300)
        self.ships.append(mediumShip)
        self.ships.append(PointsText(mediumShip, "Blue"))

        largeShip = ShipAndPoints( virtualScreen, characters.EnemyShipType.LARGE_SHIP, (0, 140), False, 150)
        self.ships.append(largeShip)
        self.ships.append(PointsText(largeShip, "Orange"))
        largeShip = ShipAndPoints( virtualScreen, characters.EnemyShipType.LARGE_SHIP, (0, 140), True, aSCREEN_WIDTH-300)
        self.ships.append(largeShip)
        self.ships.append(PointsText(largeShip, "Blue"))

        playerShip = ShipAndPoints( virtualScreen, characters.EnemyShipType.PLAYER_SHIP, (0, 220), False, 500)
        self.ships.append(playerShip)

        self.sandoval = pygame.font.SysFont("sandoval", 72, bold=True)
        self.textfont = pygame.font.SysFont("freemono", 32, bold=True)

    def doModal(self, message=""):
        running = True
        while running:
            for event in pygame.event.get():
                # Did the user hit a key?
                if event.type == KEYDOWN:
                    if event.key == K_p or event.key == K_KP_ENTER:
                        return "play"
                    if event.key == K_ESCAPE:
                        running = False
                if event.type == MOUSEBUTTONDOWN:
                    return "play"
            self.screen.fill((135, 206, 250))
            self.screen.blit(self.surf, self.screen.get_rect())

            score_text1 = self.sandoval.render(f'Blasters', True, "blue")
            x, y = self.screen.get_size()
            self.screen.blit( score_text1, (x/2-score_text1.get_width()/2, score_text1.get_height() * 1.4))

            for s in self.ships:
                self.screen.blit(s.surf, s.rect)

            i = 3
            if message != "":
                score_text1 = self.textfont.render( f'SCORE: {message}', True, "BLUE")
                self.screen.blit( score_text1, (x/2-score_text1.get_width()/2, 75*i))
            txtary = ['Destroy the evil fleet using the space bar to fire.',
                      'Points are awarded for each ship destroyed.',
                      'Additional points awarded for destroying entire squadrons.',
                      '[g=toggle grid, k=wipeout ships, up/down/left/right=move]']
            i = 5
            for txt in txtary:
                score_text1 = self.textfont.render( txt, True, "white")
                self.screen.blit(score_text1, (100, 75*i))
                i+=1

            i += 1
            score_text1 = self.textfont.render('Press "P" or click mouse to play.  ESC exits', True, "red")
            self.screen.blit(score_text1, (x/2-score_text1.get_width()/2, 75*i))

            pygame.display.flip()

            # Nuthin's moving so 1 frame per second rate is fine
            self.clock.tick(1)

        return "quit"

if __name__ == "__main__":
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()

    about = aboutDialog(screen, clock)
    result = about.doModal("Tester")
    print(result)
