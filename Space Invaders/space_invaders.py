import pygame
import random
from pygame.locals import K_r

class Spiller:
    def __init__(self, vindustørrelse):
        self.størrelse = 60
        self.x = vindustørrelse[0] // 2 - self.størrelse // 2
        self.y = vindustørrelse[1] - self.størrelse - 10
        self.fart = 5
        self.bilde = pygame.image.load("Pygame/Space Invaders/rakett.png")
        self.bilde = pygame.transform.scale(self.bilde, (self.størrelse, self.størrelse+30))

    def beveg(self, tastetrykk, vindustørrelse):
        if tastetrykk[pygame.K_LEFT]:
            self.x -= self.fart
        if tastetrykk[pygame.K_RIGHT]:
            self.x += self.fart

        if self.x <= -self.størrelse:
            self.x = vindustørrelse[0]
        elif self.x >= vindustørrelse[0]:
            self.x = 0

    def tegn(self, skjerm):
        skjerm.blit(self.bilde, (self.x, self.y))


class Fiende:
    def __init__(self, vindustørrelse):
        self.størrelse = 50
        self.fart = 2
        self.bilde = pygame.image.load("Pygame/Space Invaders/meteorite.png")
        self.bilde = pygame.transform.scale(self.bilde, (self.størrelse, self.størrelse))
        self.fiender = []

        for i in range(5):
            x = random.randint(0, vindustørrelse[0] - self.størrelse)
            y = random.randint(-150, -self.størrelse)
            self.fiender.append(pygame.Rect(x, y, self.størrelse, self.størrelse))

    def beveg(self, vindustørrelse):
        for fiende in self.fiender:
            fiende.y += self.fart
            if fiende.y > vindustørrelse[1]:
                fiende.y = random.randint(-150, -self.størrelse)
                fiende.x = random.randint(0, vindustørrelse[0] - self.størrelse)
                if len(liv.liv) > 0:
                    liv.mist_liv()
                else:
                    liv.tap()

    def tegn(self, skjerm):
        for fiende in self.fiender:
            skjerm.blit(self.bilde, fiende)

    def hent_posisjon(self):
        return self.x, self.y


class Skudd:
    def __init__(self, x, y):
        self.størrelse = 30
        self.x = x
        self.y = y
        self.fart = 7
        self.bilde = pygame.image.load("Pygame/Space Invaders/missile.png")
        self.bilde = pygame.transform.scale(self.bilde, (self.størrelse, self.størrelse+50))
        self.rekt = pygame.Rect(self.x, self.y, self.størrelse, self.størrelse)

    def beveg(self):
        self.y -= self.fart
        self.rekt.y = self.y

    def tegn(self, skjerm):
        skjerm.blit(self.bilde, (self.x-10, self.y))


class Liv:
    def __init__(self):
        self.størrelse = 70
        self.x = -20
        self.y = 20
        self.bilde = pygame.image.load("Pygame/Space Invaders/heart.png")
        self.bilde = pygame.transform.scale(self.bilde, (self.størrelse+80, self.størrelse))
        self.liv = []

        for i in range(3):
            self.liv.append(pygame.Rect(self.x + i * self.størrelse, self.y, self.størrelse, self.størrelse))
    
    def vis_liv(self, skjerm):
        for x in self.liv:
            skjerm.blit(self.bilde, x)

    def mist_liv(self):
        if len(self.liv) > 0:
            for x in self.liv:
                siste_liv = x
            self.liv.remove(siste_liv)

    def tap(self):
        tap_tekst = f"Du tapte!"
        tap_vis = font.render(tap_tekst, True, (50, 200, 50))
        skjerm.blit(tap_vis, (VINDU_STØRRELSE[0] // 2 - tap_vis.get_width() // 2, VINDU_STØRRELSE[1] // 2 - tap_vis.get_height() // 2))

        tap_tekst2 = f"Din poengsum ble: {poengsum}"
        tap_vis2 = font.render(tap_tekst2, True, (50, 200, 50))
        skjerm.blit(tap_vis2, (VINDU_STØRRELSE[0] // 2 - tap_vis2.get_width() // 2, VINDU_STØRRELSE[1] // 2 - tap_vis2.get_height() // 2 + tap_vis.get_height() ))

        tap_tekst3 = f"Trykk på r for å restarte"
        tap_vis3 = font.render(tap_tekst3, True, (50, 200, 50))
        skjerm.blit(tap_vis3, (VINDU_STØRRELSE[0] // 2 - tap_vis3.get_width() // 2, VINDU_STØRRELSE[1] // 2 - tap_vis3.get_height() // 2 + tap_vis.get_height() + tap_vis2.get_height()))


# Initialiserer PyGame
pygame.init()

# Oppretter et vindu
VINDU_STØRRELSE = (640, 480)
skjerm = pygame.display.set_mode(VINDU_STØRRELSE)
pygame.display.set_caption("Space Invaders by Sondre Indset")

# Laster inn bakgrunnsbilde
bakgrunnsbilde = pygame.image.load("Pygame/Space Invaders/space_background.png")
bakgrunnsbilde = pygame.transform.scale(bakgrunnsbilde, VINDU_STØRRELSE)


# Ytterste løkke, restart funksjon
while True:
    # Oppretter objektene
    spiller = Spiller(VINDU_STØRRELSE)
    fiender = Fiende(VINDU_STØRRELSE)
    skuddene = []
    liv = Liv()

    font = pygame.font.SysFont("Arial", 24) # Skrifttype og størrelse
    poengsum = 0

    # Oppretter klokketelleren
    klokke = pygame.time.Clock()

    # Starter hovedløkka
    run = True
    while run:
        # Håndterer hendelser
        for hendelse in pygame.event.get():
            if hendelse.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif hendelse.type == pygame.KEYDOWN:
                if hendelse.key == pygame.K_SPACE:
                    skudd = Skudd(spiller.x + spiller.størrelse // 2 - 7, spiller.y)
                    skuddene.append(skudd)

        # Tegner bakgrunnen
        skjerm.blit(bakgrunnsbilde, (0, 0))

        # Beveger og tegner spilleren
        tast = pygame.key.get_pressed()
        spiller.beveg(tast, VINDU_STØRRELSE)
        spiller.tegn(skjerm)

        # Beveger og tegner fiendene
        if len(liv.liv) > 0:
            fiender.beveg(VINDU_STØRRELSE)
            fiender.tegn(skjerm)

            # Oppretter en liste for skudd som skal fjernes
            skudd_fjernes = []

            # Beveger og tegner skuddene
            for skudd in skuddene:
                skudd.beveg()
                skudd.tegn(skjerm)

                for fiende in fiender.fiender:
                    if fiende.colliderect(skudd.rekt):
                        fiender.fiender.remove(fiende)
                        skudd_fjernes.append(skudd)  # Legger til skuddet i fjernelisten
                        ny_fiende = pygame.Rect(random.randint(0, VINDU_STØRRELSE[0] - fiender.størrelse), random.randint(-150, -fiender.størrelse), fiender.størrelse, fiender.størrelse)
                        fiender.fiender.append(ny_fiende)
                        poengsum += 1
                        break

                if skudd.y <= 0:
                    skudd_fjernes.append(skudd)  # Legger til skuddet i fjernelisten

            # Fjerner skuddene fra listen
            for skudd in skudd_fjernes:
                skuddene.remove(skudd)

            # Viser og oppdaterer liv
            liv.vis_liv(skjerm)

            # Viser og oppdaterer poengsum
            score_tekst = f"Poengsum: {poengsum}"  # Viser poengsummen øverst til venstre
            score_vis = font.render(score_tekst, True, (50, 200, 50))
            skjerm.blit(score_vis, (480, 40))
        else:
            liv.tap()
        
        # Starter spillet på nytt ved å restarte løkken
        if tast[K_r]:
            break

        # Oppdaterer skjermen
        pygame.display.update()

        # Begrenser oppdateringsfrekvensen
        klokke.tick(60)